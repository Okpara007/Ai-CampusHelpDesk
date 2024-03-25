const speechButton = document.getElementById('speech');

let recognition = new webkitSpeechRecognition() || SpeechRecognition();

recognition.lang = 'en-Us';


speechButton.addEventListener('click', function(){
    recognition.start();
});

recognition.onresult = function(e) {
    const transcript = e.results[0][0].transcript;
    body.appendChild(mgses(transcript, "user"));
    sendTextToServer(transcript);
};

recognition.onerror = function(e){
    console.error(e.error);
};

function sendTextToServer(text) {
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text:text})
    })
    .then(response => response.json())
    .then(data => {
        const response = data.res
        setTimeout(() => {
            body.appendChild(mgses(response, "assistant"));
        }, 600);
    })
    .catch(error => {
        console.error('Error sending text to server:', error);
    });
}


