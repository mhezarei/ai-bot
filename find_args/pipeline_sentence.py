from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
from hazm import word_tokenize, Lemmatizer, Normalizer


def pipeline_sentence(sentence):
	tokenizer = AutoTokenizer.from_pretrained("Model/")
	model = AutoModelForTokenClassification.from_pretrained("Model/")
	
	normalizer = Normalizer()
	sentence = normalizer.normalize(sentence)
	sentence_lem = ' '.join([Lemmatizer().lemmatize(x) for x in
	                         word_tokenize(normalizer.normalize(sentence))])
	nlp = pipeline("ner", model=model, tokenizer=tokenizer)
	sentence_ner = nlp(sentence)
	sentence_ner_lem = nlp(sentence_lem)
	return sentence_ner, sentence_ner_lem, sentence_lem
