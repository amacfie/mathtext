Here we discuss some ways to search a LaTeX corpus.

See also:
* [D. Pineau - Math-aware search engines](https://www.groundai.com/project/math-aware-search-engines-physics-applications-and-overview/1)
* https://search.mathweb.org/
* https://mathdeck.cs.rit.edu/
* https://www.springer.com/societies+&+publishing+partners/society+&+partner+zone?SGWID=0-173202-6-951123-0

Applications:
* literature review, except symbol-based rather than English-based (which
  Google Search does based on PDFs), e.g. seeing what has been done with a
  given expression
  * surveying what's known and unknown on a subject
  * locating complete solutions to problems
  * generating ideas/inspiration
* subscribe to alerts when a new paper matches a query

Four levels:
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
  <summary>Installing Google Code Search on Ubuntu</summary>

  ```bash
  sudo apt install golang
  export PATH=$PATH:/usr/local/go/bin
  export PATH=$PATH:$HOME/go/bin
  go get github.com/junkblocker/codesearch/cmd/...
  go install github.com/junkblocker/codesearch/cmd/cindex
  go install github.com/junkblocker/codesearch/cmd/csearch
  ```
</details>

[Google Code Search](https://github.com/junkblocker/codesearch/) (GCS)
is open-source software that uses a trigram index to automatically accelerate
regex search.
It doesn't support backreferences;
however, it can be used as the first step in a two-step search along with PCRE
search such as ripgrep (on Ubuntu install from
[here](https://github.com/BurntSushi/ripgrep/releases) to get
[PCRE2](https://www.pcre.org/current/doc/html/pcre2syntax.html) support) e.g.
```bash
temp_file=$(mktemp)
# find documents that match <re2_regex> according to GCS
csearch -l <re2_regex> > ${temp_file}
# among those documents, find the ones that match <pcre2_regex> according to
# ripgrep
rg --multiline --pcre2 <pcre2_regex> $(cat ${temp_file})
```
where `<re2_regex>` uses [RE2 syntax](https://github.com/google/re2/wiki/Syntax)
and ideally matches some small superset of the desired documents.

You'll likely want to use single quotes around regexes on the command line to
disable shell replacements, e.g. `csearch '\\sqrt{[a-z]}'`

A tool like <https://regex101.com/> can be helpful

Some drawbacks:
* GCS can only deal with indexes up to 4GB which translates to about 20GB of
  data.
* Running `cindex` (but not `csearch`) may have high RAM requirements. If the
  index is 1GB then RAM usage will be 2-4GB.
  <!-- even in incremental indexing -->
* GCS does not support searching across multiple lines and it ignores long
  lines by default.

The file `./index.sh` creates an index by using GCS internally
([junkblocker's fork](https://github.com/junkblocker/codesearch/)) but it overcomes
the caveats mentioned above.
The file `./search.sh` is a command line interface
that uses the index created by `./index.sh`.

Zoekt and Sourcegraph are alternatives to GCS but don't support
backreferences either.
Zoekt is notably slower and uses a much larger index but supports multiline
search.
Postgres supports fast regex search with pg_trgm.


## Structural search

[Comby](https://comby.dev/docs/overview) supports LaTeX

If structural search is slow we may want to do a two-step search as above,
i.e. using structural search to refine results returned by a fast but
somewhat overly-inclusive search.


## Semantic analysis

Chroma is a vector database for semantic search.
The file `./chroma_index.py` creates an index from the corpus, and the file
`./chroma_search.py` is a demo for doing queries.
Its default text model was apparently trained on the Stack Exchange sites so
should know LaTeX math.

Postgres together with `pgvector` can also be used for semantic search. The
documents and search query must be converted to embeddings beforehand. One way
to do so is locally through Chroma:
```python
from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()

embeddings = default_ef(["foo", "bar"])
# embeddings is now [[0.05035809800028801, 0.0626462921500206, -0.061827320605516434...], [...]]
```
Another way is the OpenAI API:
<https://platform.openai.com/docs/guides/embeddings>

