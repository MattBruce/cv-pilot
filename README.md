# cv-pilot

An AI-augmented career knowledge base and application generator. Store your entire career history in one verified source of truth (`master-cv.md`), then generate tailored, ATS-compliant CVs and cover letters for specific roles on demand — using your IDE's coding agent.

---

## Prerequisites

| Tool | Purpose | Install |
|---|---|---|
| **Python 3** | PDF compiler | pre-installed on macOS / `brew install python` |
| **Typst** | PDF rendering engine | macOS: `brew install typst` · Linux: `snap install typst` · Windows: `winget install typst` · [All platforms →](https://typst.app/) |
| **AI coding agent** | Automates tailoring | AGY, Claude Code, Cursor, Codex, etc. |

---

## Repository Structure

```text
.
├── master-cv.md                 # Your single source of truth (exhaustive, verified facts)
├── master-cv-template.md        # Blank template — start here
├── AGENTS.md                    # Universal instructions for AI coding agents
├── .agents/
│   └── skills/
│       ├── tailor-application/  # Skill: Full application tailoring (CV + Cover Letter + PDF)
│       │   └── SKILL.md
│       └── generate-pdf/        # Skill: Standalone ATS PDF compilation from markdown
│           └── SKILL.md
├── scripts/
│   └── render_cv_pdf.py         # Typst PDF compiler engine
├── prompts/
│   ├── tailor-cv.md             # Reusable prompt & ATS constraints for CV tailoring
│   └── cover-letter.md          # Reusable prompt & constraints for cover letters
└── applications/                # Audit archive of tailored applications
    ├── README.md
    └── YYYY-MM_company_role/
        ├── job-spec.md          # Input: target job description & notes
        ├── tailored-cv.md       # Output: tailored, ATS-compliant CV
        └── cover-letter.md      # Output: targeted cover letter
```

---

## Getting Started

**Fork this repo**, then follow the steps below.

### 1. Set Up Your Master CV

Copy `master-cv-template.md` to `master-cv.md` and fill it in:

```bash
cp master-cv-template.md master-cv.md
echo "master-cv.md" >> .gitignore
```

The template is structured into sections covering your career history, skills, education, certifications, and application preferences. The more detail you add, the better your tailored outputs will be. Focus on **facts, metrics, and specific contributions** — rough notes are fine.

> **Keep `master-cv.md` private.** Add it to `.gitignore` if you fork this repo publicly.

---

### 2. Tailor an Application for a Target Role

#### Method 1: Using Your IDE Coding Agent (Preferred)
Your IDE's coding agent (AGY, Claude Code, Cursor, Codex, etc.) has direct filesystem access and automates the entire preparation in seconds:

1. Create a target folder under `applications/`:
   ```bash
   mkdir -p applications/2026-11_stripe_staff-engineer
   ```
2. Add the job description to that folder. The agent accepts any of these formats — use whichever is easiest:

   | Format | File to drop in the folder |
   |---|---|
   | Copy-paste from web / recruiter email | Just paste it directly into the agent chat |
   | Plain text | `job-spec.txt` |
   | Markdown | `job-spec.md` |
   | PDF (downloaded from job board) | `job-spec.pdf` |
   | HTML (saved from browser) | `job-spec.html` |
   | Word document | `job-spec.docx` |

   The agent will extract the content and normalise it to `job-spec.md` automatically before proceeding. You can also append personal notes (salary expectations, referral context, deadline) to that file below a `---` separator.
3. Open your coding agent chat and prompt:
   > *"Tailor an application for `applications/2026-11_stripe_staff-engineer`"*
   > *(or `/tailor-application applications/2026-11_stripe_staff-engineer` in AGY)*
4. The agent will:
   - Perform a **Gap Analysis** (matching strengths, terminology mapping, missing requirements).
   - Write `tailored-cv.md` directly into the subfolder.
   - Write `cover-letter.md` directly into the subfolder.
   - Automatically compile `tailored-cv.pdf` using **Typst** (if installed).
   - Output a **Verification Checklist** for you to confirm before sending.

---

#### Method 2: Manual LLM Prompting (Web / Chat)
If you're using a web chat interface (ChatGPT, Claude.ai, Gemini):

1. Create the application folder: `applications/YYYY-MM_company_role/`.
2. Copy the job description text (from any source) into `job-spec.md`.
3. Open `prompts/tailor-cv.md` and copy the prompt template.
4. Paste the prompt, the job description, and the contents of `master-cv.md` into your web chat.
5. Save the result as `tailored-cv.md` and repeat with `prompts/cover-letter.md` for `cover-letter.md`.

---

### 3. PDF Generation with Typst (ATS-Compliant)

cv-pilot includes a built-in compiler powered by [Typst](https://typst.app/) to render publication-grade, ATS-compliant vector PDFs:

1. **Install Typst (once)** — see the Prerequisites table above for your platform.
2. **Automated upon Application Creation:** Coding agents will automatically compile `tailored-cv.pdf` alongside `tailored-cv.md` during tailoring.
3. **Manual Recompilation on Demand:**
   - **Ask Your Coding Agent:**
     > *"Generate PDF for `applications/2026-11_stripe_staff-engineer/tailored-cv.md`"*
     > *(or `/generate-pdf applications/2026-11_stripe_staff-engineer/tailored-cv.md` in AGY)*
   - **Terminal CLI:**
     ```bash
     python3 scripts/render_cv_pdf.py applications/2026-11_stripe_staff-engineer/tailored-cv.md
     ```
4. **Custom Page Breaks:** Insert `<!-- pagebreak -->` anywhere in `tailored-cv.md` and recompile to control page layout.

---

## How the Agent Guardrails Work

cv-pilot is built around a strict **zero-hallucination** principle:

- The agent reads **only** from `master-cv.md` — it never invents metrics, tools, employers, or dates.
- If the job spec requires something not in your master CV, the agent flags it as a **gap** rather than fabricating experience.
- A **Verification Checklist** is always produced at the end of each run, listing every metric or claim you should double-check before submitting.

These rules are enforced via `AGENTS.md` (read by all agents on startup) and the `.agents/skills/` instruction files.

---

## Workflow Overview

```
master-cv.md  +  job-spec.md
        │
        ▼
   [Coding Agent]
        │
        ├── Gap Analysis & Alignment
        ├── tailored-cv.md  ──▶  tailored-cv.pdf (via Typst)
        └── cover-letter.md
```

---

## Licence

MIT
