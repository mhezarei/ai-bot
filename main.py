from aibot import BOT


def main():
    my_bot = BOT()
    sentence = 'دمای هوای امروز شیراز ساعت ۱۴:۲۵ چقدر است؟   '
    answer = my_bot.AIBOT(sentence)
    print(answer)


if __name__ == "__main__":
    main()
