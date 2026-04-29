#!/usr/bin/env python3
"""
tools/job-scraper.py — Weekly job discovery tool.

Sources:
  - Adzuna API  (EU/UK/India — free tier, 250 calls/day)
  - Reed API    (UK — free)
  - Remotive    (remote — no key needed)
  - Playwright  (company career pages — static list)

Output:
  job-tracker/new-this-week.md   — new roles not seen before
  job-tracker/seen.txt           — dedup registry (hashed title+company)

Setup:
  pip install requests playwright pyyaml
  playwright install chromium

API keys (optional — skip source if unset):
  export ADZUNA_APP_ID=...
  export ADZUNA_APP_KEY=...
  export REED_API_KEY=...

Usage:
  python tools/job-scraper.py
  python tools/job-scraper.py --dry-run      # print only, no file write
  python tools/job-scraper.py --no-browser   # skip Playwright
  python tools/job-scraper.py --source adzuna reed  # run specific sources only
"""

import os
import re
import sys
import time
import hashlib
import argparse
import requests
from datetime import date
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent
OUTPUT_FILE = REPO_ROOT / "job-tracker" / "new-this-week.md"
SEEN_FILE   = REPO_ROOT / "job-tracker" / "seen.txt"

# ── Config ────────────────────────────────────────────────────────────────────

ADZUNA_APP_ID  = os.environ.get("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY", "")
REED_API_KEY   = os.environ.get("REED_API_KEY", "")

INCLUDE_KEYWORDS = [
    "RTL", "VLSI", "chip design", "SoC", "silicon", "FPGA",
    "embedded", "firmware", "hardware engineer",
    "staff engineer", "principal engineer", "senior engineer",
    "LLM", "AI platform", "ML engineer", "machine learning", "AI hardware",
    "legal tech", "compliance automation",
    "fintech", "systems software",
]

EXCLUDE_KEYWORDS = ["intern", "graduate", "junior", "entry level", "entry-level"]

ADZUNA_COUNTRIES = {
    "gb": "United Kingdom",
    "de": "Germany",
    "nl": "Netherlands",
    "in": "India",
    "ch": "Switzerland",
}

ADZUNA_QUERIES = [
    "RTL engineer", "silicon engineer", "ML engineer",
    "embedded engineer", "AI engineer", "VLSI engineer",
]

REED_QUERIES = [
    "RTL engineer", "machine learning engineer",
    "embedded engineer", "silicon design",
]

REMOTIVE_CATEGORIES = ["software-dev", "data", "devops-sysadmin"]

COMPANY_CAREER_PAGES: dict[str, str] = {
    "Synopsys":    "https://www.synopsys.com/company/jobs.html",
    "Cadence":     "https://www.cadence.com/en_US/home/company/careers.html",
    "ARM":         "https://www.arm.com/company/careers",
    "Qualcomm":    "https://www.qualcomm.com/company/careers",
    "NVIDIA":      "https://www.nvidia.com/en-us/about-nvidia/careers/",
    "Intel":       "https://jobs.intel.com/",
    "Siemens EDA": "https://jobs.siemens.com/jobs?experience=Experienced+Professional&domain=EDA",
    "Infineon":    "https://www.infineon.com/cms/en/careers/",
    "NXP":         "https://www.nxp.com/company/careers",
    "IBM Research":"https://www.ibm.com/careers/search?field_keyword_08[0]=Research",
}

RATE_LIMIT_SECS = 5


# ── Utilities ─────────────────────────────────────────────────────────────────

def role_hash(title: str, company: str) -> str:
    key = f"{title.lower().strip()}|{company.lower().strip()}"
    return hashlib.md5(key.encode()).hexdigest()[:12]


def load_seen() -> set[str]:
    if SEEN_FILE.exists():
        return set(SEEN_FILE.read_text().splitlines())
    return set()


def save_seen(seen: set[str]):
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text("\n".join(sorted(seen)))


def is_relevant(title: str) -> bool:
    tl = title.lower()
    if any(kw.lower() in tl for kw in EXCLUDE_KEYWORDS):
        return False
    return any(kw.lower() in tl for kw in INCLUDE_KEYWORDS)


def normalize(role: dict) -> dict:
    return {
        "title":    role.get("title", "").strip(),
        "company":  role.get("company", "Unknown").strip(),
        "location": role.get("location", "").strip(),
        "url":      role.get("url", "").strip(),
        "source":   role.get("source", "unknown"),
        "date":     role.get("date", str(date.today())),
    }


# ── Adzuna ────────────────────────────────────────────────────────────────────

def fetch_adzuna() -> list[dict]:
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        print("  [Adzuna] ADZUNA_APP_ID / ADZUNA_APP_KEY not set — skipping")
        return []

    roles = []
    for code, country_name in ADZUNA_COUNTRIES.items():
        for query in ADZUNA_QUERIES:
            try:
                r = requests.get(
                    f"https://api.adzuna.com/v1/api/jobs/{code}/search/1",
                    params={
                        "app_id": ADZUNA_APP_ID,
                        "app_key": ADZUNA_APP_KEY,
                        "what": query,
                        "results_per_page": 20,
                        "content-type": "application/json",
                    },
                    timeout=10,
                )
                r.raise_for_status()
                for job in r.json().get("results", []):
                    roles.append({
                        "title":    job.get("title", ""),
                        "company":  job.get("company", {}).get("display_name", ""),
                        "location": job.get("location", {}).get("display_name", country_name),
                        "url":      job.get("redirect_url", ""),
                        "source":   f"Adzuna/{code.upper()}",
                        "date":     job.get("created", str(date.today()))[:10],
                    })
                time.sleep(RATE_LIMIT_SECS)
            except Exception as e:
                print(f"  [Adzuna/{code}] '{query}': {e}", file=sys.stderr)

    print(f"  Adzuna: {len(roles)} raw roles")
    return roles


# ── Reed ──────────────────────────────────────────────────────────────────────

def fetch_reed() -> list[dict]:
    if not REED_API_KEY:
        print("  [Reed] REED_API_KEY not set — skipping")
        return []

    roles = []
    for query in REED_QUERIES:
        try:
            r = requests.get(
                "https://www.reed.co.uk/api/1.0/search",
                params={"keywords": query, "resultsToTake": 20},
                auth=(REED_API_KEY, ""),
                timeout=10,
            )
            r.raise_for_status()
            for job in r.json().get("results", []):
                roles.append({
                    "title":    job.get("jobTitle", ""),
                    "company":  job.get("employerName", ""),
                    "location": job.get("locationName", "UK"),
                    "url":      job.get("jobUrl", ""),
                    "source":   "Reed/UK",
                    "date":     str(date.today()),
                })
            time.sleep(RATE_LIMIT_SECS)
        except Exception as e:
            print(f"  [Reed] '{query}': {e}", file=sys.stderr)

    print(f"  Reed: {len(roles)} raw roles")
    return roles


# ── Remotive ──────────────────────────────────────────────────────────────────

def fetch_remotive() -> list[dict]:
    roles = []
    for category in REMOTIVE_CATEGORIES:
        try:
            r = requests.get(
                f"https://remotive.com/api/remote-jobs?category={category}&limit=50",
                timeout=10,
            )
            r.raise_for_status()
            for job in r.json().get("jobs", []):
                if is_relevant(job.get("title", "")):
                    roles.append({
                        "title":    job.get("title", ""),
                        "company":  job.get("company_name", ""),
                        "location": "Remote",
                        "url":      job.get("url", ""),
                        "source":   "Remotive",
                        "date":     job.get("publication_date", str(date.today()))[:10],
                    })
            time.sleep(RATE_LIMIT_SECS)
        except Exception as e:
            print(f"  [Remotive] '{category}': {e}", file=sys.stderr)

    print(f"  Remotive: {len(roles)} raw relevant roles")
    return roles


# ── Playwright (company career pages) ────────────────────────────────────────

def fetch_company_pages() -> list[dict]:
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print("  [Playwright] Not installed — skipping company pages")
        print("  To enable: pip install playwright && playwright install chromium")
        return []

    roles = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for company, url in COMPANY_CAREER_PAGES.items():
            try:
                print(f"  Scraping {company}...", end="", flush=True)
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(2000)

                base_domain = "/".join(url.split("/")[:3])
                links = page.query_selector_all("a[href]")
                found = 0
                for link in links:
                    try:
                        text = (link.inner_text() or "").strip()
                        href = link.get_attribute("href") or ""
                        if not (5 <= len(text) <= 150):
                            continue
                        if not is_relevant(text):
                            continue
                        full_url = href if href.startswith("http") else f"{base_domain}{href}"
                        roles.append({
                            "title":    text,
                            "company":  company,
                            "location": "See listing",
                            "url":      full_url,
                            "source":   f"careers/{company}",
                            "date":     str(date.today()),
                        })
                        found += 1
                    except Exception:
                        continue
                print(f" {found} roles")
                time.sleep(RATE_LIMIT_SECS)
            except PWTimeout:
                print(f" timeout", file=sys.stderr)
            except Exception as e:
                print(f" error: {e}", file=sys.stderr)

        browser.close()

    print(f"  Company pages: {len(roles)} raw roles")
    return roles


# ── Output ────────────────────────────────────────────────────────────────────

def write_output(new_roles: list[dict], dry_run: bool):
    if not new_roles:
        print("\nNo new roles found this week.")
        return

    if dry_run:
        print(f"\n[DRY RUN] {len(new_roles)} new roles:\n")
        for r in new_roles:
            print(f"  [{r['source']}] {r['title']} @ {r['company']} — {r['location']}")
            print(f"    {r['url']}")
        return

    today = str(date.today())
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    by_source: dict[str, list] = {}
    for r in new_roles:
        by_source.setdefault(r["source"], []).append(r)

    lines = [
        f"# New Roles — {today}\n\n",
        f"{len(new_roles)} new roles across {len(by_source)} sources.\n\n",
        "---\n",
    ]
    for source, roles in sorted(by_source.items()):
        lines.append(f"\n## {source} ({len(roles)})\n\n")
        for r in roles:
            lines.append(f"- **{r['title']}** @ {r['company']} — {r['location']}\n")
            lines.append(f"  {r['url']}\n")

    OUTPUT_FILE.write_text("".join(lines))
    print(f"\nWrote {len(new_roles)} new roles → {OUTPUT_FILE.relative_to(REPO_ROOT)}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Weekly job discovery scraper")
    parser.add_argument("--dry-run",    action="store_true", help="Print roles without writing file")
    parser.add_argument("--no-browser", action="store_true", help="Skip Playwright company page scraping")
    parser.add_argument("--source",     nargs="+",
                        choices=["adzuna", "reed", "remotive", "company"],
                        help="Run only specified sources (default: all)")
    args = parser.parse_args()

    sources = set(args.source) if args.source else {"adzuna", "reed", "remotive", "company"}
    seen    = load_seen()
    all_roles: list[dict] = []

    if "adzuna" in sources:
        print("Fetching Adzuna (EU/UK/India/CH)...")
        all_roles.extend(fetch_adzuna())

    if "reed" in sources:
        print("Fetching Reed (UK)...")
        all_roles.extend(fetch_reed())

    if "remotive" in sources:
        print("Fetching Remotive (remote)...")
        all_roles.extend(fetch_remotive())

    if "company" in sources and not args.no_browser:
        print("Fetching company career pages...")
        all_roles.extend(fetch_company_pages())

    # Normalize → filter → deduplicate
    normalized = [normalize(r) for r in all_roles]
    relevant   = [r for r in normalized if r["title"] and is_relevant(r["title"])]

    new_roles: list[dict] = []
    new_hashes: set[str]  = set()
    for r in relevant:
        h = role_hash(r["title"], r["company"])
        if h not in seen and h not in new_hashes:
            new_roles.append(r)
            new_hashes.add(h)

    print(f"\nTotal: {len(all_roles)} fetched → {len(relevant)} relevant → {len(new_roles)} new")

    write_output(new_roles, dry_run=args.dry_run)

    if not args.dry_run and new_hashes:
        save_seen(seen | new_hashes)


if __name__ == "__main__":
    main()
