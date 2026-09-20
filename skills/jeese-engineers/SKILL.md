---
name: jeese-engineers
description: >-
  Support Jeese's engineering handoff when explicitly invoked: list
  incremental or feature-related full file paths, generate a
  self-contained review prompt for the current work, independently verify
  returned findings into three dispositions, or explain completed changes
  at the requested depth. Also perform a standalone consistency review of
  specified existing technical or OpenSpec documents when explicitly
  requested. For explicitly requested workflow artifact review, dispatch a
  subagent, verify its findings into two dispositions, and correct intermediate
  artifacts. Use only when the user invokes jeese-engineers or an authorized
  workflow delegates that artifact review. This skill
  adapts handoff and explanation; it does not define an engineering workflow
  or author and advance OpenSpec changes.
---

# Jeese Engineers

用户手动调用本 Skill，选择要交付的产物。情况一至五保留现有交付方式，其中双窗口送审由用户自行搬运材料。情况六用于用户明确要求的 workflow 中间产物审查，由主 Agent 调度子 Agent，核实并修正产物后返回原工作流。

先判断**这一轮要交的产物是哪一种**。六种情况互斥：一次只走一条。用户指定了产物，就按指定走；没指定时，结合当前窗口上下文判断这条消息里贴来的材料。只有点名，或材料仍不足以确定任务时，先询问，等用户确认再进入对应情况。对照少样本：[指定了就按指定、有材料就按材料](references/examples-and-counterexamples.md#指定了就按指定有材料就按材料)、[只有点名时询问或按进度推荐](references/examples-and-counterexamples.md#只有点名时询问或按进度推荐)、[有材料但任务仍不明确时针对歧义询问](references/examples-and-counterexamples.md#有材料但任务仍不明确时针对歧义询问)。

**用户指定了。** 这句话里已经点明要落盘路径、生成送审指令、独立核查指定文档、核实返回的意见，或讲解改动：按指定进入对应情况。用户只写了 `/jeese-engineers`，但同一条消息里已经带了材料的，结合上下文判断任务。

**用户要求审查 workflow 中间产物。** 用户直接点名情况六，或在 workflow 中明确要求最终生成前用子 Agent 检查中间产物时，进入情况六，不要求再点一次本 Skill。不因出现 `work.md`、Markdown 或“检查一下”就自动派子 Agent；需要明确的中间产物独立审查意图。情况六接收到自己派出的子 Agent 发现时继续情况六，不切到情况四。

**没指定，但材料对得上。** 执行窗口收到按条列出对象、问题、建议的审查发现，当前上下文也表明这是送回来的意见时，直接进入情况四。仅有文件路径、方案文字或问题列表，还不足以证明用户要独立核查文档；情况三需要清楚的文档核查意图。

**双窗口送审的交接。** 情况二生成的指令包含审查任务和回复要求，用户自行拼接对象后交给审查窗口。审查窗口直接执行这份指令，无需再次调用本 Skill。若用户仍在完整指令旁点名本 Skill，按已经明确的指令执行；这不改变情况三的独立文档核查用途。同一审查窗口的后续复查沿用已收到的指令，并以用户的新要求和新材料为准。

**只有点名。** 用户就是发了 `/jeese-engineers` 或同等点名，同一条里没有指定、也没有上面那些材料：停下来问这一轮要交什么。问法跟着当前窗口走，可以给一个推荐，例如刚改完代码、路径还没交，推荐先做情况一；路径已经有了、审查指令还没有，推荐情况二。推荐之后等用户应一声再做。所有产物做成固定选择题、每轮都点一遍，不是这一步要的问法。

**有材料，但任务仍不明确。** 结合材料和当前上下文仍无法确定要做哪一种时，说明最可能的理解，针对实际歧义问一句，等用户确认。材料足以确定任务时，直接进入对应情况。

认准后只进入对应情况，读取它的 reference 和其中指向的必要资料，按给出的少样本标题对照。

用户说「全量」或「存量」时，都按全量处理：收齐和当前功能、需求相关的已落盘文件。用户说「增量」时，只收本次指定的修改任务中实际落盘的文件；事后单独索要路径时，指向用户所指的那次已完成修改。

## 情况一：列出实际落盘文件的绝对路径

在下面任一时机进入：

- 用户让执行窗口开始写方案、写代码、写文档、改 Skill 或改配置，并顺带点名本 Skill，要求做完后交出落盘路径；
- 正事已经做完、当时没有交路径，用户再引用本 Skill，只要刚才那次修改落到磁盘上的地址。

先确认这一轮是增量还是全量。用户在当前这句话、或同一任务里已经说过，就按已说的执行。当前也没说、前面也没说时：只问这一句，问清之前停在提问。正事还没开始的，确认范围后再开始改文件。

确认之后：若用户是在开始干活时顺带点名的，先完成用户要的正事，等实际落盘结束，再交路径。若用户只是单独来要路径，只交路径。

产物是已经写到磁盘上的文件路径，并说明每个路径在本任务里是什么。默认给绝对路径；当前工作区内的文件，用户只要相对路径时给仓库相对路径即可。范围包括代码、文档、Skill、配置。

读 [references/landed-paths.md](references/landed-paths.md)。

## 情况二：为当前方案或改动生成完整送审指令

时机是改完、输出完，也包括情况一的路径已经整理完之后，用户再点名，要求生成审查指令。

产物是直接打在对话里的一份可独立使用的审查指令。它围绕当前方案或改动，写清审查对象、背景、范围、判断依据、与相关实现的配合，以及审查意见怎样回复。执行窗口自己的实现选择也应接受核对。

读 [references/review-brief.md](references/review-brief.md)。

用户会自己把原始材料或路径包起来，再拼上这份指令，贴到审查窗口。拼接是用户的工作。

## 情况三：独立核查指定的已有技术文档

用户明确要求检查指定的已有技术方案、技术笔记或 OpenSpec 文档，核对它与当前代码、相关约定或适用的外部技术资料是否一致时进入。对象可以在当前工作区之外，按用户给出的绝对路径读取。

这是低频、保守触发的直接核查。仅出现 Markdown 路径、OpenSpec 名称或文档可能过时的迹象时，保持当前任务；核查意图明确但对象或依据不清时，针对缺口询问。

产物是直接打在对话里的核查发现、依据和建议。区分文档过时、实现偏离约定、计划尚未实施，以及证据不足；文件修改由用户后续指令决定。

读 [references/document-review.md](references/document-review.md)。

## 情况四：执行窗口把审查结论核实成三类

用户把审查窗口写好的发现丢回执行窗口。用户点了核实、分类、整理成三类，或只在这份发现的首尾加了本 Skill 的点名，都走这里。

先对着方案、用户给出的路径或磁盘上的实际文件自己查，再划分：

1. **认可**：执行窗口确认这项成立，可以采纳；
2. **不采纳**：已有可核对证据，足以排除审查意见的关键前提，确认这项不成立；
3. **争议、待用户判断**：证据不足以判定、双方对取舍有分歧，或两边都认为该改、但还要用户自己判断或去问产品、leader、客户端。这一类写清待决点，并给出参考意见和推荐选项。

产物是这三类的整理说明。这一轮只整理。

读 [references/review-disposition.md](references/review-disposition.md)。

## 情况五：讲已经改了什么

在中间或更晚，用户要求讲清楚已经发生的改动时进入。再看用户要的是哪一种深度：

- 用户只问某一个点、某一处行为、某一个文件为什么这样改：只答这一点，让用户能接着读代码或接着问下一句。
- 用户要拿去做笔记、归纳、沉淀，或明确要求把相关改动讲全：按磁盘上的实际改动把该讲的部分讲完整。

读 [references/explain-changes.md](references/explain-changes.md)。

## 情况六：审查并修正 workflow 中间产物

用户明确要求独立审查时，由主 Agent 将本次理解目标、范围、深度、必要背景和中间产物交给一个子 Agent 检查。子 Agent 只返回发现；主 Agent 自己核实，按「采纳／不采纳」处理，并直接修正本次中间产物。

不复用情况二的手动搬运和回合结束，不复用情况四的第三类拍板或只整理不修改。审查与修正仅限本次中间产物及其图文，不修改被解释的代码、项目配置或 Skill 本身。不增加一套增量／全量询问。

产物是经过核实修正的中间材料及简短处置记录。完成后继续调用方原来的工作流，不把审查报告作为最终讲解交给用户。子 Agent 收到完整审查指令后直接执行，不再加载本 Skill 或派出另一层 Agent。

读 [references/workflow-artifact-review.md](references/workflow-artifact-review.md)。

## 少样本

正例和反例在 [references/examples-and-counterexamples.md](references/examples-and-counterexamples.md)。各情况的 reference 会指向需要对照的标题。进入某一情况时读那些标题，不必整份通读。
