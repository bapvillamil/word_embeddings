from django.shortcuts import render
from .apps import AppSentimentConfig
from django.http import JsonResponse
from rest_framework.views import(APIView)

# Create your views here.

class call_model(APIView):
    def get(self,request):
        if request.method == 'GET':
            text = request.GET.get('text')
            
            vector = AppSentimentConfig.vectorizer.transform([text])
            prediction = AppSentimentConfig.model.predict(vector)[0]
            response = {'text_sentiment': prediction}
            return JsonResponse(response)
        
        
