# AII Ecosystem Overview

> Related projects, standards, and how they connect

---

## The Landscape

```
┌─────────────────────────────────────────────────────────────────┐
│                        AII ECOSYSTEM                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PARADIGM LAYER (Why & What)                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                        AII                               │    │
│  │            Intent-driven interaction design              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│  ────────────────────────────┼───────────────────────────────   │
│                              │                                   │
│  PROTOCOL LAYER (How)        │                                   │
│  ┌─────────────┐    ┌────────┴───────┐    ┌─────────────┐       │
│  │    A2UI     │    │      MCP       │    │  AGENTS.md  │       │
│  │  Agent UI   │    │ Tool Protocol  │    │ AI Context  │       │
│  └─────────────┘    └────────────────┘    └─────────────┘       │
│                              │                                   │
│  ────────────────────────────┼───────────────────────────────   │
│                              │                                   │
│  INFRASTRUCTURE LAYER        │                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                        AAIF                              │    │
│  │            Agentic AI Foundation (Linux Foundation)      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## A2UI — Agent-to-User Interface

**What:** Google's open-source protocol for agent-generated UIs.

**Repository:** [github.com/google/A2UI](https://github.com/google/A2UI)

### How A2UI Implements AII Principles

| AII Principle | A2UI Implementation |
|---------------|---------------------|
| Adaptive Response | Agent selects components based on context |
| Human Oversight | Allowlist mechanism, client controls rendering |
| Transparency | Declarative format is auditable |
| Safety | Data-only, no executable code |

### Key Features

```
┌─────────────────────────────────────────────────────────┐
│                      A2UI                                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Security-first                                          │
│  • Allowlist of approved components                      │
│  • No code execution in UI definitions                   │
│  • Client controls what renders                          │
│                                                          │
│  LLM-friendly                                            │
│  • Flat component list with ID references                │
│  • Incremental updates supported                         │
│  • JSON format easy for models to generate               │
│                                                          │
│  Cross-platform                                          │
│  • Same JSON renders on Flutter, React, Angular, SwiftUI │
│  • Platform-appropriate native components                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Relationship to AII

```
AII (Paradigm)              A2UI (Protocol)
━━━━━━━━━━━━━━              ━━━━━━━━━━━━━━━
Why & What                  How (for visual)
Design principles           JSON format + renderers
Cross-modal                 Visual UI focus
```

A2UI is one implementation of AII's adaptive modality principle, specifically for visual interfaces. AII also encompasses voice, gesture, and other modalities.

---

## AAIF — Agentic AI Foundation

**What:** Linux Foundation project for collaborative agentic AI development.

**Website:** [aaif.io](https://aaif.io)

### How AAIF Enables AII Principles

| AII Principle | AAIF Implementation |
|---------------|---------------------|
| Action Loop | MCP enables agents to integrate external tools |
| Intent Understanding | AGENTS.md provides context for AI comprehension |
| Adaptive Response | goose demonstrates extensible agent patterns |

### Key Projects

```
┌─────────────────────────────────────────────────────────┐
│                        AAIF                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Model Context Protocol (MCP)                            │
│  • Open protocol for LLM-tool integration                │
│  • Standardized way for AI to use external tools         │
│  • Foundation for AII's "action loop"                    │
│                                                          │
│  goose                                                   │
│  • Extensible AI coding agent                            │
│  • Reference implementation of agent patterns            │
│  • Shows how AII principles work in practice             │
│                                                          │
│  AGENTS.md                                               │
│  • Standardized format for AI agent instructions         │
│  • How to give AI context about a project                │
│  • Enables intent understanding at repo level            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Founding Members

Anthropic, AWS, Block, Cloudflare, Google, Microsoft, OpenAI, and others.

### Relationship to AII

```
AII (Paradigm)              AAIF (Foundation)
━━━━━━━━━━━━━━              ━━━━━━━━━━━━━━━━━
Interaction design          Execution infrastructure
How humans & AI interact    How agents act autonomously
```

AAIF provides the technical infrastructure that makes AII possible. MCP is the plumbing; AII is the experience design.

---

## MCP — Model Context Protocol

**What:** Open protocol for connecting LLMs to external tools and data sources.

**Website:** [modelcontextprotocol.io](https://modelcontextprotocol.io)

### Role in AII

```
Without MCP:
  User: "Update the spreadsheet"
  AI: "I can't access spreadsheets directly. Here's what you could do..."

With MCP:
  User: "Update the spreadsheet"
  AI: [Connects to spreadsheet tool via MCP]
  AI: "Done. Updated 47 cells. Here's a summary of changes."
```

MCP is the enabling technology for AII's "action loop" — the ability to not just answer questions but complete tasks.

---

## Other Related Concepts

### Generative UI (GenUI)

AI-generated interfaces, often platform-specific. Overlaps with A2UI but typically more tightly coupled to specific platforms.

### Agentic UI

Interfaces designed for AI agent workflows. Focuses on the agent's needs rather than the human's — complementary to AII which focuses on human experience.

### AG UI / CopilotKit

Agent UI frameworks in the A2UI ecosystem. Implementation tools for building AII-style interfaces.

### Multimodal Interaction

Beyond text: voice, vision, gestures. AII encompasses multimodal but focuses on the interaction paradigm rather than specific modalities.

---

## How They Fit Together

```
When a user says "Show me sales trends"...

1. AII principles guide the interaction design
   → Understand intent, choose optimal form

2. AAIF/MCP enables tool access
   → Connect to data sources, execute queries

3. A2UI renders the response
   → Generate appropriate visual components

4. The user sees results and can interact further
   → Loop continues with AII guiding the experience
```

---

## Resources

### Official Links

| Project | Website | GitHub |
|---------|---------|--------|
| A2UI | [a2ui.org](https://a2ui.org) | [google/A2UI](https://github.com/google/A2UI) |
| AAIF | [aaif.io](https://aaif.io) | — |
| MCP | [modelcontextprotocol.io](https://modelcontextprotocol.io) | [modelcontextprotocol](https://github.com/modelcontextprotocol) |
| AGENTS.md | — | [anthropics/agents-md](https://github.com/anthropics/agents-md) |

### Further Reading

- [Google Blog: Introducing A2UI](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/)
- [Anthropic: MCP Announcement](https://www.anthropic.com/news/model-context-protocol)

---

## Next Steps

- [Core Philosophy](../philosophy/core-philosophy.md) — The foundation of AII
- [Design Principles](../principles/design-principles.md) — How to apply these concepts
- [Interaction Patterns](../patterns/interaction-patterns.md) — Practical patterns

