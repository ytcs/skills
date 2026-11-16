# Prose review

Run `scripts/lint.py` (and `scripts/binding.py` where spaCy is available) first, then read every paragraph whole: the tools rank where to look and miss many failures. Report every hit with its location and a concrete rewrite. Patterns 1-22 and 24 are cases of the deletion test (SKILL.md rule 2): the fix is to name the thing, its size, its condition or its location. The deletion test never removes the arguments of a relational noun (what is missing from what), the name of the concept a passage explains, or a repeated noun that keeps a reference unambiguous (pattern 23); removing these makes a sentence shorter and harder to read.

## Patterns
1. **Low-content gestures.** "plays a key role", "is central to", "has important consequences", "rich structure", "subtle interplay", "deep connection", "nontrivial"; evaluations without a referent ("remarkably", "interestingly", "crucially", "of course", "indeed", "in fact", "it turns out", "the key point", "no accident"); aphoristic one-line summaries; sentences true of any text ("This is an important topic", "Several factors contribute").
2. **Self-narration.** "In this section we will", "Let us now turn to", "It is worth noting", "As we will see", "We state it here without derivation", "We give it in the form of [1, Eq. 8]". Do the thing instead. Deferrals say where the content is ("derived in Sect. 2").
3. **Inflated vocabulary.** delve, crucial, pivotal, intricate, realm, landscape, tapestry, robust (non-technical), seamless, leverage (verb), underscore, showcase, notably, essentially, fundamentally, holistic, paradigm, nuanced, "a wide range of", "cutting-edge", "game-changing".
4. **Praise, verdicts, anthropomorphism.** "this elegant result", "this powerful framework", "unlocks", "empowers", "the system knows"; figurative praise (honest, clean, sharp, tidy, neat, beautiful); paired verdict adjectives ("sufficient but loose", "exact but slow"). Let the result speak, or state the property ("exact; costs N^3").
5. **Reflexive triads.** Three adjectives or clauses chosen for rhythm.
6. **Stacked hedges.** "may potentially", "could possibly", "it might be argued". Over-qualifying established results, under-qualifying new ones.
7. **Negation framing.** "This is not just X, it is Y"; "not X but Y"; "X, not Y"; "rather than merely"; "does little more than". State the positive fact. Keep a contrast, in one clause, only where the reader would otherwise assume the wrong thing ("an estimate, not a bound").
8. **Periphrasis and withheld positives.** A figurative stand-in for the plain word, often inside stacked negations: "the data tell us", "that silence" (for null results), "sits at the heart of", "never … anything except", "nothing … but", "has yet to"; metaphor verbs and nouns for technical statements (sits, lives in, carries the weight, earns its place, pays off, turns on, buys, the price of, takes over, kicks in, enters the picture, the story, the catch, the upshot, the bottom line). Rewrite with the plain noun or technical verb (is, is given by, dominates above, depends on) and no negations. Motivate with concrete stakes, not cadence or aphorism.
9. **Invented metaphor vocabulary.** A private metaphor promoted to a term ("rung", "tier", "layer", "pillar") where the field has a name. Use the field's term; test: would a referee or practitioner use this word?
10. **Dash overuse.** More than about one em dash per paragraph, especially paired dashes as parentheses.
11. **Teasers.** Colon reveals and rhetorical questions for drama ("The answer: caching.", "The answer? Caching."); count-teasers ("Two consequences follow."). State the answer; name the consequences.
12. **Uniform rhythm.** Runs of sentences of equal length and shape, including runs of very short declaratives (which also produce the pointer chains of pattern 23).
13. **Bullets instead of argument.** Reasoning goes in connected prose. Bullets for enumerations, and where the venue is list-native (slides, release notes, checklists, reference docs).
14. **Vague quantifiers and intensifiers.** "significantly", "substantially", "a large number", "relatively small", "quite", "very", "extremely", "truly". Give the number or the scaling.
15. **Unanchored referents.** "This shows …", "the latter", "the second form" when the referent is unclear. Name it. This is the simplest case of pattern 23.
16. **Wordiness.** Throat-clearing openers, doubled synonyms ("each and every", "first and foremost"), "in order to", "due to the fact that", "the fact that", nominalisations hiding the verb. Take the shorter equivalent.
17. **Abstract category frames.** Naming a category instead of its members, so the reader asks "like what?": "We collect the facts we need", "Two consequences follow", "The previous sections fixed …". Name the facts, the consequences, the new question. Check every opening sentence and every roadmap.
18. **Restatement.** A paragraph that summarises the previous one; closing paragraphs that loop over what is already established. A part ends on its last new fact; the only sanctioned recap is a designated summary.
19. **Gesturing titles.** "Putting it together", "Beyond the basics", "What X fixes", "X and its consequences", "Some subtleties", colon pairs, questions, puns. Test: from the title alone a reader can predict the central result and find it in an index. Prefer the established name.
20. **Process artifacts.** Sentences that exist only because the text went through drafts and reviews: consistency assurances ("we use the same value throughout"), justifications aimed at a reviewer, bookkeeping about unremarkable choices, announcements of a fix; reader-directed phrases ("what a reader needs", "the one fact the reader needs", "read one at a time"). State the value and use it; keep a convention note only where a reader comparing with other sources would be misled, as one clause about those sources. An internal label becomes a descriptive name defined in the text; an internal acronym survives only if it helps the reader and is defined at first use.
21. **Citations as content.** "Source: [12], Eq. (77)", "as defined in [12]", "see the docs for the format". State the content; keep the citation for credit.
22. **Unannotated master equations** (technical). When a central equation is a product or sum of distinct pieces the text then discusses one by one, label the pieces in the display (underbraces, one or two words each). Only for the few organising equations.
23. **Unbound reference and deep parse.** See below; no word list catches it.
24. **Clefts, emphatics, double negatives.** Clefts and pseudo-clefts ("What X needs is Y", "What remains is …"): say it directly. Sentence-final emphatics ("… at all.", "… on its own.", "… in its own right."). Double negatives ("not unlike", "not without").

## Pattern 23: sentence construction
The most damaging machine construction: every word can be plain and every sentence short while the paragraph is still hard to read. A reader builds one parse per sentence and links each referring expression to one antecedent; machine prose makes the reader hold several unresolved pointers or reparse after a wrong first parse. Review it as syntax: for each sentence, find every pointer, what it resolves to, and where the parse is fixed. Target: each sentence parses in one pass, and each pointer has exactly one antecedent, written as a noun phrase, in the same or the previous sentence.

**Binding failures**
- *Ambiguous pronoun:* it, its, they, them, their, this, that, these, those, which with several number-compatible candidates in this or the previous sentence, or whose antecedent is neither the nearest candidate nor the previous subject. Repeat the noun.
- *Pointer to a non-noun:* such X, all the same, this or that for a whole proposition, a spread-out predicate, or something stated only negatively ("has the energy but not the orientation" then "the missing alignment"). Name it as a noun phrase, then refer to that.
- *Quantifier pointers:* both, either, the former, the latter, that of, those of, the one, the other, the rest, only when the set was one coordinated noun phrase in the same sentence.
- *Definite before introduction:* "the rate", "the initial state" before the object exists in the text. Introduce it first (with "a", or by name and equation).
- *Relational noun without arguments:* missing, in between, mismatch, difference, ratio, correction, remainder, shift, excess, deficit, cost: say what from what, between what and what.
- *Several names for one referent:* "a complex that fixes the orientation", "the complex in between", "it". Name a technical object once and repeat exactly that name; no elegant variation.
- *Chained sentence-initial pointers:* successive sentences each opening on a pointer back (Such…, The complex…, It…). Merge the fragments or open on a named noun.

**Parse-depth failures**
- *Garden path:* a reduced relative read as the main verb ("a proton transferred or released a moment later takes it to…"). Use a full relative or an active clause.
- *Coordination scope:* does "transferred or released a moment later" put "a moment later" on both verbs? Write it so one scope is possible.
- *Left-heavy subject:* more than about eight words, or a relative clause, before the main verb. Short subject first.
- *Stacked prepositional or genitive chains* of three or more. Name the intermediate object.
- *Defining apposition:* "an activation barrier, the mismatch between its energy and that of the reactants". Use a clause or an equation reference.
- *Negation splitting a coordinated pair* ("fixes the orientation but not the charge … fixes both"). State each case positively.
- *Dangling modifier:* "Closing the contour there, the integral is…". Give the main clause the agent.

**Fixing one axis must not break the other.** Long sentences with nested relatives trade binding failures for depth failures; a split must not leave a sentence opening on a pointer back; a long noun phrase repeated three times where one unambiguous pronoun would do is a register failure.

Before: "The two molecules have the energy to react but not the orientation, and the collision rate gives almost nothing. The reaction runs all the same, because a catalyst can supply the missing alignment. The catalyst binds one molecule into a complex that fixes the orientation but not the charge, and a proton transferred or released a moment later takes it to a product that fixes both. The complex in between is never isolated. It enters the rate through an activation barrier, the mismatch between its energy and that of the reactants."

Failures: "not the orientation" stated only negatively; "the collision rate" never introduced; "all the same" points at a proposition; "the missing alignment" at a negated object; "a proton transferred" is a garden path with ambiguous "a moment later" scope; "it" has five candidates; "both" is a pair split by negation; "the complex in between" is a second name missing both arguments; "It" is a third name; the apposition defines the barrier with more pointers; "its" has two candidates.

After: "Collisions between the two molecules have enough energy for the reaction but rarely the right orientation, so the uncatalysed reaction is slow. A catalyst supplies the orientation. The catalyst binds one molecule into an intermediate complex that has the reactive orientation but not yet the charge distribution of the product. Transferring a proton then converts the intermediate complex into the product. The intermediate complex is never isolated; it enters the reaction rate through the activation barrier, which is the difference between the energy of the intermediate complex and the energy of the reactants."

**Repair pitfalls** (check every repair):
- *Meaning loss:* restating a negated pair ("conserves A but not B") as "same A, different B" can drop a claim. Check the content is unchanged.
- *One name, two referents:* check every other use of a new name in the document.
- *Over-repair:* a pronoun with one candidate that is the previous subject is correct; replacing it makes the prose robotic.
- *Strength drift:* adding "therefore", "since", "about", "only", or dropping "at least", a width or a range, changes the claim.
- *New garden paths and heavy subjects* from moving a clause or gerund in front of the verb.
- *Invented names:* "this procedure", "this causal form" for objects the text never named.

Writer rule: after drafting a paragraph, list each sentence's pointers and antecedents; rewrite any pointer with zero or several candidates. Reviewer rule: read the paragraph whole (binding crosses sentence boundaries) and report the pointer, its candidates and the rewrite.

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
Table: location | pattern | text | rewrite (for pattern 23, also the pointer and its candidates). Verdict: PASS (at most 3 minor hits per 1,000 words), REVISE, or REWRITE (systemic voice problems).
