import pymorphy2
import re
from flask import Flask
from flask import url_for, render_template, request, redirect
from pymorphy2 import MorphAnalyzer
import json

app = Flask(__name__)

@app.route('/')  #главная
def index():
    return render_template('index.html')

@app.route('/resp')
def resp():
    user_phrase = request.args['phrase']
    if user_phrase=="":
        resp="Фразы нет и ответа не ждите"
    else:
        ana=parsing_phrase(user_phrase, morph)
        t=working_with_wordforms()
        resp=forming_response(ana, t)
    return render_template('thanks.html', phrase=user_phrase, response=resp)
    
    
def parsing_phrase(phrase, morph):
    ana=[]
    tags=[]
    words=phrase.split(" ")
    for w in words:
        parsed=morph.parse(w)[0]
        ana.append(parsed)
        tags.append(parsed.tag)
    return tags
    
def creating_json():
    wf={}
    n=0
    with open('wfcorpora.txt', 'r', encoding='utf-8') as t:
            for line in t.readlines():
                if n<100000:
                    word = re.sub(r'[^\w\s]+|[\d]+', r'', line).strip()
                    word=word.lower()
                    line=morph.parse(word)[0]
                    wf[word]=str(line.tag)
                    n+=1
    with open("wordforms.json", "w", encoding="utf-8") as f:
        json.dump(wf, f, ensure_ascii = False)
        
def working_with_wordforms():
    with open ("wordforms.json", 'r', encoding='utf-8') as f:
        json_string = f.read()
        data = json.loads(json_string)
        return data
    
def forming_response(tags, wf):
    response=[]
    for t in tags:
        for k in wf.keys():
            if str(t) == wf[k]:
                if k not in response:
                    response.append(k)
                    break
    
    myString = ' '.join(response).capitalize()
    return myString

morph = MorphAnalyzer()

if __name__ == '__main__':
    app.run(debug=False)

