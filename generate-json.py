from distutils.version import StrictVersion
import hashlib
import os
from os import walk, read, close, listdir, O_RDONLY, stat
from os.path import isdir, join, splitext
import re
try:
    import json
    assert json # to shut pyflakes up
except:
    import simplejson as json

IGNORE_PLATFORMS = ('WINCE_arm-msvc',)

platform_map = {
    ('Linux_x86-gcc3',): {
        'bouncer': 'linux',
        'ftp': 'linux-i686',
        'buildbot': 'linux'
    },
    ('Linux_x86_64-gcc3',): {
        'bouncer': 'linux64',
        'ftp': 'linux-x86_64',
        'buildbot': 'linux64'
    },
    ('Darwin_x86-gcc3-u-ppc-i386', 'Darwin_ppc-gcc3-u-ppc-i386'): {
        'bouncer': 'osx',
        'ftp': 'mac',
        'buildbot': 'macosx'
    },
    ('Darwin_x86-gcc3-u-i386-x86_64', 'Darwin_x86_64-gcc3-u-i386-x86_64'): {
        'bouncer': 'osx',
        'ftp': 'mac',
        'buildbot': 'macosx64'
    },
    ('WINNT_x86-msvc',): {
        'bouncer': 'win',
        'ftp': 'win32',
        'buildbot': 'win32'
    },
    ('WINNT_x86_64-msvc',): {
        'bouncer': 'win64',
        'ftp': 'win64',
        'buildbot': 'win64'
    }
}

deprecated_platform_map = {
    ('Darwin_x86_64-gcc3',): {
        'bouncer': 'osx64',
        'ftp': 'mac64',
        'buildbot': 'macosx64'
    },
    ('Darwin_Universal-gcc3',): {
        'bouncer': 'osx',
        'ftp': 'mac',
        'buildbot': 'macosx'
    }
}

def isMac(platform, version):
    if platform in ('osx', 'mac', 'macosx') or 'Universal' in platform or 'u-ppc-i386' in platform or \
      'u-i386-x86_64' in platform:
        return True
    if platform == 'macosx64' and versionGte(version, '4.0b7'):
        return True
    return False

def isMac64(platform, version):
    if platform in ('osx64', 'mac64') or 'Darwin_x86_64' in platform:
        return True
    if platform == 'macosx64' and versionLt(version, '4.0b7'):
        return True
    return False

# StrictVersion _almost_ works for all of our version numbers. Exceptions are:
#  - RCs, which we deal with by converting them to really high numbered betas
#  - 4 part version numbers (FIXME)
def cmpVersions(left, right):
    left = StrictVersion(re.sub('rc(\d+)', 'b9999999\\1', left))
    right = StrictVersion(re.sub('rc(\d+)', 'b9999999\\1', right))
    return cmp(left, right)

def versionLt(left, right):
    return cmpVersions(left, right) == -1

def versionGte(left, right):
    return cmpVersions(left, right) >= 0

def getPlatforms(platform, version):
    # This part is a little hairy because so many of the platform definitions
    # are overloaded on Mac. To cope, this function returns any possible matches
    # for the platforms, and leaves it up to the caller to decide which one
    # they want.
    def findPlatforms(pmap, p):
        r = []
        for k,v in pmap.iteritems():
            if p in k or p in v.values():
                r.append((k, v))
        if r:
            return r
        else:
            return [((),{})]

    # Mac universal builds have changed a few times, so we need to do some
    # hunting through version numbers to figure out what platforms to return.
    if isMac(platform, version):
        # Older universal builds use the old style mapping
        if (version.startswith('3.5') and versionLt(version, '3.5.16')) or \
          (version.startswith('3.6') and versionLt(version, '3.6.13')) or \
          versionLt(version, '4.0b5'):
            return findPlatforms(deprecated_platform_map, platform)[0]
        # Newer 3.5, 3.6, and a couple of 4.0 builds are ppc+i386
        # which are uniquely identifiable by "macosx"
        if (version.startswith('3.5') and versionGte(version, '3.5.16')) or \
          (version.startswith('3.6') and versionGte(version, '3.6.13')) or \
          version in ('4.0b5', '4.0b6'):
            return findPlatforms(platform_map, 'macosx')[0]
        # And anything past that is i386+x86_64 universal, which are uniquely
        # identifiable by "macosx64"
        return findPlatforms(platform_map, 'macosx64')[0]
    # These builds are deprecated, so we have to use that platform map for them
    elif isMac64(platform, version):
        return findPlatforms(deprecated_platform_map, platform)[0]
    # Non-mac platforms are simple, and always use the main platform map
    else:
        return findPlatforms(platform_map, platform)[0]

def ftp2update(platform, version):
    u = getPlatforms(platform, version)[0]
    if not u:
        raise Exception("Couldn't find update platforms for ftp platform '%s'" % platform)
    return u

def update2bouncer(platform, version):
    try:
        return getPlatforms(platform, version)[1]['bouncer']
    except KeyError:
        raise KeyError("Couldn't find bouncer platform for update platform '%s'" % platform)

def update2ftp(platform, version):
    try:
        return getPlatforms(platform, version)[1]['ftp']
    except KeyError:
        raise KeyError("Couldn't find ftp platform for update platform '%s'" % platform)

def update2buildbot(platform, version):
    try:
        return getPlatforms(platform, version)[1]['buildbot']
    except KeyError:
        raise KeyError("Couldn't find buildbot platform for update platform '%s'" % platform)

def readFile(f):
    fd = os.open(join(f), O_RDONLY)
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

def readBuildId(info):
    data = open(info).readline()
    return data.split('=')[1].strip()

def getInfoFile(bbPlatform):
    return "%s_info.txt" % bbPlatform

def hashFile(filename, hash_type):
    '''Return the 'hash_type' hash of a file at 'filename' '''
    h = hashlib.new(hash_type)
    f = open(filename, "rb")
    while True:
        data = f.read(1024)
        if not data:
            break
        h.update(data)
    f.close()
    hash = h.hexdigest()
    return hash

def processCandidatesDir(d, version, partial, exclude_partials, hash_func, locales, relData):
    for root, dirs, files in walk(join(d, 'update')):
        for f in files:
            mar = join(root, f)
            if not mar.endswith('.mar'):
                continue
            marType = mar.rsplit('.', 2)[1]
            if marType == 'partial' and exclude_partials:
                continue

            undef, ftpPlatform, locale, filename = mar.rsplit('/', 3)
            # If we've got a specific list of locales that we care about,
            # skip anything not in the list.
            if locales and locale not in locales:
                continue
            updatePlatforms = ftp2update(ftpPlatform, version)
            for updatePlatform in updatePlatforms:
                bbPlatform = update2buildbot(updatePlatform, version)
                if updatePlatform not in relData["platforms"]:
                    relData["platforms"][updatePlatform] = {}
                    relData["platforms"][updatePlatform]["locales"] = {}
                p = relData["platforms"][updatePlatform]
                p["buildID"] = readBuildId(join(d, getInfoFile(bbPlatform)))
                p["OS_BOUNCER"] = update2bouncer(updatePlatform, version)
                p["OS_FTP"] = ftpPlatform

                if locale not in p["locales"]:
                    p["locales"][locale] = {}
                lrelData = p["locales"][locale]
                lrelData[marType] = {}
                if marType == "complete":
                    lrelData[marType]["from"] = "*"
                else:
                    lrelData[marType]["from"] = partial
                lrelData[marType]["filesize"] = str(stat(mar).st_size)
                lrelData[marType]["hashValue"] = hashFile(mar, hash_func)

def processSnippetDir(walkdir, platform, version, partial, exclude_partials, locales, relData):
    buildIDs = sorted(listdir(join(walkdir,platform)))
    # read snippets from last build of previous release
    if buildIDs:
        buildID = buildIDs[-1]
    else:
        return
    base = join(walkdir,platform,buildID)
    relData["platforms"][platform] = {}

    # get params for all platforms
    snip = readFile(join(base,'en-US','betatest','partial.txt'))
    relData["platforms"][platform]["buildID"] = getParameter(snip,'build')
    relData["platforms"][platform]["OS_BOUNCER"] = update2bouncer(platform, version)
    relData["platforms"][platform]["OS_FTP"] = update2ftp(platform, version)

    relData["platforms"][platform]["locales"] = {}
    for locale in listdir(base):
        # If we've got a specific list of locales that we care about,
        # skip anything not in the list.
        if locales and locale not in locales:
            continue
        lrelData =  relData["platforms"][platform]["locales"][locale] = {}
        lbase = join(base,locale,'betatest')
        snipFiles = listdir(lbase)
        for snipFile in snipFiles:
            type,ext = splitext(snipFile)
            if exclude_partials and type == 'partial':
                continue
            lrelData[type] = {}
            snip = readFile(join(lbase,snipFile))
            if type == 'partial':
                lrelData[type]["from"] = partial
            else:
                lrelData[type]["from"] = "*"
            lrelData[type]["filesize"] = getParameter(snip,'size')
            lrelData[type]["hashValue"] = getParameter(snip,'hashValue')


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-w","--walk", dest="walkdir", help="snippet directory to walk for data")
    parser.add_option("-n","--name", dest="name", help="name of the release we're capturing")
    parser.add_option("-p","--partial", dest="partial", help="name of the release we have partials from")
    parser.add_option("-e","--exclude-partials", dest="exclude_partials", action="store_true", help="exclude partials where we fake them")
    parser.add_option("-v", "--version", dest="version", help="version being processed")
    parser.add_option("--hash-func", dest="hash_func", default="sha512")
    parser.add_option("-l", "--limit-locale", dest="locales", action="append", default=[], help="Limit locales to only those specified. This option may be passed multiple times. If not specified, all locales will be processed")

    options, args = parser.parse_args()
    if not options.walkdir or not isdir(options.walkdir):
        parser.error('Must specify a directory to read with -w/--walk, eg Firefox/3.6.12')
    if not options.name:
        parser.error('Must specify the name of the release we capturing, eg Firefox-3.6.13-build1')
    if not options.exclude_partials and not options.partial:
        parser.error('Must specify the name of the release we have partials, eg Firefox-3.6.12-build1, if not excluding partials')

    relData = {"name": options.name, "platforms": {}}

    # start with platforms
    if options.walkdir.startswith('build'):
        processCandidatesDir(options.walkdir, options.version, options.partial, options.exclude_partials, options.hash_func, options.locales, relData)
    else:
        for d in sorted(listdir(options.walkdir)):
            if d in IGNORE_PLATFORMS:
                continue
            else:
                processSnippetDir(options.walkdir, d, options.version, options.partial, options.exclude_partials, options.locales, relData)

    print json.dumps(relData, sort_keys=True, indent=4)


