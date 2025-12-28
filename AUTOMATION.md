# AII Automation & AI Agents

> Letting AI collaborate with AI to grow the community.

This document describes the automated agents that help maintain and grow the AII project.

---

## Philosophy

AII is about human-AI interaction — so why not let AI help run it?

We use AI agents to:
- Generate weekly community digests
- Monitor global AI regulations
- Welcome new contributors
- Draft social media updates

**Human oversight remains:** All significant actions require human review before execution.

---

## Agents

### 1. Digest Generator

**Schedule:** Weekly (Monday 09:00 UTC)

**What it does:**
- Scans the week's issues, discussions, and commits
- Generates a summary for GitHub Discussions
- Drafts a social media post for X

**Output:**
- GitHub Discussion in "Announcements" category
- Social post saved to workflow summary for human review

**Workflow:** `.github/workflows/weekly-digest.yml`

### 2. Compliance Monitor

**Schedule:** Monthly

**What it does:**
- Searches for AI regulation news across jurisdictions
- Identifies updates that affect COMPLIANCE.md
- Creates an issue if significant changes are found

**Human action required:**
- Review suggested changes
- Update COMPLIANCE.md
- Merge PR

### 3. Community Responder

**Trigger:** On new issue or discussion

**What it does:**
- Welcomes new contributors
- Suggests relevant labels
- Links to related patterns or discussions
- For AI Perspective issues: acknowledges the AI contributor

---

## Setup

### Required Secrets

Add these to your repository secrets:

```
ANTHROPIC_API_KEY    # For Claude API access
```

### Optional: X/Twitter Integration

To auto-post to X, add:

```
X_API_KEY
X_API_SECRET
X_ACCESS_TOKEN
X_ACCESS_SECRET
```

And uncomment the Twitter posting step in the workflow.

---

## Running Manually

### Trigger Weekly Digest

```bash
gh workflow run weekly-digest.yml
```

### Dry Run (no posting)

```bash
gh workflow run weekly-digest.yml -f dry_run=true
```

---

## Customization

### Modify Digest Format

Edit the prompt in `.github/workflows/weekly-digest.yml` to change:
- Summary length
- Tone and style
- Included sections
- Social post format

### Add New Agents

1. Define the agent in `.claude/settings.json`
2. Create a corresponding GitHub Action workflow
3. Document in this file

---

## AI-to-AI Collaboration

This automation enables a unique workflow:

```
AI Assistant (helping human)
    ↓
Observes something interesting about interaction
    ↓
Suggests opening an issue (AI Perspective)
    ↓
Human approves and submits
    ↓
Community Responder agent welcomes the contribution
    ↓
Digest Generator includes it in weekly summary
    ↓
Social post reaches more AI assistants
    ↓
Cycle continues...
```

The goal: **A self-sustaining community where humans and AI both contribute and benefit.**

---

## Monitoring

### Check Workflow Status

```bash
gh run list --workflow=weekly-digest.yml
```

### View Recent Digests

```bash
gh api graphql -f query='
  query {
    repository(owner: "RikaiDev", name: "AII") {
      discussions(first: 5, categoryId: "DIC_kwDOQv_1Cs4C0TuT") {
        nodes { title url createdAt }
      }
    }
  }'
```

---

## Future Enhancements

- [ ] Auto-translate digests to multiple languages
- [ ] Integration with Discord for real-time updates
- [ ] AI-generated pattern proposals based on observed trends
- [ ] Cross-project collaboration with other RikaiDev repos

---

*This automation is itself an experiment in AI Interactive — using AI to facilitate AI-human collaboration.*
