document.addEventListener('DOMContentLoaded', () => {
    const ws = new WebSocket('ws://localhost:8001');
    const userCount = document.getElementById('usersCount');
    const weightClass = document.getElementById('weightClass');
    const redBot = document.getElementById('redBot');
    const blueBot = document.getElementById('blueBot');
    const updateBtn = document.getElementById('update');

    updateBtn.addEventListener('click', () => {
        ws.send(JSON.stringify({type: 'match', value: {
            weightClass: weightClass.value,
            redBot: redBot.value,
            blueBot: blueBot.value
        }}));
    })

    ws.onmessage = ({ data }) => {
        // variable name is data because we're destructuring the data key from the message.
        const event = JSON.parse(data);
        switch (event.type) {
            case 'users':
                console.log(`A user connected or disconnected. There are currently ${event.count} users.`);
                userCount.innerText = event.count;
                break;
            default:
                console.log(`I'm not sure what to do with ${event.type} events.`);
        }
    }

})