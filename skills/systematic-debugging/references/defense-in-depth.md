# Defense-in-Depth Validation

When you fix a bug caused by invalid data, adding validation in one place feels sufficient. But that single check can be bypassed by another code path, a refactor, or a mock.

**Core principle:** validate at every layer data passes through. Make the bug structurally impossible.

## Why multiple layers

Single validation: "We fixed the bug."
Multiple layers: "We made the bug impossible."

Different layers catch different cases:

- Entry validation catches most bugs.
- Business logic catches edge cases.
- Environment guards prevent context-specific dangers.
- Debug logging helps when the other layers fail.

## The four layers

### Layer 1: Entry point validation

Reject obviously invalid input at the API boundary.

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
  // ... proceed
}
```

### Layer 2: Business logic validation

Ensure the data makes sense for this operation.

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
  // ... proceed
}
```

### Layer 3: Environment guards

Prevent dangerous operations in specific contexts.

```typescript
async function gitInit(directory: string) {
  // In tests, refuse git init outside temp directories
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));

    if (!normalized.startsWith(tmpDir)) {
      throw new Error(
        `Refusing git init outside temp dir during tests: ${directory}`
      );
    }
  }
  // ... proceed
}
```

### Layer 4: Debug instrumentation

Capture context for forensics.

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  logger.debug('About to git init', {
    directory,
    cwd: process.cwd(),
    stack,
  });
  // ... proceed
}
```

## Applying the pattern

1. **Trace the data flow** — where does the bad value originate, and where is it used?
2. **Map every checkpoint** the data passes through.
3. **Add validation at each layer** — entry, business, environment, debug.
4. **Test each layer** — try to bypass layer 1 and verify layer 2 catches it.

## Example: empty projectDir

Bug: an empty `projectDir` made `git init` run in the source directory.

**Data flow:**

1. Test setup produced an empty string.
2. `Project.create(name, '')`
3. `WorkspaceManager.createWorkspace('')`
4. `git init` ran in `process.cwd()`

**Four layers added:**

- Layer 1: `Project.create()` validates not empty, exists, and is a directory.
- Layer 2: `WorkspaceManager` validates `projectDir` is not empty.
- Layer 3: `WorktreeManager` refuses `git init` outside the temp directory during tests.
- Layer 4: stack trace logging before `git init`.

All four were necessary. During testing, each layer caught bugs the others missed: different code paths bypassed entry validation, mocks bypassed the business-logic check, platform edge cases needed an environment guard, and debug logging identified structural misuse.

## Key insight

Don't stop at one validation point. Add checks at every layer the bad value can pass through.
