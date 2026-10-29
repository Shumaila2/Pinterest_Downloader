let currentPage = 1;

function nextPage(num) {
    document.querySelector(`#page${currentPage}`).classList.add("hidden");
    document.querySelector(`#page${num}`).classList.remove("hidden");
    currentPage = num;
}

// Asks Python to close this login window
function closeWindow() {
    window.pywebview.api.close_window();
}

async function saveCookies() {
    const csrftoken = document.getElementById("csrftoken").value.trim();
    const pinterest_sess = document.getElementById("_pinterest_sess").value.trim();
    const auth = document.getElementById("_auth").value.trim();
    const routing_id = document.getElementById("_routing_id").value.trim();

    if (!csrftoken || !pinterest_sess || !auth || !routing_id) {
        alert("Please fill all fields!");
        return;
    }

    const cookies = {
        "csrftoken": csrftoken,
        "_pinterest_sess": pinterest_sess,
        "_auth": auth,
        "_routing_id": routing_id
    };

    const result = await window.pywebview.api.save_cookies(cookies);

    if (result.status === true) {
        nextPage(3);
        // give the user a moment to read the message, then close the window
        setTimeout(closeWindow, 1500);
    }
    else {
        document.getElementById("errorMessage").textContent = result.message;
        nextPage(4);
    }
}