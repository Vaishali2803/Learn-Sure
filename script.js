function submitForm() {
  const data = {
    domain: document.getElementById("domain").value,
    fee: document.getElementById("fee").value,
    duration: document.getElementById("duration").value,
    level: document.getElementById("level").value,
    demand: document.getElementById("demand").value
  };

  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {

    if (result.error) {
      document.getElementById("error").innerText = result.error;
      return;
    }

    document.getElementById("finalScore").innerText =
      "Final Score: " + result.score + "%";

    document.getElementById("status").innerText =
      "Status: " + result.status;

  })
  .catch(error => {
    document.getElementById("error").innerText =
      "Server error. Please try again.";
  });
}
