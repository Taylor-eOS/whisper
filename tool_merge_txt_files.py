import os
import re
import sys

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

def _write_merged(output_path, joined_new):
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        with open(output_path, 'r', encoding='utf-8') as f:
            prev = f.read()
        prev = prev.rstrip('\n')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prev)
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write('\n\n-----\n\n')
            f.write(joined_new)
            f.write('\n')
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(joined_new)
            f.write('\n')

def merge_txt_files(folder):
    folder = folder.lstrip() if folder else '.'
    abs_folder = os.path.abspath(folder)
    if not os.path.isdir(abs_folder):
        raise SystemExit(f'Not a directory: {folder}')
    folder_name = os.path.basename(abs_folder.rstrip(os.sep)) or 'current'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, f'{folder_name}_merged.txt')
    txt_files = _list_txt_files(abs_folder, output_path)
    new_blocks = []
    for filename in txt_files:
        file_path = os.path.join(abs_folder, filename)
        content = _read_and_clean(file_path)
        if content:
            new_blocks.append(content)
    if not new_blocks:
        return
    joined_new = '\n\n-----\n\n'.join(new_blocks)
    _write_merged(output_path, joined_new)

def main():
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        try:
            folder = input('Folder (press Enter for "."): ')
        except EOFError:
            folder = ''
        except KeyboardInterrupt:
            raise SystemExit
    merge_txt_files(folder)

if __name__ == '__main__':
    main()

