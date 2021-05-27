#init
import bs4
import requests
import datetime as date
import json
from tqdm import tqdm
from time import sleep

COMMAND_LIST = ["search", "update", "help", "exit", "printall", "export", "goto"]#rear 2 are search only command
OBJECT = "Practicing Web Crawler and search engine algorithm, the latter is probably the more important one. Probably implement GUI and sort_by_time in the future."

def main_menu() -> int:
    while True:
        print("-------------------------------------------")
        print("1. show all articles")
        print("2. search by title")
        print("3. search by tag")
        print("4. search in excerpt")
        print("5. normal search (slowest)")
        print("6. update database")
        print("7. quit program")
        print("operation> ", end="")
        try:
            opt = int(input())
            if not(0 < opt < 8):
                print("invalid input!")
                #print("-------------------------------------------")
                continue
            else:
                print("-------------------------------------------")
                return opt
        except:
            print("invalid input!")
            #print("-------------------------------------------")
            continue
    return None

def help_menu(cmd = ""):
    if cmd == "":
        print("To find out detailed information of certain command, please enter \"help [COMMAND_NAME]\"")
        print("Global commands: ")
        print("\thelp            Show description of commands.\n")
        print("Main menu commands:")
        print("\tsearch          Search in the database.")
        print("\tupdate          Update database.")
        print("\texit            Exit.")
        print("\tprintall        Print all datas in the database.\n")
        print("Search result menu commands:")
        print("Note: these command won't work if there's a connection issue.")
        print("\tgoto            Show detailed information of a chose data provided in the search menu.")
        print("\texport          Export detailed information of a chosen data provided in the search menu.\n")

    elif cmd == "help":
        print("usage: help [command]\n")
        print("\tcommand - show detailed information of the command\n")

    elif cmd == "search":
        print("usage: search [search_in] [-title] [-tag] [-excerpt] [-sort] \n")
        print("\tsearch_in - Keyword (necessary)")
        print("\t-title - Search in title only")
        print("\t-tag - Search in title only")
        print("\t-excerpt - Search in article's excerpt only")
        print("\t-sort - sort result in chronological order\n") 

    elif cmd == "update":
        print("usage: update\n")

    elif cmd == "printall":
        print("usage: printall [-!cool3c] [-!technews]\n")
        print("\t-!cool3c - Won't search in cool3c.")
        print("\t-!technews - Won't seatch in technews.\n")

    elif cmd == "exit":
        print("usage: Exit\n")

    elif cmd == "goto":
        print("usage: goto [index]\n")
        print("\tindex - Index number of the article you want to check in the search result list. Won't work in main menu. (necessary)\n")

    elif cmd == "export":
        print("usage: export [index] [destination]\n")
        print("\tindex - Index number of the article you want to check in the search result list. Won't work in main menu. (necessary)")
        print("\tdestination - File path of the output file destination. (optional)\n")
        print("Output will be text-only file.\n")

    else:
        print("No such command found!\n")

def defaultShutdownAction(interval = 0.3):
    print("Shutting down", end="")
    sleep(interval)
    print(".", end="", flush=True)
    sleep(interval)
    print(".", end="", flush=True)
    sleep(interval)
    print(".\n", flush=True)

def searchByTitleKeyword(search_in: dict, search: str, technews = True, cool3c = True, display = True, sbt = False)->list:
    result = list()
    if technews:
        if display:
            print("search \"", search, "\" in title in technews...", sep = "")
        for elm in search_in["technews"]:
            if elm["title"].find(search) != -1:
                result.append(elm)

    if cool3c:
        if display:
            print("search \"", search, "\" in title in cool3c...", sep = "")
        for elm in search_in["cool3c"]:
            if elm["title"].find(search) != -1:
                result.append(elm)
    if display:
        printSearchResultMenu(result,sbt=sbt)
    return result

def searchByTag(search_in: dict, tag:str, technews = True, cool3c = True, display = True, sbt=False)->list:
    result = list()
    if technews:
        if display:
            print("search \"", tag, "\" in tag in technews...", sep = "")
        for elm in search_in["technews"]:
            if tag in elm["tags"]:
                result.append(elm)
    if cool3c:
        if display:
            print("search \"", tag, "\" in tag in cool3c...", sep = "")
        for elm in search_in["cool3c"]:
            if tag in elm["tags"]:
                result.append(elm)
    if display:
        printSearchResultMenu(result, sbt=sbt)
    return result

def searchInArticleExcerpt(search_in: dict, search: str, technews = True, cool3c = True, display = True, sbt=False)->list:
    result = list()
    if technews:
        if display:
            print("search \"", search, "\" in excerpt in technews...", sep = "")
        for elm in search_in["technews"]:
            if elm["content"].find(search) != -1:
                result.append(elm)
    if cool3c:
        if display:
            print("search \"", search, "\" in excerpt in cool3c...", sep = "")
        for elm in search_in["cool3c"]:
            if elm["content"].find(search) != -1:
                result.append(elm)
    if display:
        printSearchResultMenu(result,sbt=sbt)
    return result

def printAllItem(to_print: dict):
    print("datas")
    print("    technews")
    for elm in to_print["technews"]:
        print("        "+elm["title"])
    print("    cool3c")
    for elm in to_print["cool3c"]:
        print("        "+elm["title"])
    print("")

def printOneItem(oneItem: dict):
    print(oneItem["title"])
    print(oneItem["link"])
    print(", ".join(oneItem["tags"]))
    print(oneItem["content"])
    print(oneItem["time"]+"\n")

def nrm_search(search_in: dict, search:str, technews = True, cool3c = True, sbt = False) -> list:
    result = []
    print("searching \"", search, "\" ...", sep="")
    [result.append(elm) for elm in searchByTag(search_in, search, technews = technews, cool3c = cool3c, display=False) if elm not in result]
    [result.append(elm) for elm in searchByTitleKeyword(search_in, search, technews = technews, cool3c = cool3c, display=False) if elm not in result]
    [result.append(elm) for elm in searchInArticleExcerpt(search_in, search, technews = technews, cool3c = cool3c, display=False) if elm not in result]
    printSearchResultMenu(result,sbt=sbt)
    return result

def init(file = "waterball.json") -> dict:

    print("Welcome to Mr. Waterball article database searching system.")
    d = dict()
    try:
        d = json.load(open(file, "r"))
        print("loaded: \""+file+"\", latest update: "+ d["update"])
        print(d["count"], "article(s): technews:", len(d["technews"]), ", cool3c:", len(d["cool3c"]))

    except:
        print("ERROR: file \""+file+"\" not found or invalid, try update() before accessing the data.")
    return d

def getSearchString() -> str:
    return input("search> ").split()[0]

def fastSearch()->list:
    pass

def searchMenuOperation(opt: str, toPrint: list) -> bool:
    opt = opt.split()
    if opt[0] == "export":       
        try:
            dest = int(opt[1])
            if dest >= len(toPrint) or dest < 0:
                print("Out of bound!")
                return False
            if len(opt) > 2:
                outputSearchResultArticle(toPrint[dest], dest=opt[2])
            else:
                outputSearchResultArticle(toPrint[dest])
            return True
        except:
            help_menu(cmd="export")
        return True
    elif opt[0] == "goto":
        try:
            dest = int(opt[1])
            if dest >= len(toPrint) or dest < 0:
                print("Out of bound!")
                return False
            goto(toPrint[dest])
            return True
        except:
            help_menu(cmd="goto")
    elif opt[0] == "help":
        help_menu(cmd="goto")
        help_menu(cmd="export")
    elif opt[0] == "exit":
        return True
    else:
        print("Unknown command!")
        return False
    print("")

def printSearchResultMenu(toPrint: list, sbt = False):
    sleep(1.0)
    print("")
    if len(toPrint) == 0:
        print("No Result!")
        return None
    if sbt:
        toPrint = sort(toPrint)
    print("---------------------result------------------------")
    i = 0
    for elm in toPrint:
        print(i,". ", sep="", end="")
        printOneItem(elm)
        i+=1
        a = False
        if i % 10 == 0:
            while True:
                opt = input("Enter command or press enter to go to next page> ")
                if opt == "":
                    print("\r", end="")
                    break
                else:
                    a = searchMenuOperation(opt, toPrint)
                    if a:
                        break
            if a:
                break
    while True:
        #a = False
        opt = input("Enter command or press enter to go back to main menu> ")
        if opt == "":
            print("\r", end="")
            break
        else:
            if searchMenuOperation(opt, toPrint):
                break
            
def update(technews = True, cool3c = True) -> dict:
    articles = {
        "update": str(date.datetime.now()),
        "untagged_count": 0,
        "count" : 0,
        "cool3c":[], 
        "technews": [],
        #"all_tags" : []
    }
    content_count = 0
    content = []
    title = []
    time = []
    tags = []
    #alltag = set()
    print("Loading...", end="",flush=True)
    if technews:  
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
                "content" : content[i].text[:-10].replace("&rdquo;", " ").replace("&ldquo;"," ")+"...",
                "time" : calTime(time[i].text),
                "tags" : list(set(tags[i].text.replace("\t","").replace("\n","").replace("\r","").replace(" ","").split(",")))
            })
            #alltag.update(list(set(tags[i].text.replace("\t","").replace("\n","").replace("\r","").replace(" ","").split(","))))
            content_count+=1
        
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
                    "content" : content[i].text[:-10].replace("&rdquo;", " ").replace("&ldquo;"," ")+"...",
                    "time" : calTime(time[i].text),
                    "tags" : list(set(tags[i].text.replace("\t","").replace("\n","").replace("\r","").replace(" ","").split(",")))
                })
                #alltag.update(list(set(tags[i].text.replace("\t","").replace("\n","").replace("\r","").replace(" ","").split(","))))
                content_count+=1
            if(len(soup.select("h1.entry-title a")) < 15):
                #print(j)
                break
    if cool3c:
        #cool3c, 10 items per page
        untagged = [
            "https://www.cool3c.com/article/159097",
            "https://www.cool3c.com/article/156566",
            "https://www.cool3c.com/article/156569",
            "https://www.cool3c.com/article/156568",
            "https://www.cool3c.com/article/156564",
            "https://www.cool3c.com/article/156563"
        ]
        articles["untagged_count"] = len(untagged)
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
                "content" : content[i].text.replace("&rdquo;", " ").replace("&ldquo;"," ")+"...", 
                "time" : calTime("",cool3c_link=title[i]["href"]),
                #"tags" : list(set(tags[i].text.replace("\n\n", "").split("\n")))
            })
            if title[i]["href"] in untagged:
                articles["cool3c"][-1]["tags"] = []
            else:
                articles["cool3c"][-1]["tags"] = list(set(tags[i].text.replace("\n\n", "").split("\n")))
                #alltag.update(list(set(tags[i].text.replace("\n\n", "").split("\n"))))
            content_count+=1
            
        for j in range(1,100):#other pages
            req = requests.get("https://www.cool3c.com/author/tiramisu/p"+str(j))
            soup = bs4.BeautifulSoup(req.text,"html.parser")
            title = soup.select("div.title a")
            content = soup.select("div.content a")
            #time = calTime("",cool3c_link="https://www.cool3c.com/author/tiramisu/p"+str(j))
            temp = [elm.text for elm in soup.select("ul.list-inline")]
            tags = soup.select("ul.list-inline")[temp.index("\n\n\n\n")+1:]
            #if len(tags) == 0:
            #    break#斷然不處理。
            for i in range(len(title)):
                if title[i]["href"] in untagged:
                    tags.insert(i, tags[0])
                if title[i].text == "訂閱硬科技電子報！":
                    continue
                #if len(tags[i:]) == 0:
                #    break
                print(".",end = "", flush=True)
                articles["cool3c"].append({
                    "title": title[i].text, 
                    "link": title[i]["href"], 
                    "content" : content[i].text.replace("&rdquo;", " ").replace("&ldquo;"," ")+"...", 
                    "time" : calTime("",cool3c_link=title[i]["href"]),
                    #"tags" : list(set(tags[i].text.replace("\n\n", "").split("\n")))
                })
                if title[i]["href"] in untagged:
                    articles["cool3c"][-1]["tags"] = []
                else:
                    articles["cool3c"][-1]["tags"] = list(set(tags[i].text.replace("\n\n", "").split("\n")))
                    #alltag.update(list(set(tags[i].text.replace("\n\n", "").split("\n"))))
                content_count+=1

            if(len(soup.select("div.title a")) < 10):
                #print(i)
                break
    articles["count"] = content_count
    #articles["all_tags"] = list(alltag)
    with open("waterball.json", "w") as f:
        json.dump(articles,f,indent=2)
        print("\nsaved.")
    return articles

def outputSearchResultArticle(to_output: dict, dest = ""):
    filename = ""
    if dest == "":
        filename = "./.exports/"+to_output["title"]+".txt"   
    else:
        filename = dest
    link = requests.get(to_output["link"])
    soup = bs4.BeautifulSoup(link.text, "html.parser")
    with open(filename, "w", encoding="utf-8") as f:
        #f.write(soup.prettify())
        f.write(to_output["title"]+"\n")
        f.write(to_output["link"]+"\n")
        f.write(to_output["time"]+"\n")
        f.write(" ".join(to_output["tags"]))
        f.write("\n\n")
        if to_output["link"].find("cool3c") != -1:
            #print("cool3c")
            content = soup.select("div.col-12 p")
            count = 0
            for elm in content:  
                if elm.text == "":
                    count+=1
                    continue
                f.write(elm.text+"\n\n")
            #print(count)
        elif to_output["link"].find("technews") != -1:
            content = soup.select("div.indent p")
            count = 0
            for elm in content:  
                if elm.text == "":
                    count+=1
                    continue
                f.write(elm.text+"\n\n")
            #print(count)
        else:
            print("ERROR!")

def goto(article: dict) -> bool:
    #print(article["link"])
    dest = requests.get(article["link"])
    soup = bs4.BeautifulSoup(dest.text, "html.parser")
    """
    with open("article2.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    """
    if article["link"].find("cool3c") != -1:
        print("\n")
        print(article["title"]+"\n")
        #print("cool3c")
        content = soup.select("div.col-12 p")
        count = 0
        for elm in content:  
            if elm.text == "":
                count+=1
                continue
            print(elm.text+"\n")
        #print(count)
    elif article["link"].find("technews") != -1:
        print("\n")
        print(article["title"]+"\n")
        #print("technews")
        content = soup.select("div.indent p")
        for elm in content:  
            if elm.text == "":
                count+=1
                continue
            print(elm.text+"\n")
    else:
        print("ERROR!")
    return False

def calTime(timeformat: str, cool3c_link="")-> str:
    currentTime = date.datetime.now()
    if cool3c_link != "":# n天前 n月前 n年前
        req = requests.get(cool3c_link)
        soup = bs4.BeautifulSoup(req.text,"html.parser")
        d = soup.select("span")[4]
        timeformat = d.text
        formatted = timeformat.replace(" ", ".").split(".")
        articleTime = date.datetime(int(formatted[0]), int(formatted[1]), int(formatted[2]))
        return str(articleTime).split()[0]
    else:#technews
        formatted = timeformat.replace(" ", "").replace("年", " ").replace("月", " ").replace("日", " ").split()
        #print(formatted)
        articleTime = date.datetime(int(formatted[0]), int(formatted[1]), int(formatted[2]))
        return str(articleTime).split()[0]

def sort(to_sort: list)->list:
    return sorted(to_sort, key = lambda d: d["time"], reverse= True)

def cmptime(time1: str, time2: str)->bool:
    pass
