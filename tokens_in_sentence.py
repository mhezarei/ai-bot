from hazm import Lemmatizer


def find_tokens_in_sentence(sentence_ner, sentence_ner_lem):
    tokens_lem = []
    for token in sentence_ner_lem:
        if len(tokens_lem) > 0:
            if token['word'].startswith('##'):
                tokens_lem[-1]['word'] += ' ' + token['word'][2:]
                tokens_lem[-1]['index'] += 1
            elif token['entity'].split('-')[1] == tokens_lem[-1][
                'entity_group'] and token['index'] == tokens_lem[-1][
                'index'] + 1:
                tokens_lem[-1]['word'] += ' ' + token['word']
                tokens_lem[-1]['index'] += 1
            else:
                tokens_lem += [
                    {'word': Lemmatizer().lemmatize(token['word']),
                     'entity_group': token['entity'].split('-')[1],
                     'index': token['index']}]
        else:
            tokens_lem += [
                {'word': Lemmatizer().lemmatize(token['word']),
                 'entity_group': token['entity'].split('-')[1],
                 'index': token['index']}]

    tokens = []
    for token in sentence_ner:

        if len(tokens) > 0:
            if token['word'].startswith('##'):
                tokens[-1]['word'] += ' ' + token['word'][2:]
                tokens[-1]['index'] += 1
            elif token['entity'].split('-')[1] == tokens[-1][
                'entity_group'] and token['index'] == tokens[-1][
                'index'] + 1:
                tokens[-1]['word'] += ' ' + token['word']
                tokens[-1]['index'] += 1
            else:
                tokens += [
                    {'word': token['word'],
                     'entity_group': token['entity'].split('-')[1],
                     'index': token['index']}]
        else:
            tokens += [{'word': token['word'],
                        'entity_group': token['entity'].split('-')[1],
                        'index': token['index']}]
    return tokens, tokens_lem
