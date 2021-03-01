import os, random, requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from models.forms import PokeForms, csrf


mail = Mail()
app = Flask(__name__)

base_url = "https://pokeapi.co/api/v2"
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf.init_app(app)


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")

'''
Aqui estão as informações de 5 pokémons aleatórios do tipo **inserir tipo aqui** 
que podem ser interessantes para você capturar durante a sua jornada.

**Inserir foto do pokémon aqui**
(front_default)

Nome do Pokémon: **inserir nome aqui**
(name)

Peso: **inserir peso aqui**
(weight)

Altura: **inserir altura aqui**
(height)

Experiência base: **inserir experiência base aqui**
(base_experience)
'''

@app.route("/poke_dados", methods=["GET", "POST"])
def poke_dados():

    poke_form = PokeForms(request.form)

    if request.method == "POST" and poke_form.validate_on_submit():

        email_principal = request.form["email_principal"]

        email_2 = request.form["email_2"]
        email_3 = request.form["email_3"]

        tipo_pokemon = request.form["tipo_pokemon"]

        print(f'Email informado: {email_principal}')
        print(f'Tipo de Pokémon informado: {tipo_pokemon}')

        req = requests.get(f'{base_url}/type/{tipo_pokemon}')
        
        for n in range(5):
            pokemon = random.choice(req.json()["pokemon"])
            url_pokemon = requests.get(pokemon["pokemon"]["url"])

            print(f'Nome do Pokémon: {pokemon["pokemon"]["name"]}')
            
            print(f'Foto do Pokémon: {url_pokemon.json()["sprites"]["front_default"]}')

            print(f'Peso: {url_pokemon.json()["weight"]}')
            print(f'Altura: {url_pokemon.json()["height"]}')

            print(f'Experiência base: {url_pokemon.json()["base_experience"]}\n')

        return redirect(url_for("index"))

    return render_template("index.html", poke_form=poke_form)


#Configurações para envio de email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'moisestedeschi@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

@app.route('/email', methods=['GET', 'POST'])
def email():
    poke_form = PokeForms()
    
    if poke_form.validate_on_submit():        
        print('-------------------------')
        print(request.form['email_principal'])
        print(request.form['email_2'])
        print(request.form['email_3'])
        print(request.form['tipo_pokemon'])       
        print('-------------------------')
        
        send_message(request.form)
        return redirect('/success') 

    return render_template('index.html', poke_form=poke_form)


@app.route('/success')
def success():
    return render_template('index.html')


def send_message(tipo_pokemon):

    print(tipo_pokemon.get('tipo_pokemon'))

    email_principal = request.form['email_principal']

    msg = Message('Pokémon API - Teste de Envio de Email.', recipients=[email_principal])

    msg.body = tipo_pokemon.get('tipo_pokemon')

    msg.html = ('<h1>Pokémon API</h1>'
                '<p>2021 - Parabéns! Seu email está funcionando!</p>')

    flash(f'Um e-mail foi enviado com sucesso para: {email_principal}.')

    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)