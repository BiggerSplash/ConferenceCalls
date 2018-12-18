# Edit this file to add the filtering/subsetting:
# which transcripts to continue processing
import pandas as pd

from transcripts_metadata import OUTPUT_FILE_METADATA

df = pd.read_csv(OUTPUT_FILE_METADATA)

subset = df[
    df['Event.@eventTypeId'] == 1 # i.e. only conference calls
    # etc etc etc all the conditions
]

eventIds = subset['Event.@Id']

filenames = eventIds.astype('str') + '_T.xml'
