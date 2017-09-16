import urllib.request  # импортируем модуль
import re
def opening():
    req = urllib.request.Request('http://vv-34.ru')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        return html

def collecting_titles(html):
    titles=[]
    new_titles = []
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    title1 = re.compile('<div class="bl_title">.*?</div>', flags= re.DOTALL)
    titles1 = title1.findall(html)
    for t in titles1:
        titles.append(t)
    title2 = re.compile('<div class="single_bl_title">.*?</div>', flags= re.DOTALL)
    titles2=title2.findall(html)
    for t in titles2:
        titles.append(t)
    title3 = re.compile('<span class="thumbname">.*?</span>', flags= re.DOTALL)
    titles3=title3.findall(html)
    for t in titles3:
        titles.append(t)
    for t in titles:
        clean_t = regSpace.sub("", t)
        clean_t = regTag.sub("", clean_t)
        new_titles.append(clean_t)
    return new_titles

def titles_in_text(titles):
    with open('titles.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(titles))
        
    
html=opening()
titles=collecting_titles(html)
titles_in_text(titles)

