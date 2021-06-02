import my_module_001 as m
import json


def command_mainmenu():
    global data
    while True:
        opt = input("command > ")
        if opt == "":
            continue
        opt = opt.split()
        if opt[0] == "search":
            if len(opt) == 1:
                m.help_menu("search")
                continue
            else:
                if "-s" in opt or "-sort" in opt:
                    if "-title" in opt or "-t" in opt:
                        m.searchByTitleKeyword(data, opt[1], sbt=True)
                    elif "-tag" in opt:
                        m.searchByTag(data, opt[1], sbt=True)
                    elif "-excerpt" in opt or "-e" in opt:
                        m.searchInArticleExcerpt(data, opt[1], sbt=True)
                    else:
                        m.nrm_search(data, opt[1], sbt=True)
                else:
                    if "-title" in opt or "-t" in opt:
                        m.searchByTitleKeyword(data, opt[1])
                    elif "-tag" in opt:
                        m.searchByTag(data, opt[1])
                    elif "-excerpt" in opt or "-e" in opt:
                        m.searchInArticleExcerpt(data, opt[1])
                    else:
                        if opt[-1].find("-") == -1:
                            m.nrm_search(data, opt[1])
                        else:
                            print("Unknown option!")
        elif opt[0] == "help":
            if len(opt) == 1:
                m.help_menu()
            else:
                m.help_menu(opt[1])
        elif opt[0] == "update":
            data = m.update()
        elif opt[0] == "printall":
            m.printAllItem(data)
        elif opt[0] == "exit":
            break
        elif opt[0] == "info":
            m.info(data)
        else:
            print("Command not found!")


def default_mainmenu():
    global data
    opt = m.main_menu()
    while opt != 7:
        print(opt)  # operations here
        if opt == 6:
            data = m.update()
        elif opt == 5:
            m.nrm_search(data, m.getSearchString())
        elif opt == 2:
            m.searchByTitleKeyword(data, m.getSearchString())
        elif opt == 3:
            m.searchByTag(data, m.getSearchString())
        elif opt == 4:
            m.searchInArticleExcerpt(data, m.getSearchString())
        elif opt == 1:
            m.printAllItem(data)
        opt = m.main_menu()


data = m.init()
# default_mainmenu()
# m.help_menu()
command_mainmenu()
m.defaultShutdownAction()
