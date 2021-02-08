from aibot import BOT


def main():
    my_bot = BOT()
    sentence = "ساعت در پایتخت ایران چند است؟  "
    answer = my_bot.AIBOT(sentence)
    print(answer)


if __name__ == "__main__":
    main()
