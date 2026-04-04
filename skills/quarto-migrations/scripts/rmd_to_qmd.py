#!/usr/bin/env python3
import sys
import os
import re

def convert_rmd_to_qmd(file_path):
    if not file_path.endswith('.Rmd'):
        print(f"Skipping {file_path}: not an .Rmd file.")
        return

    new_file_path = file_path[:-4] + '.qmd'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update YAML: output -> format
    content = re.sub(r'^output:', 'format:', content, flags=re.MULTILINE)
    
    # 2. Update chunk options: dots to dashes and comma-separated to hashpipe
    # Pattern to find chunks: ```{r label, opt1=val1, opt2=val2}
    def replace_chunk(match):
        header = match.group(1)
        body = match.group(2)
        
        # Split header into engine and options
        parts = [p.strip() for p in header.split(',')]
        engine_info = parts[0] # e.g., "r label" or just "r"
        options_list = parts[1:] # e.g., ["echo=FALSE", "fig.cap='Caption'"]
        
        new_header = f"```{{{engine_info.split()[0]}}}"
        hashpipes = []
        
        # Handle label in parts[0] if exists
        engine_parts = engine_info.split()
        if len(engine_parts) > 1:
            label = engine_parts[1]
            hashpipes.append(f"#| label: {label}")
        
        for opt in options_list:
            if '=' in opt:
                key, val = opt.split('=', 1)
                key = key.strip().replace('.', '-')
                val = val.strip()
                # Remove quotes if they are already there for simple strings? 
                # Actually Quarto YAML prefers them for some things but not all.
                hashpipes.append(f"#| {key}: {val}")
            else:
                # Handle cases without = (e.g., label)
                key = opt.strip().replace('.', '-')
                hashpipes.append(f"#| {key}")
        
        if hashpipes:
            return f"{new_header}\n" + "\n".join(hashpipes) + "\n" + body
        else:
            return f"{new_header}\n" + body

    content = re.sub(r'```\{(.*?)\}\n(.*?)(?=\n```)', replace_chunk, content, flags=re.DOTALL)
    
    # 3. Individual dot-to-dash conversions for common options not in chunks
    content = content.replace('fig.cap', 'fig-cap')
    content = content.replace('fig.width', 'fig-width')
    content = content.replace('fig.height', 'fig-height')
    content = content.replace('fig.align', 'fig-align')
    
    with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Converted {file_path} to {new_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rmd_to_qmd.py <file.Rmd>")
        sys.exit(1)
        
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            convert_rmd_to_qmd(arg)
        elif os.path.isdir(arg):
            for root, dirs, files in os.walk(arg):
                for file in files:
                    if file.endswith('.Rmd'):
                        convert_rmd_to_qmd(os.path.join(root, file))
