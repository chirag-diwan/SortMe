import os


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

    return ""


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
    all_files : list[str] = []

    for currentPath, dirs, files in os.walk(os.getcwd()):
        for file in files:
            all_files.append(os.path.join(currentPath, file))

    oldFilePaths : dict = {}
    with open("../data/OLDFILEPATH.txt" , "r" , errors='ignore') as f:
        for line in f:
            fileName , fileOldPath = line.split(":")
            oldFilePaths[fileName] = fileOldPath

    print(oldFilePaths)

    includeDict : dict [str , str] = {}

    for newfilePath in all_files:
        fileName = os.path.basename(newfilePath)
        oldpath = oldFilePaths[fileName].strip()
        oldInclude = generate_include(oldpath)
        newInclude = generate_include(newfilePath)
        if oldInclude != "" and newInclude != "":
            includeDict[oldInclude] = newInclude

    for file_path in all_files:
        with open(file_path , "r+" , errors='ignore') as f:
            fileContent:str = f.read()
            for oinc , ninc in includeDict.items():
                fileContent.replace(oinc , ninc , 999)
