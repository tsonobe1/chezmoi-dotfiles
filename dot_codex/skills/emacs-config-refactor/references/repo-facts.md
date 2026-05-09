# Repo Facts

Use this reference for concrete repo-local facts and command patterns while applying `$emacs-config-refactor`.

## Current Facts

- Repo root: `~/.emacs.d`
- Load chain: `init.el` -> `org-babel-load-file` -> `config/myinit.org`
- Primary edit surface: `config/myinit.org`
- Verification artifact: `config/myinit.el`
- Optional local secret file: `config/secrets.el`
- Current smoke harness:
  - `test/config-smoke.el`
  - `test/support/config-harness.el`
  - `test/support/stubs.el`

## Current Smoke-Test Command

```sh
emacs --batch -Q -L test/support -l test/config-smoke.el -f ert-run-tests-batch-and-exit
```

This harness is designed to keep package installation, network access, and secrets outside the regression loop.

## Recommended Refactor Order

1. Confirm source of truth and load chain
2. Expand or adjust smoke coverage for the behavior you plan to preserve
3. Refactor only structure:
   - package/bootstrap initialization
   - OS-specific path helpers
   - duplicated `setq` / `add-hook` / `require`
   - placement of generated or custom blocks
4. Run smoke tests
5. Only then remove dead config or change startup behavior

## Useful Command Patterns

Check the load chain:

```sh
sed -n '1,40p' init.el
```

Inspect section structure in the org source:

```sh
rg -n "^\\*+ " config/myinit.org
```

Find high-risk initialization and duplication points:

```sh
rg -n "package-install|package-refresh-contents|package-initialize|require 'package|if \\(eq system-type 'windows-nt|custom-set-variables|custom-set-faces|org-babel-do-load-languages|global-set-key|add-hook|use-package" config/myinit.el
```

Final whitespace sanity after edits:

```sh
git diff --check
```

## Interpretation Rules

- If `config/myinit.org` and `config/myinit.el` disagree, prefer the org source unless the task is explicitly about tangling or generated output
- Treat startup optimization as behavior-changing whenever it changes load order or lazy-loading behavior
- Treat package-manager consolidation as a decision point, not as routine cleanup
- Treat Windows path changes as portability work, not as harmless refactor

## Good Task Splits

### Behavior-Preserving Refactor

- extract OS path helpers
- consolidate package initialization into one place
- remove obvious duplicated settings without changing effective values
- move generated/custom blocks to one canonical location

### Behavior-Changing Cleanup

- remove apparently unused packages
- delete commands with no proven workflow
- change completion stack or theme behavior
- change startup loading strategy

For behavior-changing cleanup, extend the baseline first and make the intended behavior change explicit.
