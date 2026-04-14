const data = window.AUDIT_DATA;

const CATEGORY_LABELS = {
  all: "All Items",
  equipment: "Emission Units",
  control: "Controls",
  stack: "Stacks",
  monitor: "Monitors",
  fugitive: "Fugitives",
  group: "Permit Groups",
};

const KIND_CLASSES = {
  equipment: "kind-equipment",
  control: "kind-control",
  stack: "kind-stack",
  monitor: "kind-monitor",
  fugitive: "kind-fugitive",
  group: "kind-group",
};

const state = {
  query: "",
  category: "all",
  selectedKey: null,
  skipAutoSelect: false,
  detailTab: "overview",
};

const collator = new Intl.Collator(undefined, {
  numeric: true,
  sensitivity: "base",
});

const els = {
  pageTitle: document.getElementById("page-title"),
  pageSubtitle: document.getElementById("page-subtitle"),
  metaDetails: document.getElementById("meta-details"),
  documentLinks: document.getElementById("document-links"),
  statGrid: document.getElementById("stat-grid"),
  searchInput: document.getElementById("search-input"),
  categoryFilters: document.getElementById("category-filters"),
  resultCount: document.getElementById("result-count"),
  resultList: document.getElementById("result-list"),
  detailPanel: document.getElementById("detail-panel"),
  printPage: document.getElementById("print-page"),
};

const normalize = (value) => String(value || "").trim().toLowerCase();
const normalizeId = (value) => String(value || "").replace(/\s+/g, "").toUpperCase();
const normalizeKey = (value) => String(value || "").toLowerCase().replace(/[^a-z0-9]/g, "");

const isPresent = (value) => {
  if (value === null || value === undefined) {
    return false;
  }
  const text = String(value).trim();
  if (!text) {
    return false;
  }
  const lower = text.toLowerCase();
  return lower !== "nan" && lower !== "null";
};

const escapeHtml = (value) =>
  String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const unique = (values) => Array.from(new Set(values.filter(isPresent)));

const getFirst = (row, names) => {
  for (const name of names) {
    if (isPresent(row[name])) {
      return row[name];
    }
  }
  return null;
};

const getValuesByKeyPatterns = (row, patterns) => {
  const normalizedPatterns = patterns.map(normalizeKey);
  return Object.entries(row)
    .filter(([key, value]) => {
      if (!isPresent(value)) {
        return false;
      }
      const normalizedColumn = normalizeKey(key);
      return normalizedPatterns.some((pattern) => normalizedColumn.includes(pattern));
    })
    .map(([, value]) => value);
};

const formatDate = (value) => {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return null;
  }
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

const formatValue = (value) => {
  if (!isPresent(value)) {
    return "-";
  }
  if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T/.test(value)) {
    return formatDate(value) || value;
  }
  return String(value);
};

const joinValues = (values) => {
  const list = unique(values);
  return list.length ? list.join(", ") : null;
};

const relationshipSection = (data?.sections || []).find(
  (section) => section.kind === "relationship"
);

const relationshipRows = relationshipSection
  ? relationshipSection.rows.map((row) => ({
      subjectId: getFirst(row, ["Subject Item ID", "SI ID"]),
      subjectDesignation: getFirst(row, ["Subject Item Designation", "SI Designation"]),
      subjectDescription: getFirst(row, ["Subject Item Description", "Description"]),
      subjectType: getFirst(row, ["Subject Item Type Description", "SI Type Description"]),
      relationship: getFirst(row, ["Relationship", "Relationship (F/R)"]),
      relatedId: row["Related Subject Item ID"] || null,
      relatedType: row["Related Subject Item Type Description"] || null,
      percentFlow: row["% Flow"] || null,
      note: row["Unnamed: 11"] || row[""] || null,
    }))
  : [];

const itemMap = new Map();
const pdfItems = data?.pdfItems || [];
const permitData = data?.permit || {};
const permitItems = permitData?.items || [];
const permitConditions = permitData?.conditions || [];
const permitComgMemberships = permitData?.comgMemberships || { groups: {}, members: {} };
const permitAppendixExcerpts = permitData?.appendixExcerpts || [];

const getItemKey = (kind, row, fallback) => {
  const itemId = normalizeId(getFirst(row, ["Subject Item ID", "SI ID"]));
  if (itemId) {
    return `id:${itemId}`;
  }
  const designation = normalizeId(getFirst(row, ["Subject Item Designation", "SI Designation"]));
  if (designation) {
    return `designation:${kind}:${designation}`;
  }
  const description = normalize(getFirst(row, ["Subject Item Description", "Description"]));
  if (description) {
    return `description:${kind}:${description}`;
  }
  return `fallback:${kind}:${fallback}`;
};

const attachRowToItem = (section, row, index) => {
  const key = getItemKey(section.kind, row, `${section.sheet}-${index}`);
  const itemId = getFirst(row, ["Subject Item ID", "SI ID"]);
  const designation = getFirst(row, ["Subject Item Designation", "SI Designation"]);
  const description = getFirst(row, ["Subject Item Description", "Description"]);
  const itemType = getFirst(row, ["Subject Item Type Description", "SI Type Description"]);

  if (!itemMap.has(key)) {
    itemMap.set(key, {
      key,
      kind: section.kind,
      itemId: itemId || null,
      designation: designation || null,
      description: description || null,
      itemType: itemType || null,
      rows: [],
      sheets: new Set(),
      searchTokens: new Set(),
    });
  }

  const item = itemMap.get(key);
  item.rows.push({ sheet: section.sheet, columns: section.columns, row });
  item.sheets.add(section.sheet);

  [itemId, designation, description, itemType].forEach((value) => {
    if (isPresent(value)) {
      item.searchTokens.add(String(value));
    }
  });

  Object.values(row).forEach((value) => {
    if (isPresent(value)) {
      item.searchTokens.add(String(value));
    }
  });
};

(data?.sections || [])
  .filter((section) => section.kind !== "relationship")
  .forEach((section) => {
    section.rows.forEach((row, index) => attachRowToItem(section, row, index));
  });

const items = Array.from(itemMap.values()).map((item) => {
  const sheets = Array.from(item.sheets);
  const itemIdNorm = normalizeId(item.itemId);
  const designationNorm = normalizeId(item.designation);
  return {
    ...item,
    sheets,
    itemIdNorm,
    designationNorm,
    searchableText: Array.from(item.searchTokens).join(" ").toLowerCase(),
    title: item.designation || item.itemId || item.description || "Unnamed Item",
    subtitle: item.description || item.itemType || item.itemId || "No description available",
  };
});

const pdfById = new Map(pdfItems.map((item) => [normalizeId(item.itemId), item]));

const getPdfMatchForWorkbookItem = (item) => {
  if (item.itemIdNorm && pdfById.has(item.itemIdNorm)) {
    return pdfById.get(item.itemIdNorm);
  }
  return null;
};

const permitItemById = new Map(
  permitItems.map((item) => [normalizeId(item.itemId), item])
);
const permitConditionsByItem = permitConditions.reduce((acc, condition) => {
  const itemId = normalizeId(condition.subjectItemId);
  if (!itemId) {
    return acc;
  }
  if (!acc.has(itemId)) {
    acc.set(itemId, []);
  }
  acc.get(itemId).push(condition);
  return acc;
}, new Map());
const appendixExcerptById = new Map(
  permitAppendixExcerpts.map((excerpt) => [String(excerpt.appendixId || "").toUpperCase(), excerpt])
);

const getPermitKind = (itemId) => {
  if (itemId.startsWith("COMG")) {
    return "group";
  }
  if (itemId.startsWith("TREA")) {
    return "control";
  }
  if (itemId.startsWith("STRU")) {
    return "stack";
  }
  if (itemId.startsWith("FUGI")) {
    return "fugitive";
  }
  return "equipment";
};

let mergedItems = items.map((item) => {
  const pdf = getPdfMatchForWorkbookItem(item);
  const pdfDescription = pdf?.description || null;
  const pdfDesignation = pdf?.designation || null;
  const displayId = pdf?.itemId || item.itemId || null;
  const displayDesignation = pdfDesignation || item.designation || null;
  const displayDescription = pdfDescription || item.description || item.subtitle || null;
  const permitItem = permitItemById.get(normalizeId(displayId || item.itemId));
  const permitText = (permitConditionsByItem.get(normalizeId(displayId || item.itemId)) || [])
    .map((condition) => `${condition.requirementNumber} ${condition.text} ${condition.citation || ""}`)
    .join(" ");
  const searchParts = [
    item.searchableText,
    displayId,
    displayDesignation,
    displayDescription,
    permitItem?.title,
    permitText,
  ];
  return {
    ...item,
    pdf,
    permitItem,
    displayId,
    displayIdNorm: normalizeId(displayId),
    displayDesignation,
    displayDescription,
    title: displayId || item.title,
    subtitle: displayDescription || item.subtitle,
    searchableText: searchParts.filter(Boolean).join(" ").toLowerCase(),
  };
});

const matchedPdfIds = new Set(
  mergedItems.map((item) => normalizeId(item.pdf?.itemId || item.displayId || item.itemId))
);

pdfItems.forEach((pdf) => {
  const pdfIdNorm = normalizeId(pdf.itemId);
  if (!pdfIdNorm || matchedPdfIds.has(pdfIdNorm)) {
    return;
  }
  mergedItems.push({
    key: `pdf:${pdf.itemId}`,
    kind: pdf.kind,
    itemId: pdf.itemId,
    designation: pdf.designation || null,
    description: pdf.description || null,
    itemType: pdf.itemType || null,
    rows: [],
    sheets: [],
    itemIdNorm: pdfIdNorm,
    designationNorm: normalizeId(pdf.designation),
    searchableText: [
      pdf.itemId,
      pdf.designation,
      pdf.description,
      pdf.itemType,
      pdf.manufacturer,
      pdf.model,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
    title: pdf.itemId,
    subtitle: pdf.description || pdf.itemType || "PDF source record",
    pdf,
    permitItem: permitItemById.get(pdfIdNorm) || null,
    displayId: pdf.itemId,
    displayIdNorm: pdfIdNorm,
    displayDesignation: pdf.designation || null,
    displayDescription: pdf.description || pdf.itemType || null,
  });
});

const matchedItemIds = new Set(
  mergedItems.map((item) => normalizeId(item.displayId || item.itemId))
);

permitItems.forEach((permitItem) => {
  const permitId = normalizeId(permitItem.itemId);
  if (!permitId || matchedItemIds.has(permitId)) {
    return;
  }
  const directConditions = permitConditionsByItem.get(permitId) || [];
  mergedItems.push({
    key: `permit:${permitItem.itemId}`,
    kind: getPermitKind(permitId),
    itemId: permitItem.itemId,
    designation: null,
    description: permitItem.title || null,
    itemType: permitId.startsWith("COMG") ? "Permit Condition Group" : null,
    rows: [],
    sheets: [],
    itemIdNorm: permitId,
    designationNorm: "",
    searchableText: [
      permitItem.itemId,
      permitItem.title,
      ...directConditions.map(
        (condition) => `${condition.requirementNumber} ${condition.text} ${condition.citation || ""}`
      ),
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
    title: permitItem.itemId,
    subtitle: permitItem.title || "Title V permit item",
    pdf: null,
    permitItem,
    displayId: permitItem.itemId,
    displayIdNorm: permitId,
    displayDesignation: null,
    displayDescription: permitItem.title || "Title V permit item",
  });
});

mergedItems = mergedItems.map((item) => {
  const itemId = item.displayIdNorm || item.itemIdNorm;
  const directConditions = permitConditionsByItem.get(itemId) || [];
  const permitItem = item.permitItem || permitItemById.get(itemId) || null;
  return {
    ...item,
    permitItem,
    searchableText: [
      item.searchableText,
      permitItem?.title,
      ...directConditions.map(
        (condition) => `${condition.requirementNumber} ${condition.text} ${condition.citation || ""}`
      ),
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase(),
  };
});

const itemByKey = new Map(mergedItems.map((item) => [item.key, item]));
const itemById = new Map();
const itemByDesignation = new Map();

mergedItems.forEach((item) => {
  if (item.displayIdNorm && !itemById.has(item.displayIdNorm)) {
    itemById.set(item.displayIdNorm, item);
  }
  const designationNorm = normalizeId(item.displayDesignation || item.designation);
  if (designationNorm && !itemByDesignation.has(designationNorm)) {
    itemByDesignation.set(designationNorm, item);
  }
});

const categoryCounts = mergedItems.reduce(
  (acc, item) => {
    acc[item.kind] = (acc[item.kind] || 0) + 1;
    return acc;
  },
  { all: mergedItems.length }
);

const scoreItem = (item, query) => {
  if (!query) {
    return 0;
  }

  const queryNorm = normalize(query);
  const queryId = normalizeId(query);
  const itemIdNorm = item.displayIdNorm || item.itemIdNorm;
  const designationNorm = normalizeId(item.displayDesignation || item.designation);
  let score = 0;

  if (itemIdNorm && itemIdNorm === queryId) {
    score = 300;
  } else if (designationNorm && designationNorm === queryId) {
    score = 290;
  } else if (itemIdNorm && itemIdNorm.startsWith(queryId)) {
    score = 220;
  } else if (designationNorm && designationNorm.startsWith(queryId)) {
    score = 210;
  }

  if (normalize(item.description).includes(queryNorm)) {
    score = Math.max(score, 180);
  }
  if (normalize(item.itemType).includes(queryNorm)) {
    score = Math.max(score, 130);
  }
  if (item.searchableText.includes(queryNorm)) {
    score = Math.max(score, 120);
  }

  return score;
};

const getNaturalSortKey = (item) => {
  return item.displayId || item.itemId || item.displayDesignation || item.title || "";
};

const compareItemsNaturally = (left, right) => {
  const primary = collator.compare(getNaturalSortKey(left), getNaturalSortKey(right));
  if (primary !== 0) {
    return primary;
  }
  const secondary = collator.compare(left.title || "", right.title || "");
  if (secondary !== 0) {
    return secondary;
  }
  return collator.compare(left.subtitle || "", right.subtitle || "");
};

const getFilteredItems = () => {
  const filtered = mergedItems
    .filter((item) => state.category === "all" || item.kind === state.category)
    .map((item) => ({ item, score: scoreItem(item, state.query) }))
    .filter(({ score }) => !state.query || score > 0);

  filtered.sort((left, right) => {
    if (right.score !== left.score) {
      return right.score - left.score;
    }
    return compareItemsNaturally(left.item, right.item);
  });

  return filtered.map(({ item }) => item);
};

const getValues = (item, patterns) =>
  unique(item.rows.flatMap(({ row }) => getValuesByKeyPatterns(row, patterns)));

const getPreferredValue = (item, pdfField, workbookPatterns = []) => {
  if (item.pdf && item.pdf[pdfField]) {
    return item.pdf[pdfField];
  }
  if (!workbookPatterns.length) {
    return null;
  }
  return joinValues(getValues(item, workbookPatterns));
};

const buildFacts = (item) => {
  const directPermitConditions = permitConditionsByItem.get(item.displayIdNorm || item.itemIdNorm) || [];
  const commonFacts = [
    ["Subject Item ID", item.displayId || item.itemId],
    ["Designation", item.displayDesignation || item.designation],
    ["Type", getPreferredValue(item, "itemType", ["subjectitemtypedescription", "sitypedescription"]) || item.itemType],
    ["Description", item.displayDescription || item.description],
    ["Source Tabs", item.sheets.join(", ")],
    ["Workbook Notes", joinValues(getValues(item, ["notes"]))],
    ["PDF Source Page", item.pdf?.page ? `Page ${item.pdf.page}` : null],
    ["Title V Subject Item", item.permitItem?.title || null],
    ["Title V Start Page", item.permitItem?.page ? `Page ${item.permitItem.page}` : null],
    ["Direct Title V Conditions", directPermitConditions.length ? String(directPermitConditions.length) : null],
  ];

  const kindFacts = {
    equipment: [
      ["Manufacturer", getPreferredValue(item, "manufacturer", ["manufacturer"])],
      ["Model", getPreferredValue(item, "model", ["model"])],
      [
        "Max Design Capacity",
        joinValues(
          item.rows.map(({ row }) => {
            const value = getFirst(row, ["Max Design Capacity"]);
            const numerator = getFirst(row, ["Max Design Capacity Units (numerator)"]);
            const denominator = getFirst(row, ["Max Design Capacity Units (denominator)"]);
            if (!isPresent(value) && !isPresent(numerator) && !isPresent(denominator)) {
              return null;
            }
            return [value, numerator, denominator].filter(isPresent).join(" ");
          })
        ),
      ],
      ["Material", getPreferredValue(item, "material", ["material"])],
      ["Construction Start", item.pdf?.constructionStart || joinValues(getValues(item, ["constructionstartdate"]).map(formatValue))],
      ["Operation Start", item.pdf?.operationStart || joinValues(getValues(item, ["operationstartdate"]).map(formatValue))],
      ["Modification Date", item.pdf?.modificationDate || joinValues(getValues(item, ["modificationdate"]).map(formatValue))],
    ],
    control: [
      ["Manufacturer", getPreferredValue(item, "manufacturer", ["manufacturer"])],
      ["Model", getPreferredValue(item, "model", ["model"])],
      ["Pollutants Controlled", item.pdf?.pollutantsControlled || joinValues(getValues(item, ["pollutantcontrolled"]))],
      ["Capture Efficiency (%)", joinValues(getValues(item, ["captureefficiency"]))],
      [
        "Destruction/Collection Efficiency (%)",
        joinValues(getValues(item, ["destructioncollectefficiency"])),
      ],
      ["Subject to CAM", joinValues(getValues(item, ["subjecttocam"]))],
      ["PSEU Category", joinValues(getValues(item, ["largeorotherpseu"]))],
      ["Installation Start", item.pdf?.installationStart || joinValues(getValues(item, ["installationstartdate"]).map(formatValue))],
    ],
    stack: [
      ["Stack Height (ft)", joinValues(getValues(item, ["stackheight"]))],
      ["Stack Diameter (ft)", joinValues(getValues(item, ["stackdiameter"]))],
      ["Stack Flow Rate (cfm)", joinValues(getValues(item, ["stackflowrate"]))],
      ["Discharge Temperature (F)", joinValues(getValues(item, ["dischargetemperature"]))],
      ["Flow/Temp Source", joinValues(getValues(item, ["flowratetempinformationsource"]))],
      ["Discharge Direction", joinValues(getValues(item, ["dischargedirection"]))],
    ],
    monitor: [
      ["Manufacturer", getPreferredValue(item, "manufacturer", ["manufacturer"])],
      ["Model", getPreferredValue(item, "model", ["model"])],
      ["Serial Number", joinValues(getValues(item, ["serialnumber"]))],
      ["Parameter Monitored", item.pdf?.parameterMonitored || joinValues(getValues(item, ["parametermonitored"]))],
      ["Primary or Backup", joinValues(getValues(item, ["primaryorbackup"]))],
      ["Bypass Capability", joinValues(getValues(item, ["bypasscapability"]))],
      ["Install Date", item.pdf?.installationStart || joinValues(getValues(item, ["installdate"]).map(formatValue))],
      ["Certification Date", joinValues(getValues(item, ["certificationdate"]).map(formatValue))],
    ],
    fugitive: [
      ["Install Year", joinValues(getValues(item, ["installyear"]).map(formatValue))],
      ["Pollutants Emitted", item.pdf?.pollutantsEmitted || joinValues(getValues(item, ["pollutantsemitted"]))],
    ],
    group: [],
  };

  return [...commonFacts, ...(kindFacts[item.kind] || [])]
    .filter(([, value]) => isPresent(value))
    .map(([label, value]) => ({ label, value }));
};

const getItemRelations = (item) => {
  const itemId = item.displayIdNorm || item.itemIdNorm;
  const designation = normalizeId(item.displayDesignation || item.designation);

  return relationshipRows.filter((relation) => {
    const subjectId = normalizeId(relation.subjectId);
    const relatedId = normalizeId(relation.relatedId);
    const subjectDesignation = normalizeId(relation.subjectDesignation);

    return (
      (itemId && (subjectId === itemId || relatedId === itemId)) ||
      (designation && subjectDesignation === designation)
    );
  });
};

const getRelatedCards = (item, relations) => {
  const itemId = item.itemIdNorm;
  const cards = [];
  const seen = new Set();

  relations.forEach((relation) => {
    const subjectId = normalizeId(relation.subjectId);
    const relatedId = normalizeId(relation.relatedId);
    const counterpartId = subjectId === itemId ? relatedId : subjectId;
    const counterpart = itemById.get(counterpartId) || itemByDesignation.get(counterpartId) || null;
    const key = counterpart ? counterpart.key : `${counterpartId}|${relation.relationship}`;
    if (seen.has(key)) {
      return;
    }
    seen.add(key);

    cards.push(
      counterpart
        ? {
            key: counterpart.key,
            title: counterpart.displayId || counterpart.itemId || counterpart.title,
            subtitle: counterpart.displayDescription || counterpart.description || counterpart.itemType || counterpart.itemId,
            kind: counterpart.kind,
            relation: relation.relationship,
          }
        : {
            key: null,
            title: relation.relatedId || relation.subjectId || "Related item",
            subtitle: relation.relatedType || relation.subjectType || "Referenced in relationships",
            kind: null,
            relation: relation.relationship,
          }
    );
  });

  cards.sort((left, right) => collator.compare(left.title, right.title));
  return cards;
};

const buildRelationRows = (item, relations) => {
  const itemId = item.itemIdNorm;
  return relations
    .map((relation) => {
      const subjectId = normalizeId(relation.subjectId);
      const isSubject = subjectId === itemId;
      return {
        focus: isSubject ? formatValue(relation.relatedId) : formatValue(relation.subjectDesignation || relation.subjectId),
        relationship: formatValue(relation.relationship),
        role: isSubject ? "Related Item" : "Parent/Source",
        type: formatValue(isSubject ? relation.relatedType : relation.subjectType),
        flow: formatValue(relation.percentFlow),
        note: formatValue(relation.note),
      };
    })
    .sort((left, right) => collator.compare(left.focus, right.focus));
};

const EMISSION_COLUMN_CONFIG = [
  { mode: "Emitted", patterns: ["pollutantsemitted"] },
  { mode: "Controlled", patterns: ["pollutantcontrolled"] },
  { mode: "Monitored", patterns: ["parametermonitored"] },
];

const classifySignal = (name, mode) => {
  const key = normalizeKey(name);

  if (
    key.includes("oxygen") ||
    key.includes("opacity") ||
    key.includes("airflow") ||
    key.includes("steamflow") ||
    key.includes("parametric") ||
    key.includes("predictive")
  ) {
    return "Monitoring Parameters";
  }

  if (
    key.includes("co2") ||
    key.includes("carbondioxide") ||
    key.includes("methane") ||
    key.includes("ch4") ||
    key.includes("nitrousoxide") ||
    key.includes("n2o")
  ) {
    return "Greenhouse Gases";
  }

  if (
    key === "co" ||
    key.includes("carbonmonoxide") ||
    key.includes("nitrogenoxides") ||
    key.includes("nox") ||
    key.includes("sulfurdioxide") ||
    key.includes("so2") ||
    key.includes("pm10") ||
    key.includes("pm25") ||
    key.includes("particulatematter") ||
    key.includes("particulate") ||
    key.includes("voc") ||
    key.includes("volatileorganic")
  ) {
    return "Criteria Pollutants";
  }

  if (mode === "Monitored") {
    return "Monitoring Parameters";
  }

  if (
    key.includes("mercury") ||
    key.includes("h2s") ||
    key.includes("benzene") ||
    key.includes("compound") ||
    key.includes("arsenic") ||
    key.includes("cadmium") ||
    key.includes("chromium") ||
    key.includes("beryllium")
  ) {
    return "HAP and Air Toxics";
  }

  return "Other Air Signals";
};

const getCounterpartFromRelation = (item, relation) => {
  const itemId = item.displayIdNorm || item.itemIdNorm;
  const subjectId = normalizeId(relation.subjectId);
  const relatedId = normalizeId(relation.relatedId);
  const counterpartId = subjectId === itemId ? relatedId : subjectId;
  return itemById.get(counterpartId) || itemByDesignation.get(counterpartId) || null;
};

const collectEmissionSignals = (item, relations) => {
  const signals = [];
  const seen = new Set();

  const pushSignals = (sourceItem, sourceLabel, relationLabel) => {
    if (!sourceItem) {
      return;
    }

    sourceItem.rows.forEach(({ row, sheet }) => {
      EMISSION_COLUMN_CONFIG.forEach(({ mode, patterns }) => {
        getValuesByKeyPatterns(row, patterns).forEach((value) => {
          const signal = String(value).trim();
          if (!signal) {
            return;
          }
          const dedupeKey = [
            normalizeKey(signal),
            mode,
            normalizeId(sourceItem.itemId),
            normalize(relationLabel),
          ].join("|");
          if (seen.has(dedupeKey)) {
            return;
          }
          seen.add(dedupeKey);
          signals.push({
            category: classifySignal(signal, mode),
            pollutant: signal,
            mode,
            linkedItem: sourceItem.displayId || sourceItem.itemId || sourceItem.title,
            relationship: relationLabel,
            sourceSheet: sheet,
            sourceLabel,
          });
        });
      });
    });
  };

  pushSignals(item, "Direct", "Direct");

  relations.forEach((relation) => {
    const counterpart = getCounterpartFromRelation(item, relation);
    if (!counterpart) {
      return;
    }
    pushSignals(
      counterpart,
      counterpart.designation || counterpart.itemId || counterpart.title,
      relation.relationship || "Related"
    );
  });

  return signals.sort((left, right) => {
    const categorySort = collator.compare(left.category, right.category);
    if (categorySort !== 0) {
      return categorySort;
    }
    const pollutantSort = collator.compare(left.pollutant, right.pollutant);
    if (pollutantSort !== 0) {
      return pollutantSort;
    }
    return collator.compare(left.linkedItem, right.linkedItem);
  });
};

const renderMeta = () => {
  els.pageTitle.textContent = "Facility SI Details Viewer";
  els.pageSubtitle.textContent =
    "Search subject items and review SI details, emissions context, and Title V permit conditions from the supplied source files.";

  const metaBits = [
    ["Viewer", "Facility SI Details Viewer"],
    ["Source Workbook", data?.sourceFile || "Not available"],
    ["SI Details PDF", data?.pdfSourceFile || "Not available"],
    ["Title V Permit", data?.permitSourceFile || permitData?.sourceFile || "Not available"],
    ["Generated", formatDate(data?.generatedAt) || data?.generatedAt || "Not available"],
  ];

  els.metaDetails.innerHTML = metaBits
    .map(
      ([label, value]) =>
        `<div class="meta-chip"><span>${escapeHtml(label)}</span><strong>${escapeHtml(
          formatValue(value)
        )}</strong></div>`
    )
    .join("");

  const docs = data?.documents || [];
  els.documentLinks.innerHTML = docs.length
    ? docs
        .map(
          (doc) => `<a class="doc-link" href="${escapeHtml(doc.path)}">${escapeHtml(doc.name)}</a>`
        )
        .join("")
    : '<div class="meta-chip"><span>Documents</span><strong>None detected</strong></div>';
};

const renderStats = () => {
  const stats = [
    ["Total Items", categoryCounts.all || 0],
    ["Emission Units", categoryCounts.equipment || 0],
    ["Controls", categoryCounts.control || 0],
    ["Stacks", categoryCounts.stack || 0],
    ["Monitors", categoryCounts.monitor || 0],
    ["Fugitives", categoryCounts.fugitive || 0],
    ["Permit Groups", categoryCounts.group || 0],
    ["Relationships", relationshipRows.length],
  ];

  els.statGrid.innerHTML = stats
    .map(
      ([label, value]) => `
        <div class="stat-card">
          <div class="stat-label">${escapeHtml(label)}</div>
          <div class="stat-value">${escapeHtml(String(value))}</div>
        </div>`
    )
    .join("");
};

const renderFilters = () => {
  const categories = ["all", "equipment", "control", "stack", "monitor", "fugitive", "group"];
  els.categoryFilters.innerHTML = categories
    .map((category) => {
      const active = state.category === category ? " active" : "";
      const count = categoryCounts[category] || 0;
      return `<button type="button" class="filter-chip${active}" data-category="${category}">${escapeHtml(
        CATEGORY_LABELS[category]
      )} (${count})</button>`;
    })
    .join("");

  els.categoryFilters.querySelectorAll("[data-category]").forEach((button) => {
    button.addEventListener("click", () => {
      state.category = button.getAttribute("data-category");
      render();
    });
  });
};

const renderList = (filteredItems) => {
  els.resultCount.textContent = `${filteredItems.length} item${filteredItems.length === 1 ? "" : "s"}`;
  const skipAutoSelect = state.skipAutoSelect;
  state.skipAutoSelect = false;

  if (!filteredItems.length) {
    els.resultList.innerHTML =
      '<div class="empty-state">No matching items for the current search and filter.</div>';
    els.detailPanel.innerHTML =
      '<div class="empty-state">Adjust the search or category filter to find facility records.</div>';
    return;
  }

  if (!filteredItems.some((item) => item.key === state.selectedKey) && !skipAutoSelect) {
    state.selectedKey = filteredItems[0].key;
  }

  els.resultList.innerHTML = filteredItems
    .map((item) => {
      const active = item.key === state.selectedKey ? " active" : "";
      const titleLine = item.displayId || item.itemId || item.title;
      const subtitleLine = item.displayDescription || item.subtitle;
      return `
        <button type="button" class="result-item${active}" data-key="${escapeHtml(item.key)}">
          <div class="result-top">
            <div class="result-title">${escapeHtml(titleLine)}</div>
            <span class="kind-pill ${escapeHtml(KIND_CLASSES[item.kind] || "")}">${escapeHtml(
              CATEGORY_LABELS[item.kind] || item.kind
            )}</span>
          </div>
          <div class="result-subtitle">${escapeHtml(subtitleLine)}</div>
        </button>`;
    })
    .join("");

  els.resultList.querySelectorAll("[data-key]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedKey = button.getAttribute("data-key");
      renderDetail(itemByKey.get(state.selectedKey));
      renderList(filteredItems);
    });
  });
};

const renderFactsCard = (facts) => {
  if (!facts.length) {
    return "";
  }
  return `
    <section class="panel-card">
      <h3>Quick Facts</h3>
      <div class="fact-grid">
        ${facts
          .map(
            (fact) => `
              <div class="fact">
                <div class="fact-label">${escapeHtml(fact.label)}</div>
                <div class="fact-value">${escapeHtml(formatValue(fact.value))}</div>
              </div>`
          )
          .join("")}
      </div>
    </section>`;
};

const renderEmissionCard = (signals) => {
  if (!signals.length) {
    return `
      <section class="panel-card">
        <h3>Emissions Snapshot</h3>
        <p class="panel-note">No emissions-related pollutants or monitoring parameters were found in the supplied records for this item.</p>
      </section>`;
  }

  const categories = [
    "Criteria Pollutants",
    "HAP and Air Toxics",
    "Greenhouse Gases",
    "Monitoring Parameters",
    "Other Air Signals",
  ];

  const rows = categories
    .flatMap((category) => {
      const matches = signals.filter((signal) => signal.category === category);
      if (!matches.length) {
        return [];
      }
      const heading = `
        <tr class="table-section">
          <th colspan="4">${escapeHtml(category)}</th>
        </tr>`;
      const dataRows = matches
        .map(
          (signal) => `
            <tr>
              <td>${escapeHtml(signal.pollutant)}</td>
              <td>${escapeHtml(signal.mode)}</td>
              <td>${escapeHtml(signal.linkedItem)}</td>
              <td>${escapeHtml(formatValue(signal.relationship))}</td>
            </tr>`
        )
        .join("");
      return [heading, dataRows];
    })
    .join("");

  return `
    <section class="panel-card">
      <div class="panel-header">
        <h3>Emissions Snapshot</h3>
        <p class="panel-note">Quantitative PTE rate columns were not present in the supplied workbook/PDF, so this table shows the pollutants and parameters tied to the selected item.</p>
      </div>
      <div class="table-wrap">
        <table class="emissions-table">
          <thead>
            <tr>
              <th>Pollutant / Parameter</th>
              <th>Signal Type</th>
              <th>Linked Item</th>
              <th>Relationship</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      </div>
    </section>`;
};

const renderRelatedCard = (cards) => {
  if (!cards.length) {
    return "";
  }

  return `
    <section class="panel-card">
      <h3>Related Items</h3>
      <div class="related-grid">
        ${cards
          .map(
            (card) => `
              <button
                type="button"
                class="related-card${card.key ? " related-card-link" : ""}"
                ${card.key ? `data-target-key="${escapeHtml(card.key)}"` : "disabled"}
              >
                <span class="related-card-title">${escapeHtml(card.title)}</span>
                <span class="related-card-copy">${escapeHtml(card.subtitle || "No detail available")}</span>
                <span class="detail-meta">
                  ${
                    card.kind
                      ? `<span class="tag">${escapeHtml(CATEGORY_LABELS[card.kind] || card.kind)}</span>`
                      : ""
                  }
                  <span class="tag">${escapeHtml(formatValue(card.relation))}</span>
                </span>
              </button>`
          )
          .join("")}
      </div>
    </section>`;
};

const renderRelationshipCard = (rows) => {
  if (!rows.length) {
    return "";
  }

  return `
    <section class="panel-card">
      <h3>Relationship Map</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Linked Item</th>
              <th>Relationship</th>
              <th>Perspective</th>
              <th>Type</th>
              <th>% Flow</th>
              <th>Note</th>
            </tr>
          </thead>
          <tbody>
            ${rows
              .map(
                (row) => `
                  <tr>
                    <td>${escapeHtml(row.focus)}</td>
                    <td>${escapeHtml(row.relationship)}</td>
                    <td>${escapeHtml(row.role)}</td>
                    <td>${escapeHtml(row.type)}</td>
                    <td>${escapeHtml(row.flow)}</td>
                    <td>${escapeHtml(row.note)}</td>
                  </tr>`
              )
              .join("")}
          </tbody>
        </table>
      </div>
    </section>`;
};

const renderSourceTables = (item) => {
  if (!item.rows.length && item.pdf?.rawValues) {
    const pdfRows = Object.entries(item.pdf.rawValues)
      .filter(([, value]) => value)
      .map(
        ([label, value]) => `
          <tr>
            <th>${escapeHtml(label)}</th>
            <td>${escapeHtml(formatValue(value))}</td>
          </tr>`
      )
      .join("");

    return `
      <section class="panel-card">
        <h3>Source Details</h3>
        <p class="panel-note">PDF source-of-truth record extracted from ${escapeHtml(data?.pdfSourceFile || "the SI details PDF")}.</p>
        <div class="table-wrap">
          <table>
            <tbody>
              ${pdfRows}
            </tbody>
          </table>
        </div>
      </section>`;
  }

  const groups = item.rows.reduce((acc, entry) => {
    if (!acc[entry.sheet]) {
      acc[entry.sheet] = [];
    }
    acc[entry.sheet].push(entry);
    return acc;
  }, {});

  const sections = Object.entries(groups)
    .sort((left, right) => collator.compare(left[0], right[0]))
    .map(([sheet, entries]) => {
      const activeColumns = entries[0].columns.filter((column) =>
        entries.some(({ row }) => isPresent(row[column]))
      );

      return `
        <div class="source-group">
          <h4>${escapeHtml(sheet)}</h4>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  ${activeColumns.map((column) => `<th>${escapeHtml(column)}</th>`).join("")}
                </tr>
              </thead>
              <tbody>
                ${entries
                  .map(
                    ({ row }) => `
                      <tr>
                        ${activeColumns
                          .map((column) => {
                            let value = row[column];
                            if (item.pdf) {
                              if (normalizeKey(column) === "subjectitemid" && item.displayId) {
                                value = item.displayId;
                              } else if (
                                normalizeKey(column) === "subjectitemdesignation" &&
                                item.displayDesignation
                              ) {
                                value = item.displayDesignation;
                              } else if (
                                normalizeKey(column) === "subjectitemdescription" &&
                                item.displayDescription
                              ) {
                                value = item.displayDescription;
                              } else if (
                                normalizeKey(column) === "manufacturer" &&
                                item.pdf.manufacturer
                              ) {
                                value = item.pdf.manufacturer;
                              } else if (normalizeKey(column) === "model" && item.pdf.model) {
                                value = item.pdf.model;
                              }
                            }
                            return `<td>${escapeHtml(formatValue(value))}</td>`;
                          })
                          .join("")}
                      </tr>`
                  )
                  .join("")}
              </tbody>
            </table>
          </div>
        </div>`;
    });

  return `
    <section class="panel-card">
      <h3>Source Details</h3>
      ${sections.join("")}
    </section>`;
};

const formatMultiline = (value) => escapeHtml(String(value || "")).replace(/\n/g, "<br />");

const cleanCitationText = (value) => String(value || "").replace(/\s+/g, " ").trim();

const sortPermitConditions = (conditions) =>
  [...conditions].sort((left, right) => {
    const reqSort = collator.compare(left.requirementNumber || "", right.requirementNumber || "");
    if (reqSort !== 0) {
      return reqSort;
    }
    return (left.page || 0) - (right.page || 0);
  });

const renderAppendixExcerpts = (condition) => {
  const excerpts = (condition.appendixRefs || [])
    .map((appendixId) => appendixExcerptById.get(String(appendixId || "").toUpperCase()))
    .filter(Boolean);

  if (!excerpts.length) {
    return "";
  }

  return `
    <div class="appendix-list">
      ${excerpts
        .map(
          (excerpt) => `
            <details class="appendix-detail">
              <summary>${escapeHtml(excerpt.title)}${excerpt.page ? ` • Page ${escapeHtml(String(excerpt.page))}` : ""}</summary>
              <div class="appendix-copy">${formatMultiline(excerpt.excerpt)}</div>
            </details>`
        )
        .join("")}
    </div>`;
};

const renderConditionCards = (conditions, badgeLabel) => {
  if (!conditions.length) {
    return '<p class="panel-note">No conditions found.</p>';
  }

  return `
    <div class="condition-list">
      ${sortPermitConditions(conditions)
        .map(
          (condition) => `
            <article class="condition-card">
              <div class="condition-head">
                <div>
                  <div class="condition-number">${escapeHtml(condition.requirementNumber || "Requirement")}</div>
                  <div class="condition-meta">Section ${escapeHtml(condition.section || "-")}${condition.page ? ` • Page ${escapeHtml(String(condition.page))}` : ""}</div>
                </div>
                <span class="tag">${escapeHtml(badgeLabel)}</span>
              </div>
              <div class="condition-copy">${formatMultiline(condition.text)}</div>
              ${
                condition.citation
                  ? `<div class="condition-citation">${escapeHtml(condition.citation)}</div>`
                  : ""
              }
              ${renderAppendixExcerpts(condition)}
            </article>`
        )
        .join("")}
    </div>`;
};

const renderPermitGroupSection = ({ title, badgeLabel, conditions, note, open = false }) => {
  const count = conditions.length;
  return `
    <details class="permit-section" ${open ? "open" : ""}>
      <summary>
        <span>${escapeHtml(title)}</span>
        <span class="permit-section-meta">${escapeHtml(String(count))} condition${count === 1 ? "" : "s"}</span>
      </summary>
      <div class="permit-section-body">
        ${note ? `<p class="panel-note">${escapeHtml(note)}</p>` : ""}
        ${renderConditionCards(conditions, badgeLabel)}
      </div>
    </details>`;
};

const getPermitProfile = (item) => {
  const itemId = item.displayIdNorm || item.itemIdNorm;
  const directConditions = sortPermitConditions(permitConditionsByItem.get(itemId) || []);
  const inheritedGroupIds = permitComgMemberships?.members?.[itemId] || [];
  const inheritedGroups = inheritedGroupIds
    .map((groupId) => {
      const groupItem = permitItemById.get(groupId) || permitComgMemberships?.groups?.[groupId] || null;
      return {
        itemId: groupId,
        title: groupItem?.title || groupId,
        page: groupItem?.page || null,
        conditions: sortPermitConditions(permitConditionsByItem.get(groupId) || []),
      };
    })
    .filter((group) => group.conditions.length);

  const inheritedSet = new Set(inheritedGroupIds.map(normalizeId));
  const referencedMap = new Map();
  directConditions.forEach((condition) => {
    (condition.referencedIds || []).forEach((referencedId) => {
      const normalizedRef = normalizeId(referencedId);
      if (!normalizedRef || normalizedRef === itemId || inheritedSet.has(normalizedRef)) {
        return;
      }
      if (!referencedMap.has(normalizedRef)) {
        const permitItem = permitItemById.get(normalizedRef) || null;
        referencedMap.set(normalizedRef, {
          itemId: normalizedRef,
          title: permitItem?.title || normalizedRef,
          page: permitItem?.page || null,
          via: new Set(),
          conditions: sortPermitConditions(permitConditionsByItem.get(normalizedRef) || []),
        });
      }
      referencedMap.get(normalizedRef).via.add(condition.requirementNumber);
    });
  });

  const referencedGroups = Array.from(referencedMap.values()).filter((entry) => entry.conditions.length);
  const groupMembers = permitComgMemberships?.groups?.[itemId]?.members || [];

  return {
    directConditions,
    inheritedGroups,
    referencedGroups,
    groupMembers,
  };
};

const renderPermitMembers = (memberIds) => {
  if (!memberIds.length) {
    return "";
  }

  return `
    <div class="permit-members">
      <div class="fact-label">Group Members</div>
      <div class="permit-chip-row">
        ${memberIds
          .map((memberId) => {
            const target = itemById.get(normalizeId(memberId));
            const label = target?.displayId || memberId;
            if (target) {
              return `<button type="button" class="permit-nav-chip" data-target-key="${escapeHtml(target.key)}">${escapeHtml(label)}</button>`;
            }
            return `<span class="tag">${escapeHtml(label)}</span>`;
          })
          .join("")}
      </div>
    </div>`;
};

const getFederalStandardLabel = (part, subpart) => {
  const code = String(subpart || "").toUpperCase();
  const labels = {
    "60:A": "40 CFR Part 60, Subpart A (NSPS General Provisions)",
    "60:D": "40 CFR Part 60, Subpart D (NSPS Fossil-Fuel-Fired Steam Generators)",
    "60:DB": "40 CFR Part 60, Subpart Db (NSPS Industrial-Commercial-Institutional Steam Generating Units)",
    "63:A": "40 CFR Part 63, Subpart A (MACT General Provisions)",
    "63:DDDDD": "40 CFR Part 63, Subpart DDDDD (Boiler MACT)",
  };
  return labels[`${part}:${code}`] || `40 CFR Part ${part}, Subpart ${code}`;
};

const STATE_STANDARD_LABELS = {
  "MINN. R. 7011.0010": "Applicability of Standards of Performance",
  "MINN. R. 7011.0050": "General Provisions of Federal Standards Incorporated by Reference",
  "MINN. R. 7011.0060": "Definitions",
  "MINN. R. 7011.0075": "Listed Control Equipment General Requirements",
  "MINN. R. 7011.0080": "Monitoring and Record Keeping for Listed Control Equipment",
  "MINN. R. 7011.0105": "Visible Emissions; Restrictions for Existing Facilities",
  "MINN. R. 7011.0110": "Visible Emissions; Restrictions for New Facilities",
  "MINN. R. 7011.0150": "Preventing Particulate Matter From Becoming Airborne",
  "MINN. R. 7011.0555":
    "Incorporation by Reference; New Source Performance Standards; Fossil-Fuel-Fired Steam Generators",
  "MINN. R. 7011.0565":
    "Incorporation by Reference; New Source Performance Standards; Steam Generating Units",
  "MINN. R. 7011.0605": "Determining Applicable Standards of Performance",
  "MINN. R. 7011.0610": "Performance Standards; Fossil-Fuel-Burning Direct Heating Equipment",
  "MINN. R. 7011.0715": "Standards of Performance for Post-1969 Industrial Process Equipment",
  "MINN. R. 7011.0730": "Industrial Process Equipment - Table 1",
  "MINN. R. 7011.0735": "Industrial Process Equipment - Table 2",
  "MINN. R. 7011.1005": "Standards of Performance for Dry Bulk Agricultural Commodity Facilities",
  "MINN. R. 7011.1110": "Standards of Performance for Existing Outstate Coal Handling Facilities",
  "MINN. R. 7011.1125": "Ceasing Operations; Wind",
  "MINN. R. 7011.7050":
    "Incorporation by Reference; Emission Standards; Industrial, Commercial, and Institutional Boilers and Process Heaters; Major Sources",
};

const getStateStandardLabel = (citation) =>
  STATE_STANDARD_LABELS[String(citation || "").toUpperCase()] || String(citation || "");

const inferFederalStandardKey = (citation) => {
  const cleaned = cleanCitationText(citation);
  const explicitSubpart = cleaned.match(/40 CFR (?:pt\.|Part)\s*(60|63),?\s*subp\.?\s*([A-Z0-9]+)/i);
  if (explicitSubpart) {
    const part = explicitSubpart[1];
    const subpart = explicitSubpart[2].toUpperCase();
    return {
      key: `federal:${part}:${subpart}`,
      label: getFederalStandardLabel(part, subpart),
      citation: explicitSubpart[0],
      group: "Federal",
    };
  }

  const section60 = cleaned.match(/40 CFR\s+60\.(\d+[A-Za-z]?)/i);
  if (section60) {
    const token = section60[1];
    const numeric = Number.parseInt(token, 10);
    const suffix = token.replace(String(numeric), "").toUpperCase();
    if (suffix === "B" && numeric >= 40 && numeric <= 49) {
      return {
        key: "federal:60:DB",
        label: getFederalStandardLabel("60", "DB"),
        citation: `40 CFR 60.${token}`,
        group: "Federal",
      };
    }
    if (!suffix && numeric >= 40 && numeric <= 49) {
      return {
        key: "federal:60:D",
        label: getFederalStandardLabel("60", "D"),
        citation: `40 CFR 60.${token}`,
        group: "Federal",
      };
    }
    if (!suffix && numeric >= 1 && numeric <= 19) {
      return {
        key: "federal:60:A",
        label: getFederalStandardLabel("60", "A"),
        citation: `40 CFR 60.${token}`,
        group: "Federal",
      };
    }
  }

  const section63 = cleaned.match(/40 CFR\s+63\.(\d+[A-Za-z]?)/i);
  if (section63) {
    const token = section63[1];
    const numeric = Number.parseInt(token, 10);
    if (numeric >= 7500 && numeric < 7600) {
      return {
        key: "federal:63:DDDDD",
        label: getFederalStandardLabel("63", "DDDDD"),
        citation: `40 CFR 63.${token}`,
        group: "Federal",
      };
    }
    if (numeric >= 1 && numeric <= 16) {
      return {
        key: "federal:63:A",
        label: getFederalStandardLabel("63", "A"),
        citation: `40 CFR 63.${token}`,
        group: "Federal",
      };
    }
  }

  return null;
};

const collectApplicablePerformanceStandards = (permitProfile) => {
  const standards = new Map();

  const registerStandard = (entry, sourceLabel) => {
    if (!entry?.key) {
      return;
    }
    if (!standards.has(entry.key)) {
      standards.set(entry.key, {
        key: entry.key,
        label: entry.label,
        group: entry.group,
        citations: new Set(),
        sources: new Set(),
      });
    }
    const target = standards.get(entry.key);
    if (entry.citation) {
      target.citations.add(cleanCitationText(entry.citation));
    }
    if (sourceLabel) {
      target.sources.add(sourceLabel);
    }
  };

  const scanConditions = (conditions, sourceLabel) => {
    conditions.forEach((condition) => {
      const body = cleanCitationText(`${condition.citation || ""} ${condition.text || ""}`);

      const stateMatches = body.match(/Minn\. R\. 7011\.\d+(?:\.\d+)?/gi) || [];
      stateMatches.forEach((match) =>
        registerStandard(
          {
            key: `state:${match.toUpperCase()}`,
            label: getStateStandardLabel(match),
            citation: match,
            group: "State",
          },
          sourceLabel
        )
      );

      const federalCitations = new Set();
      const explicitMatches = [
        ...body.matchAll(/40 CFR (?:pt\.|Part)\s*(60|63),?\s*subp\.?\s*([A-Z0-9]+)/gi),
        ...body.matchAll(/40 CFR\s+(60|63)\.(\d+[A-Za-z]?)/gi),
      ];
      explicitMatches.forEach((match) => federalCitations.add(match[0]));
      federalCitations.forEach((citation) => {
        const inferred = inferFederalStandardKey(citation);
        if (!inferred) {
          return;
        }
        registerStandard(
          {
            ...inferred,
          },
          sourceLabel
        );
      });
    });
  };

  scanConditions(permitProfile.directConditions, "Direct");
  permitProfile.inheritedGroups.forEach((group) =>
    scanConditions(group.conditions, `Inherited ${group.itemId}`)
  );
  permitProfile.referencedGroups.forEach((group) =>
    scanConditions(group.conditions, `Referenced ${group.itemId}`)
  );

  return {
    federal: Array.from(standards.values())
      .filter((entry) => entry.group === "Federal")
      .sort((left, right) => collator.compare(left.label, right.label)),
    state: Array.from(standards.values())
      .filter((entry) => entry.group === "State")
      .sort((left, right) => collator.compare(left.label, right.label)),
  };
};

const renderPerformanceStandardGroup = (title, entries) => {
  if (!entries.length) {
    return `
      <div class="standards-group">
        <h4>${escapeHtml(title)}</h4>
        <p class="panel-note">No ${escapeHtml(title.toLowerCase())} performance standards were identified from the applicable permit citations.</p>
      </div>`;
  }

  return `
    <div class="standards-group">
      <h4>${escapeHtml(title)}</h4>
      <div class="standards-list">
        ${entries
          .map(
            (entry) => `
              <article class="standard-card">
                <div class="standard-title">${escapeHtml(entry.label)}</div>
                <div class="standard-meta">${escapeHtml(Array.from(entry.citations).sort((left, right) => collator.compare(left, right)).join("; "))}</div>
                <div class="permit-chip-row">
                  ${Array.from(entry.sources)
                    .sort((left, right) => collator.compare(left, right))
                    .map((source) => `<span class="tag">${escapeHtml(source)}</span>`)
                    .join("")}
                </div>
              </article>`
          )
          .join("")}
      </div>
    </div>`;
};

const renderPerformanceStandardsCard = (permitProfile) => {
  const standards = collectApplicablePerformanceStandards(permitProfile);
  const totalCount = standards.federal.length + standards.state.length;

  return `
    <section class="panel-card">
      <div class="panel-header">
        <h3>Applicable Performance Standards</h3>
        <p class="panel-note">Quick-reference summary of state and federal performance standards identified from the applicable Title V citations. Generic authority citations such as Minn. R. 7007.0800 are excluded.</p>
      </div>
      ${
        totalCount
          ? `<p class="panel-note">Identified ${escapeHtml(String(totalCount))} performance standard${totalCount === 1 ? "" : "s"} across direct, inherited, and referenced permit conditions.</p>`
          : '<p class="panel-note">No Minn. R. 7011, 40 CFR Part 60 NSPS, or 40 CFR Part 63 MACT standards were identified from the applicable permit citations.</p>'
      }
      <div class="standards-grid">
        ${renderPerformanceStandardGroup("Federal Standards", standards.federal)}
        ${renderPerformanceStandardGroup("State Standards", standards.state)}
      </div>
    </section>`;
};

const renderPermitConditionsCard = (item) => {
  const permitProfile = getPermitProfile(item);
  const hasDirectPermitItem = Boolean(item.permitItem);
  const noPermitMatch =
    !hasDirectPermitItem &&
    !permitProfile.directConditions.length &&
    !permitProfile.inheritedGroups.length &&
    !permitProfile.referencedGroups.length;

  if (noPermitMatch) {
    return `
      <section class="panel-card">
        <h3>Permit Conditions</h3>
        <p class="panel-note">No current Title V subject-item section was found for this item in ${escapeHtml(
          data?.permitSourceFile || permitData?.sourceFile || "the Title V permit"
        )}. Workbook notes and SI details remain visible above.</p>
      </section>`;
  }

  return `
    <section class="panel-card">
      <div class="panel-header">
        <h3>Permit Conditions</h3>
        <p class="panel-note">Conditions are grouped by direct applicability, COMG inheritance, and explicit permit cross-references. Expand only the sections you need.</p>
      </div>
      ${renderPermitMembers(permitProfile.groupMembers)}
      ${renderPermitGroupSection({
        title: "Direct Conditions",
        badgeLabel: "Direct",
        conditions: permitProfile.directConditions,
        open: true,
      })}
      ${
        permitProfile.inheritedGroups
          .map(
            (group) =>
              renderPermitGroupSection({
                title: `Inherited via ${group.itemId}${group.title ? `: ${group.title}` : ""}`,
                badgeLabel: `Inherited from ${group.itemId}`,
                conditions: group.conditions,
              })
          )
          .join("")
      }
      ${
        permitProfile.referencedGroups
          .map(
            (group) =>
              renderPermitGroupSection({
                title: `Referenced ${group.itemId}${group.title ? `: ${group.title}` : ""}`,
                badgeLabel: `Referenced via ${item.displayId || item.itemId}`,
                conditions: group.conditions,
                note: `Referenced by ${Array.from(group.via)
                  .sort((left, right) => collator.compare(left, right))
                  .join(", ")}.`,
              })
          )
          .join("")
      }
    </section>`;
};

const renderDetailTabs = (item, overviewContent, permitContent, permitCount) => {
  const hasPermitContent = Boolean(item.permitItem) || permitCount > 0;
  if (!hasPermitContent) {
    return overviewContent;
  }

  return `
    <section class="detail-tabs">
      <div class="detail-tab-bar">
        <button type="button" class="detail-tab-button${
          state.detailTab === "overview" ? " active" : ""
        }" data-detail-tab="overview">Overview</button>
        <button type="button" class="detail-tab-button${
          state.detailTab === "permit" ? " active" : ""
        }" data-detail-tab="permit">Permit Conditions (${escapeHtml(String(permitCount))})</button>
      </div>
      <div class="detail-tab-panel${state.detailTab === "overview" ? " active" : ""}" data-detail-panel="overview">
        ${overviewContent}
      </div>
      <div class="detail-tab-panel${state.detailTab === "permit" ? " active" : ""}" data-detail-panel="permit">
        ${permitContent}
      </div>
    </section>`;
};

const renderDetail = (item) => {
  if (!item) {
    els.detailPanel.innerHTML =
      '<div class="empty-state">Select a record to review facility details and related subject items.</div>';
    return;
  }

  const facts = buildFacts(item);
  const relations = getItemRelations(item);
  const relatedCards = getRelatedCards(item, relations);
  const relationRows = buildRelationRows(item, relations);
  const emissionSignals = collectEmissionSignals(item, relations);
  const permitProfile = getPermitProfile(item);
  const permitCount =
    permitProfile.directConditions.length +
    permitProfile.inheritedGroups.reduce((sum, group) => sum + group.conditions.length, 0) +
    permitProfile.referencedGroups.reduce((sum, group) => sum + group.conditions.length, 0);
  const detailTags = [
    item.kind ? CATEGORY_LABELS[item.kind] : null,
    item.displayDesignation ? `Delta designation: ${item.displayDesignation}` : null,
    item.pdf?.page ? `PDF page: ${item.pdf.page}` : null,
    item.permitItem?.page ? `Title V page: ${item.permitItem.page}` : null,
    `${item.rows.length} source row${item.rows.length === 1 ? "" : "s"}`,
  ].filter(Boolean);

  const overviewContent = `
    <div class="detail-grid">
      ${renderFactsCard(facts)}
      ${renderPerformanceStandardsCard(permitProfile)}
      ${renderSourceTables(item)}
      ${renderEmissionCard(emissionSignals)}
      ${renderRelatedCard(relatedCards)}
      ${renderRelationshipCard(relationRows)}
    </div>`;

  const permitContent = `
    <div class="detail-grid">
      ${renderPermitConditionsCard(item)}
    </div>`;

  els.detailPanel.innerHTML = `
    <section class="detail-header">
      <div>
        <h2>${escapeHtml(item.displayId || item.itemId || item.title)}</h2>
        <p class="detail-sub">${escapeHtml(item.displayDescription || item.subtitle)}</p>
        <div class="detail-meta">
          ${detailTags.map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}
        </div>
      </div>
    </section>
    ${renderDetailTabs(item, overviewContent, permitContent, permitCount)}`;

  els.detailPanel.querySelectorAll("[data-detail-tab]").forEach((button) => {
    button.addEventListener("click", () => {
      state.detailTab = button.getAttribute("data-detail-tab") || "overview";
      renderDetail(item);
    });
  });

  els.detailPanel.querySelectorAll("[data-target-key]").forEach((button) => {
    button.addEventListener("click", () => {
      const targetKey = button.getAttribute("data-target-key");
      if (!targetKey || !itemByKey.has(targetKey)) {
        return;
      }
      state.query = "";
      state.category = "all";
      state.selectedKey = targetKey;
      state.skipAutoSelect = true;
      if (els.searchInput) {
        els.searchInput.value = "";
      }
      state.detailTab = "overview";
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
};

const render = () => {
  renderFilters();
  const filteredItems = getFilteredItems();
  renderList(filteredItems);
  renderDetail(itemByKey.get(state.selectedKey));
};

if (!data || !Array.isArray(data.sections)) {
  els.detailPanel.innerHTML =
    '<div class="empty-state">Data file not loaded. Run `python build_data.py` first.</div>';
} else {
  renderMeta();
  renderStats();
  render();
}

els.searchInput.addEventListener("input", (event) => {
  state.query = event.target.value.trim();
  render();
});

els.printPage.addEventListener("click", () => window.print());
