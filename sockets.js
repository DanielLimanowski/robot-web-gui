/**
 * Created by dlimanow on 4/26/2017.
 */
window.onload = function () {
    var form = document.getElementById('cmd_form');
    var command = document.getElementById('cmd_sel');
    var parameter = document.getElementById('cmd_param');
    var status = document.getElementById('socket_status');
    var messages = document.getElementById('message_list');


    //specify correct server ip/url in WebSocket()
    var web_socket = new WebSocket('ws://127.0.0.1:5000');

    //error handling
    web_socket.onerror = function(error) {
        console.log('WEBSOCKET ERROR: ' + error);
    };

    //update status on page when we connect to the socket successfully
    web_socket.onopen = function(event) {
        status.innerHTML = 'Success! Connected to web socket.';

        //TODO: Implement in css
        status.className = 'socket_open';
    };

    web_socket.onmessage = function(event) {
        var msg = event.data;
        //TODO: Implement received in css
        messages.innerHTML += '<li class="received"><span>Received:</span>' + msg + '</li>'
    };



}