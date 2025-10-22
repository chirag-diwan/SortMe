import os , re

data = {
    ".c": "#include",
    ".cpp": "#include",
    ".h": "#include",
    ".hpp": "#include",
    ".py": "import",
    ".js": "import",
    ".ts": "import",
    ".java": "import",
    ".go": "import",
    ".rs": "use",
    ".php": "include",
    ".cs": "using",
    ".sh": "source",
    ".md": "include",
    ".sql": "source",
}


regexPatterns = {
    ".c":    r'#include\s*[<"]([^>"]+)[>"]',                # captures what's inside quotes or <>
    ".cpp":  r'#include\s*[<"]([^>"]+)[>"]',
    ".h":    r'#include\s*[<"]([^>"]+)[>"]',
    ".hpp":  r'#include\s*[<"]([^>"]+)[>"]',
    ".py":   r'^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.]+))',  # group(1) or group(2)
    ".js":   r'^\s*(?:import\s+(?:[\w\{\}\*\s,]+\s+from\s+)?["\']([^"\']+)["\']|require\(["\']([^"\']+)["\']\))',
    ".ts":   r'^\s*(?:import\s+(?:[\w\{\}\*\s,]+\s+from\s+)?["\']([^"\']+)["\']|require\(["\']([^"\']+)["\']\))',
    ".java": r'^\s*import\s+([\w\.]+);',
    ".go":   r'^\s*(?:"([^"]+)"|import\s*\(\s*((?:"[^"]+"\s*)+)\s*\))',  # capture single import or list of imports
    ".rs":   r'^\s*(?:use\s+([\w\:]+)|mod\s+([\w_]+))',
    ".php":  r'^\s*(?:use\s+([\w\\]+)|require(?:_once)?\s*\(?["\']([^"\']+)["\']\)?|include(?:_once)?\s*\(?["\']([^"\']+)["\']\)?)',
    ".cs":   r'^\s*using\s+([\w\.]+);',
    ".sh":   r'^\s*(?:source|\.)\s+([^\s]+)',
    ".md":   r'\{\{\s*include\s+["\'](.*?)["\']\s*\}\}',      # capture included filename
    ".sql":  r'^\s*(?:\\i\s+|source\s+)([^\s;]+)',
}




def generate_include(file_path: str) -> str:
    file_path = os.path.normpath(file_path)
    ext = os.path.splitext(file_path)[1].lower()

    file_name_with_ext = os.path.basename(file_path)                 # e.g. math.cpp
    file_name_no_ext = os.path.splitext(file_name_with_ext)[0]       # e.g. math
    file_dir = os.path.dirname(file_path)                            # e.g. src/utils
    module_path = file_path.replace(os.sep, '.')                     # e.g. src.utils.math.cpp

    if ext in ['.c', '.cpp', '.cc', '.cxx']:
        header_ext = '.hpp' if os.path.exists(os.path.join(file_dir, file_name_no_ext + '.hpp')) else '.h'
        return f'#include "{file_dir}/{file_name_no_ext}{header_ext}"'

    elif ext in ['.h', '.hpp']:
        return f'// Header file: {file_name_with_ext}'

    elif ext == '.py':
        rel_path = os.path.relpath(file_path, os.getcwd())  
        rel_no_ext = os.path.splitext(rel_path)[0]
        module_path = rel_no_ext.replace(os.sep, '.')

        if '.' in module_path:
            parent, mod = module_path.rsplit('.', 1)
            return f'from {parent} import {mod}'
        else:
            return f'import {module_path}'


    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        return f'import {file_name_no_ext} from "./{file_path}";'

    elif ext == '.java':
        return f'import {module_path};'

    elif ext == '.rs':
        return f'mod {file_name_no_ext};'

    elif ext == '.go':
        return f'import "{file_name_no_ext}"'

    elif ext == '.cs':
        return f'using {module_path};'

    return f'// Unsupported or unknown file type: {ext}'


def getNameToPath() -> dict[str , str]:
    namePath : dict [str , str] = {}
    for currentPath, dirs, files in os.walk(os.getcwd()):
        for file in files:
            filePath = os.path.join(currentPath , file)
            #file == name 
            _bufName , _bufExt = os.path.splitext(file)
            namePath[_bufName] = filePath
    return namePath

    

def getFileNameList(Files : list) -> list[str]:
    name : list = []
    for file in Files:
        name.append(file)
    return name

def replaceLinesWithWord(newline : str , targetWord  : str , filePath) -> list[str]:
    lines : list = []
    filename , extension = os.path.splitext(filePath)
    with open(filePath , "r" , errors='ignore') as f:
            for line in f:
                if targetWord in line:
                        lines.append(newline + "\n")
                else:
                    lines.append(line)

    return lines



def changeIncludes():
    name_path : dict = getNameToPath()
    all_files : list[str] = []

    for currentPath, dirs, files in os.walk(os.getcwd()):
        for file in files:
            all_files.append(os.path.join(currentPath, file))

    for filePath in all_files:
        with open(filePath , "r") as file:
            n , ext = os.path.splitext(filePath)
            for line in file:
                if data[ext] in line: 
                    #data[ext] is a import keyword
#                    regex = regexPatterns[ext]

                    regex = regexPatterns[ext] if ext in regexPatterns else "Unsupported file"

                    match = re.match(regex ,line)
                    if match:
                        input_name = match.group(1) or match.group(2)
                        if input_name in name_path.keys():
                            newDir = name_path[input_name]
                            newLine = generate_include(newDir)
                            newFileContent = replaceLinesWithWord(newLine, n , filePath)
                            open(filePath , "w" , errors='ignore').close()
                            with open(filePath , "a" , errors='ignore') as f:
                                for line in newFileContent:
                                    f.write(line)
