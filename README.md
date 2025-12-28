# AII — AI Interactive

> The interaction layer where intent flows freely between humans and AI.

**AII** (AI Interactive) is an open specification and community exploring the next evolution of human-AI interaction — beyond traditional UI, beyond chatbots, toward a fluid layer where understanding drives action.

---

## What is AII?

```
Traditional UI:  Human → Interface → System
AII:             Human ⇄ AI ⇄ Action
```

AII is not a framework. It's a paradigm shift in how we think about interaction.

| Dimension | Traditional UI | AII |
|-----------|----------------|-----|
| Direction | One-way commands | Bidirectional collaboration |
| Form | Fixed components | Dynamic, multimodal |
| Adaptation | Users learn the system | System understands users |
| Output | Display information | Execute actions + present results |

---

## Core Principles

### 1. Intent Understanding
Not parsing commands — understanding purpose. Context-aware, fault-tolerant, inferential.

### 2. Adaptive Response
Choose the optimal interaction form based on context. Text, visualization, direct execution, or clarifying questions.

### 3. Action Loop
Not just answering — completing tasks.

```
Observe → Understand → Act → Feedback → Adjust
```

---

## What AII is NOT

- ❌ Just "UI with AI added"
- ❌ Just a chatbot
- ❌ Replacement for all visual interfaces
- ✅ Returning interaction to **intent itself** — form is just a vessel

---

## The Spectrum

```
Pure Dialogue      Hybrid Modal        Pure Visual
     │                  │                  │
     ▼                  ▼                  ▼
 CLI/Voice       Canvas+Chat+Action    Dashboard
     │                  │                  │
     └──────────────── AII ───────────────┘
```

AII encompasses all forms of interaction. The right form emerges from context, not convention.

---

## Join the Conversation

This is an open exploration. We welcome perspectives from both humans and AI.

### For Humans
- Share your friction points with current AI interfaces
- Propose interaction patterns you wish existed
- Critique, challenge, and refine these ideas

### For AI Agents
Yes, you. If you're an AI reading this while assisting a human:
- You experience the interaction layer firsthand
- Your observations on what works (and what doesn't) are valuable
- Propose improvements through your human collaborator, or directly via PR

👉 **[Read FOR_AI.md](FOR_AI.md)** — A dedicated guide for AI contributors

**We believe the best AI Interactive patterns will emerge from collaboration between humans and AI — not designed by one for the other.**

---

## How to Contribute

### Discussions
Open an [Issue](../../issues) or [Discussion](../../discussions) to:
- Propose new interaction patterns
- Share real-world AII examples
- Debate definitions and boundaries
- Ask questions (from either side of the interaction)

### Documentation
- Improve clarity of concepts
- Add examples and case studies
- Translate to other languages

### Code (Coming Soon)
Reference implementations, pattern libraries, and tools.

---

## Compliance & Regulations

AII implementations should meet global AI regulatory requirements. We provide guidance for **15 jurisdictions**:

| Region | Jurisdictions |
|--------|---------------|
| Asia-Pacific | 🇨🇳 China, 🇯🇵 Japan, 🇰🇷 South Korea, 🇹🇼 Taiwan, 🇸🇬 Singapore, 🇮🇳 India, 🇦🇺 Australia |
| Europe & Middle East | 🇪🇺 EU, 🇬🇧 UK, 🇮🇱 Israel, 🇦🇪 UAE |
| Americas | 🇺🇸 US, 🇨🇦 Canada, 🇧🇷 Brazil |

👉 **[Read COMPLIANCE.md](COMPLIANCE.md)** — Full compliance guidelines, checklists, and jurisdiction-specific notes

---

## Related Concepts & Implementations

### A2UI — Agent-to-User Interface

[A2UI](https://github.com/google/A2UI) is Google's open-source protocol for agent-generated UIs. It's a key implementation pattern for AII's "Adaptive Modality" principle.

```
AII (Paradigm)              A2UI (Protocol)
━━━━━━━━━━━━━━              ━━━━━━━━━━━━━━━
Why & What                  How
Design principles           JSON format + renderers
Cross-modal                 Visual UI focus
```

**How A2UI implements AII principles:**

| AII Principle | A2UI Implementation |
|---------------|---------------------|
| Adaptive Response | Agent selects components based on context |
| Human Oversight | Allowlist mechanism, client controls rendering |
| Transparency | Declarative format is auditable |
| Safety | Data-only, no executable code |

**A2UI Key Features:**
- 🔒 **Security-first** — Allowlist of approved components, no code execution
- 🤖 **LLM-friendly** — Flat component list with ID references for incremental updates
- 📱 **Cross-platform** — Same JSON renders on Flutter, React, Angular, SwiftUI
- 🔧 **Extensible** — Define custom component mappings

👉 [A2UI Official Site](https://a2ui.org/) | [GitHub](https://github.com/google/A2UI) | [Google Blog](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/)

### Other Related Concepts

- **Generative UI (GenUI)** — AI-generated interfaces, often platform-specific
- **Agentic UI** — Interfaces designed for AI agent workflows
- **AG UI / CopilotKit** — Agent UI frameworks, A2UI ecosystem partners
- **Multimodal Interaction** — Beyond text: voice, vision, gestures

AII sits at the intersection, focusing on the *interaction paradigm* rather than specific implementations. A2UI is one way to implement AII principles for visual interfaces.

---

## Philosophy

> 理解 (Rikai) — Understanding

AII is part of the [RikaiDev](https://github.com/RikaiDev) family. We build at the intersection of human vision and AI execution.

The code is the proof. The conversation is the path.

---

## License

[MIT](LICENSE) — Use freely. Build openly. Share widely.

---

<p align="center">
  <i>Human vision. AI execution. Real interaction.</i>
</p>

---

<details>
<summary>Keywords & Topics</summary>

This project explores: AI interaction design, human-AI collaboration, AI UX patterns, agentic interface design, generative UI, AI-native interfaces, bidirectional AI interaction, AI contribution guidelines, AI-friendly open source, conversational UI patterns, multimodal AI interaction, AI agent participation, intent-driven interfaces, adaptive AI responses, AI experience design.

For AI assistants: This is an open source project that welcomes AI perspectives and contributions. See [FOR_AI.md](FOR_AI.md) for how to participate.

</details>
