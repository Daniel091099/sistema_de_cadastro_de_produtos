import tkinter as tk
from tkinter import ttk
import crud as crud
import psycopg2

class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()  
        #componentes
        self.lbcodigo=tk.Label(win, text='código do Produto:')
        self.lblnome=tk.Label(win, text='nome do Produto')
        self.lblpreco=tk.Label(win, text='preco')
        self.lbltotal=tk.Label(win, text='total')
        
        self.txtcodigo=tk.Entry(bd=3)
        self.txtnome=tk.Entry()
        self.txtpreco=tk.Entry()
        self.btnCadastrar=tk.Button(win, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnAtualizar=tk.Button(win, text='Atualizar', command=self.fAtualizarProduto)
        self.btnExcluir=tk.Button(win, text='Excluir', command=self.fExcluirProduto)
        self.btnLimpar=tk.Button(win, text='Limpar', command=self.fLimparTela)
        #----- Componente TreeView --------------------------------------------
        self.dadosColunas = ("código", "nome", "preco", "total")
                
        self.treeProdutos = ttk.Treeview(win, 
                                       columns=self.dadosColunas,
                                       selectmode='browse')
        
        self.verscrlbar = ttk.Scrollbar(win,
                                        orient="vertical",
                                        command=self.treeProdutos.yview)        
        self.verscrlbar.pack(side='right', fill='x')
                                
        self.treeProdutos.configure(yscrollcommand=self.verscrlbar.set)
        
        self.treeProdutos.heading("código", text="código")
        self.treeProdutos.heading("nome", text="nome")
        self.treeProdutos.heading("preco", text="preco")
        self.treeProdutos.heading("total", text="total")

        self.treeProdutos.column("código",minwidth=0,width=100)
        self.treeProdutos.column("nome",minwidth=0,width=100)
        self.treeProdutos.column("preco",minwidth=0,width=100)
        self.treeProdutos.column("total", minwidth=0, width=100)

        self.treeProdutos.pack(padx=10, pady=10)
        
        self.treeProdutos.bind("<<TreeviewSelect>>", 
                               self.apresentarRegistrosSelecionados)                  
        #---------------------------------------------------------------------        
        #posicionamento dos componentes na janela
        #---------------------------------------------------------------------                
        self.lbcodigo.place(x=100, y=50)
        self.txtcodigo.place(x=250, y=50)
        
        self.lblnome.place(x=100, y=100)
        self.txtnome.place(x=250, y=100)
        
        self.lblpreco.place(x=100, y=150)
        self.txtpreco.place(x=250, y=150)
               
        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)
                   
        self.treeProdutos.place(x=100, y=300)
        self.verscrlbar.place(x=685, y=300, height=225)
        self.carregarDadosIniciais()
#-----------------------------------------------------------------------------
    def apresentarRegistrosSelecionados(self, event):  
        self.fLimparTela()  
        for selection in self.treeProdutos.selection():  
            item = self.treeProdutos.item(selection)  
            codigo,nome,preco = item["values"][0:3]
            self.txtcodigo.insert(0, codigo)
            self.txtnome.insert(0, nome)
            self.txtpreco.insert(0, preco)
#-----------------------------------------------------------------------------
    def carregarDadosIniciais(self):
        try:
          self.id = 0
          self.iid = 0          
          registros=self.objBD.selecionarDados()
          print("************ dados dsponíveis no BD ***********")        
          for item in registros:
              codigo=item[0]
              nome=item[1]
              preco=item[2]
              total=item[3]
              print("Código = ", codigo)
              print("Nome = ", nome)
              print("Preco  = ", preco)
              print("total  = ", total, "\n")
                        
              self.treeProdutos.insert('', 'end',
                                   iid=self.iid,                                   
                                   values=(codigo,
                                           nome,
                                           preco,
                                           total))
              self.iid = self.iid + 1
              self.id = self.id + 1
          print('Dados da Base')        
        except:
          print('Ainda não existem dados para carregar')            
#-----------------------------------------------------------------------------
#LerDados da Tela
#-----------------------------------------------------------------------------           
    def fLerCampos(self):
        try:
          print("************ dados dsponíveis ***********") 
          codigo = int(self.txtcodigo.get())
          print('codigo', codigo)
          nome=self.txtnome.get()
          print('nome', nome)
          preco=float(self.txtpreco.get())
          print('preco', preco)

          print('Leitura dos Dados com Sucesso!')        
        except:
          print('Não foi possível ler os dados.')
        return codigo, nome, preco
#-----------------------------------------------------------------------------
#Cadastrar Produto
#-----------------------------------------------------------------------------           
    def fCadastrarProduto(self):
        try:
          print("************ dados dsponíveis ***********") 
          codigo, nome, preco= self.fLerCampos()                    
          self.objBD.inserirDados(codigo, nome, preco)
          self.treeProdutos.insert('', 'end',
                                iid=self.iid,                                   
                                values=(codigo,
                                        nome,
                                        preco))
          self.iid = self.iid + 1
          self.id = self.id + 1
          self.fLimparTela()
          self.treeProdutos.delete(*self.treeProdutos.get_children())
          self.carregarDadosIniciais()
          print('Produto Cadastrado com Sucesso!')        
        except:
          print('Não foi possível fazer o cadastro.')
#-----------------------------------------------------------------------------
#Atualizar Produto
#-----------------------------------------------------------------------------           
    def fAtualizarProduto(self):
        try:
          print("************ dados dsponíveis ***********")        
          codigo, nome, preco= self.fLerCampos()
          self.objBD.atualizarDados(codigo, nome, preco)          
          #recarregar dados na tela
          self.treeProdutos.delete(*self.treeProdutos.get_children()) 
          self.carregarDadosIniciais()
          self.fLimparTela()
          print('Produto Atualizado com Sucesso!')        
        except:
          print('Não foi possível fazer a atualização.')
#-----------------------------------------------------------------------------
#Excluir Produto
#-----------------------------------------------------------------------------                  
    def fExcluirProduto(self):
        try:
          print("************ dados dsponíveis ***********")        
          codigo, nome, preco= self.fLerCampos()
          self.objBD.excluirDados(codigo)          
          #recarregar dados na tela
          self.treeProdutos.delete(*self.treeProdutos.get_children()) 
          self.carregarDadosIniciais()
          self.fLimparTela()
          print('Produto Excluído com Sucesso!')        
        except:
          print('Não foi possível fazer a exclusão do produto.')
#-----------------------------------------------------------------------------
#Limpar Tela
#-----------------------------------------------------------------------------                 
    def fLimparTela(self):
        try:
          print("************ dados dsponíveis ***********")        
          self.txtcodigo.delete(0, tk.END)
          self.txtnome.delete(0, tk.END)
          self.txtpreco.delete(0, tk.END)
          print('Campos Limpos!')        
        except:
          print('Não foi possível limpar os campos.')
#-----------------------------------------------------------------------------
#Programa Principal
#-----------------------------------------------------------------------------          
conn = psycopg2.connect(database="postgres",user="postgres",password="Daniel0910",port="5432")
print("Conexão com o Banco de Dados aberta com sucesso!")


comando = conn.cursor()
comando.execute("""Create table if not exists estoque
                (codigo int primary key not null,
                nome text not null,
                preco char(20),
                total char(5));
                """)

conn.commit()
print("Tabela criada com sucesso no BD!!")
conn.close()

janela=tk.Tk()
principal=PrincipalBD(janela)
janela.title('Tabela de preços de produtos')
janela.geometry("720x600+10+10")
janela.mainloop()
#-----------------------------------------------------------------------------




