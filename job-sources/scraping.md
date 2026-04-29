# Job Discovery: Scraping vs. APIs — Analysis & Recommendation

## TL;DR

**Best approach for you**: Use official APIs where they exist (LinkedIn, Indeed) + lightweight scraping for company career pages that have no API. Build a simple Python script that runs weekly, deduplicates results, and writes new roles directly to `job-tracker/applications.md`.

---

## Option Comparison

| Method | Cost | Reliability | Legal risk | Best for |
|--------|------|-------------|------------|---------|
| Official job board APIs | Free–$300/mo | High | None | LinkedIn, Indeed, Glassdoor |
| Puppeteer/Playwright scraping | ~$0 (self-hosted) | Medium (breaks on DOM changes) | Medium (ToS grey area) | Company career pages |
| Commercial scraping APIs | $50–$500/mo | High | Handled by provider | Aggregators at scale |
| RSS feeds | Free | Low (few sites still offer) | None | Limited; some boards still support |
| Email alerts + parser | Free | Medium | None | Good complement |

---

## Official APIs (use these first)

### LinkedIn Jobs API
- **Access**: Requires LinkedIn partner application — not open to individuals, only approved partners
- **Workaround**: LinkedIn has a "Job Search" URL structure you can parameterize:
  ```
  https://www.linkedin.com/jobs/search/?keywords=RTL+engineer&location=Switzerland&f_TPR=r604800
  ```
  Automate with Playwright (headless browser) logged in as yourself — low risk since it's your own account
- **Cost**: $0 if self-hosted

### Indeed Publisher API / Indeed Hire
- **Access**: indeed.com/publisher — free for job seekers, requires approval
- **Endpoint**: `http://api.indeed.com/ads/apisearch?publisher=YOUR_ID&q=RTL+engineer&l=Zurich`
- **Cost**: Free (ad-supported)
- **Limit**: 25 results per call, 500 calls/day

### Glassdoor API
- **Access**: partner program — individual access not available
- **Alternative**: scrape job listings (less data than LinkedIn)

### Adzuna API
- **Access**: Open — free tier available at developer.adzuna.com
- **Coverage**: UK, Germany, Netherlands, India, Switzerland (good EU coverage)
- **Cost**: Free tier = 250 calls/day; $0/mo
- **Best for**: EU + UK aggregation
- ```python
  GET https://api.adzuna.com/v1/api/jobs/{country}/search/1
    ?app_id=YOUR_ID&app_key=YOUR_KEY&what=RTL+engineer&where=Zurich
  ```

### Reed API (UK)
- **Access**: Open — free at reed.co.uk/developers/jobseeker
- **Coverage**: UK-only
- **Cost**: Free
- **Best for**: UK roles

### The Muse API
- **Access**: Open and free
- **Coverage**: Global but US-heavy
- **Cost**: Free

### Remotive API
- **Access**: Open — https://remotive.com/api/remote-jobs
- **Coverage**: Remote roles only
- **Cost**: Free

---

## Scraping — Company Career Pages

For companies with no API (Synopsys, Cadence, ARM, Qualcomm, etc.), scrape their careers pages directly.

### Tools
| Tool | Use case | Cost |
|------|---------|------|
| Playwright (Python) | Headless browser; handles JS-rendered pages | Free (self-hosted) |
| BeautifulSoup + requests | Static HTML pages | Free |
| Scrapy | Large-scale crawling | Free |
| Bright Data / Oxylabs | Managed proxies for scale | $50–200/mo |
| ScrapingBee | Managed scraper API | Free tier: 1,000 credits; $49/mo for 150k |
| Apify | Managed scraping platform | Free tier: $5/mo equivalent |

### Recommended scraping targets (career pages with stable structure)
```python
targets = {
    "synopsys": "https://synopsys.com/company/jobs.html",
    "cadence": "https://cadence.com/en_US/home/company/careers.html",
    "arm": "https://arm.com/company/careers",
    "qualcomm": "https://qualcomm.com/company/careers",
    "siemens_eda": "https://jobs.siemens.com/eda",
    "infineon": "https://infineon.com/cms/en/careers",
    "nxp": "https://nxp.com/company/careers",
    "ibm_zurich": "https://research.ibm.com/labs/zurich",
}
```

---

## Commercial Data Providers (if you want scale)

| Provider | What you get | Cost |
|----------|-------------|------|
| Coresignal | Job postings DB, refreshed daily | $300–1000/mo |
| People Data Labs | Company + job data | $0 for 1k records/mo free tier |
| Diffbot | Structured data from any page | $299/mo |
| Bright Data Datasets | Bulk LinkedIn/Indeed snapshots | $500+/mo |
| Jobspikr | Aggregated job feeds | $99/mo starter |

**Verdict**: Overkill for personal job search. Skip.

---

## Recommended Setup (free, effective, yours to own)

### Architecture
```
weekly_cron.py
  → calls Adzuna API (EU/UK/India)
  → calls Indeed API (global)
  → calls Reed API (UK)
  → Playwright scrapes 10 company career pages
  → deduplicates by title+company
  → filters by keywords (your role targets)
  → appends new roles to job-tracker/applications.md
  → sends you a summary email or writes to a new file: job-tracker/new-this-week.md
```

### Keyword filters (customize)
```python
INCLUDE_KEYWORDS = [
    "RTL", "VLSI", "chip design", "SoC", "embedded",
    "staff engineer", "principal engineer",
    "LLM", "AI platform", "ML engineer",
    "legal tech", "compliance", "fintech",
    "Python", "systems software"
]
EXCLUDE_KEYWORDS = ["intern", "graduate", "junior"]
LOCATIONS = ["Switzerland", "UK", "United Kingdom", "Germany",
             "Netherlands", "India", "Bangalore", "Remote"]
```

### Cost
- APIs: $0 (free tiers)
- Hosting: $0 if run locally on a cron job, or ~$5/mo on a VPS
- Total: **$0–$5/month**

---

## Legal / ToS Notes

- **LinkedIn scraping**: violates ToS. Using your own session for personal job search is low practical risk but not endorsed.
- **Indeed API**: fully authorized
- **Adzuna API**: fully authorized
- **Company career pages**: generally fine for personal use; don't hammer at high rate
- **Rule of thumb**: If there's an official API, use it. If scraping, be polite (rate-limit to 1 req/5s, honor robots.txt).

---

## Scraper is built ✓

`tools/job-scraper.py` — Adzuna + Reed + Remotive APIs + Playwright for 10 company career pages.
Output: `job-tracker/new-this-week.md` + `job-tracker/seen.txt` (dedup registry).
Automated weekly via `.github/workflows/weekly-scraper.yml` (Monday 08:00 UTC).

```bash
python tools/job-scraper.py --dry-run        # preview without writing
python tools/job-scraper.py --no-browser     # skip Playwright
python tools/job-scraper.py --source adzuna  # one source only
```

Set `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `REED_API_KEY` as GitHub repo secrets to activate the cron.
