from lxml import html
from sys import argv
fname=argv[1]
et=html.parse(fname)
ht=et.getroot()
body=ht.body
list_md=[]
for div in body.getiterator():
    try:
        attr=div.attrib['class']
    except KeyError:
        continue
    if attr=='sectionHeading':
        txt=div.text_content()
        txt_nospace=''.join(e for e in txt if not e.isspace())
        list_md.append({})
        list_md[-1]['sectionHeading']=txt_nospace
        list_md[-1]['notes']=[]
    elif attr=='noteHeading':
        dict_note={}
        dict_note['noteHeading']=div.text_content()
    elif attr=='noteText':
        txt=div.text_content()
        txt_nospace=''.join(e for e in txt if not e.isspace())
        dict_note['noteText']=txt_nospace
        list_md[-1]['notes'].append(dict_note)

fname=fname[:-5]+'.md'
f=open(fname,'w')
contents=[]
for dict_sec in list_md:
    line='+ '+dict_sec['sectionHeading']
    contents.append(line+'\n')
    list_sec_notes=dict_sec['notes']
    for dict_note in list_sec_notes:
        line='  - '+dict_note['noteHeading']
        contents.append(line+'\n')
        line='  - '+dict_note['noteText']
        contents.append(line+'\n')
f.writelines(contents)
f.close()
