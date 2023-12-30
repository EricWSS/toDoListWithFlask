from db.helper_controller import *

class UserToDoList:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.task = None
            
    def createUserTable(self): #ok
        '''Cria uma tabela com TODOS os usuários da minha TO-DO 
        LIST com chave estrangeira no user e na senha.'''
        conn = DBHelper()
        sql = f"""CREATE TABLE IF NOT EXISTS users_todolist (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                username VARCHAR(30) NOT NULL UNIQUE, 
                password VARCHAR(30) NOT NULL
            );"""

        try:
            conn.execute(sql)
            print(f"Table created for user {self.username}")
        except mysql.connector.Error as err:
            print(f"Error creating table for user {self.username}: {err}")

    def insertUser(self):
        conn = DBHelper()
        sql = f"""INSERT INTO users_todolist (
            username, password
            ) VALUES (
                '{self.username}',
                '{self.password}'
                );"""
        try:
            conn.execute(sql)
            print(f"User {self.username} inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting user {self.username}: {err}")

    def userExists(self):
        '''Verifica se um usuário já existe na tabela.'''
        conn = DBHelper()
        try:
            sql = f"SELECT * FROM users_todolist WHERE username = '{self.username}';"
            user = conn.execute(sql)

            # Se a consulta for bem-sucedida e retornar algum resultado, o usuário existe
            return bool(user)

        except mysql.connector.Error as err:
            # Se ocorrer um erro (por exemplo, tabela não encontrada), assume-se que o usuário não existe
            print(f"Erro MySQL: {err}")
            return False

    ###################################################################################
    def createToDoListTable(self):
        '''Cria uma tabela para TODOS os usuários com suas 
        respectivas tarefas por chave estrangeira.'''
        conn = DBHelper()
        create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS tasks_todolist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task VARCHAR(200) NOT NULL, 
                status_feito CHAR NOT NULL,
                id_user INT,
                FOREIGN KEY (id_user) REFERENCES users_todolist(id)
            );
        """
        conn.execute(create_table_sql)


    ####################################### LEMBRAR DE PESQUISAR COMO FAZER O "query parameterization" ou "bind parameter" 
        
    def insertTask(self, task):#ok
        '''Insere uma nova tarefa na tabela.'''
        self.task = task
        conn = DBHelper()
        if self.username:
            sql = f"""INSERT INTO tasks_todolist (
                task, 
                status_feito, 
                id_user
                ) VALUES (
                    '{self.task}', 
                    0, 
                    (SELECT id FROM users_todolist WHERE username = '{self.username}' LIMIT 1));"""
            conn.execute(sql)
        else: 
            print("Erro: Nome de usuário não encontrado.")

    def deleteTask(self, task_id):# OK =>>>> Minha task no frontend precisa de um chekbox e um button para deletar.
        '''Deleta uma tarefa da tabela.'''
        conn = DBHelper()
        sql = f"DELETE FROM tasks_todolist WHERE id = {task_id};"
        conn.execute(sql)
    
    def showTasks(self): 
        '''Mostra todas as tarefas de um usuário.'''
        conn = DBHelper()
        try:
            # Utilizamos um JOIN para relacionar as tabelas e filtramos pelo username
            sql = f"""
                SELECT tasks.*
                FROM tasks_todolist tasks
                JOIN users_todolist users ON tasks.id_user = users.id
                WHERE users.username = '{self.username}';
            """
            tasks = conn.execute(sql)
            return tasks

        except mysql.connector.Error as err:
            # Lidar com erros, como a tabela ainda não existir
            print(f"Erro MySQL: {err}")
            return []


