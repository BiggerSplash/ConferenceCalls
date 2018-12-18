# Read in and story the body of each transcript in a big CSV
# Based on the filtered filenames in
# 'transcripts_filter_on_metadata.py'
import os
import pandas as pd
import xmltodict

from transcripts_filter_on_metadata import filenames

TRANSCRIPT_DIR = 'transcripts/raw/'
OUTPUT_FILE_FILTERED_BODY = 'transcripts/output/transcripts_filtered_body.csv'

def write_results(frame, filename):
    with open(filename, 'a') as f:
            header = f.tell() == 0
            frame.to_csv(f, header=header, index=False, na_rep='NA')

if __name__ == '__main__':
    path = TRANSCRIPT_DIR

    body_columns = ['Event.@Id', 'Event.EventStory.Body']

    for filename in filenames:
        with open("{0}/{1}".format(path, filename), 'r') as file:
            parsed = xmltodict.parse(file.read())
            frame = pd.io.json.json_normalize(parsed)
            # Write results as we go as the file may grow very large
            write_results(frame[body_columns], OUTPUT_FILE_FILTERED_BODY)
