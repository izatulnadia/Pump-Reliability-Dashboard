// The dashboard page: asks the backend for the analysis, then draws everything.

// Get the analysis of the chosen pump and draw it
async function refresh(addNewReading) {
  if (addNewReading) {
    await api("/api/simulate/" + currentPump(), "POST");     // live update: add a new reading
  }

  const data = await api("/api/analysis/" + currentPump());

  if (data.detail) {                                          // the backend sent an error message
    document.getElementById("cards").innerHTML = "<p>" + data.detail + "</p>";
    return;
  }

  document.getElementById("title").innerText = data.pump + " - " + data.service;
  document.getElementById("updated").innerText = "Last update: " + new Date().toLocaleTimeString();

  drawIndicators(data.summary);       // panels.js
  drawPump(data.parameters);          // pump-picture.js
  drawCards(data.parameters);         // panels.js
  drawCharts(data.parameters);        // charts.js
  drawInsight(data.insights);         // panels.js
  drawRca(data.rca);                  // panels.js
}

// The "Ask AI" button
async function askAI() {
  const box = document.getElementById("insight");
  box.innerText = "Asking AI...";
  try {
    const response = await fetch(API_BASE + "/api/insight/" + currentPump(), {
      signal: AbortSignal.timeout(50000),
    });
    const responseBody = await response.text();
    let answer;
    try {
      answer = JSON.parse(responseBody);
    } catch {
      throw new Error(responseBody || `Request failed (${response.status})`);
    }
    if (!response.ok) {
      throw new Error(answer.detail || `Request failed (${response.status})`);
    }
    box.innerText = answer.text || "The server returned an empty AI response.";
  } catch (error) {
    box.innerText = error.name === "TimeoutError"
      ? "AI request timed out. Check your connection and try again."
      : `AI request failed: ${error.message}`;
    console.error("AI insight request failed:", error);
  }
}

// api.js calls this when you choose another pump in the drop-down
function pumpChanged() {
  document.getElementById("insight").innerText = "Click the button to get the AI insight.";
  refresh(false);
}

// Start: fill the pump list, draw the dashboard, then update every 5 seconds
async function start() {
  await loadPumpList();
  await refresh(false);
  setInterval(function () {
    refresh(document.getElementById("live").checked);
  }, 5000);
}
start();
