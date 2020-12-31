def find_cities(tokens):
    """
    find city in args:
      input : string from tokens
      output: list
    """
    cities = []
    for token in tokens:
        if token['entity_group'] == 'location':
            cities.append(token['word'])
    print(cities)
    return cities
