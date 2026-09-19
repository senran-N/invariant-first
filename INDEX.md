# INDEX

Generated from `config/routing.json`. This is a map, not a reading checklist.

| Kind | ID | Module | Preferred capabilities |
| --- | --- | --- | --- |
| PRIMARY | frame | [定向、架构与接手](skills/if-frame/SKILL.md) | read, search |
| PRIMARY | build | [预览与功能开发](skills/if-build/SKILL.md) | read, search, edit, run |
| PRIMARY | review | [设计与代码审查](skills/if-review/SKILL.md) | read, search |
| PRIMARY | release | [打包与交付发布](skills/if-release/SKILL.md) | read, edit, run, artifact |
| PRIMARY | operate | [运行能力与故障恢复](skills/if-operate/SKILL.md) | read, run |
| PRIMARY | fix | [缺陷与根因修复](skills/if-fix/SKILL.md) | read, search, edit, run |
| PRIMARY | optimize | [性能与成本优化](skills/if-optimize/SKILL.md) | read, edit, run, measure |
| PRIMARY | evolve | [重构、迁移与转向](skills/if-evolve/SKILL.md) | read, search, edit, run |
| PRIMARY | retire | [弃用、移除与退役](skills/if-retire/SKILL.md) | read, search, edit |
| PRIMARY | document | [用户、接口与维护文档](skills/if-document/SKILL.md) | read, search, edit |
| SUPPORT | handoff | [跨会话恢复与接手](skills/if-handoff/SKILL.md) | read |
| SUPPORT | recovery | [打破无效循环](skills/if-recovery/SKILL.md) | read |
| SUPPORT | state | [安全、状态与并发边界](skills/if-state/SKILL.md) | read |
| SUPPORT | contracts | [真实兼容与迁移契约](skills/if-contracts/SKILL.md) | read |
| SUPPORT | dependencies | [依赖与 API 事实](skills/if-dependencies/SKILL.md) | read, search |
| SUPPORT | architecture | [表示、边界与修改落点](skills/if-architecture/SKILL.md) | read, search |
| SUPPORT | interface | [真实交互而非界面空壳](skills/if-interface/SKILL.md) | read, interact |

## Facts accepted by the router

- `external_consumers`: 本次改变影响已依赖的外部行为
- `persisted_data`: 涉及需要保留或迁移的持久数据
- `shared_state`: 存在共享可变状态或并发更新
- `external_effects`: 涉及外部写入或不可重复副作用
- `untrusted_input`: 触及外部不可信输入
- `auth_change`: 改变身份、权限或秘密处理
- `structure_change`: 需要调整职责、表示或依赖边界
- `dependency_change`: 新增、升级或替换依赖
- `unknown_api`: 依赖某个尚未核实的 API 或版本行为
- `ui_change`: 改变用户界面的实际交互
- `cross_session`: 需要恢复上下文或接续长任务
- `stalled`: 尝试已重复且没有新信息
- `environment_blocked`: 工具、依赖或执行环境阻塞

## Read on demand

- [Rules](RULES.md): shared action, architecture and delivery constraints.
- [Runtime adaptation](references/runtime.md): only when execution is blocked.
- [Experience](experience/README.md): scoped learning without global self-modification.
- [Pain-point research](references/ai-coding-pain-points.md): provenance, not runtime overhead.
- [Source lessons](references/source-lessons.md): inherited repository lessons.
