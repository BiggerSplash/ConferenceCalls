Content: individual Thomson Reuters xml transcript files *xxxxxx_T.xml*

Start with for example 1000 random transcripts with:
```bash
N=1000
TFILE=pathToTranscriptZip

zipinfo -1 $TFILE | gshuf | head -n $N | \
  xargs -I file unzip -j $TFILE file -d raw/
```
