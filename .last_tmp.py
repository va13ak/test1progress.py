from time import sleep
from datetime import date
from datetime import datetime
import sys
import os
#import requests
import base64
import sqlite3

def progress():
	values = range(0, 100)
	for i in values:
		print ("\rComplete: ", i, "%", end="")
		sleep(0.001)
	print ("\rComplete: 100%")
	print(sys.version_info)
	print(os.path.abspath(sys.argv[0]))
	print(os.path.abspath(
			os.path.dirname(sys.argv[0])))
	
def get_p24api(str):
	return requests.get(
			'https://api.privatbank.ua/p24api/' + str)

def get_nb_сurrencies_rates():
	d = date.fromordinal(date.today().toordinal()-7)
	r = get_p24api('exchange_rates?json&date='
					+ d.strftime("%d.%m.%Y"))
	#print(r.text)
	print(r.json())
	#print(j)
	#print(j['exchangeRate'])

def get_privat_currencies_rates():
    pass
	#r = get_p24api('pubinfo?exchange&json&coursid=11')
	#print(r.json())
	#for k in r.json():
	#	print("{ccy}: {buy} / {sale}".format(**k))
	
#https://stackoverflow.com/questions/26745462/python-request-basic-auth-doesnt-worko

def stpos_auth(login, password):
    pass
	#return requests.auth.HTTPBasicAuth(login, password)

def stpos_auth_string(login, password):
	return base64.b64encode(
				(login + ':' + password).encode()
			).decode()

def stpos_headers():
	return {'content-type':'application/json'}
				
def stpos_headers_with_auth(login, password):
	headers = stpos_headers()
	auth_string = 'Basic '
	auth_string += stpos_auth_string(login, password)
	headers['Authorization'] = auth_string
	return headers
					

def get_stpos_price_list_new():
	hostname = 'en.smarttouchpos.eu'
	auth = ('us136', '123')
	#r = requests.get('http://' + hostname
		#+ '/webapi/func_call/pos_price_list_new/0',
		#auth=stpos_auth(*auth),
		#headers = stpos_headers())headers = stpos_headers_with_auth(*auth))
	#print(r.json())
	#print(r)
	#for k in r.json()['result']:
	#	print("{name} {price} {gi_id} {mg_id}".format(
		#		**k))

def get_db_connection():
	path = os.path.abspath(
				os.path.dirname(sys.argv[0]))
	path = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/db'
	#return sqlite3.connect(path + '/' + 'test.db')
	return sqlite3.connect(path + '/te5t.db')

	
def create_db_notebook():
	db = get_db_connection()
	c = db.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS notebook2'
	#c.execute('CREATE TABLE notebook2'
				+ ' (date text, note text)')
	db.commit()
	db.close()
		
def write_to_db():
	create_db_notebook()
	note = input('input your note: ')
	db = get_db_connection()
	c = db.cursor()
	#c.execute('CREATE TABLE IF NOT EXISTS notebook'
	#			+ ' (date text, note text)')
	c.execute('INSERT INTO notebook2 values(?, ?)',
				(datetime.now().isoformat(
					timespec='milliseconds'
				),
				note))
	db.commit()
	db.close()
	
def read_from_db():
	db = get_db_connection()
	c = db.cursor()
	for row in c.execute('SELECT * FROM notebook2'):
		print(row)
	c.close()
	
		
menu = {
	1: ['get nb currencies rates',
			get_nb_сurrencies_rates],
	2: ('get privat currencies rates',
			get_privat_currencies_rates),
	3: ('get stpos pricelist',
			get_stpos_price_list_new),
	4: ('run progressbar demo',
			progress),
	5: ('write to db', write_to_db),
	6: ('read from db', read_from_db),
	0: ('to quit', )
}

while True:
	for k, v in menu.items():
		print('{0} - {1}'.format(k, v[0]))
	r = input('make your choice:')
	if r.isdigit():
		if int(r) == 0:
			break
		else:
			func = menu.get(int(r), ('',None))[1]
			if func != None: func()