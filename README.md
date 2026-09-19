# Invariant First · 工程技能路由包

**选对方法，直接做完，让下一位接得住。**

这是构建优先、跨 harness 的工程 Skills：按目标选方法，做完整实现，留下清楚的架构和可用文档。提供可选的路由程序、独立技能、失速恢复和跨会话接续；不把它们变成每次开发都要经过的流程。

初衷在 [RULES](RULES.md)：减少不必要的防御与猜测性设计，但不省略真实责任；工程判断要落到成果，而不是更长的计划和验证报告。维护本仓库先读 [AGENTS](AGENTS.md)，本次改动见 [CHANGELOG](CHANGELOG.md)。

## 安装与第一次使用

解压完整 `invariant-first/`，放到当前工具实际支持的 Skills 目录；不要只复制 SKILL.md。工具的发现目录与安装操作遵循该工具说明，本包不声称所有 harness 有统一安装路径。

加载后直接给任务：

```text
使用 invariant-first 实现这个功能。保持现有 CLI 行为，完成代码和真实用法。
```

模型从 [SKILL.md](SKILL.md) 读取[共同规则](RULES.md)，按目标选 PRIMARY，直接读取需要的技能并行动。普通任务无需执行路由脚本或生成 JSON；你不需要替模型选路线。需要接续或从失速中恢复时，先恢复事实与进展，再继续原任务。

包中有两种分发形态，规则相同：完整路由包保留独立子技能入口；单入口导出版只有根 SKILL.md，其他方法是 GUIDE.md 资源，供不能导入多个 Skill 的工具使用。具体边界见[可移植性](references/portability.md)。

## 批量、集成或诊断：运行同源路由程序

已有 Python 3.10+ 时，在 `invariant-first/` 目录运行；无第三方依赖，不联网，不改项目文件：

```sh
python scripts/route.py --request examples/route-request.json --format text
```

这个示例的当前目标是修复重复写入，然后准备安装包，不执行公开部署。预期关键输出是：

```text
PRIMARY -> skills/if-fix/SKILL.md
LOAD_NOW: skills/if-fix/SKILL.md, skills/if-state/SKILL.md, skills/if-contracts/SKILL.md
NEXT (requested only): release
```

完整真实输出保存在 [examples/route-output.json](examples/route-output.json)。路由结果不是已经修好了代码；主入口要求继续读取 PRIMARY 并执行 ACTION。

也可以直接输入任务：

```sh
python scripts/route.py --task "修复重复写入问题" --intent fix --facts shared_state,external_effects,external_consumers
```

`--intent` 是明确的工程目标，优先于关键词。省略它时只得到候选分类，需由 Agent 对照真实请求确认；脚本不是任意语言的完整语义理解器。`--facts` 只填写已经确认的条件，不能把猜想当事实。

[同源分流表](MASTER-ROUTING.md)始终可直接使用，不限于缺少 Python 时。意图已经明确就读对应方法，不为纠正关键词候选反复执行脚本，不为路由安装运行时。

## 生命周期与专项能力

主路线覆盖：定向与接手 frame、预览与功能 build、审查 review、发布 release、运行 operate、修复 fix、优化 optimize、重构迁移和转向 evolve、退役 retire、文档 document。已经完成的阶段不会重新执行，一个小修复不需要走完生命周期。

专项只在触发时加入：architecture 解决表示与责任；contracts 处理真实兼容；state 处理安全、持久化和并发；dependencies 核对包与 API；interface 接通真实交互；recovery 打破无效循环；handoff 接续新会话。

完整路径与触发条件见 [INDEX](INDEX.md)，事实、别名、优先级与路径的唯一来源是 [routing.json](config/routing.json)。事实只属于本次修改，不是全仓技术清单。即时专项按配置顺序选择：需要恢复上下文时 handoff 在前，然后 recovery，再处理领域边界；其余专项在真正用到之前读取。

## 路由不是一张阶段标签表

```text
用户目标 + 当前事实
  → PRIMARY：眼前要交付什么
  → SUPPORT：这次真正难在哪里
  → CAPABILITIES：现有工具能怎样执行
  → ACTION：立即改代码、写正文或形成判断
  → DONE：当前约定成果完成
  → NEXT：只继续用户已请求的后续工作
```

“修 bug，必要时重构”仍走 fix；“审查迁移”走 review 而不是改库；“写故障手册”走 document 而不是操作线上。卡住加载 recovery，但不改变原目标。新项目不造兼容，已有真实依赖则守外部契约，内部可以直接简化。

默认不会创建路由日志、全仓索引或任务数据库，不自动下载工具，不用关键词授予操作权限。缺能力时提供可应用成果与真实缺口；有能力与权限就继续执行，不把可逆选择推回给用户。

`CAPABILITIES.preferred` 与 `missing` 只计算 PRIMARY 和 LOAD_NOW，`deferred` 单列后续专项独有的能力。例如写文档时尚未加载界面专项，不会先要求交互工具。字段表示当前有用的手段而非强制门槛；没有某种工具，先用能完成目标的等价能力。

## 源码地图

```text
AGENTS.md                本仓库的初衷与维护落点
SKILL.md                 总入口与加载契约
RULES.md                 构建、架构、文档和授权底线
config/routing.json      唯一路由事实源
MASTER-ROUTING.md         生成的无脚本路由视图
INDEX.md                 生成的能力地图
skills/if-*/SKILL.md      独立主路线和专项方法
scripts/route.py          只读分派器
scripts/catalog.py        生成视图与检查漂移
scripts/export_single.py  单入口导出，不分叉规则
experience/README.md     项目经验回流边界
references/              研究依据、文档和接入说明
```

稳定项目事实留在项目代码、测试、配置与文档；临时接续只记录下一步需要的信息。经验必须有条件与依据，不每次写流水账，不把一次失败写成全局禁令。

## 修改和检查本包

改路由登记只改 routing.json；改具体方法则改对应子技能。然后在本包根目录运行：

```sh
python scripts/catalog.py
python scripts/catalog.py --check
python -m unittest discover -s tests -v
```

测试包含 52 条路由固定案例，以及接续优先、即时能力范围、失速解除、导出排除仓库元数据、输入约束与引用一致性检查。它们是分派程序的测试，不是真实编码 Agent 对照实验。普通项目开发不需要运行本包测试。

生成单入口目录：

```sh
python scripts/export_single.py --output ../single-entry/invariant-first
```

目标目录必须不存在。导出保留全部规则与路由功能，改变子入口文件名和对应引用；同时排除版本库元数据与 Python 缓存，保留 `.gitignore` 等项目文件。导出物不作为第二套手工编辑源。这不是对任意源码树进行秘密扫描或清理的工具。

## 依据与效果边界

[路由设计](references/routing-design.md)说明本包如何借鉴你指定的 reverse-skill；[AI 编码痛点](references/ai-coding-pain-points.md)把调查与论文发现映射到纠偏动作；[名仓库依据](references/source-lessons.md)与[文档写法](references/documentation.md)保留此前提炼。

路由器能使分派可复现，不能强制任意模型正确理解意图或完成开发。默认实现没有后台运行、跨模型切换或自行放宽权限。结构测试通过不等于已提升开发质量；真实模型评估设计见[evaluation](references/evaluation.md)。
