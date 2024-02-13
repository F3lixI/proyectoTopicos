from django.shortcuts import render
from django.http import JsonResponse
import requests, json



def index(request):
    url = "https://www.floristone.com/api/rest/flowershop/getproducts?category=lr&count=1&start=1"
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

