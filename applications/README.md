# Applications Archive

Store each job application in its own subfolder named by date, company, and role:

```text
applications/
├── 2026-11_stripe_staff-engineer/
│   ├── job-spec.md
│   ├── tailored-cv.md
│   └── cover-letter.md
└── 2026-12_monzo_lead-platform/
    ├── job-spec.md
    └── tailored-cv.md
```

### Benefits of this structure:
1. **Audit Trail:** You always know exactly what version of your CV and claims you submitted to each employer.
2. **Interview Prep:** Before an interview, open that specific folder to review what the recruiter and interviewers saw.
3. **Continuous Improvement:** Notice which variations get callbacks and refine your Master CV accordingly.

---

### Generating with your IDE Coding Agent:
1. Create a new folder: `mkdir -p applications/YYYY-MM_company_role`
2. Drop the job description into `job-spec.md` in that folder.
3. In your agent chat (AGY, Claude Code, Cursor, Codex), type:
   > *"Tailor an application for `applications/YYYY-MM_company_role`"*
4. The agent will analyze the role against `master-cv.md` and write both `tailored-cv.md` and `cover-letter.md` directly into the folder.
