from django.shortcuts import render
from django.http import JsonResponse
import requests, json



def welcome(request):
    url = "https://www.floristone.com/api/rest/flowershop/welcome"
    payload = {}
    headers = {
      'Authorization': 'Basic NTkzOTE5Okhpc0VFbQ==',
      'Cookie': 'CFID=49269679; CFTOKEN=da0434cbd367fbc8-D8BBFBE5-E0A4-F32B-6374406A26AE16E7; JSESSIONID=03CA41F72A86539F70B7400157C72110.cfusion'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    
    # Devuelve la respuesta como JSON
    return JsonResponse(response.json())


def flower_detail(request):
    url = "https://www.floristone.com/api/rest/flowershop/getproducts?code=F1-509"
    headers = {
        'Authorization': 'Basic NTkzOTE5Okhpc0VFbQ==',
        'Cookie': 'CFID=49269679; CFTOKEN=da0434cbd367fbc8-D8BBFBE5-E0A4-F32B-6374406A26AE16E7; JSESSIONID=03CA41F72A86539F70B7400157C72110.cfusion'
    }
    response = requests.get(url, headers=headers)
    
    print(response.text)  # Imprime la respuesta para verificar su contenido
    
    try:
        data = response.json()
        flowers = data['PRODUCTS']
    except ValueError as e:
        print("Error al decodificar la respuesta como JSON:", e)
        flowers = []
        
    return render(request, 'flower_detail.html', {'flowers': flowers})

def index(request):
    products = [
        {
            "CODE": "F1-509",
            "PRICE": 74.95,
            "RECIPIENT": {
                "ZIPCODE": "11779"
            }
        }
    ]
    
    # Codificar la lista de productos en JSON
    products_json = json.dumps(products)
    
    # Construir la URL con los datos JSON codificados
    url = f"https://www.floristone.com/api/rest/flowershop/gettotal?products={products_json}"
    
    headers = {
        'Authorization': 'Basic NTkzOTE5Okhpc0VFbQ==',
        'Cookie': 'CFID=49269679; CFTOKEN=da0434cbd367fbc8-D8BBFBE5-E0A4-F32B-6374406A26AE16E7; JSESSIONID=03CA41F72A86539F70B7400157C72110.cfusion'
    }
    
    response = requests.get(url, headers=headers)
    
    return JsonResponse(response.json())