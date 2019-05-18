from multiprocessing import Pool

import csv
import json
import requests
import time
import urllib3
import pandas as pd
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

connection_count = 300
retry_count = 3
time_out = 5
chunk_size = 300

area_url_skeleton = "https://pemilu2019.kpu.go.id/static/json/wilayah/"
result_url_skeleton = "https://pemilu2019.kpu.go.id/static/json/hhcw/ppwp/"
image_url_skeleton = "https://pemilu2019.kpu.go.id/img/c/"

def expand(row):
	result = []
	write = False
	start = time.time()
	for i in range(retry_count):
		try:
			r = requests.get(row[-1], verify=False, timeout=time_out)
			skeleton = row[-1].split('.json')[0]
			tps = skeleton.split('/')[-1]
			tps_result_json = json.loads(r.text)
			if tps_result_json != {}:
				c1_image_1 = image_url_skeleton + tps[:3] + "/" + tps[3:6] + "/" + tps + "/" + tps_result_json["images"][0] \
					if len(tps_result_json["images"]) > 0 and tps_result_json["images"][0] is not None else None
				c1_image_2 = image_url_skeleton + tps[:3] + "/" + tps[3:6] + "/" + tps + "/" + tps_result_json["images"][1] \
					if len(tps_result_json["images"]) > 0 and tps_result_json["images"][0] is not None else None
				result = [
					tps_result_json["ts"],
					tps_result_json["pemilih_j"], tps_result_json["pengguna_j"], tps_result_json["chart"]["21"], tps_result_json["chart"]["22"],
					tps_result_json["suara_sah"], tps_result_json["suara_tidak_sah"], tps_result_json["suara_total"], c1_image_1, c1_image_2
				]
				result = row[:-1] + result
			write = True
			break
		except Exception as e:
			pass
			# print("Try : " + str(i+1), file=sys.stderr)
			# print(row[-1], file=sys.stderr)
			# print(e, file=sys.stderr)
			# print("", file=sys.stderr)
		if i == retry_count-1:
			print(",".join([str(item) for item in row]), file=sys.stderr)
		else:
			time.sleep(3*(i+1))
	end = time.time()
	print(write,end-start)
	return result


if __name__ == '__main__':
	result_tps_df = pd.read_csv(sys.argv[1])
	result_tps = result_tps_df.values.tolist()

	if len(sys.argv) > 2:
		recap = pd.read_csv(sys.argv[2])
		result_tps = pd.merge(
				result_tps_df, recap,
				on=['wilayah','kabupaten','kecamatan','kelurahan','tps'],
				how='outer', indicator=True
			).query(
				"_merge == 'left_only'"
			).reset_index()[['wilayah','kabupaten','kecamatan','kelurahan','tps','link']].values.tolist()

	index = [i for i in range(0, len(result_tps), chunk_size)]
	index.append(len(result_tps))
	with open('recap-tps-' + time.strftime("%Y%m%d%H%M%S") + '.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["wilayah", "kabupaten", "kecamatan", "kelurahan", "tps", "timestamp",
			"jumlah pemilih", "jumlah pengguna", "pemilih jokowi", "pemilih prabowo", "jumlah suara sah",
			"jumlah suara tidak sah", "total suara", "link C1 halaman 1", "link C1 halaman 2"])
		for i in range(len(index)-1):
			p = Pool(connection_count)
			recap_tps = p.map(expand, result_tps[index[i]:index[i+1]])
			recap_tps = [item for item in recap_tps if len(item) > 0]
			p.close()
			writer.writerows(recap_tps)