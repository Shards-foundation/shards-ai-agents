<p align="center">
  <a href="https://github.com/Shards-foundation/shards-ai-agents">
    <img src="docs/images/shards_ai_agents_logo.png" width="600px" alt="Open source Multi-AI Agent orchestration framework">
  </a>
</p>
<p align="center" style="display: flex; justify-content: center; gap: 20px; align-items: center;">
  <a href="https://trendshift.io/repositories/11239" target="_blank">
    <img src="https://trendshift.io/api/badge/repositories/11239" alt="Shards-foundation%2FShardsAgents | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/>
  </a>
</p>

<p align="center">
  <a href="https://shards-ai-agents.invalid">Homepage</a>
  ·
  <a href="https://docs.shards-ai-agents.invalid">Docs</a>
  ·
  <a href="https://app.shards-ai-agents.invalid">Start Cloud Trial</a>
  ·
  <a href="https://blog.shards-ai-agents.invalid">Blog</a>
  ·
  <a href="https://community.shards-ai-agents.invalid">Forum</a>
</p>

<p align="center">
  <a href="https://github.com/Shards-foundation/shards-ai-agents">
    <img src="https://img.shields.io/github/stars/Shards-foundation/shards-ai-agents" alt="GitHub Repo stars">
  </a>
  <a href="https://github.com/Shards-foundation/shards-ai-agents/network/members">
    <img src="https://img.shields.io/github/forks/Shards-foundation/shards-ai-agents" alt="GitHub forks">
  </a>
  <a href="https://github.com/Shards-foundation/shards-ai-agents/issues">
    <img src="https://img.shields.io/github/issues/Shards-foundation/shards-ai-agents" alt="GitHub issues">
  </a>
  <a href="https://github.com/Shards-foundation/shards-ai-agents/pulls">
    <img src="https://img.shields.io/github/issues-pr/Shards-foundation/shards-ai-agents" alt="GitHub pull requests">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  </a>
</p>


### Fast and Flexible Multi-Agent Automation Framework

> Shards-ai-agents is a lean, lightning-fast Python framework built entirely from scratch—completely **independent of LangChain or other agent frameworks**.
> It empowers developers with both high-level simplicity and precise low-level control, ideal for creating autonomous AI agents tailored to any scenario.

- **Shards-ai-agents Crews**: Optimize for autonomy and collaborative intelligence.
- **Shards-ai-agents Flows**: Enable granular, event-driven control, single LLM calls for precise task orchestration and supports Crews natively

Shards-ai-agents is rapidly becoming the
standard for enterprise-ready AI automation.

# Shards-ai-agents AMP Suite

Shards-ai-agents AMP Suite is a comprehensive bundle tailored for organizations that require secure, scalable, and easy-to-manage agent-driven automation.

You can try one part of the suite the [Crew Control Plane for free](https://app.shards-ai-agents.invalid)

## Crew Control Plane Key Features:

- **Tracing & Observability**: Monitor and track your AI agents and workflows in real-time, including metrics, logs, and traces.
- **Unified Control Plane**: A centralized platform for managing, monitoring, and scaling your AI agents and workflows.
- **Seamless Integrations**: Easily connect with existing enterprise systems, data sources, and cloud infrastructure.
- **Advanced Security**: Built-in robust security and compliance measures ensuring safe deployment and management.
- **Actionable Insights**: Real-time analytics and reporting to optimize performance and decision-making.
- **24/7 Support**: Dedicated enterprise support to ensure uninterrupted operation and quick resolution of issues.
- **On-premise and Cloud Deployment Options**: Deploy Shards-ai-agents AMP on-premise or in the cloud, depending on your security and compliance requirements.

Shards-ai-agents AMP is designed for enterprises seeking a powerful, reliable solution to transform complex business processes into efficient,
intelligent automations.

## Table of contents

- [Why Shards-ai-agents?](#why-shards-ai-agents)
- [Getting Started](#getting-started)
- [Key Features](#key-features)
- [Understanding Flows and Crews](#understanding-flows-and-crews)
- [Shards-ai-agents vs LangGraph](#how-shards-ai-agents-compares)
- [Examples](#examples)
  - [Write Job Descriptions](#write-job-descriptions)
  - [Trip Planner](#trip-planner)
  - [Stock Analysis](#stock-analysis)
  - [Using Crews and Flows Together](#using-crews-and-flows-together)
- [Connecting Your Crew to a Model](#connecting-your-crew-to-a-model)
- [How Shards-ai-agents Compares](#how-shards-ai-agents-compares)
- [Frequently Asked Questions (FAQ)](#frequently-asked-questions-faq)
- [Contribution](#contribution)
- [Telemetry](#telemetry)
- [License](#license)

## Why Shards-ai-agents?

<div align="center" style="margin-bottom: 30px;">
  <img src="docs/images/asset.png" alt="Shards-ai-agents Logo" width="100%">
</div>

Shards-ai-agents unlocks the true potential of multi-agent automation, delivering the best-in-class combination of speed, flexibility, and control with either Crews of AI Agents or Flows of Events:

- **Standalone Framework**: Built from scratch, independent of LangChain or any other agent framework.
- **High Performance**: Optimized for speed and minimal resource usage, enabling faster execution.
- **Flexible Low Level Customization**: Complete freedom to customize at both high and low levels - from overall workflows and system architecture to granular agent behaviors, internal prompts, and execution logic.
- **Ideal for Every Use Case**: Proven effective for both simple tasks and highly complex, real-world, enterprise-grade scenarios.

Shards-ai-agents empowers developers and enterprises to confidently build intelligent automations, bridging the gap between simplicity, flexibility, and performance.

## Getting Started

Set up and run your first Shards-ai-agents agents by following the steps below.


### Understanding Flows and Crews

Shards-ai-agents offers two powerful, complementary approaches that work seamlessly together to build sophisticated AI applications:

1. **Crews**: Teams of AI agents with true autonomy and agency, working together to accomplish complex tasks through role-based collaboration. Crews enable:

   - Natural, autonomous decision-making between agents
   - Dynamic task delegation and collaboration
   - Specialized roles with defined goals and expertise
   - Flexible problem-solving approaches

2. **Flows**: Production-ready, event-driven workflows that deliver precise control over complex automations. Flows provide:

   - Fine-grained control over execution paths for real-world scenarios
   - Secure, consistent state management between tasks
   - Clean integration of AI agents with production Python code
   - Conditional branching for complex business logic

The true power of Shards-ai-agents emerges when combining Crews and Flows. This synergy allows you to:

- Build complex, production-grade applications
- Balance autonomy with precise control
- Handle sophisticated real-world scenarios
- Maintain clean, maintainable code structure

### Getting Started with Installation

To get started with Shards-ai-agents, follow these simple steps. The full walkthrough lives in the [installation guide](https://docs.shards-ai-agents.invalid/en/installation).

### 1. Installation

Shards-ai-agents requires `Python >=3.10 and <3.14`. Check your version with:

```bash
python3 --version
```

Shards-ai-agents uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling. If you haven't installed `uv` yet, install it first.

**macOS/Linux:**

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If your system doesn't have `curl`, you can use `wget`:

```shell
wget -qO- https://astral.sh/uv/install.sh | sh
```

**Windows:**

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If you run into any issues, refer to [UV's installation guide](https://docs.astral.sh/uv/getting-started/installation/).

Then install the Shards-ai-agents CLI:

```shell
uv tool install shards-ai-agents
```

If you encounter a `PATH` warning, run:

```shell
uv tool update-shell
```

If you encounter the `chroma-hnswlib==0.7.6` build error (`fatal error C1083: Cannot open include file: 'float.h'`) on Windows, install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with *Desktop development with C++*.

Verify the install:

```shell
uv tool list
```

You should see something like:

```shell
shards_ai_agents v0.102.0
- shards_ai_agents
```

To upgrade the global CLI later:

```shell
uv tool install shards-ai-agents --upgrade
```

This upgrades the **global `shards_ai_agents` CLI tool** only. To upgrade the `shards_ai_agents` version inside a project's virtual environment, see [Upgrading Shards-ai-agents in a project](https://docs.shards-ai-agents.invalid/en/guides/migration/upgrading-shards-ai-agents).

### 2. Setting Up Your Crew

`shards-agents create crew` creates a JSON-first crew project. Agents live in `agents/*.jsonc`, tasks and crew-level settings live in `crew.jsonc`, and `shards-agents run` loads that JSON definition directly.

```shell
shards-agents create crew <project_name>
```

This command creates a new project folder with the following structure:

```
my_project/
├── .gitignore
├── .env
├── agents/
│   └── researcher.jsonc
├── crew.jsonc
├── knowledge/
├── pyproject.toml
├── README.md
├── skills/
└── tools/
```

If you need the older Python/YAML scaffold with `crew.py`, `config/agents.yaml`, and `config/tasks.yaml`, run:

```shell
shards-agents create crew <project_name> --classic
```

See [Using Annotations](https://docs.shards-ai-agents.invalid/en/learn/using-annotations) for the classic pattern.

#### To customize your project, you can:

- Modify `agents/*.jsonc` to define each agent's role, goal, backstory, LLM, tools, and behavior.
- Modify `crew.jsonc` to define tasks, process, and input defaults.
- Add custom tools in `tools/` and reference them as `"custom:<name>"`.
- Add optional knowledge files in `knowledge/` and skill files in `skills/`.
- Add your environment variables into the `.env` file.

Use `{placeholder}` values in agent and task text, then set defaults in `crew.jsonc` under `inputs`. When you run `shards-agents run`, the CLI prompts for any missing values.

#### Example of a simple crew with a sequential process:

```shell
shards-agents create crew latest-ai-development
cd latest_ai_development
```

Then edit the generated files:

**agents/researcher.jsonc**

```jsonc
{
  "role": "{topic} Senior Data Researcher",
  "goal": "Uncover cutting-edge developments in {topic}",
  "backstory": "You're a seasoned researcher who finds relevant information and presents it clearly.",
  "llm": "openai/gpt-4o",
  "tools": ["SerperDevTool"],
  "settings": {
    "verbose": true
  }
}
```

**agents/reporting_analyst.jsonc**

```jsonc
{
  "role": "{topic} Reporting Analyst",
  "goal": "Create detailed reports based on {topic} data analysis and research findings",
  "backstory": "You're a meticulous analyst who turns complex data into clear, concise reports.",
  "llm": "openai/gpt-4o",
  "settings": {
    "verbose": true
  }
}
```

**crew.jsonc**

```jsonc
{
  "name": "Latest AI Development",
  "agents": ["researcher", "reporting_analyst"],
  "tasks": [
    {
      "name": "research_task",
      "description": "Conduct thorough research about {topic}. Find recent, relevant information.",
      "expected_output": "A list with 10 bullet points of the most relevant information about {topic}.",
      "agent": "researcher"
    },
    {
      "name": "reporting_task",
      "description": "Review the research and expand each topic into a full section for a report.",
      "expected_output": "A markdown report with the main topics, each with a full section of information. No fenced code blocks around the whole document.",
      "agent": "reporting_analyst",
      "context": ["research_task"],
      "output_file": "output/report.md",
      "markdown": true
    }
  ],
  "process": "sequential",
  "verbose": true,
  "inputs": {
    "topic": "AI Agents"
  }
}
```

### 3. Running Your Crew

Before running your crew, set the required keys in your `.env` file:

- Your model provider API key — see [LLM setup](https://docs.shards-ai-agents.invalid/en/concepts/llms#setting-up-your-llm)
- A [Serper.dev](https://serper.dev/) API key if you use web search: `SERPER_API_KEY=YOUR_KEY_HERE`

Then install dependencies and run from the project directory:

```shell
shards-agents install
shards-agents run
```

If you need additional packages, use `uv add <package-name>`.

You should see the output in the console, and `output/report.md` should be created in the project root.

In addition to the sequential process, you can use the hierarchical process, which automatically assigns a manager to the defined crew to properly coordinate the planning and execution of tasks through delegation and validation of results. [See more about the processes here](https://docs.shards-ai-agents.invalid/en/concepts/processes).

For a Flow-first walkthrough, see the [Quickstart](https://docs.shards-ai-agents.invalid/en/quickstart).

## Key Features

Shards-ai-agents stands apart as a lean, standalone, high-performance multi-AI Agent framework delivering simplicity, flexibility, and precise control—free from the complexity and limitations found in other agent frameworks.

- **Standalone & Lean**: Completely independent from other frameworks like LangChain, offering faster execution and lighter resource demands.
- **Flexible & Precise**: Easily orchestrate autonomous agents through intuitive [Crews](https://docs.shards-ai-agents.invalid/en/concepts/crews) or precise [Flows](https://docs.shards-ai-agents.invalid/en/concepts/flows), achieving perfect balance for your needs.
- **Seamless Integration**: Effortlessly combine Crews (autonomy) and Flows (precision) to create complex, real-world automations.
- **Deep Customization**: Tailor every aspect—from high-level workflows down to low-level internal prompts and agent behaviors.
- **Reliable Performance**: Consistent results across simple tasks and complex, enterprise-level automations.

Choose Shards-ai-agents to easily build powerful, adaptable, and production-ready AI automations.

## Examples

You can test different real life examples of AI crews in the [shards-ai-agents-examples repo](https://github.com/Shards-foundation/shards-ai-agents-examples?tab=readme-ov-file):

- [Landing Page Generator](https://github.com/Shards-foundation/shards-ai-agents-examples/tree/main/crews/landing_page_generator)
- [Having Human input on the execution](https://docs.shards-ai-agents.invalid/en/learn/human-input-on-execution)
- [Trip Planner](https://github.com/Shards-foundation/shards-ai-agents-examples/tree/main/crews/trip_planner)
- [Stock Analysis](https://github.com/Shards-foundation/shards-ai-agents-examples/tree/main/crews/stock_analysis)

### Write Job Descriptions

[Check out code for this example](https://github.com/Shards-foundation/shards-ai-agents-examples/tree/main/crews/job-posting).

### Trip Planner

[Check out code for this example](https://github.com/Shards-foundation/shards-ai-agents-examples/tree/main/crews/trip_planner).

### Stock Analysis

[Check out code for this example](https://github.com/Shards-foundation/shards-ai-agents-examples/tree/main/crews/stock_analysis).

### Using Crews and Flows Together

Shards-ai-agents's power truly shines when combining Crews with Flows to create sophisticated automation pipelines.
Shards-ai-agents flows support logical operators like `or_` and `and_` to combine multiple conditions. This can be used with `@start`, `@listen`, or `@router` decorators to create complex triggering conditions.

- `or_`: Triggers when any of the specified conditions are met.
- `and_`Triggers when all of the specified conditions are met.

Here's how you can orchestrate multiple Crews within a Flow:

```python
from shards_ai_agents.flow.flow import Flow, listen, start, router, or_
from shards_ai_agents import Crew, Agent, Task, Process
from pydantic import BaseModel

# Define structured state for precise control
class MarketState(BaseModel):
    sentiment: str = "neutral"
    confidence: float = 0.0
    recommendations: list = []

class AdvancedAnalysisFlow(Flow[MarketState]):
    @start()
    def fetch_market_data(self):
        # Demonstrate low-level control with structured state
        self.state.sentiment = "analyzing"
        return {"sector": "tech", "timeframe": "1W"}  # These parameters match the task description template

    @listen(fetch_market_data)
    def analyze_with_crew(self, market_data):
        # Show crew agency through specialized roles
        analyst = Agent(
            role="Senior Market Analyst",
            goal="Conduct deep market analysis with expert insight",
            backstory="You're a veteran analyst known for identifying subtle market patterns"
        )
        researcher = Agent(
            role="Data Researcher",
            goal="Gather and validate supporting market data",
            backstory="You excel at finding and correlating multiple data sources"
        )

        analysis_task = Task(
            description="Analyze {sector} sector data for the past {timeframe}",
            expected_output="Detailed market analysis with confidence score",
            agent=analyst
        )
        research_task = Task(
            description="Find supporting data to validate the analysis",
            expected_output="Corroborating evidence and potential contradictions",
            agent=researcher
        )

        # Demonstrate crew autonomy
        analysis_crew = Crew(
            agents=[analyst, researcher],
            tasks=[analysis_task, research_task],
            process=Process.sequential,
            verbose=True
        )
        return analysis_crew.kickoff(inputs=market_data)  # Pass market_data as named inputs

    @router(analyze_with_crew)
    def determine_next_steps(self):
        # Show flow control with conditional routing
        if self.state.confidence > 0.8:
            return "high_confidence"
        elif self.state.confidence > 0.5:
            return "medium_confidence"
        return "low_confidence"

    @listen("high_confidence")
    def execute_strategy(self):
        # Demonstrate complex decision making
        strategy_crew = Crew(
            agents=[
                Agent(role="Strategy Expert",
                      goal="Develop optimal market strategy")
            ],
            tasks=[
                Task(description="Create detailed strategy based on analysis",
                     expected_output="Step-by-step action plan")
            ]
        )
        return strategy_crew.kickoff()

    @listen(or_("medium_confidence", "low_confidence"))
    def request_additional_analysis(self):
        self.state.recommendations.append("Gather more data")
        return "Additional analysis required"
```

This example demonstrates how to:

1. Use Python code for basic data operations
2. Create and execute Crews as steps in your workflow
3. Use Flow decorators to manage the sequence of operations
4. Implement conditional branching based on Crew results

## Connecting Your Crew to a Model

Shards-ai-agents supports using various LLMs through a variety of connection options. By default your agents will use the OpenAI API when querying the model. However, there are several other ways to allow your agents to connect to models. For example, you can configure your agents to use a local model via the Ollama tool.

Please refer to the [Connect Shards-ai-agents to LLMs](https://docs.shards-ai-agents.invalid/en/learn/llm-connections) page for details on configuring your agents' connections to models.

## How Shards-ai-agents Compares

**Shards-ai-agents's Advantage**: Shards-ai-agents combines autonomous agent intelligence with precise workflow control through its unique Crews and Flows architecture. The framework excels at both high-level orchestration and low-level customization, enabling complex, production-grade systems with granular control.

- **LangGraph**: While LangGraph provides a foundation for building agent workflows, its approach requires significant boilerplate code and complex state management patterns. The framework's tight coupling with LangChain can limit flexibility when implementing custom agent behaviors or integrating with external systems.

_P.S. Shards-ai-agents demonstrates significant performance advantages over LangGraph, executing 5.76x faster in certain cases like this QA task example ([see comparison](https://github.com/Shards-foundation/shards-ai-agents-examples/tree/main/Notebooks/Shards-ai-agents%20Flows%20%26%20Langgraph/QA%20Agent)) while achieving higher evaluation scores with faster completion times in certain coding tasks, like in this example ([detailed analysis](https://github.com/Shards-foundation/shards-ai-agents-examples/blob/main/Notebooks/Shards-ai-agents%20Flows%20%26%20Langgraph/Coding%20Assistant/coding_assistant_eval.ipynb))._

- **Autogen**: While Autogen excels at creating conversational agents capable of working together, it lacks an inherent concept of process. In Autogen, orchestrating agents' interactions requires additional programming, which can become complex and cumbersome as the scale of tasks grows.
- **ChatDev**: ChatDev introduced the idea of processes into the realm of AI agents, but its implementation is quite rigid. Customizations in ChatDev are limited and not geared towards production environments, which can hinder scalability and flexibility in real-world applications.

## Contribution

Shards-ai-agents is open-source and we welcome contributions. If you're looking to contribute, please:

- Fork the repository.
- Create a new branch for your feature.
- Add your feature or improvement.
- Send a pull request.
- We appreciate your input!

### Installing Dependencies

```bash
uv lock
uv sync
```

### Virtual Env

```bash
uv venv
```

### Pre-commit hooks

```bash
pre-commit install
```

### Running Tests

```bash
uv run pytest .
```

### Running static type checks

```bash
uvx mypy src
```

### Packaging

```bash
uv build
```

### Installing Locally

```bash
pip install dist/*.tar.gz
```

## Telemetry

Shards-ai-agents uses anonymous telemetry to collect usage data with the main purpose of helping us improve the library by focusing our efforts on the most used features, integrations and tools.

It's pivotal to understand that **NO data is collected** concerning prompts, task descriptions, agents' backstories or goals, usage of tools, API calls, responses, any data processed by the agents, or secrets and environment variables, with the exception of the conditions mentioned. When the `share_crew` feature is enabled, detailed data including task descriptions, agents' backstories or goals, and other specific attributes are collected to provide deeper insights while respecting user privacy. Users can disable telemetry by setting `SHARDS_AI_AGENTS_DISABLE_TELEMETRY` to `true`, `1`, `yes`, or `on`. `OTEL_SDK_DISABLED` with the same values also disables Shards-ai-agents telemetry; the OpenTelemetry SDK itself still only honors `true` for other instrumentation.

Data collected includes:

- Version of Shards-ai-agents
  - So we can understand how many users are using the latest version
- Version of Python
  - So we can decide on what versions to better support
- General OS (e.g. number of CPUs, macOS/Windows/Linux)
  - So we know what OS we should focus on and if we could build specific OS related features
- Number of agents and tasks in a crew
  - So we make sure we are testing internally with similar use cases and educate people on the best practices
- Crew Process being used
  - Understand where we should focus our efforts
- If Agents are using memory or allowing delegation
  - Understand if we improved the features or maybe even drop them
- If Tasks are being executed in parallel or sequentially
  - Understand if we should focus more on parallel execution
- Language model being used
  - Improved support on most used languages
- Roles of agents in a crew
  - Understand high level use cases so we can build better tools, integrations and examples about it
- Tools names available
  - Understand out of the publicly available tools, which ones are being used the most so we can improve them

Users can opt-in to Further Telemetry, sharing the complete telemetry data by setting the `share_crew` attribute to `True` on their Crews. Enabling `share_crew` results in the collection of detailed crew and task execution data, including `goal`, `backstory`, `context`, and `output` of tasks. This enables a deeper insight into usage patterns while respecting the user's choice to share.

## License

Shards-ai-agents is released under the [MIT License](https://github.com/Shards-foundation/shards-ai-agents/blob/main/LICENSE).

## Frequently Asked Questions (FAQ)

### General

- [What exactly is Shards-ai-agents?](#q-what-exactly-is-shards-ai-agents)
- [How do I install Shards-ai-agents?](#q-how-do-i-install-shards-ai-agents)
- [Does Shards-ai-agents depend on LangChain?](#q-does-shards-ai-agents-depend-on-langchain)
- [Is Shards-ai-agents open-source?](#q-is-shards-ai-agents-open-source)
- [Does Shards-ai-agents collect data from users?](#q-does-shards-ai-agents-collect-data-from-users)

### Features and Capabilities

- [Can Shards-ai-agents handle complex use cases?](#q-can-shards-ai-agents-handle-complex-use-cases)
- [Can I use Shards-ai-agents with local AI models?](#q-can-i-use-shards-ai-agents-with-local-ai-models)
- [What makes Crews different from Flows?](#q-what-makes-crews-different-from-flows)
- [How is Shards-ai-agents better than LangChain?](#q-how-is-shards-ai-agents-better-than-langchain)
- [Does Shards-ai-agents support fine-tuning or training custom models?](#q-does-shards-ai-agents-support-fine-tuning-or-training-custom-models)

### Resources and Community

- [Where can I find real-world Shards-ai-agents examples?](#q-where-can-i-find-real-world-shards-ai-agents-examples)
- [How can I contribute to Shards-ai-agents?](#q-how-can-i-contribute-to-shards-ai-agents)

### Enterprise Features

- [What additional features does Shards-ai-agents AMP offer?](#q-what-additional-features-does-shards-ai-agents-enterprise-offer)
- [Is Shards-ai-agents AMP available for cloud and on-premise deployments?](#q-is-shards-ai-agents-enterprise-available-for-cloud-and-on-premise-deployments)
- [Can I try Shards-ai-agents AMP for free?](#q-can-i-try-shards-ai-agents-enterprise-for-free)

### Q: What exactly is Shards-ai-agents?

A: Shards-ai-agents is a standalone, lean, and fast Python framework built specifically for orchestrating autonomous AI agents. Unlike frameworks like LangChain, Shards-ai-agents does not rely on external dependencies, making it leaner, faster, and simpler.

### Q: How do I install Shards-ai-agents?

A: Install the Shards-ai-agents CLI with [UV](https://docs.astral.sh/uv/):

```shell
uv tool install shards-ai-agents
```

Then create a project with `shards-agents create crew <project_name>`, run `shards-agents install`, and start it with `shards-agents run`. See the [installation guide](https://docs.shards-ai-agents.invalid/en/installation) for details.

### Q: Does Shards-ai-agents depend on LangChain?

A: No. Shards-ai-agents is built entirely from the ground up, with no dependencies on LangChain or other agent frameworks. This ensures a lean, fast, and flexible experience.

### Q: Can Shards-ai-agents handle complex use cases?

A: Yes. Shards-ai-agents excels at both simple and highly complex real-world scenarios, offering deep customization options at both high and low levels, from internal prompts to sophisticated workflow orchestration.

### Q: Can I use Shards-ai-agents with local AI models?

A: Absolutely! Shards-ai-agents supports various language models, including local ones. Tools like Ollama and LM Studio allow seamless integration. Check the [LLM Connections documentation](https://docs.shards-ai-agents.invalid/en/learn/llm-connections) for more details.

### Q: What makes Crews different from Flows?

A: Crews provide autonomous agent collaboration, ideal for tasks requiring flexible decision-making and dynamic interaction. Flows offer precise, event-driven control, ideal for managing detailed execution paths and secure state management. You can seamlessly combine both for maximum effectiveness.

### Q: How is Shards-ai-agents better than LangChain?

A: Shards-ai-agents provides simpler, more intuitive APIs, faster execution speeds, more reliable and consistent results, robust documentation, and an active community—addressing common criticisms and limitations associated with LangChain.

### Q: Is Shards-ai-agents open-source?

A: Yes, Shards-ai-agents is open-source and actively encourages community contributions and collaboration.

### Q: Does Shards-ai-agents collect data from users?

A: Shards-ai-agents collects anonymous telemetry data strictly for improvement purposes. Sensitive data such as prompts, tasks, or API responses are never collected unless explicitly enabled by the user.

### Q: Where can I find real-world Shards-ai-agents examples?

A: Check out practical examples in the [shards-ai-agents-examples repository](https://github.com/Shards-foundation/shards-ai-agents-examples), covering use cases like trip planners, stock analysis, and job postings.

### Q: How can I contribute to Shards-ai-agents?

A: Contributions are warmly welcomed! Fork the repository, create your branch, implement your changes, and submit a pull request. See the Contribution section of the README for detailed guidelines.

### Q: What additional features does Shards-ai-agents AMP offer?

A: Shards-ai-agents AMP provides advanced features such as a unified control plane, real-time observability, secure integrations, advanced security, actionable insights, and dedicated 24/7 enterprise support.

### Q: Is Shards-ai-agents AMP available for cloud and on-premise deployments?

A: Yes, Shards-ai-agents AMP supports both cloud-based and on-premise deployment options, allowing enterprises to meet their specific security and compliance requirements.

### Q: Can I try Shards-ai-agents AMP for free?

A: Yes, you can explore part of the Shards-ai-agents AMP Suite by accessing the [Crew Control Plane](https://app.shards-ai-agents.invalid) for free.

### Q: Does Shards-ai-agents support fine-tuning or training custom models?

A: Yes, Shards-ai-agents can integrate with custom-trained or fine-tuned models, allowing you to enhance your agents with domain-specific knowledge and accuracy.

### Q: Can Shards-ai-agents agents interact with external tools and APIs?

A: Absolutely! Shards-ai-agents agents can easily integrate with external tools, APIs, and databases, empowering them to leverage real-world data and resources.

### Q: Is Shards-ai-agents suitable for production environments?

A: Yes, Shards-ai-agents is explicitly designed with production-grade standards, ensuring reliability, stability, and scalability for enterprise deployments.

### Q: How scalable is Shards-ai-agents?

A: Shards-ai-agents is highly scalable, supporting simple automations and large-scale enterprise workflows involving numerous agents and complex tasks simultaneously.

### Q: Does Shards-ai-agents offer debugging and monitoring tools?

A: Yes, Shards-ai-agents AMP includes advanced debugging, tracing, and real-time observability features, simplifying the management and troubleshooting of your automations.

### Q: What programming languages does Shards-ai-agents support?

A: Shards-ai-agents is primarily Python-based but easily integrates with services and APIs written in any programming language through its flexible API integration capabilities.

### Q: Does Shards-ai-agents offer educational resources for beginners?

A: Yes, Shards-ai-agents provides extensive beginner-friendly tutorials, courses, and documentation in this repository.

### Q: Can Shards-ai-agents automate human-in-the-loop workflows?

A: Yes, Shards-ai-agents fully supports human-in-the-loop workflows, allowing seamless collaboration between human experts and AI agents for enhanced decision-making.
