from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setupbd import Base, All_people, Pessoa, Usuario

#engine = create_engine("mysql+mysqldb://root:password@localhost/app_proximo")
engine = create_engine('mysql+mysqldb://so2018:bastoseleleo123@so2018.mysql.pythonanywhere-services.com/so2018$default')


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


aluno1 = All_people(nome="Zé das Couves",dre="12345678")
session.add(aluno1)
session.commit()


testeTabela = Pessoa(nome="Zé das Couves", dre = aluno1.dre, hora_chegada="08:00:10", hora_saida="18:00:10")
session.add(testeTabela)
session.commit()

print ("Banco de dados completo")
