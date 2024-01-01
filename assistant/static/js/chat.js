const sidebar = document.querySelector("#logo-sidebar");
const msg = document.querySelectorAll(".message");
const logo = document.querySelectorAll(".name");
const side = document.querySelectorAll(".logo-side");
const form = document.querySelectorAll("#message-form");
const hide_sidebar = document.querySelector(".hide-sidebar");
const new_chat_button = document.querySelector(".new-chat");
const views = document.querySelectorAll(".view");
let isBarHidden = false
let chat_id = getChatId()

function scrollToBottomOfResults() {
    const terminalResultsDiv = document.querySelectorAll("view");

    terminalResultsDiv.forEach(function(end){
        end.scrollTop = end.scrollHeight;
    })
};

// #############  SIDEBAR FUNCTIONALITY ###################
// MAKES THE SIDEBAR GOES IN
hide_sidebar.addEventListener('click', function() {
    sidebar.style.opacity = '0';
    sidebar.style.transform = 'translateX(-100%)';
    isBarHidden = true;

    views.forEach(function(element) {
        element.style.marginTop = "3em";
    });
    form.forEach(function(box){
        box.classList.add('formbox')
    });
    msg.forEach(function(msg){
        msg.classList.add('defaultmessage')
    });
    logo.forEach(function(lo){
        lo.classList.add('logostyle')
    });
    side.forEach(function(side){
        side.style.display = 'block';
        side.classList.add('side')
    })

});

// MAKES THE SIDEBAR COMES OUT
side.forEach(function(side){
    side.addEventListener('click', function() {
        sidebar.style.opacity = '1';
        sidebar.style.transform = 'translateX(0%)';
        isBarHidden= false;

        views.forEach(function(element) {
            element.style.marginTop = "5em";
        });
        form.forEach(function(box){
            box.classList.remove('formbox')
        });
        msg.forEach(function(msg){
            msg.classList.remove('defaultmessage')
        });
        logo.forEach(function(lo){
            lo.classList.remove('logostyle')
        });
        side.forEach(function(side){
            side.classList.remove('side')
        })
    });
    
});

const message_box = document.querySelector("#message");

const send = document.querySelector(".send-button");
const body = document.querySelector(".new-chat-view");
let usermsg;
function msgchat(e){
    e.preventDefault()
    usermsg = message_box.value.trim();
   if(!usermsg) return;
   message_box.value = '';

   body.appendChild(mgses(usermsg, "user")); 

    try{
        $.ajax({
            type: 'POST',
            url: 'initiate-chat/',
            data: {
                message: usermsg,
                chatId: chat_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function(json){
                const res = json['chats']
                setTimeout(() => {
                    body.appendChild(mgses(res, "assistant"));
                }, 600);
                console.log(json)
            },
            error: function(rs, e){
                console.log(rs.error);
            },
        });
    }
    catch{
        document.querySelectorAll(".conversation-button").forEach(button => {
            button.addEventListener("click", function() {
                const itemId =  document.querySelectorAll(".conversation-button").getAttribute('data-pk');
                $.ajax({
                    type: 'POST',
                    url: `chat-previous/${itemId}/`,
                    data: {
                        message: usermsg,
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        action: 'post'
                    },
                    success: function(response) {
                        const res = json['chats']
                        setTimeout(() => {
                            body.appendChild(mgses(res, "assistant"));
                        }, 600);
                        // Handle the successful response here
                        console.log('Success:', response);
                        // Process the received data as needed
                    },
                    error: function(xhr, status, error) {
                        // Handle any errors that occur during the request
                        console.error('Error:', status, error);
                    }
                });
                const newside = document.querySelector(".logo button");
                const logo = document.querySelector(".name");
                newside.style.display = "block";
            
                new_chat_button.addEventListener("click", function() {
                    show_view( ".new-chat-view" );
                    // body.innerHTML = `
                    //     <div class="logo text-grey">
                    //         <button id="side" class="logo-side"><i class="fa fa-chevron-right"></i></button>
                    //         <span class="name"> Medical Chat</span>
                    //     </div>
                    // `;
                    window.location.reload();
                    chat_id = getChatId();
                
                    // window.history.pushState({}, '', `?chatId=${getChatId()}`);
                
                    const newside = document.querySelector(".logo button");
                    const logo = document.querySelector(".name");
                    newside.style.display = "block";
                
                    hide_sidebar.addEventListener('click', function() {
                        sidebar.style.opacity = '0';
                        sidebar.style.transform = 'translateX(-100%)';
                        isBarHidden = true;
                
                        logo.classList.add('logostyle');
                
                    });
                
                    newside.addEventListener('click', function() {
                        sidebar.style.opacity = '1';
                        sidebar.style.transform = 'translateX(0%)';
                        isBarHidden= false;
                
                        views.forEach(function(element) {
                            element.style.marginTop = "5em";
                        });
                        form.forEach(function(box){
                            box.classList.remove('formbox')
                        });
                        msg.forEach(function(msg){
                            msg.classList.remove('defaultmessage')
                        });
                        logo.classList.remove('logostyle')
                        side.forEach(function(side){
                            side.classList.remove('side')
                        })
                    });
                });
            
            })
        });
    }

    //    scrollToBottomOfResults();


    //    scrollToBottomOfResults();
}

const mgses = (msg, className) => {
    const chat = document.createElement('div');
    chat.classList.add("pl-72","message", `${className}`);
    // msg.classList.add("pl-28", "py-[10px]", "md:pl-72", "lg:py-[10px]");
    let content = className == "assistant" ?
    `
        <div class="identity">
            <i class="user-icon">G</i>
        </div>
        <div class="content gpt">
            <p>${msg}</p>
        </div>
    ` :
    `
        <div class="identity">
            <i class="user-icon">u</i>
        </div>
        <div class="content user">
            <p>${msg}</p>
        </div>
    `;
    chat.innerHTML = content;
    return chat;
};

send.addEventListener("click", msgchat);

function show_view( view_selector ) {
    document.querySelectorAll(".view").forEach(view => {
        view.style.display = "none";
    });

    document.querySelector(view_selector).style.display = "flex";
}

new_chat_button.addEventListener("click", function() {
    show_view( ".new-chat-view" );
    // body.innerHTML = `
    //     <div class="logo text-grey">
    //         <button id="side" class="logo-side"><i class="fa fa-chevron-right"></i></button>
    //         <span class="name"> Medical Chat</span>
    //     </div>
    // `;
    window.location.reload();
    chat_id = getChatId();

    // window.history.pushState({}, '', `?chatId=${getChatId()}`);

    const newside = document.querySelector(".logo button");
    const logo = document.querySelector(".name");
    newside.style.display = "block";

    hide_sidebar.addEventListener('click', function() {
        sidebar.style.opacity = '0';
        sidebar.style.transform = 'translateX(-100%)';
        isBarHidden = true;

        logo.classList.add('logostyle');

    });

    newside.addEventListener('click', function() {
        sidebar.style.opacity = '1';
        sidebar.style.transform = 'translateX(0%)';
        isBarHidden= false;

        views.forEach(function(element) {
            element.style.marginTop = "5em";
        });
        form.forEach(function(box){
            box.classList.remove('formbox')
        });
        msg.forEach(function(msg){
            msg.classList.remove('defaultmessage')
        });
        logo.classList.remove('logostyle')
        side.forEach(function(side){
            side.classList.remove('side')
        })
    });
});


// async function index(formData) {
//     try {
//         const response = await fetch('', {
//             method: 'POST',
//             headers: {'Content-Type': 'application/json',},
//             body: formData.toString(),
//         });
//         return response.json();
//     }catch(error) {
//         console.error('Error fetching chat history:', error);
//     };
// }

function getChatId() {
    const newId = Math.floor(Math.random() * 1000);
    return newId;
}




