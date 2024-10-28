import os

#Merges the text files in the same folder into one file

txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
#txt_files.sort()
with open('merged_output.txt', 'w') as outfile:
    for i, filename in enumerate(txt_files):
        with open(filename, 'r') as infile:
            outfile.write(infile.read())
        if i < len(txt_files) - 1:
            outfile.write('\n\n-----\n\n')
