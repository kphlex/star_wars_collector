import json, requests



def get_item(request):
    resp = requests.get('https://swapi.dev/api/')
    data = resp.json()

    for key, value in data.iteritems():
        print (key , value)