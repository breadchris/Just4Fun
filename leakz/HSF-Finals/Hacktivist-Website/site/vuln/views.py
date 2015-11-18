from flask import render_template, request, session, redirect
import hashlib, struct, os

from encrypt_utils import *
username = "sassycassi128"
password = "deadbeefcafebab3:loolmonyytcrackr:1234098710101100:asdfhjklqwertyui:sinoonymfortehwn"
dir = os.path.dirname(__file__)
storage_dir = os.path.join(dir, '../static/storage/')

def init_views(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/connect')
    def connect():
        return render_template('connect.html')

    @app.route('/conditionals')
    def conditionals():
        global password
        import random

        appa = [[ord(c) for c in x] for x in password.split(":")]

        operations = ["-", "+", "*", "^", "/", "%"]

        cond_stuff = "appa = [[ord(c) for c in x] for x in password.split(\":\")]\n"
        for s1, s2 in [(random.choice(range(0, len(appa))), random.choice(range(0, len(appa)))) for _ in range(0, 10)]:
            for t1, t2 in [(random.choice(range(0, len(appa[0]))), random.choice(range(0, len(appa[0])))) for _ in range(0, 10)]:
                op = random.choice(operations)
                thing = "int(appa[%d][%d] %s appa[%d][%d])" % (s1, t1, op, s2, t2)
                cond_stuff += "if " + thing + " != " + str(eval(thing)) + " :" + "\n"
                cond_stuff += "\texit(-1)\n"

        return cond_stuff

    @app.route('/conds')
    def conds():
        asdf = "asdf"
        return render_template("conds.html", conds=asdf)

    @app.route('/lol')
    def lol():
        return render_template('lol.html')

    @app.route('/learn')
    def learn():
        return render_template('learn.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    def make_tree(path):
        tree = []
        try: lst = os.listdir(path)
        except OSError:
            pass #ignore errors
        else:
            for name in lst:
                tree.append(name)
        return tree

    @app.route('/storage')
    def storage():
        global storage_dir
        if "username" in session.keys() and session["username"] == username:
            tree = make_tree(storage_dir)
            return render_template('storage.html', username=username, tree=tree)
        return redirect('/login')

    @app.route('/login', methods=["POST", "GET"])
    def login():
        global password, username
        if request.method == "POST":
            if "usrname" in request.form.keys() and "usrpass" in request.form.keys():
                un = request.form['usrname']
                pw = request.form['usrpass']
                if un == username and pw == password:
                    session["username"] = username
                    return redirect('/storage')
                else:
                    #return render_template('login.html')
                    return un + pw
            else:
                return render_template('login.html')
        else:
            return render_template('login.html')

    @app.route('/login-crypto')
    def login_crypto():
        sid = request.args.get('matrix-id')

        challenge = "the matrix is real guys|user=neo|password=neo_is_cool_yo|authlevel=5|challenge1"
        matrix_id = aes_encrypt(challenge, challenge1_key, codec='base64')

        if sid:
            try:
                ptext = aes_decrypt(sid, challenge1_key, codec='base64')
            except typeerror:
                error = "caught exception during aes decryption..."
                return render_template('challenge1.html', matrix_id=matrix_id, error=error)

            # this is where we introduce a cbc padding oracle vulnerability
            padding_length = struct.unpack("b", ptext[-1])[0]
            good = (ptext[-padding_length:] == struct.pack("b", padding_length) * padding_length)

            if good is false:
                error = "looks like you gave the wrong padding for your encrypted stuff"
                return render_template('challenge1.html', matrix_id=matrix_id, error=error)
            else:
                ptext = ptext[:-padding_length]
                print ptext

            try:
                role = ptext.split('|')[3][-1]
                print ptext.split('|')[3][-1]
            except indexerror:
                error = "was not able to compute your authlevel. please submit a valid matrix id."
                return render_template('challenge1.html', matrix_id=matrix_id, error=error)

            try:
                username, password = ptext.split('|')[1:3]
            except valueerror:
                error = "was not able to locate username and password in given matrix id."
                return render_template('challenge1.html', matrix_id=matrix_id, error=error)

            if role == '0':
                return render_template('challenge1.html', flag=challenge1_flag)
            else:
                error = "your authlevel is not 0. you will never be able to get access to the matrix, neo."
                return render_template('challenge1.html', matrix_id=matrix_id, error=error)

        else:
            return render_template('challenge1.html', matrix_id=matrix_id)

