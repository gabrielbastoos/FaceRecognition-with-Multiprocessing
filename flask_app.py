
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask import Flask, request, redirect, url_for, flash, render_template, jsonify

from setupbd import Base, All_people, Pessoa, Usuario

engine = create_engine("mysql+mysqldb://root:password@localhost/so2018")
#engine = create_engine('mysql+mysqldb://so2018:bastoseleleo123@so2018.mysql.pythonanywhere-services.com/so2018$default')
app = Flask(__name__)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

dataAtual = datetime.now().strftime('%d/%m/%Y')

@app.route("/")
def print_result():

	pessoas = session.query(Pessoa).filter_by(data=dataAtual).all()
	return render_template('acesso.html', pessoas=pessoas)

@app.route("/atualizado", methods=['POST'])
def print_resultado():

	pessoas = session.query(Pessoa).filter_by(data=dataAtual).all()
	return render_template('acessoAtualizado.html', pessoas=pessoas)



app.run(host="0.0.0.0", debug=True)

