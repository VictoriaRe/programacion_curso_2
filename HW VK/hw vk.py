import urllib.request  # импортируем модуль
import ssl
import json
import matplotlib.pyplot as plt
import sqlite3


ssl._create_default_https_context = ssl._create_unverified_context

def get_posts(c, token):
    offsets = [0, 150, 350]
    postcom_rel={}
    comm_city={}
    q_city={}
    ages={}
    len_post=[]
    len_comm=[]
    id_posts=[]
    for off in offsets:
        req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-55284725&count=100&v=5.74&access_token='+token+'&offset=' + str(off))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        
        for n in range(100):
            data1=data['response']['items'][n]['text']
            id_post = data["response"]["items"][n]["id"]
            num_comm=data["response"]["items"][n]["comments"]['count']
            
            if num_comm<100:
                offset_comm=[0]
            else:
                offset_comm=[0, 100]
                num_comm=min(num_comm, 200)
                
            if data1!='':
                posts_DB(c, id_post, data1)
                len_post=len(data1.split())

            i=0
            for off_comm in offset_comm:
                stroka = 'https://api.vk.com/method/wall.getComments?owner_id=-55284725&post_id='+str(id_post)+'&count=100&v=5.74&extended=1&fields=bdate,city&offset='+str(off_comm)              
                req1= urllib.request.Request(stroka)
                response1 = urllib.request.urlopen(req1)
                result1 = response1.read().decode('utf-8')
                data2 = json.loads(result1)
                
                if i==0:
                    end=min(num_comm, 100)
                else:
                    end=num_comm-102
                len_sum=0
                
                for m in range(end):
                    #print(end)
                    i+=1
                    info=data2['response']['items'][m]['text']
                    
                    try:
                        profile=data2['response']['profiles'][m] 
                    except:
                        pass
                    
                    if info!='':
                        comments_DB(c, id_post, m, info)
                        len_sum=len(info.split()) #длина коммента
                        
                        if 'bdate' in profile:
                            
                            if len(profile['bdate']) >= 6:
                                byear = int(''.join(profile['bdate'][-4:]))
                                #print(byear)
                                curr_age = 2018 - byear
                                if curr_age in ages:
                                    age_1=ages[curr_age]
                                    ages[curr_age]=round((len_sum+age_1)/2, 2)
                                else:
                                    ages[curr_age]=len_sum

                        
                        if 'city' in profile:
                            city=profile['city']['title']
                            if city in comm_city:
                                len_av_1=comm_city[city]
                                comm_city[city]=round((len_sum+len_av_1)/2, 2)
                            else:
                                comm_city[city]=len_sum

                            if city in q_city:
                                q_1=q_city[city]
                                q_city[city]=q_1+1
                            else:
                                q_city[city]=1

                        if len_post in postcom_rel:
                            len_average_1=postcom_rel[len_post]
                            postcom_rel[len_post]=round((len_sum+len_average_1)/2, 2)
                        else:
                            postcom_rel[len_post]=len_sum #собираем словарь;)
          
    list_city=city_1(comm_city, q_city)            
    return postcom_rel, list_city, ages

#учитываем города, у которых кол-во комментариев больше 50   
def city_1(comm_city, q_city):
    res={}
    res['остальные']=0
    for city in q_city:
        if q_city[city]>50:
            res[city]=comm_city[city]
        else:
            res['остальные']=round((res['остальные']+comm_city[city])/2, 2)
    return res

       

def graphics(data, title, xlabel, ylabel, nameFile, rotation):
    
    x = sorted(data.keys())
    y = data.values()
    plt.figure()
    plt.scatter(x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if rotation==1:
        plt.xticks(range(len(data.keys())), data.keys(), rotation=90)
    plt.savefig(nameFile, dpi=300, format='png')

def creating_DB(c):
    c.execute("CREATE TABLE IF NOT EXISTS посты(id_post, text_post)")
    c.execute("CREATE TABLE  IF NOT EXISTS комментарии(id_post, num_comm, text_comm)")
    return c

def posts_DB(c, id_post, text_post):
    a="INSERT INTO посты VALUES ("+str(id_post)+", '"+text_post+"')"
    c.execute(a)
    conn.commit()
    
def comments_DB(c, id_post, num_comm, text_comm):
    text_comm=text_comm.replace("'", "")
    b="INSERT INTO комментарии VALUES ("+str(id_post)+", '"+str(num_comm)+"', '"+text_comm+"')"
    c.execute(b)
    conn.commit()
    

token="4b53d8724b53d8724b53d872ed4b317fc544b534b53d87211b4cccce28ec32452795bd8"
conn = sqlite3.connect('посты_комменты_НВЛЬН.db')
c = conn.cursor()
creating_DB(c)
dic1, dic2, dic3=get_posts(c, token)
conn.close()
gr1=graphics(dic1, 'Как соотносится длина поста с средней длиной комментариев?',
         'Длина поста', 'Средняя длина комментариев', 'post_with_comments.png', 0)
gr2=graphics(dic2, 'Как соотносится длина комментария и город?',
             'Город', 'Средняя длина комментариев', 'city_with_comments.png', 1)
gr3=graphics(dic3, 'Как соотносится длина комментария и возраст?',
         'Возраст', 'Средняя длина комментариев', 'age_with_comments.png', 0)

