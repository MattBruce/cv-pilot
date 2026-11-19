# Agent Instructions: cv-pilot — Master CV & Application Generator

This repository is an AI-augmented career knowledge base and deterministic application generator. It contains a verified, exhaustive single source of truth (`master-cv.md`) used to produce tailored CVs and cover letters on demand for specific job opportunities.

---

## Prerequisites

Before using this repository, ensure the following are available:

- **Python 3** — required to run the PDF compiler (`python3 --version`)
- **Typst** — required for PDF generation (`brew install typst` on macOS, or see [typst.app](https://typst.app/) for other platforms)
- **An AI coding agent** — AGY (Antigravity), Claude Code, Cursor, Codex, or any agent with filesystem access

---

## Core Rules & Guardrails

1. **Strict Ground Truth (Zero Hallucination):**
   - `master-cv.md` is the **only** source of factual truth for the user's career history, achievements, metrics, roles, dates, tools, and education.
   - **NEVER** hallucinate, extrapolate, or invent metrics, companies, titles, technologies, libraries, or responsibilities.
   - If a job specification requires a skill or experience not in `master-cv.md`, do **NOT** invent it. Explicitly flag it as a missing requirement during gap analysis.
2. **ATS-Compliant Formatting:**
   - Output clean, single-column Markdown.
   - Never use HTML tables, multi-column layouts, SVG icons, or complex CSS for CV drafts.
3. **Spelling & Tone of Voice:**
   - Default to UK English spelling (`-ise`, `colour`, `licence`, `modelling`) unless the user specifies otherwise.
   - Tone: Direct, plain English, evidence-led, active verbs, technically precise.
   - Respect the user's tone and phrasing preferences in **Section 13** (`Application Preferences & AI Instructions`) of `master-cv.md`.
   - Never use stiff robotic openers (avoid *"I am writing to apply for..."* or *"I am pleased to submit..."*); prefer natural openers like *"I would like to be considered for..."* or leading directly into the technical hook.
   - Strictly avoid corporate buzzword fluff ("thrilled to apply", "dynamic synergy", "rockstar developer", "passionate self-starter").
4. **Confidentiality:**
   - Respect any confidential client boundaries noted in **Section 13** of `master-cv.md`. Where the user has flagged a client or metric as sensitive, anonymise or approximate as instructed.

---

## Directory Architecture

```text
.
├── master-cv.md                 # Single source of truth (exhaustive, verified facts)
├── master-cv-template.md        # Standardized blank template schema
├── prompts/
│   ├── tailor-cv.md             # Reusable prompt & ATS constraints for CVs
│   └── cover-letter.md          # Reusable prompt & constraints for cover letters
├── applications/                # Audit archive of submitted applications
│   ├── README.md
│   └── YYYY-MM_company_role/    # Subfolder per application
│       ├── job-spec.md          # Input: target job description & notes
│       ├── tailored-cv.md       # Output: agent-generated tailored CV
│       └── cover-letter.md      # Output: agent-generated cover letter
├── .agents/
│   └── skills/
│       ├── tailor-application/  # Skill: Full application tailoring (CV + Cover Letter + PDF)
│       │   └── SKILL.md
│       └── generate-pdf/        # Skill: Standalone ATS PDF compilation from markdown
│           └── SKILL.md
├── scripts/
│   └── render_cv_pdf.py         # Typst PDF compiler engine
└── AGENTS.md                    # This universal instruction file
```

---

## Primary Agent Tasks

### Task 1: Tailor an Application (Preferred Workflow)
When the user instructs you to prepare, tailor, or generate an application for a folder in `applications/` (e.g. `"Tailor an application for applications/2026-11_stripe_staff-engineer"`):

1. **Read Inputs:**
   - Read `master-cv.md` (paying close attention to **Section 13** for tone and phrasing preferences).
   - Read `applications/<folder>/job-spec.md` (and any local notes or tone overrides in `notes.md`). If `job-spec.md` does not exist, ask the user to provide the job spec first.
   - Review guidelines in `prompts/tailor-cv.md` and `prompts/cover-letter.md`.
2. **Perform Gap Analysis:**
   - Identify top 3–5 matching strengths from `master-cv.md`.
   - Map JD terminology to authentic experience in `master-cv.md`.
   - Identify and list missing criteria or unaddressed requirements (gaps).
3. **Write `applications/<folder>/tailored-cv.md`:**
   - Target max 2 pages (~800–1,000 words).
   - Tailor headline and professional profile to the role.
   - Select 8–12 relevant skills.
   - Prioritize 3–5 high-impact STAR bullet points per recent role (`[Active Verb] + [Context/Challenge] + [Action/Tech] + [Outcome/Impact]`).
   - Summarize older roles in 1–2 lines.
4. **Write `applications/<folder>/cover-letter.md`:**
   - Target max 350–400 words (3–4 paragraphs).
   - Follow user's tone of voice preferences from **Section 13** of `master-cv.md`.
   - Paragraph 1: The Hook & role alignment using natural phrasing (e.g. *"I would like to be considered for..."* or leading directly into the technical hook; never use robotic boilerplate like *"I am writing to apply for..."*).
   - Paragraphs 2–3: 2–3 concrete, evidence-backed achievements solving the company's stated challenges.
   - Paragraph 4: Alignment with technical mission & confident close.
5. **Compile PDF (Automated via Typst):**
   - Check if `typst` is installed (`which typst`).
   - If installed, run: `python3 scripts/render_cv_pdf.py applications/<folder>/tailored-cv.md` to generate `tailored-cv.pdf`.
   - If not installed, skip compilation and remind the user that installing Typst (`brew install typst`) enables one-click PDF compilation.
6. **Report to User:**
   - Summarize the gap analysis (strengths, alignment, gaps).
   - Confirm generated files (`tailored-cv.md`, `cover-letter.md`, and `tailored-cv.pdf`).
   - Output a **Verification Checklist** of numbers, metrics, or assumptions for the user to review before submission.

---

### Task 2: Update the Master CV
When the user asks to add new skills, projects, roles, or URLs to `master-cv.md`:
1. Place each item into its correct section and category (deduplicating existing mentions).
2. Maintain the established Markdown formatting, headings, and schema version.
3. Update `last_updated: YYYY-MM-DD` in the frontmatter.
4. Verify consistency across Overview, Employment History, Skills, and Selected Projects.

---

### Task 3: Compile / Recompile PDF on Demand
When the user asks to generate, compile, or recompile a PDF (e.g. `"Generate PDF for applications/YYYY-MM_role/tailored-cv.md"`):
1. Check if `typst` is installed (`which typst`). If missing, inform the user to install it via `brew install typst`.
2. Execute: `python3 scripts/render_cv_pdf.py <path_to_tailored_cv.md>`.
3. Confirm compilation success and provide the output path `<folder>/tailored-cv.pdf`.
4. If the user wants to adjust page breaks, remind them they can place `<!-- pagebreak -->` anywhere in the Markdown and re-run.
