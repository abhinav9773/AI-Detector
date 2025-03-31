async function analyzeNews() {
  let input = document.getElementById("newsInput").value;
  let result = document.getElementById("result");

  if (input.trim() === "") {
    result.innerText = "Please enter a valid news URL or text.";
    result.style.color = "red";
    return;
  }

  result.style.color = "black";
  result.innerText = "Analyzing... ";

  try {
    // Send a request to the backend API
    let response = await fetch("http://localhost:5000/api/news/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input }), // Sending user input to backend
    });

    let data = await response.json(); // Get response from backend

    if (data.success) {
      result.innerText = `Result: ${data.message}`; // Show result
    } else {
      result.innerText = "Error: Unable to analyze the news.";
    }
  } catch (error) {
    result.innerText = "Error: Server is unreachable.";
  }
}

function scrollToChecker() {
  document.getElementById("checker").scrollIntoView({ behavior: "smooth" });
}
