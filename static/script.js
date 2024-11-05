let userId = null;
let currentTopicId = null;
let currentExerciseIndex = 0;
let exercisesData = [];
let currentScore = 0;

// Registro de usuario
function registerUser() {
    const username = document.getElementById("reg_username").value;
    const password = document.getElementById("reg_password").value;

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("registerMessage").innerText = data.message;
    });
}

// Inicio de sesión
function loginUser() {
    const username = document.getElementById("login_username").value;
    const password = document.getElementById("login_password").value;

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            userId = data.user_id;
            showSection("topicsSection");
        } else {
            document.getElementById("loginMessage").innerText = data.message;
        }
    });
}

// Obtener y mostrar temas
function fetchTopics() {
    fetch("/topics")
    .then(response => response.json())
    .then(data => {
        const topicsContainer = document.getElementById("topicsContainer");
        topicsContainer.innerHTML = "";
        data.topics.forEach(topic => {
            const topicCard = document.createElement("div");
            topicCard.classList.add("topic-card");
            topicCard.innerHTML = `<h3>${topic.name}</h3><p>${topic.description}</p>`;
            topicCard.onclick = () => fetchExercises(topic.topic_id);
            topicsContainer.appendChild(topicCard);
        });
    });
}

// Obtener ejercicios del tema seleccionado
function fetchExercises(topicId) {
    currentTopicId = topicId;
    fetch(`/exercises?topic_id=${topicId}`)
    .then(response => response.json())
    .then(data => {
        exercisesData = data.exercises;
        currentExerciseIndex = 0;
        currentScore = 0;
        loadExercise();
    });
}

// Cargar la pregunta actual
function loadExercise() {
    const exercise = exercisesData[currentExerciseIndex];
    document.getElementById("exerciseQuestion").innerText = exercise.question;
    document.getElementById("userAnswer").value = "";
    document.getElementById("feedback").innerText = "";
    showSection("exerciseSection");
}

// Verificar si la respuesta es correcta
function checkAnswer() {
    const userAnswer = document.getElementById("userAnswer").value.trim().toLowerCase();
    const correctAnswer = exercisesData[currentExerciseIndex].correct_answer.trim().toLowerCase();

    if (userAnswer === correctAnswer) {
        currentScore++;
        document.getElementById("feedback").innerText = "¡Correcto!";
    } else {
        document.getElementById("feedback").innerText = "Incorrecto, intenta de nuevo.";
        return;
    }

    currentExerciseIndex++;
    if (currentExerciseIndex < exercisesData.length) {
        setTimeout(loadExercise, 1000);
    } else {
        checkLevelProgress();
    }
}

// Guardar el avance del usuario
/*function saveProgress() {
    const score = Math.round((currentScore / exercisesData.length) * 100);

    fetch("/submit_progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: userId,
            topic_id: currentTopicId,
            score: score
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}*/
function saveProgress() {
    const score = Math.round((currentScore / exercisesData.length) * 100);
    const currentExerciseId = exercisesData[currentExerciseIndex]?.exercise_id || null;  // Obtén el ID del ejercicio actual
    const correct = (currentScore > 0);  // Esto determina si el usuario respondió correctamente o no

    console.log("Saving progress...");
    console.log("User ID:", userId);
    console.log("Topic ID:", currentTopicId);
    console.log("Exercise ID:", currentExerciseId);
    console.log("Score:", score);
    console.log("Correct:", correct);

    fetch("/submit_progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: userId,
            topic_id: currentTopicId,
            exercise_id: currentExerciseId,
            score: score,
            correct: correct
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data);
        alert(data.message);
    })
    .catch(error => {
        console.error("Error saving progress:", error);
    });
}
function updateProgress() {
    const currentExerciseId = exercisesData[currentExerciseIndex]?.exercise_id || null; // Obtiene el ID del ejercicio actual
    const correct = (currentScore > 0); // Determina si la respuesta fue correcta

    fetch('/update_progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            topic_id: currentTopicId,
            exercise_id: currentExerciseId,
            correct: correct
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Verificar el avance de nivel
function checkLevelProgress() {
    const percentageScore = Math.round((currentScore / exercisesData.length) * 100);

    if (percentageScore >= 80) {
        document.getElementById("levelMessage").innerText = `¡Felicidades! Has obtenido un puntaje de ${percentageScore}% y puedes avanzar al siguiente nivel.`;
        showSection("levelSection");
    } else {
        document.getElementById("levelMessage").innerText = `Obtuviste un puntaje de ${percentageScore}%. Debes mejorar para avanzar de nivel.`;
        showSection("levelSection");
    }
}

// Continuar al siguiente nivel
function continueToNextLevel() {
    alert("Avanzando al siguiente nivel...");
    fetchTopics(); // Cargar nuevos temas
    showSection("topicsSection");
}

// Mostrar una sección específica
function showSection(sectionId) {
    document.querySelectorAll(".content-section, .auth-section").forEach(section => {
        section.style.display = section.id === sectionId ? "block" : "none";
    });
}
