def find_weather_method(sentence_lem):
    temp_key_words = ["حداکثر", "بیشترین", "گرمترین", "گرم‌ترین",
                      "گرم ترین", "حداقل", "کمترین", "کمینه", "میانگین",
                      'دما', 'درجه', 'اندازه', 'چقدر', 'میزان', 'اختلاف',
                      'تفاوت', 'سردتر', 'سرد تر', "گرم‌تر ", "گرمتر ", "گرم تر ", "سرد", "گرم"]
    for word in temp_key_words:
        if word in sentence_lem:
            return "temp"
    return "cond"
