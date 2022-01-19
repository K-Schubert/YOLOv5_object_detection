import os
import glob
import random
from shutil import copyfile

def create_trn_val_test(seed):
	
	random.seed(seed)
	path = '../data/images/birds_merged/'
	# ATM only take first 8 main species (A)
	species = os.listdir(path)[1:9]
	print(species)

	# list all image files
	all_files = []
	for s in species:
		all_files.extend(glob.glob(f'{path}{s}/*.jpg'))

	# Create random trn/val set
	trn = random.sample(all_files, int(0.8*len(all_files)))
	val = list(set(all_files) - set(trn))
	test_idx = int(0.8*len(val))
	test = val[test_idx:]
	val = val[:test_idx]

	return trn, val, test

if __name__ == '__main__':

	trn, val, test = create_trn_val_test(42)
	print(len(trn))
	print(len(val))
	print(len(test))

	# copy files to train_merged image folder
	for file in trn:
		new_name = file.split('/')[-1:]
		copyfile(file, f"../data/images/train_merged/{new_name[0]}") #{('_').join(new_name)}")

	# copy files to val_merged image folder
	for file in val:
		new_name = file.split('/')[-1:]
		copyfile(file, f"../data/images/val_merged/{new_name[0]}") #{('_').join(new_name)}")

	# copy labels to train_merged label folder
	train_path = '../data/images/train_merged/'
	for file in os.listdir(train_path)[1:]:
		label = file.replace('.jpg', '.txt')
		try:
			copyfile(f'../data/labels/all_labels/{label}', f'../data/labels/train_merged/{label}')
		except FileNotFoundError:
			continue

	# copy labels to val_merged label folder
	val_path = '../data/images/val_merged/'
	for file in os.listdir(val_path)[1:]:
		label = file.replace('.jpg', '.txt')
		try:
			copyfile(f'../data/labels/all_labels/{label}', f'../data/labels/val_merged/{label}')
		except FileNotFoundError:
			continue
