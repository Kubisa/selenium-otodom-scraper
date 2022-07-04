from otodom import otodom
from otodom.otodom import Otodom

city=input('What city are you intrested in?\n')

scraper=Otodom()
scraper.openPage()
scraper.search(city)
results = scraper.scrape()

print(f'\n\nNumber of offers found: {results[0]}\n')
print(f'Average price per square meter: {results[1]}')

