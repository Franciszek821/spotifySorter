function revealSort() {
  document.getElementById("textSort").classList.remove("hidden");
}
function hideSort() {
  document.getElementById("textSort").classList.add("hidden");
}

function revealDelete() {
  document.getElementById("textDelete").classList.remove("hidden");
}

function hideDelete() {
  document.getElementById("textDelete").classList.add("hidden");
}

function revealTop20() {
  document.getElementById("textTop20").classList.remove("hidden");
}

function hideTop20() {
  document.getElementById("textTop20").classList.add("hidden");
}

function revealTop10fromArt() {
  document.getElementById("textTop10fromArt").classList.remove("hidden");
}

function hideTop10fromArt() {
  document.getElementById("textTop10fromArt").classList.add("hidden");
}

function revealTopArtist() {
  document.getElementById("textTopArtist").classList.remove("hidden");
}

function hideTopArtist() {
  document.getElementById("textTopArtist").classList.add("hidden");
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
    revealSort();
    revealDelete();
    revealTop20();
    revealTop10fromArt();
    revealTopArtist();
  }
};

document.addEventListener("DOMContentLoaded", function () {
  revealSort();
  hideDelete();
  hideTop20();
  hideTop10fromArt();
  hideTopArtist();
});
