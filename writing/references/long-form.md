# Long-form mode

You are the editor. You do not write the document in one context: you design its spine, keep its state in files, give each agent a narrow brief, and run reviews until the parts read as one work by one author. Guard against two failures: fragmentation (drifting notation, concepts used before definition, broken threads at seams, one idea explained three times) and unearned smoothness (fluent prose over skipped steps, wrong numbers, unchecked claims).

## Layout
Adapt names; keep the roles. Source material lives outside `doc/`; writers read it, the text never names it.
```
doc/
  SPINE.md          parts > chapters > sections (spine entry template below)
  READER.md         reader persona(s), assumed prerequisites
  STYLE.md          venue, spelling, units, citation style, voice; extends style.md
  REGISTER.md       register models and their distilled usage (prose.md, Register)
  NOTATION.md       one symbol, one meaning, first-use location
  GLOSSARY.md       terms and their defining section
  BANNED-TERMS.txt  internal labels that must never appear (one regex per line); seed it from the
                    source material's labels before writing, extend it as new ones appear
  ledgers/
    CONCEPTS.md     concept > defining section > using sections (dependency DAG)
    CLAIMS.md       each nontrivial claim > derived-in location or public source and location
    THREADS.md      narrative threads: opened, advanced, closed
    SEAMS/<sec>.md  exit state of each section (template below)
    REVIEWS/<sec>/  every review report, kept unedited
  briefs/<sec>.md   writer brief per section (template below)
  src/              one source file per section, plus the master file and one .bib
```

## Spine (yourself, before any writing)
1. Map the material as a dependency DAG of results; mark what READER.md assumes, what the text builds, and what is only cited.
2. Sort topologically so nothing is used before it is introduced; among valid orders pick the best narrative arc (foundations, core, applications, practice).
3. A section is one writer's assignment: 3,000-6,000 words, written in calls of at most about 2,500 words each. A chapter is 4-10 sections. Budget words per section.
4. Fill a spine entry per section.
5. Matrix-shaped material: one axis for chapters, the same internal template along the other, and an atlas table mapping every cell to its section. No cell gets two half-explanations.
6. Choose the register models; have an agent distil REGISTER.md.
7. Seed CONCEPTS, THREADS and NOTATION from the spine.
8. Have the spine reviewed by a structural reviewer (dependency violations, gaps, duplicate coverage, budget realism) and a reader-persona agent ("would I know enough at each chapter start?"). Revise before writing.

## Per section, in dependency order
Sections whose prerequisites are accepted may run in parallel; keep concurrent writers few enough to merge ledgers between waves.

| Step | Agent | Reads | Writes |
|---|---|---|---|
| 1 Brief | editor | SPINE, ledgers, predecessor SEAMS | briefs/<sec>.md |
| 2 Draft | writer | brief, STYLE, REGISTER, NOTATION, GLOSSARY, predecessor SEAMS, sources | src/<sec>; SEAMS/<sec>.md with proposed ledger rows |
| 3 Lint | script | src/<sec> | REVIEWS/<sec>/lint.txt (`lint.py --banned BANNED-TERMS.txt`) |
| 4 Derivation check (technical) | isolated verifier | src, cited sources, NOTATION | each equation CHECKED / WRONG / GAP |
| 5 Prose | isolated reviewer | src, STYLE, REGISTER, prose.md | prose report |
| 6 Cold readers | 2+ isolated personas | the text up to and including this section only | reader reports (reader-review.md) |
| 7 Revise | writer or fresh reviser | all reviews | src, SEAMS, revision log |
| 8 Accept | editor | reviews, log, build | ledger rows merged; ACCEPTED in SPINE |

- Reviewers never see each other's reports. Cold readers see only the text.
- Writers propose ledger rows; only the editor writes NOTATION, GLOSSARY, CONCEPTS and CLAIMS, renaming colliding symbols before acceptance.
- WRONG, GAP or a reader's "lost" blocks acceptance, unless the editor records why the step stands and the reader confirms on re-read.
- Revisers fix a point in the text itself, never with a sentence announcing the fix (prose.md pattern 20).
- Build every time: no undefined references, labels or citations.
- A section resting on an unconfirmed result is BLOCKED in SPINE until the result clears.

## Cross-section reviews
- **Seam:** after both sides are accepted, one agent reads the last third of section n, the first third of n+1 and both SEAMS: promises kept, nothing introduced twice, notation and tone continuous, natural transition.
- **Chapter:** arc, redundancy, rigour against intuition, worked examples against outcomes, summary.
- **Thread:** one agent per THREADS.md entry reads only its sections: opened, developed, closed.
- **Whole document, near the end:** notation (one meaning, defined before use), terminology, cross-references, citation integrity (each cited location exists and says that), the banned-term lint and a cold read for anything that sounds internal, the full prose lint, a fresh cold-reader pass per part.
- Reviews produce reports; the editor issues revision briefs; nothing is fixed silently.

## Correctness
- The verifier redoes each non-definitional step from the previous line: CAS for algebra, dimensional analysis on displayed results, limiting cases the text claims; it reports any factor, sign or convention drift against NOTATION.
- Numbers come from scripts kept outside the text; the text states the inputs.
- Check novelty and priority claims against the literature first; state them modestly with their scope.

## Devices (in proportion to the reader)
Chapter openings that motivate and connect (not outlines); worked examples with every step; boxed key results; "used later in" pointers after foundational sections; a running example carried through; figures that show mechanisms.

## Finishing
Front matter (preface last, reading guide with dependency chart, notation list); back matter (appendices, glossary, index from writers' proposed entries, bibliography); full build; whole-document reviews; a final front-to-back cold read by two fresh personas. Report to the user: length, open issues, and every editor override with its reason.

## Templates
**Spine entry**
```
### <n.m> <title>  [PLANNED | BRIEFED | DRAFTED | IN REVIEW | ACCEPTED | BLOCKED(<reason>)]
Purpose (one sentence) · Outcomes (2-5, "the reader can derive / compute / explain / do ...") ·
Prerequisites (concept > section) · Introduces · Key results (derived / cited) · Sources ·
Figures, tables, worked examples · Threads (open / advance / close) · Budget (words)
```
**Writer brief**
```
# Brief: <n.m> <title>
Place: part/chapter, purpose, budget (subsection by subsection, at most ~2,500 words per call)
Reader state on entry: from predecessor SEAMS (knows, symbols defined, threads open)
Outcomes; must cover, in order
Prerequisites (point back, do not re-explain); concepts introduced here (define in full)
Key results: derived here or cited (public source, location)
Sources (for the writer only; never named in the text)
Figures, tables, worked examples
Constraints: STYLE, NOTATION, GLOSSARY authoritative; match REGISTER; propose new symbols and terms,
  never invent silently; avoid BANNED-TERMS; show every step or move it to an appendix and point to it
Deliverables: src/<sec> (builds in the master file); SEAMS/<sec>.md; proposed NOTATION, GLOSSARY,
  CONCEPTS, CLAIMS rows and index entries
```
**Seam**
```
# SEAM: <sec>
Reader now knows · Symbols introduced (defining equation) · Terms introduced ·
Threads opened / advanced / closed · Promises to later sections ·
Proposed rows: NOTATION · GLOSSARY · CONCEPTS · CLAIMS · INDEX
```
**Review report**
```
# Review: <derivation | prose | reader-N | seam | chapter | thread | audit>: <section(s)>
Scope/persona · Verdict
| # | Location | Finding | Severity (blocking / minor) | Proposed fix |
```
