from __future__ import annotations

import json
from pathlib import Path


def write_dashboard(
    path: Path,
    *,
    summary_rows: list[dict],
    category_rows: list[dict],
    recommendation_rows: list[dict],
    result_rows: list[dict],
    run_id: str,
) -> None:
    payload = {
        "runId": run_id,
        "summary": summary_rows,
        "categories": category_rows,
        "recommendations": recommendation_rows,
        "results": compact_result_rows(result_rows),
    }
    html = DASHBOARD_TEMPLATE.replace("__RAG_BENCHMARK_DATA__", json.dumps(payload, ensure_ascii=False))
    path.write_text(html, encoding="utf-8")


def compact_result_rows(rows: list[dict]) -> list[dict]:
    fields = [
        "track",
        "domain",
        "question_id",
        "rag_method",
        "system_id",
        "embedding_model",
        "generator_model",
        "answer_correctness",
        "evidence_recall",
        "context_precision",
        "failure_type",
    ]
    return [{field: row.get(field) for field in fields} for row in rows]


DASHBOARD_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>RAG Benchmark Dashboard</title>
  <style>
    :root {
      --paper: #f4f1ea;
      --surface: #fffcf4;
      --ink: #20231f;
      --muted: #6b7068;
      --line: #d8d2c4;
      --green: #0f766e;
      --rust: #b4532a;
      --gold: #b38600;
      --steel: #415a6b;
      --bad: #a23535;
      --shadow: 0 16px 32px rgba(32, 35, 31, 0.08);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "IBM Plex Sans", "Aptos", "Segoe UI", sans-serif;
    }

    header {
      border-bottom: 1px solid var(--line);
      background: var(--surface);
    }

    .wrap {
      width: min(1480px, calc(100vw - 32px));
      margin: 0 auto;
    }

    .topbar {
      min-height: 112px;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 24px;
      align-items: center;
    }

    h1 {
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(30px, 4vw, 58px);
      font-weight: 700;
      letter-spacing: 0;
      line-height: 0.95;
    }

    .run-id {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      font-variant-numeric: tabular-nums;
    }

    .filters {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: flex-end;
    }

    label {
      display: grid;
      gap: 4px;
      font-size: 11px;
      text-transform: uppercase;
      color: var(--muted);
      letter-spacing: .08em;
    }

    select {
      min-width: 172px;
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fffaf0;
      color: var(--ink);
      padding: 0 10px;
      font: inherit;
    }

    main {
      padding: 22px 0 40px;
    }

    .kpis {
      display: grid;
      grid-template-columns: repeat(5, minmax(150px, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }

    .panel, .kpi {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }

    .kpi {
      padding: 14px 16px;
      min-height: 86px;
    }

    .kpi .label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
    }

    .kpi .value {
      margin-top: 8px;
      font-size: 30px;
      font-weight: 750;
      font-variant-numeric: tabular-nums;
    }

    .grid {
      display: grid;
      grid-template-columns: 1.18fr .82fr;
      gap: 14px;
      align-items: start;
    }

    .panel {
      min-height: 360px;
      padding: 16px;
      overflow: hidden;
    }

    .wide { grid-column: 1 / -1; }

    .panel-title {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
      margin-bottom: 12px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 10px;
    }

    h2 {
      margin: 0;
      font-size: 16px;
      letter-spacing: 0;
    }

    .sub {
      color: var(--muted);
      font-size: 12px;
      font-variant-numeric: tabular-nums;
    }

    svg {
      width: 100%;
      display: block;
    }

    .axis, .tick {
      stroke: #bcb4a5;
      stroke-width: 1;
    }

    .chart-label {
      fill: var(--muted);
      font-size: 11px;
      font-family: "IBM Plex Sans", "Aptos", "Segoe UI", sans-serif;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    th {
      text-align: left;
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: .06em;
      border-bottom: 1px solid var(--line);
      padding: 8px 6px;
    }

    td {
      border-bottom: 1px solid #ebe4d5;
      padding: 9px 6px;
      vertical-align: top;
    }

    .num {
      text-align: right;
      font-variant-numeric: tabular-nums;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      min-height: 22px;
      padding: 2px 7px;
      border-radius: 999px;
      background: #eee6d6;
      color: #343832;
      font-size: 12px;
      white-space: nowrap;
    }

    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 8px 12px;
      margin-top: 10px;
      color: var(--muted);
      font-size: 12px;
    }

    .legend span::before {
      content: "";
      width: 9px;
      height: 9px;
      display: inline-block;
      margin-right: 6px;
      background: var(--c);
      border-radius: 2px;
    }

    @media (max-width: 1040px) {
      .topbar, .grid { grid-template-columns: 1fr; }
      .filters { justify-content: flex-start; }
      .kpis { grid-template-columns: repeat(2, minmax(150px, 1fr)); }
    }

    @media (max-width: 620px) {
      .wrap { width: min(100vw - 20px, 1480px); }
      .kpis { grid-template-columns: 1fr; }
      select { min-width: min(100%, 320px); }
      .panel { padding: 12px; }
    }
  </style>
</head>
<body>
  <header>
    <div class="wrap topbar">
      <div>
        <h1>RAG Benchmark Dashboard</h1>
        <div class="run-id" id="runId"></div>
      </div>
      <div class="filters">
        <label>Track<select id="trackFilter"></select></label>
        <label>Domain<select id="domainFilter"></select></label>
        <label>Metric<select id="metricFilter"></select></label>
      </div>
    </div>
  </header>

  <main class="wrap">
    <section class="kpis" id="kpis"></section>
    <section class="grid">
      <div class="panel">
        <div class="panel-title"><h2>Quality Ranking</h2><span class="sub" id="rankingCount"></span></div>
        <div id="barChart"></div>
      </div>
      <div class="panel">
        <div class="panel-title"><h2>Recall vs Answer</h2><span class="sub">each point is one stack</span></div>
        <div id="scatterChart"></div>
        <div class="legend" id="legend"></div>
      </div>
      <div class="panel">
        <div class="panel-title"><h2>Question Quality Distribution</h2><span class="sub" id="histCount"></span></div>
        <div id="histChart"></div>
      </div>
      <div class="panel">
        <div class="panel-title"><h2>Category Heatmap</h2><span class="sub">answer score</span></div>
        <div id="heatmap"></div>
      </div>
      <div class="panel wide">
        <div class="panel-title"><h2>Top Operating Choices</h2><span class="sub">quality, efficiency, stability</span></div>
        <div id="table"></div>
      </div>
    </section>
  </main>

  <script id="payload" type="application/json">__RAG_BENCHMARK_DATA__</script>
  <script>
    const data = JSON.parse(document.getElementById("payload").textContent);
    const colors = ["#0f766e", "#b4532a", "#415a6b", "#b38600", "#6b5d7a", "#7a6237"];
    const metrics = [
      ["answer_correctness", "Answer"],
      ["evidence_recall", "Evidence"],
      ["context_precision", "Precision"],
      ["citation_validity", "Citation"],
      ["failure_rate", "Failure"]
    ];

    const fmt = value => Number(value || 0).toFixed(3);
    const pct = value => `${Math.round(Number(value || 0) * 100)}%`;
    const uniq = rows => [...new Set(rows)].sort();
    const byId = id => document.getElementById(id);

    function init() {
      byId("runId").textContent = `run ${data.runId}`;
      fillSelect("trackFilter", ["all", ...uniq(data.summary.map(row => row.track))], "end-to-end");
      fillSelect("domainFilter", ["all", ...uniq(data.summary.map(row => row.domain))], "all");
      fillSelect("metricFilter", metrics.map(item => item[0]), "answer_correctness", key => {
        const found = metrics.find(item => item[0] === key);
        return found ? found[1] : key;
      });
      ["trackFilter", "domainFilter", "metricFilter"].forEach(id => {
        byId(id).addEventListener("change", render);
      });
      render();
    }

    function fillSelect(id, values, selected, labeler = value => value) {
      byId(id).innerHTML = values.map(value => {
        const attr = value === selected ? " selected" : "";
        return `<option value="${escapeHtml(value)}"${attr}>${escapeHtml(labeler(value))}</option>`;
      }).join("");
    }

    function selectedRows(rows) {
      const track = byId("trackFilter").value;
      const domain = byId("domainFilter").value;
      return rows.filter(row => (track === "all" || row.track === track) && (domain === "all" || row.domain === domain));
    }

    function render() {
      const summary = selectedRows(data.summary);
      const categories = selectedRows(data.categories);
      const results = selectedRows(data.results);
      const recommendations = selectedRows(data.recommendations);
      renderKpis(summary, results);
      renderBar(summary);
      renderScatter(summary);
      renderHistogram(results);
      renderHeatmap(categories);
      renderTable(recommendations.length ? recommendations : summary);
    }

    function renderKpis(summary, results) {
      const best = maxOf(summary, "answer_correctness");
      const avgAnswer = average(summary, "answer_correctness");
      const avgEvidence = average(summary, "evidence_recall");
      const avgFailure = average(summary, "failure_rate");
      const questions = uniq(results.map(row => `${row.domain}:${row.question_id}`)).length;
      const items = [
        ["Best answer", pct(best)],
        ["Avg answer", pct(avgAnswer)],
        ["Avg evidence", pct(avgEvidence)],
        ["Avg failure", pct(avgFailure)],
        ["Questions", String(questions)]
      ];
      byId("kpis").innerHTML = items.map(([label, value]) => `
        <div class="kpi"><div class="label">${label}</div><div class="value">${value}</div></div>
      `).join("");
    }

    function renderBar(rows) {
      const metric = byId("metricFilter").value;
      const ranked = [...rows].sort((a, b) => Number(b[metric]) - Number(a[metric])).slice(0, 14);
      byId("rankingCount").textContent = `${ranked.length} shown`;
      const width = 860, height = Math.max(300, ranked.length * 30 + 36);
      const left = 230, right = 34, top = 14;
      const max = Math.max(1, ...ranked.map(row => Number(row[metric] || 0)));
      const bars = ranked.map((row, index) => {
        const y = top + index * 30;
        const value = Number(row[metric] || 0);
        const w = (width - left - right) * value / max;
        const label = variantLabel(row);
        return `
          <text class="chart-label" x="0" y="${y + 17}">${escapeSvg(trimLabel(label, 36))}</text>
          <rect x="${left}" y="${y}" width="${w}" height="20" rx="4" fill="${colorFor(row.rag_method)}"></rect>
          <text class="chart-label" x="${left + w + 8}" y="${y + 15}">${fmt(value)}</text>
        `;
      }).join("");
      byId("barChart").innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img">${bars}</svg>`;
    }

    function renderScatter(rows) {
      const width = 560, height = 330, pad = 44;
      const points = rows.map(row => {
        const x = pad + Number(row.evidence_recall || 0) * (width - pad * 2);
        const y = height - pad - Number(row.answer_correctness || 0) * (height - pad * 2);
        return `<circle cx="${x}" cy="${y}" r="5.5" fill="${colorFor(row.rag_method)}" opacity="0.82">
          <title>${escapeHtml(variantLabel(row))}</title>
        </circle>`;
      }).join("");
      byId("scatterChart").innerHTML = `
        <svg viewBox="0 0 ${width} ${height}" role="img">
          <line class="axis" x1="${pad}" y1="${height - pad}" x2="${width - pad}" y2="${height - pad}"></line>
          <line class="axis" x1="${pad}" y1="${pad}" x2="${pad}" y2="${height - pad}"></line>
          <text class="chart-label" x="${width - 105}" y="${height - 10}">Evidence recall</text>
          <text class="chart-label" x="8" y="24">Answer</text>
          ${points}
        </svg>`;
      const methods = uniq(rows.map(row => row.rag_method));
      byId("legend").innerHTML = methods.map(method => `<span style="--c:${colorFor(method)}">${escapeHtml(method)}</span>`).join("");
    }

    function renderHistogram(rows) {
      const values = rows.map(row => (Number(row.answer_correctness || 0) + Number(row.evidence_recall || 0)) / 2);
      const bins = Array.from({ length: 10 }, () => 0);
      values.forEach(value => {
        const index = Math.min(9, Math.max(0, Math.floor(value * 10)));
        bins[index] += 1;
      });
      byId("histCount").textContent = `${values.length} question runs`;
      const width = 560, height = 300, pad = 36;
      const max = Math.max(1, ...bins);
      const barWidth = (width - pad * 2) / bins.length - 6;
      const bars = bins.map((count, index) => {
        const x = pad + index * ((width - pad * 2) / bins.length);
        const h = (height - pad * 2) * count / max;
        const y = height - pad - h;
        return `
          <rect x="${x}" y="${y}" width="${barWidth}" height="${h}" rx="3" fill="#b4532a"></rect>
          <text class="chart-label" x="${x + 2}" y="${height - 12}">${index / 10}</text>
        `;
      }).join("");
      byId("histChart").innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img">${bars}</svg>`;
    }

    function renderHeatmap(rows) {
      const categories = uniq(rows.map(row => row.category));
      const methods = uniq(rows.map(row => row.rag_method || row.system_id));
      const cellW = 118, cellH = 30;
      const left = 160, top = 34;
      const width = left + methods.length * cellW + 18;
      const height = top + categories.length * cellH + 28;
      const cells = [];
      methods.forEach((method, xIndex) => {
        cells.push(`<text class="chart-label" x="${left + xIndex * cellW + 4}" y="18">${escapeSvg(trimLabel(method, 14))}</text>`);
      });
      categories.forEach((category, yIndex) => {
        cells.push(`<text class="chart-label" x="0" y="${top + yIndex * cellH + 19}">${escapeSvg(trimLabel(category, 22))}</text>`);
        methods.forEach((method, xIndex) => {
          const matches = rows.filter(row => (row.rag_method || row.system_id) === method && row.category === category);
          const value = matches.length ? average(matches, "answer_correctness") : 0;
          const fill = heatColor(value);
          const x = left + xIndex * cellW;
          const y = top + yIndex * cellH;
          cells.push(`<rect x="${x}" y="${y}" width="${cellW - 5}" height="${cellH - 5}" rx="4" fill="${fill}"></rect>`);
          cells.push(`<text class="chart-label" x="${x + 8}" y="${y + 17}" fill="#20231f">${fmt(value)}</text>`);
        });
      });
      byId("heatmap").innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img">${cells.join("")}</svg>`;
    }

    function renderTable(rows) {
      const ranked = [...rows].sort((a, b) => {
        const left = Number(b.recommendation_score ?? b.answer_correctness ?? 0);
        const right = Number(a.recommendation_score ?? a.answer_correctness ?? 0);
        return left - right;
      }).slice(0, 16);
      byId("table").innerHTML = `
        <table>
          <thead><tr>
            <th>Domain</th><th>RAG</th><th>Embedding</th><th>Generator</th>
            <th class="num">Answer</th><th class="num">Evidence</th><th class="num">Failure</th><th class="num">Score</th>
          </tr></thead>
          <tbody>
            ${ranked.map(row => `
              <tr>
                <td>${escapeHtml(row.domain || "")}</td>
                <td><span class="pill">${escapeHtml(row.rag_method || row.system_id || "")}</span></td>
                <td>${escapeHtml(row.embedding_model || "none")}</td>
                <td>${escapeHtml(row.generator_model || "")}</td>
                <td class="num">${fmt(row.answer_correctness)}</td>
                <td class="num">${fmt(row.evidence_recall)}</td>
                <td class="num">${fmt(row.failure_rate)}</td>
                <td class="num">${fmt(row.recommendation_score ?? row.answer_correctness)}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>`;
    }

    function variantLabel(row) {
      return `${row.rag_method || row.system_id} / ${row.embedding_model || "none"} / ${row.generator_model || ""}`;
    }

    function colorFor(key) {
      const keys = uniq(data.summary.map(row => row.rag_method || row.system_id));
      const index = Math.max(0, keys.indexOf(key || ""));
      return colors[index % colors.length];
    }

    function heatColor(value) {
      const v = Math.max(0, Math.min(1, Number(value || 0)));
      if (v >= 0.85) return "#87b5a9";
      if (v >= 0.65) return "#c8bd75";
      if (v >= 0.45) return "#d7a06f";
      return "#d4867e";
    }

    function average(rows, key) {
      if (!rows.length) return 0;
      return rows.reduce((sum, row) => sum + Number(row[key] || 0), 0) / rows.length;
    }

    function maxOf(rows, key) {
      if (!rows.length) return 0;
      return Math.max(...rows.map(row => Number(row[key] || 0)));
    }

    function trimLabel(value, length) {
      return value.length > length ? `${value.slice(0, length - 1)}...` : value;
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
      }[char]));
    }

    function escapeSvg(value) {
      return escapeHtml(value);
    }

    init();
  </script>
</body>
</html>
"""
