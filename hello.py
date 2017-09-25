from flask import Flask, redirect, url_for, request, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def getProblems(uID):	

	v = []
	pagNum = 1
	
	while True:

		page = requests.get('https://www.urionlinejudge.com.br/judge/pt/profile/' + str(uID) + '?page='+str(pagNum));
		
		if page.status_code != 200:
			return v
			
		soup = BeautifulSoup(page.content, 'html.parser')
		tr = soup.find_all('tr')
        
		for x in range(1, 29):
			linha = str(tr[x].find_all('td')[0].find('a'));
			lenn = len(linha)
			idx = linha.find('>')
			num = linha[idx+1:idx+5]
			if num != 'None':
				v.append(num)
		
		pagNum = pagNum + 1;

def func(user1, user2):
    v1 = getProblems(user1)
    v2 = getProblems(user2)
    return list(set(v1) - set(v2))


@app.route('/compara/<user1>_<user2>')   
def comparador(user1, user2):	
	res = func(user1, user2)
	return render_template('result.html', result = sorted(res))

@app.route('/compara',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user1 = request.form['id1']
      user2 = request.form['id2']
      return redirect(url_for('comparador',user1 = user1, user2 = user2)) #nome fa função (comparador)
   else:
      user = request.args.get('id1')
      return redirect(url_for('comparador',name = user1, user2 = user2))

if __name__ == '__main__':
   app.run(debug = True)