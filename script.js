function analyzeNews() {
  let input = document.getElementById("newsInput").value;
  let result = document.getElementById("result");

  if (input.trim() === "") {
    result.innerText = "Please enter a valid news URL or text.";
    result.style.color = "red";
    return;
  }

  result.style.color = "black";
  result.innerText = "Analyzing... ";

  setTimeout(() => {
    result.innerText = "Result: This news appears credible ";
  }, 2000);
}

function scrollToChecker() {
  document.getElementById("checker").scrollIntoView({ behavior: "smooth" });
}
