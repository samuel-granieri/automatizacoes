import sqlite3

def create_db():
    
    conn = sqlite3.connect("alert.db")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS tb_alerta (data TEXT)")
        
        
def insert_db(data):
    
    conn = sqlite3.connect("alert.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tb_alerta (data) VALUES (?)", (data,))
    conn.commit()
    
    
def select_db():
    
    conn = sqlite3.connect("alert.db")
    cursor = conn.cursor()
    
    data = cursor.execute("SELECT * FROM tb_alerta")
    
    list_bd = []
    
    for row in data:
        list_bd.append(row)
        
    return list_bd
    
     
    
    
    
    

        
        
        
	    
    
    
    