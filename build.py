from bs4 import BeautifulSoup
try:
    from termcolor import colored
except ImportError:
    vprint("Failed to import coloring library. Defaulting to boring terminal output.")

HTML_PARSER = "html5lib"
indexFile = open("index.html")
tabFiles = {
    'about' : open("about.html"),
    'cv' : open("cv.html"),
    'contact' : open("contact.html"),
}
tabData = {}

#TODO
#   * Make backup of index file before creation

def vprint(s, **args):
    '''Wrapper for print() in case I decide to add fancy debug prints later.'''
    print(s, **args)

def makeSoups():
    vprint("Loading source files...")

    vprint("\t* loading index... ", end="")
    indexSoup = BeautifulSoup(indexFile, HTML_PARSER)
    vprint(colored("done.", 'green'))

    for key in tabFiles.keys():
        vprint("\t* loading {0}... ".format(tabFiles[key].name), end="")
        tabData[key] = BeautifulSoup(tabFiles[key], HTML_PARSER)
        vprint(colored("done.", 'green'))

def build():
    makeSoups()

if __name__ == "__main__":
    vprint("Beginning build\n---------------")
    build()
    vprint("---------------\nBuild complete.") #TODO: Check for build errors
print(tabData['about'].body)
print(tabData['cv'].body)
print(tabData['contact'].body)