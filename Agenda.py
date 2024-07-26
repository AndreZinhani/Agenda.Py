#Classes e Objetos: Crie classes para representar os compromissos e a agenda.

class Compromisso:
    def __init__(self, titulo, data, hora, descricao):
        self.titulo = titulo
        self.data = data
        self.hora = hora
        self.descricao = descricao

class Agenda:
    def __init__(self):
        self.compromissos = []

    def adicionar_compromisso(self, compromisso):
        self.compromissos.append(compromisso)

    def remover_compromisso(self, titulo):
        self.compromissos = [c for c in self.compromissos if c.titulo != titulo]

    def listar_compromissos(self):
        return self.compromissos
#SQLite para armazenar os compromissos de forma persistente

import sqlite3

class BancoDeDados:
    def __init__(self, nome_banco):
        self.conn = sqlite3.connect(nome_banco)
        self.criar_tabela()

    def criar_tabela(self):
        query = '''
        CREATE TABLE IF NOT EXISTS compromissos (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            descricao TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def adicionar_compromisso(self, compromisso):
        query = 'INSERT INTO compromissos (titulo, data, hora, descricao) VALUES (?, ?, ?, ?)'
        self.conn.execute(query, (compromisso.titulo, compromisso.data, compromisso.hora, compromisso.descricao))
        self.conn.commit()

    def remover_compromisso(self, titulo):
        query = 'DELETE FROM compromissos WHERE titulo = ?'
        self.conn.execute(query, (titulo,))
        self.conn.commit()

    def listar_compromissos(self):
        cursor = self.conn.execute('SELECT titulo, data, hora, descricao FROM compromissos')
        return cursor.fetchall()

#Tkinter para criar a interface do usuário

import tkinter as tk
from tkinter import messagebox

class AplicativoAgenda:
    def __init__(self, root, bd):
        self.bd = bd
        self.root = root
        self.root.title('Agenda')

        self.titulo_label = tk.Label(root, text='Título:')
        self.titulo_label.grid(row=0, column=0)
        self.titulo_entry = tk.Entry(root)
        self.titulo_entry.grid(row=0, column=1)

        self.data_label = tk.Label(root, text='Data:')
        self.data_label.grid(row=1, column=0)
        self.data_entry = tk.Entry(root)
        self.data_entry.grid(row=1, column=1)

        self.hora_label = tk.Label(root, text='Hora:')
        self.hora_label.grid(row=2, column=0)
        self.hora_entry = tk.Entry(root)
        self.hora_entry.grid(row=2, column=1)

        self.descricao_label = tk.Label(root, text='Descrição:')
        self.descricao_label.grid(row=3, column=0)
        self.descricao_entry = tk.Entry(root)
        self.descricao_entry.grid(row=3, column=1)

        self.adicionar_btn = tk.Button(root, text='Adicionar', command=self.adicionar_compromisso)
        self.adicionar_btn.grid(row=4, column=0)

        self.listar_btn = tk.Button(root, text='Listar', command=self.listar_compromissos)
        self.listar_btn.grid(row=4, column=1)

    def adicionar_compromisso(self):
        titulo = self.titulo_entry.get()
        data = self.data_entry.get()
        hora = self.hora_entry.get()
        descricao = self.descricao_entry.get()

        compromisso = Compromisso(titulo, data, hora, descricao)
        self.bd.adicionar_compromisso(compromisso)
        messagebox.showinfo('Sucesso', 'Compromisso adicionado com sucesso!')

    def listar_compromissos(self):
        compromissos = self.bd.listar_compromissos()
        listar_janela = tk.Toplevel(self.root)
        listar_janela.title('Lista de Compromissos')

        for i, compromisso in enumerate(compromissos):
            tk.Label(listar_janela, text=f'Título: {compromisso[0]}').grid(row=i, column=0)
            tk.Label(listar_janela, text=f'Data: {compromisso[1]}').grid(row=i, column=1)
            tk.Label(listar_janela, text=f'Hora: {compromisso[2]}').grid(row=i, column=2)
            tk.Label(listar_janela, text=f'Descrição: {compromisso[3]}').grid(row=i, column=3)

if __name__ == '__main__':
    root = tk.Tk()
    bd = BancoDeDados('agenda.db')
    app = AplicativoAgenda(root, bd)
    root.mainloop()