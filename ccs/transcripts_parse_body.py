# Based on the format in '1000326_T.xml', all other will be ignored
# Parse the transcripts into:
# 1) a csv with participants
# 2) a csv with speech
# 3) a csv with log of transcripts that were not successfully parsed

import re
import numpy as np
import pandas as pd
from collections import defaultdict

from transcripts_body import OUTPUT_FILE_FILTERED_BODY

OUTPUT_FILE_LOG = 'transcripts/output/log_unparseable.csv'
OUTPUT_FILE_PARTICIPANTS = 'transcripts/output/participants.csv'
OUTPUT_FILE_SPEECH = 'transcripts/output/speech.csv'


def parse_participants(text, regex):
    found = defaultdict(list)
    participants = re.findall(regex, text, flags = re.DOTALL)

    if not participants:
        return None

    for participant in participants[0].split('*')[1:]:
        name_affils = [s.strip() for s in participant.strip().split('\n')]
        if len(name_affils) != 2:
            # If either of name or affiliation unparsable, set to missing
            name, affil = np.nan, np.nan
        else:
            name, affil =   name_affils
        found['name'].append(name)
        found['affiliation'].append(affil)

    out = pd.DataFrame(found)

    # If all names or affiliations missing, recorded as unparseable
    if any(out.isnull().all()):
        return None

    return out


def parse_section(text, regex):

    found = defaultdict(list)
    # this is the "name, affil [block number]" before participant speech
    blocknr_regex = r'\[(\d+)\]\n'

    sec = re.findall(regex, text, flags=re.DOTALL)

    if not sec:
        return None

    seclist = sec[0].split('-' * 80)[1:]

    for idx, val in enumerate(seclist):
        block_number =  re.findall(blocknr_regex, val)
        if not block_number:
            continue

        # looks like  "first last, affiliation bla, bla  [n]"
        name_affil = re.sub(blocknr_regex, '', val
                           ).replace('\n', '').strip().split(',', maxsplit=1)

        if 'Operator' in name_affil:
            continue

        name = name_affil[0].strip()
        if len(name_affil) != 2:
            affil = np.nan
        else:
            affil = name_affil[1].strip()

        speech = seclist[idx + 1].replace('\n', '').strip()

        found['block_number'].append(block_number[0])
        found['name'].append(name)
        found['affiliation'].append(affil)
        found['speech'].append(speech)

    if not found:
        return None

    return pd.DataFrame(found)


def write_results(frame, filename):
    with open(filename, 'a') as f:
            header = f.tell() == 0
            frame.to_csv(f, header=header, index=False, na_rep='NA')


def log_unparseable(eventId):
    f = pd.DataFrame({'Event.@Id': [eventId]})
    write_results(f, OUTPUT_FILE_LOG)


if __name__ == '__main__':

    # chunks can be run in parallell
    chunksize = 10**3
    for chunk in pd.read_csv(OUTPUT_FILE_FILTERED_BODY,
                             chunksize = chunksize):

        for idx, row in chunk.iterrows():

            eventId = row['Event.@Id']
            text = row['Event.EventStory.Body']
            text = text.replace('&amp;', '&')

            # Participants
            regex = r'Corporate Participants.*?(\*.*?(?=\n\=))'
            frame_corporate = parse_participants(text, regex)

            regex = r'Conference Call Participants.*?(\*.*?(?=\n\=))'
            frame_cc =  parse_participants(text, regex)

            if frame_corporate is None or frame_cc is None:
                log_unparseable(eventId)
                continue

            frame_corporate['type'] = 'Corporate'
            frame_cc['type'] = 'Analyst'
            out_participants = pd.concat([frame_corporate, frame_cc])
            out_participants['Event.@Id'] = eventId

            # Speech
            regex = r'Presentation.*?(?=\n\=)'
            pres = parse_section(text, regex)

            regex = r'Questions and Answers.*'
            qanda = parse_section(text, regex)

            # transcripts with no QandA part will be disregarded
            if pres is None or qanda is None:
                log_unparseable(eventId)
                continue

            pres['section'] = 'Presentation'
            qanda['section'] = 'QandA'
            out_speech = pd.concat([pres, qanda])
            out_speech['Event.@Id'] = eventId
            columns_reordered = out_speech.columns.difference(['speech']).tolist()
            columns_reordered.append('speech')

            write_results(out_participants, OUTPUT_FILE_PARTICIPANTS)
            # This file will grow big, can use another light format that has an index
            write_results(out_speech[columns_reordered], OUTPUT_FILE_SPEECH)
