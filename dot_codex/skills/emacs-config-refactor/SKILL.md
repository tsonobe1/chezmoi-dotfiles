---
name: emacs-config-refactor
description: Refactor and maintain the shared Emacs configuration in `~/.emacs.d` for a Syncthing-linked macOS and Windows setup. Use when the user wants behavior-preserving cleanup, smoke-harness-first refactoring, package/bootstrap consolidation, dead config removal after a baseline, or startup cleanup without breaking cross-OS compatibility.
---

# Emacs Config Refactor

## Use When

- The user wants to refactor or maintain the shared Emacs config in `~/.emacs.d`.
- Use for behavior-preserving cleanup, smoke-harness-first refactoring, package/bootstrap consolidation, dead config removal after a baseline, startup cleanup, or cross-OS portability work.
- Do not use this for generic Emacs Lisp work outside this repo, or for normal application code that only happens to be written in Emacs Lisp.

## Goal

Keep the shared macOS/Windows Emacs config maintainable without accidentally changing behavior, breaking Syncthing portability, or editing generated artifacts as the source of truth.

## Done

- The task type is classified before editing.
- `config/myinit.org` remains the primary editing surface unless the user explicitly changes the source-of-truth contract.
- Behavior-preserving work has a protected baseline or a stated verification gap.
- Smoke or cheap verification relevant to the slice has been run, or the blocker is reported.
- Commit, package strategy, source-of-truth, or broad removal gates are not crossed without explicit user confirmation.

## Stop

Stop and confirm when:

- changing the package-manager strategy or bootstrap order
- changing the source of truth away from `config/myinit.org`
- changing the Windows sync layout or path model
- removing features whose usage is still unclear
- making broad startup or performance changes without first protecting the baseline

## Overview

Use this skill for the shared Emacs config repo at `~/.emacs.d`, where the same files are synced to Windows and macOS. It keeps the work in the right order: stabilize current behavior first, then clean structure, then remove dead config or improve startup.

If the user wants explicit approval gates, structured `it.todo`, or strict TDD flow, combine this skill with `$collab-loop`. This skill provides Emacs-config-specific facts and workflow, not the outer collaboration contract.

## Current Repo Facts

- `init.el` loads `config/myinit.org` via `org-babel-load-file`
- Treat `config/myinit.org` as the source of truth
- Treat `config/myinit.el` as a generated or runtime artifact for verification, not the primary editing surface
- The config is shared to Windows through Syncthing, so OS-specific behavior must be preserved intentionally
- `config/secrets.el` is optional and should stay outside regression checks
- The lightweight smoke harness currently lives under `test/`

Read `references/repo-facts.md` for the current command patterns, verification command, and refactor checklist.

## Workflow

1. Classify the task before editing:
   - behavior-preserving refactor
   - behavior-changing cleanup
   - startup or performance pass
   - portability pass
2. For behavior-preserving refactors:
   - update or extend the smoke harness first
   - edit `config/myinit.org` in small slices
   - verify preserved user-visible behavior after each slice
3. Only after the baseline is protected:
   - remove unused packages, hooks, commands, or dead sections
   - consolidate package/bootstrap strategy
   - change startup behavior or OS abstractions
4. After each slice:
   - run the smoke tests
   - inspect the diff for accidental changes to generated or local-state files
   - call out unresolved Windows assumptions explicitly
5. Before any commit:
   - summarize what the commit will contain and get user confirmation before committing
   - rerun the stable smoke or other cheap verification relevant to the slice
   - perform a review and surface concrete findings before committing
   - fix review findings or get explicit user acceptance of the remaining risk
   - commit only after the verification result and review status are both clear

## Editing Rules

- Prefer editing `config/myinit.org`
- Do not hand-edit `config/myinit.el` unless the task is specifically about tangling output or verifying divergence
- Separate "refactor" from "improvement"; do not mix structural cleanup with feature removal in one step
- Centralize OS-specific paths and helpers before wide cleanup
- Be suspicious of repeated `require`, `package-install`, `package-refresh-contents`, `setq`, `add-hook`, and duplicate package initialization
- Do not delete a package or command only because it looks unused; first find its keybinding, hook, path dependency, or actual workflow
- Keep secrets and machine-local data out of tests
- If `custom-set-variables` or generated blocks are duplicated, decide one canonical location before further cleanup

## Verification

- Start with the existing smoke harness
- If the refactor touches new behavior, add or update smoke coverage before changing structure
- Keep tests isolated from network access, package installation, and secrets
- Prefer one command that stays stable and cheap enough to run repeatedly during refactor work
- Before committing, tell the user what the pending commit contains in concrete terms and wait for confirmation
- Treat commit-time verification as mandatory: before committing, rerun the smoke or cheap verification that protects the slice and report the result
- Treat review as a separate gate from test execution: do not commit immediately after tests pass; review the change and surface findings first

## Output

Final response should state what changed, what behavior was preserved or intentionally changed, verification result, unresolved OS assumptions, and the next safe action.

See `references/repo-facts.md` for the current smoke-test command and repo-specific grep patterns.

## Test Naming

- When adding or updating smoke tests, name tests in Japanese using `condition + result`
- Test names should describe observable Emacs-config behavior, not helper names or method-name paraphrases
- Do not put runner, temp-directory, stub, network-blocking, or other harness-only details into the test name unless the harness itself is the behavior under test
- If an internal identifier or helper name appears in a test name, rewrite it into user-understandable behavior when possible
- If the behavior you want to preserve is still unclear, clarify the behavior first instead of inventing a placeholder test name

## Invocation

Trigger this skill when the user says things like:

- `Emacs の設定を整理したい`
- `挙動を変えずに .emacs.d をリファクタしたい`
- `myinit.org を source of truth として整理したい`
- `Windows でも動くまま高速化したい`
- `使っていない設定を後で安全に消したい`
