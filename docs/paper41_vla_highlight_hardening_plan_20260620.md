# Paper 41 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Harden Paper 41's visible PDF link-box styling so it matches the VLA-v4 role-model PDF's professional red and green boxed callouts while preserving the final 26-page embodied abstraction failure modes manuscript, its full-scale benchmark, and all scientific claims.

## Current Evidence

- Canonical PDF: `C:/Users/wangz/Downloads/41.pdf`.
- Pre-change artifact existed at the canonical path and was superseded by the final rebuild recorded below.
- Current size: 391726 bytes.
- Current page count: 26.
- Current affected link pages: 6, 7, 10, 12, 13, 16, and 17.
- Current link annotations: 22 green citation/link boxes and 13 red internal-reference boxes.
- Current border state: all 35 link annotations use border `(0, 0, 0)`, so the boxes are invisible.
- Current LaTeX source uses `\usepackage[hidelinks]{hyperref}` in root `main.tex`.
- Current build wrapper is `scripts/build_pdf.ps1`; it builds from the repository root, exports `C:/Users/wangz/Downloads/41.pdf`, and removes local `main.pdf`.
- Current full-scale benchmark remains 235,872 compact condition rows and 34,871,316,480 represented trial evaluations.
- Pre-change pages 6, 7, 10, 12, 13, 16, and 17 were rendered to `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper41_before` at 160 dpi for baseline visual comparison.

## Role-Model Style Target

Match the VLA-v4 role model's link annotation style:

```tex
\usepackage{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

Expected Paper 41 result after rebuild:

- Page count remains 26.
- All 22 citation/link annotations remain green.
- All 13 internal-reference link annotations remain red.
- All 35 link annotations use visible border `(0, 0, 1)`.
- No benchmark data, tables, figures, claims, or manuscript body text changes.

## Execution Plan

1. Preserve the before-render evidence for pages 6, 7, 10, 12, 13, 16, and 17 until post-change QA passes.
2. Replace `\usepackage[hidelinks]{hyperref}` in root `main.tex` with plain `\usepackage{hyperref}` plus the VLA-v4 `\hypersetup` block above.
3. Rebuild using `scripts/build_pdf.ps1`, which exports only `C:/Users/wangz/Downloads/41.pdf`, records build metadata, and removes local `main.pdf`.
4. Verify with `pypdf` that the rebuilt PDF has 26 pages, 22 green link annotations, 13 red link annotations, and 35 `(0, 0, 1)` borders.
5. Render affected post-change pages 6, 7, 10, 12, 13, 16, and 17 and visually inspect the boxes for role-model-like color, line weight, alignment, spacing, and legibility.
6. Update README, child status, and tracked audit/readiness metadata with the final hash, size, and visual hardening evidence.
7. Remove Paper 41 temporary render folders after QA while preserving the shared `role_model` render.
8. Commit and push the clean repo before moving to the next paper.

## Non-Goals

- Do not rerun the benchmark.
- Do not pad content or alter the 26-page manuscript.
- Do not revise claims, tables, captions, figures, or body text unless visual QA exposes a layout defect that requires a tiny local fix.

## Final QA Result

- Rebuilt canonical PDF: `C:/Users/wangz/Downloads/41.pdf`.
- Final SHA256: `9334E545BBDB8218703B8E53A8E15C410DE2BF0D4C9968A6CE77E1C4A0C39DEE`.
- Final size: 391726 bytes.
- Page count remains 26.
- Annotation inventory: 22 green citation/link boxes, 13 red internal-reference boxes, and 35 visible `(0, 0, 1)` borders.
- Visual QA rendered pages 6, 7, 10, 12, 13, 16, and 17 at 160 dpi. The boxes are thin, aligned, legible, and collision-free, matching the VLA-v4 role-model treatment.
- Local `main.pdf` was removed by the build wrapper after export.
