create database aprender

use aprender

CREATE TABLE Users (
    user_id INT PRIMARY KEY IDENTITY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(50) NOT NULL,
    level INT DEFAULT 1
);

CREATE TABLE Levels (
    level_id INT PRIMARY KEY,
    name NVARCHAR(50) NOT NULL,
    description NVARCHAR(255) NOT NULL
);

CREATE TABLE Topics (
    topic_id INT PRIMARY KEY IDENTITY,
    level_id INT NOT NULL,
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(255),
    FOREIGN KEY (level_id) REFERENCES Levels(level_id)
);

CREATE TABLE Exercises (
    exercise_id INT PRIMARY KEY IDENTITY,
    topic_id INT NOT NULL,
    question NVARCHAR(255) NOT NULL,
    correct_answer NVARCHAR(255) NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
);

CREATE TABLE Progress (
    progress_id INT PRIMARY KEY IDENTITY,
    user_id INT NOT NULL,
    topic_id INT NOT NULL,
    score INT CHECK (score BETWEEN 0 AND 100),
    last_accessed DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
);

ALTER TABLE Progress ADD exercise_id INT NULL;


INSERT INTO Levels (level_id, name, description)
VALUES 
    (1, 'Principiante', 'Nivel básico para aprender conceptos básicos del español'),
    (2, 'Intermedio', 'Nivel intermedio para aprender gramática y frases comunes'),
    (3, 'Avanzado', 'Nivel avanzado para dominar el español en conversaciones complejas'),
	(4, 'Experto', 'Nivel experto para perfeccionar habilidades y expresarse como un hablante nativo'),
    (5, 'Maestría', 'Nivel de maestría para quienes buscan un conocimiento completo del idioma y su cultura');


INSERT INTO Topics (level_id, name, description)
VALUES 
    (1, 'Saludos y Presentaciones', 'Aprender a saludar y presentarse en español'),
    (1, 'Colores y Números', 'Conceptos básicos de colores y números en español'),
    (2, 'Conjugación de Verbos', 'Conjugación de verbos en presente'),
    (2, 'Frases Cotidianas', 'Frases comunes para conversaciones diarias'),
    (3, 'Conversación Compleja', 'Vocabulario y frases para conversaciones avanzadas'),
    (3, 'Expresiones Idiomáticas', 'Expresiones comunes en el habla nativa'),
	(4, 'Expresiones Culturales', 'Frases y expresiones típicas de diversas culturas hispanohablantes'),
    (4, 'Lenguaje Técnico y Profesional', 'Vocabulario técnico para ámbitos profesionales'),
    (5, 'Literatura Española', 'Análisis y comprensión de textos literarios en español'),
    (5, 'Modismos Regionales', 'Explorar modismos y expresiones únicas de regiones hispanohablantes');









--Saludos y presentaciones
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (1, '¿Cómo se dice "Hello" en español?', 'Hola'),
    (1, '¿Cómo preguntas "What is your name?" en español?', '¿Cual es tu nombre?'),
    (1, '¿Cómo respondes "My name is Ana"?', 'Mi nombre es Ana'),
    (1, '¿Cómo se dice "Goodbye" en español?', 'Adios'),
    (1, '¿Cómo preguntas "How are you?" en español?', '¿Como estas?'),
    (1, '¿Cómo respondes "I am fine" en español?', 'Estoy bien'),
	(1, '¿Cómo preguntas "Where are you from?" en español?', '¿De donde eres?'),
    (1, '¿Qué significa "Nice to meet you"?', 'Encantado de conocerte'),
    (1, '¿Cómo respondes "I am from Guatemala" en español?', 'Soy de Guatemala');

-- Colores y Números
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (2, '¿Cual es el color del cielo?', 'Azul'),
    (2, '¿Como se dice "five" en español?', 'Cinco'),
    (2, '¿Que color es el sol?', 'Amarillo'),
    (2, '¿Como se dice "red" en español?', 'Rojo'),
    (2, '¿Que color es el pasto?', 'Verde'),
    (2, '¿Como se dice "ten" en español?', 'Diez'),
    (2, '¿Que color es una manzana madura?', 'Rojo'),
	(2, '¿Qué color es el agua del océano?', 'Azul'),
    (2, '¿Cómo se dice "green" en español?', 'Verde'),
    (2, '¿Cuántos son cinco más tres?', 'Ocho');

-- Conjugacion de Verbos
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (3, 'Conjuga "yo (comer)" en presente', 'como'),
    (3, 'Conjuga "tu (vivir)" en presente', 'vives'),
    (3, 'Conjuga "el (tener)" en presente', 'tiene'),
    (3, 'Conjuga "nosotros (hablar)" en presente', 'hablamos'),
    (3, 'Conjuga "ellos (escribir)" en presente', 'escriben'),
    (3, 'Conjuga "ella (ser)" en presente', 'es'),
	(3, 'Conjuga "él (comer)" en presente', 'come'),
    (3, 'Conjuga "yo (vivir)" en presente', 'vivo'),
    (3, 'Conjuga "ustedes (correr)" en presente', 'corren');

-- Frases Cotidianas
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (4, '¿Como se dice "How are you?" en español?', '¿Como estas?'),
    (4, '¿Que significa "Good night"?', 'Buenas noches'),
    (4, '¿Como se dice "Good morning" en español?', 'Buenos dias'),
    (4, '¿Que significa "See you later"?', 'Hasta luego'),
    (4, '¿Como se dice "Thank you" en español?', 'Gracias'),
    (4, '¿Que significa "Sorry"?', 'Perdon'),
	(4, '¿Cómo se dice "Excuse me, where is the bathroom?" en español?', 'Disculpa, ¿donde esta el baño?'),
    (4, '¿Qué significa "I’m sorry"?', 'Lo siento'),
    (4, '¿Cómo se dice "I don’t understand" en español?', 'No entiendo');

-- Conversacion Compleja
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (5, '¿Como se dice "I would like to travel to Guatemala" en español?', 'Me gustaria viajar a Guatemala'),
    (5, '¿Que significa "I am excited to see yo"?', 'Estoy emocionado de verte'),
    (5, '¿Como se dice "I need help" en español?', 'Necesito ayuda'),
    (5, '¿Que significa "I miss you"?', 'Te extraño'),
    (5, '¿Como se dice "I am learning Spanish" en español?', 'Estoy aprendiendo español'),
    (5, '¿Que significa "I want to visit new places"?', 'Quiero visitar nuevos lugares'),
	(5, '¿Cómo se dice "I would like to practice my Spanish" en español?', 'Me gustaria practicar mi español'),
    (5, '¿Qué significa "Thank you very much"?', 'Te agradezco mucho'),
    (5, '¿Cómo se dice "I feel nervous" en español?', 'Me siento nervioso');

-- Expresiones Idiomaticas
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (6, '¿Que significa "To be daydreaming"?', 'Estar en las nubes'),
    (6, '¿Como se dice "break the ice" en español?', 'Romper el hielo'),
    (6, '¿Que significa "To give up"?', 'Tirar la toalla'),
    (6, '¿Como se dice "to kill two birds with one stone" en español?', 'Matar dos pajaros de un tiro'),
    (6, '¿Que significa "Every cloud has a silver lining"?', 'No hay mal que por bien no venga'),
    (6, '¿Como se dice "bite the bullet" en español?', 'Aguantar vara'),
	(6, '¿Qué significa "To be in a difficult situation"?', 'Estar en una situacion dificil'),
    (6, '¿Cómo se dice "be in seventh heaven"?', 'Estar en el septimo cielo'),
    (6, '¿Qué significa "Dont mince words"?', 'No te andes con rodeos');

	-- Expresiones Culturales
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (7, 'Como se dice "Let’s get to work" en español de Guatemala?', 'Vamos a trabajar'),
    (7, 'Que significa "Long live the party" en español?', 'Que viva la fiesta'),
    (7, 'Como se dice "Better late than never" en español?', 'Mas vale tarde que nunca'),
    (7, 'Como se dice "This is a big celebration" en español?', 'Esto es una gran celebracion'),
    (7, 'Como se dice "To feel right at home" en español?', 'Sentirse como en casa'),
    (7, 'Como se dice "To have a great time" en español?', 'Pasarla bien'),
    (7, 'Que significa "Put on a brave face in difficult times" en español?', 'Al mal tiempo, buena cara'),
    (7, 'Como se dice "Good vibes only" en español?', 'Solo buenas vibras');

-- Lenguaje Tecnico y Profesional
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (8, 'Como se dice "database" en español?', 'Base de datos'),
    (8, 'Como se dice "Job market" en español?', 'Mercado laboral'),
    (8, 'Como se dice "To apply for a job" en español?', 'Postularse para un trabajo'),
    (8, 'Como se dice "Software engineering" en español?', 'Ingenieria de software'),
    (8, 'Como se dice "Project management" en español?', 'Gestion de proyectos'),
    (8, 'Como se dice "Data analysis" en español?', 'Analisis de datos'),
    (8, 'Como se dice "Network security" en español?', 'Seguridad de red'),
    (8, 'Como se dice "Financial management" en español?', 'Administracion financiera'),
    (8, 'Como se dice "To conduct research" en español?', 'Realizar una investigacion');

-- Literatura Espanola
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (9, 'Quien escribio "Don Quijote de la Mancha"?', 'Miguel de Cervantes'),
    (9, 'Como se dice "Lyrical poetry" en español?', 'Poesia lirica'),
    (9, 'Como se llama el autor de "Cien Años de Soledad"?', 'Gabriel Garcia Marquez'),
    (9, 'Como se dice "Magical realism" en español?', 'Realismo magico'),
    (9, 'Como se dice "Poetry" en español?', 'Poesia'),
    (9, 'Que obra escribio Federico Garcia Lorca?', 'La Casa de Bernarda Alba'),
    (9, 'Como se dice "Novel" en español?', 'Novela'),
    (9, 'Como se dice "Romanticism" en español?', 'Romanticismo'),
    (9, 'Quien es el autor de "El amor en los tiempos del colera"?', 'Gabriel Garcia Marquez');

-- Modismos Regionales
INSERT INTO Exercises (topic_id, question, correct_answer) VALUES
    (10, 'Como se dice "How cool!" en español de Guatemala?', 'Que chilero'),
    (10, 'Como se dice "Let’s grab a coffee" en español de Guatemala?', 'Vamos por un cafe'),
    (10, 'Como se dice "Pure life / All good" en español de Costa Rica?', 'Pura vida'),
    (10, 'Como se dice "No way!" en español de Argentina?', 'Ni a palos'),
    (10, 'Como se dice "To be really worried" en español?', 'Andar con el Jesus en la boca'),
    (10, 'Como se dice "I am really tired" en español de Mexico?', 'Estoy muerto'),
    (10, 'Como se dice "To be very tired" en español de Chile?', 'Estar hecho lena'),
    (10, 'Como se dice "I can’t believe it" en español de Argentina?', 'No lo puedo creer'),
    (10, 'Como se dice "To be awesome at something" en español de Mexico?', 'Ser un chingon');






CREATE PROCEDURE UpdateUserLevel
    @userId INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @totalQuestions INT;
    DECLARE @correctAnswers INT;
    DECLARE @averageScore FLOAT;

    -- Calcular el número total de preguntas y respuestas correctas para el usuario
    SELECT 
        @totalQuestions = COUNT(*),
        @correctAnswers = SUM(CASE WHEN score >= 80 THEN 1 ELSE 0 END) -- Asumimos que score >= 80 significa correcto
    FROM Progress
    WHERE user_id = @userId;

    -- Calcular el puntaje promedio
    IF @totalQuestions > 0
    BEGIN
        SET @averageScore = (@correctAnswers * 100.0) / @totalQuestions;  -- Calcular el porcentaje de respuestas correctas
    END
    ELSE
    BEGIN
        SET @averageScore = 0;  -- Si no hay preguntas, el puntaje promedio es 0
    END

    -- Actualizar el nivel si el promedio es mayor o igual a 80
    IF @averageScore >= 80
    BEGIN
        UPDATE Users
        SET level = level + 1
        WHERE user_id = @userId;
    END
END

CREATE PROCEDURE SaveUserProgress
    @user_id INT,
    @topic_id INT,
    @exercise_id INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Insertar o actualizar el progreso del usuario
    MERGE INTO Progress AS target
    USING (SELECT @user_id AS user_id, @topic_id AS topic_id) AS source
    ON (target.user_id = source.user_id AND target.topic_id = source.topic_id)
    WHEN MATCHED THEN 
        UPDATE SET exercise_id = @exercise_id, last_accessed = GETDATE()
    WHEN NOT MATCHED THEN
        INSERT (user_id, topic_id, exercise_id, score, last_accessed) 
        VALUES (@user_id, @topic_id, @exercise_id, 0, GETDATE());
END;


