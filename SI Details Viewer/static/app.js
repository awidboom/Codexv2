const form = document.getElementById("lookup-form");
const input = document.getElementById("unit-id");
const compareInput = document.getElementById("unit-id-compare");
const compareMode = document.getElementById("compare-mode");
const broadSearch = document.getElementById("broad-search");
const filterCriteria = document.getElementById("filter-criteria");
const filterHap = document.getElementById("filter-hap");
const filterGhg = document.getElementById("filter-ghg");
const exportCsv = document.getElementById("export-csv");
const exportPdf = document.getElementById("export-pdf");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const summaryEl = document.getElementById("summary");
const suggestionsEl = document.getElementById("unit-suggestions");

const dashboardForm = document.getElementById("dashboard-form");
const dashboardEqui = document.getElementById("dashboard-equi");
const dashboardNonzero = document.getElementById("dashboard-nonzero");
const dashboardStatus = document.getElementById("dashboard-status");
const dashboardResults = document.getElementById("dashboard-results");
const equiSuggestions = document.getElementById("equi-suggestions");
const dashboardExportXlsx = document.getElementById("dashboard-export-xlsx");

const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".tab-panel");

const CRITERIA_POLLUTANTS = [
  "nox",
  "no2",
  "nitrogen oxides",
  "so2",
  "sulfur dioxide",
  "pm",
  "pm10",
  "pm2.5",
  "particulate",
  "lead",
  "pb",
  "voc",
  "volatile organic compounds",
  "carbon monoxide",
  "co",
];

const GHG_POLLUTANTS = [
  "co2",
  "co2e",
  "carbon dioxide",
  "ch4",
  "methane",
  "n2o",
  "nitrous oxide",
  "hfc",
  "pfc",
  "sf6",
  "nf3",
];

const state = {
  lastResults: [],
  lastDashboard: null,
};

const setStatus = (message, tone = "info") => {
  statusEl.className = `status ${tone}`;
  statusEl.textContent = message;
};

const setDashboardStatus = (message, tone = "info") => {
  dashboardStatus.className = `status ${tone}`;
  dashboardStatus.textContent = message;
};

const clearResults = () => {
  resultsEl.innerHTML = "";
};

const clearSummary = () => {
  summaryEl.innerHTML = "";
};

const clearDashboardResults = () => {
  dashboardResults.innerHTML = "";
};

const normalize = (value) => String(value || "").trim().toLowerCase();

const normalizeEqui = (value) => String(value || "").replace(/\s+/g, "").toUpperCase();

const isEmptyValue = (value) => {
  if (value === null || value === undefined || value === "") {
    return true;
  }
  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase();
    return normalized === "null" || normalized === "nan";
  }
  return false;
};

const formatNumber = (value) => {
  if (value === null || value === undefined) {
    return null;
  }
  const num = typeof value === "number" ? value : Number(String(value).replace(/,/g, ""));
  if (Number.isNaN(num)) {
    return null;
  }
  const abs = Math.abs(num);
  if (abs >= 0.005) {
    return num.toFixed(2);
  }
  if (abs > 0) {
    return num.toFixed(4);
  }
  return "0.00";
};

const formatValue = (value) => {
  if (isEmptyValue(value)) {
    return "-";
  }
  const numeric = formatNumber(value);
  if (numeric !== null) {
    return numeric;
  }
  return String(value);
};

const toNumber = (value) => {
  if (value === null || value === undefined) {
    return null;
  }
  if (typeof value === "number") {
    return value;
  }
  const text = String(value).replace(/,/g, "").trim();
  if (!text) {
    return null;
  }
  const parsed = Number(text);
  return Number.isNaN(parsed) ? null : parsed;
};

const renderRowTable = (row, columns) => {
  const table = document.createElement("table");
  table.className = "detail-table";

  columns.forEach((column) => {
    const value = row[column];
    if (isEmptyValue(value)) {
      return;
    }

    const tr = document.createElement("tr");
    const th = document.createElement("th");
    const td = document.createElement("td");
    th.textContent = column;
    td.textContent = formatValue(value);
    tr.appendChild(th);
    tr.appendChild(td);
    table.appendChild(tr);
  });

  return table;
};

const getSheetData = (name) => {
  const data = window.PERMIT_DATA;
  if (!data || !data.sheets) {
    return null;
  }
  return data.sheets.find((sheet) => sheet.sheet === name) || null;
};

const buildSuggestions = () => {
  if (!window.PERMIT_DATA || !window.PERMIT_DATA.sheets) {
    return;
  }
  const set = new Set();
  window.PERMIT_DATA.sheets.forEach((group) => {
    group.rows.forEach((row) => {
      ["Subject Item ID", "Subject Item Designation", "Subject Item Description"].forEach(
        (key) => {
          const value = row[key];
          if (value && String(value).trim().length > 0) {
            set.add(String(value).trim());
          }
        }
      );
    });
  });

  const sorted = Array.from(set).sort((a, b) => a.localeCompare(b));
  suggestionsEl.innerHTML = "";
  sorted.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    suggestionsEl.appendChild(option);
  });
};

const buildEquiSuggestions = () => {
  if (!window.BASELINE_PTE || !window.BASELINE_PTE.segments) {
    return;
  }
  const set = new Set();
  window.BASELINE_PTE.segments.forEach((row) => {
    if (row.equiId) {
      set.add(row.equiId);
    }
  });
  const sorted = Array.from(set).sort((a, b) => a.localeCompare(b));
  equiSuggestions.innerHTML = "";
  sorted.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    equiSuggestions.appendChild(option);
  });
};

const normalizeKey = (value) =>
  String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "");

const HAP_METALS = [
  "arsenic",
  "cadmium",
  "chromium",
  "hexavalentchromium",
  "cobalt",
  "manganese",
  "mercury",
  "nickel",
  "selenium",
  "antimony",
  "barium",
  "beryllium",
];

const classifyPollutant = (name) => {
  const raw = String(name || "").toLowerCase().trim();
  const key = normalizeKey(raw);
  const ghgKeys = [
    "co2",
    "co2e",
    "ch4",
    "n2o",
    "hfc",
    "pfc",
    "sf6",
    "nf3",
    "carbondioxide",
    "methane",
    "nitrousoxide",
  ];
  const criteriaKeys = [
    "carbonmonoxide",
    "nox",
    "no2",
    "nitrogenoxides",
    "so2",
    "sulfurdioxide",
    "voc",
    "volatileorganiccompounds",
    "pm",
    "pm10",
    "pm25",
    "particulatematter",
    "lead",
    "pb",
  ];

  if (ghgKeys.some((token) => key.startsWith(token))) {
    return "ghg";
  }
  if (key === "co" || key === "carbonmonoxide") {
    return "criteria";
  }
  if (criteriaKeys.some((token) => key === token || key.startsWith(token))) {
    return "criteria";
  }
  if (raw.includes("compound") || raw.includes("compounds")) {
    return "hap";
  }
  if (HAP_METALS.some((metal) => key.includes(metal))) {
    return "hap";
  }
  return "hap";
};

const renderPteTable = (group) => {
  const table = document.createElement("table");
  table.className = "data-table";

  const thead = document.createElement("thead");
  thead.innerHTML = `
    <tr>
      <th>Pollutant</th>
      <th>Potential (lbs/hr)</th>
      <th>Unrestricted Potential (tons/yr)</th>
      <th>Potential Limited (tons/yr)</th>
      <th>Actual Emissions (tons/yr)</th>
    </tr>`;
  table.appendChild(thead);

  const filters = {
    criteria: filterCriteria.checked,
    hap: filterHap.checked,
    ghg: filterGhg.checked,
  };

  const buckets = {
    criteria: [],
    hap: [],
    ghg: [],
  };

  group.rows.forEach((row) => {
    const category = classifyPollutant(row.Pollutant);
    buckets[category].push(row);
  });

  const sections = [
    { key: "criteria", title: "Criteria Pollutants" },
    { key: "hap", title: "HAP and Air Toxics" },
    { key: "ghg", title: "Greenhouse Gases (GHG)" },
  ];

  const tbody = document.createElement("tbody");
  sections.forEach((section) => {
    if (!filters[section.key]) {
      return;
    }
    const rows = buckets[section.key];
    if (!rows || rows.length === 0) {
      return;
    }
    rows.sort((a, b) =>
      normalize(String(a.Pollutant || "")).localeCompare(
        normalize(String(b.Pollutant || ""))
      )
    );

    const heading = document.createElement("tr");
    heading.className = "table-section";
    heading.innerHTML = `<th colspan="5">${section.title}</th>`;
    tbody.appendChild(heading);

    rows.forEach((row) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${formatValue(row.Pollutant)}</td>
        <td>${formatValue(row["Potential (lbs/hr)"])}</td>
        <td>${formatValue(row["Unrestricted Potential (tons/yr)"])}</td>
        <td>${formatValue(row["Potential Limited (tons/yr)"])}</td>
        <td>${formatValue(row["Actual Emissions (tons/yr)"])}</td>`;
      tbody.appendChild(tr);
    });
  });

  table.appendChild(tbody);
  return table;
};

const bubble = (label, subtitle, active = false) => {
  const el = document.createElement("div");
  el.className = `bubble${active ? " active" : ""}`;
  el.innerHTML = `
    <div class="bubble-label">${formatValue(label)}</div>
    ${subtitle ? `<div class="bubble-sub">${formatValue(subtitle)}</div>` : ""}`;
  return el;
};

const isToken = (value, token) => normalize(value).includes(token);

const renderRelationshipSummary = (query, relatedRows) => {
  const sheet = getSheetData("SI - Relationships");
  if (!sheet) {
    return null;
  }

  const queryNorm = normalize(query);
  const rows = sheet.rows;
  const comgToken = "comg";
  const focusRows = relatedRows && relatedRows.length > 0 ? relatedRows : rows;

  const comgId = focusRows.reduce((found, row) => {
    if (found) {
      return found;
    }
    const type = normalize(row["Subject Item Type Description"]);
    const relatedType = normalize(row["Related Subject Item Type Description"]);
    if (type.includes(comgToken)) {
      return row["Subject Item ID"] || row["Subject Item Designation"];
    }
    if (relatedType.includes(comgToken)) {
      return row["Related Subject Item ID"];
    }
    return null;
  }, null);

  const wrapper = document.createElement("div");
  wrapper.className = "relationship-summary";

  if (comgId) {
    const comgNorm = normalize(comgId);
    const comgRows = rows.filter((row) => {
      return (
        normalize(row["Subject Item ID"]) === comgNorm ||
        normalize(row["Related Subject Item ID"]) === comgNorm
      );
    });

    const members = [];
    const seen = new Set();
    comgRows.forEach((row) => {
      const type = normalize(row["Subject Item Type Description"]);
      const relatedType = normalize(row["Related Subject Item Type Description"]);
      if (!type.includes(comgToken)) {
        const label = row["Subject Item Designation"] || row["Subject Item ID"];
        const id = row["Subject Item ID"];
        const key = `${label}|${id}`;
        if (!seen.has(key)) {
          members.push({ label, id });
          seen.add(key);
        }
      }
      if (!relatedType.includes(comgToken)) {
        const label = row["Related Subject Item ID"];
        if (label) {
          const key = `${label}|${label}`;
          if (!seen.has(key)) {
            members.push({ label, id: label });
            seen.add(key);
          }
        }
      }
    });

    const comgBlock = document.createElement("div");
    comgBlock.className = "comg-block";
    comgBlock.appendChild(bubble("COMG", comgId, false));

    const group = document.createElement("div");
    group.className = "bubble-group";
    members.forEach((member) => {
      const isMatch =
        normalize(member.label) === queryNorm || normalize(member.id) === queryNorm;
      group.appendChild(bubble(member.label, member.id, isMatch));
    });
    comgBlock.appendChild(group);
    wrapper.appendChild(comgBlock);
  }

  const flowRows = focusRows.filter((row) => {
    const subjectType = normalize(row["Subject Item Type Description"]);
    const relatedType = normalize(row["Related Subject Item Type Description"]);
    const subjectId = normalize(row["Subject Item ID"]);
    const relatedId = normalize(row["Related Subject Item ID"]);
    const idMatch =
      subjectId === queryNorm ||
      relatedId === queryNorm ||
      normalize(row["Subject Item Designation"]) === queryNorm;
    return (
      idMatch &&
      (isToken(subjectType, "stru") ||
        isToken(subjectType, "trea") ||
        isToken(subjectType, "sv") ||
        isToken(relatedType, "stru") ||
        isToken(relatedType, "trea") ||
        isToken(relatedType, "sv"))
    );
  });

  if (flowRows.length > 0) {
    const flow = document.createElement("div");
    flow.className = "relationship-flow";

    flowRows.forEach((row) => {
      const subjectLabel = row["Subject Item Designation"] || row["Subject Item ID"];
      const relatedLabel = row["Related Subject Item ID"];
      const relationship = normalize(row["Relationship (F/R)"]);
      const receives = relationship.includes("receives from");
      const from = receives ? relatedLabel : subjectLabel;
      const to = receives ? subjectLabel : relatedLabel;

      const fromActive = normalize(from) === queryNorm;
      const toActive = normalize(to) === queryNorm;

      const line = document.createElement("div");
      line.className = "flow-row";
      line.appendChild(bubble(from, null, fromActive));
      const arrow = document.createElement("div");
      arrow.className = "flow-arrow";
      arrow.textContent = "->";
      line.appendChild(arrow);
      line.appendChild(bubble(to, null, toActive));
      flow.appendChild(line);
    });

    wrapper.appendChild(flow);
  }

  if (!wrapper.hasChildNodes()) {
    return null;
  }
  return wrapper;
};

const renderRelationshipFallback = (rows) => {
  const wrapper = document.createElement("div");
  wrapper.className = "relationship-fallback";
  rows.forEach((row) => {
    const line = document.createElement("div");
    line.className = "flow-row";
    const left = row["Subject Item Designation"] || row["Subject Item ID"];
    const right = row["Related Subject Item ID"];
    line.appendChild(bubble(left, row["Subject Item Type Description"], false));
    const arrow = document.createElement("div");
    arrow.className = "flow-arrow";
    arrow.textContent = row["Relationship (F/R)"] || "related to";
    line.appendChild(arrow);
    line.appendChild(bubble(right, row["Related Subject Item Type Description"], false));
    wrapper.appendChild(line);
  });
  return wrapper;
};

const buildSummaryCard = (title, items) => {
  const card = document.createElement("div");
  card.className = "summary-card";
  const heading = document.createElement("h3");
  heading.textContent = title;
  card.appendChild(heading);

  const list = document.createElement("div");
  list.className = "summary-list";
  items.forEach((item) => {
    if (isEmptyValue(item.value)) {
      return;
    }
    const row = document.createElement("div");
    row.className = "summary-item";
    row.innerHTML = `<span>${item.label}</span><span>${formatValue(item.value)}</span>`;
    list.appendChild(row);
  });
  card.appendChild(list);
  return card;
};

const formatCapacity = (row) => {
  const value = row["Max Design Capacity"];
  const num = row["Max Design Capacity Units (numerator)"];
  const den = row["Max Design Capacity Units (denominator)"];
  if (isEmptyValue(value) && isEmptyValue(num) && isEmptyValue(den)) {
    return null;
  }
  return `${formatValue(value)} ${formatValue(num)} ${formatValue(den)}`.trim();
};

const renderSummary = (query, matches) => {
  if (!matches || matches.length === 0) {
    return;
  }

  const summaryCards = [];
  const general = matches.find((group) => group.sheet === "EU - General");
  const combustion = matches.find((group) => group.sheet === "EU - Combustion");
  const baseRow =
    (general && general.rows[0]) || (combustion && combustion.rows[0]) || null;

  if (baseRow) {
    summaryCards.push(
      buildSummaryCard(`Unit Summary: ${query}`, [
        { label: "Designation", value: baseRow["Subject Item Designation"] },
        { label: "Subject Item ID", value: baseRow["Subject Item ID"] },
        { label: "Type", value: baseRow["Subject Item Type Description"] },
        { label: "Manufacturer", value: baseRow["Manufacturer"] },
        { label: "Model", value: baseRow["Model"] },
        { label: "Description", value: baseRow["Description"] },
        { label: "Max Design Capacity", value: formatCapacity(baseRow) },
        { label: "Material", value: baseRow["Material"] },
        { label: "Construction Start", value: baseRow["Construction Start Date"] },
        { label: "Operation Start", value: baseRow["Operation Start Date"] },
      ])
    );
  }

  const relationships = matches.find(
    (group) => group.sheet === "SI - Relationships"
  );
  if (relationships) {
    const summary = renderRelationshipSummary(query, relationships.rows);
    if (summary) {
      const card = document.createElement("div");
      card.className = "summary-card";
      const heading = document.createElement("h3");
      heading.textContent = `Relationship Map: ${query}`;
      card.appendChild(heading);
      card.appendChild(summary);
      summaryCards.push(card);
    }
  }

  summaryCards.forEach((card) => summaryEl.appendChild(card));
};

const renderResultsInto = (container, matches, query) => {
  if (!matches || matches.length === 0) {
    container.innerHTML =
      "<div class=\"empty\">No matching emission unit found.</div>";
    return;
  }

  matches.forEach((group) => {
    const section = document.createElement("section");
    section.className = "result-group";

    const header = document.createElement("div");
    header.className = "result-header";
    header.innerHTML = `<h2>${group.sheet}</h2><span>${group.rows.length} match(es)</span>`;
    section.appendChild(header);

    if (group.sheet === "SI - Relationships") {
      const summary = renderRelationshipSummary(query, group.rows);
      if (summary) {
        const card = document.createElement("div");
        card.className = "result-card";
        card.appendChild(summary);
        section.appendChild(card);
      } else if (group.rows && group.rows.length > 0) {
        const card = document.createElement("div");
        card.className = "result-card";
        card.appendChild(renderRelationshipFallback(group.rows));
        section.appendChild(card);
      }
      container.appendChild(section);
      return;
    }

    if (group.sheet === "PTE - Subject Item") {
      const card = document.createElement("div");
      card.className = "result-card";
      card.appendChild(renderPteTable(group));
      section.appendChild(card);
    } else {
      group.rows.forEach((row) => {
        const card = document.createElement("div");
        card.className = "result-card";
        card.appendChild(renderRowTable(row, group.columns));
        section.appendChild(card);
      });
    }

    container.appendChild(section);
  });
};

const findMatches = (query, broad = false) => {
  const data = window.PERMIT_DATA;
  if (!data || !data.sheets) {
    return [];
  }

  const queryNorm = normalize(query);
  const matches = [];

  data.sheets.forEach((group) => {
    const columns =
      group.matchColumns && group.matchColumns.length > 0
        ? group.matchColumns
        : ["Subject Item ID", "Subject Item Designation"];

    const rows = group.rows.filter((row) => {
      if (broad) {
        return group.columns.some((column) =>
          normalize(row[column]).includes(queryNorm)
        );
      }
      return columns.some((column) => normalize(row[column]) === queryNorm);
    });

    if (rows.length > 0) {
      matches.push({
        sheet: group.sheet,
        columns: group.columns,
        rows,
      });
    }
  });

  return matches;
};

const downloadCsv = () => {
  if (!state.lastResults.length) {
    setStatus("No results to export yet.", "warn");
    return;
  }

  const rows = [];
  state.lastResults.forEach((result) => {
    result.matches.forEach((group) => {
      group.rows.forEach((row) => {
        const record = { Query: result.query, Sheet: group.sheet };
        group.columns.forEach((col) => {
          record[col] = row[col];
        });
        rows.push(record);
      });
    });
  });

  if (rows.length === 0) {
    setStatus("No rows available for export.", "warn");
    return;
  }

  const headers = Array.from(
    rows.reduce((set, row) => {
      Object.keys(row).forEach((key) => set.add(key));
      return set;
    }, new Set())
  );

  const escapeCsv = (value) => {
    const text = value === null || value === undefined ? "" : String(value);
    if (text.includes("\"") || text.includes(",") || text.includes("\n")) {
      return `"${text.replace(/"/g, "\"\"")}"`;
    }
    return text;
  };

  const csv = [
    headers.join(","),
    ...rows.map((row) => headers.map((h) => escapeCsv(row[h])).join(",")),
  ].join("\n");

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "permit_lookup_results.csv";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

const handleSearch = () => {
  const query = input.value.trim();
  if (!query) {
    setStatus("Enter an emission unit ID to search.", "warn");
    return;
  }

  if (!window.PERMIT_DATA) {
    setStatus("Data file not loaded. Run build_data.py first.", "error");
    return;
  }

  const compareEnabled = compareMode.checked;
  const compareQuery = compareInput.value.trim();
  if (compareEnabled && !compareQuery) {
    setStatus("Enter a value to compare.", "warn");
    return;
  }

  setStatus("Searching the permit data...", "info");
  clearResults();
  clearSummary();

  const matches = findMatches(query, broadSearch.checked);
  state.lastResults = [{ query, matches }];

  resultsEl.classList.toggle("compare", compareEnabled);
  if (!compareEnabled) {
    renderSummary(query, matches);
    renderResultsInto(resultsEl, matches, query);
    if (!summaryEl.hasChildNodes()) {
      summaryEl.innerHTML = "<div class=\"empty\">No summary found.</div>";
    }
    setStatus(`Results for "${query}".`, "success");
    return;
  }

  const compareMatches = findMatches(compareQuery, broadSearch.checked);
  state.lastResults.push({ query: compareQuery, matches: compareMatches });

  renderSummary(query, matches);
  renderSummary(compareQuery, compareMatches);
  if (!summaryEl.hasChildNodes()) {
    summaryEl.innerHTML = "<div class=\"empty\">No summary found.</div>";
  }

  const left = document.createElement("div");
  const right = document.createElement("div");
  renderResultsInto(left, matches, query);
  renderResultsInto(right, compareMatches, compareQuery);
  resultsEl.appendChild(left);
  resultsEl.appendChild(right);
  setStatus(`Comparing "${query}" with "${compareQuery}".`, "success");
};

const renderDashboardTable = (segments, references) => {
  const card = document.createElement("div");
  card.className = "dashboard-card";
  const heading = document.createElement("h3");
  heading.textContent = "Segment Emissions and Methodology";
  card.appendChild(heading);

  const wrap = document.createElement("div");
  wrap.className = "table-wrap";
  const table = document.createElement("table");
  table.className = "dashboard-table";
  table.innerHTML = `
    <thead>
      <tr>
        <th>Seg Description</th>
        <th>Source Category</th>
        <th>Pollutant</th>
        <th>Hourly Potential (lb/hr)</th>
        <th>Limited Potential (tpy)</th>
        <th>Emission Factor</th>
        <th>EF Unit</th>
        <th>Throughput</th>
        <th>Control Efficiency (%)</th>
        <th>EF Source</th>
        <th>Reference ID</th>
        <th>Reference Text</th>
        <th>SV/STRU/TREA</th>
      </tr>
    </thead>`;

  const tbody = document.createElement("tbody");
  const buckets = {
    criteria: [],
    hap: [],
    ghg: [],
  };

  segments.forEach((row) => {
    const category = classifyPollutant(row.pollutant);
    buckets[category].push(row);
  });

  const sections = [
    { key: "criteria", title: "Criteria Pollutants" },
    { key: "hap", title: "HAP and Air Toxics" },
    { key: "ghg", title: "Greenhouse Gases (GHG)" },
  ];

  sections.forEach((section) => {
    const rows = buckets[section.key];
    if (!rows || rows.length === 0) {
      return;
    }
    rows.sort((a, b) =>
      normalize(String(a.pollutant || "")).localeCompare(
        normalize(String(b.pollutant || ""))
      )
    );

    const headingRow = document.createElement("tr");
    headingRow.className = "dashboard-section";
    headingRow.innerHTML = `<th colspan="13">${section.title}</th>`;
    tbody.appendChild(headingRow);

    rows.forEach((row) => {
      const referenceId = row.efSourceId || "";
      const referenceText = referenceId && references[referenceId]
        ? references[referenceId]
        : "";
      const svStruTrea = [
        row.deltaSv ? row.deltaSv : null,
        row.tempoStru ? row.tempoStru : null,
        row.tempoTrea ? row.tempoTrea : null,
      ]
        .filter(Boolean)
        .join(" / ");

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${formatValue(row.segDescription)}</td>
        <td>${formatValue(row.sourceCategory)}</td>
        <td>${formatValue(row.pollutant)}</td>
        <td>${formatValue(row.hourlyPotentialLbHr)}</td>
        <td>${formatValue(row.limitedPotentialTpy)}</td>
        <td>${formatValue(row.emissionFactor)}</td>
        <td>${formatValue(row.emissionFactorUnit)}</td>
        <td>${formatValue(row.throughput)} ${formatValue(row.throughputUnits)}</td>
        <td>${formatValue(row.controlEfficiency)}</td>
        <td>${formatValue(row.emissionFactorSource)}</td>
        <td>${formatValue(referenceId)}</td>
        <td>${formatValue(referenceText)}</td>
        <td>${formatValue(svStruTrea)}</td>`;
      tbody.appendChild(tr);
    });
  });
  table.appendChild(tbody);
  wrap.appendChild(table);
  card.appendChild(wrap);
  return card;
};

const buildDashboardMetrics = (segments) => {
  const totals = {
    hourly: 0,
    limited: 0,
  };
  segments.forEach((row) => {
    const hourly = toNumber(row.hourlyPotentialLbHr);
    const limited = toNumber(row.limitedPotentialTpy);
    if (hourly) {
      totals.hourly += hourly;
    }
    if (limited) {
      totals.limited += limited;
    }
  });

  const wrap = document.createElement("div");
  wrap.className = "dashboard-metrics";
  wrap.appendChild(
    buildSummaryCard("Total Hourly (lb/hr)", [
      { label: "Sum", value: formatValue(totals.hourly) },
    ])
  );
  wrap.appendChild(
    buildSummaryCard("Total Limited (tpy)", [
      { label: "Sum", value: formatValue(totals.limited) },
    ])
  );
  wrap.appendChild(
    buildSummaryCard("Segments", [
      { label: "Count", value: segments.length },
    ])
  );
  return wrap;
};

const buildBarChart = (title, series, valueLabel) => {
  const card = document.createElement("div");
  card.className = "dashboard-card";
  const heading = document.createElement("h3");
  heading.textContent = title;
  card.appendChild(heading);

  if (!series.length) {
    card.innerHTML += "<div class=\"empty\">No data available.</div>";
    return card;
  }

  const max = Math.max(...series.map((item) => item.value));
  const list = document.createElement("div");
  list.className = "bar-list";
  series.forEach((item) => {
    const row = document.createElement("div");
    row.className = "bar-row";
    const label = document.createElement("div");
    label.className = "bar-label";
    label.textContent = item.label;
    const barWrap = document.createElement("div");
    barWrap.className = "bar-track";
    const bar = document.createElement("div");
    bar.className = "bar-fill";
    bar.style.width = max > 0 ? `${(item.value / max) * 100}%` : "0%";
    barWrap.appendChild(bar);
    const value = document.createElement("div");
    value.className = "bar-value";
    value.textContent = `${formatValue(item.value)} ${valueLabel}`;
    row.appendChild(label);
    row.appendChild(barWrap);
    row.appendChild(value);
    list.appendChild(row);
  });
  card.appendChild(list);
  return card;
};

const buildRankCards = (query, segments) => {
  const pollutants = ["NOx", "SO2", "PM10", "VOC"];
  const card = document.createElement("div");
  card.className = "dashboard-card";
  const heading = document.createElement("h3");
  heading.textContent = "Ranking Among Sources (Limited tpy)";
  card.appendChild(heading);

  if (!window.BASELINE_PTE || !window.BASELINE_PTE.segments) {
    card.innerHTML += "<div class=\"empty\">Baseline data not loaded.</div>";
    return card;
  }

  const allSegments = window.BASELINE_PTE.segments;
  const rankList = document.createElement("div");
  rankList.className = "rank-list";

  pollutants.forEach((pollutant) => {
    const totals = {};
    allSegments.forEach((row) => {
      if (normalizeKey(row.pollutant) !== normalizeKey(pollutant)) {
        return;
      }
      const limited = toNumber(row.limitedPotentialTpy) || 0;
      if (!limited) {
        return;
      }
      const equi = row.equiId || row.equiIdNorm || "Unknown";
      totals[equi] = (totals[equi] || 0) + limited;
    });

    const ordered = Object.entries(totals)
      .map(([equi, value]) => ({ equi, value }))
      .sort((a, b) => b.value - a.value);

    const idx = ordered.findIndex(
      (item) => normalizeEqui(item.equi) === normalizeEqui(query)
    );
    const rank = idx >= 0 ? idx + 1 : null;
    const total = ordered.length;
    const row = document.createElement("div");
    row.className = "rank-row";
    row.innerHTML = `
      <div class="rank-label">${pollutant}</div>
      <div class="rank-value">${
        rank ? `#${rank} of ${total}` : "Not ranked"
      }</div>
      <div class="rank-emission">${
        rank ? `${formatValue(ordered[idx].value)} tpy` : "-"
      }</div>`;
    rankList.appendChild(row);
  });

  card.appendChild(rankList);
  return card;
};

const handleDashboardSearch = () => {
  const query = dashboardEqui.value.trim();
  if (!query) {
    setDashboardStatus("Enter an EQUI ID to search.", "warn");
    return;
  }
  if (!window.BASELINE_PTE || !window.BASELINE_PTE.segments) {
    setDashboardStatus("Baseline data not loaded. Run build_baseline_data.py first.", "error");
    return;
  }

  setDashboardStatus("Loading emission calculations...", "info");
  clearDashboardResults();

  const queryNorm = normalizeEqui(query);
  const segments = window.BASELINE_PTE.segments.filter(
    (row) => normalizeEqui(row.equiIdNorm || row.equiId) === queryNorm
  );

  const nonzeroOnly = dashboardNonzero.checked;
  const filtered = nonzeroOnly
    ? segments.filter((row) => {
        const hourly = toNumber(row.hourlyPotentialLbHr);
        const limited = toNumber(row.limitedPotentialTpy);
        return (hourly && hourly > 0) || (limited && limited > 0);
      })
    : segments;

  if (!filtered.length) {
    setDashboardStatus("No segment data found for that EQUI ID.", "warn");
    dashboardResults.innerHTML = "<div class=\"empty\">No segment rows found.</div>";
    return;
  }

  const references = window.BASELINE_PTE.references || {};
  dashboardResults.appendChild(buildDashboardMetrics(filtered));
  dashboardResults.appendChild(buildRankCards(query, filtered));
  dashboardResults.appendChild(renderDashboardTable(filtered, references));
  state.lastDashboard = {
    query,
    segments: filtered,
    references,
  };
  const note = nonzeroOnly ? "Non-zero emissions only." : "Including zero rows.";
  setDashboardStatus(`Showing ${filtered.length} segment rows. ${note}`, "success");
};

const handleTabClick = (event) => {
  const target = event.currentTarget;
  const tabId = target.getAttribute("data-tab");
  tabs.forEach((tab) => tab.classList.remove("active"));
  panels.forEach((panel) => panel.classList.remove("active"));
  target.classList.add("active");
  const panel = document.getElementById(`tab-${tabId}`);
  if (panel) {
    panel.classList.add("active");
  }
};

form.addEventListener("submit", (event) => {
  event.preventDefault();
  handleSearch();
});

dashboardForm.addEventListener("submit", (event) => {
  event.preventDefault();
  handleDashboardSearch();
});

compareMode.addEventListener("change", () => {
  form.classList.toggle("compare-active", compareMode.checked);
  if (!compareMode.checked) {
    compareInput.value = "";
  }
});

[filterCriteria, filterHap, filterGhg].forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    if (state.lastResults.length) {
      handleSearch();
    }
  });
});

exportCsv.addEventListener("click", downloadCsv);
exportPdf.addEventListener("click", () => window.print());

tabs.forEach((tab) => {
  tab.addEventListener("click", handleTabClick);
});

const exportDashboardXlsx = () => {
  if (!state.lastDashboard || !state.lastDashboard.segments.length) {
    setDashboardStatus("Run a dashboard search before exporting.", "warn");
    return;
  }
  if (typeof XLSX === "undefined") {
    setDashboardStatus("XLSX library not loaded.", "error");
    return;
  }

  const { query, segments, references } = state.lastDashboard;
  const rows = [
    [
      "EQUI ID",
      "Seg",
      "Seg Description",
      "Source Category",
      "Pollutant",
      "Hourly Potential (lb/hr)",
      "Limited Potential (tpy)",
      "Emission Factor",
      "EF Unit",
      "Throughput",
      "Throughput Units",
      "Control Efficiency (%)",
      "EF Source",
      "Reference ID",
      "Reference Text",
      "SV/STRU/TREA",
    ],
  ];

  segments.forEach((row) => {
    const referenceId = row.efSourceId || "";
    const referenceText =
      referenceId && references[referenceId] ? references[referenceId] : "";
    const svStruTrea = [
      row.deltaSv ? row.deltaSv : null,
      row.tempoStru ? row.tempoStru : null,
      row.tempoTrea ? row.tempoTrea : null,
    ]
      .filter(Boolean)
      .join(" / ");

    rows.push([
      row.equiId,
      row.seg,
      row.segDescription,
      row.sourceCategory,
      row.pollutant,
      row.hourlyPotentialLbHr,
      row.limitedPotentialTpy,
      row.emissionFactor,
      row.emissionFactorUnit,
      row.throughput,
      row.throughputUnits,
      row.controlEfficiency,
      row.emissionFactorSource,
      referenceId,
      referenceText,
      svStruTrea,
    ]);
  });

  const worksheet = XLSX.utils.aoa_to_sheet(rows);
  worksheet["!cols"] = [
    { wch: 12 },
    { wch: 6 },
    { wch: 26 },
    { wch: 18 },
    { wch: 14 },
    { wch: 20 },
    { wch: 20 },
    { wch: 16 },
    { wch: 10 },
    { wch: 14 },
    { wch: 16 },
    { wch: 18 },
    { wch: 16 },
    { wch: 12 },
    { wch: 60 },
    { wch: 18 },
  ];

  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Emission Calculations");
  XLSX.writeFile(workbook, `${query.replace(/\s+/g, "_")}_emissions.xlsx`);
  setDashboardStatus("Exported XLSX successfully.", "success");
};

dashboardExportXlsx.addEventListener("click", exportDashboardXlsx);

if (window.PERMIT_DATA) {
  buildSuggestions();
}

if (window.BASELINE_PTE) {
  buildEquiSuggestions();
}
