def find_weather_method(sentence_lem):
    temp_key_words = ['دما', 'درجه', 'اندازه', 'چقدر', 'میزان']
    for word in temp_key_words:
        if word in sentence_lem:
            return "temp"
    return "cond"