# Patterns

Pick a pattern because it serves a quality goal, never for its own sake. Patterns marked
**(OO)** assume objects and classes; the third column gives the dataflow counterpart where one
exists.

## Architectural patterns

| Pattern | Structure | Dataflow reading |
|---|---|---|
| Layered | Each layer uses only the one below. | Signal conditioning → control → supervision, wired one way. |
| Pipe-and-filter | Independent steps pass data along a chain. | The native form: blocks connected signal to signal. |
| Plug-in (microkernel) | A small core plus variants behind fixed contracts. | Replaceable blocks behind a fixed port contract. |
| Client-server | Clients request; one server answers. | Co-simulation master and FMUs. |
| Event-driven | Producers emit events; consumers react. | Triggered subsystems, `when` clauses, state machines. |

Overview: <https://www.geeksforgeeks.org/system-design/design-patterns-architecture/>.

## Design patterns (Gang of Four)

| Pattern | Group | Dataflow counterpart |
|---|---|---|
| Abstract Factory, Factory Method, Builder, Prototype, Singleton (OO) | Creational | A parameter record that configures a block; a model's single `inner` instance for Singleton |
| Adapter | Structural | A converter block between two connector types |
| Facade | Structural | A subsystem with a small port set hiding its internal wiring |
| Composite | Structural | Hierarchical subsystems that expose the same ports as a leaf block |
| Bridge, Decorator, Flyweight, Proxy (OO) | Structural | - |
| Strategy | Behavioral | A replaceable block with the same ports (`replaceable` / variant subsystem) |
| Template Method | Behavioral | A fixed init/step/terminate schedule whose steps blocks fill |
| Observer | Behavioral | A signal fanned out to several readers |
| State | Behavioral | A state machine block (StateGraph, Stateflow) |
| Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Visitor (OO) | Behavioral | - |

Source: Gamma, Helm, Johnson, Vlissides, *Design Patterns*, Addison-Wesley, 1994. Catalog:
<https://refactoring.guru/design-patterns/catalog>.
