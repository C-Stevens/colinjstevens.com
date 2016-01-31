from bs4     import BeautifulSoup

HTML_PARSER = "html5lib"
tabFiles = {
    'about' : open("about.html"),
    'cv' : open("cv.html"),
    'contact' : open("contact.html"),
}
tabData = {}

for key in tabFiles.keys():
    tabData[key] = BeautifulSoup(tabFiles[key], HTML_PARSER)

print(tabData['about'].body)
print(tabData['cv'].body)
print(tabData['contact'].body)