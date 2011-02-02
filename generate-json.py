from os import *
from os.path import *
import re
try:
    import json
except:
    import simplejson as json


def getBouncerPlatform(arch):
    mapping = {
        'Darwin_Universal-gcc3': 'osx',
        'Darwin_x86-gcc3-u-ppc-i386': 'osx',
        'Linux_x86-gcc3': 'linux',
        'WINNT_x86-msvc': 'win'
    }
    return mapping[arch]

def getFTPPlatform(arch):
    mapping = {
        'Darwin_Universal-gcc3': 'mac',
        'Darwin_x86-gcc3-u-ppc-i386': 'mac',
        'Linux_x86-gcc3': 'linux-i686',
        'WINNT_x86-msvc': 'win32'
    }
    return mapping[arch]

def readFile(f):
    fd = open(join(f),O_RDONLY)
    snip = read(fd,1000)
    close(fd)
    return snip

def getParameter(data, linestart):
    # eg or a snippet containting 'build=20101203075014' and linestart='build'
    # return '20101203075014'
    for line in data.splitlines():
        if line.startswith(linestart):
            return line.split('=')[1]
    return None

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-w","--walk", dest="walkdir", help="snippet directory to walk for data")
    parser.add_option("-n","--name", dest="name", help="name of the release we're capturing")
    parser.add_option("-p","--partial", dest="partial", help="name of the release we have partials from")

    options, args = parser.parse_args()
    if not options.walkdir or not isdir(options.walkdir):
        parser.error('Must specify a directory to read with -w/--walk, eg Firefox/3.6.12')
    if not options.name:
        parser.error('Must specify the name of the release we capturing, eg Firefox-3.6.13-build1')
    if not options.partial:
        parser.error('Must specify the name of the release we have partials for, eg Firefox-3.6.12-build1')

    relData = {"platforms": {}}

    # start with platforms
    platforms = sorted(listdir(options.walkdir))
    for platform in platforms:
        buildIDs = sorted(listdir(join(options.walkdir,platform)))
        # read snippets from last build of previous release
        if buildIDs:
            buildID = buildIDs[-1]
        else:
            continue
        base = join(options.walkdir,platform,buildID)
        relData["platforms"][platform] = {}

        # get params for all platforms
        snip = readFile(join(base,'en-US','betatest','partial.txt'))
        relData["platforms"][platform]["buildID"] = getParameter(snip,'build')
        relData["platforms"][platform]["OS_BOUNCER"] = getBouncerPlatform(platform)
        relData["platforms"][platform]["OS_FTP"] = getFTPPlatform(platform)

        relData["platforms"][platform]["locales"] = {}
        locales = listdir(base)
        for locale in locales:
#            if locale != "en-US":
#                continue
            lrelData =  relData["platforms"][platform]["locales"][locale] = {}
            lbase = join(base,locale,'betatest')
            snipFiles = listdir(lbase)
            for snipFile in snipFiles:
                type,ext = splitext(snipFile)
                lrelData[type] = {}
                snip = readFile(join(lbase,snipFile))
                if type == 'partial':
                    lrelData[type]["from"] = options.partial
                else:
                    lrelData[type]["from"] = "*"
                lrelData[type]["filesize"] = getParameter(snip,'size')
                lrelData[type]["hashValue"] = getParameter(snip,'hashValue')


    print "data is:"
    print json.dumps(relData, sort_keys=True, indent=4)