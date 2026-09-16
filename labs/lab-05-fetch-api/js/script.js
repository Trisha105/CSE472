// Earlier JavaScript interactions retained from Lab 03.
let availableSeats = 12;

function checkRegistration() {
  let message = document.getElementById("registrationStatus");
  message.textContent = "Registration is currently open.";
}

function checkSeats() {
  let message = document.getElementById("seatMessage");
  if (availableSeats > 0) {
    message.textContent = "Seats are available. Remaining seats: " + availableSeats;
  } else {
    message.textContent = "Sorry, no seats are available.";
  }
}

function showGreeting() {
  let name = document.getElementById("studentName").value;
  let output = document.getElementById("greetingMessage");
  output.textContent = "Welcome, " + name + "!";
}

function showWorkshopReminder() {
  let message = document.getElementById("workshopReminder");
  message.textContent = "Reminder: bring your student ID to the workshop.";
}

// Lab 05: request workshop information from a local JSON file.
async function loadWorkshop() {
  document.getElementById("loadMessage").textContent =
    "Please wait. Loading workshop information...";

  const response = await fetch("data/workshop.json");

  if (response.status === 200) {
    const workshop = await response.json();
    document.getElementById("workshopTitle").textContent = workshop.title;
    document.getElementById("workshopDate").textContent = workshop.date;
    document.getElementById("workshopVenue").textContent = workshop.venue;
    document.getElementById("workshopSeats").textContent = workshop.seats;
    document.getElementById("workshopInstructor").textContent = workshop.instructor;
    document.getElementById("workshopDuration").textContent = workshop.duration;
    document.getElementById("loadMessage").textContent =
      "Workshop data loaded successfully.";
  } else {
    document.getElementById("loadMessage").textContent =
      "Could not load workshop data.";
  }
}

// Lab 05: request one sample user from the JSONPlaceholder practice API.
async function loadSampleUser() {
  const response = await fetch(
    "https://jsonplaceholder.typicode.com/users/1"
  );

  if (response.status === 200) {
    const user = await response.json();
    document.getElementById("apiUser").textContent =
      user.name + " - " + user.email;
  } else {
    document.getElementById("apiUser").textContent =
      "Could not load API data.";
  }
}
