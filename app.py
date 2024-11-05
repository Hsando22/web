import cherrypy
import pyodbc
import json
import os
from datetime import datetime

class SpanishApp:
    def __init__(self):
        # Configuración de conexión a SQL Server
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost;'
                'DATABASE=aprender;'  # Asegúrate de que este sea el nombre correcto de tu base de datos
                'UID=sa;'
                'PWD=$54K38k5;'  # Cambia esto por la contraseña real del usuario sa
            )
            self.cursor = self.conn.cursor()
            self.create_tables()
        except pyodbc.InterfaceError as e:
            cherrypy.log("Error de conexión a la base de datos: " + str(e))
            raise cherrypy.HTTPError(500, "No se pudo conectar a la base de datos")

    def create_tables(self):
        # Crear las tablas necesarias si no existen
        self.cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
        CREATE TABLE Users (
            user_id INT PRIMARY KEY IDENTITY,
            username NVARCHAR(50) NOT NULL,
            password NVARCHAR(50) NOT NULL,
            level INT DEFAULT 1
        );
        
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Topics' AND xtype='U')
        CREATE TABLE Topics (
            topic_id INT PRIMARY KEY IDENTITY,
            name NVARCHAR(100) NOT NULL,
            description TEXT
        );
        
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Exercises' AND xtype='U')
        CREATE TABLE Exercises (
            exercise_id INT PRIMARY KEY IDENTITY,
            topic_id INT FOREIGN KEY REFERENCES Topics(topic_id),
            question TEXT NOT NULL,
            correct_answer NVARCHAR(100) NOT NULL,
            difficulty INT
        );
        
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Progress' AND xtype='U')
        CREATE TABLE Progress (
            progress_id INT PRIMARY KEY IDENTITY,
            user_id INT FOREIGN KEY REFERENCES Users(user_id),
            topic_id INT FOREIGN KEY REFERENCES Topics(topic_id),
            score FLOAT,
            last_accessed DATETIME DEFAULT GETDATE()
        );
        ''')
        self.conn.commit()

    @cherrypy.expose
    def index(self):
        return open('templates/index.html')

    @cherrypy.expose
    def test_connection(self):
        try:
            self.cursor.execute("SELECT 1")
            return "Conexión a la base de datos exitosa"
        except Exception as e:
            return f"Error de conexión: {e}"



    # 1. Registro de Usuario
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def register(self):
        data = cherrypy.request.json
        username = data.get("username")
        password = data.get("password")

        self.cursor.execute("INSERT INTO Users (username, password, level) VALUES (?, ?, ?)", 
                            (username, password, 1))
        self.conn.commit()
        return {"status": "success", "message": "Usuario registrado exitosamente"}

    # 2. Inicio de Sesión
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def login(self):
        data = cherrypy.request.json
        username = data.get("username")
        password = data.get("password")

        self.cursor.execute("SELECT user_id, level FROM Users WHERE username = ? AND password = ?", 
                            (username, password))
        user = self.cursor.fetchone()
        if user:
            # Almacenar el user_id en la sesión
            cherrypy.session['user_id'] = user[0]
            return {"status": "success", "user_id": user[0], "level": user[1]}
        else:
            return {"status": "error", "message": "Usuario o contraseña incorrectos"}








    # 3. Consultar Temas
    # 3. Consultar Temas
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def topics(self):
        user_id = cherrypy.session.get('user_id')
        if user_id is None:
            return {"status": "error", "message": "Usuario no autenticado"}
        
        # Llamar al procedimiento almacenado para actualizar el nivel
        self.cursor.execute("EXEC UpdateUserLevel @userId = ?", (user_id,))
        self.conn.commit()

        # Consultar los temas de acuerdo al nivel del usuario
        self.cursor.execute("""
            SELECT t.topic_id, t.name, t.description 
            FROM Topics t
            JOIN Users u ON u.level >= t.level_id  -- Selecciona temas hasta el nivel del usuario
            WHERE u.user_id = ?;  -- Cambia el ? por el user_id real
        """, (user_id,))
        
        topics = [{"topic_id": row[0], "name": row[1], "description": row[2]} for row in self.cursor.fetchall()]
        return {"status": "success", "topics": topics}


    # Consultar Progreso del Usuario
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_user_progress(self):
        user_id = cherrypy.session.get('user_id')
        if user_id is None:
            return {"status": "error", "message": "Usuario no autenticado"}
        
        self.cursor.execute("SELECT topic_id, exercise_id FROM Progress WHERE user_id = ?", (user_id,))
        progress = self.cursor.fetchone()
        
        if progress:
            return {
                "status": "success",
                "topic_id": progress[0],
                "exercise_id": progress[1]
            }
        else:
            return {"status": "info", "message": "No se encontró progreso para este usuario."}

        

    '''# 4. Consultar Ejercicios por Tema
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def exercises(self, topic_id):
        self.cursor.execute("SELECT exercise_id, question, correct_answer FROM Exercises WHERE topic_id = ?", 
                            (topic_id,))
        exercises = [{"exercise_id": row[0], "question": row[1], "correct_answer": row[2]} for row in self.cursor.fetchall()]
        return {"status": "success", "exercises": exercises}'''
    

    '''@cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def update_progress(self):
        # Obtener datos de la solicitud JSON
        input_data = cherrypy.request.json
        user_id = cherrypy.session.get('user_id')
        
        topic_id = input_data.get('topic_id')
        exercise_id = input_data.get('exercise_id')
        correct = input_data.get('correct')
        
        # Verificar que el usuario esté autenticado
        if user_id is None:
            return {"status": "error", "message": "Usuario no autenticado"}
        
        # Verificar que exercise_id no sea NULL
        if exercise_id is None:
            return {"status": "error", "message": "Exercise ID no puede ser NULL"}
        
        # Solo actualiza el progreso si la respuesta fue correcta
        if correct:
            try:
                # Llama al procedimiento almacenado para guardar o actualizar el progreso
                self.cursor.callproc('SaveUserProgress', [user_id, topic_id, exercise_id])
                
                # Confirma los cambios en la base de datos
                self.connection.commit()
                print("Progreso actualizado con el procedimiento almacenado")  # Debugging

                return {"status": "success", "message": "Progreso actualizado exitosamente"}
            except Exception as e:
                # Muestra el error en la consola para depuración
                print("Error al actualizar el progreso:", e)
                return {"status": "error", "message": "Ocurrió un error al actualizar el progreso"}
        
        # Si la respuesta es incorrecta, no se actualiza el progreso
        return {"status": "error", "message": "La respuesta fue incorrecta, progreso no actualizado"}'''





    # 4. Consultar Ejercicios por Tema
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def exercises(self, topic_id):
        user_id = cherrypy.session.get('user_id')
        if user_id is None:
            return {"status": "error", "message": "Usuario no autenticado"}

        # Obtener el último ejercicio completado
        self.cursor.execute("""
            SELECT COALESCE(MAX(p.exercise_id), 0) AS last_completed_exercise
            FROM Progress p
            WHERE p.user_id = ? AND p.topic_id = ?;
        """, (user_id, topic_id))
        last_completed_exercise = self.cursor.fetchone()[0]

        # Consultar ejercicios desde el último ejercicio completado en adelante
        self.cursor.execute("""
            SELECT e.exercise_id, e.question, e.correct_answer
            FROM Exercises e
            WHERE e.topic_id = ? AND e.exercise_id >= ?;
        """, (topic_id, last_completed_exercise))

        exercises = [
            {"exercise_id": row[0], "question": row[1], "correct_answer": row[2]}
            for row in self.cursor.fetchall()
        ]
        return {"status": "success", "exercises": exercises}



    '''@cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def submit_progress(self):
        # Obtener datos de la solicitud JSON
        input_data = cherrypy.request.json
        user_id = cherrypy.session.get('user_id')
        
        # Mensajes de depuración para verificar el contenido del JSON
        print("Datos recibidos en JSON:", input_data)
        
        topic_id = input_data.get('topic_id')
        exercise_id = input_data.get('exercise_id')
        correct = input_data.get('correct')
        
        # Mensajes de depuración para verificar valores específicos
        print("User ID:", user_id)
        print("Topic ID:", topic_id)
        print("Exercise ID:", exercise_id)
        print("Correct:", correct)

        # Verificar que el usuario esté autenticado
        if user_id is None:
            return {"status": "error", "message": "Usuario no autenticado"}

        # Verificar que exercise_id no sea NULL
        if exercise_id is None:
            return {"status": "error", "message": "Exercise ID no puede ser NULL"}

        # Solo actualiza el progreso si la respuesta fue correcta
        if correct:
            # Verifica si ya hay un progreso registrado para el usuario y el tema
            self.cursor.execute("""
                SELECT progress_id FROM Progress 
                WHERE user_id = ? AND topic_id = ?;
            """, (user_id, topic_id))
            
            progress = self.cursor.fetchone()
            print("Progress record found:", progress)  # Debugging

            if progress:
                # Si existe un registro, actualiza el último ejercicio completado y la fecha
                self.cursor.execute("""
                    UPDATE Progress
                    SET exercise_id = ?, last_accessed = ?
                    WHERE progress_id = ?;
                """, (exercise_id, datetime.now(), progress[0]))
                print("Progreso actualizado para progress_id:", progress[0])  # Debugging
            else:
                # Si no existe un registro, crea uno nuevo
                self.cursor.execute("""
                    INSERT INTO Progress (user_id, topic_id, exercise_id, score, last_accessed)
                    VALUES (?, ?, ?, 0, ?);
                """, (user_id, topic_id, exercise_id, datetime.now()))
                print("Nuevo registro de progreso creado para user_id:", user_id)  # Debugging
            
            # Confirma los cambios en la base de datos
            self.conn.commit()
            print("Cambios confirmados en la base de datos")  # Debugging

            # Verificar si el usuario puede avanzar de nivel
            return self.update_level(user_id)

        # Si la respuesta es incorrecta, no se actualiza el progreso
        return {"status": "error", "message": "La respuesta fue incorrecta, progreso no actualizado"}

    def update_level(self, user_id):
        # Lógica para actualizar el nivel del usuario
        print("Actualizando nivel para user_id:", user_id)
        # Retorna el resultado del nivel actualizado
        return {"status": "success", "message": "Nivel actualizado exitosamente"}'''






    '''# 5. Registrar Avance del Usuario y Actualizar Nivel
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def submit_progress(self):
        data = cherrypy.request.json
        user_id = data.get("user_id")
        topic_id = data.get("topic_id")
        score = data.get("score")

        # Insertar o actualizar el progreso
        self.cursor.execute("""
            MERGE INTO Progress AS target
            USING (SELECT ? AS user_id, ? AS topic_id) AS source
            ON (target.user_id = source.user_id AND target.topic_id = source.topic_id)
            WHEN MATCHED THEN 
                UPDATE SET score = ?, last_accessed = ?
            WHEN NOT MATCHED THEN
                INSERT (user_id, topic_id, score, last_accessed) VALUES (?, ?, ?, ?);
        """, (user_id, topic_id, score, datetime.now(), user_id, topic_id, score, datetime.now()))
        
        self.conn.commit()

    # Verificar si el usuario puede avanzar de nivel
        return self.update_level(user_id)'''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def submit_progress(self):
        data = cherrypy.request.json
        user_id = data.get("user_id")
        topic_id = data.get("topic_id")
        score = data.get("score")
        exercise_id = data.get("exercise_id")  # Obtener exercise_id de los datos

        # Insertar o actualizar el progreso
        self.cursor.execute(""" 
            MERGE INTO Progress AS target
            USING (SELECT ? AS user_id, ? AS topic_id) AS source
            ON (target.user_id = source.user_id AND target.topic_id = source.topic_id)
            WHEN MATCHED THEN 
                UPDATE SET score = ?, last_accessed = ?, exercise_id = ?  -- Actualizar exercise_id
            WHEN NOT MATCHED THEN
                INSERT (user_id, topic_id, score, last_accessed, exercise_id) 
                VALUES (?, ?, ?, ?, ?);  -- Incluir exercise_id en el INSERT
        """, (user_id, topic_id, score, datetime.now(), exercise_id, 
                user_id, topic_id, score, datetime.now(), exercise_id))
        
        self.conn.commit()

        # Verificar si el usuario puede avanzar de nivel
        return self.update_level(user_id)
                


# Configuración de CherryPy
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Crear la carpeta de sesiones si no existe
    sessions_dir = os.path.join(current_dir, 'sessions')
    if not os.path.exists(sessions_dir):
        os.makedirs(sessions_dir)

    # Habilitar sesiones
    cherrypy.config.update({
        'tools.sessions.on': True,
        'tools.sessions.storage_type': 'file',
        'tools.sessions.storage_path': sessions_dir,  # Ruta actualizada
        'tools.sessions.timeout': 60
    })

    config = {
        '/': {
            'tools.staticdir.root': current_dir,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static',
        }
    }
    cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 8080})
    cherrypy.quickstart(SpanishApp(), '/', config)
