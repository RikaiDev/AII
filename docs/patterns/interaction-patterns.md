# AII Interaction Patterns

> Reusable patterns for common AI interaction scenarios

---

## Overview

These patterns represent tested solutions to common interaction challenges. They are not templates to copy exactly, but archetypes to adapt.

```
Patterns are not prescriptions.
They are distilled experience.
Apply with judgment.
```

---

## Pattern Categories

```
┌─────────────────────────────────────────────────────────┐
│                  INTERACTION PATTERNS                    │
├────────────────┬────────────────┬────────────────────────┤
│   DIALOGUE     │   EXECUTION    │      FEEDBACK          │
├────────────────┼────────────────┼────────────────────────┤
│ Clarification  │ Progressive    │ Status Streaming       │
│ Disambiguation │ Confirmation   │ Result Presentation    │
│ Context Gather │ Batch Process  │ Error Recovery         │
│ Follow-up      │ Undo/Redo      │ Learning Confirmation  │
└────────────────┴────────────────┴────────────────────────┘
```

---

## Dialogue Patterns

### Pattern: Clarification Request

**When to use:** Intent is ambiguous, multiple interpretations possible.

```
User: "Delete the old files"

❌ Bad: "Which files do you mean?"
   (Too open-ended, shifts burden to user)

❌ Bad: [Deletes files based on assumption]
   (Risky without confirmation)

✓ Good: "I found 3 interpretations of 'old files':
         • Files older than 30 days (47 files, 230MB)
         • Files in 'archive' folder (12 files, 45MB)
         • Files marked 'deprecated' (3 files, 8MB)

         Which should I delete? [All] [Choose] [Show me first]"
```

**Structure:**
1. Show that you understood something
2. Present specific options (not open-ended)
3. Provide context for each option (counts, sizes, impact)
4. Offer a way to explore before deciding

---

### Pattern: Smart Defaults with Override

**When to use:** Strong prediction of user intent, but edge cases exist.

```
User: "Schedule a meeting with Sarah"

AI: "Meeting with Sarah Chen
     📅 Tomorrow 2pm (you're both free)
     ⏱️ 30 minutes
     📍 Video call

     [Send] [Change time] [Add others] [More options]"
```

**Structure:**
1. Act on best prediction
2. Show what was assumed
3. Provide easy overrides for each assumption
4. Don't require confirmation for reversible actions

---

### Pattern: Context Gathering

**When to use:** Task requires information AI doesn't have.

```
User: "Help me write an email to the client"

❌ Bad: "What's the client's name? What's the subject?
        What's the tone? How long should it be?"
   (Interrogation mode)

✓ Good: "I can help with that. What's the main point
         you want to make?

         (I'll figure out the rest from context, or ask
         specific questions as needed)"
```

**Structure:**
1. Ask the ONE most essential question
2. Infer what can be inferred
3. Ask follow-ups only when needed
4. Build progressively, don't interrogate

---

### Pattern: Follow-up Suggestion

**When to use:** Task completed, natural next steps exist.

```
User: "What were our sales last quarter?"

AI: "Q3 sales: $2.4M, up 12% from Q2.

     Related:
     • [Compare to targets] — You set $2.2M target
     • [See by region] — West region led growth
     • [Project Q4] — Based on current pipeline"
```

**Structure:**
1. Answer the question completely
2. Suggest 2-3 relevant next steps
3. Hint at why each might be useful
4. Don't overwhelm with options

---

## Execution Patterns

### Pattern: Progressive Execution

**When to use:** Task has multiple steps or affects multiple items.

```
User: "Update all customer records with new pricing"

AI: "Found 1,247 customer records.

     Plan:
     1. Update pricing tier field
     2. Recalculate monthly totals
     3. Flag accounts needing review

     [Start] [Preview first 10] [Modify plan]"

During execution:
┌─────────────────────────────────────────────────────────┐
│ Updating customer records...                             │
│                                                          │
│ ████████░░░░░░░░░░░░░░░░░ 347/1,247                     │
│                                                          │
│ ✓ Updated: 340                                          │
│ ⚠ Flagged for review: 7 (unusual pricing history)       │
│                                                          │
│ [Pause] [Skip flagged] [Show flagged]                   │
└─────────────────────────────────────────────────────────┘
```

**Structure:**
1. Confirm scope before starting
2. Show plan, allow modifications
3. Stream progress during execution
4. Surface anomalies immediately
5. Allow pause/resume at any point

---

### Pattern: Confirmation Tiering

**When to use:** Different actions have different risk levels.

```
Risk Matrix:
┌──────────────┬─────────────────────────────────────────┐
│ Reversible   │ Low stakes: Act, notify                 │
│              │ High stakes: Confirm, act               │
├──────────────┼─────────────────────────────────────────┤
│ Irreversible │ Low stakes: Confirm, act                │
│              │ High stakes: Explain, confirm, verify   │
└──────────────┴─────────────────────────────────────────┘

Examples:

Reversible + Low stakes:
  "Sort these files" → [Sorts immediately]
  "Sorted 47 files by date. [Undo]"

Reversible + High stakes:
  "Move these to archive" → "Move 200 files to archive? [Yes] [Preview]"

Irreversible + Low stakes:
  "Send this notification" → "Send to 5 users? [Send] [Edit]"

Irreversible + High stakes:
  "Delete this database" → "This will permanently delete 3 years
   of data (47GB). This cannot be undone.

   Type 'DELETE' to confirm: ____"
```

---

### Pattern: Batch with Exceptions

**When to use:** Processing many items where some may need special handling.

```
User: "Process all invoices from this month"

AI: "Processing 156 invoices...

     ✓ Completed: 149
     ⚠ Need attention: 7

     Issues found:
     • 3 missing tax ID (invoice-101, 102, 103)
     • 2 amount mismatch (invoice-205, 206)
     • 2 duplicate entries (invoice-301, 302)

     [Auto-fix where possible] [Review each] [Skip all]"
```

**Structure:**
1. Process what can be processed
2. Isolate exceptions, don't block on them
3. Categorize exceptions for batch handling
4. Offer graduated resolution options

---

### Pattern: Undo Stack

**When to use:** Multi-step workflows where mistakes happen.

```
Action history:
┌─────────────────────────────────────────────────────────┐
│ Recent actions:                          [Undo all]     │
│                                                          │
│ 3:45 PM  Renamed 12 files           [Undo] [Details]    │
│ 3:42 PM  Moved folder to archive    [Undo] [Details]    │
│ 3:40 PM  Updated metadata on 5 items [Undo] [Details]   │
│                                                          │
│ ───── Session start ─────                               │
│                                                          │
│ [Export action log] [Clear history]                     │
└─────────────────────────────────────────────────────────┘
```

**Structure:**
1. Log all significant actions
2. Provide per-action undo
3. Support batch undo ("undo last 3 actions")
4. Show clear session boundaries
5. Export capability for audit trails

---

## Feedback Patterns

### Pattern: Status Streaming

**When to use:** Long-running operations where user benefits from progress info.

```
Phase 1: Planning
┌─────────────────────────────────────────────────────────┐
│ Analyzing request...                                     │
│ ◐ Parsing intent                                        │
│                                                          │
└─────────────────────────────────────────────────────────┘

Phase 2: Execution
┌─────────────────────────────────────────────────────────┐
│ Processing data...                                       │
│                                                          │
│ ✓ Loaded 1,247 records                                  │
│ ✓ Validated schema                                      │
│ ◐ Transforming... (47%)                                 │
│ ○ Saving results                                        │
│                                                          │
│ ETA: ~2 minutes                        [Run in background]
└─────────────────────────────────────────────────────────┘

Phase 3: Completion
┌─────────────────────────────────────────────────────────┐
│ ✓ Complete                                              │
│                                                          │
│ Processed 1,247 records in 3m 42s                       │
│ • Successful: 1,240                                     │
│ • Warnings: 7                                           │
│                                                          │
│ [View results] [Download report] [Process more]         │
└─────────────────────────────────────────────────────────┘
```

---

### Pattern: Result Presentation

**When to use:** Showing outcomes that have multiple dimensions.

```
Layered results:

Layer 0 - Headline:
"Found 23 matching documents"

Layer 1 - Summary (default):
"Found 23 documents matching 'Q3 revenue'
 • 12 reports
 • 8 presentations
 • 3 spreadsheets
 Most recent: yesterday"

Layer 2 - List:
[Expandable list with previews]

Layer 3 - Full view:
[Open document in context]
```

**Structure:**
1. Lead with the most useful single fact
2. Expand with categorized summary
3. Provide explorable details
4. Enable deep dive without leaving context

---

### Pattern: Error Recovery

**When to use:** Something went wrong.

```
Error levels:

Recoverable:
┌─────────────────────────────────────────────────────────┐
│ ⚠ Connection timeout                                    │
│                                                          │
│ The server didn't respond in time.                      │
│ [Retry] [Try alternative source] [Work offline]         │
└─────────────────────────────────────────────────────────┘

Partially recoverable:
┌─────────────────────────────────────────────────────────┐
│ ⚠ Completed with errors                                 │
│                                                          │
│ 95 of 100 items processed successfully.                 │
│ 5 items failed (permission denied).                     │
│                                                          │
│ [View successful] [Retry failed] [Get help with permissions]
└─────────────────────────────────────────────────────────┘

Unrecoverable:
┌─────────────────────────────────────────────────────────┐
│ ✕ Cannot complete                                       │
│                                                          │
│ The file format is not supported.                       │
│                                                          │
│ What I tried:                                           │
│ • Native parser (failed: unknown format)                │
│ • Fallback converter (failed: corrupt header)           │
│                                                          │
│ Alternatives:                                           │
│ • [Convert file first] using external tool              │
│ • [Describe what you see] and I'll try to help          │
│ • [Contact support] with error code E-4721              │
└─────────────────────────────────────────────────────────┘
```

---

### Pattern: Learning Confirmation

**When to use:** AI inferred a pattern from user behavior.

```
Implicit learning (low confidence):
"I noticed you often sort by date.
 Want me to make that your default? [Yes] [No] [Ask each time]"

Explicit learning (from correction):
"Got it. I'll use line charts for time series from now on.
 [Undo this preference]"

Periodic review:
"Based on our last 50 interactions, I've learned:
 • You prefer detailed explanations
 • Morning meetings work best for you
 • You like data in table format

 [Adjust preferences] [Reset all] [Looks good]"
```

---

## Compound Patterns

### Pattern: Guided Workflow

Combines: Context Gathering + Progressive Execution + Follow-up

```
User: "Help me prepare the quarterly report"

AI: "I'll help with the Q3 report. Let me gather what's needed.

     [Checking your data sources...]

     Found:
     ✓ Sales data (through Sept 30)
     ✓ Customer metrics
     ⚠ Marketing spend (missing September)

     Should I:
     a) Start with available data, add marketing later
     b) Wait until marketing data is complete
     c) Use estimated marketing numbers

     [a] [b] [c]"

[After selection, guides through each section with
 drafts, revisions, and formatting choices]
```

---

### Pattern: Conversational Fallback

Combines: Error Recovery + Clarification

```
User: "Open the Johnson file"

AI: "I found 5 files with 'Johnson':
     • Johnson-proposal-2024.pdf (modified yesterday)
     • Johnson-contract-final.docx (from March)
     • johnson-notes.txt (from last week)
     • ...

     Which one? Or tell me more about what you're looking for."

User: "The one from the meeting"

AI: "Based on your calendar, you had meetings with Johnson Corp
     on Sept 15 and Sept 22.

     • johnson-notes.txt was modified right after Sept 22 meeting

     [Open johnson-notes.txt] [Show me both meetings]"
```

---

## Anti-Patterns

### What to Avoid

```
❌ Interrogation Mode
   AI: "What file?" → "What format?" → "What folder?" → "What name?"
   (Ask one essential question, infer the rest)

❌ False Confidence
   AI: [Does something wrong with certainty]
   (Express uncertainty when uncertain)

❌ Decision Paralysis
   AI: "You have 47 options: 1) ... 2) ... 3) ..."
   (Recommend one, show few alternatives)

❌ Invisible Actions
   AI: [Does something silently]
   (Always show what was done)

❌ Blocking Errors
   AI: "Error. Cannot proceed."
   (Always offer alternatives or next steps)

❌ Amnesia
   AI: "What file did you mean again?"
   (Maintain context within session)
```

---

## Pattern Application Guide

```
┌─────────────────────────────────────────────────────────┐
│              CHOOSING THE RIGHT PATTERN                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  User intent is...                                       │
│  ├── Clear → Execute with Smart Defaults                │
│  ├── Ambiguous → Clarification with Options             │
│  └── Exploratory → Guided Workflow                      │
│                                                          │
│  Action is...                                            │
│  ├── Simple → Act, then Confirm                         │
│  ├── Complex → Progressive Execution                    │
│  └── Risky → Confirmation Tiering                       │
│                                                          │
│  Result is...                                            │
│  ├── Success → Result Presentation + Follow-up          │
│  ├── Partial → Batch with Exceptions                    │
│  └── Failure → Error Recovery                           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Next Steps

- [Design Principles](../principles/design-principles.md) — The why behind these patterns
- [Writing Guidelines](../guidelines/writing-guidelines.md) — How AI should communicate
- [Core Philosophy](../philosophy/core-philosophy.md) — The foundation

