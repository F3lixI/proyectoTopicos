import requests

categories = ["bs", "ao", "bd", "an", "lr", "gw", "nb", "ty", "sy", "c", "o", "v", "r", "x",
              "p", "b", "fbs", "fa", "fb", "fs", "fp", "fl", "fw", "fh", "fx", "fc", "fu"]

# URL base del API
base_url = "https://www.floristone.com/api/rest/flowershop/getproducts?category="

# Diccionario para almacenar el total de productos por categoría
total_productos_por_categoria = {}

'''
# Iterar sobre todas las categorías y hacer la llamada al API para obtener el total de productos
for categoria in categories:
    url = base_url + categoria
    headers = {
        'Authorization': 'Basic NTkzOTE5Okhpc0VFbQ==',
        'Cookie': 'CFID=49269679; CFTOKEN=da0434cbd367fbc8-D8BBFBE5-E0A4-F32B-6374406A26AE16E7; JSESSIONID=03CA41F72A86539F70B7400157C72110.cfusion'
    }
    response = requests.get(url, headers=headers)
    total_productos = response.json()['TOTAL']
    total_productos_por_categoria[categoria] = total_productos

# Imprimir el diccionario resultante
print(total_productos_por_categoria)
'''

dict = {'bs': 98, 'ao': 194, 'bd': 231, 'an': 205, 'lr': 140, 'gw': 172, 'nb': 77, 'ty': 174, 'sy': 199, 'c': 30, 'o': 11, 'v': 63, 'r': 25, 'x': 2, 'p': 19, 'b': 9, 'fbs': 63, 'fa': 84, 'fb': 49, 'fs': 36, 'fp': 19, 'fl': 3, 'fw': 21, 'fh': 7, 'fx': 5, 'fc': 25, 'fu': 4}



