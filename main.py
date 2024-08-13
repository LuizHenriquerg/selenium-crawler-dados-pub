from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import logging
import time

class CrawlerBcbGov:

    def __init__(self) -> None:
        logging.info(f'[{datetime.now()}] Iniciando robô scrapping..')

        self.options = Options()
        self.options.set_preference("browser.download.folderList", 2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", '/Users/luizhenrique/Documents/my_projects/auto_wpp/csvs')
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

        self.driver = webdriver.Firefox(options=self.options)
    
    def execute(self):
        self.driver.get('https://dadosabertos.bcb.gov.br/dataset?res_format=CSV')

        time.sleep(10)

        while True:
            if 'A sua requisição foi rejeitada.' in self.driver.page_source:
                self.driver.refresh()
                time.sleep(4)
                continue

            break
        
        links = self.driver.find_elements(By.CSS_SELECTOR, "ul.dataset-list li div h3 a")
        links_list = [link.get_attribute('href') for link in links]
        
        # Iterar sobre os links e baixar os arquivos
        for link in links_list:
            self.driver.get(link)

            while True:
                if 'A sua requisição foi rejeitada.' in self.driver.page_source:
                    self.driver.refresh()
                    time.sleep(4)
                    continue

                break

            csv_links = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.dropdown')

            self.driver.execute_script("window.scrollBy(0, 200);")

            for csv in csv_links:
                try:
                    csv.click()
                    csv.find_element(by=By.CSS_SELECTOR, value="ul li a").click()
                    time.sleep(3)
                except:
                    print('Arquivo não é um CSV!')
            
            time.sleep(5)

if __name__ == '__main__':
    CrawlerBcbGov().execute()