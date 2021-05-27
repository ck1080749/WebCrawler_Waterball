#init
import bs4
import requests
import json


articles = {"cool3c":[], "technews": []}
content = []
title = []
time = []
tags = []# not implemented yet

print("Loading...", end="",flush=True)

#technews, 15 item per page
req = requests.get("https://technews.tw/author/handymantw/")#page1
soup = bs4.BeautifulSoup(req.text, "html.parser")
title = soup.select("h1.entry-title a")
content = soup.select("div.moreinf")
time = soup.select("span.body")[1::4]
tags = soup.select("span.body")[2::4]
for i in range(len(title)):
    #print(title[i].text)
    #print(title[i]["href"])
    print(".",end = "", flush=True)
    articles["technews"].append({
        "title": title[i].text,
        "link": title[i]["href"],
        "content" : content[i].text[:-10]+"...",
        "time" : time[i].text,
        "tags" : list(set(tags[i].text.replace("\t","").replace("\n","").replace("\r","").replace(" ","").split(",")))
    })

for j in range(2,100): #otherpages
    req = requests.get("https://technews.tw/author/handymantw/page/"+str(j)+"/")
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    title = soup.select("h1.entry-title a")
    content = soup.select("div.moreinf")
    time = soup.select("span.body")[1::4]
    tags = soup.select("span.body")[2::4]
    for i in range(len(title)):
        #print(title[i].text)
        #print(title[i]["href"])
        print(".",end = "", flush=True)
        articles["technews"].append({
            "title": title[i].text,
            "link": title[i]["href"],
            "content" : content[i].text[:-10]+"...",
            "time" : time[i].text,
            "tags" : list(set(tags[i].text.replace("\t","").replace("\n","").replace("\r","").replace(" ","").split(",")))
        })
    if(len(soup.select("h1.entry-title a")) < 15):
        #print(j)
        break


#cool3c, 10 items per page
untagged = [
    "https://www.cool3c.com/article/159097",
    "https://www.cool3c.com/article/156566",
    "https://www.cool3c.com/article/156569",
    "https://www.cool3c.com/article/156568",
    "https://www.cool3c.com/article/156564",
    "https://www.cool3c.com/article/156563"
]
req = requests.get("https://www.cool3c.com/author/tiramisu")#page 1
soup = bs4.BeautifulSoup(req.text, "html.parser")
title = soup.select("div.title a")
content = soup.select("div.content a")
time = soup.select("div.created a")
tags = soup.select("ul.list-inline")[3:]

for i in range(len(title)):
    #print(title[i].text)
    #print(title[i]["href"])
    print(".",end = "", flush=True)
    
    if title[i]["href"] in untagged:
        tags.insert(i, tags[0])
    articles["cool3c"].append({
        "title": title[i].text,
        "link": title[i]["href"],
        "content" : content[i].text+"...", 
        "time" : time[i].text.replace("\n","").replace(" ",""),
        #"tags" : list(set(tags[i].text.replace("\n\n", "").split("\n")))
    })
    if title[i]["href"] in untagged:
       articles["cool3c"][-1]["tags"] = []
    else:
        articles["cool3c"][-1]["tags"] = list(set(tags[i].text.replace("\n\n", "").split("\n")))
    
for j in range(1,100):#other pages
    req = requests.get("https://www.cool3c.com/author/tiramisu/p"+str(j))
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    title = soup.select("div.title a")
    content = soup.select("div.content a")
    time = soup.select("div.created a")
    temp = [elm.text for elm in soup.select("ul.list-inline")]
    tags = soup.select("ul.list-inline")[temp.index("\n\n\n\n"):]
    if len(tags) == 0:
       break#斷然不處理。
    for i in range(len(title)):
        if title[i]["href"] in untagged:
            tags.insert(i, tags[0])
        if title[i].text == "訂閱硬科技電子報！":
            continue
        if len(tags[i:]) == 0:
            break
        print(".",end = "", flush=True)
        articles["cool3c"].append({
            "title": title[i].text, 
            "link": title[i]["href"], 
            "content" : content[i].text+"...", 
            "time" : time[i].text.replace("\n","").replace(" ",""),
            #"tags" : list(set(tags[i].text.replace("\n\n", "").split("\n")))
        })
        if title[i]["href"] in untagged:
            articles["cool3c"][-1]["tags"] = []
        else:
            articles["cool3c"][-1]["tags"] = list(set(tags[i].text.replace("\n\n", "").split("\n")))

    if(len(soup.select("div.title a")) < 10):
        #print(i)
        break

#output as json
json.dump(articles, open("waterball.json", "w"))
