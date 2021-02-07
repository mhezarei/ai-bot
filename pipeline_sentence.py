from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification, TFBertModel, PreTrainedTokenizerFast
from hazm import word_tokenize, Lemmatizer, Normalizer
import os


def pipeline_sentence(sentence):
    symbols = "!\"#$%&()*+-./;<=>?@[\]^_`{|}~\n،,؟؛"
    for i in symbols:
        sentence = str.replace(sentence, i, ' ')
    # /var/www/AIBot/media/bert-base-parsbert-ner-uncased
    tokenizer = AutoTokenizer.from_pretrained("bert-base-parsbert-ner-uncased")
    model = AutoModelForTokenClassification.from_pretrained("bert-base-parsbert-ner-uncased")
    # tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-base-parsbert-ner-uncased")
    # model = AutoModelForTokenClassification.from_pretrained("HooshvareLab/bert-base-parsbert-ner-uncased")

    normalizer = Normalizer()
    sentence = normalizer.normalize(sentence)
    sentence_lem = ' '.join([Lemmatizer().lemmatize(x) for x in
                             word_tokenize(normalizer.normalize(sentence))])
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    sentence_ner = nlp(sentence)
    sentence_ner_lem = nlp(sentence_lem)
    return sentence_ner, sentence_ner_lem, sentence_lem
