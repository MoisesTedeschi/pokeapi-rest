from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField
from wtforms.validators import DataRequired, Email

csrf = CSRFProtect()

class PokeForms(FlaskForm):
    email_principal = StringField('email_principal', 
                                    validators=[DataRequired('Por favor, insira um endereço de email válido.'),
                                    Email("Por favor, insira um endereço de email válido.")])

    email_2 = StringField('email_2')
    email_3 = StringField('email_3')

    tipo_pokemon = StringField('tipo_pokemon', validators=[DataRequired('Por favor, insira o tipo do Pokémon!')])
