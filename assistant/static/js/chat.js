const sidebar = document.querySelector("#logo-sidebar");
const msg = document.querySelectorAll(".message");
const logo = document.querySelectorAll(".name");
const side = document.querySelectorAll(".logo-side");
const form = document.querySelectorAll("#message-form");
const hide_sidebar = document.querySelector(".hide-sidebar");
const views = document.querySelectorAll(".view");
const typing = document.querySelectorAll(".bottyping");
let isBarHidden = false;
let chat_id = getChatId();

function scrollToBottomOfResults() {
    const terminalResultsDiv = document.querySelector(".new-chat-view");
    if (terminalResultsDiv) {
        terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
    }
}

if (hide_sidebar && sidebar) {
    hide_sidebar.addEventListener("click", function () {
        sidebar.style.opacity = "0";
        sidebar.style.transform = "translateX(-100%)";
        isBarHidden = true;

        views.forEach(function (element) {
            element.style.marginTop = "3em";
        });
        form.forEach(function (box) {
            box.classList.add("formbox");
        });
        msg.forEach(function (item) {
            item.classList.add("defaultmessage");
        });
        typing.forEach(function (typin) {
            typin.classList.add("slidemessage");
        });
        logo.forEach(function (lo) {
            lo.classList.add("logostyle");
        });
        side.forEach(function (el) {
            el.style.display = "block";
            el.classList.add("side");
        });
    });
}

side.forEach(function (sideBtn) {
    sideBtn.addEventListener("click", function () {
        if (!sidebar) return;
        sidebar.style.opacity = "1";
        sidebar.style.transform = "translateX(0%)";
        isBarHidden = false;

        views.forEach(function (element) {
            element.style.marginTop = "5em";
        });
        form.forEach(function (box) {
            box.classList.remove("formbox");
        });
        msg.forEach(function (item) {
            item.classList.remove("defaultmessage");
        });
        typing.forEach(function (typin) {
            typin.classList.remove("slidemessage");
        });
        logo.forEach(function (lo) {
            lo.classList.remove("logostyle");
        });
        side.forEach(function (el) {
            el.classList.remove("side");
        });
    });
});

const message_box = document.querySelector("#message");
const send = document.querySelector(".send-button");
const body = document.querySelector(".new-chat-view");

function disableButton() {
    if (send) send.setAttribute("disabled", "");
}

function renableButton() {
    if (send) send.removeAttribute("disabled");
}

function msgchat(e) {
    e.preventDefault();
    if (!message_box || !body) return;

    const usermsg = message_box.value.trim();
    if (!usermsg) return;
    message_box.value = "";

    body.appendChild(mgses(usermsg, "user"));
    setTimeout(() => {
        scrollToBottomOfResults();
        body.appendChild(botIsTyping("bot"));
        scrollToBottomOfResults();
        disableButton();
    }, 1000);

    const url = chat_id ? "initiate-chat/" : "";

    $.ajax({
        type: "POST",
        url: url,
        data: {
            message: usermsg,
            chatId: chat_id,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            action: "post",
        },
        success: function (json) {
            const res = json["chats"];
            setTimeout(() => {
                hideTyping();
                body.appendChild(mgses(res, "assistant"));
                scrollToBottomOfResults();
                renableButton();
            }, 1000);
        },
        error: function () {
            setTimeout(() => {
                hideTyping();
                body.appendChild(setBotResponse("bot"));
                scrollToBottomOfResults();
                disableButton();
            }, 600);
        },
    });
}

const mgses = (msgText, className) => {
    const chat = document.createElement("div");
    chat.classList.add("pl-72", "message", `${className}`);
    let content =
        className == "assistant"
            ? `
        <div class="identity">
            <i class="user-icon">Asst</i>
        </div>
        <div class="content gpt">
            <p>${msgText}</p>
        </div>
    `
            : `
        <div class="identity">
            <i class="user-icon">You</i>
        </div>
        <div class="content user">
            <p>${msgText}</p>
        </div>
    `;
    chat.innerHTML = content;
    return chat;
};

function botIsTyping(className) {
    const chat = document.createElement("div");
    chat.classList.add("pl-72", "bottyping", `${className}`);
    let botloading =
        className == "bot"
            ? `
        <div class="identity">
            <i class="gpt user-icon">Asst</i>
        </div>
        <div class='flex space-x-2 justify-left items-left bg-transparent dark:invert'>
            <span class='sr-only'>Loading...</span>
            <div class='h-3 w-3 bg-[#0f162bc9] rounded-full animate-bounce [animation-delay:-0.3s]'></div>
            <div class='h-3 w-3 bg-[#0f162bc9] rounded-full animate-bounce [animation-delay:-0.15s]'></div>
            <div class='h-3 w-3 bg-[#0f162bc9] rounded-full animate-bounce'></div>
        </div>
    `
            : ``;
    chat.innerHTML = botloading;
    return chat;
}

function hideTyping() {
    const typingNode = document.querySelector(".bottyping");
    if (typingNode) typingNode.remove();
}

function setBotResponse(className) {
    const chat = document.createElement("div");
    chat.classList.add("pl-72", "bottyping", `${className}`);
    let botloading =
        className == "bot"
            ? `
        <div class="identity">
            <i class="gpt user-icon">Asst</i>
        </div>
        <div class="content gpt">
            <p>
                Not available right now. Please, do try again later or try reloading the page to start again.
            </p>
        </div>
    `
            : ``;
    chat.innerHTML = botloading;
    return chat;
}

if (send) {
    send.addEventListener("click", msgchat);
}

function show_view(view_selector) {
    document.querySelectorAll(".view").forEach((view) => {
        view.style.display = "none";
    });

    const chosen = document.querySelector(view_selector);
    if (chosen) chosen.style.display = "flex";
}

function getChatId() {
    return Math.floor(Math.random() * 1000);
}
