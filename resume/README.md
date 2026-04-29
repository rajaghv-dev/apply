# Resume / CV

## Strategy

Don't use one resume. Use clusters — one master, then tailored per role type.

| Cluster | Target roles | Key emphasis |
|---------|-------------|-------------|
| Hardware | Chip design, EDA, VLSI | RTL, VLSI, SoC, DFT |
| AI/Systems | AI platform, ML infra | LLM, agents, systems software |
| Legal Tech | Legal AI, RegTech | Compliance, NLP, domain knowledge |
| FinTech | Finance AI, quant | Risk, financial systems, Python |
| Generalist | Staff/Principal IC | Full-stack breadth + leadership |

## ATS Keyword Checklist

Before submitting any resume:
- [ ] JD top keywords appear verbatim in resume (not synonyms)
- [ ] Skills section matches LinkedIn skills section
- [ ] No tables, columns, headers/footers (ATS can't parse these)
- [ ] File format: PDF (ATS-safe)
- [ ] File name: `FirstName-LastName-RoleTitle.pdf`

## Generate cluster resume stubs

`tools/resume-gen.py` auto-generates a markdown stub per role cluster from `profile/my-profile.yaml`:

```bash
python tools/resume-gen.py                       # generate all 14 clusters
python tools/resume-gen.py --cluster silicon_engineer
python tools/resume-gen.py --list-clusters       # see all cluster IDs
```

Output: `resume/cluster-{id}.md` per cluster — skills section, target titles, target companies.
Fill in once, regenerate after updating your profile.

## Files

- `resume/cluster-{id}.md` — auto-generated stubs (edit before submission)
- `resume/master-cv.pdf` — full career history (not for submission)
- Cluster PDFs for submission: export from the markdown stubs

> Add PDF files to `.gitignore` if they contain personal info you don't want public.
