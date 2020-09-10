from pathlib import Path
import os
import re

# https://stackoverflow.com/a/4665027
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def rewrite_or_delete(fn):
    try:
        text = Path(fn).read_text()
    except:
        os.remove(fn)
        return

    # remove comments. no this isn't perfect.
    text = re.sub(r'(?<!\\)%[^\n]*(?=\n|$)', '', text)

    section_ixes = list(find_all(text, '\\section{'))
    if section_ixes and text[section_ixes[0]:].startswith('\\section{Intro'):
        if len(section_ixes) >= 2:
            text = text[section_ixes[1]:]
        else:
            text = ''
    section_ixes = list(find_all(text, '\\section{'))
    if section_ixes and text[section_ixes[-1]:].startswith('\\section{Conc'):
        text = text[:section_ixes[-1]]
    if '\\begin{document}' in text:
        text = text[text.index('\\begin{document}')+len('\\begin{document}'):]
    if '\\end{document}' in text:
        text = text[:text.index('\\end{document}')]

    if (('proof' in text and ('theorem' in text or 'lemma' in text))
        or '\\begin{proof}' in text
    ):
        with open(fn, 'w') as f:
            f.write(text)
            return fn
    else:
        os.remove(fn)

