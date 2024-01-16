import json

filename = "data/kenny_data.json"

f = open(filename, encoding="utf8")
data = json.load(f)

count = 0
for item in data:
    link = item["attachments"]
    if len(link) > 0:
        url = link[0]["proxy_url"]
        count += 1

print(count)