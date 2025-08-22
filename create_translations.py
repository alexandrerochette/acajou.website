import os
import glob
import csv
from pathlib import Path

def find_all_files_recursive(directory_path, condition= lambda x: True):
    """
    Finds and returns a list of all file paths within a given directory
    and its subdirectories.
    """
    all_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if condition(file):

                full_path = os.path.join(root, file)
                all_files.append(full_path)
    return all_files

def get_translation_paths():
    """
        returns all translation mapping found from current config

        Returns:
            path to config mapping tsv file
    """
    result = []
    for file in glob.glob("translations/*.tsv"):
        result.append(file)

    return result

def locale_from_path(path):
    filename_with_ext = os.path.basename(path)
    filename_without_ext = os.path.splitext(filename_with_ext)[0]
    return  filename_without_ext

def load_translation_mapping(path):
    result = {}
    with open(path) as inputf:
        reader = csv.reader(inputf, delimiter="\t")
        for row in reader:
            if len(row) > 1:
                result[row[0]] = row[1]
    return result

def try_make_dir(path):
    try:
        print(path)
        os.makedirs(path)
    except FileExistsError:
        pass

def create_translations():
    root_path = 'source'
    output_path = 'docs'
    localization_paths = get_translation_paths()
    for path in localization_paths:
        locale = locale_from_path(path)
        locale_path = os.path.join(output_path, locale)
        try_make_dir(locale_path)



    all_source_files = find_all_files_recursive(root_path)
    for source_path in all_source_files:
        
        source_file_path = Path(source_path)
        # To get the path relative to its anchor (e.g., '/')
        source_file = source_file_path.relative_to(root_path) 
        out_directory = os.path.join(output_path, source_file.parent)
        try_make_dir(out_directory)
        with open(os.path.join(root_path, source_file), "rb") as inputf, open(os.path.join(output_path, source_file), "wb") as outf:
          
            outf.write(inputf.read())
           
        if  source_file.suffix == '.html':   
                print(f"Translating source: {source_file}")
            
                for path in localization_paths:
                    locale = locale_from_path(path)
                    mappings = load_translation_mapping(path)
                    locale_path = os.path.join(root_path, locale)
                    out_directory = os.path.join(output_path, locale, source_file.parent)
                    try_make_dir(out_directory)
                    with open(os.path.join(root_path, source_file), "r", encoding="utf-8") as inputf, open(os.path.join(output_path, locale, source_file), "w", encoding="utf-8") as outf:
                        all_input_text = inputf.read()
                   
                        for mapping_key in sorted(mappings, key= len, reverse=True):
                            source_text = mapping_key
                            translated_text = mappings[mapping_key]
                            if translated_text != "":
                                all_input_text2 = all_input_text.replace(source_text, translated_text)
                                if all_input_text2 != all_input_text:
                                    print('  ', source_text, '-->', translated_text)
                                    all_input_text = all_input_text2
                        outf.write(all_input_text)


if __name__ == '__main__':
    create_translations()

