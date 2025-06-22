import spacy 

TRANSCRIPT_PATH = "transcripts/sample_transcript.txt"

#load transcript text 

with open(TRANSCRIPT_PATH, "r", encoding ="utf-8") as f: 
    text = f.read()

    
#loading spispacy model 

nlp = spacy.load("en_core_sci_sm")
doc = nlp(text)

#print detected mdeical entities 
print("\n--- Extracted Medical Entities ---")
for ent in doc.ents: 
    print(f"{ent.text} ({ent.label_})")