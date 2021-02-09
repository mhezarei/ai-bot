from aibot import BOT


def main():
    my_bot = BOT()
    sentence = "مناسبت روز 18 اسفند امسال و 12 مهر سال بعد چیست؟"
    answer = my_bot.AIBOT(sentence)
    print(answer)


if __name__ == "__main__":
    main()
