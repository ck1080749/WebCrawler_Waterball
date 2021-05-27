import my_module_001 as m
import json

def command_mainmenu():
    opt = input("command> ").split()

def default_mainmenu():
    global data
    opt = m.main_menu()
    while opt != 7:
        print(opt)#operations here
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
default_mainmenu()
#m.help_menu()
m.defaultShutdownAction()