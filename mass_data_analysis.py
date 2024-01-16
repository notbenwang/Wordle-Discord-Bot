from urllib.request import Request, urlopen
import numpy as np
import cv2
import requests
from detect_score import score_from_image

file1 = "data/ben_data.txt"
file2 = "data/kenny_data.txt"
file3 = "data/michael_data.txt"

input_filename = file3
outlier_output_filename = "michael_outliers.txt"
detailed_results_output_filename = "michael_detailed_results.txt"
summary_results_filename = "michael_summary_results.txt"

f = open(input_filename, "r")
lines = f.readlines()

results = {'1': [0, []], '2': [0, []], '3': [0, []], '4': [0, []], '5': [0, []], '6': [0, []]}
outliers = []

for url in lines:
    response = requests.get(url)
    try:
        req = urlopen(Request(url, headers={'User-Agent': 'Modzilla/5.0'}))
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        score, _ = score_from_image(img)
        if score != "None" and score <= 6:
            results[str(score)][0] += 1
            results[str(score)][1].append(url)
            print("Score:",score)
        else:
            outliers.append(url)
    except:
        outliers.append(url)

with open(outlier_output_filename, 'w') as f:
    for url in outliers:
        f.write(url)

with open(detailed_results_output_filename, 'w') as f:
    for score in results:
        links = results[score][1]
        for link in links:
            f.write(score + " " + link)

with open(summary_results_filename, 'w') as f:
    f.write(f"{len(outliers)} / {len(lines)}\n")
    for num in results:
        s = str(results[num][0])
        f.write((num+" "+s+"\n"))
        print(num, s)
