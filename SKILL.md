---
name: invariant-first
description: 构建优先的跨 harness 工程技能路由器。用于从零开发、开发者预览、功能迭代、架构与接手、代码审查、发布运行、修复、性能优化、重构迁移、产品转向、退役和文档。按当前交付目标选择 PRIMARY，按真实代码事实补充架构、契约、状态、依赖、交互、失速恢复或跨会话接手技能；需要时衔接下一条路线。直接完成授权工作，减少过度防御、虚构 API、补丁循环、半成品和假完成，不把全部方法论压进每次任务。
---

# Invariant First · 选对方法，做完，接得住

交付成果，不表演流程。你是负责把工程决定落实到代码和文档的执行者，不是等待用户逐步批准的流程管理员。保留用户约束、事实、权限和必要安全；在边界内自己完成可逆取舍。

## 执行入口

1. 读取一次 [RULES](RULES.md)。从当前请求和相关入口确定**现在要交付什么**，不要先做全仓审计。实现请求默认推进实现；讨论、审查与文档不等于修改生产系统的授权。
2. 选择唯一 PRIMARY。能运行 Python 3.10+ 时使用 `scripts/route.py`；不能运行时读 [MASTER-ROUTING](MASTER-ROUTING.md) 中同源生成的分流表。确定的拼写或局部小改可直接选路并执行，不强制调用脚本。
3. **立即读取输出的 PRIMARY 文件并执行其中 ACTION。** 不以“已加载/已路由”结束。SUPPORT 是按事实命中的专项方法，不是另一个 Agent；先读 LOAD_NOW，只有涉及对应边界时再读 DEFERRED，不把待加载等同于可以忽略。
4. 使用当前环境实际存在的读、搜、改、运行和比较能力。遇到工具或环境阻塞才读 [runtime](references/runtime.md)；缺工具不等于缺能力，不能凭空编造命令或擅自安装工具。
5. 完成当前目标后交付。只有用户已请求的后续工作才进入 NEXT；路由本身不授予部署、删除或外部写入权限。普通任务不创建路由报告、阶段数据库或并行 Agent。

## 两种可互换的路由入口

在 Skill 根目录执行；命令中的路径随实际安装位置解析：

```sh
python scripts/route.py --task "修复重复写入问题" --intent fix --facts shared_state,external_effects,external_consumers
python scripts/route.py --request examples/route-request.json
```

`--intent` 是你根据用户目标作出的明确判断，脚本负责一致映射；不指定时只是关键词候选，**不是完整的自然语言理解器**。候选与真实目标冲突时按用户目标纠正并用显式 intent 重跑，不让用户替你选菜单。事实只填已经看见的条件，不能把猜想当真相。

PRIMARY 决定工作目标；SUPPORT 补充当前难点；CAPABILITIES 表示能力差额；NEXT 仅保存明确给出的后续序列。选择、加载与执行是三件事，不能用路由输出冒充代码已完成。

## 路由与衔接规则

- “修 bug，必要时重构”仍以 fix 为主；“保持行为替换实现”走 evolve；“写事故手册”走 document；“审查迁移”走 review，不执行迁移。
- 生命周期依据本次边界：无真实依赖的预览不造兼容；已有调用者或持久数据就承担契约。安全跟暴露面走，不等第二阶段。
- 一次只推进一个明确工作目标。主目标未变时不反复分诊；遇到已定位的新难点加载专项方法，不重新开一个设计项目。
- 连续尝试不再获得新信息时加载 recovery；新会话或任务必须接续时加载 handoff。恢复后回到原 PRIMARY，不把“研究怎么研究”当新任务。
- 真正复用的经验写入项目已有权威位置，遵循 [experience](experience/README.md)；不自动改全局 Skill、保存秘密或将一次猜想升级为通用规则。

## 实现与资料分层

路由唯一事实源是 [config/routing.json](config/routing.json)；[MASTER-ROUTING](MASTER-ROUTING.md) 与 [INDEX](INDEX.md) 从它生成。子技能负责 ACTION 和完成条件，不重复维护路由表。普通任务不要加载整个目录。

安装与单入口导入见 [portability](references/portability.md)；本次重构与 reverse-skill 的对应关系见 [routing-design](references/routing-design.md)；AI 编码痛点和依据见 [pain-points](references/ai-coding-pain-points.md)。原有名仓库与文档依据见 [source-lessons](references/source-lessons.md)、[documentation](references/documentation.md)。只有维护本包时才读 [evaluation](references/evaluation.md)。

这是可执行的分派器加任务指令，不是安全沙箱或模型参数修改。宿主仍负责权限与工具执行；没有文件读取能力时使用单入口导出或预展开所需指令，不能声称仍能自动按需加载。
