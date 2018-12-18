o1 = output/corpus.csv
s1 = corpus_create.py
s2 = ../ccs/transcripts/output/speech.csv

.PHONY: all clean

all: $(o1)

clean:
	rm -f output/*.csv

$(o1): $(s1) $(s2)
	@echo :Creating corpus
	python corpus_create.py

