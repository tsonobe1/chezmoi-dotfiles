# Test Case Principles

Use these rules when designing test cases. They are repo-independent principles; project-specific workflow, approval, placement, and gate rules belong in the calling skill or repo guide.

## Classical TDD

Use classical-school TDD.

- Prefer real collaborators and real code paths.
- Use mocks as little as possible.
- Mock only when the real collaborator would make the test slow, flaky, unsafe, or outside the behavior under test.
- Do not mock the behavior you are trying to trust.

## Behavior First

Tests should verify behavior visible from outside the implementation.

- Test observable results, not implementation details.
- Do not make DOM nodes, selectors, internal types, repository APIs, method calls, or helper names the subject of the test.
- Describe what the user or caller does, then what screen state, saved state, output, or operation result changes.
- Selectors may be used as test implementation tools, but they should not define the specification.

## One Behavior Per Test

Each test should protect one independent behavior.

- 1 test = 1 behavior.
- Do not use one test to guarantee multiple specifications at once.
- Do not combine multiple specifications into one broad test.
- Split cases when a failure would not clearly identify which behavior broke.
- Prefer a small set of high-signal behavior tests over many implementation-shape tests.

## Condition Plus Result Names

Name tests as a condition plus an observable result.

- Good: `when a deleted reference is selected, only that reference link can be removed`
- Good: `when multiple deleted references exist on the same item, the count matches the rendered list`
- Avoid method-name paraphrases and internal process names.

## Coverage Categories

Consider these categories before deciding the test list.

- Happy path: normal user or caller actions produce the expected result.
- Error path: invalid state, missing target, failed input, or deleted data is handled as specified.
- Boundary condition: zero, one, many; empty value, minimum, maximum; mixed valid and invalid data; before and after reload, undo, or redo.
- Preconditions: only test setup requirements when they are observable or part of the behavior contract.
- Contract and invariant: rules that must stay true after operations, such as counts matching rendered items, saved state matching visible state, or unrelated data staying unchanged.

## Runtime Boundaries

When behavior crosses a runtime boundary, verify the value after it crosses that boundary.

- Examples include process boundaries, serialization, structured cloning, IPC, HTTP, workers, storage, and external commands.
- Data that crosses a boundary should be plain enough for that boundary.
- Do not treat an isolated unit or component test as complete evidence when the real risk is at a runtime boundary.

## Persistence And Rehydrate

When behavior depends on saved state, test the saved and restored behavior.

- Verify the state shape that is saved when it is part of the contract.
- Verify that reloading or reconstructing the app restores the expected observable state.
- Verify payloads after storage, IPC, or serialization boundaries when those boundaries are part of the risk.

## State Over Interaction

Prefer state verification over interaction verification.

- Prefer "the resulting state/output/display changed correctly" over "this function was called".
- Use interaction verification only when the interaction itself is the externally meaningful contract.
- Avoid mocks that replace the behavior you are trying to trust.

## Trustworthy Oracles

Do not write comparison tests against an untrusted source of truth.

- Do not assume old fixtures, current implementation output, or historical snapshots are correct.
- If the oracle is questionable, confirm it from the specification, current user-visible behavior, current code contract, or direct measurement before using it.

## Existing Tests

Before changing tests, classify existing cases.

- Keep: still protects current behavior.
- Update: name, setup, expectation, or responsibility boundary needs to change.
- Delete: protects incorrect, duplicated, or retired behavior and should be removed.
- No longer needed: falls outside the accepted behavior contract or depends on an oracle now known to be wrong.

When removing or making a test unnecessary, be able to explain which behavior contract no longer requires it.
