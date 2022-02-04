from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for
import configparser
from flask import request
import random

class Gam:
    def __init__(self):
        self.los = 0
        self.block = 0
        self.block1 = 0
        self.build = []
        self.counter = 0
        self.day = 0
        self.level = 2
        self.numofcurrentplayer = 0
        self.bankrotes = ['банкротов пока нет']
        self.transactions = [[], [], [], []]
        self.users_cond = []
        self.dead = 'банкротов пока нет'
        self.spisochek = []
        self.end = 0

    def info(self):
        total = ['''1)имя 2)кол-во цехов 3)кол-во сырья 4)кол-во истребителей 5)кол-во деняк''']
        for n in self.users_cond:
            total.append( '1)' + str(n[0]) + '     2)' + str(n[2]) + '     3)' + str(n[3]) + '     4)' + str(n[4]) + '     5)'+ str(n[5]) + '''''')
        return total

    def first_motion(self):
        if self.day != 0 and self.block == 0:

            for i in range(self.numofcurrentplayer):
                self.users_cond[i][5] -= 1000 * self.users_cond[i][2]
                self.users_cond[i][5]-= 300 * self.users_cond[i][3]
                self.users_cond[i][5] -= 500 * self.users_cond[i][4]
                if self.users_cond[i][5] < 0 or self.users_cond[i][4] < 0 or self.users_cond[i][3] < 0 or self.users_cond[i][2] < 0:
                    if self.bankrotes == ['банкротов пока нет']:
                        self.bankrotes = []
                    self.bankrotes.append(self.users_cond[i])
                    self.numofcurrentplayer -= 1
            for h in self.bankrotes:
                if self.dead == 'банкротов пока нет' and len(h) >= 1:
                    self.dead = ''

                if self.bankrotes != ['банкротов пока нет']:
                    self.dead += h[0]
                    self.users_cond.remove(h)

            for u in range(len(self.build)):
                self.build[u][2] -= 1
                if self.build[u][2] == 0:
                    for lo in range(self.numofcurrentplayer):
                        if self.users_cond[lo][1] == self.build[u][0]:
                            self.users_cond[lo][4] += self.build[u][1]

            levupc = open('levupgradechanses', 'r').readlines()
            for i in range(len(levupc)):
                if i != len(levupc) - 1:
                    levupc[i] = levupc[i][:len(levupc[i]) - 1:]
            current = levupc[self.level].split(' ')
            for t in range(len(current)):
                try:
                    if random.randint(int(current[t][0]), int(current[t][2::])) == 1:
                        print(int(current[t][2::]))
                        self.level = t
                        break
                except Exception:
                    print(2)
        if self.day == self.end or self.numofcurrentplayer <= 1:
            self.los = 1

        else:
            op = open('levinfo.txt', 'r').readlines()
            for i in range(len(op)):
                if i != len(op) - 1:
                    op[i] = op[i][:len(op[i]) - 1:]
            current = op[self.level].split(' ')
            information = ['''Предложений сырья: ''' + str(int(float(current[0]) * self.numofcurrentplayer)), 'Минимальная цена сырья: ' + str(int(float(current[1]))), 'Спрос на истребители: ' + str(int(float(current[2]) * self.numofcurrentplayer)), 'Максимальная цена за истребитель: ' + str(int(float(current[3])))]
            self.block = 1
            self.block1 = 0
            return [information, 'банкроты на текущий момент: ' + self.dead]


    def collect_usage(self,ip, g, m, mode):
        self.transactions[mode].append([ip, g, m])



    def checker(self):
        for ol in range(self.numofcurrentplayer):
            if self.users_cond[ol][1] == request.environ.get('HTTP_X_REAL_IP', request.remote_addr) and request.environ.get('HTTP_X_REAL_IP', request.remote_addr) not in self.spisochek:
                self.counter += 1
                self.spisochek.append(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
                break

    def Total(self):
        self.counter = 0
        self.spisochek = []
        print(self.transactions)
        #[[['192.168.1.68', '2', '2']], [['192.168.1.68', '32', 0], ['192.168.1.68', '43', 0]], [['192.168.1.68', '32', '4']], []]
        if self.block1 == 0:
            self.block1 = 1
            self.block = 0
            op = open('levinfo.txt', 'r').readlines()
            for i in range(len(op)):
                if i != len(op) - 1:
                    op[i] = op[i][:len(op[i]) - 1:]
            current = op[self.level].split(' ')
            for n in range(len(current)):
                if n == 0:
                    g = int(float(current[n]) * self.numofcurrentplayer)
                    no = int(float(current[n + 1]))
                    res = sorted(self.transactions[n], reverse=True, key=lambda x: x[2])
                    while g != 0 and len(res) != 0:
                        if no <= int(res[0][2]):
                            if g - int(res[0][1]) >= 0:
                                g -= int(res[0][1])
                                for i in range(len(self.users_cond)):
                                    if self.users_cond[i][1] == res[0][0]:
                                        self.users_cond[i][3] += int(res[0][1])
                                        print(self.users_cond[i])
                                        self.users_cond[i][5] -= int(res[0][1]) * int(res[0][2])
                                        break
                            else:
                                for i in range(len(self.users_cond)):
                                    if self.users_cond[i][1] == res[0][0]:
                                        self.users_cond[i][3] += g
                                        self.users_cond[i][5] -= int(res[0][2]) * g
                                        break
                        res.remove(res[0])
                if n == 1:
                    res = self.transactions[n]
                    for p in res:
                        for i in range(len(self.users_cond)):
                            if str(self.users_cond[i][1]) == p[0]:
                                if int(p[1]) <= self.users_cond[i][4] - self.users_cond[i][2]:
                                    self.users_cond[i][5] -= int(p[1]) * 2000
                                    self.users_cond[i][3] -= int(p[1]) * 2
                                    self.users_cond[i][2] += int(p[1])
                                    break
                                else:
                                    self.users_cond[i][5] -= (self.users_cond[i][4] - self.users_cond[i][2]) * 2000
                                    self.users_cond[i][3] -= (self.users_cond[i][4] - self.users_cond[i][2]) * 2
                                    self.users_cond[i][2] += (self.users_cond[i][4] - self.users_cond[i][2])
                                    break
                if n == 2:
                    g = int(float(current[n]) * self.numofcurrentplayer)
                    no = int(float(current[n + 1]))
                    res = sorted(self.transactions[n], key=lambda x: x[2])
                    while g != 0 and len(res) > 0:
                        if int(res[0][2]) <= no:
                            if g - int(res[0][1]) >= 0:
                                g -= int(res[0][1])
                                for i in range(len(self.users_cond)):
                                    if self.users_cond[i][1] == res[0][0]:
                                        self.users_cond[i][2] -= int(res[0][1])
                                        self.users_cond[i][5] += int(res[0][1]) * int(res[0][2])
                                        break
                            else:
                                for i in range(len(self.users_cond)):
                                    if self.users_cond[i][1] == res[0][0]:
                                        self.users_cond[i][2] -= g
                                        self.users_cond[i][5] += int(res[0][2]) * g
                                        break
                        res.remove(res[0])
                        print(self.users_cond)
                if n == 3:
                    res = self.transactions[n]
                    for p in res:
                        for i in range(len(self.users_cond)):
                            if self.users_cond[i][1] == p[0]:
                                self.users_cond[i][5] -= int(p[1]) * 5000
                                self.build.append([p[0], int(p[1]), 4])
                                break
            self.day += 1
            self.transactions = [[], [], [], []]
            print(self.users_cond)


app = Flask(__name__)
config = configparser.ConfigParser()
config.read("cfg.ini")
serv_adress = config['Pepega']['serv_adress']
gam = Gam()

@app.route('/end', methods=['POST', 'GET'])
def end():
    global gam
    n = gam.info()
    del gam
    gam = Gam()
    return render_template('success.html') + render_template('info1.html', hurma=n)

@app.route('/Total', methods=['POST', 'GET'])
def kk():
    global gam
    gam.Total()
    return redirect('gogogo')

@app.route('/prom', methods=['POST', 'GET'])
def prom():
    global gam
    gam.checker()
    if gam.counter != gam.numofcurrentplayer:
        return render_template('success.html') + render_template('vdvd.html')
    else:

        return redirect('Total')

@app.route('/buyI', methods=['POST', 'GET'])
def buyI():
    global gam
    global popa
    if request.method == 'GET':
        popa = gam.first_motion()
        if gam.los == 1:
            return redirect(serv_adress + 'end')
        gm = [request.args.get('nm'), request.args.get('kg'), request.args.get('uf'), request.args.get('pr'), request.args.get('ko'), request.args.get('kk')]
        print(gm)
        return render_template('success.html') + render_template('info.html', hurma=gam.info(), information=popa[0],bankwrot=popa[1])
    else:
        g = request.form['nm']
        m = request.form['kg']
        if '' not in [g, m]:
            gam.collect_usage(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), g,m, 0)

        g = request.form['uf']
        m = 0
        if '' not in [g, m]:
            gam.collect_usage(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), g,m, 1)

        g = request.form['pr']
        m = request.form['ko']
        if '' not in [g, m]:
            gam.collect_usage(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), g,m, 2)

        g = request.form['kk']
        m = 0
        if '' not in [g, m]:
            gam.collect_usage(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), g, m, 3)

        gam.counter = 0
        gam.spisochek = []
        return redirect('prom')



@app.route('/gogogo')
def start():
    global gam
    gam.checker()
    if gam.counter != gam.numofcurrentplayer:
        print(gam.counter)
        print(gam.spisochek)
        return render_template('success.html') + render_template('vdvd.html')
    else:
        return redirect('buyI')



@app.route('/success', methods=['POST', 'GET'])
def pageofmembers():
    global gam
    k = ''
    for i in gam.users_cond:
        k += i[0] + '; '
    if request.method == 'GET':
        gam.end = request.args.get('nm')
        return render_template('success.html') + k + render_template('gogogo.html')
    elif request.method == 'POST':
        gam.end = request.form['nm']
        return redirect('gogogo')

@app.route('/', methods=['POST', 'GET'])
def login():
    global gam
    if request.method == 'POST':
        g = request.form['nm']
        gam.users_cond.append([str(g), request.environ.get('HTTP_X_REAL_IP', request.remote_addr), 2, 4, 2, 10000])
        gam.numofcurrentplayer += 1
        return redirect('success')
    else:
        user = request.args.get('nm')
        return render_template('hello')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)