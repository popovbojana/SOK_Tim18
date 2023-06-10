Softverski obrasci i komponente - Tim 18

Clanovi tima:
1. Filip Vuksan SV1/2020
2. Danilo Babic SV42/2020
3. Andrea Katzenberger SV69/2020
4. Bojana Popov SV70/2020

Izvorisni plugini:
1. Plugin za parsiranje XML fajla u graf (xml_parser folder)
2. Plugin za parsiranje JSON fajla u graf (json_parser folder)

Plugini za vizuelizaciju:
1. Plugin za jednostavnu vizuelizaciju (visualisation_simple folder)
2. Plugin za kompleksnu vizuelzaciju (visualisation_complex folder)

Instalacija projekta:
1. Napraviti novo virtuelno okruzenje i aktivirati ga (komande: python -m venv ime_okruzenja, 
ime_okruzenja\Scripts\activate)
3. Uraditi pip install wheel, django, jinja2
(Svi plugini se instaliraju pozicioniranjem u glavni folder komponente i komandom python setup.py install):
4. Instalirati prvo data_core plugin
5. Instalirati xml_parser, json_parser, visualisation_simple i visualisation_complex plugine
3. Pozicionirati se u django_project folder terminalom
4. Pokrenuti redom komande:
               python manage.py makemigrations data_core_app
               python manage.py migrate
               python manage.py runserver


