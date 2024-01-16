const sidebar = document.querySelector("#logo-sidebar");
const msg = document.querySelectorAll(".message");
const logo = document.querySelectorAll(".name");
const side = document.querySelectorAll(".logo-side");
const form = document.querySelectorAll("#message-form");
const hide_sidebar = document.querySelector(".hide-sidebar");
const views = document.querySelectorAll(".view");
const typing = document.querySelectorAll(".bottyping")
let isBarHidden = false
let chat_id = getChatId()
let botloading;
let itemId;

function scrollToBottomOfResults() {
    const terminalResultsDiv = document.querySelector(".new-chat-view");
    terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
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
    typing.forEach(function(typin){
        typin.classList.add('slidemessage')
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
        typing.forEach(function(typin){
            typin.classList.remove('slidemessage')
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

function disableButton(){
    send.setAttribute("disabled", "");
}
function renableButton(){
    send.removeAttribute("disabled");
}

const body = document.querySelector(".new-chat-view");
let usermsg;
function msgchat(e){
    e.preventDefault()
    usermsg = message_box.value.trim();
   if(!usermsg) return;
   message_box.value = '';

   body.appendChild(mgses(usermsg, "user"));
    setTimeout(() => {        
        scrollToBottomOfResults();

        body.appendChild(botIsTyping("bot"));

        scrollToBottomOfResults();
        disableButton();
    }, 1000);
    

    if(!chat_id){
        url = ''
    }else{
        url = 'initiate-chat/'
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            message: usermsg,
            chatId: chat_id,
            // itemId: item_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: function(json){
            const res = json['chats']
            setTimeout(() => {
                hideTyping();
                body.appendChild(mgses(res, "assistant"));
                scrollToBottomOfResults();
                renableButton();
            }, 1000);
            console.log(json)
        },
        error: function(rs, e){
            setTimeout(() => {
                hideTyping();
                body.appendChild(setBotResponse("bot"));
                scrollToBottomOfResults();
                disableButton();
            }, 600);
            console.log(rs.error);
        },
    });
}

const mgses = (msg, className) => {
    const chat = document.createElement('div');
    chat.classList.add("pl-72","message", `${className}`);
    // msg.classList.add("pl-28", "py-[10px]", "md:pl-72", "lg:py-[10px]");
    let content = className == "assistant" ?
    `
        <div class="identity">
            <i class="user-icon">Asst</i>
        </div>
        <div class="content gpt">
            <p>${msg}</p>
        </div>
    ` :
    `
        <div class="identity">
            <i class="user-icon">You</i>
        </div>
        <div class="content user">
            <p>${msg}</p>
        </div>
    `;
    chat.innerHTML = content;
    return chat;
};

function botIsTyping(className){
    const chat = document.createElement('div');
    chat.classList.add("pl-72","bottyping", `${className}`);
    // msg.classList.add("pl-28", "py-[10px]", "md:pl-72", "lg:py-[10px]");
    let botloading = className == "bot" ?
    `
        <div class="identity">
            <i class="gpt user-icon">Asst</i>
        </div>
        <div class='flex space-x-2 justify-left items-left bg-transparent dark:invert'>
            <span class='sr-only'>Loading...</span>
            <div class='h-3 w-3 bg-[#0f162bc9] rounded-full animate-bounce [animation-delay:-0.3s]'></div>
            <div class='h-3 w-3 bg-[#0f162bc9] rounded-full animate-bounce [animation-delay:-0.15s]'></div>
            <div class='h-3 w-3 bg-[#0f162bc9] rounded-full animate-bounce'></div>
        </div>

    `:
    `
    `;
    chat.innerHTML = botloading;
    return chat;
}

function hideTyping(){
    document.querySelector(".bottyping").remove();
}

function setBotResponse(className){
    const chat = document.createElement('div');
    chat.classList.add("pl-72","bottyping", `${className}`);
    // msg.classList.add("pl-28", "py-[10px]", "md:pl-72", "lg:py-[10px]");
    let botloading = className == "bot" ?
    `
        <div class="identity">
            <i class="gpt user-icon">Asst</i>
        </div>
        <div class="content gpt">
            <p>
                Not available right now. Please, do try again later or try reloading the page to start again.
            </p>
        </div>

    `:
    `
    `;
    chat.innerHTML = botloading;
    return chat;
}

send.addEventListener("click", msgchat);

function show_view( view_selector ) {
    document.querySelectorAll(".view").forEach(view => {
        view.style.display = "none";
    });

    document.querySelector(view_selector).style.display = "flex";
}

function getChatId() {
    const newId = Math.floor(Math.random() * 1000);
    return newId;
}






