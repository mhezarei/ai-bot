from AIBOT import BOT


def main():
	my_bot = BOT()
	# sentence = "قد من بلندتر است یا تو؟"
	sentence = "فردا هوای تهران ابری است؟"
	answer = my_bot.AIBOT(sentence)
	print(answer)


if __name__ == "__main__":
	main()
