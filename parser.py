import os
import pandas as pd

def parse_transcripts(filepath):

    filename=os.path.basename(filepath)
    parts=filename.replace(".txt","").split("_")
  
    speaker_id=parts[1]
    task=parts[2]
    
    stutter_types = {"B", "IN", "PR", "SR", "WR"}
    

    with open(filepath,"r") as f:
        lines=[l.strip() for l in f if l.strip()]

    records=[]

    i=0
    while i< len(lines):
        cols=lines[i].split()
        if len(cols)<3:
            i+=1
            continue
        

        try:
            start=float(cols[0])
            end=float(cols[1])
        except ValueError:
            i+=1
            continue




        token = cols[2].upper().rstrip("0123456789")  

       
        if token in stutter_types:
            stutter_type = token

            
            if i + 1 < len(lines):
                next_cols = lines[i + 1].split()
                if len(next_cols) >= 3:
                    try:
                        float(next_cols[0])
                        float(next_cols[1])

                        
                        word_parts = next_cols[2:]
                        if word_parts and word_parts[-1].upper().rstrip("0123456789") in stutter_types:
                            word_parts = word_parts[:-1]
                        word = " ".join(word_parts).strip()

                        records.append({
                            "speaker_id": speaker_id,
                            "task": task,
                            "start_time": start,
                            "end_time": end,
                            "duration": round(end - start, 3),
                            "stutter_type": stutter_type,
                            "word": word,
                            "is_disfluent": True
                        })
                        i += 2  
                        continue
                    except ValueError:
                        pass

        
        else:
            word = " ".join(cols[2:]).strip()
            records.append({
                "speaker_id": speaker_id,
                "task": task,
                "start_time": start,
                "end_time": end,
                "duration": round(end - start, 3),
                "stutter_type": "NONE",
                "word": word,
                "is_disfluent": False
            })

        i += 1

    return records


all_records=[]
transcripts_dir=r"C:\Users\Nazneen\disf\boli-dataset\Transcripts"

for fname in os.listdir(transcripts_dir):
    if fname.endswith(".txt"):
        all_records.extend(parse_transcripts(os.path.join(transcripts_dir,fname)))


df=pd.DataFrame(all_records)
df["word"] = df["word"].str.replace("_", " ")


def fix_stutter_type(row):
    if row["is_disfluent"] == False:
        parts = str(row["word"]).split()
        
        if len(parts) >= 2 and parts[0].lower() == parts[1].lower():
            row["stutter_type"] = "SR"
            row["is_disfluent"] = True
    return row

df = df.apply(fix_stutter_type, axis=1)

df.to_csv("disfluency_data.csv", index=False)
print("Saved",len(df))
print(df.head(20))
print(f"Total disfluency events:{len(df)}")