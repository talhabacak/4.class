# -*- coding: utf-8 -*-
"""
Created on Sat May 21 08:38:56 2022

@author: talha
"""

import time
from selenium import webdriver
#from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.keys import Keys
#from bs4 import BeautifulSoup as BS
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from openpyxl import load_workcomputer
from openpyxl import Workbook


class CrawlComputer:
    def __init__(self,url="https://www.amazon.com.tr/s?rh=n%3A12601898031&fs=true&ref=lp_12601898031_sar"):
        self.url = url 
        self.driver = self.get_driver()
        self.driver.maximize_window()
        self.computersName = []
        self.pageBefore = []
        self.pageBefore.append(["marka", "ekran_boyutu", "islemci_markasi", "islemci_hizi", "RAM_boyutu", "sabit_disk", "kart_arayuzu", "isletim_sistemi", "agirlik", "fiyat", "url", "eksik"])
        self.is_continue = True
        self.computer_num = 0
        self.name = "data_amazon.xlsx"
        self.driver.get(self.url)

    def get_driver(self):
        options = webdriver.ChromeOptions()
        print("Driver has created")
        return webdriver.Chrome(r'C:/Users/talha/Desktop/chromedriver/chromedriver.exe')

    def run(self):
        print(input("başlamak için ..."))
        
    def end(self):
        print("Toplam:", self.computer_num)
        wb = Workbook()
        page = wb.active
        count = 1
        for i in self.pageBefore:
            try:
                page.append(i)
            except:
                print(count +" . satır yazılamadı")
            count += 1
            
        try:
            wb.save(filename=self.name)
            wb.close()
        except Exception as e:
            print(e)
            print("dosya yazılamadı")
    """
            try:
                self.driver.close()
            except Exception as e:
                print(e)
    """        

    def thisCategory(self):
        try:
            count = 0
            lastpage = self.driver.current_url
            while(self.is_continue):
                try:
                    self.get_computers()
                except:
                    continue
                wait = WebDriverWait(self.driver, 40)
                self.driver.get(lastpage)
                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='search']/div[1]/div[1]/div/span[3]/div[2]/div[37]/div/div/span/a[last()]")))
                try:
                    nextpage_obj = self.driver.find_element(By.XPATH,"//*[@id='search']/div[1]/div[1]/div/span[3]/div[2]/div[37]/div/div/span/a[last()]")
                    nextpage = nextpage_obj.get_attribute("href")     
                    lastpage = nextpage
                    print("lastpage: ",lastpage)
                    wait = WebDriverWait(self.driver, 40)
                    self.driver.get(nextpage)
                    wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='search']/div[1]/div[1]/div/span[3]/div[2]/div[37]/div/div/span/a[last()]")))
                    self.end()
                except Exception as e:
                    print("hata: " + str(e))
                    self.is_continue = False
        except Exception as e:
            print("Hata: " +str(e))
        print("Bitti")

    def get_computers(self):
        computers = self.driver.find_elements(By.XPATH,"//*[@id='search']/div[1]/div[1]/div/span[3]/div[2]/div/div/div/div/div/div[1]/span/a")
        computer_list = []                              
        for computer in computers:                          
            computer_url = computer.get_attribute("href")
            computer_list.append(computer_url)
        print("bilgisayar sayısı:" ,len(computers))
        try:
            self.get_computer_info(computer_list)
        except Exception as e:
            print(e)
            
    def get_computer_info(self,computer_list):
        for computer in computer_list:                
            marka = "marka"
            ekran_boyutu = "ekran_boyutu"
            islemci_markasi = "islemci_markasi"
            islemci_hizi = "islemci_hizi"
            RAM_boyutu = "RAM_boyutu"
            sabit_disk = "sabit_disk"
            kart_arayuzu ="kart_arayuzu"
            isletim_sistemi = "isletim_sistemi"
            agirlik = "agirlik"
            fiyat = "fiyat"

            try:
                wait = WebDriverWait(self.driver, 40)
                self.driver.get(computer)
                wait.until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='productDetails_techSpec_section_1']/tbody/tr/th")))
            except:
                continue
            print(1)
            name = self.driver.find_elements(By.XPATH,"//*[@id='productDetails_techSpec_section_1']/tbody/tr/th")
            attirubutes = self.driver.find_elements(By.XPATH,"//*[@id='productDetails_techSpec_section_1']/tbody/tr/td")
            index = 0
            eksik = 9
            for att in attirubutes:                           
                if name[index].text == "Marka":
                    try:
                        marka = att.text
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                elif name[index].text == "Ekran Boyutu":
                    try:
                        ekran_boyutu = att.text.replace("İnç", "")
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                elif name[index].text == "İşlemci Markası":
                    try:
                        islemci_markasi = att.text
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                elif name[index].text == "İşlemci Hızı":
                    try:
                        islemci_hizi = att.text.replace("GHz", "")
                        islemci_hizi = islemci_hizi.replace("MHz", "")
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                elif name[index].text == "RAM Boyutu":
                    try:
                        RAM_boyutu = att.text.replace("GB", "")
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                elif name[index].text == "Sabit Disk Açıklaması":
                    try:
                        sabit_disk = att.text
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                elif name[index].text == "Ekran Kartı Arayüzü":
                    try:
                        kart_arayuzu = att.text
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                elif name[index].text == "İşletim Sistemi":
                    try:
                        isletim_sistemi = att.text
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                elif name[index].text == "Ürün Ağırlığı":
                    try:
                        agirlik = att.text.replace("kg", "")
                        agirlik = agirlik.replace("g", "")
                        eksik -= 1
                    except Exception as e:
                        print(e)
                        #print(name + " price")
                index += 1
                
            try:
                fiyat = self.driver.find_element(By.XPATH,"//*[@id='corePrice_feature_div']/div/span/span[2]/span[1]").text
                fiyat = fiyat.replace(".", "")     
                print("fiyat: ", fiyat)
            except Exception as e:
                print(e)
                #print(name + " price")
                
            flag = 1
            if marka == "marka" or ekran_boyutu == "ekran_boyutu" or islemci_markasi == "islemci_markasi" or islemci_hizi == "islemci_hizi" or RAM_boyutu == "RAM_boyutu" or sabit_disk == "sabit_disk" or kart_arayuzu == "kart_arayuzu" or isletim_sistemi == "isletim_sistemi" or agirlik == "agirlik" or fiyat == "fiyat":
                flag = 0
            
            if flag == 1:
                try:
                    self.pageBefore.append([marka, ekran_boyutu, islemci_markasi, islemci_hizi, RAM_boyutu, sabit_disk, kart_arayuzu, isletim_sistemi, agirlik, fiyat])
                    self.computer_num += 1
                    print("Toplam:", self.computer_num)
                except Exception as e:
                    print(e)
            else:
                try:
                    url = self.driver.current_url
                    self.pageBefore.append([marka, ekran_boyutu, islemci_markasi, islemci_hizi, RAM_boyutu, sabit_disk, kart_arayuzu, isletim_sistemi, agirlik, fiyat, url, str(eksik)])
                    print("Toplam:", self.computer_num)
                except Exception as e:
                    print(e)

                
if __name__ == "__main__":
    start = time.time()
    obj = CrawlComputer()
    obj.run()
    obj.thisCategory()
    obj.end()
    print(time.time() - start)