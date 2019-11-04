# Returns the length requirement of the hashValue field corresponding to the hash function
def getHashLen(hashName):
    hashLen = {"sha256": 64, "sha384": 96, "sha512": 128}
    return hashLen[hashName.lower()]
