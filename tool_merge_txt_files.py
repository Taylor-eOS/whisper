import os
import re
import sys

INCLUDE_FILENAMES = len(sys.argv) > 1

def _natural_sort_key(s):
    parts = re.split(r'(\d+)', s)
    return [int(p) if p.isdigit() else p.lower() for p in parts]

def _list_txt_files(abs_folder, output_path):
    files = [
        f for f in os.listdir(abs_folder)
        if f.endswith('.txt')
        and not f.endswith('_merged.txt')
        and not f.endswith('requirements.txt')
        and os.path.abspath(os.path.join(abs_folder, f)) != output_path
    ]
    files.sort(key=_natural_sort_key)
    return files

def _read_and_clean(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    content = content.lstrip().rstrip('\n')
    return content if content else None

def merge_folder(abs_folder, output_path):
    txt_files = _list_txt_files(abs_folder, output_path)
    entries = []
    for filename in txt_files:
        file_path = os.path.join(abs_folder, filename)
        content = _read_and_clean(file_path)
        if content is None:
            continue
        entries.append((filename, content))
    return entries

def write_merged(output_path, entries):
    if not entries:
        return
    if INCLUDE_FILENAMES:
        blocks = [f'---{filename}\n\n{content}' for filename, content in entries]
    else:
        blocks = [content for filename, content in entries]
    joined_new = '\n\n'.join(blocks)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(joined_new)
        f.write('\n')

def main():
    target = input('Folder to merge (same): ') or "."
    abs_folder = os.path.abspath(target.strip())
    if not os.path.isdir(abs_folder):
        raise SystemExit(f'Not a directory: {target}')
    folder_name = os.path.basename(abs_folder.rstrip(os.sep)) or 'current'
    output_name = f'{folder_name}_merged.txt'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_name)
    entries = merge_folder(abs_folder, output_path)
    write_merged(output_path, entries)
    if entries:
        print(f'Wrote {output_path}')
    else:
        print('No content to merge')

if __name__ == '__main__':
    main()
