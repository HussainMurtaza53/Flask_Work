from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

with open('config.json', 'r') as c:
    params = json.load(c)['Parameters']

Local_Server = True

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['User'],
    MAIL_PASSWORD = params['Password']
)

mail = Mail(app)

if (Local_Server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["Local_Uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["Prod_Uri"]
db = SQLAlchemy(app)

class Contacts(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    People= db.Column(db.Integer, nullable=False)
    Date = db.Column(db.DateTime(20), nullable=False)
    Msg = db.Column(db.String(120), nullable=False)

    def __init__(self, Name, People, Date, Msg):
        self.Name = Name
        self.People = People
        self.Date = Date
        self.Msg = Msg

@app.route('/', methods = ['GET', 'POST'])
def home():
    if (request.method == 'POST'):
        name = request.form.get('Name')
        people = request.form.get('People')
        date = request.form.get('date')
        message = request.form.get('Message')
        entry = Contacts(Name=name, People=people, Date=date, Msg=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('Message from' + ' ' + name + ' ' + 'for reserving table',
                          sender = name,
                          recipients = [params['User']],
                          body = 'People :' + ' ' + people + '\n' +
                                 'Date :' + ' ' + date + '\n' +
                                 'Message :' + ' ' + message
                          )
    return render_template('index.html', params = params)

if __name__ == '__main__':
    app.run(debug = True)
