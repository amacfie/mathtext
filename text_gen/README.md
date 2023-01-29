<!--
* size of pretrained model
* GPT-2 vs transformer xl
* optimizer
* learning rate
-->
<!--
encoding got to about half of 1.7GB train.txt with 24GB of RAM,
48GB was plenty.
for 10GB dataset peak memory during encoding was 29GB, took 3.5hrs.
training required same memory.
for 117M, we can have a batch size of 3 on T4.
-->

The following is a tutorial for using a text generation model with the corpus.

Addendum:
Work has been done since that has been much more successful, see e.g.
<https://github.com/amacfie/public_notes/wiki/Survey-on-computer-assisted-natural-language-problem-solving-in-the-formal-sciences>.

applications: generate inspiration/ideas for next steps in a proof

## Results

| Pretrained model  | Dataset (subset) size | Batch size | Accelerator | Learning rate | Running time | Sampling temperature | Output |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 355M  | 6GB  | 1 | GPU | default | a few days | 1 | Some coherence but practically useless |


## Model: GPT-2

We'll use GPT-2 although alternatives exist such as
[Transformer-XL](https://github.com/kimiyoung/transformer-xl) with a
character-level tokenizer (see
[this experiment](https://arxiv.org/abs/1912.01982)).

GPT-2 uses byte pair encoding which means it can generate text at the
character level

GPT-2 pretrained models smaller than "medium" (345M) are pretty bad for natural
language so we might not expect any better results from them for this task

We'll "fine-tune" a pretrained model, which basically means using the same
architecture and initializing parameters to the values in the model

some general notes on working with GPT-2:
https://medium.com/@NPCollapse/replicating-gpt2-1-5b-86454a7f26af

## Configuring VM

<!--If you're a researcher, see [TensorFlow Research Cloud](https://www.tensorflow.org/tfrc)
to apply for free TPU credits.
You may still want to experiment with a GPU first.-->

It's easiest to use Google's
[deep learning image](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning?_ga=2.41035681.2087968058.1597093079-761847582.1591646209).

When you get to the _New Deep Learning VM deployment_ page, make the
following selections.
Under _Framework_, choose _Intel(R) optimized Base (with Intel(R) MKL and
CUDA 10.0)_.
TensorFlow 1.15 doesn't seem to work with CUDA 10.1.
Select _Install NVIDIA GPU driver automatically on first startup_.
Finding the amount of RAM required takes experimentation. Watch `top`. Encoding
and training use the same amount.
Currently, the [Tesla T4](https://cloud.google.com/compute/gpus-pricing) is the
cheapest 16GB GPU.

## Moving data to VM

Unless `data/` is already on the VM, go to `data/` and run
```bash
# https://superuser.com/a/1337788
tar -c ./documents | pv -s $(du -sb ./documents | awk '{print $1}') > documents.tar
```
[Upload](https://cloud.google.com/storage/docs/gsutil_install)
`documents.tar` to Google Cloud Storage:
```bash
gsutil cp ./documents.tar gs://<your bucket>
```
On VM, run
```bash
gcloud init
```
log in with your Google account.
Then:
```bash
gsutil cp gs://<your bucket>/documents.tar .
sudo apt install pv
pv documents.tar | tar xf - -C .
rm documents.tar
```

## Preparing to train (GPU)

You can use `117M` or any of the other [available pretrained
models](https://github.com/openai/gpt-2/issues/209#issuecomment-554246634).
```bash
export MODEL_CODE=117M
```
We use `farrell236`'s fork of
https://github.com/nshepperd/gpt-2
due to [this issue](https://github.com/nshepperd/gpt-2/issues/33).
The Python scripts in this repository accept the `--help` flag if you want
to learn more about their options.
```bash
git clone https://github.com/farrell236/gpt-2.git
cd gpt-2
# TF v1.12 and v2 don't work
pip install tensorflow-gpu==1.15
pip install -r requirements.txt
echo "GPU is available:"
python -c 'import tensorflow as tf; tf.test.is_gpu_available()'
# we need `download_model.py` from the nshepperd repo because
# it has an updated URL
rm download_model.py
wget "https://raw.githubusercontent.com/nshepperd/gpt-2/a74da5d99abaaba920de8131d64da2862a8f213b/download_model.py"
python download_model.py $MODEL_CODE
PYTHONPATH=src ./encode.py --model_name $MODEL_CODE ../documents/ ./documents.npz
```

## Training

_Note: A notebook with training on Google Colab is [here](https://colab.research.google.com/drive/1jc1L04RTfEjscTPtI46vd0OpBJpzw5Od?usp=sharing)._

We are ready to train.
Since the following is a long-running command you may want to run it in tmux:
```bash
PYTHONPATH=src python train.py  --model_name $MODEL_CODE --dataset documents.npz --batch_size 3 --save_every 50 --sample_every 20 --sample_num 1 --sample_length 128 --val_every 100
```

This will keep running indefinitely. Stop it when you wish.

Note: Pick the largest batch size you can fit on your GPU;
some trial and error may be required.
Bigger models take more VRAM.


## Sampling

The folder `checkpoint/` contains our trained model parameters.
Assuming we use the parameters from step `9000`, we name this trained model
by running
```bash
mkdir models/mymodel
cp -t models/mymodel checkpoint/run1/model-9000.* checkpoint/run1/checkpoint
cp -t models/mymodel models/$MODEL_CODE/encoder.json models/$MODEL_CODE/hparams.json models/$MODEL_CODE/vocab.bpe
```
Note: this seems to only work if you use the latest checkpoint.

We can now generate samples
```bash
python ./src/interactive_conditional_samples.py --model_name mymodel
```

<!--
## TPU usage

See Shawn Presser's TPU version
* https://github.com/shawwn/gpt-2
* https://colab.research.google.com/drive/1BXry0kcm869-RVHHiY6NZmY9uBzbkf1Q

For TPUs "The rule of thumb is to use batches of 128 elements per
core (ex: batch size of 128*8=1024 for a TPU with 8 cores)."

create TPU node and VM in the same region, set `TPU_NAME` environment variable in VM, set "Cloud API access scopes" to 
"Allow full access to all Cloud APIs" in VM

use the `.npz` file generated with the GPU section. install the `requirements.txt` file from `farrell236` too.
the one in `shawwn` installs tensorflow 2 and is unnecessary unless you use the optimizer `ada`.
use `models` folder from the GPU section and install tensorflow(-gpu?) 1.15.
-->
