import requests
from bs4 import BeautifulSoup
from typing import List,Dict
import os,sys
import django

url="https://countrycode.org/"

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from app.models import CountryCode

def get_codes()->List[Dict]:
    res=[]
    with requests.Session() as session:  
        req=session.get(url)
        content=req.content
        soup=BeautifulSoup(content,'html.parser')
        table=soup.find('table',class_="main-table")
        rows=table.find_all('tr')
        for index,row in enumerate(rows):
            if index==0:
                continue
            data=row.find_all('td')
            _res={
                "country":data[0].find('a').text.upper(),
                "country_code":data[1].text,
                "iso_code":data[2].text
            }
            res.append(_res)
    return res

if __name__=="__main__":
    data=get_codes()
    for _data in data:
        CountryCode.objects.create(
            country=_data['country'],
            country_code=_data['country_code'],
            iso_code=_data['iso_code']
        )