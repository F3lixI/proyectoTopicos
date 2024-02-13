import requests
import sqlite3

# Creación BD
conn = sqlite3.connect('floreria.db')
c = conn.cursor()

# Creación de tablas
c.execute('''CREATE TABLE IF NOT EXISTS productos
             (id INTEGER PRIMARY KEY, code TEXT, small_image TEXT, price REAL, description TEXT, dimension TEXT, large_image TEXT, extra_large_image TEXT, service TEXT, category TEXT, name TEXT)''')


c.execute('''CREATE TABLE IF NOT EXISTS categorias
             (id INTEGER PRIMARY KEY, producto_id INTEGER, display TEXT, categoria TEXT,
             FOREIGN KEY (producto_id) REFERENCES productos (id))''')

conn.close()

# Conexion a la BD
conn = sqlite3.connect('floreria.db')
c = conn.cursor()

# Diccionario para almacenar el total de productos por categoría
total_productos_por_categoria = {'bs': 98, 'ao': 194, 'bd': 231, 'an': 205, 'lr': 140, 'gw': 172, 'nb': 77, 'ty': 174, 'sy': 199, 'c': 30, 'o': 11, 'v': 63, 'r': 25, 'x': 2, 'p': 19, 'b': 9, 'fbs': 63, 'fa': 84, 'fb': 49, 'fs': 36, 'fp': 19, 'fl': 3, 'fw': 21, 'fh': 7, 'fx': 5, 'fc': 25, 'fu': 4}

# URL base del API
base_url = "https://www.floristone.com/api/rest/flowershop/getproducts?category={categoria}&count={total}&start=1"

headers = {
        'Authorization': 'Basic NTkzOTE5Okhpc0VFbQ==',
        'Cookie': 'CFID=49269679; CFTOKEN=da0434cbd367fbc8-D8BBFBE5-E0A4-F32B-6374406A26AE16E7; JSESSIONID=03CA41F72A86539F70B7400157C72110.cfusion'
    }

# Iteración sobre todas las categorías y hacer la llamada al API para obtener los productos
for categoria, total in total_productos_por_categoria.items():
    
    url = base_url.format(categoria=categoria, total=total)
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    for producto in data['PRODUCTS']:
        
        c.execute("INSERT INTO productos (code, small_image, price, description, dimension, large_image, extra_large_image, service, category, name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (producto['CODE'], producto['SMALL'], producto['PRICE'], producto['DESCRIPTION'], producto['DIMENSION'], producto['LARGE'], producto['EXTRALARGE'], producto['SERVICE'], data['CATEGORY'], producto['NAME']))
        producto_id = c.lastrowid
        
        
        for categoria_producto in producto['CATEGORIES']:
            c.execute("INSERT INTO categorias (producto_id, display, categoria) VALUES (?, ?, ?)",
                      (producto_id, categoria_producto['DISPLAY'], categoria_producto['CATEGORY']))

# Guardar cambios
conn.commit()
conn.close()