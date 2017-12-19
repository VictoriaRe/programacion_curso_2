import sqlite3
import matplotlib.pyplot as plt

def creating_DB(c):
    c.execute("CREATE TABLE IF NOT EXISTS слова(id, Lemma, Wordform, Glosses)")
    c.execute("CREATE TABLE  IF NOT EXISTS глоссы(id, обозначение, расшифровка)")
    c.execute("CREATE TABLE  IF NOT EXISTS слова_глоссы(id_слова, id_глоссы)")
    
def slova_DB(c):
    i=0
    data=[]
    c.execute('DELETE FROM слова')
    c.execute('DELETE FROM глоссы')
    c.execute('DELETE FROM слова_глоссы')
    for row in c.execute('SELECT * FROM wordforms'):
        r1=str(row[0])
        r2=str(row[1])
        r3=str(row[2])
        i+=1
        a="INSERT INTO слова VALUES ("+str(i)+", '"+r1+"', '"+r2+"', '"+r3+"')"
        data.append(a)
    for d in data:
        c.execute(d)
        
def glossi_DB(c):
    glosses=[]
    gloss_def={}
    i=0
    with open ("glossing_rules.txt", 'r', encoding='utf-8') as f:
        t= f.read()
        for row in t.split("\n"):
            row = row.split(" — ")
            i+=1
            a="INSERT INTO глоссы VALUES ("+str(i)+", '"+row[0]+"', '"+row[1]+"')"
            glosses.append(a)
            gloss_def[i]=row[0]
    for g in glosses:
        c.execute(g)
    return gloss_def

def slova_glossi_DB(c, gloss_def):  
    num_gloss={}
    quiery=[]
    quieryId=[]
    id_Word=[]
    id_Gloss=[]
    word_gloss=[]    
    for row in c.execute('SELECT * FROM слова'):
        for gl in row[3].split('.'):
            quiery.append(gl)
            quieryId.append(row[0])
    for i in range(len(quiery)):
        q=quiery[i]
        v=(q,)
        c.execute('SELECT * FROM глоссы WHERE обозначение=?',v)
        a=c.fetchone()
        if a != None:
            id_Word.append(quieryId[i])
            id_Gloss.append(a[0])  
    for i in range(len(id_Word)):
        text="INSERT INTO слова_глоссы VALUES ("+str(id_Word[i])+", '"+str(id_Gloss[i])+"')"
        word_gloss.append(text)
    for g in word_gloss:
        c.execute(g)
    for row in c.execute('SELECT * FROM слова_глоссы'):
        try:
            num_gloss[row[1]]+=1
        except KeyError:
            num_gloss[row[1]]=1
    conn.commit()
    conn.close()
    return gloss_def, num_gloss

def graphics(gloss_def, num_gloss):
    graph={}
    for g in num_gloss:
        graph[gloss_def[int(g)]]=num_gloss[g]
    X=graph.keys()
    Y=graph.values()
    plt.bar(X,Y)
    plt.title("количество глосс")
    plt.show()
    
conn = sqlite3.connect('hittite.db')
c = conn.cursor()
creating_DB(c)
slova_DB(c)
d1=glossi_DB(c)
d2, d3=slova_glossi_DB(c, d1)
graphics(d2, d3)



