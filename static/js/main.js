// Main application script
document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('start-test');
    const textToType = document.getElementById('text-to-type');
    const userInput = document.getElementById('user-input');
    const wpmElement = document.getElementById('wpm');
    const accuracyElement = document.getElementById('accuracy');
    const statsContainer = document.querySelector('.stats-container');
    const bestWpmElement = document.getElementById('best-wpm');
    const avgWpmElement = document.getElementById('avg-wpm');
    const gamesPlayedElement = document.getElementById('games-played');
    const accuracyStatElement = document.getElementById('accuracy-stat');

    let startTime;
    let endTime;
    let isTestRunning = false;
    let currentText = '';
    let errorPositions = new Set(); // Track positions of errors

    // Function to load user statistics
    async function loadUserStats() {
        try {
            const response = await fetch('/user_history');
            const data = await response.json();
            
            if (data.length > 0) {
                // Calculate statistics
                const bestWpm = Math.max(...data.map(score => score.wpm));
                const avgWpm = data.reduce((sum, score) => sum + score.wpm, 0) / data.length;
                const accuracy = Math.round(data.reduce((sum, score) => sum + score.accuracy, 0) / data.length);
                
                // Update statistics display
                bestWpmElement.textContent = bestWpm;
                avgWpmElement.textContent = avgWpm.toFixed(1);
                gamesPlayedElement.textContent = data.length;
                accuracyStatElement.textContent = accuracy + '%';
            }
        } catch (error) {
            console.error('Error loading user statistics:', error);
        }
    }

    // Function to load new typing text
    async function loadText() {
        try {
            const response = await fetch('/get_text');
            const data = await response.json();
            currentText = data.text;
            textToType.textContent = currentText;
        } catch (error) {
            console.error('Error fetching typing text:', error);
        }
    }

    // Load statistics when page loads
    loadUserStats();

    startButton.addEventListener('click', async function() {
        if (isTestRunning) {
            return;
        }

        await loadText();

        userInput.value = '';
        userInput.disabled = false;
        userInput.focus();

        startTime = Date.now();
        isTestRunning = true;

        startButton.textContent = 'End Test';
    });

    userInput.addEventListener('input', function() {
        if (!isTestRunning) {
            return;
        }

        const typedText = userInput.value;
        
        // Track errors
        for (let i = 0; i < Math.min(typedText.length, currentText.length); i++) {
            if (typedText[i] !== currentText[i]) {
                errorPositions.add(i);
            }
        }

        // Calculate accuracy based on error positions
        const totalChars = currentText.length;
        const errors = Array.from(errorPositions).length;
        const accuracy = ((totalChars - errors) / totalChars) * 100;
        accuracyElement.textContent = Math.round(accuracy) + '%';

        // Calculate WPM based on time elapsed
        const timeElapsed = (Date.now() - startTime) / 1000;
        const wordsTyped = calculateWordsTyped(typedText);
        const wpm = calculateWPM(wordsTyped, timeElapsed);
        wpmElement.textContent = Math.round(wpm);

        // Update the text display to show errors
        const textDisplay = document.getElementById('text-to-type');
        let displayText = '';
        for (let i = 0; i < Math.max(typedText.length, currentText.length); i++) {
            if (i < typedText.length && i < currentText.length) {
                if (typedText[i] === currentText[i]) {
                    displayText += `<span class="correct">${typedText[i]}</span>`;
                } else {
                    displayText += `<span class="incorrect">${typedText[i]}</span>`;
                }
            } else if (i < currentText.length) {
                displayText += `<span class="remaining">${currentText[i]}</span>`;
            }
        }
        textDisplay.innerHTML = displayText;
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

    function calculateWordsTyped(text) {
        // Split text into words, ignoring punctuation
        const words = text.trim().split(/\s+/);
        return words.length;
    }

    function calculateWPM(wordsTyped, timeElapsed) {
        // Calculate words per minute
        return (wordsTyped / (timeElapsed / 60)).toFixed(1);
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
        
        // Calculate final accuracy using error positions
        const totalChars = currentText.length;
        const errors = Array.from(errorPositions).length;
        const accuracy = ((totalChars - errors) / totalChars) * 100;

        wpmElement.textContent = Math.round(wpm);
        accuracyElement.textContent = Math.round(accuracy) + '%';

        try {
            const response = await fetch('/save_score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    wpm: wpm,
                    accuracy: Math.round(accuracy)
                })
            });

            const result = await response.json();
            console.log(result.message);

            // Reload statistics after saving score
            loadUserStats();
        } catch (error) {
            console.error('Error saving score:', error);
        }

        userInput.disabled = true;
        isTestRunning = false;
        startButton.textContent = 'Start Test';
        errorPositions.clear(); // Reset error positions for next session
    }
});
