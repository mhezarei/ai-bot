import time

from aibot import BOT


def main():
    start = time.time()

    my_bot = BOT()

    sentence = "اذان صبح در شهر گم در ۳ دی چه زمانی است؟"
    answer = my_bot.AIBOT(sentence)

    # answer = my_bot.aibot('input.wav')

    print(answer)

    end = time.time()
    print(f"Runtime of the program is {end - start}")


if __name__ == "__main__":
    main()
