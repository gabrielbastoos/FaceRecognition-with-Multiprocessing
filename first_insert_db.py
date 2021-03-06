from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setupbd import Base, All_people, Pessoa, Usuario

engine = create_engine("mysql+mysqldb://root:password@localhost/so2018")
#engine = create_engine('mysql+mysqldb://so2018:bastoseleleo123@so2018.mysql.pythonanywhere-services.com/so2018$default')


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Truncando tabelas p/ sobrescrever dados
session.execute('''SET FOREIGN_KEY_CHECKS = 0''')
session.execute('''TRUNCATE TABLE all_people''')
session.execute('''TRUNCATE TABLE usuario''')
session.execute('''TRUNCATE TABLE pessoa''')
session.execute('''SET FOREIGN_KEY_CHECKS = 1''')
session.commit()
session.close()
 

#Inserindo os dados

admin = Usuario(name="admin",password="password")
session.add(admin)
session.commit()


aluno1 = All_people(name="Zé das Couves",dre="12345678")
session.add(aluno1)
session.commit()

gabriel = All_people(name="Gabriel Bastos",dre="115036300")
session.add(gabriel)
session.commit()

leleo = All_people(name="Leonardo Feliciano",dre="115034308")
session.add(leleo)
session.commit()

rodrigo = All_people(name="Rodrigo Couto",dre="000000000")
session.add(rodrigo)
session.commit()

fabiana = All_people(name="Fabiana Ferreira",dre="115037241")
session.add(fabiana)
session.commit()


pessoa = session.query(All_people).all()

for pessoas in pessoa:

	testeTabela = Pessoa(nome=pessoas.name, dre = pessoas.dre, data="01/01/2001", hora_chegada="08:00:10", hora_saida="18:00:10")
	session.add(testeTabela)
	session.commit()

print ("Banco de dados completo")
