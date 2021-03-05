def find_cities(tokens, sentence):
    """
    find city in args:
      input : string from tokens
      output: list
    """
    cities = []
    for token in tokens:
        if token['entity_group'] == 'location':
            if token['word'] in sentence:
                cities.append(token['word'])
            else:
                city_name = token['word'].replace('ا', 'آ', 1)
                if city_name in sentence:
                    cities.append(city_name)
    return cities
