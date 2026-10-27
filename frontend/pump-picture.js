// Draws the pump picture. Each part is coloured by its status:
// green = Normal, orange = Warning, red = Alarm.
const COLOURS = { Normal: "#2f7d5b", Warning: "#d98e04", Alarm: "#c0392b" };
const RANK = { Normal: 0, Warning: 1, Alarm: 2 };

// Of two statuses, give back the worse one
function worseOf(a, b) {
  if (RANK[a] >= RANK[b]) return a;
  return b;
}

// A piece of text inside the picture
function label(x, y, text) {
  return `<text x="${x}" y="${y}" text-anchor="middle" fill="#1d2b36">${text}</text>`;
}

// p = the 4 parameters (vibration, bearing_temp, discharge_pressure, flow)
function drawPump(p) {
  // Which colour does each part get?
  const bearing = COLOURS[worseOf(p.vibration.status, p.bearing_temp.status)];
  const discharge = COLOURS[p.discharge_pressure.status];
  const suction = COLOURS[p.flow.status];
  const casing = COLOURS[worseOf(p.discharge_pressure.status, p.flow.status)];

  // The picture is drawn with SVG (shapes: rect = rectangle, circle, path = lines)
  document.getElementById("pumpImage").innerHTML = `
    <svg viewBox="0 0 540 262" font-family="Arial" font-size="13">
      <rect x="20" y="170" width="500" height="14" fill="#3d5a73"/>
      <rect x="30" y="80" width="140" height="90" rx="8" fill="#6b7f90"/>
      <rect x="170" y="118" width="30" height="20" fill="#9aa9b5"/>
      <rect x="200" y="98" width="80" height="60" rx="6" fill="${bearing}"/>
      <rect x="280" y="122" width="40" height="12" fill="#9aa9b5"/>
      <rect x="335" y="30" width="30" height="45" fill="${discharge}"/>
      <rect x="335" y="30" width="185" height="24" fill="${discharge}"/>
      <rect x="410" y="116" width="110" height="24" fill="${suction}"/>
      <circle cx="350" cy="128" r="62" fill="${casing}" stroke="#1d2b36" stroke-width="3"/>
      <circle cx="350" cy="128" r="38" fill="white" fill-opacity="0.45"/>
      <path d="M350 128 V96 M350 128 L378 112 M350 128 L378 144 M350 128 V160 M350 128 L322 144 M350 128 L322 112"
            stroke="#1d2b36" stroke-width="3"/>
      ${label(100, 72, "Motor")}
      ${label(240, 72, "Bearing")}
      ${label(240, 205, "Vibration " + p.vibration.value + " " + p.vibration.unit)}
      ${label(240, 223, "Temp " + p.bearing_temp.value + " " + p.bearing_temp.unit)}
      ${label(430, 20, "Discharge " + p.discharge_pressure.value + " " + p.discharge_pressure.unit)}
      ${label(465, 108, "Flow " + p.flow.value + " " + p.flow.unit)}
      ${label(350, 252, "Casing and impeller")}
    </svg>`;
}
