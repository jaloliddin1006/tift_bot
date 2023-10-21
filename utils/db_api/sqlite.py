import sqlite3


class Database:
    def __init__(self, path_to_db="bot_db.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE BotUsers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id integer NOT NULL,
            name varchar(255) NOT NULL,
            user_name varchar(255),
            language varchar(15),
            join_date varchar(60),
            UNIQUE(telegram_id)
            );
"""
        self.execute(sql, commit=True)

    def create_table_tiftusers(self):
            sql = """              
            CREATE TABLE TiftUsers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lms_id INTEGER NOT NULL,
                user_id INTEGER NOT  NULL ,
                username varchar(50)  NOT NULL ,
                full_name varchar(100) NOT NULL ,
                role varchar(25) NOT NULL,
                join_date DATE,
                update_date DATE,
                token varchar(255) ,
                FOREIGN KEY(user_id) REFERENCES BotUsers(telegram_id),
                UNIQUE (user_id, username, token)
                );
    """
            self.execute(sql, commit=True)
    def create_table_messages(self):
        sql = """
        CREATE TABLE Messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id integer NOT NULL,
            name varchar(255) NOT NULL,
            msg_id varchar(25),
            create_date varchar(60)
            );
"""
        self.execute(sql, commit=True)
        
    def create_table_new_messages(self):
        sql = """
        CREATE TABLE NewMessages(
            telegram_id integer NOT NULL,
            full_name varchar(255) NOT NULL,
            nick_name varchar(225),
            phone varchar(25)
            );
"""
        self.execute(sql, commit=True)
    def create_table_channels(self):
        sql = """
        CREATE TABLE Channels (
        channel_id INTEGER PRIMARY KEY,
        channel_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) ,
        channel_link VARCHAR(255) NOT NULL,
        adding_member integer
       
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_bot_user(self, telegram_id: int, name: str, user_name: str = None, language: str = 'uz'):
        sql = """
        INSERT INTO BotUsers(telegram_id, name, user_name, language, join_date) VALUES(?, ?, ?, ?, datetime('now'))
        """
        self.execute(sql, parameters=(telegram_id, name, user_name, language), commit=True)

    def add_message(self, telegram_id: int, name: str, msg_id: str):
        sql = """
        INSERT INTO Messages(telegram_id, name, msg_id, create_date) VALUES(?, ?, ?, datetime('now'))
        """
        self.execute(sql, parameters=(telegram_id, name, msg_id), commit=True)

    def add_new_message(self, telegram_id: int, full_name: str, nick_name: str, phone: str):
        sql = """
        INSERT INTO NewMessages(telegram_id, full_name, nick_name, phone) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(telegram_id, full_name, nick_name, phone), commit=True)

    def add_tift_user(self, lms_id, user_id, username, full_name, role, token):
        sql = " INSERT INTO  TiftUsers(lms_id, user_id, username, full_name, role, token, join_date) VALUES(?, ?, ?, ?, ?, ?, datetime('now'))"
        self.execute(sql, parameters=(lms_id, user_id, username, full_name, role, token), commit=True)

    def select_bot_user(self, **kwargs):
        sql = "SELECT * FROM BotUsers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def select_tift_user(self, **kwargs):
        sql = f"SELECT * FROM TiftUsers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def select_message(self, **kwargs):
        sql = f"SELECT * FROM Messages WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def select_new_message(self, **kwargs):
        sql = f"SELECT * FROM NewMessages WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def update_tift_user(self, lms_id, user_id, username, full_name, role, token):
        sql = f"""
        UPDATE TiftUsers SET lms_id=?, username=?, full_name=?, role=?, token=?  WHERE user_id=?
        """
        return self.execute(sql, parameters=(lms_id, username, full_name, role, token, user_id), commit=True)
    
    def logout_token(self, user_id, token):
        sql = f"""
        UPDATE TiftUsers SET token=?  WHERE user_id=?
        """
        return self.execute(sql, parameters=(token, user_id), commit=True)
    
    def select_all_users(self, table):
        sql = f"""
        SELECT * FROM {table}
        """
        return self.execute(sql, fetchall=True)
    
    
    def update_lang(self, lang, user_id):
        sql = f"""
        UPDATE BotUsers SET language=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(lang, user_id), commit=True)

    def update_new_message(self, nick_name, user_id):
        sql = f"""
        UPDATE NewMessages SET nick_name=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(nick_name, user_id), commit=True)

    def select_user_all_data(self, **kwargs):
        sql = f"SELECT * FROM BotUsers INNER JOIN TiftUsers ON BotUsers.telegram_id = TiftUsers.user_id WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    # def select_user(self, **kwargs):
    #     # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
    #     sql = "SELECT * FROM Users WHERE "
    #     sql, parameters = self.format_args(sql, kwargs)
    #
    #     return self.execute(sql, parameters=parameters, fetchone=True)
    #
    # def count_users(self):
    #     return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)
    #
    # def update_user_email(self, email, id):
    #     # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"
    #
    #     sql = f"""
    #     UPDATE Users SET email=? WHERE id=?
    #     """
    #     return self.execute(sql, parameters=(email, id), commit=True)
    #
    def drop_message(self):
        self.execute("DROP TABLE Messages", commit=True)


    def add_channel(self, channel_id, username, channel_name, channel_link):
        sql = " INSERT INTO  Channels(channel_id, username, channel_name, channel_link, adding_member) VALUES(?, ?, ?, ?, 0)"
        self.execute(sql, parameters=( channel_id, username, channel_name, channel_link), commit=True)
    
    def select_all_channels(self):
        sql = f"""
        SELECT * FROM Channels
        """
        return self.execute(sql, fetchall=True)
    
        
    def select_channel(self, **kwargs):
        sql = f"SELECT * FROM Channels WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def update_member_count(self, adding_member, channel_id):
        sql = f"""
        UPDATE Channels SET adding_member=? WHERE channel_id=?
        """
        return self.execute(sql, parameters=(adding_member, channel_id), commit=True)

    def delete_channel(self,  channel_id):
        sql = f"""
        DELETE FROM Channels where channel_id=?
        """
        
        return self.execute(sql, parameters=(channel_id,), commit=True)
    
    def drop_channels(self):
        self.execute("DROP TABLE Channels", commit=True)


    
    # CREATE TABLE Channels (
    #     channel_id INTEGER PRIMARY KEY,
    #     channel_name VARCHAR(255) NOT NULL,
    #     channel_link VARCHAR(255) NOT NULL,
    #     adding_member integer
       
# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)


#
# SELECT *
# FROM table1 INNER JOIN table2
# ON table1.column_name = table2.column_name;


# db = Database()
# user = db.select_all_bot_users()
# print(user)