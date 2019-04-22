from multiprocessing import Pool, cpu_count

import csv
import json
import requests
import time
import urllib3



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

area_url_skeleton = "https://pemilu2019.kpu.go.id/static/json/wilayah/"
result_url_skeleton = "https://pemilu2019.kpu.go.id/static/json/hhcw/ppwp/"
image_url_skeleton = "https://pemilu2019.kpu.go.id/img/c/"

def crawl_kelurahan(data):
	result = []

	wilayah = data[0]
	wilayah_name = data[1]
	kabupaten = data[2]
	kabupaten_name = data[3]
	kecamatan = data[4]
	kecamatan_name = data[5]
	kelurahan = data[6]
	kelurahan_name = data[7]
	kelurahan_json_file = str(wilayah) + "/" + str(kabupaten) + "/" + str(kecamatan) + "/" + str(kelurahan) + ".json"
	try:
		r = requests.get(area_url_skeleton + kelurahan_json_file, verify=False, timeout=30)
		kelurahan_json = json.loads(r.text)

		for tps in kelurahan_json.keys():
			tps_name = kelurahan_json[tps].get("nama")
			tps_json_file = str(wilayah) + "/" + str(kabupaten) + "/" + str(kecamatan) + "/" + str(kelurahan) + "/" + str(tps) + ".json"
			try:
				r = requests.get(result_url_skeleton + tps_json_file, verify=False, timeout=30)
				tps_result_json = json.loads(r.text)
				if (tps_result_json != {}):
					result.append([
						wilayah_name, kabupaten_name, kecamatan_name, kelurahan_name, tps_name, tps_result_json["ts"],
						tps_result_json["pemilih_j"], tps_result_json["pengguna_j"], tps_result_json["chart"]["21"], tps_result_json["chart"]["22"],
						tps_result_json["suara_sah"], tps_result_json["suara_tidak_sah"], tps_result_json["suara_total"],
						image_url_skeleton + tps[:3] + "/" + tps[3:6] + "/" + tps + "/" + tps_result_json["images"][0],
						image_url_skeleton + tps[:3] + "/" + tps[3:6] + "/" + tps + "/" + tps_result_json["images"][1]
					])
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)

	return result

def crawl_kecamatan(wilayah, wilayah_name, kabupaten, kabupaten_name, kecamatan, kecamatan_name, kecamatan_json, writer):

	kelurahan_list = []
	for item in kecamatan_json.items():
		kelurahan_list.append((
			wilayah,
			wilayah_name,
			kabupaten,
			kabupaten_name,
			kecamatan,
			kecamatan_name,
			item[0], # kelurahan
			item[1].get("nama") # kelurahan_name
		))
	pool = Pool(processes=cpu_count()*10)
	result = pool.map(crawl_kelurahan, kelurahan_list)
	flatten_result = [item for sublist in result for item in sublist]
	pool.close()
	writer.writerows(flatten_result)

def crawl_kabupatan(wilayah, wilayah_name, kabupaten, kabupaten_name, kabupaten_json, writer):

	for kecamatan in kabupaten_json.keys():
		kecamatan_name = kabupaten_json[kecamatan].get("nama")
		kecamatan_json_file = str(wilayah) + "/" + str(kabupaten) + "/" + str(kecamatan) + ".json"
		try:
			r = requests.get(area_url_skeleton + kecamatan_json_file, verify=False, timeout=30)
			kecamatan_json = json.loads(r.text)

			print(wilayah, wilayah_name, kabupaten, kabupaten_name, kecamatan, kecamatan_name)
			crawl_kecamatan(wilayah, wilayah_name, kabupaten, kabupaten_name, kecamatan, kecamatan_name, kecamatan_json, writer)

		except Exception as e:
			print(e)

def crawl_wilayah(wilayah, wilayah_name, wilayah_json, writer):

	for kabupaten in wilayah_json.keys():
		kabupaten_name = wilayah_json[kabupaten].get("nama")
		kabupaten_json_file = str(wilayah) + "/" + str(kabupaten) + ".json"
		try:
			r = requests.get(area_url_skeleton + kabupaten_json_file, verify=False, timeout=30)
			kabupaten_json = json.loads(r.text)

			crawl_kabupatan(wilayah, wilayah_name, kabupaten, kabupaten_name, kabupaten_json, writer)

		except Exception as e:
			print(e)


if __name__ == '__main__':
	with open('result-' + time.strftime("%Y%m%d%H%M%S") + '.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["wilayah", "kabupaten", "kecamatan", "kelurahan", "tps", "timestamp",
			"jumlah pemilih", "jumlah pengguna", "pemilih jokowi", "pemilih prabowo", "jumlah suara sah",
			"jumlah suara tidak sah", "total suara", "link C1 halaman 1", "link C1 halaman 2"])

		root_json_file = "0.json"
		r = requests.get(area_url_skeleton + root_json_file, verify=False, timeout=30)
		root_json = json.loads(r.text)

		for wilayah in root_json.keys():
			wilayah_name = root_json[wilayah].get("nama")
			wilayah_json_file = str(wilayah) + ".json"
			try:
				r = requests.get(area_url_skeleton + wilayah_json_file, verify=False, timeout=30)
				wilayah_json = json.loads(r.text)

				crawl_wilayah(wilayah, wilayah_name, wilayah_json, writer)

			except Exception as e:
				print(e)

