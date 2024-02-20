display:
	python3 src/main/Main.py -d

game:
	python3 src/main/Main.py

tests:
	python3 test/card/CardTest.py
	@echo "\n"
	python3 test/card/QuestTest.py
	@echo "\n"
	python3 test/game/BoardClassicalTest.py
	@echo "\n"
	python3 test/player/PlayerTest.py