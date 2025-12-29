# AII Design Principles

> Guidelines for building AI Interactive systems

---

## Overview

These principles guide the design of AII systems. They are not rules to follow blindly, but lenses through which to evaluate interaction decisions.

```
The best interface is no interface.
The best form is the right form.
The best AI is one that learns from you.
```

---

## Principle 1: Intent Over Interface

### The Problem

Traditional interfaces force users to translate their intent into interface language:

```
User thinks: "I need to understand why sales dropped"

Traditional UI requires:
1. Open analytics dashboard
2. Navigate to sales section
3. Select date range
4. Choose comparison view
5. Apply filters
6. Interpret chart
7. Export data
8. Open spreadsheet
9. Run analysis
10. Form conclusion

10 steps. 15 clicks. 5 minutes. Mental overhead at each step.
```

### The AII Way

```
User: "Why did sales drop last week?"

AII:
1. Understands the actual question (causal analysis, not just data)
2. Gathers relevant data
3. Analyzes patterns
4. Identifies likely causes
5. Presents findings in digestible form

"Sales dropped 12% last week. Primary driver:
 Marketing campaign ended on the 15th (accounts for ~9%).
 Secondary: Competitor launched promotion (accounts for ~3%).

 [Show supporting data] [Compare to similar periods]"
```

### Implementation Guidelines

| Don't | Do |
|-------|-----|
| Design menus | Design conversations |
| Add features | Understand needs |
| Require navigation | Infer context |
| Show all options | Show relevant options |
| Make users search | Anticipate questions |

---

## Principle 2: Adaptive Modality

### The Spectrum

```
Pure Dialogue          Hybrid                Pure Visual
     │                    │                       │
     ▼                    ▼                       ▼
  Voice/Text        Chat + Canvas          Dashboard/Map
     │                    │                       │
When it works:      When it works:         When it works:
• Quick queries     • Creative tasks       • Data overview
• Hands-free        • Iteration needed     • Spatial info
• Simple actions    • Mixed media          • Monitoring
• Sequential flow   • Collaboration        • Dense info
```

### Context Determines Form

The same intent may require different forms based on:

```
┌─────────────────────────────────────────────────────────┐
│                    CONTEXT FACTORS                       │
├──────────────┬──────────────┬──────────────┬────────────┤
│     WHO      │    WHERE     │     WHEN     │    WHAT    │
├──────────────┼──────────────┼──────────────┼────────────┤
│ Role         │ Device       │ Time avail.  │ Task type  │
│ Expertise    │ Environment  │ Urgency      │ Complexity │
│ Preferences  │ Noise level  │ Frequency    │ Data type  │
│ History      │ Privacy      │ Deadline     │ Stakes     │
└──────────────┴──────────────┴──────────────┴────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Optimal Form   │
                    │    Emerges      │
                    └─────────────────┘
```

### Examples

```
Intent: "Show me the project status"

Context A: PM in meeting, phone, 30 seconds
→ Form: Voice summary
→ "Project Alpha is on track. Two items flagged for review."

Context B: Developer at desk, monitor, 5 minutes
→ Form: Kanban board with filters
→ [Visual board with drag-drop, filters, detail panels]

Context C: Executive in car, voice only
→ Form: Audio briefing
→ Spoken summary with follow-up questions

Same intent. Different optimal forms.
```

---

## Principle 3: Action, Not Just Answers

### Beyond Information Retrieval

```
Traditional AI:
  User: "How do I sort this list?"
  AI: "You can use the sort() method with a key parameter..."
  User: [Still has to implement it]

AII:
  User: "Sort this list by date"
  AI: [Sorts the list]
  AI: "Done. Sorted 47 items by date, newest first.
       [Undo] [Sort differently] [Save as default]"
```

### The Action Loop

```
┌─────────────────────────────────────────────────────────┐
│                     ACTION LOOP                          │
│                                                          │
│    ┌──────────┐                                         │
│    │ Observe  │ ← What is the current state?            │
│    └────┬─────┘                                         │
│         │                                                │
│    ┌────▼─────┐                                         │
│    │Understand│ ← What does the user actually need?     │
│    └────┬─────┘                                         │
│         │                                                │
│    ┌────▼─────┐                                         │
│    │   Act    │ ← Take concrete action                  │
│    └────┬─────┘                                         │
│         │                                                │
│    ┌────▼─────┐                                         │
│    │ Feedback │ ← Show what was done, get confirmation  │
│    └────┬─────┘                                         │
│         │                                                │
│    ┌────▼─────┐                                         │
│    │  Adjust  │ ← Refine based on feedback              │
│    └────┬─────┘                                         │
│         │                                                │
│    ┌────▼─────┐                                         │
│    │  Learn   │ ← Remember for next time                │
│    └──────────┘                                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Levels of Action

| Level | Description | Example |
|-------|-------------|---------|
| **Inform** | Provide information | "The file is in /docs" |
| **Guide** | Step-by-step instructions | "First open settings, then..." |
| **Assist** | Do it with confirmation | "I can rename these. Proceed?" |
| **Execute** | Just do it | [Renames files silently] |
| **Anticipate** | Do it before asked | [Auto-saves when detecting risk] |

Choose the appropriate level based on:
- Task reversibility
- User expertise
- Historical preferences
- Stakes involved

---

## Principle 4: Human Control

### Always Interruptible

```
┌─────────────────────────────────────────────────────────┐
│ AI executing task...                                     │
│                                                          │
│ ████████████░░░░░░░░░░░░ 45% complete                   │
│                                                          │
│ Currently: Processing invoice-2024-003.pdf               │
│ Completed: 127 files                                     │
│ Remaining: 156 files                                     │
│                                                          │
│ [Esc] Pause   [Enter] Details   [Q] Cancel all          │
└─────────────────────────────────────────────────────────┘

After pause:
┌─────────────────────────────────────────────────────────┐
│ Paused at 45%                                            │
│                                                          │
│ Options:                                                 │
│ • [Continue] Resume from current position                │
│ • [Review] See what's been done so far                   │
│ • [Adjust] Change parameters, then continue              │
│ • [Revert] Undo all changes made                         │
│ • [Stop] Keep changes, stop processing                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Transparency Levels

```
Level 1: Silent
  AI acts, user sees only results
  Use for: Routine, low-stakes, reversible

Level 2: Notify
  AI acts, user is informed
  Use for: Expected actions, medium stakes

Level 3: Confirm
  AI proposes, user approves
  Use for: Significant changes, learning phase

Level 4: Explain
  AI proposes with reasoning, user decides
  Use for: High stakes, unusual situations

Level 5: Consult
  AI presents options, user chooses
  Use for: Preference-based, multiple valid paths
```

### Graceful Degradation

When AI is uncertain or unavailable:

```
High Confidence          Low Confidence          No AI Available
      │                        │                        │
      ▼                        ▼                        ▼
  [Execute]              [Suggest with              [Show traditional
   directly                caveats]                   interface]
      │                        │                        │
      └────────────────────────┴────────────────────────┘
                               │
                    User never gets stuck
```

---

## Principle 5: Learning System

### Individual Learning

```
Session 1:
  User: "Make a chart of this data"
  AI: [Creates bar chart]
  User: "No, I always use line charts for time series"
  AI: [Switches to line chart]
       "Noted: Line charts for time series data."

Session 47:
  User: "Chart this"
  AI: [Detects time series, creates line chart automatically]
```

### Learning Categories

| Category | What's Learned | Privacy Level |
|----------|----------------|---------------|
| **Preferences** | Chart types, formats, styles | User-specific |
| **Patterns** | Work rhythms, common tasks | User-specific |
| **Domain** | Industry terms, company context | Org-specific |
| **Interaction** | Communication style, detail level | User-specific |

### Correction Protocol

```
When AI makes a mistake:

1. Acknowledge immediately
   "You're right, I misunderstood."

2. Correct the action
   [Makes the correction]

3. Extract the learning
   "I'll remember: [specific pattern]"

4. Verify the learning
   "In the future, should I [new behavior]?"

5. Apply consistently
   [Uses learning in similar future situations]
```

---

## Principle 6: Progressive Disclosure

### Information on Demand

```
Default View:
┌─────────────────────────────────────────────────────────┐
│ Analysis complete. Revenue up 15%. [Details]             │
└─────────────────────────────────────────────────────────┘

On [Details]:
┌─────────────────────────────────────────────────────────┐
│ Revenue Analysis                                         │
│                                                          │
│ Total: $3.2M (+15% YoY)                                 │
│                                                          │
│ By segment:                                              │
│ • Enterprise: $2.1M (+22%)                              │
│ • SMB: $0.8M (+5%)                                      │
│ • Consumer: $0.3M (-3%)                                 │
│                                                          │
│ [Raw Data] [Methodology] [Compare Periods]              │
└─────────────────────────────────────────────────────────┘
```

### Complexity Layering

```
Layer 0: Result
  "Done."

Layer 1: Summary
  "Processed 500 records, 3 warnings."

Layer 2: Details
  "Warnings in: invoice-103, invoice-287, invoice-456
   Reason: Missing customer ID field"

Layer 3: Technical
  "Validation failed at schema.customer.id (required field)
   Attempted fallback: customer_legacy_id (not found)
   Records quarantined for manual review"

Layer 4: Debug
  [Full logs, stack traces, raw data]
```

---

## Anti-Patterns

### What AII is NOT

```
❌ AI that pretends to be human
   → AII is transparent about being AI

❌ AI that never admits uncertainty
   → AII says "I'm not sure" when appropriate

❌ AI that takes over completely
   → AII keeps humans in control

❌ AI that learns everything
   → AII respects privacy boundaries

❌ AI that changes behavior unpredictably
   → AII is consistent within learned preferences

❌ AI that requires AI to function
   → AII degrades gracefully to traditional UI
```

---

## Implementation Checklist

When designing an AII interaction:

- [ ] Can the user express intent naturally?
- [ ] Does the form match the context?
- [ ] Does it take action, not just answer?
- [ ] Can the user interrupt at any point?
- [ ] Is the AI's reasoning transparent when needed?
- [ ] Does it learn from corrections?
- [ ] Does it degrade gracefully without AI?
- [ ] Is user privacy respected?

---

## Next Steps

- [Interaction Patterns](../patterns/interaction-patterns.md) — Common patterns for AII systems
- [Writing Guidelines](../guidelines/writing-guidelines.md) — How to communicate in AII
- [Ecosystem](../ecosystem/overview.md) — Related projects and standards

