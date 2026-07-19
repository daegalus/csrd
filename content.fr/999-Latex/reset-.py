current_filename = './CS-Book-fr.tex'
temp_filename = current_filename + '-new.tex'
with open(current_filename,'r', encoding='UTF-8') as current_file, open(temp_filename,'w',encoding='UTF-8',newline='') as temp_file:
    for line in current_file:
        pos = line.find('\\label{subsec:')
        if line.startswith('\\subsection') and pos > 0:
            prefix = line[0:pos]
            suffix = line[pos:]
            newline = prefix + suffix.replace('-','_')
        else:
            newline = line
        temp_file.writelines([newline])
