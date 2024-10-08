This folder contains code for downloading, cleaning, and organizing a corpus of
mathematical documents in LaTeX format.

See also:
* other tools for downloading bulk data from arXiv, e.g. https://github.com/armancohan/arxiv-tools
* [S2ORC: The Semantic Scholar Open Research Corpus](https://arxiv.org/pdf/1911.02782.pdf)
* [The Pile](https://www.gwern.net/Variables#data) free arXiv dataset

_Warning:_ Downloading arXiv content will result in
[charges](https://aws.amazon.com/s3/pricing/) to your AWS
account and unpacking many arXiv tar files takes a very long time.
Ensure you have sufficient storage space or there will be errors.

* set `MATHTEXT_NUM_TARS` (e.g. `export MATHTEXT_NUM_TARS=1000`) to the maximum
  number of arXiv tars to download (default is `2` (1GB))
* set `MATHTEXT_SKIP_PROJECTS` to a nonempty string to skip individual project
  sources (books, etc.)
* set `MATHTEXT_SKIP_SE` to a nonempty string to skip Stack Exchange sources

After setting desired variables, to get data run `./get.sh`.
It may take a long time, so running from tmux is a good idea.

_Output_: files in `./documents/`, metadata in `./metadata.pickle`,
list of arXiv tars downloaded in `./arxiv_log.json`

If you run `get.sh` again it will add to the dataset, downloading new
arXiv tars.

For Stack Exchange content, each output file is a question then an answer,
where the question starts with `<QUESTION>` and the answer starts with
`<ANSWER>`

arXiv files are selectively included based on contents, see
`clean_tex.py`

