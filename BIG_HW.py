import os, urllib.request, re, html

def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('UTF-8')
        print(pageUrl)
    except:
        print("Error at", pageUrl)
        text=""
    return text

def collecting_metadata(text, pageUrl):
    d={}
    title=re.compile('<div class="title-reading hide">(.*?)</div>', flags= re.DOTALL)
    titles =title.findall(text)
    titles=titles[0].lower()
    titles=html.unescape(titles)
    d['title']=titles
    author=re.compile('([А-Я][А-Яа-я]*[^(ка)(ии)(ой)(ве)])\.<\/p><div id', flags= re.DOTALL)
    authors=author.findall(text)
    if len(authors)>0:
        if len(authors[0])>3:
            authors=authors[0]
        else:
            authors="Noname"       
    else:
        authors="Noname"
    d['authors']=authors
    date1=re.compile('\"datePublished\">.*?(\d\d-\d\d-\d\d\d\d)', flags= re.DOTALL)
    dates=date1.findall(text)
    dates=dates[0].replace('-', '.')
    d['dates']=dates
    topic=re.compile('\"genre\">(.*?)</span>', flags= re.DOTALL)
    topics=topic.findall(text)
    d['topics']=topics[0].lower()
    d['year']=dates[-4:]
    d['month']=dates[3:-5]
    return d
    
    
def making_csv(d, pageUrl, root_path, path, name_journal):
    sex=birthday=genre_fi=type1=chronotop=publisher=' '
    row = '%s\t%s\t%s\t%s\t%s\t%s\tпублицистика\t%s\t%s\t%s\t%s\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tname_journal\t%s\t%s\tгазета\tРоссия\tВолгоградская область\tru\n'
    with open(root_path+"metadata.csv", 'a', encoding='utf-8') as f:
        f.write(row % (path, d['authors'], sex, birthday, d['title'], d['dates'],
                  genre_fi, type1, d['topics'], chronotop, pageUrl, publisher, d['year']))

def plain_article(text):
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    text_article=re.compile('<p(.*)<\/p>', flags= re.DOTALL)
    texts_article=text_article.findall(text)
    if len(texts_article)==0:
        return ""
    texts_article=texts_article[0]
    texts_article=re.sub(regTag, '', texts_article)
    texts_article=re.sub(regSpace, ' ', texts_article)
    return texts_article

def making_txt(text, d, root_path, pageUrl):
    d['title']=d['title'].replace('/', '_')
    path=root_path+'plain/'+d['year']
    path2=path+'/'+d['month']
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path2):
        os.mkdir(path2)
        
    path_ms=root_path+'mystem-plain/'+d['year']
    path2_ms=path_ms+'/'+d['month']
    if not os.path.exists(path_ms):
        os.mkdir(path_ms)
    if not os.path.exists(path2_ms):
        os.mkdir(path2_ms)

    path_msxml=root_path+'mystem-xml/'+d['year']
    path2_msxml=path_msxml+'/'+d['month']
    if not os.path.exists(path_msxml):
        os.mkdir(path_msxml)
    if not os.path.exists(path2_msxml):
        os.mkdir(path2_msxml)
    
    name_file=d['title']+'.txt'
    name_file=name_file.replace(" ", "_")
    head='@au '+d['authors']+'\n'
    head=head+'@ti '+d['title']+'\n'
    head=head+'@da '+d['dates']+'\n'
    head=head+'@topic '+d['topics']+'\n'
    head=head+'@url '+pageUrl+'\n'
    text=head+text
    with open(path2+'/'+name_file, 'a', encoding='utf-8') as f:
        f.write(text)
    return path2, name_file


def mystem(root_path):
    n="-cgnid "
    m="-cgnid --format xml "
    for root, dirs, files in os.walk(root_path+"/plain"):
        for f in files:
            input_file=os.path.join(os.path.abspath(root), f)
            output_file=input_file.replace("plain", "mystem-plain")
            os.system(r"./mystem " + n +  input_file + " " + output_file)
    for root, dirs, files in os.walk(root_path+"/plain"):
        for f in files:
            input_file=os.path.join(os.path.abspath(root), f)
            output_file=input_file.replace("plain", "mystem-xml")
            output_file=output_file.replace(".txt", ".xml")
            os.system(r"./mystem " + m +  input_file + " " + output_file)
    
folders=['plain', 'mystem-plain', 'mystem-xml']
name_journal='Урюпинская_правда'
if not os.path.exists(name_journal):
    os.mkdir(name_journal)
for f in folders:
    if not os.path.exists(name_journal+'/'+f):
        os.mkdir(name_journal+'/'+f)

    
root_path=os.path.abspath('.')+"/"+name_journal+"/"
commonUrl = 'http://uryupinka.ru/'
for i in range(264, 1334):
    pageUrl = commonUrl + str(i)
    text=download_page(pageUrl)
    if text!="":
        plain_text=plain_article(text)
        if plain_text!="":
            metadata=collecting_metadata(text, pageUrl)
            path, name_file=making_txt(plain_text, metadata, root_path, pageUrl)
            making_csv(metadata, pageUrl, root_path, path+'/'+name_file, name_journal)

mystem(root_path)
   




