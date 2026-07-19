focusfilename = 'C:/Users/Nicolas/Documents/GitHub/csrd/content.en/02-creating-your-character/04-focus.md'
focus_fr_filename='C:/Users/Nicolas/Documents/GitHub/csrd/content.fr/99-tempfiles/focus-fr.txt'

with open(focusfilename, 'r') as focusfile:
    with open(focus_fr_filename,'w',newline=None) as focus_fr_file:
        for line in focusfile:
            if line.startswith('### '):
                print(line.replace('### ',''),file=focus_fr_file)
