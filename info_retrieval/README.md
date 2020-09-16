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

<details>
  <summary>Installing Zoekt on Ubuntu</summary>

  ```bash
  sudo apt install golang
  export PATH=$PATH:/usr/local/go/bin
  export PATH=$PATH:$HOME/go/bin
  go get github.com/google/zoekt/...
  go install github.com/google/zoekt/cmd/zoekt-index
  go install github.com/google/zoekt/cmd/zoekt
  ```
</details>

Google Code Search ([open sourced](https://github.com/google/codesearch))
uses a trigram index to automatically accelerate regex search.
Zoekt is very similar but more actively maintained and has improvements such
as multiline search.
Create a Zoekt index as follows:
```bash
cd data/
zoekt-index documents
```
Zoekt does not support backreferences (neither does Google Code Search);
however, it can be used as the first step in a two-step search along with
PCRE search such as ripgrep (on Ubuntu install from
[here](https://github.com/BurntSushi/ripgrep/releases) to get
[PCRE2](https://www.pcre.org/current/doc/html/pcre2syntax.html) support):
```bash
cd documents/
temp_file=$(mktemp)
zoekt -index_dir ../ -l <query> > ${temp_file}
if [[ -s ${temp_file} ]]; then
  xargs -d '\n' -a ${temp_file} rg --multiline --pcre2 <pcre2_regex>
fi
rm ${temp_file}
```
where `<query>` is some
[Zoekt](https://github.com/google/zoekt/blob/master/web/templates.go)
[query](https://cs.bazel.build/)
(regex search follows [golang regex syntax](https://golang.org/pkg/regexp/))
that matches a relatively small superset of the desired documents.
Note that `zoekt` or `rg` can fail e.g. if their argument is an invalid
regex.

You'll likely want to use single quotes around regexes on the command line to
disable shell replacements, e.g. `zoekt '\\sqrt{[a-z]}'`

A tool like <https://regex101.com/> can be helpful


## Structural search

[Comby](https://comby.dev/docs/overview) supports LaTeX

If structural search is slow we may want to do a two-step search as above,
i.e. using structural search to refine results returned by a fast but
somewhat overly-inclusive search.

