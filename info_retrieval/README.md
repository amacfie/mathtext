Here we discuss some ways to search a LaTeX corpus.

see also:
* [D. Pineau - Math-aware search engines](https://www.groundai.com/project/math-aware-search-engines-physics-applications-and-overview/1)
* https://search.mathweb.org/
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
* regular expressions
* structural search
* semantic analysis

Regular expressions and structural search allow for backreferences which let us
search for, say, `something^2 + something`, matching `x^2 + x` and `y^2 + y`
but not `x^2 + y`.
(Technically _regular_ expressions can't have unbounded-length backreferences
but they're in the PCRE specification.)

## Exact string search

I.e. query syntax that may allow e.g. wildcards but not full regular expressions

Apache Lucene is the standard for big data

## Regular expressions

Google Code Search ([open sourced](https://github.com/google/codesearch))
uses a trigram index to automatically accelerate regex search.
It works well, although it doesn't support backreferences
(and neither do Zoekt or Sourcegraph).
However, it can be used as the first step in a two-step search along with PCRE
search such as [Ag](https://github.com/ggreer/the_silver_searcher):
```bash
temp_file=$(mktemp)
csearch -l <re2_regex> > $temp_file
ag <pcre_regex> $(cat ${temp_file})
```
where `<re2_regex>` uses [RE2 syntax](https://github.com/google/re2/wiki/Syntax)
and matches a relatively small superset of the desired documents.
In a bash script you may want to use `set -e` since `csearch` will fail
e.g. if the regex is invalid.

You'll likely want to use single quotes around regexes on the command line to
disable shell replacements, e.g. `csearch '\\sqrt{[a-z]}'`

A tool like <https://regex101.com/> can be helpful


## Structural search

[Comby](https://comby.dev/docs/overview) supports LaTeX

If structural search is slow we may want to do a two-step search as above,
i.e. only using structural search to refine results returned by a fast but
overly-inclusive search.

