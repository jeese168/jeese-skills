---
name: jeese-essays-workflow
description: >-
  Turn existing discussions, chat transcripts, AI summaries, or rough drafts into
  Simplified Chinese social commentary, relationship essays, and personal reflections
  in Jeese's voice. Use a three-stage writing workflow to create, revise, or merge
  essays while preserving the author's stance and expression. Deliver illustration
  prompts and FIG captions, and optionally format approved Markdown as print HTML
  or PDF using the bundled template. Use for writing from existing ideas, not
  open-ended discussion, technical plans, or instructional project documentation.
---

# Jeese Essays Workflow

把用户已经表达的意思写成自然、连贯、有作者立场的文章。输入可以是原始聊天、其他 AI 的复述、条目化草稿或已有文章。本次要求决定目标，上下文帮助理解；用途和表达倾向已经明确时直接采用，只有影响主张、来源取舍或修改范围的实质歧义才具体询问。

## 读取与执行

| 本次工作 | 读取与执行方式 |
| --- | --- |
| 新写、修改、追加或合并文章 | 完成下方准备，完整读取 [核心风格](references/core-style.md) 与 [写作流程](references/workflow.md)，按三个阶段依次执行 |
| 准备配图或接入已有图片 | 在处理图位前读取 [配图与 FIG](references/illustrations.md)，交付位置、完整生图提示词与图注；本 Skill 不执行生图 |
| 仅将已有成稿排成 HTML／PDF，或调整打印版面 | 确定下方路径后直接读取 [打印与导出](references/print-export.md)；正文需要改写时先完成对应写作工作 |

写作流程集中为三个阶段：整理原意与主线 → 写清关键论述 → 形成全文并立即核对修订。每阶段消费有效的前阶段产物，实际加工内容、落盘，满足内容完成条件并运行结构检查后，才进入下一阶段。具体产物、命令和修正方式在流程文件中。

核心风格从第一阶段就应用于实际内容，后续继续使用。所需指导和产物完整、有效且已在上下文时复用；缺失、截断、压缩后只剩摘要或磁盘修订时，按流程目录补读相应完整章节与产物。每阶段落盘后的实际检查仍须执行。阶段产物与脚本提高执行稳定性，不构成平台强制保证。

## 准备与路径

依次采用：本次明确指定的位置；当前项目适用的 `AGENTS.md` 等规则；当前 Agent 适用的全局规则，例如全局 `AGENTS.md`、`CLAUDE.md` 或所在平台的用户规则。只查本平台适用位置与明确引用，不扫描其他平台配置或整个主目录。

整理已知位置，把仍缺失的正文、HTML／PDF 和中间产物位置一次性具体询问，然后等待回答。只询问实际缺口；没有指定导出时，目录可一并问清但不因此启动导出。

用户只给一个路径时，按共用目录处理：Markdown、HTML、PDF 均可输出到该目录，中间产物在该目录下按文章建立任务子目录。用户给出分别存放的位置时遵循；项目明确约定 HTML 和 PDF 进入 `HTML/` 时采用该约定。本次明确共用一个目录的要求优先。

正式文件使用稳定篇名，分别为 `.md`、`.html`、`.pdf`。篇名可由 Agent 根据材料拟定，用户已指定就沿用。目标已有内容且本次替换意图不清楚时，问清冲突；明确更新原文则在授权范围内修改。

实体图片默认放在 Markdown 正文所在目录下的 `文档图片/`，正文使用相对引用。该习惯用于用户已提供或已渲染的图片文件；Mermaid、PlantUML 和文字简图的代码留在适用文档或阶段产物中，导出实体图时再按图片路径处理。已有项目或本次指定的图片位置优先。

## 任务记录与交付

按文章建立不冲突的任务子目录，默认使用 `work.md` 保存任务说明与阶段产物。同一文章的修订复用目录；确实换文章时分开记录，目录选择不清楚才询问。

记录影响后续工作的实际信息：本次要求、输入来源、写作操作、作者已明确的态度及表达偏好、输出位置、是否需要导出、已有图片与待交付提示词。若用户指定先看某个中间结果，就在那个位置等待；其他情况按完成条件连续推进。

本次用途、有效来源和必要路径明确后进入相应工作。Markdown 是正文源；工作记录、生图指令和正式正文分别存放。HTML／PDF 在用户要求时生成。最终交付可打开的正文与提示词链接，并如实说明配图、导出及检查状态。

本 Skill 自包含，原始文章、聊天与本机路径不是运行依赖。
