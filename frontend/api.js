// Used by BOTH pages: talks to the backend and fills the pump drop-down.

// Send a request to the backend and get the answer back.
//   url    = the address, for example "/api/pumps"
//   method = GET (read), POST (create), PUT (update) or DELETE
//   body   = the data to send (only for POST and PUT)
async function api(url, method = "GET", body = null) {
  const response = await fetch(url, {
    method: method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : null,
  });
  return response.json();
}

// Fill the pump drop-down. The chosen pump is remembered, even on the other page.
async function loadPumpList() {
  const pumps = await api("/api/pumps");
  const dropdown = document.getElementById("pump");

  let html = "";
  for (const p of pumps) {
    html += `<option value="${p.name}">${p.name} - ${p.service}</option>`;
  }
  dropdown.innerHTML = html;
  dropdown.value = localStorage.getItem("pump") || pumps[0].name;

  dropdown.onchange = function () {
    localStorage.setItem("pump", dropdown.value);
    pumpChanged();                  // each page has its own pumpChanged() function
  };
}

// The pump that is selected right now, for example "P-101"
function currentPump() {
  return document.getElementById("pump").value;
}
