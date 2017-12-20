import datetime
from flask import Flask
from flask import url_for, render_template, request, redirect
import json
import os, urllib.request, re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

@app.route('/')
def index():
    pageUrl = 'https://pogoda.turtella.ru/Macedonia/Skopje/'
    text_html=download_page(pageUrl)
    d=plain_text(text_html)
    return render_template('main.html', r=d)
    return redirect(url_for("trans"))
    return redirect(url_for('thanks'))

@app.route('/oldbutgold')
def trans():
    if request.args:
        word=request.args['word']
        #w="старое слово"
        data=get_dic()
        try:
            w=data[word]
        except KeyError:
            w='об этом слове ниче сказать не можем'
    return render_template('dorev.html', word=word, word_old=w)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/results')
def thanks():
    d={}
    score=0
    correct=['мѣсяце', 'Нет', 'апрѣле', 'Бѣсов', 'Балбес', 'Глѣб', 'Снѣг',
             'Грѣх', 'лѣто', 'ель']
    if request.args:
        d['Q1']=request.args['Q1']
        d['Q2']=request.args['Q2']
        d['Q3']=request.args['Q3']
        d['Q4']=request.args['Q4']
        d['Q5']=request.args['Q5']
        d['Q6']=request.args['Q6']
        d['Q7']=request.args['Q7']
        d['Q8']=request.args['Q8']
        d['Q9']=request.args['Q9']
        d['Q10']=request.args['Q10']
        res=d.keys()
        res=list(res)
        res.sort()
        i=0
        for r in res: 
            if d[r]==correct[i]:
                score+=1
            i+=1
        return render_template('res.html', s=score)

@app.route('/news')
def news():
    pageUrl = 'https://lenta.ru/'
    text_html=download_page(pageUrl)
    d=plain_text(text_html)
    txt(d)
    mystem_txt()
    return render_template('news.html', t=d)

def get_dic():
    with open ("dictionary.json", 'r', encoding='utf-8') as f:
        json_string = f.read()
        data = json.loads(json_string)
        return data


    
def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('UTF-8')
    except:
        print("Error at", pageUrl)  
    return text

def replace_teg(text, value):
    res=text
    #value='<td>,</td>'
    for s in value.split(","):
        res=res.replace(s,'')
    return res

def plain_text(text):
    r={}
    p=re.compile('bigTemp">.*?<span class', flags= re.DOTALL)
    temp=p.findall(text)
    r['температура']=replace_teg(temp[0], 'bigTemp">,<span class')
    #print(r['температура'])
    p=re.compile('<div class="title mb10">.*?</div>', flags= re.DOTALL)
    date=p.findall(text)
    r['день']=replace_teg(date[0], '<div class="title mb10">,</div>')
    #print(r['день'])
    p=re.compile('Давление:.*?tableVal.*?</td>', flags= re.DOTALL)
    bar=p.findall(text)
    p=re.compile('">.*?<', flags= re.DOTALL)
    r['давление']=replace_teg(p.findall(bar[0])[0],'">,<')
    #print(r['давление'])

    p=re.compile('Влажность воздуха:.*?tableVal.*?</td>', flags= re.DOTALL)
    wet=p.findall(text)
    p=re.compile('">.*?<', flags= re.DOTALL)
    r['влажность']=replace_teg(p.findall(wet[0])[0],'">,<')
    #print(r['влажность'])

    p=re.compile('wind">.*?</td></tr></table>', flags= re.DOTALL)
    wind = p.findall(text)
    #print(wind)
    p=re.compile('[А-Я]+', flags= re.DOTALL)
    r['ветер напр']= p.findall(wind[0])
    #print(r['ветер напр'])
    p=re.compile('[0-9]+.*м/с', flags= re.DOTALL)
    r['ветер скорость']= p.findall(wind[0])
    #print(r['ветер cкорость'])
    return r

def plain_text_lenta(text):
    text=text.lower()
    p=re.compile('[а-я]+ ', flags= re.DOTALL)
    res= p.findall(text)
    #print(res)
    return res
               
def txt(res):
    for r in res:
        with open ('lenta.txt', 'a', encoding='utf-8') as f:
            f.write(r)

def mystem_txt():
    #n="-cgnid "
    os.system(r"/Users/victoriaregina/Documents/HW add/mystem -cgnid lenta.txt lenta_lemm.txt")
    #"C:\mystem.exe input.txt output.txt"
    #print(input_file, '\n', output_file)

if __name__ == '__main__':    
    app.run(debug=False)

