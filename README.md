# Process of Creating a Basic Sentiment Analysis
#### Note1: Don't expect complicated and tremendous strategies to achieve opinion mining, this is only a practical instance of using some basic rules to elicit the polarity of an input text.

#### Note2: I focus on detecting the overall polarity (Document Level Sentiment Classification) instead of Aspect level Sentiment Classification.

#### Note3: To develope a better SA system it is needed to use different corpora and apply diverse classification methods hence the following corpora have been added to the repo: <br>
* SentiWordNet
* SentiPers

#### Note3: For detecting the polarity of the sentences, a dictionary has been used. A dictionary is no more than a list of words that share a category. But sth that should be considered is, the design of the dictionaries depends on the domain where you want to do the opinion mining.
<hr>
### Text Structure:
*   Each input text is a list of sentences, each sentence is a list of tokens and each token is a row/tuple consists of <i>three</i> features:
   *   First Feature: Exact word
   *   Second Feature: A word Lemma (e.g: am/is/are:be)
   *   Third Feature: A list of associated tags
   
## Steps:
### 1. Preprocessing the input text
*   Sentence Splitting
*   Sentence Tokenization
*   POS-Tagging

##### Note: In this stage, we have the list of tokens with their associated Part of Speech. Then we have to adjust it with the defined <i>text structure</i>. Mapping has been implemented by using <i>adjust</i> method as a sub-method of <i>PreProcess</i> Class.
### 2. Defining Dictionaries 
##### Note: I used YAML configuration file for constructing dictionaries. Install into the current virtualenv by the following command<br>
> pip3 install yaml

##### Note: You can also use some pre-defined corpora like <i>SentiWordNet</i>
As described before, the dictionary is no more than a list of word that indicates the class of tokens. For instance, positive.yml, negative.yml and so on. 

### 3. Tagging the Input text with dictionaries
*   Opening Dictionaries Files
*   Loading Dictionaries Files
*   Closing Dictionaries Files
*   Creating A Tagged Dictionary List Based on Separate Loaded Dictionaries.yml

##### Note: This part of the code has been implemented in initialization scope of the <i>DictionaryTagger</i> Class.
##### Note: Also It is compulsory to get the maximum length of all the keys (dictionaries entities). why?
##### Note: Then we will find the corresponded tags through the sentences with the following priorities:
    1. Longest matches have higher priority
    2. Search from left to right
    
##### Note: Apply the finding process in each one the sentence. Afterward, if the sentence string does not match with the dictionary words then try to make the sentence into the smaller chunks up to matching with the dictionary tagged words. It was the reason for finding words with the highest matches.
    
### 4. Design SA Score Mechanism
#### Note: Finally, we have a list of words which distinguished based on their polarities. These positive polarities have one score and negative ones have minus one score. Then we accumulate all of the scores and detect what is the final consequence.


:rocket: Tip: For more accurate SA system, it is needed to add more dictionaries which support wide lexicon.<br>
:rocket: Tip: To put it in a nutshell, the main challenge for opinion mining is to find an optimal way of combining the word scores to an overall score for whole documents.

