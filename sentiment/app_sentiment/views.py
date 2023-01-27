from django.shortcuts import render
from .apps import AppSentimentConfig
from django.http import JsonResponse
from rest_framework.views import(APIView)

import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet

# Create your views here.

def negation(sentence):	
    '''
    Input: Tokenized sentence (List of words)
    Output: Tokenized sentence with negation handled (List of words)
    '''
    temp = int(0)
    for i in range(len(sentence)):
        if sentence[i-1] in ['not',"n't"]:
            antonyms = []
            for syn in wordnet.synsets(sentence[i]):
                syns = wordnet.synsets(sentence[i])
                w1 = syns[0].name()
                temp = 0
                for l in syn.lemmas():
                    if l.antonyms():
                        antonyms.append(l.antonyms()[0].name())
                max_dissimilarity = 0
                for ant in antonyms:
                    syns = wordnet.synsets(ant)
                    w2 = syns[0].name()
                    syns = wordnet.synsets(sentence[i])
                    w1 = syns[0].name()
                    word1 = wordnet.synset(w1)
                    word2 = wordnet.synset(w2)
                    if isinstance(word1.wup_similarity(word2), float) or isinstance(word1.wup_similarity(word2), int):
                        temp = 1 - word1.wup_similarity(word2)
                    if temp>max_dissimilarity:
                        max_dissimilarity = temp
                        antonym_max = ant
                        sentence[i] = antonym_max
                        sentence[i-1] = ''
    while '' in sentence:
        sentence.remove('')
    sentence = ' '.join(sentence)
    return sentence

class call_model(APIView):
    def get(self,request):
        if request.method == 'GET':
            text = request.GET.get('text')
            
            vector = AppSentimentConfig.vectorizer.transform([negation(word_tokenize(text))])
            prediction = AppSentimentConfig.model.predict(vector)[0]
            response = {'text_sentiment': prediction}
            return JsonResponse(response)
        
        
