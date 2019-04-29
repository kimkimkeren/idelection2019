from multiprocessing import Pool, cpu_count

import json
import requests
import urllib3
import pandas as pd
import time
import os
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conn_multiplier = 5
retry_count = 10
sleep_time = 1
time_out = 15

def flatten(data):
	return [item for sublist in data for item in sublist]

def expand(row):
	result = []
	for i in range(retry_count):
		try:
			r = requests.get(row[-1], verify=False, timeout=time_out)
			skeleton = row[-1].split('.json')[0]
			json_data = json.loads(r.text)
			for key, value in json_data.items():
				temp = [value['nama'], skeleton + '/' + key + '.json']
				temp = row[:-1] + temp
				result.append(temp)
		except Exception as e:
			pass
			# print("Try : " + str(i+1), file=sys.stderr)
			# print(row[-1], file=sys.stderr)
			# print(e, file=sys.stderr)
			# print("", file=sys.stderr)
		if not result == []:
			print(row[-1] + " success!")
			break
		elif i == retry_count-1:
			print(row[-1] + " failed to be crawled", file=sys.stderr)
		else:
			time.sleep(sleep_time)
	return result

if __name__ == '__main__':

	area_url_skeleton = "https://pemilu2019.kpu.go.id/static/json/wilayah/"
	result_url_skeleton = "https://pemilu2019.kpu.go.id/static/json/hhcw/ppwp/"

	if not os.path.isfile('result-wilayah.csv'):
		root_json_file = '0.json'
		json_data = None
		for i in range(retry_count):
			try:
				r = requests.get(area_url_skeleton + root_json_file, verify=False, timeout=time_out)
				json_data = json.loads(r.text)
			except Exception as e:
				pass
				# print("Try : " + str(i+1), file=sys.stderr)
				# print(root_json_file, file=sys.stderr)
				# print(e, file=sys.stderr)
				# print("", file=sys.stderr)
			if result == []:
				time.sleep(sleep_time)
			elif i == retry_count-1:
				print(root_json_file + " failed to be crawled", file=sys.stderr)
			else:
				print(root_json_file + " success!")
				break

		for key, value in json_data.items():
			result_wilayah.append([value['nama'], area_url_skeleton + key + '.json'])

		pd.DataFrame(result_wilayah, columns=['wilayah','link']).to_csv('result-wilayah.csv', index=False)
	else:
		result_wilayah = pd.read_csv('result-wilayah.csv').values.tolist()


	if not os.path.isfile('result-kabupaten.csv'):
		p = Pool(conn_multiplier * cpu_count())
		result_kabupaten = flatten(p.map(expand, result_wilayah))
		p.close()
		pd.DataFrame(result_kabupaten, columns=['wilayah','kabupaten','link']).to_csv('result-kabupaten.csv', index=False)
	else:
		result_kabupaten = pd.read_csv('result-kabupaten.csv').values.tolist()

	if not os.path.isfile('result-kecamatan.csv'):
		p = Pool(conn_multiplier * cpu_count())
		result_kecamatan = flatten(p.map(expand, result_kabupaten))
		p.close()
		pd.DataFrame(result_kecamatan, columns=['wilayah','kabupaten','kecamatan','link']).to_csv('result-kecamatan.csv', index=False)
	else:
		result_kecamatan = pd.read_csv('result-kecamatan.csv').values.tolist()

	if not os.path.isfile('result-kelurahan.csv'):
		p = Pool(conn_multiplier * cpu_count())
		result_kelurahan = flatten(p.map(expand, result_kecamatan))
		p.close()
		pd.DataFrame(result_kelurahan, columns=['wilayah','kabupaten','kecamatan','kelurahan','link']).to_csv('result-kelurahan.csv', index=False)
	else:
		result_kelurahan = pd.read_csv('result-kelurahan.csv').values.tolist()

	if not os.path.isfile('result-tps.csv'):
		p = Pool(conn_multiplier * cpu_count())
		result_tps = flatten(p.map(expand, result_kelurahan))
		p.close()
		# change link
		df = pd.DataFrame(result_tps, columns=['wilayah','kabupaten','kecamatan','kelurahan','tps','link'])
		df['link'] = df['link'].str.replace(area_url_skeleton, result_url_skeleton)
		df.to_csv('result-tps.csv', index=False)
	else:
		result_tps = pd.read_csv('result-tps.csv').values.tolist()