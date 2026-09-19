---
name: invariant-first
description: 构建优先的跨 harness 工程技能路由器。用于从零开发、开发者预览、功能迭代、架构与接手、代码审查、发布运行、修复、性能优化、重构迁移、产品转向、退役和文档。按当前交付目标选择 PRIMARY，按真实代码事实补充架构、契约、状态、依赖、交互、失速恢复或跨会话接手技能；需要时衔接下一条路线。直接完成授权工作，减少过度防御、虚构 API、补丁循环、半成品和假完成，不把全部方法论压进每次任务。
---

# Invariant First

选对方法，完成授权目标。共同判断只读一次，具体方法按需读取。

## 执行

1. 读取 [共同判断](RULES.md)，根据当前交付目标选一条 PRIMARY。语义选择由你判断，文件位置从下表取得，不从任务名生成路径。
2. 按表中原样链接打开对应文件。本页链接相对于当前已加载的根 `SKILL.md`，不是项目工作目录；子文档中的链接相对于该文档。宿主提供资源读取能力时使用它，不把资源引用当作已确认的 shell 路径。
3. 只为本次确认的难点补充 SUPPORT。PRELUDE 恢复事实与进展，DOMAIN 处理实际边界；它们不改变 PRIMARY 的交付物和权限。触发条件不明时查 [分流表](MASTER-ROUTING.md)。
4. 读到所需方法就执行 ACTION，完成当前目标。只继续用户已请求的后续工作；不把分类、加载或检查本身当交付。

路径读取失败时，核对本次安装的 [routing.json](config/routing.json) 与资源根位置。只使用登记的 `path`；登记文件确实缺失则指出安装缺口，不新建占位方法或假称已加载。可用已读的方法继续不受阻部分。

## 方法地图

<!-- BEGIN ROUTE MAP -->
Generated from `config/routing.json`.

| Role | ID | Method |
| --- | --- | --- |
| PRIMARY | frame | [定向、架构与接手](skills/if-frame/SKILL.md) |
| PRIMARY | build | [预览与功能开发](skills/if-build/SKILL.md) |
| PRIMARY | review | [设计与代码审查](skills/if-review/SKILL.md) |
| PRIMARY | release | [打包与交付发布](skills/if-release/SKILL.md) |
| PRIMARY | operate | [运行能力与故障恢复](skills/if-operate/SKILL.md) |
| PRIMARY | fix | [缺陷与根因修复](skills/if-fix/SKILL.md) |
| PRIMARY | optimize | [性能与成本优化](skills/if-optimize/SKILL.md) |
| PRIMARY | evolve | [重构、迁移与转向](skills/if-evolve/SKILL.md) |
| PRIMARY | retire | [弃用、移除与退役](skills/if-retire/SKILL.md) |
| PRIMARY | document | [用户、接口与维护文档](skills/if-document/SKILL.md) |
| PRELUDE | handoff | [跨会话恢复与接手](skills/if-handoff/SKILL.md) |
| PRELUDE | recovery | [打破无效循环](skills/if-recovery/SKILL.md) |
| DOMAIN | state | [安全、状态与并发边界](skills/if-state/SKILL.md) |
| DOMAIN | contracts | [真实兼容与迁移契约](skills/if-contracts/SKILL.md) |
| DOMAIN | dependencies | [依赖与 API 事实](skills/if-dependencies/SKILL.md) |
| DOMAIN | architecture | [表示、边界与修改落点](skills/if-architecture/SKILL.md) |
| DOMAIN | interface | [真实交互而非界面空壳](skills/if-interface/SKILL.md) |
<!-- END ROUTE MAP -->

## 可选的机器分派

普通任务直接用上表。批量、集成或路由诊断时，在本包根目录使用已有 Python 3.10+：

```sh
python scripts/route.py --task "Implement the requested feature" --intent build
```

`intent` 是已作出的目标判断，文本匹配只是候选。`facts` 只描述当前任务；`LOAD_NOW` 是阅读集合，`DEFERRED` 在触及边界前读取，`NEXT` 只保留已请求的后续目标。能力提示不是必装工具或新授权。

## 按需读取

安装见 [portability](references/portability.md)；执行受阻见 [runtime](references/runtime.md)；知识归属见 [experience](experience/README.md)；文档写作见 [documentation](references/documentation.md)。

维护本包才读 [AGENTS](AGENTS.md)、[routing-design](references/routing-design.md)、[evaluation](references/evaluation.md) 与 [机制依据](references/ai-coding-pain-points.md)、[source-lessons](references/source-lessons.md)。路径登记只在 `config/routing.json` 维护，本页地图和两份目录视图由 `scripts/catalog.py` 生成。

宿主负责权限与资源读取；无文件读取能力时由宿主预展开适用指令。路由不是强制调度器。
