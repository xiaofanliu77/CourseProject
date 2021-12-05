#Libraries for Data Collection and Cleaning
import os
import html2text
#Preprocess Data
os.remove("documents.txt")
c = open("documents.txt",'a+',encoding = "utf-8")
for filename in os.listdir('Data'):
    if filename.endswith('.txt'):
        with open(os.path.join('Data', filename)) as f:
            content = f.read()
            content = content.replace('\n',' ')
            content = content.replace('[NOISE]',' ')
            content = content.replace('[MUSIC]',' ')
            content = content.replace('[SOUND]',' ')
            content = content.replace('\u2011',' ')
            c.write(content + '\n')
            
    if filename.endswith('.html'):
        with open(os.path.join('Data', filename), encoding='utf8') as d:
            content = d.read()
            h = html2text.HTML2Text()
            content = h.handle(content)
            content = content.replace('\n',' ')
            content = content.replace('\u2011',' ')
            string = str(content)
            c.write(string + '\n')
c.close()