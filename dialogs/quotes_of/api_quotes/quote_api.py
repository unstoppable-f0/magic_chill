import requests

url = "https://andruxnet-random-famous-quotes.p.rapidapi.com/"

querystring = {"cat":"movies","count":"10"}

headers = {
	"X-RapidAPI-Key": "76f997a4e8mshbdfe0309475341cp12b8c0jsn33d856f2d5a6",
	"X-RapidAPI-Host": "andruxnet-random-famous-quotes.p.rapidapi.com"
}

response = requests.post(url, headers=headers, params=querystring)

print(response.json())