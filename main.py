import time

from aibot import BOT



def main():

    start = time.time()

    my_bot = BOT()

    # sentence = 'دمای هوای امروز شیراز ساعت ۱۴:۲۵ چقدر است؟   '
    # answer = my_bot.AIBOT(sentence)

    answer = my_bot.aibot('input.wav')
    
    print(answer)

    end = time.time()
    print(f"Runtime of the program is {end - start}")


if __name__ == "__main__":
    main()
