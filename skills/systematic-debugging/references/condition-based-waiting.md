# Condition-Based Waiting

Flaky tests often guess at timing with arbitrary delays. That creates race conditions where tests pass on a fast machine but fail under load or in CI.

**Core principle:** wait for the actual condition you care about, not a guess about how long it takes.

## When to use

- Tests have arbitrary delays (`setTimeout`, `sleep`, `time.sleep()`).
- Tests are flaky: they pass sometimes and fail under load.
- Tests time out when run in parallel.
- You are waiting for an async operation to complete.

**Don't use** when you are testing actual timing behavior (debounce, throttle intervals). If you do use an arbitrary timeout there, document why.

## Core pattern

```typescript
// BEFORE: guessing at timing
await new Promise(r => setTimeout(r, 50));
const result = getResult();
expect(result).toBeDefined();

// AFTER: waiting for the condition
await waitFor(() => getResult() !== undefined);
const result = getResult();
expect(result).toBeDefined();
```

## Quick patterns

| Scenario | Pattern |
|---|---|
| Wait for an event | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| Wait for state | `waitFor(() => machine.state === 'ready')` |
| Wait for a count | `waitFor(() => items.length >= 5)` |
| Wait for a file | `waitFor(() => fs.existsSync(path))` |
| Complex condition | `waitFor(() => obj.ready && obj.value > 10)` |

## Implementation

```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }

    await new Promise(r => setTimeout(r, 10)); // Poll every 10ms
  }
}
```

See [condition-based-waiting-example.ts](condition-based-waiting-example.ts) for a complete implementation with domain-specific helpers (`waitForEvent`, `waitForEventCount`, `waitForEventMatch`) from a real debugging session.

## Common mistakes

- **Polling too fast.** `setTimeout(check, 1)` wastes CPU. Poll every 10ms.
- **No timeout.** The loop runs forever if the condition is never met. Always include a timeout with a clear error.
- **Stale data.** Caching state before the loop keeps checking the old value. Call the getter inside the loop for fresh data.

## When an arbitrary timeout is correct

```typescript
// The tool ticks every 100ms, so 2 ticks are needed to verify partial output
await waitForEvent(manager, 'TOOL_STARTED'); // first: wait for the condition
await new Promise(r => setTimeout(r, 200));  // then: wait for timed behavior
// 200ms = 2 ticks at 100ms intervals — documented and justified
```

Requirements:

1. Wait for the triggering condition first.
2. Base the delay on known timing, not a guess.
3. Comment why the delay is needed.

## Real-world impact

One debugging session replaced arbitrary timeouts in 15 flaky tests across 3 files: pass rate went from 60% to 100%, execution time dropped 40%, and the race conditions disappeared.
