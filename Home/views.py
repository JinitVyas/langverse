from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from translate import Translator

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Create your views here.
def index(request):
    return render(request, "index.html")

def to_eng(inputText):
    translator = Translator(to_lang="en")
    # translation = translator.translate("Machine learning is a subset of artificial intelligence (AI) that focuses on enabling computers to learn from data and improve over time without being explicitly programmed. It employs various algorithms and models to analyze and interpret data, extract meaningful patterns, and make predictions or decisions. Machine learning has applications in numerous fields such as natural language processing, computer vision, healthcare, finance, and more.")
    translation_in_English = translator.translate(inputText)

    return translation_in_English

def to_OutputLang(request):
    if request.method == 'POST':
        output_lang = request.POST.get('outputLang')
        input_text = request.POST.get('inputText')

        if output_lang and input_text:
            translator = Translator(output_lang)
            translation_in_output_lang = translator.translate(to_eng(input_text))
            return HttpResponse(translation_in_output_lang)
        else:
            return HttpResponseBadRequest("Missing input text or output language.")
    else:
        return HttpResponseBadRequest("Invalid request method.")
