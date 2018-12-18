o1 = transcripts/output/transcripts_metadata.csv
o2 = transcripts/output/transcripts_filtered_body.csv
o3 = transcripts/output/speech.csv
o4 = transcripts/output/participants.csv
o5 = transcripts/output/log_unparseable.csv

s1 = transcripts_metadata.py
s2 = transcripts_body.py
s3 = transcripts_parse_body.py

.PHONY: all clean

all: $(o1) $(o2) $(o3) $(o4) $(o5)

clean: 
	rm -f transcripts/output/*.csv

$(o1): $(s1)
	@echo :Storing metadata from raw transcripts
	python transcripts_metadata.py

$(o2): $(o1) $(s2)
	@echo :Storing text body for transcripts based on filter \
		[transcripts_filter_on_metadata.py]
	python transcripts_body.py

$(o3) $(o4) $(o5): $(o2) $(s3)
	@echo :Parsing individual transcripts [speech/participants/log_unparseable]
	python transcripts_parse_body.py

