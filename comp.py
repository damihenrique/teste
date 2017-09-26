from flask import Flask, redirect, url_for, request, render_template
from bs4 import BeautifulSoup
import requests
import os, time
from threading import Thread

app = Flask(__name__)

def getNumPages(uID):

	page = requests.get('https://www.urionlinejudge.com.br/judge/pt/profile/' + str(uID))
	soup = BeautifulSoup(page.content, 'html.parser')

	pp = str(soup.find('div', id='table-info'))
	nu = ""

	for x in range(28, 30):
		if pp[x].isdigit():
			nu += pp[x]

	return int(nu)

listURL = []
v1 = []
v2 = []

def read_url(url, quem):
	page = requests.get(url)
	listURL.append(page)
	soup = BeautifulSoup(page.content, 'html.parser')
	tr = soup.find_all('tr')
	
	for x in range(1, 29):
		linha = str(tr[x].find_all('td')[0].find('a'));
		lenn = len(linha)
		idx = linha.find('>')
		num = linha[idx+1:idx+5]
		if num != 'None':
			if quem == 0:
				v1.append(num)
			if quem == 1:
				v2.append(num)


def getProblems(uID, quem, qtPag):	
	for pagNum in range(1, qtPag+1):
		t = Thread(target=read_url, args=('https://www.urionlinejudge.com.br/judge/pt/profile/' + str(uID) + '?page='+str(pagNum), quem))
		t.start()
		time.sleep(0.1)
		

def func(user1, user2):
	qt1 = getNumPages(user1)
	qt2 = getNumPages(user2)
	getProblems(user1, 0, qt1)
	getProblems(user2, 1, qt2)
	while len(listURL) < (qt1+qt2):
		aaa = 1
	time.sleep(2)
	ret = list(set(v1) - set(v2))
	v1.clear()
	v2.clear()
	listURL.clear()
	return ret

@app.route("/")
def init():
    return render_template('index.html')

@app.route('/compara/<user1>_<user2>')   
def comparador(user1, user2):	
	res = func(user1, user2)
	return render_template('result.html', result = sorted(res))

@app.route('/compara',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user1 = request.form['id1']
		user2 = request.form['id2']
		return redirect(url_for('comparador',user1 = user1, user2 = user2)) #nome da função (comparador)
	else:
		user = request.args.get('id1')
		return redirect(url_for('comparador',name = user1, user2 = user2))

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
	#app.run()