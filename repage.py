#!/usr/bin/env python3
import sys
import textwrap
import re
import html

_process = lambda text: '\n'.join(map(lambda x: ':  ' + x + ' ' * (wrap_width - len(x)) + '  :', text.split('\n')))
if len(sys.argv) <= 2:
    process = lambda text: html.escape(_process(text))
else:
    process = _process

def process_stream(wrap_width):
    paragraph = []
    
    raw_data = sys.stdin.buffer.read()

    try:
        data = raw_data.decode('utf-8')
    except UnicodeDecodeError:
        data = raw_data.decode('latin1', errors='replace')

    data = "\n" + data.strip() + "\n"
    for line in data.split("\n"):
        line = re.sub('\t','  ', line.rstrip())
        
        if '  --' in line or not line: 
            if paragraph:  # Process the previous paragraph
                text = textwrap.fill(' '.join(paragraph), width=wrap_width)
                print(process(text))
                paragraph = []
            line = textwrap.fill(line, width=wrap_width)
            print(process(line))
        else:
            paragraph.append(line.lstrip())  

    if paragraph:
        print(process(textwrap.fill(' '.join(paragraph), width=wrap_width)))

wrap_width = int(sys.argv[1] if len(sys.argv) > 1 else 80)
process_stream(wrap_width)

