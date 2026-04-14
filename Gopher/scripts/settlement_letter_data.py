from __future__ import annotations

SETTLEMENT_SOURCE_NOTE = (
    "AQMD file named '2025-06-25 Global Settlement Letter for Ecobat.pdf'; "
    "letter text is dated June 12, 2025."
)


SETTLEMENT_BY_NOTICE = {
    "P79157": {
        "response": (
            "SCAQMD rejected Ecobat's claim that the missed sample was beyond facility control. "
            "It said contractor / employee error and the attempted restart without a filter did not excuse noncompliance. "
            "For source testing, SCAQMD said the test was plainly late and the February 2022 test used the wrong contaminant; "
            "for late report submissions, it said Ecobat did not justify the delay or seek a variance."
        ),
        "offered_penalty": (
            "$22,500 visible subtotal: $3,000 missed sampling + $5,000 source testing + "
            "$14,500 late report submissions. No penalty stated for alleged 1420.1(j)(6) and 1420.1(k)(4)."
        ),
    },
    "P79172": {
        "response": (
            "SCAQMD rejected Ecobat's monitor-error and no-fugitive-emissions defenses for furnace and enclosure pressure data, "
            "stating no cited exception excused the readings and that monitor issues would undermine all 2022 data. "
            "It said the existing Title V permit limits remain enforceable unless formally revised, so Ecobat's draft-permit / "
            "E51.1 arguments did not defeat the C89 pH allegation. SCAQMD accepted compliance only for the C40 pH allegation "
            "while SOx CEMS was in full operation and for one alleged federal WESP packed-bed flow allegation, but otherwise said "
            "Ecobat had not shown timely kiln cleanout or compliance with the cited pressure / pH / water-flow requirements."
        ),
        "offered_penalty": (
            "$641,500 visible component subtotal: $520,000 furnace DP + $62,000 total enclosure DP + "
            "$40,000 C89 pH + $5,000 rotary dryer build-up + $14,500 WESP packed-bed scrubber water flow. "
            "Compliance only stated for C40 pH and one alleged federal WESP packed-bed flow allegation. "
            "This subtotal is an inference from visible line items in the letter."
        ),
    },
    "P76003": {
        "response": (
            "SCAQMD said the Q2 and Q3 2022 QCER correction reports were submitted nearly six months late, "
            "and treated the matter as the same type of Rule 2004 reporting violation resolved in prior settlement."
        ),
        "offered_penalty": "$12,500.",
    },
    "P79476": {
        "response": (
            "SCAQMD said the Q1 2023 QCER correction report was submitted nearly three months late and treated it "
            "as a repeat Rule 2004 reporting violation."
        ),
        "offered_penalty": "$7,000; letter says the penalty was heightened for the repeat nature of the violation.",
    },
    "P68909": {
        "response": (
            "SCAQMD described the NOV as a failure to report breakdown / notify after unplanned shutdown of ECDs under "
            "Rules 430, 1420.1(n), and Title V permit conditions, but for this global offer it said it was willing to accept compliance only."
        ),
        "offered_penalty": "Compliance only; no monetary penalty stated.",
    },
    "P69321": {
        "response": "Not addressed in the June 12, 2025 global settlement letter.",
        "offered_penalty": "Not addressed.",
    },
    "P69327": {
        "response": "Not addressed in the June 12, 2025 global settlement letter.",
        "offered_penalty": "Not addressed.",
    },
}
