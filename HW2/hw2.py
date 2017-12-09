import datetime

from flask import Flask
from flask import url_for, render_template, request, redirect
import json

app = Flask(__name__)


@app.route('/') #главная
def index():
    return render_template('index.html')

@app.route('/thanks')
def thanks():
    d={}
    d['name']=d['age']=d['city']=d['city_mother']=d['city_father']=d['curr_city']=""
    if request.args:
        d["name"] = request.args['name']
        d["age"]=request.args['age']
        d["city"]=request.args['city']
        d["city_mother"]=request.args['city_mother']
        d['city_father']=request.args['city_father']
        d['curr_city']=request.args['curr_city']
        d['year']=request.args['year']
        d['Q1']=request.args['Q1']
        d['Q2']=request.args['Q2']
        d['Q3']=request.args['Q3']
        
        if d["age"]!="" and d["city"]!="" and d["curr_city"]!="" and d["year"]!="..." and d['Q1']!="..." and d['Q2']!="..." and d['Q3']!="...":
            making_json(d)
            json_webpage()
        if d["name"]=="":
            d['name']="дорогой коллега"
            
        return render_template('thanks.html', name=d['name'])
    return redirect(url_for("json"))
    return redirect(url_for('stat'))
   
@app.route('/stats')
def stat():
    data = open_json()
    questions=["В эти выходные на центральной площади Дубны зажгут гирлянду главной ели Подмосковья.",
               "В Выхино пройдёт традиционный рождественский базар, а в Люблино устраивают чаепитие с блинами.",
               "С детьми можно отправиться на каток в Химки или бродить по ледяному городку в Балашихе."]
    res_Q=[
        {'ДУбны':0,'ДубнЫ':0},
        {'ЛЮблино':0,'ЛюблинО':0},
        {'БалАшихе':0,'БалашИхе':0}]
    for d in data:
        for i in range(3):
            key=d['Q'+str(i+1)]
            try:
                res_Q[i][key]+=1
            except KeyError:
                a=0
    return render_template("stat.html", number=len(data), variants=res_Q, questions=questions)
    
def open_json():
     with open ("results.json", 'r', encoding='utf-8') as f:
        json_string = f.read()
        data = json.loads(json_string)
        return data
    
@app.route('/search')
def search():
    return render_template('search.html')
    return redirect(url_for("results"))

@app.route('/results')
def results():   
    res=[]
    data=open_json()
    with open("res.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii = False)
    if request.args:
        with open("res1.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii = False)
        s_age=request.args["s_age"]
        s_curr_city=request.args["s_curr_city"]
        for d in data:
            if s_age!="" and s_curr_city=="":
                if d["age"]==s_age:
                    res.append(d)
            elif s_curr_city!="" and s_age=="":
                if d["curr_city"]==s_curr_city:
                    res.append(d)
            elif s_age!="" and s_curr_city!="":
                if d["age"]==s_age and d["curr_city"]==s_curr_city:
                    res.append(d)
            else:
                res.append(d)
        with open("res.json", "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii = False)      
    return render_template('results.html', res=res, r=len(res))
    

def making_json(d):
    data=[]
    try:
        with open ('results.json', 'r', encoding='utf-8') as f:
            json_string=f.read()
            if len(json_string)>0:
                data = json.loads(json_string)
    except:
        json_string=''
    
    with open('results.json', 'w', encoding='utf-8') as f:
        data.append(d)
        json.dump(data, f, ensure_ascii = False)

@app.route('/json')
def json_webpage():
    data=open_json()
    return render_template("json.html", content=data)

if __name__ == '__main__':    
    app.run(debug=False)

