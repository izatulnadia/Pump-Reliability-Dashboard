// Draws the 4 graphs with Chart.js.
// Solid line = the last 72 hours, dashed line = the forecast, red line = the alarm limit.
const charts = {};          // remembers the graphs, so we only create each one once

// Create an empty graph inside the canvas called "chart_vibration", "chart_flow", ...
function makeChart(key, title) {
  return new Chart(document.getElementById("chart_" + key), {
    type: "line",
    data: {
      datasets: [
        { label: "History", borderColor: "#1d2b36" },
        { label: "Forecast", borderColor: "#d98e04", borderDash: [6, 4] },
        { label: "Alarm limit", borderColor: "#c0392b" },
      ],
    },
    options: {
      animation: false,
      maintainAspectRatio: false,
      elements: { point: { radius: 0 }, line: { borderWidth: 2 } },
      plugins: {
        title: { display: true, text: title },
        legend: { position: "bottom", labels: { boxWidth: 14, font: { size: 10 } } },
      },
      scales: { x: { ticks: { maxTicksLimit: 5 }, title: { display: true, text: "Hours from now" } } },
    },
  });
}

// Put the newest numbers into a graph
function updateChart(chart, r) {
  const past = r.history.length;        // 72 hours of history
  const future = r.forecast.length;     // 168 hours of forecast

  const labels = [];                    // the x axis: ... -2, -1, 0 (now), 1, 2 ...
  const history = [];                   // solid line
  const forecast = [];                  // dashed line
  const limit = [];                     // red line

  for (let i = 0; i < past + future; i++) {
    labels.push(i - past + 1);
    limit.push(r.limit);

    if (i < past) history.push(r.history[i]);
    else history.push(null);            // no history in the future

    if (i < past - 1) forecast.push(null);                      // no forecast in the past
    else if (i === past - 1) forecast.push(r.value);            // the dashed line starts at "now"
    else forecast.push(r.forecast[i - past]);
  }

  chart.data.labels = labels;
  chart.data.datasets[0].data = history;
  chart.data.datasets[1].data = forecast;
  chart.data.datasets[2].data = limit;
  chart.update();
}

function drawCharts(params) {
  if (typeof Chart === "undefined") return;       // Chart.js could not load (no internet)

  for (const key in params) {
    const r = params[key];
    if (!charts[key]) {
      charts[key] = makeChart(key, r.name + " (" + r.unit + ")");
    }
    updateChart(charts[key], r);
  }
}
