from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import csv
from fastai.vision import download_images
import urllib.request
from bs4 import BeautifulSoup as BS

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

		time.sleep(5)

	def move_file_to_folder(self, species):
		
		folder = species
		file = "urls_" + folder + ".csv"
		dl_path = "/Users/kieranschubert/Downloads/download"
		path_to = "../data/birds/" + folder + "/"

		# Create data folders and move urls
		os.makedirs(path_to, exist_ok=True)
		os.rename(dl_path + ".csv", path_to + file)

	def download_images(self, n_images):

		path = '../data/birds/'
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
					if row and any(yr in str(row) for yr in ['2020', '2019', '2018', '2017']):
						writer.writerow(row)

			os.remove(path+folder+file)
			os.rename(path+folder+temp_csv_file, path+folder+file)

			with open(path+folder+file, 'r') as fp:
				reader = csv.reader(fp)
				print(f'nb of urls for {species}: ', len(list(reader)))

			download_images(path+folder+file, path+folder, max_pics=n_images)

			print(f'nb of downloaded images for {species}: ', len(os.listdir(path+folder))-1)


if __name__ == '__main__':

	bird = BirdScraper()

	driver = webdriver.Chrome()

	species_list = bird.species_names[:10]
	for species in species_list:
		bird.urls_to_csv(driver, species)
		species = species.replace(' ', '_')
		print(species)
		time.sleep(5)
		bird.move_file_to_folder(species)
	
	driver.quit()

	bird.download_images(n_images=100)

