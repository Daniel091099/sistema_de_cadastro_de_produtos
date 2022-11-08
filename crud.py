import psycopg2

class AppBD:
    def __init__(self):
        print('Método Construtor')
        
    def abrirConexao(self):
        try:
          self.connection = psycopg2.connect(user="postgres",
                                  password="Daniel0910",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")

        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)

#-----------------------------------------------------------------------------
#Selecionar todos os Produtos
#-----------------------------------------------------------------------------                 
    def selecionarDados(self):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
    
            print("Selecionando todos os produtos")
            sql_select_query = """select * from estoque """

            cursor.execute(sql_select_query)
            registros = cursor.fetchall()             
            print(registros)
                
    
        except (Exception, psycopg2.Error) as error:
            print("sem banco de dados!!!!!!!", error)
    
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
        return registros
#-----------------------------------------------------------------------------
#Inserir Produto
#-----------------------------------------------------------------------------                 
    def inserirDados(self, codigo, nome, preco):
        try:
          self.abrirConexao()
          cursor = self.connection.cursor()
          postgres_insert_query = """ INSERT INTO estoque 
          ("codigo", "nome", "preco", "total") VALUES (%s,%s,%s,%s)"""
          record_to_insert = (codigo, nome, preco, (preco * 1.1))
          cursor.execute(postgres_insert_query, record_to_insert)
          self.connection.commit()
          count = cursor.rowcount
          print (count, "Registro inserido com successo na tabela estoque")
        except (Exception, psycopg2.Error) as error :
          if(self.connection):
              print("Falha ao inserir registro na tabela estoque", error)
        finally:
            #closing database connection.
            if(self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
                
#-----------------------------------------------------------------------------
#Atualizar Produto
#-----------------------------------------------------------------------------                 
    def atualizarDados(self, codigo, nome, preco):
        print("Registro Antes da Atualização ")
        try:
            self.abrirConexao()    
            cursor = self.connection.cursor()

            print("Registro Antes da Atualização ")
            sql_select_query = """select * from estoque 
            where "codigo" = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)    
            # Atualizar registro
            sql_update_query = """Update estoque set "nome" = %s, 
            "preco" = %s, "total" = %s where "codigo" = %s"""
            cursor.execute(sql_update_query, (nome, preco, (preco * 1.1), codigo))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro atualizado com sucesso! ")    
            print("Registro Depois da Atualização ")
            sql_select_query = """select * from estoque 
            where "codigo" = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)    
        except (Exception, psycopg2.Error) as error:
            print("Erro na Atualização", error)    
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

#-----------------------------------------------------------------------------
#Excluir Produto
#-----------------------------------------------------------------------------                 
    def excluirDados(self, codigo):
        try:
            self.abrirConexao()    
            cursor = self.connection.cursor()    
            # Atualizar registro
            sql_delete_query = """Delete from estoque
            where "codigo" = %s"""
            cursor.execute(sql_delete_query, (codigo, ))

            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro excluído com sucesso! ")        
        except (Exception, psycopg2.Error) as error:
            print("Erro na Exclusão", error)    
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
                
#-----------------------------------------------------------------------------
