# EmotionAndIntentionRecognition
This repository contains the files and te code used in the paper "Emotion and Intention Detection in a Large Language Model"

# Emotion and Intention Detection in a Large Language Model

## This is the readme file that contains the information about how we used the dataset of Emotion aware Dialogue Act (EMOTyDA) in our paper:

**Paper Name:-** # Emotion and Intention Detection in a Large Language Model

* **Authors:** Emmanuel Castro, Hiram Calvo and Olga Kolesnikova
* **Affiliation:** Centro de Investigación en Computación, Instituto Politécnico Nacional, Mexico City, Mexico
* **Corresponding Author:** Hiram Calvo
  
You can obtain the EMOTyDA dataset from:
https://github.com/sahatulika15/EMOTyDA


We conducted three main experiments for emotion recognition and three for intention recognition: 
1. In the classification to utterance-level we send to the LLM sentence by sentence to its classification.
2. In the classification with conversational context level, we send the conversation privided toghether with the names ofeach participant. In the specific case of IEMOCAP, each turn of the conversation was provided with a fictition name to the LLM to understand the flow of the conversation.
3. In the classification with conversational context and the additional cues, the cues were attached to the end of each sentence between parentesis:

The files in this repository are organizared in 6 different carpets:
* The first 2 carpets of the present repositore have the sentences as we sended to the LLM. 
* The next 2 carpets have the results of IEMOCAP, the first one holding the files of the classification of DeepSeek-r1 and the second the classification of DeepSeek-v3.
* The final 2 carpets have the results of MELD, the first one holding the files of the classification of DeepSeek-r1 and the second the classification of DeepSeek-v3.

In order to mach every answer with the sentence whose belong is necesary to  have both files. For example,the firstt conversation on MELD dataset have 14 sentences (|1. - Chandler - also I was the point person on my company's transition from the KL-5 to GR-6 system. (neutral) /.../ 14.- The Interviewer - . Absolutely. You can relax (neutral)|)
and these need to be maches with the first 14 answer of the file:

1,Statement Non Opinion
2,Statement Opinion
3,Agreement
4,Command
5,Question
6,Statement Non Opinion
7,Acknowledge
8,Statement Non Opinion
9,Acknowledge
10,Statement Non Opinion
11,Disagreement
12,Statement Opinion
13,Question
14,Answer

Then the next conversation of 7 sentences (|1. - Joey - But then who? The waitress I went out with last month? /.../ 7.- Rachel - . Yeah, sure!|) ned to be mach with the next 7 answers:

1: Question
2: Command
3: Question
4: Answer
5: Acknowledge
6: Acknowledge
7: Agreement

We did the same for all the file.


