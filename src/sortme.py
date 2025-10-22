#!/usr/bin/env python3

from openai import OpenAI
import re
import json
import os
import shutil
from editFiles import changeIncludes
import sys


wrkDir = os.getcwd()
if(len(sys.argv) == 1):
    print("Please Provide a valid OpenAI AIP Key")
    sys.exit()
elif(len(sys.argv) == 3):
    wrkDir = sys.argv[3]
    
lsoutput = os.listdir(wrkDir)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=sys.argv[1],
)

completion = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You Have To provide me with exactly what is being asked from you. No extras, no introduction."
        },
        {
            "role": "user",
            "content": f"{lsoutput}\nGiven the following list of files, generate a project folder structure that is logical, easy to navigate, and makes the purpose of each file immediately clear. Organize the following files into a nested folder structure. Each folder should have a key 'files' with a list of its files. Subfolders should appear as keys inside their parent folder. Respond only in JSON, no extra text or explanations."
        }
    ]
)

rawData : str = str(completion.choices[0].message.content)
cleaned = re.sub(r"^```json\s*|```$", "", rawData, flags=re.MULTILINE).strip()

# Parse string into dict
data = json.loads(cleaned)


def jsonDFS(Data , rootFolder):
    files = Data.get('files' , [])
    for file in files:
        src_path = os.path.join(os.getcwd() , file)
        dest_path = rootFolder
        shutil.move(src_path , dest_path)

    for key , value in Data.items():
        keyFolder = os.path.join(rootFolder , key)
        if key == "files":
            continue

        try:
            os.makedirs(keyFolder , exist_ok=True)
        except Exception as e:
            print(e)

        if isinstance(value , dict):
            jsonDFS(value , keyFolder)



jsonData = json.dumps(data , indent=4)
print(jsonData)
jsonDFS(data , os.getcwd())

changeIncludes()
