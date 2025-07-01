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
  document.getElementById("loginButton").classList.add("hidden");
  document.getElementById("logoutButton").classList.remove("hidden");
}

function showLoginHideLogOut() {
  document.getElementById("loginButton").classList.remove("hidden");
  document.getElementById("logoutButton").classList.add("hidden");
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
  hideSort();
  hideDelete();
  hideTop20();
  hideTop10fromArt();
  hideTopArtist();
});
