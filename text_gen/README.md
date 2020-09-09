<!--
encoding got to about half of 1.7GB train.txt with 24GB of RAM,
48GB was plenty.
for 10GB dataset peak memory during encoding was 29GB, took 3.5hrs.
training required same memory.
for 117M, we can have a batch size of 3 on T4.
-->

The following is a tutorial for using a text generation model with the corpus.

applications: generate inspiration/ideas for next steps in a proof

## Model: GPT-2

Of models currently in huggingface collection, GPT-2 seems uniquely
appropriate.
(However huggingface is more difficult to use than a specialized script.)

GPT-2 uses byte pair encoding which means it can generate text at the
character level

GPT-2 pretrained models smaller than "medium" are pretty bad for natural
language

We'll "fine-tune" a pretrained model, which basically means using the same
architecture and initializing parameters to the values in the model

general notes:
https://medium.com/@NPCollapse/replicating-gpt2-1-5b-86454a7f26af

## Configuring VM

If you're a researcher, see [TensorFlow Research Cloud](https://www.tensorflow.org/tfrc)
to apply for free TPU credits.
You may want to experiment with a GPU first.

It's easiest to use Google's
[deep learning image](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning?_ga=2.41035681.2087968058.1597093079-761847582.1591646209).

Under _Framework_, choose _Intel(R) optimized Base (with Intel(R) MKL and
CUDA 10.0)_.
TensorFlow 1.15 doesn't seem to work with CUDA 10.1.
Select _Install NVIDIA GPU driver automatically on first startup_.
Finding the amount of RAM required takes experimentation. Watch `top`. Encoding
and training use the same amount.
Currently, the [T4 GPU](https://cloud.google.com/compute/gpus-pricing) is the
cheapest 16GB option.

## Moving data to VM

Unless `data/` is already on the VM, go to `data/` and run
```bash
# https://superuser.com/a/1337788
tar -c ./documents | pv -s $(du -sb ./documents | awk '{print $1}') > documents.tar
```
Upload `documents.tar` to Google Cloud Storage:
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
We use `farrell236`'s fork of 
https://github.com/nshepperd/gpt-2
due to [this issue](https://github.com/nshepperd/gpt-2/issues/33).

```bash
git clone https://github.com/farrell236/gpt-2.git
cd gpt-2
# TF v1.12 and v2 don't work
pip install tensorflow-gpu==1.15
pip install -r requirements.txt
echo "GPU is available:"
python -c 'import tensorflow as tf; tf.test.is_gpu_available()'
python download_model.py 117M
PYTHONPATH=src ./encode.py ../documents/ ./documents.npz
```

## Training

"pick the largest batch size you can fit on your GPU".
some trial and error may be required https://stackoverflow.com/questions/45132809/how-to-select-batch-size-automatically-to-fit-gpu

since the following is a long-running command you may want to run it in tmux:
```bash
PYTHONPATH=src python train.py  --model_name 117M --dataset documents.npz --batch_size 3 --save_every 50 --sample_every 20 --sample_num 1 --sample_length 128 --val_every 100
```

this will keep running indefinitely. stop it when you wish.


## Sampling

The folders in `checkpoint/` contain the trained model parameters.
Assuming we use the model from step `9000` of our first run, do
```bash
mkdir models/mymodel
cp -t models/mymodel checkpoint/run1/model-9000.* checkpoint/run1/checkpoint
cp -t models/mymodel models/117M/encoder.json models/117M/hparams.json models/117M/vocab.bpe
```

We can now generate samples
```bash
python ./src/interactive_conditional_samples.py --model_name mymodel
```
Run
```bash
python ./src/interactive_conditional_samples.py --help
```
to learn about extra parameters for this script.

## TPU usage

Shawn Presser's TPU version
* https://github.com/shawwn/gpt-2
* https://colab.research.google.com/drive/1BXry0kcm869-RVHHiY6NZmY9uBzbkf1Q

for TPUs "The rule of thumb is to use batches of 128 elements per
core (ex: batch size of 128*8=1024 for a TPU with 8 cores)."

