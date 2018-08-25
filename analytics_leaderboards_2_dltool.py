import json
import urllib.request


urlg = "https://api.faforever.com/data/globalRating" \
      "?fields[globalRating]=deviation,mean" \
      "&page[size]=10000" \
      "&page[number]="
urll = "https://api.faforever.com/data/ladder1v1Rating" \
      "?fields[ladder1v1Rating]=deviation,mean" \
      "&page[size]=10000" \
      "&page[number]="
url = urll
download = True

data = []
if download:
    for p in range(1, 100):  # page
        print(url + str(p))
        with urllib.request.urlopen(url + str(p)) as j:
            new = json.loads(j.read())
            new = new['data']
            data = data + new
        print(new)
        if new.__len__() == 0:
            break
    with open('data/ladderleaderboard.json', 'w') as outfile:
        json.dump(data, outfile)
print(data)
