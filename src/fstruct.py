from openai import OpenAI
import re
import json
import os
import shutil
import sys

def getKey():
    KEY : str = ""
    keyFilePath = os.path.join("../" , "data/APIKEY.txt")


    if os.path.exists(keyFilePath):
        with open(keyFilePath , "r") as f:
            for line in f :
                if (line != "" or " "):
                    key=line
    else:
        if(len(sys.argv) == 1):
            print("Please Provide a valid OpenAI AIP Key")
            sys.exit()
        KEY=sys.argv[1]
        with open(keyFilePath , "w") as f:
            f.write(KEY)

def getworkingDir():
    if(len(sys.argv) == 3):
        wrkDir = sys.argv[2]
        return wrkDir
    return os.getcwd()

    
def getFolderStruct():
    wrkDir = getworkingDir()
    open(os.path.join("../" , "data/OLDFILEPATH.txt") , "w").close() # reset the file 
    f = open(os.path.join("../" , "data/OLDFILEPATH.txt") , "a")
    lsoutput : dict = {}
    for currentpath , dirs , files in os.walk(wrkDir):
        lsoutput[currentpath] = [dirs , files]
        for file in files:
            f.write(file + ":" + currentpath)
    f.close()

    #lsoutput = os.listdir(wrkDir)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=getKey(),
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
    
    data = json.loads(cleaned)
    return data


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



def makeDirs():
    data = getFolderStruct()
    jsonDFS( data , getworkingDir())
    jsonData = json.dumps(data , indent=4)
    print(jsonData)
