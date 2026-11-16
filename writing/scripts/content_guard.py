#!/usr/bin/env python3
"""Check that a language-only edit left the content of LaTeX or Markdown files unchanged.

Usage: content_guard.py BASE_COMMIT FILE [FILE ...]    compare each working-tree file with BASE_COMMIT
       content_guard.py OLD_FILE NEW_FILE               compare two files
Compares the multisets of inline and display math, code spans and blocks, \\SI/\\num/\\qty, numbers in prose,
citation keys, labels and link targets. Repeating or dropping a repeat of an item that stays in the file, and
adding \\cref targets, are reported but allowed. An item new to the file, or one that disappears from it, is a stop.
Exit status 1 if any file has a stop.
"""
import os
import re
import subprocess
import sys
from collections import Counter

DISPLAY = r"equation|align|gather|multline|eqnarray"  # tables: their math, numbers and citations are compared item by item


def items(t, tex):
    out = Counter()
    if tex:
        t = re.sub(r"(?<!\\)%.*", "", t)
        for m in re.finditer(r"(?s)\\begin\{(%s)\*?\}(.*?)\\end\{\1\*?\}" % DISPLAY, t):
            out["display:" + re.sub(r"\s+", " ", m.group(2)).strip()] += 1
        t = re.sub(r"(?s)\\begin\{(%s)\*?\}.*?\\end\{\1\*?\}" % DISPLAY, " ", t)
    else:
        for m in re.finditer(r"(?ms)^```.*?^```", t):
            out["code:" + m.group(0)] += 1
        t = re.sub(r"(?ms)^```.*?^```", " ", t)
        for m in re.finditer(r"`([^`\n]+)`", t):
            out["code:" + m.group(1)] += 1
        t = re.sub(r"`[^`\n]+`", " ", t)
    for m in re.finditer(r"\$\$(.+?)\$\$|\$([^$]+)\$|\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S):
        out["math:" + re.sub(r"\s+", "", next(g for g in m.groups() if g is not None))] += 1
    t = re.sub(r"\$\$.+?\$\$|\$[^$]+\$|\\\(.*?\\\)|\\\[.*?\\\]", " ", t, flags=re.S)
    for m in re.finditer(r"\\(SI|num|qty|SIrange|numrange)\{([^}]*)\}(?:\{([^}]*)\})?", t):
        out["num:" + m.group(0)] += 1
    for m in re.finditer(r"\\cites?(?:\[[^\]]*\])*\{([^}]*)\}", t):
        for k in m.group(1).split(","):
            out["cite:" + k.strip()] += 1
    for m in re.finditer(r"\\label\{([^}]*)\}", t):
        out["label:" + m.group(1)] += 1
    for m in re.finditer(r"\]\(([^)\s]+)[^)]*\)|\\(?:url|href)\{([^}]*)\}|(?<![(\w{])(https?://[^\s)>\]}]+)", t):
        out["link:" + next(g for g in m.groups() if g is not None)] += 1
    prose = re.sub(r"\\(?:SI|num|qty|SIrange|numrange|cites?|label|[cC]ref|ref|eqref|url|href|includegraphics)\*?"
                   r"(?:\[[^\]]*\])*(?:\{[^}]*\})+|\]\([^)]*\)|https?://\S+", " ", t)
    for m in re.finditer(r"(?<![\w.])\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?%?(?![\w])", prose):
        out["number:" + m.group(0)] += 1
    return out


def refs(t):
    c = Counter()
    for m in re.finditer(r"\\[cC]ref(?:range)?\*?\{([^}]*)\}", t):
        for k in m.group(1).split(","):
            c[k.strip()] += 1
    return c


def compare(name, old, new, tex):
    o, n = items(old, tex), items(new, tex)
    lost = Counter({k: v for k, v in (o - n).items() if k not in n})      # item gone entirely
    flat = re.sub(r"\s+", "", old)
    gained = Counter({k: v for k, v in (n - o).items() if k not in o       # item new to the file
                      and not (k.startswith("math:") and k[5:] in flat)})  # unless it is a piece of existing math
    recount = sorted(set((o - n) | (n - o)) - set(lost) - set(gained))     # repeats of existing items
    ro, rn = refs(old), refs(new)
    rlost, rgain = Counter({k: v for k, v in (ro - rn).items() if k not in rn}), rn - ro
    if recount:
        print(f"note {name}: repeat count changed for {len(recount)} existing item(s)")
    if rgain:
        print(f"note {name}: added cref " + ", ".join(rgain))
    if not (lost or gained or rlost):
        return False
    print(f"STOP {name}")
    for k, v in lost.items():
        print(f"   - {v}x {k[:160]}")
    for k, v in gained.items():
        print(f"   + {v}x {k[:160]}")
    for k, v in rlost.items():
        print(f"   - {v}x cref {k}")
    return True


def main(a):
    if len(a) < 2:
        print(__doc__)
        return 0
    if len(a) == 2 and os.path.isfile(a[0]):
        bad = compare(a[1], open(a[0]).read(), open(a[1]).read(), a[1].endswith(".tex"))
    else:
        bad = 0
        for f in a[1:]:
            rel = subprocess.run(["git", "ls-files", "--full-name", f], capture_output=True, text=True).stdout.strip() or f
            old = subprocess.run(["git", "show", f"{a[0]}:{rel}"], capture_output=True, text=True).stdout
            bad += compare(f, old, open(f).read(), f.endswith(".tex"))
    print("content_guard: %d file(s) with a stop" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
