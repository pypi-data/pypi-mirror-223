<img src="./voicebox.png" width="400px"></img>

## Voicebox - Pytorch (wip)

Implementation of <a href="https://arxiv.org/abs/2306.15687">Voicebox</a>, new SOTA Text-to-Speech model from MetaAI, in Pytorch. <a href="https://about.fb.com/news/2023/06/introducing-voicebox-ai-for-speech-generation/">Press release</a>

In this work, we will use rotary embeddings. The authors seem unaware that ALiBi cannot be straightforwardly used for bidirectional models.

## Appreciation

- <a href="https://stability.ai/">StabilityAI</a> for the generous sponsorship, as well as my other sponsors, for affording me the independence to open source artificial intelligence.

- <a href="https://github.com/b-chiang">Bryan Chiang</a> for the ongoing code review, sharing his expertise on TTS, and pointing me to <a href="https://github.com/atong01/conditional-flow-matching">an open sourced implementation</a> of conditional flow matching

## Install

```bash
$ pip install voicebox-pytorch
```

## Usage

```python
import torch
from voicebox_pytorch.voicebox_pytorch import (
    VoiceBox,
    ConditionalFlowMatcherWrapper
)

model = VoiceBox(
    dim = 512,
    num_phoneme_tokens = 256,
    depth = 2,
    dim_head = 64,
    heads = 16
)

cfm_wrapper = ConditionalFlowMatcherWrapper(
    voicebox = model
)

x = torch.randn(1, 1024, 512)
phonemes = torch.randint(0, 256, (1, 1024))
mask = torch.randint(0, 2, (1, 1024))

loss = cfm_wrapper(
    x,
    phoneme_ids = phonemes,
    cond = x,
    mask = mask
)

loss.backward()

# after much training above...

sampled = cfm_wrapper.sample(
    phoneme_ids = phonemes,
    cond = x,
    mask = mask
)
```

## Todo

- [x] read and internalize original flow matching paper
    - [x] basic loss
    - [ ] get neural ode working with torchdyn
- [ ] consider switching to adaptive rmsnorm for time conditioning
- [ ] integrate with either hifi-gan or soundstream / encodec
- [ ] basic trainer
- [ ] get basic mask generation logic with the p_drop of 0.2-0.3 for ICL

## Citations

```bibtex
@article{Le2023VoiceboxTM,
    title   = {Voicebox: Text-Guided Multilingual Universal Speech Generation at Scale},
    author  = {Matt Le and Apoorv Vyas and Bowen Shi and Brian Karrer and Leda Sari and Rashel Moritz and Mary Williamson and Vimal Manohar and Yossi Adi and Jay Mahadeokar and Wei-Ning Hsu},
    journal = {ArXiv},
    year    = {2023},
    volume  = {abs/2306.15687},
    url     = {https://api.semanticscholar.org/CorpusID:259275061}
}
```

```bibtex
@inproceedings{dao2022flashattention,
    title   = {Flash{A}ttention: Fast and Memory-Efficient Exact Attention with {IO}-Awareness},
    author  = {Dao, Tri and Fu, Daniel Y. and Ermon, Stefano and Rudra, Atri and R{\'e}, Christopher},
    booktitle = {Advances in Neural Information Processing Systems},
    year    = {2022}
}
```
