function revealChoices() {
  document.getElementById("choices").classList.remove("hidden");
}
function hideChoices() {
  document.getElementById("choices").classList.add("hidden");
}

function revealNumberSort() {
  document.getElementById("numberSort").classList.remove("hidden");
}
function hideNumberSort() {
  document.getElementById("numberSort").classList.add("hidden");
}

function revealButtons() {
  document.getElementById("buttons").classList.remove("hidden");
}
function hideButtons() {
  document.getElementById("buttons").classList.add("hidden");
}

function revealArtist() {
  document.getElementById("artist").classList.remove("hidden");
}
function hideArtist() {
  document.getElementById("artist").classList.add("hidden");
}

function showLoader() {
  const loader = document.getElementById("loader");
  if (loader) {
    loader.style.display = "flex";
  }
}

function hideLoginShowLogOut() {
  const loginButton = document.getElementById("loginButton");
  const logoutButton = document.getElementById("logoutButton");

  loginButton.classList.add("hidden");
  loginButton.disabled = true;

  logoutButton.classList.remove("hidden");
  logoutButton.disabled = false;
}

function showLoginHideLogOut() {
  const loginButton = document.getElementById("loginButton");
  const logoutButton = document.getElementById("logoutButton");

  loginButton.classList.remove("hidden");
  loginButton.disabled = false;

  logoutButton.classList.add("hidden");
  logoutButton.disabled = true;
}

window.onload = function () {
  const isLoggedIn = document.body.getAttribute("data-logged-in") === "true";

  if (isLoggedIn) {
    hideLoginShowLogOut();
  } else {
    showLoginHideLogOut();
  }


  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("reveal") === "true") {
    revealChoices();
    revealNumberSort();
    hideButtons();
    revealArtist();
  }
};
