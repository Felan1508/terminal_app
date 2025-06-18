function joinRoom(roomName) {
    // Navigate to the room
    window.location.href = `/chat/${roomName}/`;

    // Highlight the active room (optional if full page reloads)
    document.querySelectorAll('.room-item').forEach(item => {
        item.classList.remove('active-room');
    });

    const activeButton = document.querySelector(`.room-item[onclick*="${roomName}"]`);
    if (activeButton) {
        activeButton.classList.add('active-room');
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const roomMatch = path.match(/\/chat\/(room\d+)\//);

    if (roomMatch) {
        const currentRoom = roomMatch[1];
        const activeButton = document.querySelector(`.room-item[onclick*="${currentRoom}"]`);
        if (activeButton) {
            activeButton.classList.add('active-room');
        }
    }
});
