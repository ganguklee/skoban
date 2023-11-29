from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guestname = db.Column(db.String, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    guestmessage = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/time_table/")
def time_table():
    return render_template("time_table.html")


@app.route("/member/")
def member():
    return render_template("member.html")

@app.route("/guestbook/")
def guestbook():
    card_list = Cards.query.order_by(desc(Cards.id)).all()
    return render_template("guestbook.html", data=card_list)

@app.route("/menu/")
def menu():
    return render_template("menu.html")

@app.route("/donation/")
def donation():
    return render_template("donation.html")

@app.route("/guestbook/create/")
def card_create():
    guestname_receive = request.args.get("guestname")
    password_receive = request.args.get("password")
    guestmessage_receive = request.args.get("guestmessage")

    card = Cards(guestname=guestname_receive,password=password_receive,guestmessage=guestmessage_receive)
    db.session.add(card)
    db.session.commit()
    return redirect(url_for('guestbook'))

@app.route("/guestbook/delete/<int:id>/", methods=['GET', 'POST'])
def card_delete(id):
    if request.method == 'POST':
        card_delete = Cards.query.filter_by(id=id).first()
        entered_password =  request.form['delete_password']
        if entered_password == str(card_delete.password) :
            db.session.delete(card_delete)
            db.session.commit()
            flash("방명록이 삭제되었습니다.")
            return redirect(url_for('guestbook'))
        else :
            flash("비밀번호가 일치하지 않습니다.")
            return redirect(url_for('guestbook'))

if __name__ == "__main__":
    app.run(debug=True, port=8080)

