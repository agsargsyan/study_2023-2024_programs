all:  clean run plot

run:
	sudo python main.py

plot: 
	sudo python all.py
	sudo python queue.py
	gnuplot plots.plt

clean:
	sudo rm -f *.dat *.pdf *.json *.csv *.txt
	sudo rm -rf results/*
	sudo rm -rf output/*
	sudo mn -c
