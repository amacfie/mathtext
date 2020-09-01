computation with latex math corpus

original motivation: enter math problem then generate "solutions" which may
give some inspiration. see also
* https://mathdeck.cs.rit.edu/
* https://www.springer.com/societies+&+publishing+partners/society+&+partner+zone?SGWID=0-173202-6-951123-0


# Data sources

exclude .git, .hg folders (i.e. hidden folders)

to transfer, use multi-part 7z without compression

# Information retrieval

applications:
* literature review, except symbol-based rather than English-based (which
  Google does based on PDFs), e.g. seeing what has been done with a given
  expression
  * surveying what's known and unknown on a subject
  * locating complete solutions to problems
  * generating ideas/inspiration
* subscribe to alerts when a new paper matches a query

e.g. regex search, something w/ latex parsing?

since there are many small documents, they can be processed in parallel,
each worker need only have one document open at a time for low memory usage

allow for certain subexpression substitution e.g. x^2 + x matches y^2 + y. not
regex although common syntax supports it (backreferences) although if we bound
the length of the subexpression it's regex

# Conditional text generation

applications: generate inspiration/ideas for next steps in a proof

## Deep learning infrastructure

dataset -> GC Storage

TPU (TFRC 1 month free)
practice with GPU first

GC image https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning?_ga=2.41035681.2087968058.1597093079-761847582.1591646209
T4 https://cloud.google.com/compute/gpus-pricing

## Tokens

~~Character-level, ~~byte bair~~, or LaTeX~~

GPT-2's "byte pair encoding" means it can produce arbitrary
sequences of characters, like character-level generation
https://www.gwern.net/GPT-2#training-gpt-2-117m-to-generate-poetry
other HF models are mostly word-level https://github.com/huggingface/transformers/issues/4090

character-level is hard to find in pretrained models

### LaTeX

pip3 install texsoup
```python
from TexSoup.category import categorize
from TexSoup.tokens import tokenize
list(tokenize(categorize('\\frac{a}{b}')))
['\\', 'frac', '{', 'a', '}', '{', 'b', '}']
```

more trouble than it's worth, considers i+1 and f(x) as one token

## Model

of models in huggingface collection, GPT-2 seems uniquely appropriate

GPT-2 pretrained models smaller than medium are pretty bad for natural language

generally fine-tuning doesn't change the number of parameters by much

"pick the largest batch size you can fit on your GPU"
for TPUs "The rule of thumb is to use batches of 128 elements per
core (ex: batch size of 128*8=1024 for a TPU with 8 cores)."
some trial and error may be required https://stackoverflow.com/questions/45132809/how-to-select-batch-size-automatically-to-fit-gpu

general notes https://medium.com/@NPCollapse/replicating-gpt2-1-5b-86454a7f26af

huggingface sucks. by building a general framework they actually make it
more difficult to work with any one model

### nshepperd implementation

https://github.com/nshepperd/gpt-2

encode data in batches to reduce RAM https://github.com/nshepperd/gpt-2/issues/43

Shawn Presser's TPU version
  https://github.com/shawwn/gpt-2
  https://colab.research.google.com/drive/1BXry0kcm869-RVHHiY6NZmY9uBzbkf1Q

end-of-sequence token not handled within files or between files
  https://github.com/nshepperd/gpt-2/issues/33
  farrell236's code does between-file handling, extend to get within-file

naming your model https://medium.com/@ngwaifoong92/beginners-guide-to-retrain-gpt-2-117m-to-generate-custom-text-content-8bb5363d8b7f#3157

