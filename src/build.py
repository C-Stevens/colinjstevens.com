import sys, re, tempfile

BUILD_DIR = ""
OUTFILE_STR = "index.html"
BASEFILE_STR = "index_base.html"
OUTFILE = None
BASEFILE = None
runError = False

def vprint(s, indentNum=0, **args):
    '''Print wrapper, allows argument based indenting.'''
    print("{0}{1}".format(("\t"*indentNum), s), **args)

def baseSetup():
    '''Basic preliminary setup before building.'''
    global runError
    global BUILD_DIR
    global OUTFILE
    global BASEFILE
    try:
        BUILD_DIR = sys.argv[1]
        OUTFILE = open("{0}/{1}".format(BUILD_DIR, OUTFILE_STR), 'w')
        BASEFILE = open("{0}/{1}".format(BUILD_DIR, BASEFILE_STR))
    except FileNotFoundError as e:
        vprint("failed ({0})".format(e))
        runError = True

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
    global runError
    tmp = tempfile.TemporaryFile(mode='r+', encoding='UTF-8')
    vprint("- Scanning `{0}` for build comments...".format(BASEFILE.name), 1)
    for line in BASEFILE.readlines():
        result = re.match('\s*<!--##BUILD:(\s)?(?P<filePath>.*)##-->', line)
        if result:
            filePath = result.groupdict()['filePath']
            vprint("* Found build comment. Inserting body content from `{0}`... ".format(filePath), 2, end="")
            try:
                sourceFile = open("{0}/{1}".format(BUILD_DIR,filePath))
            except FileNotFoundError as e:
                vprint("failed ({0})".format(e))
                runError = True
                continue
            for l in extractBody(sourceFile):
                tmp.write(l)
            sourceFile.close()
            vprint("done")
        else:
            tmp.write(line)
    tmp.seek(0)
    return tmp


if __name__ == "__main__":
    vprint("Beginning pre-build setup... ", end="") 
    baseSetup()
    if not runError:
        vprint("done")
        vprint("Building index...")
        if not runError:
            tmp = buildIndex()
            OUTFILE.write(tmp.read())
            vprint("- Index concatenated.", 1)
        vprint("Cleaning up... ", end="")
        tmp.close()
        BASEFILE.close()
        OUTFILE.close()
        vprint("done")
        if not runError:
            vprint("Build successfully completed.")
            exit(0)
    vprint("Build ended with error(s).")
    exit(1)
