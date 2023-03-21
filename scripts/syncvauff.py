import json
from multiprocessing.pool import ThreadPool
from PIL import Image
import urllib.request
import os

# Get map list
vauffMapList = {}
# Get json from url
with urllib.request.urlopen("https://vauff.com/mapimgs/list.php") as url:
    data = json.loads(url.read().decode())
    vauffMapList = data

print('Loaded vauff map list')

def LevenshteinDistance(string1, string2):
    matrix = []

    for i in range(len(string1) + 1):
        matrix.append([i])

    for j in range(1, len(string2) + 1):
        matrix[0].append(j)

    for i in range(1, len(string1) + 1):
        for j in range(1, len(string2) + 1):
            if string1[i - 1] == string2[j - 1]:
                matrix[i].append(matrix[i - 1][j - 1])
            else:
                matrix[i].append(min(matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1]) + 1)

    return matrix[len(string1)][len(string2)]

def getVauffMapImageURL(map, appId):
    trimmedMap = map[:31]
    bestMatch = ''
    bmLevenshteinDist = 999

    # Loop through all map names and find the one that is the closest match
    for mapImageName in vauffMapList[str(appId)]:
        mapImageNameLower = mapImageName.lower()
        distance = LevenshteinDistance(trimmedMap, mapImageNameLower)

        if distance < bmLevenshteinDist and trimmedMap.startswith(mapImageNameLower):
            bestMatch = mapImageName
            bmLevenshteinDist = distance

    if bestMatch == '':
        return ''
    else:
        return 'https://vauff.com/mapimgs/' + str(appId) + '/' + bestMatch.replace(' ', '%20') + '.jpg'

# Get image from url
def getImage(map):
    url = getVauffMapImageURL(map, 730)
    # Check url empty
    if (url == ''):
        print(f"{map} not found")
        return
    response = urllib.request.urlopen(url)
    image = Image.open(response)
    # Get image resolution from stream
    width, height = image.size
    if (width != 1920 or height != 1080):
        print(f"{map} image is not 1920x1080")
        return
    # Save image to file
    print(f'Saving {map}...')
    image.save(f"../images/{map}.jpg")

# Init Thead pool
pool = ThreadPool(10)

# Read map & match the image
mapList = []
with open('mapcycle.txt', 'r') as f:
    list = f.readlines()
    for map in list:
        map = map.strip()
        # Check file exists
        if (os.path.exists(f'../images/{map}.jpg')): continue
        mapList.append(map)

# Join get image pool
pool.map(getImage, mapList)
