const plusQuestion = document.getElementById("plusQuestion");
const plusResultDivision = document.getElementById("plusResultDivision");
let questionNumber = 1
let resultNumber = 1
addQuestion();
questionNumber++;


plusQuestion.onclick = () => {
    addQuestion();
    questionNumber++;
}

plusResultDivision.onclick = () => {
    addResult();
    resultNumber++;
}

function addQuestion() {
    const parentDiv = plusQuestion.parentNode;
    const div = document.createElement('div');
    div.innerHTML = `
        <div class="card" style="padding: 5%; margin: 3% 0 2% 0;">
            <h5><b>Вопрос №${questionNumber}</b></h5>
            <textarea id="question${questionNumber}" name="question${questionNumber}"></textarea><br>

            <p><b>Ответ 1</b></p>
            <input id="answer${questionNumber}" name="answer${questionNumber}.1"><br>
            <p><b>Баллы</b></p>
            <input id="score${questionNumber}" name="score${questionNumber}.1" type="number" min="0"><br>

            <p><b>Ответ 2</b></p>
            <input id="answer${questionNumber}" name="answer${questionNumber}.2"><br>
            <p><b>Баллы</b></p>
            <input id="score${questionNumber}" name="score${questionNumber}.2" type="number" min="0"><br>

            <p><b>Ответ 3</b></p>
            <input id="answer${questionNumber}" name="answer${questionNumber}.3"><br>
            <p><b>Баллы</b></p>
            <input id="score${questionNumber}" name="score${questionNumber}.3" type="number" min="0"><br>
        </div>
    `;
    parentDiv.insertBefore(div, plusQuestion);
}


function addResult() {
    const parentDiv = plusResultDivision.parentNode;
    const div = document.createElement('div');
    div.innerHTML = `
        <input id="result_score_${resultNumber}" name="result_score_${resultNumber}"
            type="number" min="0" placeholder="Баллы" class="col-md-2">
        <input id="result_message_${resultNumber}" name="result_message_${resultNumber}"
            placeholder="Сообщение" class="col-md-8"><br><br>
    `;
    parentDiv.insertBefore(div, plusResultDivision);
}
