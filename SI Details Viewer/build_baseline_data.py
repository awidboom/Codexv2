import json
from datetime import datetime

import pandas as pd

from shared_config import BASE_DIR, load_config, resolve_baseline_workbook

OUTPUT_FILE = BASE_DIR / "static" / "baseline.js"


def normalize_header(value):
    return " ".join(str(value or "").strip().lower().split())


def build_reference_map(data_file):
    ref = pd.read_excel(data_file, sheet_name="References - PTE", header=None, engine="openpyxl")
    mapping = {}
    for _, row in ref.iterrows():
        first = row.iloc[0]
        second = row.iloc[1]
        if isinstance(first, (int, float)) and not pd.isna(first) and isinstance(second, str) and second.strip():
            mapping[str(int(first))] = second.strip()
    return mapping


def load_segments(data_file):
    df = pd.read_excel(data_file, sheet_name="PTE - Segment Emissions Calcs", header=5, engine="openpyxl")
    columns = {normalize_header(column): column for column in df.columns}

    def get_col(name):
        return columns.get(normalize_header(name))

    def to_float(value):
        if value is None or pd.isna(value):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        try:
            return float(str(value).replace(",", "").strip())
        except ValueError:
            return None

    rows = []
    for _, row in df.iterrows():
        equi = row.get(get_col("TEMPO EQUI #"))
        if pd.isna(equi):
            equi = row.get(get_col("TEMPO EQUI # Lookup"))
        if pd.isna(equi):
            equi = row.get(get_col("TEMPO SEG VLOOKUP"))
        if pd.isna(equi):
            continue

        equi_str = str(equi).strip()
        if equi_str:
            equi_str = equi_str.split("-")[0].strip()

        source = row.get(get_col("Emission Factor Source"))
        ef_ref = row.get(get_col("EF Reference"))
        ef_source_id = None
        if isinstance(source, (int, float)) and not pd.isna(source):
            ef_source_id = str(int(source))
        elif isinstance(ef_ref, (int, float)) and not pd.isna(ef_ref):
            ef_source_id = str(int(ef_ref))

        rows.append(
            {
                "equiId": equi_str,
                "equiIdNorm": equi_str.replace(" ", "").upper(),
                "seg": row.get(get_col("Seg")),
                "segDescription": row.get(get_col("Seg Description")),
                "sourceCategory": row.get(get_col("Source Category")),
                "pollutant": row.get(get_col("Pollutant")),
                "emissionFactor": row.get(get_col("Emission Factor (lb/unit)")),
                "emissionFactorUnit": row.get(get_col("Emission Factor Unit")),
                "emissionFactorSource": source,
                "efReference": ef_ref,
                "efSourceId": ef_source_id,
                "throughput": row.get(get_col("Throughput (unit/hr)")),
                "throughputUnits": row.get(get_col("Throughput Units")),
                "hourlyPotentialLbHr": to_float(row.get(get_col("Hourly Potential Emissions (lb/hr)"))),
                "limitedPotentialTpy": to_float(row.get(get_col("Limited Potential Emissions (tpy)"))),
                "controlEfficiency": row.get(get_col("Pollution Control Efficiency (%)")),
                "tempoStru": row.get(get_col("TEMPO STRU #")),
                "tempoTrea": row.get(get_col("TEMPO TREA #")),
                "deltaSv": row.get(get_col("DELTA SV #")),
            }
        )
    return rows


def write_payload(payload):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as handle:
        handle.write("window.BASELINE_PTE = ")
        if payload is None:
            handle.write("null;\n")
        else:
            json.dump(payload, handle, ensure_ascii=True, indent=2)
            handle.write(";\n")


def main():
    config = load_config()
    try:
        data_file = resolve_baseline_workbook(config)
        payload = {
            "generatedAt": datetime.now().isoformat(timespec="seconds"),
            "facilityName": config.get("facility_name"),
            "baselineTitle": config.get("baseline_title"),
            "sourceFile": data_file.name,
            "references": build_reference_map(data_file),
            "segments": load_segments(data_file),
        }
    except FileNotFoundError:
        payload = None

    write_payload(payload)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
