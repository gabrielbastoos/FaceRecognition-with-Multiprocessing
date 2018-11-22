
import sys
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuario(Base):
	__tablename__ = 'usuario'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	password = Column(String(250), nullable=False)

	@property
	def serialize(self):
		return {
		'id': self.id,
		'name': self.name,
		'password': self.password,
		}

class All_people(Base):
	__tablename__ = 'all_people'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	dre = Column(Integer, nullable=False)

	@property
	def serialize(self):
		return {
		'id': self.id,
		'nome': self.name,
		'dre': self.dre,
		}

class Pessoa(Base):
	__tablename__ = 'pessoa'

	id = Column(Integer, primary_key=True)
	nome = Column(String(250), nullable=False)
	dre = Column(Integer, ForeignKey('all_people.dre'))
	all_people = relationship('All_people')
	hora_chegada = Column(String(250), nullable=False)
	hora_saida = Column(String(250), nullable=False)

	@property
	def serialize(self):
		return {
		'id': self.id,
		'nome': self.nome,
		'dre': self.dre,
		'hora_chegada':self.hora_chegada,
		'hora_saida':self.hora_saida
		}


#engine = create_engine("mysql+mysqldb://root:password@localhost/app_proximo")
engine = create_engine('mysql+mysqldb://so2018:bastoseleleo123@so2018.mysql.pythonanywhere-services.com/so2018$default')

Base.metadata.create_all(engine)
