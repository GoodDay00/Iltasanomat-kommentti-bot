import requests
import urllib.request
import time
import fuctions
from bs4 import BeautifulSoup

class vote:
    def __init__(self, url):
        self.url = url
        self.vastaukset = []

    def getVoteSite(self):
        splitted = self.url.split("-")
        id = splitted[1].split(".")
        self.ID = int(id[0])

        site = requests.get(self.url)
        soup = BeautifulSoup(site.text, "html.parser")
        kysymys = soup.find("h4", class_="cf")
        self.kysymys = kysymys.get_text()
        vastaukset = soup.find("div", class_="survey-buttons").findAll("button", recursive=False)
        for nappi in vastaukset:
            self.vastaukset.append(nappi.get_text())
        self.printKysymykset()
    
        print("Kyselyä ei löytynyt tuosta linkistä!")
        exit()

    def printKysymykset(self):
        print('Kysymys: {}'.format(self.kysymys))
        i = 0
        while i < len(self.vastaukset):
            print('{}. {} '.format(i, self.vastaukset[i]))
            i+=1
        try:
            vastaus = input("Anna vastauksen numero jolle haluat antaa pisteitä: ")
            self.valittuVastaus = int(vastaus)
            self.lähetäVastauksia()
        except Exception as e:
            print("Antamasi arvo ei käy vastauksiin. {}".format(str(e)))

    def lähetäVastauksia(self):
        määrä = input("Anna haluamasi äänten määrä: ")
        try:
            body = {"surveyId": self.ID,"index": self.valittuVastaus}
            headers = {'Content-type': 'application/json; charset=UTF-8'}
            for i in range(int(määrä)):
                r = requests.post("https://www.is.fi/rest/quick-survey/vote", json=body, headers=headers)
                if r.status_code != 200:
                    print("Ei toimi")
                else:
                    fuctions.progress(i,int(määrä), "Lisätään ääniä")
            
            exit()

        except Exception as e:
            print(f"Äänten annossa on jokin vika :( {str(e)}")


            


