// Main application script
document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('start-test');
    const textToType = document.getElementById('text-to-type');
    const userInput = document.getElementById('user-input');
    const wpmElement = document.getElementById('wpm');
    const accuracyElement = document.getElementById('accuracy');

    let startTime;
    let endTime;
    let isTestRunning = false;

    startButton.addEventListener('click', async function() {
        if (isTestRunning) {
            return;
        }

        try {
            const response = await fetch('/get_text');
            const data = await response.json();
            textToType.textContent = data.text;

            userInput.value = '';
            userInput.disabled = false;
            userInput.focus();

            startTime = Date.now();
            isTestRunning = true;

            startButton.textContent = 'End Test';

            userInput.addEventListener('input', function() {
                const typedText = userInput.value;
                const correctChars = calculateCorrectChars(typedText, data.text);
                const accuracy = (correctChars / data.text.length) * 100;
                accuracyElement.textContent = Math.round(accuracy);
            });
        } catch (error) {
            console.error('Error fetching typing text:', error);
        }
    });

    userInput.addEventListener('input', function() {
        if (!isTestRunning) {
            return;
        }

        const typedText = userInput.value;
        const correctChars = calculateCorrectChars(typedText, textToType.textContent);
        const accuracy = (correctChars / textToType.textContent.length) * 100;
        accuracyElement.textContent = Math.round(accuracy);
    });

    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && isTestRunning) {
            endTest();
        }
    });

    function calculateCorrectChars(typedText, originalText) {
        let correctChars = 0;
        for (let i = 0; i < Math.min(typedText.length, originalText.length); i++) {
            if (typedText[i] === originalText[i]) {
                correctChars++;
            }
        }
        return correctChars;
    }

    async function endTest() {
        if (!isTestRunning) {
            return;
        }

        endTime = Date.now();
        const timeElapsed = (endTime - startTime) / 1000;
        const typedText = userInput.value;
        const wordsTyped = calculateWordsTyped(typedText);
        const wpm = calculateWPM(wordsTyped, timeElapsed);
        const correctChars = calculateCorrectChars(typedText, textToType.textContent);
        const totalChars = textToType.textContent.length;

        wpmElement.textContent = Math.round(wpm);
        accuracyElement.textContent = Math.round((correctChars / totalChars) * 100);

        try {
            const response = await fetch('/save_score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    wordsTyped: wordsTyped,
                    timeElapsed: timeElapsed,
                    correctChars: correctChars,
                    totalChars: totalChars
                })
            });

            const result = await response.json();
            console.log(result.message);
        } catch (error) {
            console.error('Error saving score:', error);
        }

        userInput.disabled = true;
        isTestRunning = false;
        startButton.textContent = 'Start Test';
    }

    function calculateWordsTyped(text) {
        return text.trim().split(/\s+/).length;
    }

    function calculateWPM(wordsTyped, timeElapsed) {
        return (wordsTyped / (timeElapsed / 60)).toFixed(1);
    }
});
