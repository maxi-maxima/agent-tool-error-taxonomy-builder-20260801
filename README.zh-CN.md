# Agent Tool Error Taxonomy Builder

AI 编码 Agent 的失败常常重复出现，但原始日志太吵，团队很难据此改进提示词、权限和重试策略。这个 CLI 会扫描 Agent 日志，归类工具调用失败，并输出面向修复的错误分类报告。

## 为什么现在值得做

终端 Agent、MCP 服务、定时自动化、多 Agent 协作都在升温。团队需要本地优先的小工具，把混乱 trace 转成可执行的运维反馈，而不是把日志上传到第三方服务。

## 安装与运行

```bash
python -m agent_tool_error_taxonomy_builder_20260801.cli examples/agent.log
python -m agent_tool_error_taxonomy_builder_20260801.cli examples/agent.log --format json
python -m agent_tool_error_taxonomy_builder_20260801.cli examples/agent.log --format sarif > agent-errors.sarif
python -m unittest discover -s tests
```

SARIF 输出会把每个已分类事件映射到原始日志文件和行号，便于 CI 系统和 GitHub Code Scanning 直接显示注解。

## 示例

输入：`examples/agent.log`

输出片段：

```text
Total events: 4
- auth: 1
- network: 1
- rate_limit: 1
- schema: 1
```

## 路线图

- 支持不同 Agent 框架的自定义规则包
- 对比多次运行的错误趋势
