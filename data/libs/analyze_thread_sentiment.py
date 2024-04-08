import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from data.models import Thread

plt.style.use('ggplot')

def filter_threads(input):
    thread_id = input.get("thread_id")
    title_words = input.get("title_words")
    content_words = input.get("content_words")

    thread_data = Thread.objects.filter(
        thread_id = thread_id, 
        article__icontains=title_words,
        body__icontains=content_words
          )
    return thread_data

def nltk_analyzer(data):
    ...

def transformer(data):
    ...

def other(data):
    ...

def main(input):
    ...
    # build django filters for model
    data = filter_threads(input)
    # nltk method
    nltk_data = nltk_analyzer(data)
    # transformer method
    transformer_data = transformer(data)
    # other method
    other_data = other(data)

    context = {
        "nltk_data": nltk_data,
        # "transformer_data": transformer_data,
        # "other_data": other_data 
    }

    return context