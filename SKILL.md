---
name: invariant-first
description: 构建优先的跨 harness 工程技能路由器。用于从零开发、开发者预览、功能迭代、架构与接手、代码审查、发布运行、修复、性能优化、重构迁移、产品转向、退役和文档。按当前交付目标选择 PRIMARY，按真实代码事实补充架构、契约、状态、依赖、交互、失速恢复或跨会话接手技能；需要时衔接下一条路线。直接完成授权工作，减少过度防御、虚构 API、补丁循环、半成品和假完成，不把全部方法论压进每次任务。
---

# Invariant First · 选对方法，做完，接得住

交付成果，不表演流程。保留用户硬约束、真实契约和必要安全；在边界内自己完成工程取舍。架构让修改有落点，文档让用户会用、下一轮 AI 会改。路由只是选择方法，不能成为开工审批。

## 执行入口

1. 读取一次 [RULES](RULES.md)，从当前目标和相关入口确定要交付什么。不要先全仓审计；实现请求直接推进实现，讨论、审查与文档不自动授权修改生产系统。
2. 按 [MASTER-ROUTING](MASTER-ROUTING.md) 选择唯一 PRIMARY，已知对应路径就直接读取。普通任务不必生成 JSON 或运行脚本；批量分派、宿主集成或排查路由时才使用 `scripts/route.py`。小到确定的局部修正，不加载无关模块。
3. **读完当前需要的模块，立即执行 PRIMARY 的 ACTION。** SUPPORT 只解决当前难点，不另开工程。需要接续时先用 handoff 恢复事实；已经失速时用 recovery 获得新信息，再继续原目标。脚本的 LOAD_NOW 是本轮阅读集合，不是照着执行的流水线；DEFERRED 在触及对应边界前加载。
4. PRIMARY 控制交付物和行动范围：给 review 加架构专项仍然是审查，给 document 加状态专项仍然是写文档。工具不支持或环境受阻时才读 [runtime](references/runtime.md)，不假定专属命令、shell、子代理或记忆存在。
5. 完成当前授权目标后交付。仅当用户已请求后续工作才进入 NEXT；不要以“已路由”“已检查”替代实现，也不为普通任务创建路由报告、阶段数据库或多 Agent 编排。

## 需要可重复分派时

在 Skill 根目录执行；只使用已提供的 Python 3.10+，不为路由安装运行时：

```sh
python scripts/route.py --task "修复重复写入问题" --intent fix --facts shared_state,external_effects,external_consumers
python scripts/route.py --request examples/route-request.json
```

`--intent` 是根据用户目标作出的语义判断；不指定时只产生关键词候选，不是完整的自然语言理解。候选不合适就采用正确 PRIMARY，不为纠正一次分类反复运行脚本，也不让用户替你选菜单。

事实只描述**本次改动和当前阻塞**，不是整个仓库拥有的所有技术。仓库里有数据库，不代表改一段帮助文字也要加载持久化专项。接续已完成、阻塞已解除时撤下临时 SUPPORT，不继续沿用过期事实。

PRIMARY 决定目标；SUPPORT 分两类：handoff/recovery 是 prelude，只恢复上下文或进展，不占领域专项预算；状态、契约、依赖、架构和交互属于 domain，按当前边界最多先加载配置数量，其余延后到真正触及时。CAPABILITIES 的 preferred/missing 只覆盖 PRIMARY 与 LOAD_NOW，deferred 单列后续才可能用到的能力。能力是可用手段，不是任务前置门槛，更不是操作授权。

## 目标不被方法抢走

- “修 bug，必要时重构”仍是 fix；“保持行为替换实现”是 evolve；“写事故手册”是 document；“审查迁移”是 review，不执行迁移。
- 主目标未变就继续实现。只有新的具体困难才补方法，不反复分诊、重做计划或重开架构项目。
- 新情况按 [共同判断](RULES.md) 的因果关系处理：相同责任迁移方法，实际条件不同则调整动作，不因故事相似照抄答案。知识需要保留时见 [experience](experience/README.md)。

## 一个配置源，按需读取

[routing.json](config/routing.json) 是路由唯一事实源；[MASTER-ROUTING](MASTER-ROUTING.md) 与 [INDEX](INDEX.md) 从它生成。子技能负责 ACTION 与完成条件。覆盖整个生命周期不等于每次读完整个目录。

安装见 [portability](references/portability.md)；机制见 [routing-design](references/routing-design.md)；依据见 [机制归纳](references/ai-coding-pain-points.md)、[source-lessons](references/source-lessons.md) 与 [documentation](references/documentation.md)。维护本包才读 [AGENTS](AGENTS.md) 和 [evaluation](references/evaluation.md)，它们不是普通开发的前置步骤。

这不是安全沙箱或模型参数修改。宿主负责权限与执行；单入口导出仍需读取相对资源，不具备读取能力的宿主必须预展开适用指令，不能冒充自动按需加载。