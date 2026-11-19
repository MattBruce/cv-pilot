---
name: tailor-application
description: Tailor an ATS-compliant CV and evidence-backed cover letter for a target job application subfolder in applications/ using master-cv.md as the verified single source of truth.
---

# Tailor Job Application Skill

This skill guides an AI coding agent (AGY, Claude Code, Cursor, Codex, etc.) to evaluate a job specification, perform a gap analysis, and generate both a tailored CV (`tailored-cv.md`) and cover letter (`cover-letter.md`) directly in the target application folder.

---

## Trigger & Invocation

Activate this skill when:
- The user asks to tailor, generate, or prepare a CV, cover letter, or application for a folder in `applications/` (e.g., `applications/2026-11_stripe_staff-engineer/`).
- The user provides or updates a `job-spec.md` inside an application folder and requests an application draft.

---

## Inputs & File Locations

1. **Master CV (Ground Truth):**
   `master-cv.md` at the repository root.
   > **CRITICAL:** `master-cv.md` is the single source of truth. You must **NEVER** hallucinate, invent, or extrapolate skills, technologies, dates, metrics, or responsibilities not documented here.

2. **Target Application Directory:**
   `applications/<application-folder>/`
   - Target job description: `applications/<application-folder>/job-spec.md`
   - (Optional) Supplementary notes or recruiter instructions in that folder.

3. **Prompt Specifications:**
   - `prompts/tailor-cv.md` (CV tailoring parameters and ATS guidelines)
   - `prompts/cover-letter.md` (Cover letter structure, tone, and word count constraints)

---

## Step-by-Step Execution Workflow

### Step 1: Ingest & Inspect
1. Read `master-cv.md` completely.
2. Locate the job specification in the target application folder. Accept it in any of the following formats:
   - `job-spec.md` — Markdown (preferred)
   - `job-spec.txt` — Plain text
   - `job-spec.pdf` — PDF (read via available tools)
   - `job-spec.html` — HTML (strip tags, extract body text)
   - `job-spec.docx` — Word document (extract plain text)
   - **Inline paste:** If the user pastes the job description directly into the chat, use that text.

   **If none of the above exist in the folder**, ask the user to either drop a file into the folder or paste the JD directly.

   **If the job spec is provided in any format other than `job-spec.md`** (or pasted inline), extract the plain text content and write it to `applications/<application-folder>/job-spec.md` before proceeding. Confirm this normalisation step to the user.

3. Check for any existing notes, salary targets, or role context inside the folder (e.g. `notes.md`).

### Step 2: Gap Analysis & Strategic Alignment
Before drafting the documents, perform a strategic alignment check:
1. **Core Alignment (Strengths):** Identify the 3–5 most compelling achievements and skills in `master-cv.md` that directly satisfy the job spec's must-have criteria.
2. **Terminology Mapping:** Identify terminology in the job description that corresponds to the user's experience without exaggerating facts (e.g. mapping "microservices" to documented modular API work, or "design systems" to documented component libraries).
3. **Gaps & Missing Criteria:** Explicitly identify any required skills or qualifications in the job spec that are **absent** from `master-cv.md`.
   - **RULE:** Never invent experience to fill gaps. Flag them clearly for the user.

### Step 3: Generate the Tailored CV (`tailored-cv.md`)
Write `applications/<application-folder>/tailored-cv.md` adhering strictly to these standards:
- **Length Constraint:** Max 2 pages (~800–1,000 words total).
- **Format:** ATS-compliant single-column Markdown. No tables, multi-column layouts, HTML divs, or custom icon fonts.
- **Spelling:** Default to UK English (`-ise`, `colour`, `licence`) unless the user specifies otherwise in Section 13 of `master-cv.md`.
- **Header:** Full contact links from `master-cv.md` with a tailored professional headline matching the target role seniority and focus.
- **Professional Profile (3–4 sentences):** Identity, core technical specialisms, standout scale/impact metrics, and immediate value proposition for the target company.
- **Core Competencies / Key Skills:** 8–12 bulleted skills prioritized specifically for the job spec.
- **Employment History:**
  - Reverse chronological order.
  - Highlight 3–5 high-impact bullet points for recent/relevant roles using the formula:
    `[Active Verb] + [Context / Challenge] + [Action / Technologies] + [Measurable Outcome / Business Impact]`
  - Prioritize achievements matching the job spec; de-emphasize or omit irrelevant achievements.
  - For earlier roles, use 1–2 line summaries to conserve vertical space.
- **Education & Credentials:** As documented in `master-cv.md`.
- **Selected Projects (Optional / Selective):** Include 1–2 relevant projects from `master-cv.md` only if they directly reinforce key requirements of the target role.

### Step 4: Generate the Cover Letter (`cover-letter.md`)
Write `applications/<application-folder>/cover-letter.md` adhering strictly to these standards:
- **Length Constraint:** Max 350–400 words (3–4 focused paragraphs).
- **Tone:** Direct, authentic, evidence-led, technically precise. Follow user's tone of voice and phrasing preferences in **Section 13** of `master-cv.md` (and any local overrides in `notes.md` or `job-spec.md`).
- **Openers & Phrasing:** Never use stiff robotic openers (e.g. avoid *"I am writing to apply for..."* or *"I am pleased to submit my application"*). Prefer natural, confident openers (e.g. *"I would like to be considered for..."* or leading directly into the technical hook).
- **Zero corporate fluff:** Avoid hollow clichés such as *"thrilled to apply"*, *"dynamic self-starter"*, or *"passionate team player"*.
- **Paragraph Structure:**
  1. **The Hook:** State the target position with natural, confident phrasing, immediate alignment with the company's technical challenge or mission, and core value proposition.
  2. **The Evidence (1–2 paragraphs):** Directly address the 2–3 biggest problems in the JD using concrete achievements, technologies, and metrics from `master-cv.md`.
  3. **Why This Team / Role:** Authentic alignment with the company's problem space, technical direction, or product scale.
  4. **The Close:** Confident, polite invitation for a technical discussion.

### Step 5: Compile ATS-Compliant PDF (`tailored-cv.pdf`)
If `typst` is installed on the system (check via `which typst`):
1. Execute: `python3 scripts/render_cv_pdf.py applications/<application-folder>/tailored-cv.md`
2. This generates a publication-grade, ATS-compliant 2-page PDF (`tailored-cv.pdf`) using Typst.
3. If Typst is not installed, skip this step and add a friendly note informing the user to run `brew install typst` to enable automatic PDF generation.

### Step 6: Report to User
Provide a concise summary in the chat response:
1. **Summary of Action:** Confirm `tailored-cv.md`, `cover-letter.md`, and (if compiled) `tailored-cv.pdf` have been generated.
2. **Gap Analysis Summary:** Core strengths leveraged, terminology aligned, and identified gaps.
3. **Verification Checklist:** List all metrics, dates, or assumptions the user must verify before submitting.

---

## Strict Guardrails

1. **Zero Hallucination:** You may emphasize, prioritize, and rephrase, but never invent a metric, client, tool, library, date, or responsibility not documented in `master-cv.md`.
2. **Confidentiality:** Adhere to Section 13 of `master-cv.md` for any sensitive or anonymised client/employer details.
3. **File Integrity:** Always write files directly to disk in the target subfolder so the user has an immediate version-controlled record.
