class persian_num_change:
    """
        resource: https://github.com/bestmahdi2/word2number/blob/master/ProgramFile/Persian_calculator.py
    """
    def __init__(self, text):
        self.text = text.replace(" و ", " ").replace("  "," ").replace(" صد ", "صد ").split(" ")
        self.text.append("صفر")
        self.num = 0
        self.Million = []
        self.Thousand = []
        self.Hundred = []

    def Million_separator(self, text):
        x = 0
        Num_M = 0

        for i in text:
            if i == "میلیون":
                Num_M = text.index(i)

        new_text = []
        while x < Num_M:
            new_text.append(text[x])
            x += 1
        self.Million = new_text

    def Thousand_seprator(self, text):
        x = 1
        Num_M = 0
        Num_T = 0

        for i in text:
            if i == "هزار":
                Num_T = text.index(i)
            if i == "میلیون":
                Num_M = text.index(i)
                x += Num_M

        if "میلیون" not in text:
            Num_M = -1
            x = 0

        new_text = []
        while x < Num_T and x > Num_M:
            new_text.append(text[x])
            x += 1
        self.Thousand = new_text

    def Hundred_seprator(self, text):
        x = 1
        Num_T = 0
        if "هزار" in text:
            for i in text:
                if i == "هزار":
                    Num_T = text.index(i)
                    x += Num_T

        if "هزار" not in text and "میلیون" in text:
            for i in text:
                if i == "میلیون":
                    Num_T = text.index(i)
                    x += Num_T

        if "هزار" not in text and "میلیون" not in text:
            x= 0
            Num_T = -1

        new_text = []
        while x > Num_T and x < len(text):
            new_text.append(text[x])
            x += 1
        self.Hundred = new_text

    def counter(self, text , sep):
        all_dic = {"یکصد": 100, "دویست": 200, "سیصد": 300, "چهارصد": 400,
                   "پانصد": 500, "ششصد": 600, "هفتصد": 700, "هشتصد": 800,
                   "نهصد": 900,
                   "بیست": 20, "سی": 30, "چهل": 40, "پنجاه": 50, "شصت": 60, "هفتاد": 70, "هشتاد": 80,
                   "نود": 90,
                   "ده": 10,"صفر" : 0 ,"یک": 1, "دو": 2, "سه": 3, "چهار": 4, "پنج": 5, "شش": 6, "هفت": 7, "هشت": 8,
                   "نه": 9,
                   "یازده": 11, "دوازده": 12, "سیزده": 13, "چهارده": 14, "پانزده": 15, "شانزده": 16,
                   "هفده": 17, "هجده": 18, "نوزده": 19}
        textlist = text.split(" ")
        for i in textlist:
            self.num += all_dic[i] * sep

    def duplicate_error(self , text):
        Rhundred = 0
        Rtens = 0
        Rteens = 0
        Rones = 0

        hundred = ["صد" , "دویست" , "سیصد" , "چهارصد" , "پانصد" , "ششصد" , "هفتصد " , "هشتصد" , "نهصد" ]
        tens = ["بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود","ده"]
        ones = [ "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه"]
        teens = [ "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده", "نوزده"]

        for i in text:
            if i in hundred:
                Rhundred += 1
            if i in tens:
                Rtens += 1
            if i in teens :
                Rteens += 1
            if i in ones:
                Rones += 1
        if Rhundred > 1 or Rones > 1 or Rteens> 1 or Rtens> 1 :
            self.dup = "yes"
        else:
            self.dup = "no"

    def results(self):
        s = " "
        if "میلیون" in self.text :
            self.Million_separator(self.text)
            million_str = s.join(self.Million)
            self.counter(million_str, 1000000)
            self.duplicate_error(self.Million)

        if "هزار" in self.text :
            self.Thousand_seprator(self.text)
            thousand_str = s.join(self.Thousand)
            self.counter(thousand_str, 1000)
            self.duplicate_error(self.Thousand)

        self.Hundred_seprator(self.text)
        hundred_str = s.join(self.Hundred)
        self.counter(hundred_str , 1)
        self.duplicate_error(self.Hundred)