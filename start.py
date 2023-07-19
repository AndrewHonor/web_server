from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:postgres@localhost/py_sweater"
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Columm(db.Integer, primary_key=True)
    text = db.Colum(db.String(1024), nullable=False)

    def __int__(self, text, tags):
        self.text = text.strip()
        self.tags = [Tag(text=tag.strip()) for tag in tags.strip()]

class Tag(db.Model):
    id = db.Columm(db.Integer, primary_key=True)
    text = db.Colum(db.String(32), nullable=False)

    messsage_id = db.Column(db.Integer, db.ForeingKey('message_id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tag', lazy=True))

db.create_all()

@app.route("/", methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', message=Message.query.all())


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    db.session.add(Message(text, tag))
    db.session.commit()

    return redirect(url_for('main'))
