---
name: jeese-change-review
description: Explain completed edits to existing code, configuration, documentation, or Skills as a reviewable Simplified Chinese change handoff for Jeese. Use only when the user explicitly invokes this Skill or explicitly asks for its review format after changes are made. Focus on the actual diff, relevant surrounding context, affected behavior or meaning, and verification. Do not use to perform the change itself or define an engineering workflow.
---

# Jeese Change Review

Turn changes that have already been made into a reviewable explanation. The user should be able to approve, reject, or question each substantive modification without reopening every changed file merely to discover what happened.

For a focused modification to existing files, read [references/precise-edits.md](references/precise-edits.md). It contains the calibrated example for the current primary use case. Large greenfield additions are supported only by the general boundary below until real tasks provide better examples.

## Inspect the actual result

Read the current diff, requested commit, or other user-specified baseline before explaining anything. Use the changed files and their surrounding context as the source of truth; discussion and plans explain intent but do not prove what was implemented.

Identify the exact file, section, symbol, configuration key, or other object that changed. Use names that exist in the project. If a new concept was introduced by the change, define it and connect it to the concrete files or runtime objects that implement it.

Separate the requested changes from unrelated pre-existing modifications. Report the actual Git state—uncommitted, committed, pushed, or uncertain—only after verifying it.

## Match detail to the change

For a precise edit inside an existing artifact, preserve enough surrounding context to show what the edited passage or code already did, what changed, and how the new part fits. When the relevant block is short, show the complete before-and-after content. When it is long, quote the decisive fragment and summarize the surrounding definitions, conditions, callers, or neighboring paragraphs that complete its meaning.

For repeated mechanical edits, state the transformation, scope, count when useful, and one representative example. List every occurrence only when the user needs item-by-item verification.

For a new capability spanning many files, group the explanation by concrete module or observable capability. Name its entry points, important relationships, and externally visible behavior instead of narrating every created file. This is a starting rule rather than a fully calibrated large-change format; refine it only after real review tasks expose a stable need.

## Make each section independently reviewable

Use a heading only when it gives the user a useful approval unit. Write the heading as a compact statement of the concrete object and the implemented result, such as “`retry.go` 将固定次数改为读取服务配置”. Do not use a teaser question or an abstract heading such as “配置怎样配合” when the result is already known.

Within each section, keep together:

- the exact object and its role in the project;
- the relevant prior behavior or wording;
- the implemented behavior or wording;
- why the change was made and what it affects;
- the verification that actually supports the result;
- any decision that still needs the user.

These are information requirements, not a fixed six-part template. Integrate them into a coherent explanation and omit an item when it does not affect review. State the object before positional details: “`workflow.md` 的失败处理段落……” establishes identity; “它位于路由说明之后……” may then explain why the location matters.

Use project-relative paths in prose and clickable absolute file links when the interface supports them. Translate or paraphrase unfamiliar source language before relying on it. Quote the smallest self-contained passage that preserves the relevant subject, condition, relationship, contrast, and conclusion.

## Finish with verified state

End with checks that were actually run, their results, and any important check that remains unperformed. Mention commit and push state only when relevant to the user's review. Do not commit, push, publish, or modify external state merely because this Skill was invoked.

The handoff succeeds when the user can locate every substantive change, understand its effect and surrounding relationship, and respond to each independent decision without first reconstructing the implementation from the raw diff.
