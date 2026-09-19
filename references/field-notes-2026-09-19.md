# 社区反馈与成熟实现：编辑意图、行为契约与有效配置

最近核查：2026-09-20。此文件供维护本技能包时按需读取，不加入日常任务的默认上下文。先读原始论坛反馈，再对照下面的历史版本；只抽取能改变行动的方法。项目是协作成果，不把全部源码归于创始人，也不宣称读过整个仓库。

## 社区线索与可信度

| 编号 | 原始帖子 | 实际观察与限制 |
| --- | --- | --- |
| F1 | [Cursor：移动文件变成重新生成](https://forum.cursor.com/t/agent-and-model-consistently-misunderstand-concept-of-moving-code-files/131207)，2025-08-20 | 发帖者在 Cursor 1.4.5 中报告：要求移动已验证代码，Agent 却生成不同内容并删除原件；纠正后仍坚持新文件。这是单个用户的反馈，不能据此判断当前版本或所有模型。 |
| F2 | [V2EX：重构把整数金额改回浮点](https://www.v2ex.com/t/1211151)，页面标记 May 8 | 发帖者称结算重构删除整数转换并重新引入舍入误差。帖子位于推广节点并宣传自有工具，未提供可复现仓库；只作为语义丢失的风险线索，不采纳其普遍化结论或工具推荐。 |
| F3 | [V2EX：CSV 新功能遗漏已有规则](https://www.v2ex.com/t/1219159)，页面标记 Jun 9 | 发帖者要求按勾选顺序导出、缺失留空、保留权限与审计；报告实际结果排序改变且遗漏保护。未独立复现；帖子附带的重流程提示并非本包采用的方法。 |
| F4 | [Claude Code issue 65961：冗长注释](https://github.com/anthropics/claude-code/issues/65961)，2026-06-07 | 用户报告重复、显然及引用聊天的注释，要求停止仍会出现。示例里也有可能承载真实语义的说明，因此不接受“所有长注释都应删除”的推论。 |
| F5 | [Hacker News：Don't paste the AI, please](https://news.ycombinator.com/item?id=49371857) | 部分评论反对把未编辑的模型输出交给他人承担阅读成本；也有评论认为应按内容价值而非作者身份判断。提炼信息责任，不限制作者身份。 |
| F6 | [Claude Code #51265](https://github.com/anthropics/claude-code/issues/51265) 与其重复问题 [#47056](https://github.com/anthropics/claude-code/issues/47056)，2026-04 | 用户给出步骤说明 `CLAUDE_CONFIG_DIR` 指向自定义目录、部分 CLI 设置已经从那里生效，但 Agent 查找或上下文加载仍触及 `~/.claude`。两个 issue 的关闭或 stale 状态都不能证明当前行为已修复；这里只作为“声明的配置位置与实际消费者可能不是同一层”的线索。 |
| F7 | [Claude Code #79527：`--agents` 无效 JSON 静默通过](https://github.com/anthropics/claude-code/issues/79527)，2026-07-20 | 报告称错误的 `--agents` JSON 仍以退出码 0 启动，定制 Agent 没有定义，而相邻 `--settings` / `--mcp-config` 会失败；issue 标记为维护方已复现。它支持“进程成功不等于目标配置已生效”，不能外推为所有配置入口都 fail-open。 |
| F8 | [Cursor：`.cursorrules` 是否被忽略](https://forum.cursor.com/t/cursorrules-file-silently-ignored-in-agent-mode-with-no-warning/152046)，2026-02-16 起 | 最初 0/9 对 9/9 的报告随后被作者纠正：工作区里已有 `.mdc` 规则会覆盖冲突项，版本号也曾报错；进一步又发现特定目录结构差异，而 3 月在当前构建上复测成功。这个反例比最初结论更有价值：先确认覆盖顺序、工作区识别和实际版本，再判断“配置被忽略”，不要从一次表面失效固化根因。 |

这些是不同社区的原始讨论，不是代表性抽样、发生率统计或因果证据；未把热度当可靠性，也没有复现发帖者的私有项目。

## 对照实现及落点

### E1 · Git：结构移动操作原件

[Git v2.46.0 的 builtin/mv.c](https://github.com/git/git/blob/v2.46.0/builtin/mv.c) 在普通移动路径调用 `rename(src, dst)`，再更新索引；另有子模块和稀疏检出处理。关注的机制是移动现有内容，不是生成替代代码。`git mv` 也不是额外的“历史保留魔法”。

**落实 F1：** `if-evolve` 将移动、重命名和提取与语义重写分开；原内容保持，只更新必要引用。无需强制安装专用重构工具，使用已有编辑能力即可。文本路由补充明确的文件/符号移动与重命名候选，显式目标仍优先。

### E2 · Go：表示方式承担语义

[Go go1.23.2 的 time.go](https://github.com/golang/go/blob/go1.23.2/src/time/time.go) 区分墙上时间与单调时钟信息；比较、求差和序列化并不对这些信息做相同处理。表面相近的表示因此不能任意互换。

**落实 F2：** `if-evolve` 先辨认单位、精度、顺序、身份、时间基准；`if-architecture` 优先把含义写进名称、类型和构造边界。Go 样本不是金额案例的复现，也不要求保护所有旧代码；它支持先理解表示的责任再简化。

### E3 · Django：沿已有入口继承真实责任

[Django 5.2 的 ModelAdmin.get_urls](https://github.com/django/django/blob/5.2/django/contrib/admin/options.py) 将视图交给 `admin_site.admin_view`；[AdminSite.admin_view](https://github.com/django/django/blob/5.2/django/contrib/admin/sites.py) 负责权限检查、按条件限制缓存和 CSRF 包装。它不是可以随意合并的空转发层。

**落实 F3：** `if-build` 先追一个实际同类入口，复用其适用的保护与业务路径，保留排序、缺失值等要求。审计、事务和取消传播是面向各项目的扩展判断，不声称这段 Django 包装统一实现了它们。

### E4 · Go：让目标逻辑接受真实反馈

[Go go1.23.2 的 httptest/example_test.go](https://github.com/golang/go/blob/go1.23.2/src/net/http/httptest/example_test.go) 中，`ExampleResponseRecorder` 调用真正的 handler，读取状态码、响应头和响应体；`ExampleServer` 演示本地服务器路径。

**落实：** `RULES` 与 `if-fix` 要求保留被改逻辑，通过最近真实边界检查结果；必要替身放到外部效果处。这是工程设计选择，不由帖子推导出 mock 一概有害，也不强制新建端到端基础设施。

<a id="e5"></a>
### E5 · Linux 与 Git：说明要服务未来读者

[Linux 6.12 编码风格第 8 节](https://docs.kernel.org/6.12/process/coding-style.html#commenting) 提醒避免过量、复述实现的注释，保留用途和必要解释。[Git v2.46.0 的 SubmittingPatches](https://github.com/git/git/blob/v2.46.0/Documentation/SubmittingPatches) 要求解释问题、理由和影响，并将补丁迭代说明与最终提交正文区别对待；真正有用的替代方案讨论仍可保留。

**落实 F4–F5：** 共同规则区分当前语义、最终差异和聊天经过；`if-document` 与文档方法使用“没有这次对话还需要吗”的判断。`if-release` 从实际交付内容形成说明。清理语言残留不等于删除合法非目标、真实回归用例、已发布迁移记录或审计历史。

<a id="e6"></a>
### E6 · Git 与 pip：分层配置要能追到实际解析结果

[Git v2.46.0 的 `builtin/config.c`](https://github.com/git/git/blob/v2.46.0/builtin/config.c) 为查询提供 `--show-origin` 与 `--show-scope`，并从每个键的 `key_value_info` 输出来源类型、文件和 worktree/local/global/system/command 等作用域。它没有假定“我改了某个常见配置文件，所以这个值一定胜出”，而是把配置来源作为可检查事实。

[pip 24.2 的 `configuration.py`](https://github.com/pypa/pip/blob/24.2/src/pip/_internal/configuration.py) 明确区分 GLOBAL、USER、SITE、ENV 与 ENV_VAR，并用固定覆盖顺序合成读取结果；[同版本配置命令](https://github.com/pypa/pip/blob/24.2/src/pip/_internal/commands/configuration.py) 的 `debug` 会列出环境变量、候选配置文件及各来源中的值。这里借鉴的是“知道值从哪一层来、哪一层能够覆盖”，不是要求每个小程序都暴露完整 provenance API。

本轮在隔离临时目录做了一个机制小试验：本机 Git 2.47.3 同时给 `demo.mode` 提供 local 与 command 值时，`--show-origin --show-scope --get-all` 显示两层，而普通 `--get` 取得 command 值；pip 25.1.1 同时看到 `PIP_CONFIG_FILE`、配置文件值和 `PIP_TIMEOUT` 环境变量时，`pip config debug` 能区分这些来源。版本与上述历史源码样本不同，因此这只确认当前本机工具仍有相应观测能力，不是上游完整行为测试，也不是模型效果评估。

[Simon Willison 的 Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/) 强调 Agent 能执行代码就应实际执行目标路径，并指出自动测试全绿仍可能漏掉服务器启动、界面或集成层的明显失败。这里沿用的是让证据到达真实消费边界；具体用 `python -c`、`curl` 或浏览器取决于系统，不把作者使用的工具变成统一流程。

**落实 F6–F8：** 当 PATH、虚拟环境、配置文件、环境变量、CLI 参数或工作区规则存在覆盖关系时，先确认实际消费者解析到的值、版本和胜出来源，再决定应改配置、启动方式还是代码。文件存在、变量已设置、参数被接受和进程退出 0 都只是中间事实；没有多层覆盖或消费歧义时，直接验证目标行为，不额外建设配置追踪平台。

## 边界

这些材料只用于强化已有判断与专项，不按帖子增加新技能或案例禁令。确定性测试检查分派、生成和导出一致性；工具机制试验只验证观测能力。上述行为方法是否改善真实模型，仍需按 [evaluation](evaluation.md) 的保留任务做独立对照。
