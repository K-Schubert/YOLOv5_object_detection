from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import csv
from fastai.vision import download_images
import urllib.request
from bs4 import BeautifulSoup as BS

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DownloadImages():

	def __init__(self):
		self.species_names = self.get_species_names()

	def get_species_names(self):

		url = "https://www.ornitho.ch/index.php?m_id=15"
		soup = BS(urllib.request.urlopen(url), 'lxml')
		species = [str(x.text) for x in soup.find_all('option')]
		#species = [s.replace(' ', '_') for s in species]
		return species
		

	def urls_to_csv(self, driver, url=None):
		
		url = "https://www.ornitho.ch/index.php?m_id=7&langu=fr"
		script = 'var urls=[];var a=document.getElementsByTagName("img");for (var i=0,l=a.length;i<l;i++){	if (/\\.(jpg)$/im.test(a[i].getAttribute("src")))	{	urls.push(a[i].getAttribute("src"));}};let csv = "data:text/csv;charset=utf-8," + urls.join("\\n");var encodedUri = encodeURI(csv);window.open(encodedUri);'

		driver.get(url)

		inputElement = driver.find_element_by_id("qselectspecies")
		inputElement.send_keys(self.species_names[0])
		time.sleep(2)
		#inputElement.send_keys(Keys.RETURN)
		#inputElement.submit()

		#WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='col-sm-2 text-center']//input[@type='button']"))).click()
		#button = driver.find_element_by_class_name("submit")
		print('waiting 10s')
		#my_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(button))
		
		wait = WebDriverWait(driver, 10)
		confirm = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='col-sm-2 text-center']//input[@type='button']")))
		confirm.click()

		time.sleep(2)
		print('click')
		confirm.click()
		time.sleep(2)
		print('return')
		confirm.send_keys(Keys.RETURN)
		time.sleep(2)
		print('enter')
		confirm.send_keys(Keys.ENTER)
		time.sleep(2)
		#print('submit')
		#confirm.submit()



		time.sleep(5)

		for i in range(5):
			driver.execute_script("window.scrollTo(0, 40000);")
			time.sleep(3.5)

		driver.execute_script(script)

		time.sleep(5)

	def move_file_to_folder(self, bird_name):
		
		folder = bird_name
		file = "urls_" + folder + ".csv"
		dl_path = "/Users/kieranschubert/Downloads/download"
		path_to = "data/birds/" + folder + "/"

		# Create data folders and move urls
		os.makedirs(path_to, exist_ok=True)
		os.rename(dl_path + ".csv", path_to + file)

	def download_images(self, n_images):

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
					if row:
						writer.writerow(row)

			os.remove(path+folder+file)
			os.rename(path+folder+temp_csv_file, path+folder+file)

			with open(path+folder+file, 'r') as fp:
				reader = csv.reader(fp)
				print(f'nb of urls for {species}: ', len(list(reader)))

			download_images(path+folder+file, path+folder, max_pics=n_images)

			print(f'nb of downloaded images for {species}: ', len(os.listdir(path+folder))-1)


if __name__ == '__main__':

	bird = DownloadImages()

	driver = webdriver.Chrome()

	bird.urls_to_csv(driver)
	bird_names = [s.replace(' ', '_') for s in bird.species_names]
	bird.move_file_to_folder(bird_names[0])
	bird.download_images(n_images=10)

	driver.quit()




'''
var urls=[];
var a=document.getElementsByTagName('img');
for (var i=0,l=a.length;i<l;i++)
{
	if (/\.(jpg)$/im.test(a[i].getAttribute('src')))
	{
		urls.push(a[i].getAttribute('src'));
	}
}

let csv = "data:text/csv;charset=utf-8," 
	+ urls.join("\n")

var encodedUri = encodeURI(csv);
window.open(encodedUri);
'''
