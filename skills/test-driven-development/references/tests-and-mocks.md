# Tests and Mocks

Load this reference when writing or changing tests, adding a mock, or adding a helper that only tests call.

A test exists to catch a specific break. Two principles govern everything here:

```
1. Every test names the break it catches.
2. Every test exercises the real thing.
```

Strict TDD produces both naturally: a test written first and watched failing against real code has already proven it can fail, and it earns a mock only when the real dependency is slow or external.

## Name the break

Before writing the test body, answer: **what production change should make this test fail — and is that change a bug or a decision?** A test earns its place by catching a wrong branch, a missing side effect, a wrong argument, a boundary case, or a broken contract.

If you cannot name a production change, the test checks nothing. Redesign around observable behavior.

### Derive expectations independently

Use literals and hand-checked fixtures. Table-driven tests with literal `want` values are the preferred shape. An expectation computed by the code under test — or by its helpers — passes no matter what that code does.

```typescript
// BAD: the expected value is recomputed the way the code computes it
const items = [{ price: 10 }, { price: 5 }];
const expected = items.reduce((sum, i) => sum + i.price, 0);
expect(calculateTotal(items)).toBe(expected);

// GOOD: an independent, known literal
expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
```

The same failure with a builder: if `buildSearchQuery` computes both sides of the assertion, the assertion is always true. Assert the literal it should produce instead — `expect(buildSearchQuery({ tag: 'urgent' })).toBe('tag:"urgent"')`.

### No change detectors

If only intentional decisions can fail a test — a constant's value, exact message wording, private structure — the test fires on redesign and sleeps through bugs. Test the behavior that depends on the decision: not `expect(MAX_RETRIES).toBe(5)` but "a failing call is retried 5 times and the 6th attempt never happens."

### Behavior, not text

Asserting that a script, skill, or config contains an exact line proves only that the source is the source. Run scripts against controlled inputs and assert outputs, side effects, or exit codes. Documents that instruct agents are tested by the consuming agent's behavior (see `writing-for-agents`); prose for humans earns no test at all.

### Your code, not the framework

Test the contract your code makes at its boundaries: the route you register, the query you emit, the payload you produce. Upstream mechanics are their maintainers' tests to write — asserting that your router invokes a registered handler is the framework's test, not yours. When upstream behavior genuinely surprised you, write one narrow characterization test naming the assumption.

The same boundary applies inside your code: constructors, getters, constants, and trivial forwarding earn tests only when they validate, normalize, default, derive, enforce, or cause side effects. Otherwise assert the first consumer-visible result that depends on them.

### Gate function

```
BEFORE writing the test body:
  Name the production change that would make this test fail.

  Cannot name one            → redesign around observable behavior
  "The source text changed"  → run the artifact and assert its effects
  Only intentional decisions → change detector; test the behavior
                               that depends on the decision

  Confirm the expected value is derived without the code under test.
  IF it reuses the code's logic or helpers:
    Replace it with a literal or hand-checked fixture
```

## Exercise the real thing

### The mock earns no assertions

A mock assertion passes when the mock is present and fails when it is absent; it says nothing about the component. Assert the real component's behavior. If the mock is what you are checking, unmock it or delete the assertion.

```typescript
// GOOD: real behavior
expect(screen.getByRole('navigation')).toBeInTheDocument();

// BAD: mock existence
expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
```

### Mock at the right level

Learn every side effect of the real method before replacing it. Mock the slow or external operation and keep what the test depends on real. When unsure, run the test against the real implementation first and observe what actually needs to happen.

```typescript
// BAD: the mock swallows the config write that duplicate detection reads
vi.mock('ToolCatalog', () => ({
  discoverAndCacheTools: vi.fn().mockResolvedValue(undefined),
}));

// GOOD: mock only the slow server startup; the config write stays real
vi.mock('MCPServerManager');
```

### Make doubles specific

When arguments, call counts, or ordering are part of the contract, assert them — a fake that accepts anything verifies nothing. Give each branch (success, error, malformed) its own fixture or spy, so the wrong branch cannot satisfy the expectation.

### Mirror real data completely

Mock the complete structure as it exists in reality, with all documented fields, not just the ones your test reads. A partial mock fails silently when downstream code reads an omitted field: the test passes while integration breaks.

### Test-only code lives in utilities

Cleanup that only tests need belongs in a test utility, never as a `destroy()` on the production class. Ask: is this method called only from test files? Does this class own the resource's lifecycle? Wrong answers mean test utility.

### Prefer real components when setup balloons

When mock setup outgrows the test logic, mocks miss methods the real components have, or tests break when the mock changes, switch to an integration test with real components.

### Gate function

```
BEFORE adding a mock or test helper:
  List the real method's side effects; keep the ones the test depends on
  real — mock the slow/external level below them.

  Mock responses mirror the complete real structure.

  A method only tests call lives in test utilities, not production.

  About to assert on the mock itself?
    Unmock it or delete the assertion.
```

## Where to mock

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases, sometimes — prefer a real test database
- Time and randomness
- The file system, sometimes

Don't mock:

- Your own classes and modules
- Internal collaborators
- Anything you control

### Design for mockability

**Inject dependencies** instead of constructing them inside the function:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**Prefer SDK-style functions over a generic fetcher.** One specific function per external operation gives each mock one shape, removes conditional logic from test setup, and makes it obvious which endpoints a test exercises:

```typescript
// GOOD: each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

## Good and bad, side by side

**Test observable behavior through the interface.**

```typescript
// GOOD
test('user can checkout with valid cart', async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe('confirmed');
});

// BAD: tests an internal call
test('checkout calls paymentService.process', async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

**Verify through the interface, not a side channel.**

```typescript
// BAD: bypasses the interface to inspect storage
test('createUser saves to database', async () => {
  await createUser({ name: 'Alice' });
  const row = await db.query('SELECT * FROM users WHERE name = ?', ['Alice']);
  expect(row).toBeDefined();
});

// GOOD: verifies what a caller can observe
test('createUser makes user retrievable', async () => {
  const user = await createUser({ name: 'Alice' });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe('Alice');
});
```

A good test is integration-style, uses the public API, describes WHAT rather than HOW, makes one logical assertion, and survives an internal refactor. A test that mocks internal collaborators, tests private methods, asserts on call counts or order, bypasses the interface, or breaks on a behavior-preserving refactor is implementation-coupled.

## The mutation check

Before finishing, mentally mutate the production code. At least one test should fail for each realistic mutation:

- Wrong constant or argument
- Wrong branch handler
- Missing state change or side effect
- Empty or default return
- Missing validation for zero, empty, nil, unauthorized, or malformed input

A mutation nothing catches marks the behavior as unprotected — or the test as tautological.

## Warning signs

- Setup and assertion share the same object, guaranteeing equality
- The test can fail only through a panic, crash, or missing selector
- The test fails on every intentional change, never on accidental breakage
- Expected values are hidden behind loops, builders, or helpers
- The test greps source text, or asserts a removed symbol stays removed
- The test would still matter if only the framework remained
- The test exists for coverage, checking no side effect or outcome
- An assertion checks a `*-mock` test ID, or fails if you remove the mock
- A method is called only from test files
- Mock setup is more than half the test, or you cannot explain why the mock is needed
- Mocking "just to be safe"

## Quick reference

| When you... | Do |
|---|---|
| Write any test | Name the break it catches — a bug, not a decision |
| Build an expected value | Derive it by hand; never with the code under test |
| Test a script or document | Run it, or pressure-test its consumer; never grep its text |
| Reach for a dependency test | Test your boundary contract, not their documented mechanics |
| Want to assert on a mocked element | Test the real component, or unmock it |
| Are about to mock a method | Learn its side effects; mock the slow/external level |
| Build a mock response | Mirror the real structure completely |
| Need cleanup only tests use | Put it in test utilities |
| Watch mock setup balloon | Switch to an integration test with real components |
| Finish a test file | Run the mutation check |
