from transformers import pipeline
from hazm import word_tokenize, Lemmatizer, Normalizer
import os

from capitals import capital_dictionary_keys, country_to_capital


def pipeline_sentence(sentence, model, tokenizer):
    sentence = change_words(sentence)

    normalizer = Normalizer()
    sentence = normalizer.normalize(sentence)
    sentence_lem = ' '.join([Lemmatizer().lemmatize(x) for x in
                             word_tokenize(normalizer.normalize(sentence))])
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    sentence_ner = nlp(sentence)
    sentence_ner_lem = nlp(sentence_lem)
    return sentence_ner, sentence_ner_lem, sentence_lem, sentence


def change_words(sentence):
    symbols = "!\"#$%&()*+-./;<=>?@[\\]^_`{|}~\n،,؟؛"
    for i in symbols:
        sentence = str.replace(sentence, i, ' ')

    if "پایتخت" in sentence:
        for key in capital_dictionary_keys():
            if key in sentence:
                sentence = sentence.replace(key, country_to_capital(key))
    if " دبی " in sentence:
        if "شهر دبی" not in sentence:
            sentence = sentence.replace("دبی", "شهر دبی")
    return sentence
