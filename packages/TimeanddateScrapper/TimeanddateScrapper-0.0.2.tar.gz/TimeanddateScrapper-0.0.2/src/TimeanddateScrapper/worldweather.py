import os
import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

class Weather:
    def _city_temp_extractor(self,elem):
        temp = elem[len(elem)-3:-1]
        if temp[0] == '0':
            temp = temp[1]
        city =""
        for ele in elem:
            if ele.isalpha() or ele == ' ':
                city+=ele
            else:
                break
        city = city[:-1]
        return [city,temp,str(datetime.now())] 
    
    def saveToExcel(self):
        lis = self.worldWideReport()
        df = pd.DataFrame(data = lis,columns = ['City','Temparature-in-Celcius','Extraction-Datetime'])
        df.to_csv('weather.csv')
        print(f"Data saved in {os.getcwd()}\\weather.csv")
        
    def worldWideReport(self):
        url= 'https://www.timeanddate.com/weather/'
        page = requests.get(url)
        print(page)
        soup =  BeautifulSoup(page.content,'html.parser')
        table = soup.find_all('tr')
        unfiltered_weather_list1 = []
        unfiltered_weather_list2 = []
        final_weather_list = []
        for i in range(len(table)):
            if i == 0:
                continue
            text = table[i].getText()
            weather_text = text.split('°C')
            unfiltered_weather_list1.append(weather_text[0])
            unfiltered_weather_list2.append(weather_text[1])
            
        for elem in unfiltered_weather_list1:
            final_weather_list.append(self._city_temp_extractor(elem))
        for elem in unfiltered_weather_list2:
            final_weather_list.append(self._city_temp_extractor(elem)) 

        return final_weather_list
        
        