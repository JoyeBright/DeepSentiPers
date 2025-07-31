## DeepSentiPers: Novel Deep Learning Models Trained Over Proposed Augmented Persian Sentiment Corpus
## Sentiment Analysis in Persian Using Deep Neural Networks
## Binary and multiclass sentiment detection using deep neural architectures (BLSTM and CNN) on Persian augmented texts
NB: DeepSentiPers is a modified version of our paper presented at the fifth computational linguistics conference in Iran.
<br>
[https://arxiv.org/pdf/2004.05328.pdf](https://arxiv.org/pdf/2004.05328.pdf)

This study uses deep neural networks to extract opinions from each Persian sentence-level text. Deep learning models have introduced a new way to boost output quality. However, these architectures require large annotated datasets and must be carefully designed. To the best of our knowledge, we not only suffer from a lack of well-annotated Persian sentiment corpora but also from the absence of a novel model capable of classifying Persian opinions for both multi-class and binary classification tasks. Therefore, our study first proposes two novel deep learning architectures, comprising bidirectional LSTM and CNN layers. These architectures form part of a precisely designed deep neural hierarchy and can classify sentences for both tasks. Second, we propose three data augmentation techniques for the low-resource Persian sentiment corpus. Our comprehensive experiments on three baselines and two different neural word embedding methods demonstrate that our data augmentation strategies and proposed models successfully address the research objectives.

![DeepSentiPers](https://javad.pourmostafa.com/assets/images/DeepSentiPers.png)

## Results
Overall the DeepSentiPers achieved the following results in the Persian sentiment analysis task. H/E, read the paper to find out more about the results.

| Classification-Type | BLSTM F1-Score | Word-Embedding | Data-Augmentation |
|:-------------------:|:--------------:|:--------------:|:-----------------:|
|        Binary       |      91.98     |      Keras     |   Translation     |
|     Multi-Class     |      69.33     |    FastText    |   Translation     |

## Citation
Please cite the [arXiv](https://arxiv.org/pdf/2004.05328.pdf) paper if you use DeepSentiPers in your work:
```
@misc{sharami2020deepsentipers,
    title={DeepSentiPers: Novel Deep Learning Models Trained Over Proposed Augmented Persian Sentiment Corpus},
    author={Javad PourMostafa Roshan Sharami and Parsa Abbasi Sarabestani and Seyed Abolghasem Mirroshandel},
    year={2020},
    eprint={2004.05328},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

## Getting started

All the things you need to work on this project is an Ipython environment like the *Google Colab* or *Jupyter* and the dataset files.

## Dataset

The dataset used in this project was collected from *[SentiPers](https://arxiv.org/abs/1801.07737)* corpus, containing 7419 Persian sentences and their corresponding polarity.
The original and augmented dataset files are accessible in the "*Dataset*" folder.

## Authors

- **Javad Pourmostafa** - [GitHub](https://github.com/JoyeBright), [LinkedIn](https://www.linkedin.com/in/javadpourmostafa), [ResearchGate](https://www.researchgate.net/profile/Javad_Pourmostafa_Roshan_Sharami), [Website](https://javad.pourmostafa.com)
- **Parsa Abbasi** - [GitHub](https://github.com/parsa-abbasi), [LinkedIn](https://www.linkedin.com/in/parsa-abbasi/), [ResearchGate](https://www.researchgate.net/profile/Parsa_Abbasi_Sarabestani), [Website](http://parsa-abbasi.ir)
- **Seyed Abolghasem Mirroshandel** [LinkedIn](https://ir.linkedin.com/in/seyed-abolghasem-mirroshandel-1a3a5950), [ResearchGate](https://www.researchgate.net/profile/Seyedabolghasem_Mirroshandel), [Website](https://nlp.guilan.ac.ir/mirroshandel)

## Miscellaneous

See also the list of [contributors](https://github.com/parsa-abbasi/Sentiment-Analysis/contributors) who participated in this project.

We're glad to announce that the DeepSentiPers has also been written in Persian. You can find it here: https://zenodo.org/record/3551273. Please note that the intended version is slightly different from the English version. 

**Persian Title:** ارائه یک سیستم تحلیل احساس در زبان فارسی با استفاده از مدل های یادگیری عمیق
