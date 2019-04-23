from multiprocessing import Pool, cpu_count

import pandas as pd 
import re
import requests
import pathlib
import sys
import os

image_url_skeleton = "https://pemilu2019.kpu.go.id/img/c/"

def download_image(link):
	try:
		r = requests.get(link, allow_redirects=True, verify=False, timeout=30)
		filename = link.replace(image_url_skeleton, '')
		pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
		open(filename, 'wb').write(r.content)
	except Exception as e:
		print(e)


data = pd.read_csv(sys.argv[1])
image_links_data = data[['link C1 halaman 1', 'link C1 halaman 2']]
for _, image_links in image_links_data.iterrows():
	download_image(image_links['link C1 halaman 1'])
	download_image(image_links['link C1 halaman 2'])