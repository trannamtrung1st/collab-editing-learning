function post(msg) {
    const temp1 = document.getElementById('office_frame').contentWindow;
    temp1.postMessage(JSON.stringify(msg), '*');
}

function postReady() {
    post({ 'MessageId': 'Host_PostmessageReady' });
}

function save() {
    post({
        'MessageId': 'Action_Save',
        'Values': { 'Notify': true, 'ExtendedData': 'CustomFlag=Custom Value;AnotherFlag=AnotherValue' }
    });
}

function receiveMessage(event) {
    console.log('==== framed.doc.html receiveMessage: ' + event.data);
    var msg = JSON.parse(event.data);
    if (!msg) {
        return;
    }

    let messageOut = document.getElementById("messages");
    messageOut.textContent = messageOut.textContent + JSON.stringify(msg) + "\n";

    if (msg.MessageId == 'App_LoadingStatus') {
        if (msg.Values) {
            if (msg.Values.Status == 'Document_Loaded') {
                postReady();
            }
        }
    }
}

// 'main' code of this <script> block, run when page is being
// rendered. Install the message listener.
window.addEventListener("message", receiveMessage, false);