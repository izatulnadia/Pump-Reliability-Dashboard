// Draws the text parts of the dashboard: indicator tiles, parameter cards,
// the insight sentences and the root cause analysis.

// ----- Indicator tiles (next to the pump picture) -----
function drawIndicators(s) {
  const tiles = [
    ["Health score", s.health + " / 100"],
    ["Overall status", s.status],
    ["First alarm in", s.first_alarm ? s.first_alarm + " hours" : "None in 14 days"],
    ["Needs attention", s.attention + " of 4 parameters"],
    ["Most critical", s.critical],
    ["Last reading", s.last_time],
  ];

  let html = "";
  for (const tile of tiles) {
    html += `<div class="box tile ${s.status.toLowerCase()}">
               <small>${tile[0]}</small><b>${tile[1]}</b>
             </div>`;
  }
  document.getElementById("indicators").innerHTML = html;
}

// ----- One card for each parameter -----
function drawCards(params) {
  let html = "";
  for (const key in params) {
    const r = params[key];

    let forecastText = "No alarm within 14 days";
    if (r.hours) {
      forecastText = `Alarm in about ${r.hours} hours (${(r.hours / 24).toFixed(1)} days)`;
    }

    html += `<div class="box ${r.status.toLowerCase()}">
      <b>${r.name}</b>
      <div class="big">${r.value} <small>${r.unit}</small></div>
      <div class="track"><div class="fill" style="width:${r.percent}%"></div></div>
      <div class="ends"><span>Normal ${r.normal}</span><span>Alarm ${r.limit}</span></div>
      <p>Forecast: ${forecastText}</p>
      <b>${r.status}</b>
    </div>`;
  }
  document.getElementById("cards").innerHTML = html;
}

// ----- Insight: a few sentences about the data -----
function drawInsight(notes) {
  let html = "";
  for (const note of notes) {
    html += `<li>${note}</li>`;
  }
  document.getElementById("insightList").innerHTML = html;
}

// Turn a list of texts into an HTML bullet list
function bulletList(items) {
  let html = "<ul>";
  for (const item of items) {
    html += `<li>${item}</li>`;
  }
  return html + "</ul>";
}

// ----- Root cause analysis -----
function drawRca(causes) {
  const box = document.getElementById("rca");

  if (causes.length === 0) {
    box.innerHTML = "<h3>No known fault pattern found</h3><p>Keep monitoring.</p>";
    return;
  }

  const top = causes[0];                         // the best match

  let others = "";                               // the other possible causes
  for (const c of causes.slice(1)) {
    others += `<span class="chip">Also possible: ${c.name} (${c.score}%)</span>`;
  }

  let chain = "<ol>";                            // the "why" chain
  for (const step of top.chain) {
    chain += `<li>${step}</li>`;
  }
  chain += "</ol>";

  box.innerHTML = `
    <div class="cause-head">
      <b>Most likely: ${top.name}</b>
      <span class="chip">${top.score}% match, ${top.confidence} confidence</span>
      ${others}
    </div>
    <div class="cols">
      <div><h4>Evidence</h4>${bulletList(top.evidence)}</div>
      <div><h4>Why is it happening?</h4>${chain}</div>
      <div><h4>Check on site</h4>${bulletList(top.checks)}</div>
      <div><h4>Corrective action</h4>${bulletList(top.actions)}
        <h4 style="margin-top:14px">How to prevent it</h4><p>${top.prevent}</p></div>
    </div>`;
}
