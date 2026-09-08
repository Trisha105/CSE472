"use strict";

// Safety helper only: field validation remains native HTML validation.
// Install the handlers before enabling Submit. No storage or network calls.
const form = document.getElementById("registration-form");
const submitButton = document.getElementById("submit-demo");
const statusMessage = document.getElementById("form-status");

if (form && submitButton && statusMessage) {
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    statusMessage.textContent =
      "Validation successful. Demo only: no information was sent or saved.";
  });

  form.addEventListener("reset", function () {
    statusMessage.textContent =
      "Form reset. Use sample information to try the demonstration again.";
  });

  // Without this helper, the disabled button prevents click/Enter submission.
  submitButton.disabled = false;
}
