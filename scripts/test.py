import urllib.request
from bs4 import BeautifulSoup as BS

url = "https://www.ornitho.ch/index.php?m_id=15"
soup = BS(urllib.request.urlopen(url), 'lxml')
species = [str(x.text) for x in soup.find_all('option')]
print(len(species))
main_cat = [s.split(' ', 1)[0] for s in species]
print(set(main_cat))
print(len(set(main_cat)))