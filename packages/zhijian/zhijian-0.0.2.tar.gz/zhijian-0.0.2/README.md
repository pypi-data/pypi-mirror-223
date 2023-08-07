<div align="center">
  <a href="http://zhijian.readthedocs.io"><img width="450px" height="auto" src="https://github.com/zhangyikaii/LAMDA-ZhiJian/raw/main/assests/logo.png?raw=true"></a>
</div>

&nbsp;

<div align="center">
    <img src="https://img.shields.io/badge/License-MIT-<COLOR>.svg?style=for-the-badge" alt="Generic badge", height="21">
    <img src="https://img.shields.io/github/actions/workflow/status/zhangyikaii/LAMDA-ZhiJian/tests.yml?branch=main&style=for-the-badge" alt="GitHub Workflow Status (branch)", height="21">
    <img src="https://img.shields.io/readthedocs/smp?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Read the Docs", height="21">
    <br>
    <img src="https://img.shields.io/pypi/v/ZhiJian?color=blue&style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI", height="21">
    <img src="https://img.shields.io/pypi/dm/ZhiJian?style=for-the-badge&color=blue" alt="PyPI - Downloads", height="21">
    <br>
    <img src="https://img.shields.io/badge/PYTORCH-1.4+-red?style=for-the-badge&logo=pytorch" alt="PyTorch - Version", height="21">
    <img src="https://img.shields.io/badge/PYTHON-3.7+-red?style=for-the-badge&logo=python&logoColor=white" alt="Python - Version", height="21">
</div>
<h4 align="center">
    <p>
        A PyTorch-based Toolbox for Reusing Pre-trained Models
    <p>
    <p>
        <b>English</b> |
        <a href="https://github.com/baichuan-inc/baichuan-7B/blob/main/README_CN.md">中文</a>
    <p>
</h4>


**ZhiJian** ([**执简**驭繁](https://baike.baidu.com/item/%E6%89%A7%E7%AE%80%E9%A9%AD%E7%B9%81)) is a *comprehensive* and *user-friendly* `PyTorch`-based **toolbox** for leveraging **foundation pre-trained models** and their **fine-tuned counterparts** to *extract* knowledge and *expedite* learning in real-world tasks, *i.e.*, **serving the Model Reuse tasks**.

**The rapid progress** in deep learning has led to the emergence of **numerous open-source Pre-Trained Models (PTMs)** on platforms like PyTorch, TensorFlow, and HuggingFace Transformers. Leveraging these PTMs for specific tasks empowers them to handle objectives effectively, creating valuable resources for the machine-learning community. **Reusing PTMs is vital in enhancing target models' capabilities and efficiency**, achieved through adapting the architecture, customizing learning on target data, or devising optimized inference strategies to leverage PTM knowledge.

![overview](https://github.com/zhangyikaii/LAMDA-ZhiJian/raw/main/assests/overview.png?raw=true)

🔥 **To facilitate a holistic consideration of various model reuse strategies**, ZhiJian categorizes model reuse methods into *three* sequential modules: **Architect**, **Tuner**, and **Merger**, aligning with the stages of **model preparation**, **model learning**, and **model inference** on the target task, respectively. **The provided interface methods include**:

<details>
<summary style="margin-left: 2px;"><b>A</b>rchitect Module [<em>Click to Expand</em>]<p style="margin-left: 12px;">The Architect module involves <b>modifying the pre-trained model to fit the target task</b>, and reusing certain parts of the pre-trained model while introducing new learnable parameters with specialized structures.</p></summary>
  <details>
  <summary style="margin-left: 12px;"><strong>LoRA</strong>, <em>LoRA: Low-Rank Adaptation of Large Language Models.</em> In: ICLR'22. <a href="https://arxiv.org/pdf/2106.09685.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Adapter</strong>, <em>Parameter-Efficient Transfer Learning for NLP.</em> In: ICML'19. <a href="https://arxiv.org/pdf/1902.00751.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Diff Pruning</strong>, <em>Parameter-Efficient Transfer Learning with Diff Pruning.</em> In: ACL'21. <a href="https://arxiv.org/pdf/2012.07463.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Visual Prompt Tuning / Prefix</strong>, <em>Visual Prompt Tuning.</em> In: ECCV'22. <a href="https://arxiv.org/pdf/2203.12119.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Convpass</strong>, <em>Convolutional Bypasses Are Better Vision Transformer Adapters.</em> In: Tech Report 07-2022. <a href="https://arxiv.org/pdf/2207.07039.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Scaling &amp; Shifting</strong>, <em>Scaling &amp; Shifting Your Features: A New Baseline for Efficient Model Tuning.</em> In: NeurIPS'22. <a href="https://arxiv.org/pdf/2210.08823.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>AdaptFormer</strong>, <em>AdaptFormer: Adapting Vision Transformers for Scalable Visual Recognition.</em> In: NeurIPS'22. <a href="https://arxiv.org/pdf/2205.13535.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Fact-Tuning</strong>, <em>FacT: Factor-Tuning for Lightweight Adaptation on Vision Transformer.</em> In: AAAI'23. <a href="https://arxiv.org/pdf/2212.03145.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>
  
  <details>
    <summary style="margin-left: 12px;"><strong>VQT</strong>, <em>Visual Query Tuning: Towards Effective Usage of Intermediate Representations for Parameter and Memory Efficient Transfer Learning.</em> In: CVPR'23. <a href="https://arxiv.org/pdf/2212.03220.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
    <div style="margin-left: 30px;">
      <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
    </div>
  </details>
</details>

<details>
<summary style="margin-left: 2px;"><b>T</b>uner Module [<em>Click to Expand</em>]<p style="margin-left: 12px;">The Tuner module focuses on <b>training the target model with guidance from pre-trained model knowledge</b> to expedite the optimization process, <em>e.g.</em>, via adjusting objectives, optimizers, or regularizers.</p></summary>
  <details>
  <summary style="margin-left: 12px;"><strong>Linear Probing</strong>, <em>Parameter-Efficient Transfer Learning for NLP.</em> In: ICML'19. <a href="https://arxiv.org/pdf/1902.00751.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Partial-k</strong>, <em>How transferable are features in deep neural networks?</em> In: NeurIPS'14. <a href="https://arxiv.org/pdf/1411.1792.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Nearest Class Mean</strong>, <em>Generalizing to new classes at near-zero cost.</em> In: TPAMI'13. <a href="https://ieeexplore.ieee.org/document/6517188">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>SimpleShot</strong>, <em>SimpleShot: Revisiting Nearest-Neighbor Classification for Few-Shot Learning.</em> In: CVPR'19. <a href="https://arxiv.org/pdf/1911.04623.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>BitFit</strong>, <em>BitFit: Simple Parameter-efficient Fine-tuning for Transformer-based Masked Language-models.</em> In: ACL'22. <a href="https://arxiv.org/pdf/2106.10199.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>Head2Toe</strong>, <em>Head2Toe: Utilizing Intermediate Representations for Better Transfer Learning.</em> In: ICML'22. <a href="https://arxiv.org/pdf/2201.03529.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>
  <details>
  <summary style="margin-left: 12px;"><strong>Vanilla Knowledge Distillation / LwF</strong>, <em>Learning without Memorizing.</em> In: CVPR'19. <a href="https://arxiv.org/pdf/1811.08051.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>FitNet</strong>, <em>FitNets: Hints for Thin Deep Nets.</em> In: ICLR'15. <a href="https://arxiv.org/pdf/1412.6550.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>FSP</strong>, <em>A Gift from Knowledge Distillation: Fast Optimization, Network Minimization and Transfer Learning.</em> In: CVPR'17. <a href="https://openaccess.thecvf.com/content_cvpr_2017/papers/Yim_A_Gift_From_CVPR_2017_paper.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>NST</strong>, <em>Like What You Like: Knowledge Distill via Neuron Selectivity Transfer.</em> In: CVPR'17. <a href="https://arxiv.org/pdf/1707.01219.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>RKD</strong>, <em>Relational Knowledge Distillation.</em> In: CVPR'19. <a href="https://arxiv.org/pdf/1412.6550.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>SPKD</strong>, <em>Similarity-Preserving Knowledge Distillation.</em> In: CVPR'19. <a href="https://arxiv.org/pdf/1907.09682.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>CRD</strong>, <em>Contrastive Representation Distillation.</em> In: ICLR'20. <a href="https://arxiv.org/pdf/1910.10699.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>REFILLED</strong>, <em>Distilling Cross-Task Knowledge via Relationship Matching.</em> In: CVPR'20. <a href="http://www.lamda.nju.edu.cn/lus/files/CVPR20_ReFilled.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>
  <details>
  <summary style="margin-left: 12px;"><strong>Vanilla Knowledge Distillation / LwF</strong>, <em>Learning without Memorizing.</em> In: CVPR'19. <a href="https://arxiv.org/pdf/1811.08051.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>FitNet</strong>, <em>FitNets: Hints for Thin Deep Nets.</em> In: ICLR'15. <a href="https://arxiv.org/pdf/1412.6550.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>FSP</strong>, <em>A Gift from Knowledge Distillation: Fast Optimization, Network Minimization and Transfer Learning.</em> In: CVPR'17. <a href="https://openaccess.thecvf.com/content_cvpr_2017/papers/Yim_A_Gift_From_CVPR_2017_paper.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>NST</strong>, <em>Like What You Like: Knowledge Distill via Neuron Selectivity Transfer.</em> In: CVPR'17. <a href="https://arxiv.org/pdf/1707.01219.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>RKD</strong>, <em>Relational Knowledge Distillation.</em> In: CVPR'19. <a href="https://arxiv.org/pdf/1412.6550.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>SPKD</strong>, <em>Similarity-Preserving Knowledge Distillation.</em> In: CVPR'19. <a href="https://arxiv.org/pdf/1907.09682.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>CRD</strong>, <em>Contrastive Representation Distillation.</em> In: ICLR'20. <a href="https://arxiv.org/pdf/1910.10699.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>REFILLED</strong>, <em>Distilling Cross-Task Knowledge via Relationship Matching.</em> In: CVPR'20. <a href="http://www.lamda.nju.edu.cn/lus/files/CVPR20_ReFilled.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>
</details>

<details>
<summary style="margin-left: 2px;"><b>M</b>erger Module [<em>Click to Expand</em>]<p style="margin-left: 12px;">The Merger module influences <b>the inference phase</b> by either reusing pre-trained features or incorporating adapted logits from the pre-trained model.</p></summary>
  <details>
  <summary style="margin-left: 12px;"><strong>Model Soup:</strong> <em>averaging weights of multiple fine-tuned models improves accuracy without increasing inference time.</em> In: ICML'22. <a href="https://arxiv.org/pdf/2203.05482.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>

  <details>
  <summary style="margin-left: 12px;"><strong>WiSE-FT</strong>, <em>Robust fine-tuning of zero-shot models.</em> In: CVPR'22. <a href="https://arxiv.org/pdf/2109.01903.pdf">[Paper]</a> <a href="https://github.com">[Code]</a></summary>
  <div style="margin-left: 30px;">
    <img src="https://github.com/zhangyikaii/LAMDA-ZhiJian/blob/main/assests/adapter.png?raw=true" alt="WSFG" width="auto" height="300px" />
  </div>
  </details>
</details>

<!-- &nbsp; -->

💡 **ZhiJian** also has the following **highlights**:

+ **Support** reuse of various **pre-trained model zoo**, including:
  +  PyTorch [Torchvision](https://pytorch.org/vision/stable/models.html); OpenAI [CLIP](https://github.com/openai/CLIP); 🤗Hugging Face [PyTorch Image Models (timm)](https://github.com/huggingface/pytorch-image-models), [Transformers](https://github.com/huggingface/transformers)
  + Other popular projects, *e.g.*, [vit-pytorch](https://github.com/lucidrains/vit-pytorch) (stars [14k](https://github.com/lucidrains/vit-pytorch/stargazers)).
  + Large Language Model, including [baichuan](https://huggingface.co/baichuan-inc/baichuan-7B), [LLaMA](https://github.com/facebookresearch/llama), and [BLOOM](https://huggingface.co/bigscience/bloom).
+ **Extremely easy** to get started and **customize**
  + Get started with a 10 minute blitz [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](TODO)
  + Customize datasets and pre-trained models with step-by-step instructions [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](TODO)
  + Feel free to create a novel approach for reusing pre-trained model [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](TODO)
+ **Concise** things do **big**
  + only ~5000 lines of the base code, with incorporating method like building *LEGO* blocks
  + **State-of-the-art** results on [VTAB benchmark](https://google-research.github.io/task_adaptation/) with approximately **10k** experiments [[here]](https://github.com/zhangyikaii/LAMDA-ZhiJian/tree/main/results)
  + Support friendly guideline and comprehensive documentation to custom dataset and pre-trained model [[here]](TODO)

> "ZhiJian" in Chinese means handling complexity with concise and efficient methods. Given the variations in pre-trained models and the deployment overhead of full parameter fine-tuning, ZhiJian represents a solution that is easily reusable, maintains high accuracy, and maximizes the potential of pre-trained models.
> 
> “执简驭繁”的意思是用简洁高效的方法驾驭纷繁复杂的事物。“繁”表示现有预训练模型和复用方法种类多、差异大、部署难，所以取名"执简"的意思是通过该工具包，能轻松地驾驭模型复用方法，易上手、快复用、稳精度，最大限度地唤醒预训练模型的知识。

&nbsp;

## 🕹️ Quick Start

1. An environment with Python 3.7+ from [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html "conda-env"), [venv](https://docs.python.org/3/library/venv.html), or [virtualenv](https://virtualenv.pypa.io/en/latest/).

2. Install ZhiJian using pip:
   ```bash
   $ pip install ZhiJian
   ```
   For more details please click [installation instructions](TODO/INSTALL.md).

   + [Option] Install with the newest version through GitHub:
      ```bash
      $ pip install git+https://github.com/ZhangYikaii/ZhiJian.git@main --upgrade
      ```

3. Open your python console and type
   ```python
   import ZhiJian
   print(ZhiJian.__version__)
   ```
   If no error occurs, you have successfully installed ZhiJian.


&nbsp;

## Documentation

📚 The tutorials and API documentation are hosted on [ZhiJian.readthedocs.io](https://zhijian.readthedocs.io/)

中文文档正在搭建中..

&nbsp;

## Why ZhiJian?

![architecture](https://github.com/zhangyikaii/LAMDA-ZhiJian/raw/main/assests/architecture.png?raw=true)

<table>
  <tr>
    <td colspan="9" style="border-bottom: 2px solid black;"></td>
  </tr>
  <tr>
    <td><b>Related Library</b></td>
    <td><b>GitHub Stars</b></td>
    <td><b># of Alg.<sup>(1)</sup></b></td>
    <td><b># of Model<sup>(1)</sup></b></td>
    <td><b># of Dataset<sup>(1)</sup></b></td>
    <td><b># of Fields<sup>(2)</sup></b></td>
    <td><b>LLM Supp.</b></td>
    <td><b>Docs.</b></td>
    <td><b>Last Update</b></td>
  </tr>
  <tr>
    <td><a href="https://github.com/huggingface/peft">PEFT</a></td>
    <td><a href="https://github.com/huggingface/peft/stargazers">
      <img src="https://img.shields.io/github/stars/huggingface/peft" alt="GitHub stars">
    </a></td>
    <td>6</td>
    <td>~15</td>
    <td>➖<sup>(3)</sup></td>
    <td>1<sup>(a)</sup></td>
    <td>✔️</td>
    <td>✔️</td>
    <td>
    <a>
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/huggingface/peft?label=last%20update">
    </a>
    </td>
  </tr>
  <tr>
    <td><a href="https://github.com/adapter-hub/adapter-transformers">adapter-transformers</a></td>
    <td><a href="https://github.com/adapter-hub/adapter-transformers/stargazers">
      <img src="https://img.shields.io/github/stars/adapter-hub/adapter-transformers" alt="GitHub stars">
    </a></td>
    <td>10</td>
    <td>~15</td>
    <td>➖<sup>(3)</sup></td>
    <td>1<sup>(a)</sup></td>
    <td>❌</td>
    <td>✔️</td>
    <td>
    <a>
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/adapter-hub/adapter-transformers?label=last%20update">
    </a>
    </td>
  </tr>
  <tr>
    <td><a href="https://github.com/hiyouga/LLaMA-Efficient-Tuning">LLaMA-Efficient-Tuning</a></td>
    <td><a href="https://github.com/hiyouga/LLaMA-Efficient-Tuning/stargazers">
      <img src="https://img.shields.io/github/stars/hiyouga/LLaMA-Efficient-Tuning" alt="GitHub stars">
    </a></td>
    <td>4</sup></td>
    <td>5</td>
    <td>~20</td>
    <td>1<sup>(a)</sup></td>
    <td>✔️</td>
    <td>❌</td>
    <td>
    <a>
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/hiyouga/LLaMA-Efficient-Tuning?label=last%20update">
    </a></td>
  </tr>
  <tr>
    <td><a href="https://github.com/AberHu/Knowledge-Distillation-Zoo">Knowledge-Distillation-Zoo</a></td>
    <td><a href="https://github.com/AberHu/Knowledge-Distillation-Zoo/stargazers">
      <img src="https://img.shields.io/github/stars/AberHu/Knowledge-Distillation-Zoo" alt="GitHub stars">
    </a></td>
    <td>20</td>
    <td>2</td>
    <td>2</td>
    <td>1<sup>(b)</sup></td>
    <td>❌</td>
    <td>❌</td>
    <td>
    <a>
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/AberHu/Knowledge-Distillation-Zoo?label=last%20update">
    </a></td>
  </tr>
  <tr>
    <td><a href="https://github.com/sicara/easy-few-shot-learning">Easy Few-Shot Learning</a></td>
    <td><a href="https://github.com/sicara/easy-few-shot-learning/stargazers">
      <img src="https://img.shields.io/github/stars/sicara/easy-few-shot-learning" alt="GitHub stars">
    </a></td>
    <td>10</td>
    <td>3</td>
    <td>2</td>
    <td>1<sup>(b)</sup></td>
    <td>❌</td>
    <td>❌</td>
    <td>
    <a>
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/sicara/easy-few-shot-learning?label=last%20update">
    </a></td>
  </tr>
  <tr>
    <td><a href="https://github.com/mlfoundations/model-soups">Model soups</a></td>
    <td><a href="https://github.com/mlfoundations/model-soups/stargazers">
      <img src="https://img.shields.io/github/stars/mlfoundations/model-soups" alt="GitHub stars">
    </a></td>
    <td>3</sup></td>
    <td>3</td>
    <td>5</td>
    <td>1<sup>(c)</sup></td>
    <td>❌</td>
    <td>❌</td>
    <td>
    <a>
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/mlfoundations/model-soups?label=last%20update">
    </a></td>
  </tr>
  <tr>
    <td><a href="https://github.com/samuela/git-re-basin">Git Re-Basin</a></td>
    <td><a href="https://github.com/samuela/git-re-basin/stargazers">
      <img src="https://img.shields.io/github/stars/samuela/git-re-basin" alt="GitHub stars">
    </a></td>
    <td>3</sup></td>
    <td>5</td>
    <td>4</td>
    <td>1<sup>(c)</sup></td>
    <td>❌</td>
    <td>❌</td>
    <td>
    <a>
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/samuela/git-re-basin?label=last%20update">
    </a></td>
  </tr>
  <tr>
    <td colspan="9" style="border-bottom: 2px solid grey;"></td>
  </tr>
  </tr>
    <tr>
    <td><b>ZhiJian</b></td>
    <!-- <td><a href="https://github.com/adapter-hub/adapter-transformers/stargazers">
      <img src="https://img.shields.io/github/stars/zhangyikaii/LAMDA-ZhiJian" alt="GitHub stars">
    </a></td> -->
    <td>🙌</td>
    <td>30+</td>
    <td>~50</td>
    <td>19</td>
    <td>3<sup>(a,b,c)</sup></td>
    <td>✔️</td>
    <td>✔️</td>
    <td>
    <a>
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/zhangyikaii/LAMDA-ZhiJian?label=last%20update">
    </a></td>
  </tr>

</table>


<sup><b>(1)</b>: access date: 2023-08-05</sup>
<sup><b>(2)</b>: fields for (a) Architect; (b) Tuner; (c) Merger;</sup>

### 📦 Reproducible SoTA Results

**ZhiJian** fixed the random seed to ensure reproducibility of the results, with only minor variations across different devices.
Partial results are displayed below. For more, please click [[here]](TODO)

<!-- **Trained Weights**:

<details>
<summary style="margin-left: 20px;"><b>Adapter</b> from "Parameter-Efficient Transfer Learning for NLP", ICML'19</summary>
<div style="margin-left: 30px;">

|Datasets | Acc@1 | Acc@5 | Link to Weights
|---|---|---|---|
| CIFAR-100 | TODO | TODO | [Google Drive](), [Baidu Drive]() |
| Caltech101| TODO | TODO | [Google Drive](), [Baidu Drive]() |
| DTD | TODO | TODO | [Google Drive](), [Baidu Drive]() |
</div>
</details> -->

&nbsp;

## Installation for Research


&nbsp;

## Contributing

**ZhiJian** is currently in active development, and we warmly welcome any contributions aimed at enhancing capabilities. Whether you have insights to share regarding pre-trained models, data, or innovative reuse methods, we eagerly invite you to join us in making **ZhiJian** even better. If you want to submit your valuable contributions, please click [here](TODO).

&nbsp;

## Citing ZhiJian

```latex
@article{zhijian,
  arxiv cite todo
}
```

&nbsp;

## Acknowledgment

