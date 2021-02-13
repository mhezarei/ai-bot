from transformers import pipeline
from hazm import word_tokenize, Lemmatizer, Normalizer
import os


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

    capital_dictionary = {
        "پایتخت آذربایجان": "باکو",
        "پایتخت آرژانتین": "بوئنوس آیرس",
        "پایتخت آلبانی": "تیرانا",
        "پایتخت آلمان": "برلین",
        "پایتخت آنتیگوا و باربودا": "سنت جونز",
        "پایتخت آندورا": "آندورا",
        "پایتخت آنگولا": "لوآندا",
        "پایتخت اتریش": "وین",
        "پایتخت اتیوپی": "آدیس آبابا",
        "پایتخت اردن": "امّان(عمّان)",
        "پایتخت ارمنستان": "ایروان",
        "پایتخت اسپانیا": "مادرید",
        "پایتخت استرالیا": "کانبرا",
        "پایتخت استونی": "تالین",
        "پایتخت اسلواکی": "براتیسلاوا",
        "پایتخت اسلوونی": "لیوبلیانا",
        "پایتخت افریقای جنوبی": "پرتوریا-کیپ تاون",
        "پایتخت افریقای مرکزی": "بانگی",
        "پایتخت افغانستان": "کابل",
        "پایتخت اکوادور": "کیتو",
        "پایتخت الجزایر": "الجزیره",
        "پایتخت السالوادور": "سان سالوادور",
        "پایتخت امارات متحده عربی": "ابوظبی",
        "پایتخت انگلستان": "لندن",
        "پایتخت اوروگوئه": "مونته ویدئو",
        "پایتخت اوکراین": "کیف",
        "پایتخت اوگاندا": "کامپالا",
        "پایتخت ایالات متحده  امریکا": "واشینگتن",
        "پایتخت ایتالیا": "رم",
        "پایتخت ایران": "تهران",
        "پایتخت ایرلند": "دوبلین",
        "پایتخت ایسلند": "ریکیاویک",
        "پایتخت باربادوس": "بریج تاون",
        "پایتخت باهاما": "ناسائو",
        "پایتخت بحرین": "منامه",
        "پایتخت برزیل": "برازیلیا",
        "پایتخت برونئی": "سری بگاوان",
        "پایتخت بلژیک": "بروکسل",
        "پایتخت بلیز": "بلموپان",
        "پایتخت بنگلادش": "داکا",
        "پایتخت بنین": "پرتونوو",
        "پایتخت بوتان": "تیمبو(تیمپو)",
        "پایتخت بوتسوانا": "گابرون",
        "پایتخت بورکینا فاسو": "واگادوگو",
        "پایتخت بوروندی": "بوجومبورا",
        "پایتخت بوسنی و هرزگوین": "سارایوو",
        "پایتخت بولیوی": "سوکره -لاپاز",
        "پایتخت پاپوا گینه نو": "پورت مورسبی",
        "پایتخت پاراگوئه ": "آسونسیون",
        "پایتخت پاکستان": "اسلام آباد",
        "پایتخت پالائو": "نگرولمود",
        "پایتخت پاناما": "پاناما سیتی",
        "پایتخت پرتغال": "لیسبون",
        "پایتخت پرو": "لیما",
        "پایتخت تاجیکستان": "دوشنبه",
        "پایتخت تانزانیا": "دودوما",
        "پایتخت تایلند": "بانکوک",
        "پایتخت تایوان": "تایپه",
        "پایتخت ترکمنستان ": "عشق آباد",
        "پایتخت ترکیه": "آنکارا",
        "پایتخت ترینیداد و توباگو": "پرت آو اسپاین",
        "پایتخت توگو": "لومه",
        "پایتخت تونس": "تونس",
        "پایتخت تونگا": "نوکوآلوفا",
        "پایتخت تووالو": "فونافوتی",
        "پایتخت جامائیکا": "کینگستون",
        "پایتخت اریتره": "اسمره",
        "پایتخت اندونزی": "جاکارتا",
        "پایتخت جیبوتی": "جیبوتی",
        "پایتخت چاد": "انجامنا",
        "پایتخت چک": "پراگ",
        "پایتخت چین": "پکن",
        "پایتخت دانمارک": "کپنهاگ",
        "پایتخت دومینیکا": "روسو",
        "پایتخت دومینیکن": "سانتو دومینگو",
        "پایتخت روآندا": "کیگالی",
        "پایتخت روسیه": "مسکو",
        "پایتخت بلاروس": "مینسک",
        "پایتخت رومانی": "بخارست",
        "پایتخت (جمهوری دمکراتیک کنگو (زئیر- کنگوی کینشاسا": "کینشاسا",
        "پایتخت زامبیا": "لوساکا",
        "پایتخت زلاند نو": "ولینگتون",
        "پایتخت زیمبابوه": "هراره",
        "پایتخت ژاپن": "توکیو",
        "پایتخت سائوتومه و پرنسیپ": "سائوتومه",
        "پایتخت ساحل عاج": "یاموسوکرو",
        "پایتخت ساموآ": "آپیا",
        "پایتخت سن مارینو(سان مارینو)": "سن مارینو",
        "پایتخت سری لانکا": "کلمبو",
        "پایتخت جزایرسلیمان": "هونیارا",
        "پایتخت سنت کیتس و نویس": "باستر",
        "پایتخت سنت لوسیا": "کاستریس",
        "پایتخت سنت وینسنت و گرنادین": "کینگزتاون",
        "پایتخت سنگاپور": "سنگاپور",
        "پایتخت سنگال": "داکار",
        "پایتخت سوئد": "استکهلم",
        "پایتخت سوئیس": "برن",
        "پایتخت سوازیلند": "امبابان",
        "پایتخت سودان": "خارطوم",
        "پایتخت سورینام": "پاراماریبو",
        "پایتخت سوریه": "دمشق",
        "پایتخت سومالی": "موگادیشو",
        "پایتخت سیرالئون": "فری تاون",
        "پایتخت سیشل": "ویکتوریا",
        "پایتخت شیلی": "سانتیاگو",
        "پایتخت صحرای غربی": "العیون",
        "پایتخت صربستان": "بلگراد",
        "پایتخت عراق": "بغداد",
        "پایتخت عربستان سعودی": "ریاض",
        "پایتخت عمان": "مسقط",
        "پایتخت غنا": "آکرا",
        "پایتخت فرانسه": "پاریس",
        "پایتخت فلسطین": "بیت المقدس(قدس)",
        "پایتخت فنلاند": "هلسینکی",
        "پایتخت فیجی": "سووا",
        "پایتخت فیلیپین": "مانیل",
        "پایتخت قبرس": "نیکوزیا",
        "پایتخت قرقیزستان": "بیشکک",
        "پایتخت قزاقستان": "آستانه",
        "پایتخت قطر": "دوحه",
        "پایتخت کالدونیای جدید": "نومئا",
        "پایتخت کامبوج": "پنوم پن",
        "پایتخت کامرون": "یائونده",
        "پایتخت کانادا": "اتاوا",
        "پایتخت کرواسی": "زاگرب",
        "پایتخت کره جنوبی": "سئول",
        "پایتخت کره شمالی": "پیونگ یانگ",
        "پایتخت کاستاریکا": "سان خوزه",
        "پایتخت کلمبیا": "بوگوتا",
        "پایتخت کنگو": "برازاویل",
        "پایتخت کنیا": "نایروبی",
        "پایتخت کوبا": "هاوانا",
        "پایتخت کومور": "مورونی",
        "پایتخت کویت": "کویت",
        "پایتخت کیپ ورد": "پرایا",
        "پایتخت کیریباتی": "تاراوا",
        "پایتخت گابن": "لیبرویل",
        "پایتخت گامبیا": "بانجول",
        "پایتخت گرجستان": "تفلیس",
        "پایتخت گرنادا": "سنت جورجز",
        "پایتخت گواتمالا": "گواتمالا سیتی",
        "پایتخت گویان": "جورج تاون",
        "پایتخت گینه": "کوناکری",
        "پایتخت گینه استوائی": "مالابو",
        "پایتخت گینه بیسائو": "بیسائو",
        "پایتخت لائوس": "وین تیان",
        "پایتخت لاتوی(لتونی)": "ریگا",
        "پایتخت لبنان": "بیروت",
        "پایتخت لسوتو": "ماسرو",
        "پایتخت لوکزامبورگ": "لوکزامبورگ",
        "پایتخت لهستان": "ورشو",
        "پایتخت لیبریا ": "مونروویا",
        "پایتخت لیبی": "تریپولی)طرابلس)",
        "پایتخت لیتوانی": "ویلنیوس",
        "پایتخت لیختن اشتاین": "فادوتس",
        "پایتخت جزایر مارشال": "ماجورو",
        "پایتخت ماداگاسکار(مالاگاسی)": "آنتاناناریوو",
        "پایتخت مالاوی": "لیلونگوه",
        "پایتخت مالت": "والِتا",
        "پایتخت مالدیو": "ماله",
        "پایتخت مالزی": "کوالالامپور",
        "پایتخت مالی": "باماکو",
        "پایتخت مجارستان": "بوداپست",
        "پایتخت مصر": "قاهره",
        "پایتخت مغرب(مراکش)": "رباط",
        "پایتخت مغولستان ": "اولان باتور",
        "پایتخت مقدونیه": "اسکوپیه",
        "پایتخت مکزیک": "مکزیکو سیتی",
        "پایتخت موریتانی": "نواکشوت",
        "پایتخت موریس": "پورت لوئیس",
        "پایتخت موزامبیک": "ماپوتو",
        "پایتخت مولداوی": "(کیشیناو)کیشی نف",
        "پایتخت موناکو": "موناکو",
        "پایتخت مونته نگرو": "پودگوریتسا",
        "پایتخت میانمار(برمه)": "تایپیداو",
        "پایتخت نائورو": "یارن",
        "پایتخت نامیبیا": "ویندهوک",
        "پایتخت نپال": "کاتماندو",
        "پایتخت نروژ ": "اسلو",
        "پایتخت نیجر": "نیامی",
        "پایتخت نیجریه": "آبوجا",
        "پایتخت نیکاراگوآ": "ماناگوآ",
        "پایتخت واتیکان": "واتیکان",
        "پایتخت وانواتو": "پورت ویلا",
        "پایتخت ونزوئلا": "کاراکاس",
        "پایتخت ویتنام": "هانوی",
        "پایتخت هائیتی": "پورتوپرنس",
        "پایتخت هلند": "آمستردام",
        "پایتخت هند": "دهلی نو",
        "پایتخت هندوراس": "تگوسیگالپا",
        "پایتخت یمن": "صنعا",
        "پایتخت یونان": "آتن",
        "پایتخت بلغارستان": "صوفیه",
        "پایتخت ازبکستان": "تاشکند"
    }
    if "پایتخت" in sentence:
        for key in capital_dictionary.keys():
            if key in sentence:
                sentence = sentence.replace(key, capital_dictionary[key])
    if "دبی" in sentence:
        if "شهر دبی" not in sentence:
            sentence = sentence.replace("دبی", "شهر دبی")
    return sentence
