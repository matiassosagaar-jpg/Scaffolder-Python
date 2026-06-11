#!/usr/bin/env python3
from pathlib import Path
import argparse
import shutil
def parse_file(text_file : Path, project_name):
    """Replaces all {{project_name}} in the textfile with the string passed"""
    target = "{{project_name}}"
    content = text_file.read_text() # store content in a string
    replaced_content = content.replace(target, project_name) # replacing all target ocurrences
    text_file.write_text(replaced_content) # replacing previous content in the file

def parse_files_r(root_folder : Path, project_name):
    """Parses recursively all the files from a root folder"""
    for element in root_folder.iterdir():
        if element.is_dir():
            parse_files_r(element, project_name)
        else:
            parse_file(element, project_name)

def remove_suffixes(root_folder : Path):
    """Removes all the suffixes from files recursively in a root directory"""
    for element in root_folder.iterdir():
        if element.is_dir():
            remove_suffixes(element)
        else:
            element.rename(element.with_name(element.stem)) # removing the last suffix
            #element.with_name returns the path of the element, replacing the element with the name "element.stem" which
            # is it's name without the last suffix, and rename changes the actual element to de path - string passed as argument
def main():
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parent
    parser.add_argument("project_name", nargs="?") #nargs="?" It can appear once or none
    parser.add_argument("-t", "--template", default="Basic") #stores a string, default value= "Basic"
    parser.add_argument("--templates", action="store_true") # if passed as argument, it stores true to de arg
    
    args = parser.parse_args()
    templates_dir = root / "templates"
    if args.templates:
        print("Available templates:")
        for folder in (templates_dir).iterdir():
            if folder.is_dir():
                print(f"- {folder.name}")
        return # We'll return, since this is an informative arg and shouldn't create folders
    
    if args.project_name == None:
        parser.print_usage()
        return # Print usage if no name or ifo argument is passed
    
    output_folder = Path.cwd()/args.project_name # cwd() returns the dir's absolute Path where the script is executed
    template_dir = templates_dir / args.template # The Path of the selected template directory
    if output_folder.exists():
        print(f'Folder "{args.project_name}" already exists in this directory')
        return
    elif not template_dir.exists():
        print(f'Template folder "{args.temp}" not found')
        return
    else:
        shutil.copytree(template_dir, output_folder)
        parse_files_r(output_folder, args.project_name)
        remove_suffixes(output_folder)
        print(f"Folder {args.project_name} created at {output_folder.parent}")
        return
        
if __name__ == "__main__":
    main()

    