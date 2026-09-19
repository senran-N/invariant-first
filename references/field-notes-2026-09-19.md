# 社区反馈与成熟实现：编辑意图和行为契约

核查日期：2026-09-19。此文件供维护本技能包时按需读取，不加入日常任务的默认上下文。先读原始论坛反馈，再对照下面的历史版本；只抽取能改变行动的方法。项目是协作成果，不把全部源码归于创始人，也不宣称读过整个仓库。

## 社区线索与可信度

| 编号 | 原始帖子 | 实际观察与限制 |
| --- | --- | --- |
| F1 | [Cursor：移动文件变成重新生成](https://forum.cursor.com/t/agent-and-model-consistently-misunderstand-concept-of-moving-code-files/131207)，2025-08-20 | 发帖者在 Cursor 1.4.5 中报告：要求移动已验证代码，Agent 却生成不同内容并删除原件；纠正后仍坚持新文件。这是单个用户的反馈，不能据此判断当前版本或所有模型。 |
| F2 | [V2EX：重构把整数金额改回浮点](https://www.v2ex.com/t/1211151)，页面标记 May 8 | 发帖者称结算重构删除整数转换并重新引入舍入误差。帖子位于推广节点并宣传自有工具，未提供可复现仓库；只作为语义丢失的风险线索，不采纳其普遍化结论或工具推荐。 |
| F3 | [V2EX：CSV 新功能遗漏已有规则](https://www.v2ex.com/t/1219159)，页面标记 Jun 9 | 发帖者要求按勾选顺序导出、缺失留空、保留权限与审计；报告实际结果排序改变且遗漏保护。未独立复现；帖子附带的重流程提示并非本包采用的方法。 |
| F4 | [Claude Code issue 65961：冗长注释](https://github.com/anthropics/claude-code/issues/65961)，2026-06-07 | 用户报告重复、显然及引用聊天的注释，要求停止仍会出现。示例里也有可能承载真实语义的说明，因此不接受“所有长注释都应删除”的推论。 |
| F5 | [Hacker News：Don't paste the AI, please](https://news.ycombinator.com/item?id=49371857) | 部分评论反对把未编辑的模型输出交给他人承担阅读成本；也有评论认为应按内容价值而非作者身份判断。提炼信息责任，不限制作者身份。 |

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

## 边界

本轮修改的是已有技能的行动规则，以及机械编辑的候选路由；不添加新的审核阶段或专项。确定性测试只检查分派、生成和导出一致性；上述行为方法是否改善真实模型，需要按 [evaluation](evaluation.md) 的同任务对照另行衡量。
