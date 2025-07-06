function activateTab(button, textId) {
  const allTextIds = [
    "textSort",
    "textDelete",
    "textTop20",
    "textTop10fromArt",
    "textTopArtist"
  ];

  // Hide all text sections
  allTextIds.forEach(id => {
    document.getElementById(id).classList.add("hidden");
  });

  // Show selected one
  document.getElementById(textId).classList.remove("hidden");

  // Handle active button styling
  const buttons = document.querySelectorAll(".button-group button");
  buttons.forEach(btn => btn.classList.remove("active"));
  button.classList.add("active");
}

// Login/Logout UI toggling
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
  isLoggedIn ? hideLoginShowLogOut() : showLoginHideLogOut();

  // Show all text sections if URL includes ?reveal=true
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("reveal") === "true") {
    ["textSort", "textDelete", "textTop20", "textTop10fromArt", "textTopArtist"].forEach(id => {
      document.getElementById(id).classList.remove("hidden");
    });
  } else {
    // Default state: show only Sort section
    activateTab(document.querySelector(".button-group button"), "textSort");
  }
};
