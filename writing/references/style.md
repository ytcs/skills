# Default house style

Venue conventions override every item (publisher or journal author instructions, docs-site guide, repo style). For books, the default is a Springer-type monograph (svmono); for papers, the target journal's.

## Titles and headings
- Short noun phrases, typically 1-5 words, naming the content in the field's terms. No subtitles unless required, no colon pairs, questions, puns, punchlines or epigraphs.
- The reader can predict the central result from the title.

## Text
- One spelling convention (American or British) throughout.
- Person: "we" for author and reader in academic and technical exposition; "you" and the imperative in instructions, docs and messages.
- Words for one to nine in prose; numerals with units and in technical counts.
- Abbreviations defined at first use (per chapter if chapters may be read alone).
- Lists only for enumerable items: assumptions, steps, conditions, options.

## Equations and units
- Number the displayed equations that are referred to, by chapter in books: "Eq. (3.12)". Consistent form throughout.
- Equations are part of sentences and end with the punctuation grammar requires.
- Define every symbol at first use, in the introducing sentence or a "where …" clause directly after.
- One convention each for vectors, operators and differentials; upright text subscripts for labels (E_\mathrm{g}).
- State the unit system once ("natural units, ħ = c = 1, unless stated"); give values with a thin space before the unit (1.17 eV).

## Figures, tables, code
- Each is cited in the text before it appears, and numbered (by chapter in books).
- Captions stand alone: what is shown, in what units, for which parameters.
- Axis labels carry quantity and unit, using the text's symbols. Prefer vector graphics.
- Every plotted or tabulated number traces to a script; code shown to readers runs as shown.

## Citations and cross-references
- One citation style throughout (numbered or author-year). Cite specific equations or sections: "[12, Eq. (5)]".
- Cite only what a public reader can obtain; give preprint identifiers alongside journal references.
- Books: a bibliography per chapter, in order of first citation, kept as one master .bib rendered with biblatex `refsection` or `chapterbib`, unless the venue wants one global list.
- Use labels and links, never hard-coded numbers; one abbreviation form throughout ("Sect. 4.3", "Chap. 7", "Fig. 2.1", "Appendix B").

## Books and long reports
- Front matter: title page, preface (written last), contents, reading guide, notation and acronyms.
- Numbered decimally to three levels at most (Chapter 3, Sect. 3.2, Sect. 3.2.1); run-in headings below.
- Each chapter opens with a short paragraph giving its question and its link to the previous chapter (not an outline), and ends with a summary.
- Appendices are lettered; long derivations moved there are pointed to explicitly.
- No exercises unless the venue is a textbook that wants them; every step is in the text or an appendix.
