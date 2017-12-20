import json
import os, urllib.request, re

def collecting_dict():
    letters=['a', 'b', 'v', 'g', 'd', 'e', 'sch', 'z', 'i', 'k',
             'l', 'm', 'n', 'o', 'p', 'po','pr', 'r', 's', 'sm', 't', 'u', 'f', 'x', 'c', 'ch', 'sh', 'ya']
    #letters=['a']
    commonUrl = 'http://slovnik.narod.ru/old/slovar/'
    d={}
    for i in letters:
        pageUrl = commonUrl + i +'.html'
        #print(pageUrl)
        text_html=download_page(pageUrl)
        plain_text(text_html,d)
        #print(a)
    return(d)
        
def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('UTF-8')
    except:
        print("Error at", pageUrl)  
    return text

def replace_teg(text):
    res=text
    value='<td>,</td>'
    for s in value.split(","):
        res=res.replace(s,'')
    return res

def plain_text(text, d):
    p=re.compile('<table border=1 width=100%>.*?</table>', flags= re.DOTALL)
    text=p.findall(text)
    p=re.compile('<tr>.*?</tr>', flags= re.DOTALL)
    text=p.findall(text[0])
       
    for t in text:
        p=re.compile('<td>.*?</td>', flags= re.DOTALL)
        value=p.findall(t)
        key = replace_teg(value[0])
        val = replace_teg(value[1])
        d[key]=val
               
def save_json(data):
    with open('dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii = False)

d=collecting_dict()
save_json(d)

