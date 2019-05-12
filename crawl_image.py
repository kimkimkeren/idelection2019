from multiprocessing import Pool

import pandas as pd 
import re
import requests
import pathlib
import sys
import os
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

image_url_skeleton = "https://pemilu2019.kpu.go.id/img/c/"

connection_count = 100
retry_count = 3
time_out = 30
chunk_size = 100
root_folder = "."

def download_image(link):
	write = False
	start = time.time()
	for i in range(retry_count):
		try:
			filename = link.replace(image_url_skeleton, '')
			filename = root_folder + "/" + filename
			pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
			r = requests.get(link, allow_redirects=True, verify=False, timeout=time_out)
			open(filename, 'wb').write(r.content)
			write = True
			break
		except Exception as e:
			pass
			# print("Try : " + str(i+1), file=sys.stderr)
			# print(row[-1], file=sys.stderr)
			# print(e, file=sys.stderr)
			# print("", file=sys.stderr)
		if i == retry_count-1:
			print(link, file=sys.stderr)
		else:
			time.sleep(3*(i+1))
	end = time.time()
	print(write,end-start)

data = pd.read_csv(sys.argv[1])
root_folder = sys.argv[2] if len(sys.argv) > 2 else "."
image_links_data = data[['link C1 halaman 1', 'link C1 halaman 2']]
images = data['link C1 halaman 2'].values.tolist() + data['link C1 halaman 1'].values.tolist()

print("Scanning retrieved files...", file=sys.stderr)
image_count = len(images)
print(image_count, file=sys.stderr)
current_images = []
for r, d, f in os.walk(root_folder):
	for file in f:
		file_path = os.path.join(r, file)
		file_link = image_url_skeleton + file_path.replace(root_folder + "/", "")
		if os.path.getsize(file_path) < 100000:
			os.remove(file_path)
		else:
			current_images.append(file_link)
images = list(set(images) - set(current_images))
print(len(images), file=sys.stderr)
print("Scanning retrieved files done", file=sys.stderr)

index = [i for i in range(0, len(images), chunk_size)]
index.append(len(images))
for i in range(len(index)-1):
	p = Pool(connection_count)
	p.map(download_image, images[index[i]:index[i+1]])
	p.close()