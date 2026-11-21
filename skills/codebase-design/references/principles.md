# Programming principles

Short rules for code that is easy to understand and change. Most are forms of information
hiding ([Parnas, 1972](https://dl.acm.org/doi/10.1145/361598.361623)): each module hides a
decision likely to change behind an interface that reveals as little as possible.

| Principle | Rule | Dataflow reading (Modelica, Simulink) |
|---|---|---|
| [Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) | Split a problem into parts understood and changed on their own. | Plant, controller, solver settings and logging are separate blocks. |
| [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) | Every piece of knowledge has one authoritative representation: parameters, interfaces and build steps too. | Constants and connector or bus definitions live in one place; a bus change is one edit. |
| [KISS](https://en.wikipedia.org/wiki/KISS_principle) | Prefer the simplest design that solves the problem. | Small port sets with documented units; no generic plug-in machinery without a need. |
| [YAGNI](https://martinfowler.com/bliki/Yagni.html) | Build what is needed now. | Add a variant when a second project needs it. |
| SRP ([SOLID](https://en.wikipedia.org/wiki/SOLID)) | Keep together what changes for the same reason. | One subsystem per physical or control responsibility. |
| [OCP](https://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html) | Open for extension, closed for modification. | A new controller is a new block behind an existing port contract, not an edit of a working one. |
| [LSP](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf) | An implementation must not surprise code that uses its interface. | Two plant models with the same ports are swappable, with the same units and sign conventions. |
| ISP | Keep interfaces small so users don't depend on what they don't need. | A sensor block does not receive a bus carrying actuator commands. |
| DIP | Depend on abstractions, not on low-level details. | Blocks depend on the shared connector definitions, not on each other. |
| [Law of Demeter](https://en.wikipedia.org/wiki/Law_of_Demeter) | Talk only to your direct neighbours. | A model connects subsystems through ports and never reads another block's parameters or internals. |
| [Rule of Three](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)) | Tolerate a second copy; extract on the third. | Extract a shared block when a third model needs it. |

The principles pull against each other:

- **YAGNI vs. OCP/DIP**: design the interface at a seam for change; defer the features behind it.
- **DRY vs. premature abstraction**: code that only looks alike may be different knowledge. The
  Rule of Three settles it.

Overview: <https://geeksprogramming.com/key-principles-in-software-and-acronyms/>. SOLID in
practice: <https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html>.
