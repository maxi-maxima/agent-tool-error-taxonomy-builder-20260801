# Agent Tool Error Taxonomy Builder

AI coding agents fail in repetitive ways, but their raw logs are too noisy for teams to improve prompts, permissions, and retry policies. This CLI scans agent logs, classifies tool-call failures, and produces a repair-first taxonomy.

## Why now

Terminal agents, MCP servers, scheduled automations, and multi-agent coding workflows are all growing quickly. Teams need small local tools that turn messy traces into operational feedback without uploading logs to another service.

## Install and run

```bash
python -m agent_tool_error_taxonomy_builder_20260801.cli examples/agent.log
python -m agent_tool_error_taxonomy_builder_20260801.cli examples/agent.log --format json
python -m agent_tool_error_taxonomy_builder_20260801.cli examples/agent.log --format sarif > agent-errors.sarif
python -m unittest discover -s tests
```

The SARIF output maps every classified event to its source log and line number, so CI systems and GitHub Code Scanning can surface the taxonomy as annotations.

## Example

Input: `examples/agent.log`

Output excerpt:

```text
Total events: 4
- auth: 1
- network: 1
- rate_limit: 1
- schema: 1
```

## Roadmap

- Custom rule packs per agent framework
- Trend comparison across multiple runs
