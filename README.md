## DeepSentiPers: Deep Learning Models Plus Data Augmentation Methods in Persian Sentiment Analysis

Binary and multiclass sentiment detection using deep neural architectures (BLSTM and CNN) on Persian augmented texts
<br>
[https://arxiv.org/pdf/2004.05328.pdf](https://arxiv.org/pdf/2004.05328.pdf)

This paper focuses on how to extract opinions over each Persian sentence-level text. Deep learning models provided a new way to boost the quality of the output. However, these architectures need to feed on big annotated data as well as an accurate design. To best of our knowledge, we do not merely suffer from lack of well-annotated Persian sentiment corpus, but also a novel model to classify the Persian opinions in terms of both multiple and binary classification. So in this work, first we propose two novel deep learning architectures comprises of bidirectional LSTM and CNN. They are a part of a deep hierarchy designed precisely and also able to classify sentences in both cases. Second, we suggested three data augmentation techniques for the low-resources Persian sentiment corpus. Our comprehensive experiments on three baselines and two different neural word embedding methods show that our data augmentation methods and intended models successfully address the aims of the research.

![DeepSentiPers](https://javad.pourmostafa.com/assets/images/DeepSentiPers.png)

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

The dataset is used in this project was collected from *[SentiPers](https://arxiv.org/abs/1801.07737)* corpus. It contains 7419 Persian sentences and their relative polarity.
The original and augmented dataset files are accessible in the "*Dataset*" folder.

## Authors

- **Javad PourMostafa** - [GitHub](https://github.com/JoyeBright), [LinkedIn](https://www.linkedin.com/in/javadpourmostafa), [ResearchGate](https://www.researchgate.net/profile/Javad_Pourmostafa_Roshan_Sharami), [Website](https://javad.pourmostafa.com)
- **Parsa Abbasi** - [GitHub](https://github.com/parsa-abbasi), [LinkedIn](https://www.linkedin.com/in/parsa-abbasi/), [ResearchGate](https://www.researchgate.net/profile/Parsa_Abbasi_Sarabestani), [Website](http://parsa-abbasi.ir)

See also the list of [contributors](https://github.com/parsa-abbasi/Sentiment-Analysis/contributors) who participated in this project.

