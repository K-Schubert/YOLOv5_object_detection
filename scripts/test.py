import os
import csv


path = 'data/birds/'
folders = os.listdir(path)[1:]

for species in folders:
	
	folder = species + "/"
	file = os.listdir(path + folder)

	# Check for hidden .DS_Store file
	if len(file) > 1:
		file = file[1]
	else:
		file = file[0]

	temp_csv_file = file[:-4] + '_tmp' + file[-4:]

	with open(path+folder+file, 'r') as inp, open(path+folder+temp_csv_file, 'w') as out:
		writer = csv.writer(out)
		for row in csv.reader(inp):
			if row and 'www.ornitho.ch/2020' in row:
				writer.writerow(row)

	os.remove(path+folder+file)
	os.rename(path+folder+temp_csv_file, path+folder+file)