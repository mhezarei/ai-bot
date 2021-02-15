import time

from aibot import BOT


def main():
    start = time.time()

    my_bot = BOT()

    sentence = "امروز ساعت دو و نیم بعد از ظهر هوای تهران سردتر است یا فردا ساعت سه و نیم بامداد؟  "
    answer = my_bot.AIBOT(sentence)

    # answer = my_bot.aibot('input.wav')

    print(answer)

    end = time.time()
    print(f"Runtime of the program is {end - start}")


if __name__ == "__main__":
    main()
