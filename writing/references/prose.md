# Prose review

Run `scripts/lint.py` first, then read in full. Report every hit with its location and a concrete rewrite. Every pattern is a case of the deletion test (SKILL.md rule 2): the fix is always to name the thing, its size, its condition or its location.

## Patterns
1. **Low-content gestures.** "plays a key role", "is central to", "has important consequences", "rich structure", "subtle interplay", "deep connection", "nontrivial"; evaluations without a referent ("remarkably", "interestingly", "crucially"); sentences true of any text ("This is an important topic", "Several factors contribute").
2. **Self-narration.** "In this section we will", "Let us now turn to", "It is worth noting", "As we will see", "We state it here without derivation", "We give it in the form of [1, Eq. 8]". Do the thing instead. Deferrals say where the content is ("derived in Sect. 2").
3. **Inflated vocabulary.** delve, crucial, pivotal, intricate, realm, landscape, tapestry, robust (non-technical), seamless, leverage (verb), underscore, showcase, notably, essentially, fundamentally, holistic, paradigm, nuanced, "a wide range of", "cutting-edge", "game-changing".
4. **Praise, marketing, anthropomorphism.** "this elegant result", "this powerful framework", "unlocks", "empowers", "the system knows". Let the result speak.
5. **Reflexive triads.** Three adjectives or clauses chosen for rhythm.
6. **Stacked hedges.** "may potentially", "could possibly", "it might be argued". Over-qualifying established results, under-qualifying new ones.
7. **False contrast.** "This is not just X, it is Y"; "Rather than merely …".
8. **Periphrasis and withheld positives.** A figurative stand-in for the plain word, often inside stacked negations: "the data tell us", "that silence" (for null results), "sits at the heart of", "never … anything except", "nothing … but", "does little more than", "has yet to". Rewrite with the plain noun and no negations. Motivate with concrete stakes, not cadence or aphorism.
9. **Invented metaphor vocabulary.** A private metaphor promoted to a term ("rung", "tier", "layer", "pillar") where the field has a name. Use the field's term; test: would a referee or practitioner use this word?
10. **Dash overuse.** More than about one em dash per paragraph, especially paired dashes as parentheses.
11. **Colon reveals and rhetorical questions** for drama ("The answer? Caching.").
12. **Uniform rhythm.** Runs of sentences of equal length and shape.
13. **Bullets instead of argument.** Reasoning goes in connected prose. Bullets for enumerations, and where the venue is list-native (slides, release notes, checklists, reference docs).
14. **Vague quantifiers.** "significantly", "substantially", "a large number", "very", "quite". Give the number or the scaling.
15. **Unanchored referents.** "This shows …", "the latter", "the second form" when the referent is unclear. Name it.
16. **Wordiness.** Throat-clearing openers, doubled synonyms ("each and every", "first and foremost"), "in order to", "due to the fact that", "the fact that", nominalisations hiding the verb. Take the shorter equivalent.
17. **Abstract category frames.** Naming a category instead of its members, so the reader asks "like what?": "We collect the facts we need", "Two consequences follow", "The previous sections fixed …". Name the facts, the consequences, the new question. Check every opening sentence and every roadmap.
18. **Restatement.** A paragraph that summarises the previous one; closing paragraphs that loop over what is already established. A part ends on its last new fact; the only sanctioned recap is a designated summary.
19. **Gesturing titles.** "Putting it together", "Beyond the basics", "What X fixes", "X and its consequences", "Some subtleties", colon pairs, questions, puns. Test: from the title alone a reader can predict the central result and find it in an index. Prefer the established name.
20. **Process artifacts.** Sentences that exist only because the text went through drafts and reviews: consistency assurances ("we use the same value throughout"), justifications aimed at a reviewer, bookkeeping about unremarkable choices, announcements of a fix. State the value and use it; keep a convention note only where a reader comparing with other sources would be misled, as one clause about those sources. An internal label becomes a descriptive name defined in the text; an internal acronym survives only if it helps the reader and is defined at first use.
21. **Citations as content.** "Source: [12], Eq. (77)", "as defined in [12]", "see the docs for the format". State the content; keep the citation for credit.
22. **Unannotated master equations** (technical). When a central equation is a product or sum of distinct pieces the text then discusses one by one, label the pieces in the display (underbraces, one or two words each). Only for the few organising equations.

## Register
The text reads as a practitioner explaining the subject to a colleague in the venue's own voice. For substantial work, name one to three human-written models known for clear writing in the field and venue. Distil their usage into a register note: terms of art, characteristic phrasings, how estimates and pictures are introduced, sentence rhythm, a few example sentences, connective frequencies.
- Use the field's terms in the field's sense; coin nothing that has a name. If a forced symbol or term is non-standard, say once what others write.
- Plain verb, concrete noun ("the rate drops", "the request fails") over bureaucratic constructions ("a reduction is obtained").
- Use idioms and connectives at the model's frequency; watch crutches ("so", "gives", "therefore", "only") running several times above it.
- Estimates before exact results where they help; a concrete picture, stated, then checked.
- Sentences a person would say aloud: active voice by default, no stacked appositives, nothing that needs a second reading.
- Do not narrate an equation or code block symbol by symbol when one sentence about its meaning does the job.
- Avoid "thereby", "whereby", "hence" chains, "respectively" pairings, "thus" at every turn.
- Calibrate: pick two or three passages and ask whether a model author could have written them. Where not, rewrite one sentence as that author would.

## Arrangement
- Each part opens with why the reader needs it, tied to what came before, in one or two sentences.
- Each step follows from the last. No forward references for definitions; no result before the tools to understand it.
- Simplest correct case first, then the generalisation.

## Clarity
- One job per paragraph; its first sentence says what it is.
- Every equation, code block or figure is introduced by what it is for and followed by what it means.
- Every symbol and term is defined at first use and used in one sense only (matching the notation and glossary files, where they exist).
- Intuition accompanies formal results and never replaces a derivation.

## Report
Table: location | pattern | text | rewrite. Verdict: PASS (at most 3 minor hits per 1,000 words), REVISE, or REWRITE (systemic voice problems).
