from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os
import csv
from fastai.vision import download_images
import urllib.request
from bs4 import BeautifulSoup as BS
import shutil
import glob

'''
This module allows to scrap bird images from www.ornitho.ch and download them into separate species folders.
'''


class BirdScraper():

	def __init__(self):
		self.species_names = self.get_species_names()

	def get_species_names(self):

		url = "https://www.ornitho.ch/index.php?m_id=15"
		soup = BS(urllib.request.urlopen(url), 'lxml')
		species = [str(x.text) for x in soup.find_all('option')]
		return species

	def urls_to_csv(self, driver, species):
		
		url = "https://www.ornitho.ch/index.php?m_id=7&langu=fr"
		script = 'var urls=[];var a=document.getElementsByTagName("img");for (var i=0,l=a.length;i<l;i++){	if (/\\.(jpg)$/im.test(a[i].getAttribute("src")))	{	urls.push(a[i].getAttribute("src"));}};let csv = "data:text/csv;charset=utf-8," + urls.join("\\n");var encodedUri = encodeURI(csv);window.open(encodedUri);'

		driver.get(url)

		inputElement = driver.find_element_by_id("qselectspecies")

		ActionChains(driver).click(inputElement) \
							.send_keys(species) \
							.key_up(Keys.CONTROL) \
							.send_keys(Keys.ENTER) \
							.perform()

		time.sleep(8)

		driver.find_element_by_xpath("//input[contains(@onclick,'form_filter_action')]").click()

		time.sleep(5)

		for i in range(7):
			driver.execute_script("window.scrollTo(0, 40000);")
			time.sleep(3.5)

		driver.execute_script(script)

		time.sleep(7)

	def move_file_to_folder(self, species):
		
		folder = species
		file = "urls_" + folder + ".csv"
		dl_path = "/Users/kieranschubert/Downloads/download"
		path_to = "../data/birds/" + folder + "/"

		# Create data folders and move urls
		os.makedirs(path_to, exist_ok=True)
		os.rename(dl_path + ".csv", path_to + file)

	def download_images(self, species_list, n_images):

		path = '../data/birds/'
		# folders = os.listdir(path)[1:]

		yrs = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', \
				'2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000']

		check = ['https://cdnmedia3.biolovision.net/www.ornitho.ch/2020-08/small/8772-20965643-1245.jpg',
		'https://cdnmedia3.biolovision.net/www.ornitho.ch/2020-08/small/9924-20965108-6490.jpg', 
		'https://cdnmedia3.biolovision.net/www.ornitho.ch/2020-08/small/687-20986514-2909.jpg',
		'https://cdnmedia3.biolovision.net/www.ornitho.ch/2020-08/small/687-20986510-8124.jpg',
		'https://cdnmedia3.biolovision.net/www.ornitho.ch/2020-08/small/687-20986442-2776.jpg']

		for species in species_list:
			
			folder = species + "/"

			try:
				if not glob.glob(f'{path}{folder}/*.jpg'):
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
							if row and any([yr in str(row) for yr in yrs]):
								writer.writerow(row)

					os.remove(path+folder+file)
					os.rename(path+folder+temp_csv_file, path+folder+file)

					# If csv file has specific urls, delete dir with sub-species
					# Some species don't have images so the scraper dls images of
					# all species mixed. The pattern of urls in this scenario is
					# detected and these species are removed.

					with open(path+folder+file,'r') as inp:
						existingLines = [line for line in csv.reader(inp)]
					
					check1 = any([check[0] in line for line in existingLines])
					check2 = any([check[1] in line for line in existingLines])
					#check3 = any([check[2] in line for line in existingLines])
					#check4 = any([check[3] in line for line in existingLines])
					#check5 = any([check[4] in line for line in existingLines])

					#if check1 and check2 and check3 and check4 and check5:
					if check1 and check2:
						shutil.rmtree(path+folder)
						#continue
					else:
						# Check nb of urls per species
						with open(path+folder+file, 'r') as fp:
							reader = csv.reader(fp)
							print(f'nb of urls for {species}: ', len(list(reader)))

						# Download images
						download_images(path+folder+file, path+folder, max_pics=n_images)
						print(f'nb of downloaded images for {species}: ', len(os.listdir(path+folder))-1)
						time.sleep(30)

			except FileNotFoundError:
				continue

	def enable_download_in_headless_chrome(self, download_dir):
	    
	    self.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

	    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
	    self.execute("send_command", params)
	    self.set_window_size(1024, 768)


if __name__ == '__main__':

	chrome_options = Options()
	chrome_options.add_argument("--headless")

	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.enable_download_in_headless_chrome("/Users/kieranschubert/Downloads/")

	bird = BirdScraper()

	# driver = webdriver.Chrome(options=option)

	# 57, 368, 479, 541 missing
	species_list = bird.species_names
	for species in species_list:
		bird.urls_to_csv(driver, species)
		species = species.replace(' ', '_')
		print(species)
		time.sleep(5)
		bird.move_file_to_folder(species)
	
	driver.quit()

	# species_list = os.listdir('../data/birds/')[1:]
	# bird.download_images(species_list, n_images=100)

