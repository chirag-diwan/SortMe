from openai import OpenAI
import re
import json

lsoutput = input()

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

print (json.dumps(data , indent=4))
