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


}