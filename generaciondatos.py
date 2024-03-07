import csv
import random
from faker import Faker
from datetime import datetime

fake = Faker()

start_date = datetime(2015, 1, 1)
end_date = datetime(2024, 12, 31)

with open('usuarios.csv', 'w', newline='') as csvfile:
    fieldnames = ['password', 'username', 'nombre', 'apellido', 'email', 'fecha_creacion', 'telefono', 'edad', 'sexo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Genera 50 usuarios
    for _ in range(200):
        password = fake.password()
        username = fake.user_name()
        nombre = fake.first_name()
        apellido = fake.last_name()
        email = fake.email()
        fecha_creacion = fake.date_time_between_dates(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')
        telefono = fake.phone_number().replace(' ', '').replace('-', '')[:10]
        edad = random.randint(18, 80)
        sexo = random.choice(['H', 'M', 'X'])

        
        writer.writerow({
            'password': password,
            'username': username,
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'fecha_creacion': fecha_creacion,
            'telefono': telefono,
            'edad': edad,
            'sexo': sexo
        })


