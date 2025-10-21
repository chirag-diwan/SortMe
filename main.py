from openai import OpenAI
import re
import json
import os
import shutil


lsoutput = input()
currentDirectory = input()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
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

def jsonDFS(data , rootPath):
    if isinstance(data , dict):
        for key,value in data:
            folder_path = rootPath + "/" + key
            if isinstance(value , (dict , list)):
                try:
                    os.mkdir(folder_path)
                except Exception as e:
                    print("Error :: " , {e})
                    jsonDFS(value , folder_path)
            else:
                try:
                    os.mkdir(folder_path)
                except Exception as e:
                    print("Error :: " , {e})
                shutil.move(os.path.abspath(value) , folder_path + value)

    elif isinstance(data , list):
        for i , item in enumerate(data):
            if isinstance(item , (dict , list)):
                jsonDFS(item , rootPath)
            else:
                shutil.move(os.path.abspath(item) , rootPath + item)


jsonData = json.dumps(data , indent=4)
jsonDFS(jsonData , os.getenv("CURRENTDIRECTORY"))
