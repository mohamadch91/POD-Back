import json
import requests

provinces = json.load(open('proviences_a.json'))

provinces = provinces['data']

temp =[]
city=[]
for i in range(len(provinces)):
    province ={
        "model": "api.Province",
        "pk": i+1,
        "fields": {
            "value": provinces[i]['label']
        }
    }
    temp.append(province)
    print(str(i)+("done"))
    response =requests.get('https://api.goldiranasayesh.com/api/v2/Affiliation/GetCityList?Id='+str(provinces[i]['value']))
    response= response.json()["data"]
    for j in range (len(response)):
        city.append({
            "model": "api.City",
            "pk": len(city)+1,
            "fields": {
                "province": i+1,
                "value": response[j]['label']
            }
        })
    print(provinces[i]['label']+("done"))


with open('province.json', 'w') as f:
    json.dump(temp, f)

with open('city.json', 'w') as f:
    json.dump(city, f)


