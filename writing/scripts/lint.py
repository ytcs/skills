#!/usr/bin/env python3
"""Prose, style and banned-term lint for LaTeX or Markdown sources.

usage: lint.py FILE [FILE ...] [--banned TERMS.txt] [--max-dash 1.0] [--json]

Pattern numbers refer to references/prose.md. Exit 1 on a blocking hit (banned term or RUG).
"""
import argparse, json, re, statistics, sys

AI_PHRASES = [r"\bdelve\w*", r"\bcrucial\w*", r"\bpivotal\b", r"\bintricat\w+", r"\brealm\b", r"\blandscape\b",
    r"\btapestry\b", r"\bseamless\w*", r"\bleverag\w+", r"\bunderscor\w+", r"\bshowcas\w+", r"\bnotably\b",
    r"\bplays? an? (key|vital|crucial|pivotal|important) role\b", r"\ba wide (range|array|variety) of\b",
    r"\bcutting[- ]edge\b", r"\bpowerful\b", r"\belegant\w*", r"\bunlock\w*", r"\bempower\w*",
    r"\bin the realm of\b", r"\bgame[- ]chang\w+", r"\bholistic\b", r"\bparadigm\b", r"\bnuanced\b"]
SIGNPOST = [r"\bin this (section|chapter|post|article|guide|document|paper) we will\b", r"\blet us now turn\b", r"\bit is worth noting\b",
    r"\bit is important to note\b", r"\bit should be noted\b", r"\bneedless to say\b", r"\bas we will see\b",
    r"\bit goes without saying\b", r"\binterestingly,", r"\bimportantly,", r"\bremarkably,"]
HEDGES = [r"\bmay potentially\b", r"\bcould possibly\b", r"\bmight possibly\b", r"\bpotentially could\b",
    r"\bit (might|could) be argued\b"]
VAGUE = [r"\bsignificantly\b", r"\bsubstantially\b", r"\ba large number of\b", r"\bvery\b", r"\bquite\b"]
RUGS = [r"\bit can (easily )?be shown\b", r"\bstraightforward algebra\b", r"\bstandard manipulations?\b",
    r"\bone can show\b", r"\bit is easy to (see|show|verify)\b", r"\btrivially\b", r"\bobviously\b",
    r"\bclearly,"]
WORDY = [r"\beach and every\b", r"\bfirst and foremost\b", r"\bin order to\b", r"\bdue to the fact that\b",
    r"\bat this point in time\b", r"\bthe fact that\b", r"\bin terms of\b", r"\bit is (clear|evident) that\b"]
PERIPHRASIS = [r"\bnever\b.{0,40}\b(anything|anyone)\b.{0,20}\b(except|but)\b", r"\bnothing\b.{0,30}\bexcept\b",
    r"\bdoes little more than\b", r"\bhas yet to\b", r"\b(that|this|the) silence\b",
    r"\b(data|results?|numbers|silence|nature)\b (tells?|speaks?|whispers?|hides?)\b"]
NEGFRAME = [r"\bnot (just|merely|only) [^.]{1,60}, (but|it is)\b", r"\brather than merely\b"]
LINE_CHECKS = (("AI-PHRASE", AI_PHRASES, False), ("SIGNPOST", SIGNPOST, False), ("HEDGE", HEDGES, False),
    ("VAGUE", VAGUE, False), ("RUG", RUGS, True), ("NEG-FRAME", NEGFRAME, False), ("WORDY", WORDY, False),
    ("PERIPHRASIS", PERIPHRASIS, False))
GESTURE = (r"(?i)^(what|where|why|how|when)\b|\band (its|their) \w+$|^(putting|beyond|towards?|some|more on|"
    r"a (closer )?look)\b|\b(subtleties|story|landscape|journey|big picture)\b")
HEADING = re.compile(r"\\(?:part|chapter|section|subsection)\*?\{([^}]*)\}|^#{1,6}[ \t]+(.+)$", re.M)

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
    hits = []
    def add(kind, pat, line, txt, blocking=False):
        hits.append({"file": path, "line": line, "kind": kind, "pattern": pat, "text": txt.strip()[:120], "blocking": blocking})
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
        low = ln.lower()
        for kind, pats, blk in LINE_CHECKS:
            for p in pats:
                if re.search(p, low):
                    add(kind, p, i, ln, blk)
    body = re.sub(r"(?ms)^```.*?^```", lambda m: "\n" * m.group(0).count("\n"), raw)
    for m in HEADING.finditer(body):
        t = (m.group(1) if m.group(1) is not None else m.group(2)).strip()
        ln = lineno(body, m.start())
        if ":" in t or "?" in t or len(t.split()) > 6:
            add("TITLE", "title not a short noun phrase (pattern 19)", ln, t)
        if re.search(GESTURE, t):
            add("TITLE-GESTURE", "title gestures instead of naming content (pattern 19)", ln, t)
    for m in re.finditer(r"\\epigraph|(?:\\(?:part|chapter|section)\*?\{[^}]*\}|^#{1,6} .*)\s*\n\s*(?:\\begin\{quot|>)", body, re.M):
        add("EPIGRAPH", "epigraph or opening quotation", lineno(body, m.start()), m.group(0))
    for m in re.finditer(r"(?s)\\begin\{(equation|align|gather|multline)\*?\}(.*?)\\end\{\1\*?\}", raw):
        eq = re.sub(r"\\label\{[^}]*\}|\\nonumber|\\notag", "", m.group(2)).rstrip()
        if eq and eq[-1] not in ",.;:":
            add("EQ-PUNCT", "display equation not punctuated", lineno(raw, m.start()), eq[-60:])
    tex = path.endswith(".tex")
    text = strip_markup(raw, tex)
    for p in re.split(r"\n\s*\n", text):
        dashes = p.count("—") + (p.count("---") if tex else 0)
        if len(p.split()) > 20 and dashes > maxdash:
            pos = raw.find(p.strip()[:30])
            add("DASH", f">{maxdash} em dashes in paragraph", lineno(raw, pos) if pos >= 0 else 0, p.strip()[:80])
    sents = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)) if len(s.split()) > 2]
    lens = [len(s.split()) for s in sents]
    for s, n in zip(sents, lens):
        if n > 45:
            add("LONG-SENT", ">45 words", 0, s[:100])
    if len(lens) > 20:
        for k in range(len(lens) - 8):
            if statistics.pstdev(lens[k:k + 8]) < 2.5:
                add("MONOTONY", "8 sentences of near-equal length (pattern 12)", 0, sents[k][:80])
                break
    return hits

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
    allh = [h for f in a.files for h in lint(f, banned, a.max_dash)]
    if a.json:
        print(json.dumps(allh, indent=1, ensure_ascii=False))
    else:
        for h in allh:
            print(f"{h['file']}:{h['line']}: [{h['kind']}{'!' if h['blocking'] else ''}] {h['pattern']} :: {h['text']}")
        print(f"-- {len(allh)} hits, {sum(h['blocking'] for h in allh)} blocking")
    sys.exit(1 if any(h["blocking"] for h in allh) else 0)

if __name__ == "__main__":
    main()
