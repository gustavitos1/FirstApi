from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, declarative_base
engine = create_engine('sqlite:///Biblioteca.db')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Livro(Base):
    __tablename__ = 'livros'
    id_livro = Column(Integer, primary_key=True)
    ISBN = Column(Integer, unique=True)
    Titulo = Column(String, nullable=False, index=True)
    Autor = Column(String, nullable=False, index=True)
    Resumo = Column(String, nullable=False, index=True)

    def __repr__(self):
        return f'<Livro: {self.Titulo}, ISBN: {self.ISBN}, Autor: {self.Autor}, Resumo: {self.Resumo}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_Livro = {
            "id_cliente": self.id_livro,
            "Titulo": self.Titulo,
            "ISBN": self.ISBN,
            "Autor": self.Autor,
            "Resumo": self.Resumo
        }
        return dados_Livro

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    Nome = Column(String, nullable=False, index=True)
    cpf = Column(String, unique=True)
    Endereco = Column(String, nullable=False, index=True)

    def __repr__(self):
        return f'<Usuario: {self.Nome}, CPF: {self.cpf}, Endereço: {self.Endereco}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_Usuario = {
            "id_usuario": self.id_usuario,
            "Nome": self.Nome,
            "CPF": self.cpf,
            "Endereco": self.Endereco,
        }
        return dados_Usuario

class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    id_emprestimo = Column(Integer, primary_key=True)
    Data_Emprestimo = Column(String, nullable=True)
    Data_Devolucao = Column(String, nullable=True)
    id_livro = Column(Integer, ForeignKey('livros.id_livro'))
    livro = relationship("Livro")
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    usuario = relationship("Usuario")

    def __repr__(self):
        return f'<Emprestimo: {self.Data_Emprestimo}, Data_Devolução: {self.Data_Devolucao}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados = {
            "id_empréstimo": self.id_emprestimo,
            "Data_Empréstimo": self.Data_Emprestimo,
            "Data_Devolução": self.Data_Devolucao,
            "id_livro": self.id_livro,
            "id_usuario": self.id_usuario
        }
        return dados

def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)