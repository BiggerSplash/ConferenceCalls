.PHONY: all ccs corpus lda clean

all: ccs corpus lda

ccs:
	$(MAKE) --directory=ccs

corpus:
	$(MAKE) --directory=corpus

lda:
	$(MAKE) --directory=lda

clean:
	$(MAKE) --directory=ccs clean
	$(MAKE) --directory=corpus clean
	$(MAKE) --directory=lda clean
