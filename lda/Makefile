o1 = output/lda.pkl
o2 = output/countvec.pkl
s1 = lda_fit.py
s2 = ../corpus/output/corpus.csv

.PHONY: all clean

all: $(o1) $(o2)

clean:
	rm -f output/*.pkl

$(o1) $(o2): $(s1) $(s2)
	@echo :Fitting LDA
	python lda_fit.py


