# Root Cause Tracing

Bugs often manifest deep in the call stack: `git init` in the wrong directory, a file created in the wrong location, a database opened with the wrong path. The instinct is to fix where the error appears. That treats a symptom.

**Core principle:** trace backward through the call chain until you find the original trigger, then fix at the source.

## When to use

- The error happens deep in execution, not at the entry point.
- The stack trace shows a long call chain.
- It is unclear where the invalid data originated.
- You need to find which test or code path triggers the problem.

## The tracing process

### 1. Observe the symptom

```
Error: git init failed in ~/project/packages/core
```

### 2. Find the immediate cause

What code directly causes this?

```typescript
await execFileAsync('git', ['init'], { cwd: projectDir });
```

### 3. Ask what called this

```typescript
WorktreeManager.createSessionWorktree(projectDir, sessionId)
  → called by Session.initializeWorkspace()
  → called by Session.create()
  → called by test at Project.create()
```

### 4. Keep tracing up

What value was passed?

- `projectDir = ''` (empty string)
- An empty string as `cwd` resolves to `process.cwd()`
- That is the source code directory

### 5. Find the original trigger

Where did the empty string come from?

```typescript
const context = setupCoreTest(); // Returns { tempDir: '' }
Project.create('name', context.tempDir); // Accessed before beforeEach!
```

The root cause is top-level variable initialization reading a value before the fixture populated it. The fix belongs there — for example, make `tempDir` a getter that throws when accessed too early — not at the `git init` call.

## Adding stack traces

When you cannot trace manually, add instrumentation:

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  console.error('DEBUG git init:', {
    directory,
    cwd: process.cwd(),
    nodeEnv: process.env.NODE_ENV,
    stack,
  });

  await execFileAsync('git', ['init'], { cwd: directory });
}
```

Run and capture the tag:

```bash
npm test 2>&1 | grep 'DEBUG git init'
```

Analyze the stack traces for test file names, the line that triggered the call, and the pattern — same test every time? same parameter?

**Use `console.error()` in tests.** A logger may be suppressed by the test runner.

## Finding which test causes pollution

If state appears during a test run but you don't know which test creates it, bisect with [../scripts/find-polluter.sh](../scripts/find-polluter.sh):

```bash
bash ../scripts/find-polluter.sh '.git' 'src/**/*.test.ts'
```

It runs tests one by one and stops at the first polluter. See the script header for options.

## Real example: empty projectDir

**Symptom:** `.git` created in `packages/core/`, the source directory.

**Trace chain:**

1. `git init` runs in `process.cwd()` because the cwd parameter was empty.
2. `WorktreeManager` was called with an empty `projectDir`.
3. `Session.create()` passed the empty string through.
4. The test accessed `context.tempDir` before `beforeEach`.
5. `setupCoreTest()` returns `{ tempDir: '' }` initially.

**Root cause:** top-level variable initialization accessing an empty value.

**Fix:** make `tempDir` a getter that throws if accessed before `beforeEach`.

**Then add defense-in-depth:** validate the directory at the entry point, validate it again in the workspace manager, refuse `git init` outside the temp directory during tests, and log a stack trace before `git init`. See [defense-in-depth.md](defense-in-depth.md).

## Key principle

Found the immediate cause? Ask whether you can trace one level up. If yes, keep tracing. If you reach the source, fix there. If the trace dead-ends, never settle for fixing only where the error appears.

Then add validation at each layer so the bug becomes impossible, not merely absent on the path you tested.

## Stack trace tips

- **In tests:** use `console.error()`, not a logger that may be suppressed.
- **Before the operation:** log before the dangerous operation, not after it fails.
- **Include context:** directory, cwd, environment variables, timestamps.
- **Capture the chain:** `new Error().stack` shows the full call chain.
