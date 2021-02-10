from aibot import BOT


def main():
    my_bot = BOT()
    sentence = 'امسال جشن سده در کدام روز است؟    '
    answer = my_bot.AIBOT(sentence)
    print(answer)


if __name__ == "__main__":
    main()
