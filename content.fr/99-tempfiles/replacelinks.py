import json,uuid,os
from pathlib import Path

frjsonfilename = 'C:\\Users\\Nicolas\\Documents\\GitHub\\nikofrom94.github.io\\db\\og-csrd-fr.json'
enjsonfilename = 'C:\\Users\\Nicolas\\Documents\\GitHub\\nikofrom94.github.io\\db\\og-csrd.json'

#indexfilename = 'C:\\Users\\Nicolas\\Documents\\GitHub\\nikofrom94.github.io\\index-fr.html'
indexfilename = 'C:\\Users\\Nicolas\\Documents\\GitHub\\nikofrom94.github.io\\og-cspg-fr.html'

with open(frjsonfilename, 'r', encoding='utf8') as frjsonfile, open(enjsonfilename, 'r', encoding='utf8') as enjsonfile:
    frjson = json.load( frjsonfile )
    enjson = json.load( enjsonfile )

descriptor_links = {}
for en_descriptor_link in enjson["characterdescriptor"]:
    a_left = en_descriptor_link[en_descriptor_link.find('<'):en_descriptor_link.find('>')]
    for fr_descriptor_link in frjson["characterdescriptor"]:
        if a_left in fr_descriptor_link:
            descriptor_links[en_descriptor_link[en_descriptor_link.find('<'):en_descriptor_link.rfind('>')+1].replace('\'','"')] = fr_descriptor_link.replace('\'','"')[0:fr_descriptor_link.find(" <span c")].strip()

focus_links = {}
for en_focus_link in enjson["characterfocus"]:
    a_left = en_focus_link[en_focus_link.find('<'):en_focus_link.find('>')]
    for fr_focus_link in frjson["characterfocus"]:
        if a_left in fr_focus_link:
            focus_links[en_focus_link[en_focus_link.find('<'):en_focus_link.rfind('>')+1].replace('\'','"')] = fr_focus_link.replace('\'','"')[0:].strip()

characterarc_links = {}
for en_characterarc_link in enjson["characterarc"]:
    a_left = en_characterarc_link[en_characterarc_link.find('<'):en_characterarc_link.find('>')]
    for fr_characterarc_link in frjson["characterarc"]:
        if a_left in fr_characterarc_link:
            characterarc_links[en_characterarc_link[en_characterarc_link.find('<'):en_characterarc_link.rfind('>')+1].replace('\'','"')] = fr_characterarc_link.replace('\'','"')[fr_characterarc_link.find('<'):fr_characterarc_link.rfind('>')+1].strip()

# print(descriptor_links)
# print(focus_links)
print(characterarc_links)
# tempfilename = Path(os.environ['TEMP']) / format(uuid.uuid1())


# with open(indexfilename, 'r', encoding='utf8') as indexfile, open(tempfilename, 'w', encoding='utf8') as tempfile:
#     buffer = indexfile.read()
#     for en_descriptor_link in descriptor_links.keys():
#         buffer= buffer.replace(en_descriptor_link,descriptor_links[en_descriptor_link] )
#     for en_focus_link in focus_links.keys():
#         buffer= buffer.replace(en_focus_link,focus_links[en_focus_link] )
#     for en_characterarc_link in characterarc_links.keys():
#         buffer= buffer.replace(en_characterarc_link,characterarc_links[en_characterarc_link] )

#     tempfile.write(buffer)

# os.remove(indexfilename)
# os.replace(tempfilename,indexfilename)

