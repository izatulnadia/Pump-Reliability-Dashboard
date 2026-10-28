// The Manage page: Create, Read, Update and Delete (CRUD) the readings of a pump.
const FIELDS = ["vibration", "bearing_temp", "discharge_pressure", "flow"];
let rows = [];                      // the readings shown in the table

// READ: show the latest 15 readings
async function showTable() {
  rows = await api("/api/readings?pump=" + currentPump());

  let html = "";
  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    html += `<tr>
      <td>${r.id}</td>
      <td>${r.time.slice(0, 16).replace("T", " ")}</td>
      <td>${r.vibration}</td><td>${r.bearing_temp}</td><td>${r.discharge_pressure}</td><td>${r.flow}</td>
      <td>
        <button onclick="editReading(${i})">Edit</button>
        <button class="delete" onclick="deleteReading(${r.id})">Delete</button>
      </td>
    </tr>`;
  }
  document.getElementById("table").innerHTML = html;
}

// CREATE: add the reading typed in the form
async function addReading(event) {
  event.preventDefault();                       // do not reload the page
  const newReading = { pump: currentPump() };
  for (const field of FIELDS) {
    newReading[field] = parseFloat(document.getElementById(field).value);
  }
  await api("/api/readings", "POST", newReading);
  event.target.reset();                         // empty the form
  showTable();
}

// UPDATE: ask for new values, then save them
async function editReading(i) {
  const newValues = {};
  for (const field of FIELDS) {
    const answer = parseFloat(prompt("New " + field, rows[i][field]));
    if (isNaN(answer)) newValues[field] = rows[i][field];     // Cancel = keep the old value
    else newValues[field] = answer;
  }
  await api("/api/readings/" + rows[i].id, "PUT", newValues);
  showTable();
}

// DELETE: remove a reading
async function deleteReading(id) {
  if (!confirm("Delete reading " + id + "?")) return;
  await api("/api/readings/" + id, "DELETE");
  showTable();
}

// api.js calls this when you choose another pump
function pumpChanged() {
  if (getPassword()) showTable();
}

// SIGN IN: check the password with the backend
async function signIn(event) {
  event.preventDefault();
  setPassword(document.getElementById("password").value);
  try {
    await api("/api/login", "POST");
    document.getElementById("password").value = "";
    signedIn();
  } catch (error) {
    document.getElementById("loginMessage").innerText = error.message;
  }
}

function signOut() {
  setPassword("");
  signedOut();
}

// Show the login box or the manage page
function signedIn() {
  document.getElementById("login").hidden = true;
  document.getElementById("manage").hidden = false;
  document.getElementById("loginMessage").innerText = "";
  showTable();
}
function signedOut() {
  document.getElementById("manage").hidden = true;
  document.getElementById("login").hidden = false;
}

loadPumpList().then(() => (getPassword() ? signedIn() : signedOut()));
