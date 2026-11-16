#!/usr/bin/env python3
"""Prose lint for LaTeX or Markdown: banned terms, machine-prose tells, titles, equations, rhythm.

usage: lint.py FILE [FILE ...] [--banned TERMS.txt] [--max-dash 1.0] [--json]

Pattern numbers refer to references/prose.md. A hit is a candidate, not a verdict: read the sentence and decide;
technical uses of a flagged word stay. Exit 1 on a blocking hit (BANNED or RUG). Sentence construction
(pattern 23) needs binding.py.
"""
import argparse, json, re, statistics, sys
from collections import Counter

# (kind, prose.md pattern, blocking, case-sensitive, regexes)
CHECKS = [
    ("AI-PHRASE", 3, False, False, [r"\bdelve\w*", r"\bcrucial\w*", r"\bpivotal\b", r"\bintricat\w+", r"\brealm\b",
        r"\blandscape\b", r"\btapestry\b", r"\bseamless\w*", r"\bleverag\w+", r"\bunderscor\w+", r"\bshowcas\w+",
        r"\bnotably\b", r"\bplays? an? (key|vital|crucial|pivotal|important) role\b", r"\ba wide (range|array|variety) of\b",
        r"\bcutting[- ]edge\b", r"\bpowerful\b", r"\belegant\w*", r"\bunlock\w*", r"\bempower\w*", r"\bgame[- ]chang\w+",
        r"\bholistic\b", r"\bparadigm\b", r"\bnuanced\b"]),
    ("EVALUATION", 1, False, False, [r"\b(remarkabl[ye]|strikingly?|surprisingly|importantly|interestingly|naturally,|"
        r"of course|indeed,|in fact,|simply put|in short|in other words|put differently|that is to say|it turns out|"
        r"as it happens|the key (point|fact|step|ingredient|insight)|key insight|no accident|not a coincidence|"
        r"by no means|far from)\b"]),
    ("SIGNPOST", 2, False, False, [r"\bin this (section|chapter|post|article|guide|document|paper) we will\b",
        r"\blet us now turn\b", r"\bit is worth noting\b", r"\bit is important to note\b", r"\bit should be noted\b",
        r"\bneedless to say\b", r"\bas we will see\b", r"\bit goes without saying\b",
        r"\b(we (now )?(turn to|state|note|recall|emphasi[sz]e|stress|highlight|summari[sz]e)|as (we )?(noted|mentioned|"
        r"discussed|shown) (above|earlier|before)|here we|in what follows|below we)\b"]),
    ("VERDICT", 4, False, False, [r"\b(sufficient|necessary|correct|exact|true|right|safe|clean|valid) but (loose|crude|"
        r"weak|rough|slow|expensive|incomplete|limited)\b", r"\b(honest(ly)?|clean(ly)? (split|separation|answer|number|"
        r"result|picture)|sharp(ly)? (answer|statement|picture)|tidy|neat(ly)?|beautiful(ly)?|robust(ly)?|subtle|"
        r"delicate|nontrivial|non-trivial|rich structure)\b"]),
    ("HEDGE", 6, False, False, [r"\b(may|might|could) (perhaps|possibly|potentially|conceivably)\b",
        r"\bpotentially could\b", r"\bit (might|could) be argued\b"]),
    ("NEG-FRAME", 7, False, False, [r"\bnot (just |merely |only |simply )?[^.,;:]{2,45},? but (rather )?\b",
        r"\bnot (just|merely|only) [^.]{1,60}, it is\b",
        r", not (a|an|the|by|from|in|on|at|its|their|as|through|for|with|to|what|how|one)\b[^.;]{0,40}[.;]",
        r"\brather than (merely|simply|just)\b", r"\b(does|do) (little|nothing) more than\b|\bnothing (more|else) than\b"]),
    ("PERIPHRASIS", 8, False, False, [r"\bnever\b.{0,40}\b(anything|anyone)\b.{0,20}\b(except|but)\b",
        r"\bnothing\b.{0,30}\bexcept\b", r"\bhas yet to\b", r"\b(that|this|the) silence\b",
        r"\b(data|results?|numbers|silence|nature)\b (tells?|speaks?|whispers?|hides?)\b"]),
    ("METAPHOR", 8, False, False, [r"\b(earns? (its|their) (place|keep)|pays? (off|for itself)|turns? on (the|a|whether|how)|"
        r"has no standing|carr(y|ies) the (weight|burden|argument|story|day)|lives? (in|on|inside) (the|a|one)|"
        r"does the (job|work|heavy lifting)|buys?\b|at stake|the price (of|is)|hands? (it|them|over) (to|back)|"
        r"takes over\b|steps in\b|kicks in\b|comes? into play|enters? the picture|sets? the stage|paves? the way|"
        r"opens? the door|holds? the key|tells? the (story|whole)|the (whole|full) story|the story\b|the bottom line|"
        r"the upshot|the catch\b|the trick\b|the punchline)"]),
    ("TEASER", 11, False, True, [r"(?:^|[.]\s+)(?:Two|Three|Four|Five|Six|Several) (?:\w+ ){0,3}(?:matter|follow|stand out|"
        r"remain|are needed|differ|deserve|are worth|come from|are left)\b",
        r"\b(?:The|the) (?:answer|reason|point|catch|upshot|difference|result|lesson|moral|surprise)(?: is)?:"]),
    ("VAGUE", 14, False, False, [r"\bsignificantly\b", r"\bsubstantially\b", r"\ba large number of\b", r"\bquite\b",
        r"\b(somewhat|rather|fairly|relatively) (small|large|close|similar|different|important)\b"]),
    ("INTENSIFIER", 14, False, False, [r"\b(very|extremely|highly|truly|really|vastly|hugely) \w+"]),
    ("WORDY", 16, False, False, [r"\beach and every\b", r"\bfirst and foremost\b", r"\bin order to\b",
        r"\bdue to the fact that\b", r"\bat this point in time\b", r"\bthe fact that\b", r"\bin terms of\b",
        r"\bit is (clear|evident) that\b"]),
    ("PROCESS", 20, False, False, [r"\b(the|a|our) reader (needs|must|should|can|will|may|has)\b|\bwhat a reader\b|"
        r"\bthe one (fact|number|thing) (a|the|that)\b", r"\bread (one|two) at a time\b|\btaken one at a time\b"]),
    ("CLEFT", 24, False, True, [r"(?:^|[.;]\s+)What (?:\w+[ -]){1,7}(?:is|are|was|were)\b(?! (?:the |a )?(?:same|ratio|rate|"
        r"energy|value|number|probability|fraction|scale)\b)"]),
    ("EMPHATIC", 24, False, False, [r"\b(at all|on its own|by itself|in itself|in its own right)\."]),
    ("DOUBLE-NEG", 24, False, False, [r"\bnot (un\w+|in\w+able|without)\b|\bno (\w+ ){0,2}without\b"]),
    ("RUG", 0, True, False, [r"\bit can (easily )?be shown\b", r"\bstraightforward algebra\b", r"\bstandard manipulations?\b",
        r"\bone can show\b", r"\bit is easy to (see|show|verify)\b", r"\btrivially\b", r"\bobviously\b", r"\bclearly,"]),
]
COMPILED = [(k, n, b, [re.compile(r, 0 if cs else re.I) for r in rx]) for k, n, b, cs, rx in CHECKS]
GESTURE = (r"(?i)^(what|where|why|how|when)\b|\band (its|their) \w+$|^(putting|beyond|towards?|some|more on|"
    r"a (closer )?look)\b|\b(subtleties|story|landscape|journey|big picture)\b")
HEADING = re.compile(r"\\(?:part|chapter|section|subsection)\*?\{([^}]*)\}|^#{1,6}[ \t]+(.+)$", re.M)

def strip_line(ln, tex):
    if tex:
        ln = re.sub(r"(?<!\\)%.*", "", ln)
        ln = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)", " M ", ln)
        ln = re.sub(r"\\(?:c|C)ref(?:range)?\*?\{[^}]*\}(?:\{[^}]*\})?|\\(?:eq)?ref\{[^}]*\}|\\label\{[^}]*\}|"
                    r"\\cites?(?:\[[^\]]*\])*\{[^}]*\}", " REF ", ln)
        ln = re.sub(r"\\SI\{[^}]*\}\{[^}]*\}|\\num\{[^}]*\}", " NUM ", ln)
        ln = re.sub(r"\\(?:emph|textit|textbf|mathrm|text)\{([^}]*)\}", r"\1", ln)
    else:
        ln = re.sub(r"`[^`]*`", " C ", ln)
        ln = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", ln)
    return re.sub(r"\$[^$]*\$", " M ", ln)

def strip_markup(t, tex):
    t = re.sub(r"(?ms)^```.*?^```", " ", t)
    if not tex:
        t = re.sub(r"`[^`\n]*`", " C ", t)
    t = re.sub(r"(?m)^\|.*$", " ", t)
    t = re.sub(r"(?s)\\begin\{(equation|align|eqnarray|gather|multline)\*?\}.*?\\end\{\1\*?\}", " EQN ", t)
    t = re.sub(r"\$\$.*?\$\$", " EQN ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " M ", t)
    if tex:
        t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\(cite|ref|eqref|label)\{[^}]*\}", " ", t)
    return t

def lineno(raw, pos):
    return raw.count("\n", 0, pos) + 1

def lint(path, banned, maxdash):
    raw = open(path, encoding="utf-8").read()
    tex = path.endswith(".tex")
    hits = []
    def add(kind, what, line, txt, blocking=False):
        hits.append({"file": path, "line": line, "kind": kind, "pattern": what, "text": txt.strip()[:120], "blocking": blocking})
    fenced = False
    for i, ln in enumerate(raw.splitlines(), 1):
        if ln.startswith("```"):
            fenced = not fenced
            continue
        for p in banned:
            if re.search(p, ln):
                add("BANNED", p, i, ln, True)
        if fenced:
            continue
        p = strip_line(ln, tex)
        for kind, num, blk, rxs in COMPILED:
            seen = set()
            for m in (m for r in rxs for m in r.finditer(p)):
                if any(a <= m.start() < b for a, b in seen):
                    continue
                seen.add(m.span())
                ctx = p[max(0, m.start() - 50):m.end() + 50]
                add(kind, f"p{num}: {m.group(0).strip()}" if num else m.group(0).strip(), i, ctx, blk)
    body = re.sub(r"(?ms)^```.*?^```", lambda m: "\n" * m.group(0).count("\n"), raw)
    for m in HEADING.finditer(body):
        t = (m.group(1) if m.group(1) is not None else m.group(2)).strip()
        ln = lineno(body, m.start())
        if ":" in t or "?" in t or len(t.split()) > 6:
            add("TITLE", "p19: not a short noun phrase", ln, t)
        if re.search(GESTURE, t):
            add("TITLE-GESTURE", "p19: gestures instead of naming content", ln, t)
    for m in re.finditer(r"\\epigraph|(?:\\(?:part|chapter|section)\*?\{[^}]*\}|^#{1,6} .*)\s*\n\s*(?:\\begin\{quot|>)", body, re.M):
        add("EPIGRAPH", "p19: epigraph or opening quotation", lineno(body, m.start()), m.group(0))
    for m in re.finditer(r"(?s)\\begin\{(equation|align|gather|multline)\*?\}(.*?)\\end\{\1\*?\}", raw):
        eq = re.sub(r"\\label\{[^}]*\}|\\nonumber|\\notag", "", m.group(2)).rstrip()
        if eq and eq[-1] not in ",.;:":
            add("EQ-PUNCT", "display equation not punctuated", lineno(raw, m.start()), eq[-60:])
    text = strip_markup(raw, tex)
    for p in re.split(r"\n\s*\n", text):
        dashes = p.count("—") + (p.count("---") if tex else 0)
        if len(p.split()) > 20 and dashes > maxdash:
            pos = raw.find(p.strip()[:30])
            add("DASH", f"p10: >{maxdash} em dashes in paragraph", lineno(raw, pos) if pos >= 0 else 0, p.strip()[:80])
    sents = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)) if len(s.split()) > 2]
    lens = [len(s.split()) for s in sents]
    for s, n in zip(sents, lens):
        if n > 45:
            add("LONG-SENT", ">45 words", 0, s[:100])
    if len(lens) > 20:
        for k in range(len(lens) - 8):
            if statistics.pstdev(lens[k:k + 8]) < 2.5:
                add("MONOTONY", "p12: 8 sentences of near-equal length", 0, sents[k][:80])
                break
    return hits, len(text.split())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--banned")
    ap.add_argument("--max-dash", type=float, default=1.0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    banned = []
    if a.banned:
        banned = [l.strip() for l in open(a.banned, encoding="utf-8") if l.strip() and not l.startswith("#")]
    allh, words = [], 0
    for f in a.files:
        h, w = lint(f, banned, a.max_dash)
        allh += h
        words += w
    if a.json:
        print(json.dumps(allh, indent=1, ensure_ascii=False))
    else:
        for h in allh:
            print(f"{h['file']}:{h['line']}: [{h['kind']}{'!' if h['blocking'] else ''}] {h['pattern']} :: {h['text']}")
        kinds = Counter(h["kind"] for h in allh)
        print(f"-- {len(allh)} hits in {words} words ({1000 * len(allh) / max(words, 1):.1f} per 1000), "
              f"{sum(h['blocking'] for h in allh)} blocking; " + ", ".join(f"{k} {n}" for k, n in kinds.most_common()))
    sys.exit(1 if any(h["blocking"] for h in allh) else 0)

if __name__ == "__main__":
    main()
