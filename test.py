import os
import re

data = {
    ".c":  r'#include\s*[<"]([^>"]+)[>"]',
    ".cpp": r'#include\s*[<"]([^>"]+)[>"]',
    ".h":  r'#include\s*[<"]([^>"]+)[>"]',
    ".hpp": r'#include\s*[<"]([^>"]+)[>"]',
    ".py": r'^\s*(?:from\s+([\w\.]+)\s+import\s+([\w\*,\s]+)|import\s+([\w\.]+(?:\s*,\s*[\w\.]+)*))',
    ".js": r'(?:import\s+(?:[\w\{\}\*\s,]+?\s+from\s+)?["\']([^"\']+)["\']|require\(["\']([^"\']+)["\']\))',
    ".ts": r'(?:import\s+(?:[\w\{\}\*\s,]+?\s+from\s+)?["\']([^"\']+)["\']|require\(["\']([^"\']+)["\']\))',
    ".java": r'^\s*import\s+([\w\.]+);',
    ".go": r'^\s*import\s*(?:\(\s*([\s\S]*?)\s*\)|"([^"]+)")',
    ".rs": r'^\s*(?:use\s+([\w\:]+)(?:\s+as\s+\w+)?\s*;|mod\s+([\w_]+)\s*;)',
    ".php": r'^\s*(?:use\s+([\w\\]+)\s*;|require(?:_once)?\s*\(?["\']([^"\']+)["\']\)?;|include(?:_once)?\s*\(?["\']([^"\']+)["\']\)?;)',
    ".cs": r'^\s*using\s+([\w\.]+);',
    ".sh": r'^\s*(?:source|\.)\s+([^\s]+)',
    ".md": r'!\[.*?\]\((.*?)\)|\[(.*?)\]\((.*?)\)|\{\{\s*include\s+["\'](.*?)["\']\s*\}\}',
    ".sql": r'^\s*\\i\s+([^\s;]+)|^\s*source\s+([^\s;]+)',
}

def generate_include(file_path: str) -> str:
    file_path = os.path.normpath(file_path)
    file_name, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # Convert path separators to module-style
    module_path = file_name.replace(os.sep, '.')

    # --- C / C++ ---
    if ext in ['.c', '.cpp', '.cc', '.cxx']:
        # Determine the matching header extension
        header_ext = '.hpp' if os.path.exists(file_name + '.hpp') else '.h'
        header_path = file_name + header_ext
        return f'#include "{header_path}"'

    # --- Header file itself ---
    elif ext in ['.h', '.hpp']:
        return f'// Header file: {os.path.basename(file_path)}'

    # --- Python ---
    elif ext == '.py':
        parts = module_path.split('.')
        if len(parts) > 1:
            module = parts[-1]
            parent = '.'.join(parts[:-1])
            return f'from {parent} import {module}'
        else:
            return f'import {module_path}'

    # --- JavaScript / TypeScript ---
    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        base = os.path.basename(file_name)
        return f'import {base} from "./{file_path}";'

    # --- Java ---
    elif ext == '.java':
        return f'import {module_path};'

    # --- Rust ---
    elif ext == '.rs':
        return f'mod {module_path.replace(".", "::")};'

    # --- Go ---
    elif ext == '.go':
        base = os.path.basename(file_name)
        return f'import "{base}"'

    # --- C# ---
    elif ext == '.cs':
        return f'using {module_path};'

    # --- Fallback ---
    else:
        return f'// Unsupported or unknown file type: {ext}'


def getFileNameList(Files : list) -> list[str]:
    name : list = []
    for file in Files:
        filename , extension = os.path.splitext(file)
        name.append(filename)
    return name

def replaceLinesWithWord(newline : str , targetWord  : str , filePath) -> list[str]:
    lines : list[str] = []
    with open(filePath , "r" , errors='ignore') as f:
        for line in f:
            if targetWord in line:
                lines.append(newline + "\n")
            else:
                lines.append(line)

    return lines



def changeIncludes():
    names : list = []
    for currentPath , dirsInCurrentPath , files  in os.walk(os.getcwd()):
        names .append( getFileNameList(files))


    for currentPath , dirsInCurrentPath , files  in os.walk(os.getcwd()):
        for file in files:
            filePath = os.path.join(currentPath , file) #get file path
            filename , fileExtension = os.path.splitext(file) #get filename and extension
            for name in names: #get a list of file names , find if a file name is is the match if yes then replace that line with new filepath
                newLine = generate_include(filePath)
                print(filePath)
                print (newLine)
                newFileContent : list[str] = replaceLinesWithWord( newLine, name , filePath)
                open(filePath , "w").close()
                with open(filePath , "a" ) as f:
                    for line in newFileContent:
                        f.write(line)



changeIncludes()
