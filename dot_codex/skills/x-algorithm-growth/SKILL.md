---
name: x-algorithm-growth
description: Use when planning, reviewing, or drafting X posts to grow followers by applying the public xai-org/x-algorithm For You feed model: candidate sourcing, engagement prediction, profile/follow conversion, negative-signal avoidance, and build-in-public positioning. Especially useful for @tsonobe_ and the /Users/tsonobe/devs/x_foll workspace.
---

# Objective

Turn X follower-growth work into a repeatable posting system based on the public For You feed model, without pretending there is a guaranteed hack.

Optimize for:

1. candidate eligibility and discovery
2. predicted positive actions: like, reply, repost, quote, click, profile_click, dwell, follow_author
3. reduced negative actions: not_interested, block, mute, report
4. profile conversion: a visitor immediately understands why to follow
5. repeatable identity: the account becomes recognizable over time

# Use When

Use this skill when the user asks to:

- increase X followers
- apply the X / xAI algorithm to posting
- draft, review, or schedule posts for growth
- improve `@tsonobe_` positioning or pinned post
- analyze strong X posts and extract reusable patterns
- create a daily/weekly posting plan from local project work

# Source Policy

If the user asks about the latest algorithm, exact implementation, or claims tied to a current repo state, verify against official or primary sources first. Prefer:

- `https://github.com/xai-org/x-algorithm`
- local artifacts under `/Users/tsonobe/devs/x_foll` when the request is about the user's existing analysis

Treat X metrics, account samples, and algorithm details as time-sensitive snapshots. Say when a recommendation is an inference from the public model, not a confirmed ranking weight.

# Core Model

Use this mental model:

```text
candidate sources -> hydration -> filters -> scoring -> selection -> post-selection filters
```

Practical translation:

- Candidate sources: get posts into followed users' feeds and out-of-network discovery.
- Hydration: make the post and author easy to understand: text, media, topic, author identity.
- Filters: avoid spammy, duplicated, stale, muted, blocked, or low-quality signals.
- Scoring: increase the chance a viewer will like, reply, repost, click, dwell, visit profile, or follow.
- Selection: compete against other candidates with concrete, relevant, timely content.
- Post-selection: avoid content that creates policy, spam, or visibility risk.

# Default Strategy For @tsonobe_

Default positioning:

```text
An engineer steadily building a mindmap app, sharing visible product progress,
specific engineering/product lessons, unresolved UI/UX questions, and occasional
parenting/life constraints as human context.
```

Default mix:

- 50% build progress, screenshots, before/after, visible product evidence
- 25% technical notes, process lessons, product/engineering opinions
- 15% parenting or life context connected to building constraints
- 10% reactions, quote posts, timely comments

Do not optimize for generic tech tips alone. The durable follow reason is the visible journey of building the mindmap app.

# Workflow

## 1. Fix The Follow Reason

Before drafting a batch, check whether the profile gives a clear follow reason.

Minimum profile contract:

- what is being built
- why it matters
- what followers will see
- one concrete artifact if possible: screenshot, demo, before/after, or pinned thread

If the profile/pinned post is weak, recommend fixing it before optimizing individual posts.

## 2. Classify The Post Goal

Assign one primary goal before drafting:

- `artifact_progress`: show a concrete change
- `ux_question`: invite replies around a product decision
- `technical_note`: teach a specific implementation/process lesson
- `origin_story`: explain the lived pain behind the product
- `life_constraint`: connect parenting/life limits to the making process
- `opinion`: state a product/engineering view with concrete evidence
- `social_proof`: amplify user feedback or a milestone

Avoid posts whose only goal is "get engagement."

## 3. Draft With Positive Actions In Mind

For each post, deliberately design one or two positive actions:

- reply: ask a real unresolved decision or tradeoff
- repost/quote: make the insight compact and reusable
- click/profile_click: make the product identity visible enough to invite profile visits
- dwell: use a short structured explanation, before/after, or concrete story
- follow_author: connect the post to a continuing journey

Good pattern:

```text
<specific artifact or tension>

<why it matters / what changed>

<open question, concrete lesson, or next step>
```

Weak pattern:

```text
<generic thought>
<generic lesson>
<no visible product, no specific context>
```

## 4. Reduce Negative Signals

Actively remove:

- vague outrage or dunking
- engagement bait
- repeated near-duplicate posts
- overly broad AI/product takes without evidence
- pure diary posts detached from building, taste, or constraint
- hard sales language before the product is legible
- claims that may be false, stale, or unverifiable

If a post could attract blocks/mutes from the intended audience, rewrite it toward a useful observation or skip it.

## 5. Review A Draft

Score drafts on this checklist:

- `identity`: would a stranger know what this account is about?
- `artifact`: is there a concrete product/process detail?
- `action`: what positive action is the post designed to trigger?
- `specificity`: is the claim falsifiable or visibly grounded?
- `continuity`: does it make the next post easier to care about?
- `risk`: does it invite mute/block/report/not_interested?

Return direct edits, not only critique.

## 6. Build A Posting Plan

For a 7-day plan, prefer:

1. pinned/profile fix or product statement
2. visible feature progress
3. unresolved UX question
4. technical/process lesson
5. life constraint connected to building
6. before/after or demo
7. origin story or weekly learning

For each day, include:

- post goal
- draft text
- recommended media
- intended positive action
- risk to avoid

# Local Workspace Guidance

When working in `/Users/tsonobe/devs/x_foll`, useful local sources include:

- `x_growth_analysis_start.md`: account positioning and starter templates
- `x_growth_collected_strong_posts.md`: reusable strong-post patterns
- `pinned_post_drafts.md`: pinned-post options
- `daily_post_ideas/`: dated post ideas from recent work
- `daily_research/`: sampled reference-account observations

This workspace is not necessarily a git repository. Validate by direct file inspection and artifact checks instead of relying on `git status`.

# Output Shapes

For a strategy answer:

```text
結論:
根拠:
今日からやること:
投稿比率:
避けること:
最初の投稿案:
```

For draft review:

```text
判定:
強い点:
弱い点:
修正版:
狙う positive action:
避けた negative signal:
```

For a posting plan:

```text
方針:
7日分:
固定投稿/プロフィール変更:
検証方法:
```

# Stop Conditions

Stop and ask before:

- posting, deleting, or editing live X content
- using logged-in browser actions on X
- making claims about current algorithm internals without current verification
- turning private local project details into public posts when sanitization is uncertain

