# Anti-patterns

A recurring practice that looks helpful and does more harm than good; a pattern applied in the
wrong context becomes one. Each has a refactored solution.

| Anti-pattern | What it is | OO sign | Dataflow sign | Refactored solution |
|---|---|---|---|---|
| The Blob | One module holds most behaviour and data. | A god class every other class calls | One "framework" model or setup script everything depends on | Split by responsibility behind small interfaces |
| Lava Flow | Dead code kept because nobody dares remove it. | Unused classes kept "for compatibility" | Unused legacy blocks and parameter formats | Delete it, with tests through the interface as the net |
| Golden Hammer | One favourite technique applied to every problem. | Inheritance hierarchies for every variation | Every module forced into the same structure | Choose per quality goal |
| Spaghetti Code | Unstructured control and data flow. | Tangled calls and shared mutable state | `Goto`/`From` tags, shared workspace variables, `inner`/`outer` reaching across subsystems | Route signals through ports |
| Analysis Paralysis | Analysis that delays every decision. | Specifying every class before code exists | Specifying every interface before any block exists | Decide at the seams, iterate behind them |

Source: Brown, Malveau, McCormick, Mowbray, *AntiPatterns*, Wiley, 1998. Overview:
<https://sourcemaking.com/antipatterns>. The Blob and Lava Flow are confirmed against a
secondary summary; the other three names are from general knowledge of the book.
