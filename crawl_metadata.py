from multiprocessing import Pool, cpu_count

import json
import requests
import urllib3
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def flatten(data):
	return [item for sublist in data for item in sublist]

def expand(row):
	result = []
	try:
		r = requests.get(row[-1], verify=False, timeout=30)
		skeleton = row[-1].split('.json')[0]
		json_data = json.loads(r.text)
		for key, value in json_data.items():
			temp = [value['nama'], skeleton + '/' + key + '.json']
			temp = row[:-1] + temp
			result.append(temp)
	except Exception as e:
		print(e)
	return result

if __name__ == '__main__':
	area_url_skeleton = "https://pemilu2019.kpu.go.id/static/json/wilayah/"
	result_url_skeleton = "https://pemilu2019.kpu.go.id/static/json/hhcw/ppwp/"
	root_json_file = '0.json'
	r = requests.get(area_url_skeleton + root_json_file, verify=False, timeout=30)
	json_data = json.loads(r.text)

	result_wilayah = []
	for key, value in json_data.items():
		result_wilayah.append([value['nama'], area_url_skeleton + key + '.json'])

	pd.DataFrame(result_wilayah, columns=['wilayah','link']).to_csv('result-wilayah.csv', index=False)

	p = Pool(cpu_count()*10)
	result_kabupaten = flatten(p.map(expand, result_wilayah))
	p.close()
	pd.DataFrame(result_kabupaten, columns=['wilayah','kabupaten','link']).to_csv('result-kabupaten.csv', index=False)

	p = Pool(cpu_count()*10)
	result_kecamatan = flatten(p.map(expand, result_kabupaten))
	p.close()
	pd.DataFrame(result_kecamatan, columns=['wilayah','kabupaten','kecamatan','link']).to_csv('result-kecamatan.csv', index=False)

	p = Pool(cpu_count()*10)
	result_kelurahan = flatten(p.map(expand, result_kecamatan))
	p.close()
	pd.DataFrame(result_kelurahan, columns=['wilayah','kabupaten','kecamatan','kelurahan','link']).to_csv('result-kelurahan.csv', index=False)

	p = Pool(cpu_count()*10)
	result_tps = flatten(p.map(expand, result_kelurahan))
	p.close()
	# change link
	df = pd.DataFrame(result_tps, columns=['wilayah','kabupaten','kecamatan','kelurahan','link'])
	df['link'] = df['link'].str.replace(area_url_skeleton, result_url_skeleton)
	df.to_csv('result-tps.csv', index=False)
