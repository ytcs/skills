---
name: burn-off
description: Repo burn-off procedure. Behaviour-preserving purge of everything not load-bearing, including every trace of the development process and of upstreams the end user or consumer does not need, to minimise codebase entropy and token spend; then a wasted-compute audit and a performance pass. Use when the user asks for a burn-off, or after a batch of features lands.
---

# burn-off

Goal: lowest practical entropy. What remains is what an end user or consumer needs, plus the gate. Behaviour, performance and output accuracy must not change.

Placeholders: `<gate>` is the repo's single pass/fail check (e.g. `bash tools/gate.sh`: lint with warnings-as-errors, then the test suite). `<entry>` is the repo's entry point(s): binary, CLI, `python -m pkg`, server, public API.

## 1. Preconditions
1. Start only when every agent and job has finished. Plan nothing before that.
2. Merge all branches and worktrees into the default branch; delete them (local and remote).
3. Baseline: `<gate>` passes. Record the benchmarks and profiles you care about before changing anything.

## 2. Manifest (read-only)
4. Classify each tracked file KEEP / GATE / COMPRESS / DELETE / UNCERTAIN by its references: imports/mods, executed scripts, `include_*`, build manifests and features, data reads, tests, benches, examples, skills, README, CLAUDE.md, hooks, config.
5. Load-bearing: `<entry>` and everything it reaches, with their tests, benches and fixtures; data the kept code reads; docs the code cites; README; config example; external API references the code implements; licences and notices that are legally required; the gate; this skill.
6. Development-process traces are not load-bearing (the umbilical cut, section 4). Mark them DELETE.
7. Also list: dead code in kept files (file:line), references that break when something goes, and hot-path port candidates.
8. Send the user one message: the counts, the UNCERTAIN questions with a recommended answer for each, and the process material worth archiving outside the repo before it goes. Wait for the reply.

## 3. Phases
One commit each, `<gate>` after each, push only if told.
9. **Delete** files that need no code change. Build, import-smoke every kept module, run the gate.
10. **Simplify code:** dead functions, flags, branches, shims, one-use helpers, features the user ablated. No numeric or behaviour change, no language ports.
11. **Umbilical cut** (section 4).
12. **Compress docs and skills** to a current-state snapshot (section 5).
13. **Comments:** keep one terse line only for a non-obvious invariant whose violation silently breaks correctness (SAFETY, units, cache keys, ordering, API quirks, information contracts). Prefer renaming. The readers are AI; code is self-documenting.
14. **Tests:** run the full suite one last time, then delete the out-of-gate tests the user agreed to drop.

## 4. Umbilical cut
15. The repo reads as if it had always been in its current form. Remove the following, after archiving whatever the user asked to keep.
16. Process artifacts: plans, roadmaps, stage and status files, evidence and experiment logs, briefs, agent returns, session notes, RESUME and TODO files, scratch scripts, ablation, sweep and comparison code, run outputs and caches.
17. Process language in code, names, docs and messages: stage, phase, round, attempt, ticket and agent IDs; "v2", "new", "old", "legacy", "fixed", "now", "previously", "we tried"; references to branches, PRs, worktrees, campaigns or tools used only during development. Rename identifiers that carry history (`foo_v2` becomes `foo`).
18. Upstreams: vendored or forked sources, submodules, pinned toolchains, CI configs, issue templates and docs inherited from an upstream and not used by the product; upstream git remotes; "based on" and "ported from" notes that no licence requires. Keep only the upstream code `<entry>` reaches, trimmed to what it reaches, with its required licence.
19. Dev tooling the consumer never runs (agent config, editor settings, personal hooks, local `.claude`/`.codex` dirs) leaves the tracked tree unless the gate or the shipped workflow uses it.
20. History: if the user wants it, graduate to a fresh single-commit repo (or squash) with neutral commit and author metadata. This is irreversible, so confirm first and keep the old repo as the archive.
21. Grep the tree for every removed name, ID and path, plus the process words above; only what the code needs to run may remain.

## 5. Docs and skills style
22. Keep every name and string that code, tests or hooks check. Grep the code before moving a doc path or heading.
23. Grep for each deleted file, command and option; no reference may remain.
24. Docs address the consumer: what it is, how to install, run, configure and use it, and its current behaviour and limits. No rationale, history or changelog narrative unless the product ships a changelog.
25. Skills: numbered, terse, imperative rules. No why unless the why is itself a rule. No history, no anecdotes. Aim for about a third of the size.
26. Leave the user's active work untouched; ask whether it ships before cutting it.

## 6. Agents
27. The manifest is one read-only agent.
28. If builds are cheap and independent, run non-overlapping worktree agents (e.g. code vs docs/skills; code that spans languages stays with one agent). Merge in phase order and run the gate after each merge.
29. If agents share a scarce build resource (a single target dir, a lock, a small tmpfs), run one agent at a time with phases in sequence.

## 7. Wasted compute (audit read-only first)
30. Look for work repeated on unchanged inputs: per-frame or per-tick recomputation, full-history recompute where an incremental update works, duplicate work across consumers, cache keys too fine or too coarse, redundant clones, copies or saves.
31. Fix with content or pointer keys and correct invalidation. Output stays bit-identical with no added latency, and each fix ships with a test that counts recomputations.

## 8. Performance pass
32. On a quiet machine, profile the recorded benches and real workloads. Optimise or port only what is hot.
33. Results stay bit-identical under the gate, or within stated tolerances (or statistically equivalent) for numerics. Report before/after numbers for each change.
