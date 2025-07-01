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

window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("reveal") === "true") {
    revealChoices();
    revealNumberSort();
    hideButtons();
    revealArtist();
  }
};
