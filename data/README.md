This folder contains code for downloading, cleaning, and organizing a corpus of
mathematical documents in LaTeX format.

see also:
* other tools for downloading bulk data from arXiv, e.g. https://github.com/armancohan/arxiv-tools
* [S2ORC: The Semantic Scholar Open Research Corpus](https://arxiv.org/pdf/1911.02782.pdf)

tested on _Ubuntu 18 and 20_

`install.sh` contains dependencies.
it is recommended to use a Python virtual environment

_warning_: downloading arXiv content will result in charges to your AWS
account and unpacking many arXiv tar files takes a very long time (multiple
days). processing stack exchange data involves reading multi-gigabyte files,
16GB+ RAM recommended. ensure you have sufficient storage space.

* set `export MATHTEXT_NUM_TARS=...` for number of arXiv tars to download (default is 2 (1GB))
* set `MATHTEXT_SKIP_PROJECTS` to a nonempty string to skip individual project sources (books, etc.)
* set `MATHTEXT_SKIP_SE` to a nonempty string to skip stack exchange sources

After setting variables, to get data run `./get.sh`.
It may take a long time, so running from tmux is a good idea.

_output_: files in `./documents/`, and `./index.json` contains metadata for each

For Stack Exchange content, each output file is a question then an answer,
where the question starts with `<QUESTION>` and the answer starts with
`<ANSWER>`

arXiv files are selectively included based on contents, see
`cleantex.good_or_none`

