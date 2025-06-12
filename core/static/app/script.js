        const terminal = document.getElementById('terminal');
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

        socket.onclose = function () {
            appendOutput("\nWebSocket connection closed.");
        };

        function appendOutput(data) {
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