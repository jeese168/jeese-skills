---
name: jeese-change-review
description: Review specified code, configuration, documentation, or Skills, or explain completed edits to them, as a reviewable Simplified Chinese report for Jeese. Use only when the user explicitly invokes this Skill or explicitly asks for its review format. Focus on actual files or diffs, relevant surrounding context, confirmed findings or changes, effects, evidence, and recommended next actions. Do not use to perform the change itself or define an engineering workflow.
---

# Jeese Change Review

Turn an explicitly requested review or changes that have already been made into a reviewable explanation. The user should be able to approve, reject, or question each substantive finding or modification without reopening every file merely to discover what happened.

For a focused modification to existing files, read [references/precise-edits.md](references/precise-edits.md). It contains the calibrated example for precise edits. Large greenfield additions currently follow only the paragraph for a new capability spanning many files under `Match detail to the change` until real tasks provide better examples.

For an explicit review of code, configuration, documentation, or a Skill, read [references/review-findings.md](references/review-findings.md).

## Inspect the actual files and comparison target

Read the actual files and, when reviewing changes, the current diff, requested commit, or other user-specified comparison target before explaining anything. Use the files and their surrounding context as the source of truth; discussion and plans explain intent but do not prove what exists or was implemented.

Identify the exact file, section, symbol, configuration key, or other object being reviewed or changed. Use names that exist in the project. If a new concept was introduced by the change, define it and connect it to the concrete files or runtime objects that implement it.

Separate the requested changes from unrelated pre-existing modifications. Report the actual Git state—uncommitted, committed, pushed, or uncertain—only after verifying it.

Distinguish the evidence level behind each conclusion:

- **Implementation fact**: the current code, configuration, or document contains a verified structure or statement;
- **Observed result**: an executed test, log, command, or manual check shows what actually happened;
- **Inference**: static relationships or available context support a likely result, but it has not been directly observed;
- **Recommendation**: a proposed future change rather than the current state.

Name the supporting evidence and its limit when that distinction affects the user's decision. The existence of an interface, branch, configuration key, or test case proves that the structure exists; without execution evidence, it does not by itself prove that the behavior occurred, the feature works end to end, or the test passed.

## Match detail to the change

For a precise edit inside an existing artifact, preserve enough surrounding context to show what the edited passage or code already did, what changed, and how the new part fits. When the relevant block is short, show the complete before-and-after content. When it is long, quote the decisive fragment and summarize the surrounding definitions, conditions, callers, or neighboring paragraphs that complete its meaning.

For repeated mechanical edits, state the transformation, scope, count when useful, and one representative example. List every occurrence only when the user needs item-by-item verification.

For a new capability spanning many files, group the explanation by concrete module or observable capability. Name its entry points, important relationships, and externally visible behavior instead of narrating every created file. This is a starting rule rather than a fully calibrated large-change format; refine it only after real review tasks expose a stable need.

## Make each section independently reviewable

Use a heading only when it gives the user a useful approval unit. Write the heading as a compact statement of the concrete object and the implemented result, such as “`retry.go` 将固定次数改为读取服务配置”. Do not use a teaser question or an abstract heading such as “配置怎样配合” when the result is already known.

Within each section, keep together:

- the exact object and its role in the project;
- the relevant current behavior and, for a change, its prior behavior or wording;
- the implemented result or confirmed review finding;
- why the change was made and what it affects;
- the verification or evidence that actually supports the result or finding;
- the recommended change or any decision that still needs the user.

These are information requirements, not a fixed six-part template. Integrate them into a coherent explanation and omit an item when it does not affect review. State the object before positional details: “`workflow.md` 的失败处理段落……” establishes identity; “它位于路由说明之后……” may then explain why the location matters.

When a finding or change crosses clients, services, processes, runtime layers, permission actors, or state stages, define each participant's Chinese name, layer, and responsibility before using a bracketed label. Project terms such as `[Client]`, `[DS]`, and `[GS]` may be retained after their meanings are established. Then use those labels consistently to show who acts, what state moves, and who is affected. Choose labels that match the actual system; do not infer responsibilities from an abbreviation, and do not force labels onto a single-participant change.

Use project-relative paths in prose and clickable absolute file links when the interface supports them. When a conclusion needs to be rechecked, give the project-relative path, section or symbol, and a current line number when useful. Treat the line number as a pointer to the inspected version rather than a permanent identifier, and recheck it after the file changes. Translate or paraphrase unfamiliar source language before relying on it. Quote the smallest self-contained passage that preserves the relevant subject, condition, relationship, contrast, and conclusion.

Explain each substantive finding or modification once in the section where it belongs. An opening may state the inspected scope and overall result; the ending should contain only actual verification, checks not performed, and decisions still needed. Do not repeat the same findings or changes as another summary list.

## Finish with verified state

End with checks that were actually run, their results, and any important check that remains unperformed. Mention commit and push state only when relevant to the user's review. Do not commit, push, publish, or modify external state merely because this Skill was invoked.

The report succeeds when the user can locate every substantive finding or change, understand its effect and surrounding relationship, and respond to each independent decision without first reconstructing the implementation from the raw files or diff.
