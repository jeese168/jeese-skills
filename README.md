# jeese-skills

这是个人 Agent Skills 仓库。仓库只维护可直接编辑的 Skill 源码，不预先创建空 Plugin、发布包或多套平台副本。

当前包含：

- [`jeese-writing`](skills/jeese-writing/)：按 Jeese 的思考与表达习惯撰写、重构和修订中文技术文章与学习笔记。

## 仓库结构

```text
jeese-skills/
├── README.md
└── skills/
    └── jeese-writing/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/
```

只有 `skills/<skill-name>/` 是源码目录。目录内按实际需要保留 `SKILL.md`、`references/`、`scripts/`、`assets/` 和平台可选元数据，不创建没有用途的占位目录。

## 唯一真源

每个 Skill 只能有一份可编辑源码，位置固定为 `skills/<skill-name>/`。

- Agent 的用户级或项目级发现目录必须通过软链接或目录联接指向这里，不能复制一份再分别修改。
- 建立链接前先检查目标位置。若那里已有实体目录，应先迁移或合并内容，不能直接覆盖。
- 将来如果增加 Plugin 或发布包，它们只能由 `skills/` 生成；生成物不是编辑入口，也不能反向成为源码。
- 代码审查时，如果同名 Skill 同时出现为两个实体目录，应视为唯一真源被破坏。

## 平台适配边界

可移植部分遵循 [Agent Skills 开放规范](https://agentskills.io/)：`SKILL.md` 是入口，引用、脚本和资源与它放在同一个 Skill 目录中。

平台差异留在边界层：

- `agents/openai.yaml` 是 ChatGPT/Codex 的可选界面与调用元数据；不识别它的平台可以忽略该文件。
- Skill 的本机发现路径由各平台决定，不把机器相关的绝对路径提交进仓库。
- Codex 的个人发现路径是 `~/.agents/skills/`，并支持链接到仓库中的 Skill。其他 Agent 应按各自文档，把发现路径链接到同一个 `skills/<skill-name>/`。
- 只有出现跨用户安装、多个 Skill 打包或连接器依赖的真实需求时，才增加 Plugin 层。当前仓库不包含 Plugin。

OpenAI 当前的 Skill 结构、发现位置和软链接支持见 [Build skills](https://developers.openai.com/codex/skills)。

## 在本机建立发现链接

先确认目标不存在，或确认它只是需要替换的旧链接。不要对未经检查的实体目录执行覆盖命令。

macOS / Linux：

```bash
mkdir -p ~/.agents/skills
ln -s /absolute/path/to/jeese-skills/skills/jeese-writing ~/.agents/skills/jeese-writing
```

Windows PowerShell 可使用目录联接：

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"
New-Item -ItemType Junction -Path "$HOME\.agents\skills\jeese-writing" -Target "C:\absolute\path\to\jeese-skills\skills\jeese-writing"
```

如果平台使用别的发现目录，只替换链接位置，不复制 `skills/` 下的源码。

## 验证 Skill

新增或修改 Skill 后至少完成以下检查：

1. 使用 `skill-creator` 提供的 `quick_validate.py` 校验 Skill 目录。
2. 确认 `SKILL.md` 的 `name` 与目录名一致，`description` 能准确区分触发范围。
3. 确认 `SKILL.md` 引用的文件真实存在，没有未完成的脚手架占位内容。
4. 检查本机发现路径最终解析到仓库内的同一个实体目录。
5. 运行 `git diff --check`，再审阅实际差异。

验证器路径随 Codex 安装位置而变化，通用调用形式是：

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/jeese-writing
```
