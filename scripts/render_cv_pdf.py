#!/usr/bin/env python3
"""
render_cv_pdf.py — Convert a tailored-cv.md file into an ATS-compliant, beautifully typeset PDF using Typst.

Usage:
    python3 scripts/render_cv_pdf.py applications/2026-11_company_role/tailored-cv.md
    python3 scripts/render_cv_pdf.py applications/2026-11_company_role/tailored-cv.md [output.pdf]
"""

import sys
import os
import re
import subprocess
from pathlib import Path


def escape_typst_text(text: str) -> str:
    """Escapes special Typst characters in normal body text."""
    # Escape @ when not inside #link(...)
    # Escape # when not a Typst keyword
    text = re.sub(r'(?<!\\)@', r'\@', text)
    # Escape standalone dollar signs
    text = re.sub(r'(?<!\\)\$', r'\$', text)
    return text


def convert_inline_markdown(text: str) -> str:
    """Converts markdown bold, italic, and links into Typst inline markup."""
    # First extract and placeholder links to prevent their URLs from being corrupted
    links = []
    def link_repl(match):
        label = match.group(1)
        url = match.group(2)
        idx = len(links)
        links.append((label, url))
        return f"__LINK_PLACEHOLDER_{idx}__"
    
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, text)

    # Convert bold: **text** -> *text*
    text = re.sub(r'\*\*([^*]+)\*\*', r'*\1*', text)

    # Convert italic: *text* (that wasn't bold) -> _text_
    # Be careful not to match existing *bold* from above
    # We look for single *...* that are surrounded by whitespace or punctuation
    def italic_repl(match):
        inner = match.group(1)
        return f"_{inner}_"
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', italic_repl, text)

    # Escape Typst special characters in the text
    text = escape_typst_text(text)

    # Restore links
    for idx, (label, url) in enumerate(links):
        clean_label = escape_typst_text(label)
        # Ensure url has scheme if needed or mailto
        if '@' in url and not url.startswith('mailto:') and not url.startswith('http'):
            link_url = f"mailto:{url}"
        else:
            link_url = url
        typst_link = f'#link("{link_url}")[{clean_label}]'
        text = text.replace(f"__LINK_PLACEHOLDER_{idx}__", typst_link)

    return text


def parse_markdown_to_typst(md_content: str) -> str:
    lines = md_content.splitlines()
    
    name = "[Your Name]"  # Fallback — overridden by the `# Heading` in tailored-cv.md
    headline = ""
    contact_items = []
    
    i = 0
    # 1. Parse header block
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("# ") and not line.startswith("## "):
            name = line[2:].strip()
            i += 1
            break
        i += 1
        
    # Find headline and contact items
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("## ") or line == "---":
            break
        if line.startswith("**") and line.endswith("**") and not headline:
            headline = line.strip("*").strip()
        elif line.startswith("- "):
            raw_contact = line[2:].strip()
            # Split by | if present
            parts = [p.strip() for p in raw_contact.split("|")]
            for p in parts:
                contact_items.append(p)
        i += 1

    # Skip any separator
    while i < len(lines) and (lines[i].strip() == "---" or not lines[i].strip()):
        i += 1

    # Process remaining sections
    body_elements = []
    current_role_lines = []
    in_role_block = False

    def flush_role_block():
        nonlocal current_role_lines, in_role_block
        if current_role_lines:
            body_elements.append("#block(breakable: true)[\n" + "\n".join(current_role_lines) + "\n]\n#v(4pt)")
            current_role_lines = []
            in_role_block = False

    while i < len(lines):
        line = lines[i]
        sline = line.strip()

        if sline in ("<!-- pagebreak -->", "<pagebreak>", "\\pagebreak"):
            flush_role_block()
            body_elements.append("\n#pagebreak()\n")
            i += 1
            continue

        if sline.startswith("## "):
            flush_role_block()
            section_title = sline[3:].strip().upper()
            body_elements.append(f"""
#v(6pt)
#block(width: 100%, stroke: (bottom: 0.75pt + rgb("#d0d7de")), inset: (bottom: 3pt))[
  #text(size: 10pt, weight: "bold", fill: rgb("#0d1117"))[{section_title}]
]
#v(2pt)
""")
            i += 1
            continue

        elif sline.startswith("### "):
            flush_role_block()
            in_role_block = True
            role_title = convert_inline_markdown(sline[4:].strip())
            header_lines = [f"#text(weight: \"bold\", size: 9.5pt, fill: rgb(\"#0d1117\"))[{role_title}] \\"]
            i += 1
            # Check if next line is dates (e.g. *2026-04 – Present | Permanent*)
            if i < len(lines) and lines[i].strip().startswith("*") and lines[i].strip().endswith("*"):
                date_str = lines[i].strip().strip("*").strip()
                date_str = convert_inline_markdown(date_str)
                header_lines.append(f"#text(style: \"italic\", size: 8.5pt, fill: rgb(\"#57606a\"))[{date_str}]")
                i += 1
            current_role_lines.append("#block(breakable: false, width: 100%)[\n" + "\n".join(header_lines) + "\n]\n#v(2pt)")
            continue

        elif sline.startswith("#### "):
            # Sub-heading (e.g. achievement title)
            sub_title = convert_inline_markdown(sline[5:].strip())
            target = current_role_lines if in_role_block else body_elements
            target.append(f"\n#text(weight: \"semibold\", size: 9pt, fill: rgb(\"#24292f\"))[{sub_title}]\n")
            i += 1
            continue

        elif sline.startswith("- "):
            bullet_text = convert_inline_markdown(sline[2:].strip())
            target = current_role_lines if in_role_block else body_elements
            target.append(f"- {bullet_text}\n")
            i += 1
            continue

        elif sline == "---":
            flush_role_block()
            i += 1
            continue

        elif sline:
            # Normal paragraph text
            para = convert_inline_markdown(sline)
            target = current_role_lines if in_role_block else body_elements
            target.append(f"{para}\n\n")
            i += 1
            continue

        else:
            # Blank line
            i += 1

    flush_role_block()

    # Format contact items into clean horizontal line
    formatted_contacts = []
    for item in contact_items:
        # Strip leading **Key:** if present
        clean_item = convert_inline_markdown(item)
        formatted_contacts.append(clean_item)
    
    contacts_str = " #h(6pt) • #h(6pt) ".join(formatted_contacts)

    typst_doc = f"""// Auto-generated by Master CV Typst Compiler
#set page(
  paper: "a4",
  margin: (x: 1.5cm, top: 1.4cm, bottom: 1.4cm),
  footer: context [
    #align(center)[
      #text(fill: rgb("#6e7781"), size: 8pt)[
        {name} — Curriculum Vitae #h(6pt) | #h(6pt) Page #counter(page).display("1 of 1", both: true)
      ]
    ]
  ]
)

#set text(
  font: ("Helvetica Neue", "Arial"),
  size: 9pt,
  fill: rgb("#24292f"),
  lang: "en",
  region: "gb",
  spacing: 110%,
)

#set par(justify: false, leading: 0.52em)
#set list(spacing: 5pt, marker: text(fill: rgb("#57606a"))[•])

// Header
#align(center)[
  #text(size: 19pt, weight: "bold", fill: rgb("#0d1117"))[{name}] \\
  #v(2pt)
  #text(size: 10.5pt, weight: "medium", fill: rgb("#0969da"))[{escape_typst_text(headline)}] \\
  #v(4pt)
  #text(size: 8pt, fill: rgb("#57606a"))[
    {contacts_str}
  ]
]

#v(4pt)

{"".join(body_elements)}
"""
    return typst_doc


def compile_md_to_pdf(md_path: Path, output_pdf_path: Path = None) -> Path:
    if not md_path.exists():
        raise FileNotFoundError(f"Input file not found: {md_path}")

    if output_pdf_path is None:
        output_pdf_path = md_path.with_suffix(".pdf")

    typ_path = md_path.with_suffix(".typ")

    md_content = md_path.read_text(encoding="utf-8")
    typst_content = parse_markdown_to_typst(md_content)

    typ_path.write_text(typst_content, encoding="utf-8")

    # Run typst compile
    cmd = ["typst", "compile", str(typ_path), str(output_pdf_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Typst compilation failed:\n{result.stderr}")

    return output_pdf_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/render_cv_pdf.py <path/to/tailored-cv.md> [output.pdf]")
        sys.exit(1)

    md_path = Path(sys.argv[1]).resolve()
    pdf_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None

    try:
        out = compile_md_to_pdf(md_path, pdf_path)
        print(f"Successfully compiled ATS-compliant PDF: {out}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
