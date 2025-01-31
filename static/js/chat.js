const baseUrl = window.location.origin.replace(/^http/, 'ws');
const socket = new WebSocket(baseUrl +"/ws/");

const $chatMessages = Qs(".messages");
var user_autenticated= '';

function scrollToBottom() {
    Qs(".messages").scrollTop = Qs(".messages").scrollHeight;
}
    
socket.onopen = () => {
    getAllRoom()
    console.log("Conectado")

}

const setRoomActive = (room_id) =>{
    var chatContainer = Qs('.chat-messages');
    QsAll(".list-rooms li").forEach(el => {
        el.classList.remove("active");
        
    })
    // var activeRoom = document.querySelector('.list-rooms li active');
        
        // Verifica se existe uma sala ativa
    chatContainer.style.display = 'block';


    Qs(`#room-${room_id}`).classList.add("active");
    Qs("#selected-room").value = room_id
    
};

const getMessages = async (wa_id) => {
    // Exemplo de como sair de uma sala
    // socket.send(JSON.stringify({
    //     'command': 'leave',
    //     'room_name': document.querySelector("#selected-room").value
    // }));
    const response = await fetch(`/${wa_id}`);
    const html = await response.text();
    $chatMessages.innerHTML = html

    setRoomActive(wa_id);
    
};


socket.onmessage = (e) => {
    data = JSON.parse(e.data)
    
    if (data.number==Qs('#selected-room').value) {
        addMessage(data)
    }
};


socket.onclose = () => {
    
}


const addMessage = (data) =>{
        var html = `
        <div class="chat-message  message-received clearfix">
            <div class="message-text">
            <div class="message-username">${data.user}</div>
            ${data.message}
            </div>
        </div>
        `  
        const $uniqueMessageContainer = Qs("#messages");
        $uniqueMessageContainer.insertAdjacentHTML("beforeend", html);
    }




const getAllRoom = async (data) =>{
    
    socket.send(JSON.stringify({
        'command': 'getRooms',

    }));

}
const sendMessage = async (data) =>{
    var response = await fetch('/send_message',{
        method:"POST",
        headers:{
            "Content-type":"aplication/json",
            "X-CSRFToken":data.csrfmiddlewaretoken
        },
        body: JSON.stringify(data)
    })

    Qs(".send-message").reset()
};

const createRoom = async (data) =>{

    socket.send(JSON.stringify({
        'command': 'createRoom',
        'room_name': data.title
    }));
    const modal = bootstrap.Modal.getInstance(Qs(".modal"));
    modal.hide()
    
    
}


const getLastRoom  =  () => {
    Qs(".list-rooms li").click();
}


Qs(".send-message").addEventListener('submit', (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    sendMessage(data);
});

const textarea = document.getElementById('chat_textarea');
const form = Qs(".send-message");


// textarea.addEventListener('input', ()=>{
//     form.style.height = 'auto'; // Reseta a altura para calcular a nova altura corretamente
//     textarea.style.height = 'auto'; // Reseta a altura para calcular a nova altura corretamente
//     textarea.style.height = (textarea.scrollHeight) + 'px'; 
// }
// );


// Qs(".create-room").addEventListener('submit', (e) =>{
//     e.preventDefault();
//     const data = Object.fromEntries(new FormData(e.target).entries());
//     createRoom(data)
// })


function scrollToBottom() {
    var messages = document.getElementById('messages');
    messages.scrollTop = messages.scrollHeight;
}


const addRoom= (room) =>{
    html = `<li role='button'class = "list-group-item"  id="room-${room.id}" onclick="getMessages('${room.id}')">${room.title}</li> `
    const $uniqueRoomContainer = Qs(".list-rooms");
    $uniqueRoomContainer.insertAdjacentHTML("afterbegin", html);
}
