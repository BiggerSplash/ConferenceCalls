# Read in and parse metadata of all raw transcript
import os
import pandas as pd
import xmltodict

TRANSCRIPT_DIR = 'transcripts/raw/'
OUTPUT_FILE_METADATA = 'transcripts/output/transcripts_metadata.csv'

if __name__ == '__main__':
    path = TRANSCRIPT_DIR

    frames_metadata = []
    body_column = ['Event.EventStory.Body']
    filenames = os.listdir(path)

    for filename in filenames:
        if filename.endswith('.xml'):
            with open("{0}/{1}".format(path, filename), 'r') as file:
                parsed = xmltodict.parse(file.read())
                frame = pd.io.json.json_normalize(parsed)
                frames_metadata.append(
                    frame[frame.columns.difference(body_column)]
                )

    pd.concat(frames_metadata).to_csv(OUTPUT_FILE_METADATA, index=False)
