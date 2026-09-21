---
name: jeese-docs-workflow
description: >-
  Create, revise, or merge Simplified Chinese learning notes, project explanations,
  technical retrospectives, and engineering proposals in Jeese's writing style.
  Use a staged file-based workflow with reusable content, explicit completion
  conditions, and executed artifact checks to produce durable documents.
  New learning documents and engineering proposals have separate four-stage
  paths; maintenance and merging have three stages each. Use for document work,
  not conversational explanations, code implementation, or social commentary and essays.
---

# Jeese Docs Workflow

把学习、项目探索和需求讨论形成的材料，写成可独立阅读、维护或用于工程协作的中文文档。核心风格以本 Skill 内的指导为准；阶段产物逐步完成内容整理、解释、设计和组织，供后续实际使用。

## 根据本次交付选择路线

| 本次要求 | 路线与阶段数 | 执行路径标识 `flow` |
| --- | --- | --- |
| 从材料形成新的学习笔记、项目理解文章或技术复盘 | 新文档：学习分支，四阶段 | `learning` |
| 围绕实际需求形成新的技术方案、设计文档或 PRD | 新文档：技术方案分支，四阶段 | `proposal` |
| 对指定的已有文档新增、删改、调整结构或整体重组 | 维护，三阶段 | `maintenance` |
| 明确将多篇独立文档合成一篇 | 合并，三阶段 | `merge` |

先遵循本次明确要求，再结合相关上下文判断。意图清楚就直接选择；只有歧义会改变交付时才问。例如讨论 Bug 或功能需求后要求“整理方案”，进入技术方案分支；学习机制后要求“整理笔记”，进入学习分支。参考多份资料写文章仍可属于新文档；只有明确合并多篇文档才进入合并路线。修改已有技术方案进入维护路线，同时应用技术方案指导。

一次沿一条执行路径推进。用户改变本次目标时重新判断，保留仍有效的材料。解释过某个内容不等于用户已理解或认可它，本文的目标与展开程度以本次要求为准。

## 共同准备，然后只读当前阶段

先读 [核心风格](references/core-style.md) 和 [共同准备](references/start.md)。准备完成后，按选定路径只读相应第一阶段：

- 学习：[准备内容与依据](references/learning-1-content.md) → 文章组织 → 完整初稿 → 核对成稿。
- 技术方案：[需求与现状](references/proposal-1-context.md) → 确认设计 → 方案初稿 → 核对成稿。
- 维护：[修改内容与影响](references/maintenance-1-scope.md) → 修订稿 → 写回核对。
- 合并：[来源与合并结构](references/merge-1-sources.md) → 合并初稿 → 核对成稿。

各阶段文件给出本阶段要读的指导、实际产物、完成条件和下一文件。达到完成条件并通过落盘检查后才读下一阶段指导。事实材料按当前查证需要读取。

学习和技术方案各有独立的四份阶段指导；共同风格与方法由内部 references 提供。全部运行材料位于本 Skill 内，不要求安装或先执行其他 Skill。

## 阶段执行与修正

每阶段使用有效的任务记录和所需前阶段产物，读取当前指导，实际加工内容并落盘，核对内容完成条件，再运行 [结构检查](references/artifact-checks.md)。两者都完成才继续；结构检查通过只说明结构有效。

核心风格贯穿过程。前期已经能判断的对象身份、概念解释、事实边界和因果关系，在当前产物中检查并修正；全文关系在组织时落实，整篇节奏和重复在成文后核对。中间产物保存实际完成的解释、设计、取舍、衔接或草稿，不以“已分析、已检查”替代内容，也不先写成稿再补阶段记录。

早期产物聚焦当前要解决的内容问题，原始材料保留为依据。完整初稿放在后期；局部维护按受影响范围形成修订稿。每阶段产物可以短，但必须能供后续使用，不按字数或固定栏目凑齐内容。

完整且有效的内容仍在上下文就复用；缺失、截断、压缩后只剩摘要或发生修订时，按结构检查约定补读需要的区块。每阶段的实际落盘和检查仍须执行。内容已在上下文不等于磁盘检查已完成。

发现事实错误，修正对应依据和受影响解释；发现概念缺口，补足实际说明；设计改变时更新依赖它的组织、图稿与正文。只重做受影响部分，修订后重跑对应检查点。若后续阶段尚未更新，在任务记录中明确失效范围，恢复时先处理这些变化。

默认连续执行并自检。真正影响本次交付的歧义、重要设计选择、无法解决的来源冲突或超出授权范围的改动，按当前阶段具体询问；已有明确安排直接执行。完成条件可通过限定结论和调整内容达到时，由 Agent 处理，不把一般材料整理变成用户问卷。

## 文档结构与写作依据

正式文档的结构依次依据：本次要求和目标项目明确约定；用户或项目指定的参考文档；同类、同受众文档中反复出现的稳定惯例。单篇文档只有被指定为参考时才建立约定。明确要求的模板属于任务要求；其他空白模板只在更强依据不足时作为参考。没有适用约定时按实际内容组织。

项目结构优先于个人 Markdown 默认值，兼容的核心风格继续保留。方案的工程讨论服务于本次文档，用户授权的文件修改范围仍有效；撰写方案不等于实施项目代码。

风格样例用于判断表达方式，事实按 [依据指导](references/evidence.md) 核对。审计或校准本 Skill 时才读 [语料观察](references/corpus-observations.md)。交付正式文档及重要变化、实际验证和未决事项，按最终阶段指导执行。
