from aibot import BOT


def main():
	my_bot = BOT()
	sentence = " اذان ظهر پس فردای تهران سردتر است یا نیمه شب شرعی ۳ روز بعد آن؟   "
	answer = my_bot.AIBOT(sentence)
	print(answer)


if __name__ == "__main__":
	main()
