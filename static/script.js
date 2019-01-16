// If user hasn't set a display name, redirect them to create one
if (!localStorage.getItem('displayName') && window.location.pathname != "/displayname") {
  window.location.replace('/displayname')
}


document.addEventListener('DOMContentLoaded', () => {



  //Code for displayname page
  if (window.location.pathname == "/displayname") {
    document.querySelector('#displayNameForm').onsubmit = () => {
      localStorage.setItem('displayName', document.querySelector('#displayName').value);
    }
  }

  // When a new chat is created
  document.querySelector('#newChat').onclick = () => {

    // If nothing was inputted
    if (document.querySelector('#newChatName').value.length == 0) {
      alert('Please enter fields')
      return false;
    }

    // Initialize the request and the data
    const request = new XMLHttpRequest();
    const newChatName = document.querySelector('#newChatName').value;
    request.open('POST', '/newchat');

    // When the server returns a responese
    request.onload = () => {

      // Get data
      const data = JSON.parse(request.responseText);

      // If it was a success redirect to new chat
      if (data.success) {
        window.location.href = (`/chat/${newChatName}`)
      }
      // Else, alert user (This will be changed later)
      else {
        alert('Chat name already taken')
      }

    }

    // Get ready to send data
    const data = new FormData();
    data.append('newChatName', newChatName)

    // Send data
    request.send(data)
  }

  var socket = io();

  socket.on('connect', () => {

    document.querySelector('#newMessageSubmit').onclick = () => {

      if (document.querySelector('#newMessage').value.length == 0) {
        alert('Please enter fields');
        return false;
      }

      else {
        const message = document.querySelector('#newMessage').value;
        const room = document.querySelector('#roomName').value;
        const user = localStorage.getItem('displayName');





        socket.emit('new message', {'user': user, 'message': message, 'room': room});


      }
    }
  })
  socket.on('display message', data => {

    const p = document.createElement('p')
    p.innerHTML = `${data.time} ${data.user}: ${data.message}`
    document.querySelector('#allMessages').append(p)

    if (document.getElementById("allMessages").getElementsByTagName("li").length > 100) {
      let elem = document.querySelector('#allMessages li');
      elem.parentNode.removeChild(elem)
    }
  })




})
