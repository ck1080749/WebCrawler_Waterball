import bs4
import requests
import json
#f = open("456.html", "w", encoding="utf-8")
#g = open("123.html", "w", encoding="utf-8")
#h = open("789.json", "w")
technews = requests.get("https://technews.tw/author/handymantw/")# 15 item per page
cool3c = requests.get("https://www.cool3c.com/author/tiramisu")#10 item per page
soup_technews = bs4.BeautifulSoup(technews.text, "html.parser")
soup_cool3c = bs4.BeautifulSoup(cool3c.text, "html.parser")
#f.write(soup_cool3c.prettify())
#f.close()
#g.write(soup_technews.prettify())
#g.close()
#res = soup_cool3c.find_all("a")
#print("\n".join([str(elm) for elm in res]))
articles = {"cool3c":[], "technews": []}
for elm in soup_technews.select("h1.entry-title a"):
    print(elm.text,end=": ")
    print(elm["href"])
    articles["technews"].append({"title": elm.text, "link": elm["href"]})
"""
for elm in soup_cool3c.select("div.title a"):
    print(elm.text,end=": ")
    print(elm["href"])
    articles["cool3c"].append({"title": elm.text, "link": elm["href"]})
"""
for i in range(2,100):
    technews = requests.get("https://technews.tw/author/handymantw/page/"+str(i)+"/")
    soup_technews = bs4.BeautifulSoup(technews.text,"html.parser")
    for elm in soup_technews.select("h1.entry-title a"):
        print(elm.text,end=": ")
        print(elm["href"])
        articles["technews"].append({"title": elm.text, "link": elm["href"]})
    if(len(soup_technews.select("h1.entry-title a")) < 15):
        #print(i)
        break
print("\n")
for elm in soup_cool3c.select("div.title a"):
    print(elm.text,end=": ")
    print(elm["href"])
    articles["cool3c"].append({"title": elm.text, "link": elm["href"]})
for i in range(1,100):
    cool3c = requests.get("https://www.cool3c.com/author/tiramisu/p"+str(i))
    soup_cool3c = bs4.BeautifulSoup(cool3c.text,"html.parser")
    for elm in soup_cool3c.select("div.title a"):
        print(elm.text,end=": ")
        print(elm["href"])
        articles["cool3c"].append({"title": elm.text, "link": elm["href"]})
    if(len(soup_cool3c.select("div.title a")) < 10):
        #print(i)
        break
json.dump(articles, open("789.json", "w"))
#print(res[0].select("a"))
#print(soup_technews.prettify())
#h.write(json.dumps(articles))
#h.close()