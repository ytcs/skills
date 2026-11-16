---
name: writing
description: Write, edit or review prose of any length (messages, emails, READMEs, docs, reports, proposals, papers, essays, posts, manuals, books) so it reads as plain, dense, human writing for a stated reader. Covers the information-content rule, an anti-AI-prose checklist with a lint, register matching, cold-reader review, house style for technical text, and a multi-agent mode for documents too long for one agent.
---

# writing

## Rules (every text)
1. Name the reader and the purpose first: who reads it, what they already know, what they must know or do afterwards. Use the persona the user gives, else the obvious one for the venue.
2. Information content governs. Every sentence and title carries a fact, number, definition, named object, instruction or step of argument. Deletion test: remove it; if the reader loses nothing, cut it or make it carry something.
3. Remove the patterns in `references/prose.md`. Run `scripts/lint.py` on any draft longer than a few paragraphs.
4. Sound like the field and the venue: its terms of art, plain verbs and concrete nouns, its idioms at its frequency (`references/prose.md`, Register).
5. Arrange so each part follows from the last: the reader's question first, the simplest correct case before the general one, nothing used before it is defined.
6. Be concise. Short sentences of varied length. Titles and headings are short noun phrases naming the content: no subtitles, punchlines, questions or epigraphs.
7. Standalone: the text never shows the process that produced it (drafts, reviews, agents, tools, internal labels, file paths, branch names) unless the reader needs it. No sentence announces a fix, assures consistency or answers a past reviewer. Every name the reader meets is defined in the text or common to the audience.
8. Citations and links attribute and let the reader verify; they never carry the argument. State the formula, value, definition or step the reader needs where it is used.
9. Follow the venue's conventions (publisher, journal, docs site, repo, organisation; including its heading forms, such as FAQ questions or email subject lines) where they exist; `references/style.md` is the default where they do not.
10. Calibrate confidence to evidence: state each claim with its actual condition and scope. No stacked hedges, no unearned certainty, no unchecked priority claims.
11. Technical text: every equation that is not a definition, and every number, is derived in the text (or an appendix it points to) or cited to a specific location in a public source. No "it can be shown", "straightforward algebra" or "left to the reader" without the steps. Check derivations independently, with a CAS where possible.

## Short texts
One context: a message up to a few thousand words.
1. Fix reader, purpose and venue (rules 1, 9).
2. Outline as the ordered list of facts the reader must leave with.
3. Draft.
4. Revise: deletion test per sentence; list the new fact in each paragraph and cut repeats; check `references/prose.md`; run the lint.
5. When the text matters, have a fresh agent that sees only the text and the persona read it cold (`references/reader-review.md`). Fix every point where it got lost.

## Long texts
Switch to `references/long-form.md` when the text is more than one agent can draft and revise in one context, or when many parts must share notation, terminology and a narrative thread (long reports, theses, manuals, books).

## Files
- `references/prose.md`: anti-AI patterns, register, arrangement and clarity checks, review report format.
- `references/style.md`: default house style (titles, text, equations, figures, citations, book structure).
- `references/reader-review.md`: cold-reader protocol and report.
- `references/long-form.md`: multi-agent orchestration, state files, reviews, templates.
- `scripts/lint.py FILE... [--banned TERMS.txt] [--max-dash 1.0] [--json]`: LaTeX or Markdown. Exit 1 on a blocking hit (banned term or unsupported-step phrase).
