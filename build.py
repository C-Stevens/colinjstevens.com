import re
import tempfile

OUTFILE = open("index.html", 'w')
BASEFILE = open("index_base.html")

def vprint(s, indentNum=0, **args):
    '''Print wrapper, allows argument based indenting.'''
    print("{0}{1}".format(("\t"*indentNum), s), **args)

def extractBody(f):
    '''Creates a string array of the lines in a file `f` between lines containing "<body>",
    and "</body>".'''
    output = []
    read = False
    for l in f.readlines():
        if "<body>" in l:
            read = True
            continue # Avoid appending "<body>" to output
        elif "</body>" in l:
            read = False
        if read:
            output.append(l)
    return output

def buildIndex():
    '''Matches lines in `BASEFILE` against a regex match, attempts to open files based on
    matches and write their contents into a temporary file. Returns a temporary file
    handler.'''
    tmp = tempfile.TemporaryFile(mode='r+', encoding='UTF-8')
    vprint("Scanning `{0}` for build comments...".format(BASEFILE.name), 1)
    for line in BASEFILE.readlines():
        result = re.match('\s*<!--##BUILD:(\s)?(?P<filePath>.*)##-->', line)
        if result:
            filePath = result.groupdict()['filePath']
            vprint("* Found build comment. Inserting body content from `{0}`... ".format(filePath), 2, end="")
            try:
                sourceFile = open(filePath)
            except FileNotFoundError as e:
                vprint("failed ({0})".format(e))
                continue
            for l in extractBody(sourceFile):
                tmp.write(l)
            sourceFile.close()
            vprint("done")
        else:
            tmp.write(line)
    tmp.seek(0)
    vprint("Index concatenated.", 1)
    return tmp


if __name__ == "__main__":
    vprint("Building index...")
    tmp = buildIndex()
    OUTFILE.write(tmp.read())
    # Cleanup
    tmp.close()
    BASEFILE.close()
    OUTFILE.close()
    vprint("Build complete.") #TODO: Check for build errors
