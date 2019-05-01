from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as c:
    params = json.load(c)["Parameters"]

Local_Server = True

app = Flask(__name__)

if (Local_Server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["Local_Uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["Prod_Uri"]

db = SQLAlchemy(app)


class Contacts(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(50), unique=True, nullable=False)
    Msg = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.DateTime(40), nullable=True)

    def __init__(self, Name, Email, Msg, Date):
        self.Name = Name
        self.Email = Email
        self.Msg = Msg
        self.Date = Date

@app.route('/', methods = ['GET', 'POST'])
def home():
    if (request.method == 'POST'):
        Name = request.form.get('Name')
        Email = request.form.get('Email')
        Message = request.form.get('Message')
        entry = Contacts(Name=Name, Email=Email, Msg=Message, Date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('index.html', params = params)

if __name__ == '__main__':
    app.run(debug=True)