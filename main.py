import time

from aibot import BOT


def main():
    start = time.time()

    my_bot = BOT()

    sentence = "ادان ظهر تهران کی است"
    answer, answer_sen = my_bot.AIBOT(sentence)
    # print(answer)
    # answer = my_bot.aibot('input.wav')

    print(answer)
    # print("final answer : " + answer_sen)

    end = time.time()
    print(f"Runtime of the program is {end - start}")


if __name__ == "__main__":
    main()
