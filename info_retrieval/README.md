Here we discuss some ways to search a LaTeX corpus including the provided
`./regex.py` script.

see also:
* https://search.mathweb.org/
* [D. Pineau - Math-aware search engines](https://www.groundai.com/project/math-aware-search-engines-physics-applications-and-overview/1)
* https://mathdeck.cs.rit.edu/
* https://www.springer.com/societies+&+publishing+partners/society+&+partner+zone?SGWID=0-173202-6-951123-0

applications:
* literature review, except symbol-based rather than English-based (which
  Google does based on PDFs), e.g. seeing what has been done with a given
  expression
  * surveying what's known and unknown on a subject
  * locating complete solutions to problems
  * generating ideas/inspiration
* subscribe to alerts when a new paper matches a query

four levels:
* exact string search
  * may allow e.g. wildcards but not full regular expression syntax
* regular expressions
* structural search
* semantic analysis

Regular expressions and structural search allow for backreferences which let us
search for, say, `something^2 + something`, matching `x^2 + x` and `y^2 + y`
but not `x^2 + y`.
(Technically _regular_ expressions can't have unbounded-length backreferences
but they're in the PCRE specification.)

Exact string search, e.g. with Apache Lucene, is fast but inflexible.
It can be used in a two-step search:
First use exact search to get a relatively small superset of the desired
results, then use slower methods like regex or structural search on that set.

## Regular expressions

`./regex.py <regex>`

you'll likely want to use single quotes around the regex to disable shell
replacements, e.g. `./regex.py '\\sqrt{[a-z]}'`

set `MATHTEXT_NUM_WORKERS`, e.g. run `export MATHTEXT_NUM_WORKERS=2`, to
modify the number of processes used (default is number of cores)

a tool like https://regex101.com/ can be helpful

Google Code Search ([open sourced](https://github.com/google/codesearch))
uses an index to automatically accelerate regex search, obviating the two-step
search process mentioned above.
It works well, although it doesn't support backreferences
(and neither do Zoekt or Sourcegraph).


## Structural search

[Comby](https://comby.dev/docs/overview) supports LaTeX

