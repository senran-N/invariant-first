# MASTER-ROUTING

Generated from `config/routing.json`; edit the manifest, not this table.

## PRIMARY

Choose the current deliverable, not every keyword in a full specification. Explicit intent wins.
For text candidates: highest matching rule weight wins; ties use the listed priority.
A text candidate always needs an intent check. No route grants permission to act.

| Priority | ID | Deliverable / intent | Open now | First action |
| --- | --- | --- | --- | --- |
| 1 | review | 交付审查发现；只读请求不等于修复授权 | [设计与代码审查](skills/if-review/SKILL.md) | 对照目标读变更与直接协作者，找有具体后果的问题。 |
| 2 | document | 文档、教程、说明或参考是主要交付物 | [用户、接口与维护文档](skills/if-document/SKILL.md) | 按读者任务写可直接用的正文与真实示例。 |
| 3 | operate | 恢复正在受影响的使用，或完成运行改进 | [运行能力与故障恢复](skills/if-operate/SKILL.md) | 确认用户侧影响，执行最直接的已授权恢复或运行改进。 |
| 4 | retire | 结束已存在的能力、支持或服务 | [弃用、移除与退役](skills/if-retire/SKILL.md) | 处理真实消费者与数据，移除已无责任的入口和资源。 |
| 5 | optimize | 改善明确负载的延迟、吞吐、内存或成本 | [性能与成本优化](skills/if-optimize/SKILL.md) | 看目标负载与真实瓶颈，先消掉不必要的工作。 |
| 6 | fix | 改变已观察到的错误行为 | [缺陷与根因修复](skills/if-fix/SKILL.md) | 追到最早失真的事实或状态转移，完成最小完整修复。 |
| 7 | evolve | 移动、重命名或替换结构、依赖与方向，完成范围内切换 | [重构、迁移与转向](skills/if-evolve/SKILL.md) | 先区分结构编辑与语义变化，改完必要引用和调用。 |
| 8 | release | 生成发布产物、准备交付或执行已授权发布 | [打包与交付发布](skills/if-release/SKILL.md) | 用仓库真实流程构建分发产物，检查产物使用路径。 |
| 9 | frame | 用户要方向、设计、解释或接手判断，而非立刻实现 | [定向、架构与接手](skills/if-frame/SKILL.md) | 找真实入口与核心表示，做出一个能推进任务的取舍。 |
| 10 | build | 实现新的可用能力或补完现有功能 | [预览与功能开发](skills/if-build/SKILL.md) | 先实现核心难点，再接通真实入口、处理与输出。 |

No useful text match: provisional `build`; resolve from the user's goal, not guesswork.
Use explicit `--intent` or the equivalent semantic choice; do not ask the user to choose a routing menu.

## SUPPORT

Load only for confirmed, current-task facts. Text hints are suggestions, not facts.
Prelude specialists restore context or progress first and do not consume the domain-support budget.
Then load up to 2 confirmed domain specialists; remaining domain matches stay visible in DEFERRED.
Read LOAD_NOW before acting. Handoff/recovery restore the current PRIMARY, not a new project.
Load a deferred specialist before working on its boundary; deferred does not mean waived.

| Phase | ID | Confirmed facts | Open when needed | Action |
| --- | --- | --- | --- | --- |
| prelude | handoff | 需要恢复上下文或接续长任务 | [跨会话恢复与接手](skills/if-handoff/SKILL.md) | 从仓库恢复当前事实，只保留下一动作需要的接续信息。 |
| prelude | recovery | 尝试已重复且没有新信息; 工具、依赖或执行环境阻塞 | [打破无效循环](skills/if-recovery/SKILL.md) | 按原操作状态区分等待、取结果与安全重试，恢复后继续目标。 |
| domain | state | 涉及需要保留或迁移的持久数据; 存在共享可变状态或并发更新; 涉及外部写入或不可重复副作用; 触及外部不可信输入; 改变身份、权限或秘密处理 | [安全、状态与并发边界](skills/if-state/SKILL.md) | 明确保证建立的位置、原子转移和部分失败语义。 |
| domain | contracts | 本次改变影响已依赖的外部行为; 涉及需要保留或迁移的持久数据 | [真实兼容与迁移契约](skills/if-contracts/SKILL.md) | 保护受影响的真实承诺，在边界完成必要兼容。 |
| domain | dependencies | 新增、升级或替换依赖; 依赖某个尚未核实的 API 或版本行为 | [依赖与 API 事实](skills/if-dependencies/SKILL.md) | 核对已装版本的真实接口与来源，不根据名字猜包。 |
| domain | architecture | 需要调整职责、表示或依赖边界 | [表示、边界与修改落点](skills/if-architecture/SKILL.md) | 决定事实来源和修改责任，缩小需要同时理解的范围。 |
| domain | interface | 改变用户界面的实际交互 | [真实交互而非界面空壳](skills/if-interface/SKILL.md) | 连通用户动作、真实状态、反馈与输出，不交付静态按钮。 |

## STAGE

Stage adjusts obligations; it is not another pipeline.

- **preview**: 无真实旧依赖时直接定接口；做完整核心，不造兼容平台。
- **adopted**: 保护本次触及的真实外部契约；内部可以直接简化。
- **unknown**: 沿实际调用和数据判断边界，不为确认阶段启动全仓调查。

## NEXT / CAPABILITIES

NEXT is only the remaining user-requested sequence. It is never inferred as an authorization.
CAPABILITIES.preferred/missing covers PRIMARY + LOAD_NOW only; deferred lists later-only domain capabilities.
Capabilities describe useful tools, not compulsory workflow or permission to use them.
Missing capabilities use [runtime](references/runtime.md); no auto-installation or model switching.
Selection, instruction loading, implementation and observed execution remain separate facts.
