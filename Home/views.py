from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from translate import Translator

# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer
# import nltk

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


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
            translation_in_output_lang = translator.translate(summarize_text(to_eng(input_text), num_sentences = request.POST.get('numOfLines')))
            return HttpResponse(translation_in_output_lang)
        else:
            print("Missing input text or output language.")
            return HttpResponseBadRequest("Missing input text or output language.")
    else:
        print("Invalid request method.")
        return HttpResponseBadRequest("Invalid request method.")

# def summarize_text(text, num_sentences=2):
    # Initialize parser and tokenizer
    # parser = PlaintextParser.from_string(text, Tokenizer("english"))
    
    # # Initialize LSA Summarizer
    # summarizer = LsaSummarizer()
    
    # # Summarize the text
    # summary = summarizer(parser.document, num_sentences)
    
    # # Join the summarized sentences into a single string
    # summarized_text = " ".join([str(sentence) for sentence in summary])
    
    # return summarized_text

def summarize_text(text, num_sentences=3, summarization_model='LSA'):
    # Preprocess the input text if necessary

    # Create a parser object
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Initialize the summarization model
    if summarization_model == 'LSA':
        summarizer = LsaSummarizer(Stemmer("english"))

    # Summarize the text
    summary = summarizer(parser.document, num_sentences)

    # Join the summarized sentences into a single string
    summarized_text = " ".join([str(sentence) for sentence in summary])

    return summarized_text