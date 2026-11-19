---
name: generate-pdf
description: Compile an ATS-compliant, publication-grade PDF from any tailored-cv.md file using Typst.
---

# Generate CV PDF Skill

This skill compiles an ATS-compliant, 2-page vector PDF from a `tailored-cv.md` file using Typst and the repository's rendering engine.

---

## Trigger & Invocation

Activate this skill when:
- The user asks to "generate PDF", "compile PDF", or "recompile PDF" for an application subfolder or markdown file (e.g. `"Generate PDF for applications/2026-11_Blinds2Go_senior_front_end_dev/tailored-cv.md"` or `"Recompile PDF in applications/2026-11_Blinds2Go_senior_front_end_dev"`).
- The user makes manual edits to a `tailored-cv.md` and wants an updated PDF.

---

## Execution Steps

1. **Verify Prerequisites:**
   - Check if `typst` is installed: `which typst`.
   - If not installed, inform the user:
     > *"Typst is required for automated PDF compilation. You can install it with: `brew install typst`."*

2. **Identify Target File:**
   - Resolve the target markdown file (defaults to `tailored-cv.md` in the specified directory).

3. **Execute Compilation:**
   - Run the compiler script:
     ```bash
     python3 scripts/render_cv_pdf.py <path/to/tailored-cv.md>
     ```

4. **Verify & Report:**
   - Ensure the process exited with code 0.
   - Confirm the output path (e.g., `<subfolder>/tailored-cv.pdf`).
   - Remind the user that inserting `<!-- pagebreak -->` anywhere in the Markdown allows them to adjust the page break point if needed.
