
   
    const socket = new WebSocket('ws://' + window.location.host + '/ws/terminal/');
    
    function stopCommand() {
    console.log("Sending stop...");
    socket.send("__STOP__");
    }

    socket.onopen = function () {
        appendOutput("WebSocket connection established.\n");
    };

    socket.onmessage = function (e) {
        appendOutput(e.data);
    };

    socket.onclose = function (event) {
    appendOutput("\nWebSocket connection closed.");
    appendOutput("\nCode: " + event.code + " Reason: " + event.reason);
    };
    
    socket.onerror = function (e) {
    appendOutput("\nWebSocket error occurred.");
    console.error("WebSocket error:", e);
    };

    function appendOutput(data) {
        const terminal = document.getElementById('terminal');
        terminal.textContent += data;
        terminal.scrollTop = terminal.scrollHeight;
    }

    function sendCommand() {
        const cmdInput = document.getElementById('command');
        const command = cmdInput.value.trim();
        if (command) {
            socket.send(command);
            appendOutput(`\n$ ${command}\n`);
            cmdInput.value = '';
        }
    }

/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}