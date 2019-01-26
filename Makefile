.PHONY: clean

FILE="src/network_vis.py"
OUT="temp-plot.html"

all:
	sudo python3 $(FILE)
	#open $(OUT)

