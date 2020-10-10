# Analyzing Firm Reports for Volatility Prediction: AKnowledge-Driven Text Embedding Approach

## [Description]

This folder contains source code to train finance-specificed word2vec model using Loughran and McDonald (LM) Dictionary as constraints. In particular, we use the Positive and Negative word lists.

## [Data Source]

The Form 10-Ks can be obtained from https://www.sec.gov/edgar/searchedgar/companysearch.html
You should extract text-related sections, including Section 1, Section 1A, and Section 7 section from the Form 10-Ks.

The LM Sentiment word list can be obtained from https://sraf.nd.edu/textual-analysis/resources/

## [Compile]

gcc LM-w2v.c -o LM-w2v -lm -pthread -O2 -Wall -funroll-loops -Wno-unused-result

## [Train Corpus]

To prepare a customized training corpus, you can refer to prepare_corpus.py. This script strips all the punctuations, tokenize texts and convert the uppercase to lowercase at the beginning of a sentence.


[Train Embedding]
To train a finance-specific word2vec model, you need to provide a training corpus, a binary label for sentiment words, and a vocabulary. You also need to configure hyperparameters beta-m and beta-c that control the stength of must-links and cannot-links.

./LM-w2v -size 200 -train train_corpus.txt -label labels_LM_binary.txt -save_vocab vocab.txt -debug 2 -lambda 4e-4 -output 200_1_1_5.txt -window 5 -sample 1e-4 -hs 0 -negative 5 -constraints 32 -beta-m 1 -beta-c 1 -threads 10 -epochs 1

[Pre-trained Embedding]
You can download our pre-trained embeddings at: https://gohkust-my.sharepoint.com/:f:/g/personal/imyiyang_ust_hk/Eh0_BWRQ_1FAvKr6-mwa1d8BD2KGE2M1-Vvq9cY6gcdYvg?e=DbU5lP

[Acknowledge]
Part of the code is adopted from the Google word2vec [1] and sentivec [2]. We thank to the atuhors for releasing their codes. Please also consider citing their work.

[1] Mikolov, Tomas, Ilya Sutskever, Kai Chen, Greg S. Corrado, and Jeff Dean. "Distributed representations of words and phrases and their compositionality." In Advances in neural information processing systems, pp. 3111-3119. 2013.

[2] Tkachenko, Maksim, Chong Cher Chia, and Hady Lauw. "Searching for the x-factor: Exploring corpus subjectivity for word embeddings." In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics, pp. 1212-1221. 2018.

[Disclaimer]
This is a reference implementation of LM-WE (L&M Dictionary Enhanced Word Embeddings). For details or questions, please contact the author.

We also thank Xinyi Wang for her RA work and contribution to this codebase.
