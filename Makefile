.PHONY: clean

FILE="src/lib/main.py"
OUT="out/call_network.html"

all:
	sudo python3 $(FILE)
	open $(OUT)

