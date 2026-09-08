// Store the seat count used by the availability checker.
let availableSeats = 12;

function checkRegistration() {
  let message = document.getElementById("registrationStatus");
  message.textContent = "Registration is currently open.";
}

function checkSeats() {
  let message = document.getElementById("seatMessage");
  if (availableSeats > 0) {
    message.textContent =
      "Seats are available. Remaining seats: " + availableSeats;
  } else {
    message.textContent = "Sorry, no seats are available.";
  }
}

function showGreeting() {
  let name = document.getElementById("studentName").value;
  let output = document.getElementById("greetingMessage");
  output.textContent = "Welcome, " + name + "!";
}

// This extra button updates only the reminder paragraph.
function showWorkshopReminder() {
  let message = document.getElementById("workshopReminder");
  message.textContent =
    "Reminder: bring your student ID to the workshop.";
}
