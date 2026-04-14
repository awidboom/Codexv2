from __future__ import annotations

AQMD_NOV_SUMMARY_HEADERS = [
    "Notice",
    "Violation Date",
    "Issue Date",
    "Status",
    "Rules",
    "Violation Description",
    "Ecobat Response Summary",
    "SCAQMD Response (Global Settlement Letter)",
    "Offered Penalty (Global Settlement Letter)",
]


AQMD_NOV_SUMMARY_ROWS = [
    {
        "notice": "P79172",
        "violation_date": "2022-01-01",
        "issue_date": "2024-02-29",
        "status": "NOV",
        "rules": "1420.1(f)(3); Rule 221(b)",
        "violation_description": "Furnace differential pressure for D84 and D8 allegedly exceeded the -0.02 inches water column requirement across 2022.",
        "ecobat_response": (
            "Ecobat acknowledged readings above -0.02 but argued they were largely caused by plugged monitor tubes and communication errors, "
            "not actual pressure loss. It said both furnaces still showed draft below zero for nearly all averaging blocks, any draft routed "
            "emissions to downstream controls, ambient monitors did not show increases, and added second monitors, alarms, and staff training."
        ),
        "scaqmd_response": (
            "SCAQMD rejected the monitor-issue defense, said no cited exception excused the over-4,000 non-compliant readings, and said "
            "Rule 218.2 did not apply. It also said Ecobat's argument called the reliability of all 2022 readings into question and asked why "
            "corrective action was not taken sooner."
        ),
        "offered_penalty": "$520,000.",
    },
    {
        "notice": "P79172",
        "violation_date": "2022-01-01",
        "issue_date": "2024-02-29",
        "status": "NOV",
        "rules": "1420.1(e)(3); 40 CFR 63.544(c)(1); Rule 3002(c)(1); Permit E448.5",
        "violation_description": "Total enclosure negative pressure and missing DPM data for 2022 building enclosure monitors.",
        "ecobat_response": (
            "Ecobat argued that a single monitor reading was insufficient to show building-wide loss of negative pressure, and said the permanent "
            "enclosure and Busch units make localized positive pressure unlikely. It attributed many events to monitor or communications faults "
            "or localized effects rather than enclosure-wide noncompliance."
        ),
        "scaqmd_response": (
            "SCAQMD said each DPM can demonstrate noncompliance with the enclosure standard, assumed the readings were accurate for settlement, "
            "and said the records showed the required limits were not maintained, including an hour with no DPM data at all."
        ),
        "offered_penalty": "$62,000.",
    },
    {
        "notice": "P76003",
        "violation_date": "2022-04-01",
        "issue_date": "2023-10-13",
        "status": "In Compliance",
        "rules": "Rule 2004(e)",
        "violation_description": "Quarter 2 and Quarter 3 QCERs allegedly contained inaccurate emissions and correction reports were not timely submitted.",
        "ecobat_response": (
            "Ecobat said the Q2 error came from an incorrect meter reading for Rule 2019 exempt-equipment natural gas use and understated usage by "
            "about 0.3 percent. It said the Q3 error came from a later-discovered gasoline receipt affecting exempt-equipment gasoline use by less "
            "than 0.02 percent, that both errors were voluntarily corrected once discovered, and that staff were retrained."
        ),
        "scaqmd_response": (
            "SCAQMD characterized the matter as failure to submit corrected QCERs within the reconciliation period and treated it as the same type "
            "of Rule 2004 reporting violation resolved in prior settlement."
        ),
        "offered_penalty": "$12,500.",
    },
    {
        "notice": "P80830",
        "violation_date": "2023-01-01",
        "issue_date": "2024-06-21",
        "status": "NOV",
        "rules": "Rule 221(b); 1420.1(e)(3), (f)(3); 40 CFR 63.544; Rule 3002(c)(1)",
        "violation_description": "Grouped pressure-related allegations, including furnace differential pressure, enclosure negative pressure, and related duplicate rule citations.",
        "ecobat_response": (
            "Ecobat said it identified only limited periods of concern, many during rebuilds, downtime, or when furnaces were not operating. It "
            "argued many readings reflected monitor or network issues, not actual pressure loss, and said the November 7, 2023 enclosure event was "
            "a single 15-minute period during rebuild. It also criticized the NOV for broad date ranges and lack of specificity."
        ),
        "scaqmd_response": "Not addressed in the June 12, 2025 global settlement letter located in the AQMD folder.",
        "offered_penalty": "Not addressed.",
    },
    {
        "notice": "P80830",
        "violation_date": "2023-01-01",
        "issue_date": "2024-06-21",
        "status": "NOV",
        "rules": "1420.1(h)(2)",
        "violation_description": "Alleged failure to repair gaps, breaks, or separations in the total enclosure within 72 hours of discovery.",
        "ecobat_response": (
            "Ecobat said the 'King Kong' door gap identified on May 3, 2024 was repaired on May 6 within 72 hours, and an additional bottom gap "
            "discovered during that repair was fixed on May 7 within 72 hours of that later discovery."
        ),
        "scaqmd_response": "Not addressed in the June 12, 2025 global settlement letter located in the AQMD folder.",
        "offered_penalty": "Not addressed.",
    },
    {
        "notice": "P80830",
        "violation_date": "2023-01-01",
        "issue_date": "2024-06-21",
        "status": "NOV",
        "rules": "Permit C6.2, C6.3, D11.3, D12.8; Device C161 temperature limit",
        "violation_description": "Grouped temperature-limit allegations for C39, C88, C21, D3, C182, and C161.",
        "ecobat_response": (
            "Ecobat said the cited temperature limits were not actually exceeded and that some data gaps occurred during rebuilds, furnace downtime, "
            "or instrumentation / data interruptions rather than high-temperature operation."
        ),
        "scaqmd_response": "Not addressed in the June 12, 2025 global settlement letter located in the AQMD folder.",
        "offered_penalty": "Not addressed.",
    },
    {
        "notice": "P80830",
        "violation_date": "2023-01-01",
        "issue_date": "2024-06-21",
        "status": "NOV",
        "rules": "Permit C8.1, C8.2, C8.3, C8.6, D12.16; 40 CFR 63.548i",
        "violation_description": "Grouped scrubber / WESP chemistry, flow, and voltage allegations, including pH, water flow, and WESP cell average voltage.",
        "ecobat_response": (
            "Ecobat argued some permit conditions are outdated or overly restrictive, referenced draft permit revisions lowering certain pH limits, "
            "and said many low pH / flow / voltage readings occurred during downtime, rebuilds, or monitoring anomalies without corresponding ambient "
            "or stack evidence of excess emissions."
        ),
        "scaqmd_response": "Not addressed in the June 12, 2025 global settlement letter located in the AQMD folder.",
        "offered_penalty": "Not addressed.",
    },
    {
        "notice": "P80830",
        "violation_date": "2023-01-01",
        "issue_date": "2024-06-21",
        "status": "NOV",
        "rules": "Rule 1110.2; visible emissions; multi-metal CEMS reporting; Rule 3002(c)(1)",
        "violation_description": "Grouped reporting, visible emissions, multi-metal CEMS, and general compliance allegations.",
        "ecobat_response": (
            "Ecobat said some allegations lacked meaningful dates and units, some were duplicative of earlier notices, and some were factually inaccurate. "
            "It acknowledged the Q2 2023 engine quarterly report appears to have been submitted one day late but said that delay caused no emission exceedance "
            "or operating-limit breach."
        ),
        "scaqmd_response": "Not addressed in the June 12, 2025 global settlement letter located in the AQMD folder.",
        "offered_penalty": "Not addressed.",
    },
    {
        "notice": "P79157",
        "violation_date": "2023-06-07",
        "issue_date": "2024-02-29",
        "status": "In Compliance",
        "rules": "Rule 1420.1(j)(2)(A), (j)(2)(B), (j)(6)",
        "violation_description": "Missed valid 24-hour lead and arsenic samples on April 12, 2023 and alleged failure to operate ambient monitoring equipment in accordance with EPA methods.",
        "ecobat_response": (
            "Ecobat said only monitor 2D failed, all other fence-line monitors operated, and the failure was caused by a backup Kleinfelder technician "
            "who did not enter the start date correctly. It argued the event qualified as a beyond-control monitor malfunction under Rule 1420.1(j)(2)(C), "
            "that timely notice was given, that no second missed day occurred, and that timer mis-setting is an inherent source of error under Appendix B."
        ),
        "scaqmd_response": (
            "SCAQMD rejected the beyond-control argument, saying contractor and employee errors did not excuse the missed sample and the no-filter restart "
            "did not comply with regulatory standards. It considered the missed sample significant because the sampling is used to detect public-health risks."
        ),
        "offered_penalty": "$3,000 for the sampling allegations; no penalty stated for the alleged 1420.1(j)(6) violation.",
    },
    {
        "notice": "P79476",
        "violation_date": "2023-05-01",
        "issue_date": "2024-11-19",
        "status": "Pending",
        "rules": "Rule 2004",
        "violation_description": "Inaccurate Quarter 1 QCER.",
        "ecobat_response": "No separate Ecobat response document was located in the AQMD subdirectory reviewed for P79476.",
        "scaqmd_response": (
            "SCAQMD described P79476 as a repeat Rule 2004 QCER-correction violation and said the Q1 2023 correction report was submitted nearly three months late."
        ),
        "offered_penalty": "$7,000.",
    },
    {
        "notice": "P68909",
        "violation_date": "2025-01-07",
        "issue_date": "2025-01-30",
        "status": "In Compliance",
        "rules": "Rules 430, 1420.1(n); Title V permit conditions",
        "violation_description": "Alleged failure to report a breakdown / unplanned shutdown after a short WESP interruption on January 7, 2025.",
        "ecobat_response": (
            "Ecobat said the NOV's five alleged violations were all duplicative of one event: a three-minute Edison-caused power sag during a voluntary plant shutdown. "
            "It argued furnaces were no longer being fed, the WESP did not completely shut down, voltage stayed compliant, at least partial scrubber flow continued, "
            "and all relevant information was later provided to the District, so the breakdown / unplanned-shutdown reporting rules were not triggered."
        ),
        "scaqmd_response": (
            "SCAQMD described the matter as failure to report a breakdown and notify after an unplanned shutdown of ECDs, but for the global settlement offer said it "
            "was willing to accept compliance only."
        ),
        "offered_penalty": "Compliance only; no monetary penalty stated.",
    },
    {
        "notice": "P69321",
        "violation_date": "2024-01-02",
        "issue_date": "2025-06-27",
        "status": "Pending",
        "rules": "1420.1; 221; 3002; 430; 40 CFR",
        "violation_description": "Failure to maintain negative pressure, report breakdown, use water / HEPA vacuum during maintenance, comply with permit terms, and operate according to plan.",
        "ecobat_response": (
            "The AQMD folder did not contain a direct response to NOV P69321. The closest Ecobat file in that folder is a February 28, 2025 Rule 1420.1 notification "
            "stating a February 19, 2025 Monitor 5 lead exceedance was caused by fugitive dust from auger pan replacement and that future auger-pan maintenance would "
            "use standby operators and wet suppression."
        ),
        "scaqmd_response": "Not addressed in the June 12, 2025 global settlement letter located in the AQMD folder.",
        "offered_penalty": "Not addressed.",
    },
    {
        "notice": "P79157",
        "violation_date": "2023-06-07",
        "issue_date": "2024-02-29",
        "status": "In Compliance",
        "rules": "Rule 1420.1(k)(3), (k)(4); Rule 3002(c)(1)",
        "violation_description": "Late initial source testing, pre-test protocol issues, and alleged Title V noncompliance tied to the Kiln Baghouse / Device C182.",
        "ecobat_response": (
            "Ecobat said repeated auger jamming and startup problems made timely source testing impossible, and that District staff allowed use of previously approved "
            "protocols to address conflicting permit and rule timing requirements. It also argued the February 2022 PM10 exceedance was a testing error because the contractor "
            "measured total particulate instead of PM10, and a later test showed compliance."
        ),
        "scaqmd_response": (
            "SCAQMD said there may have been confusion about protocol timing, but not about the requirement to test within 60 days of startup. It said the February 2022 "
            "test was late and not conducted in accordance with the prior approved protocol because the correct contaminant was not measured."
        ),
        "offered_penalty": "$5,000; no penalty stated for the alleged Rule 1420.1(k)(4) violation.",
    },
    {
        "notice": "P79157",
        "violation_date": "2023-06-07",
        "issue_date": "2024-02-29",
        "status": "In Compliance",
        "rules": "Rule 1420.1(k)(15)",
        "violation_description": "Late source-test report submissions.",
        "ecobat_response": (
            "Ecobat said the allegation was meritless and listed proof-of-delivery dates showing the cited 2022 and 2023 source-test reports were submitted within 90 days."
        ),
        "scaqmd_response": (
            "SCAQMD said the NOV concerned January-February 2022 tests whose reports were submitted late, found the delay unexplained, and said Ecobat did not seek a variance."
        ),
        "offered_penalty": "$14,500.",
    },
    {
        "notice": "P69327",
        "violation_date": "2025-08-01",
        "issue_date": "2025-11-07",
        "status": "In Compliance",
        "rules": "Rule 1403; 40 CFR",
        "violation_description": "Failure to survey the affected facility or facility components for asbestos before demolition or renovation activity.",
        "ecobat_response": "No Ecobat response file for P69327 was located in the AQMD subdirectories reviewed.",
        "scaqmd_response": "Not addressed in the June 12, 2025 global settlement letter located in the AQMD folder.",
        "offered_penalty": "Not addressed.",
    },
    {
        "notice": "P79172",
        "violation_date": "2022-01-01",
        "issue_date": "2024-02-29",
        "status": "NOV",
        "rules": "Permit C8.2",
        "violation_description": "C89 EAF scrubber pH below the 9.4 permit limit.",
        "ecobat_response": (
            "Ecobat argued the EAF scrubber should be treated like the reverberatory scrubber while the WESP SOx CEMS is in full operation, and that the District had "
            "already issued a draft permit lowering C8.2 to a minimum pH of 8.0. Ecobat therefore argued the current 9.4 limit is outdated."
        ),
        "scaqmd_response": (
            "SCAQMD said the plain language of E51.1 applies only to C40, not C89, and that it must enforce the existing Title V permit until a final permit revision is issued. "
            "It added that even under an 8.0 pH threshold there were still dozens of low-pH instances."
        ),
        "offered_penalty": "$40,000.",
    },
    {
        "notice": "P79172",
        "violation_date": "2022-01-01",
        "issue_date": "2024-02-29",
        "status": "NOV",
        "rules": "Permit C8.1",
        "violation_description": "C40 reverberatory scrubber pH below the 8.9 permit limit.",
        "ecobat_response": (
            "Ecobat argued the C40 pH allegation should be excused under Permit Condition E51.1 while the WESP SOx CEMS was in full operation, and also referenced the same "
            "lower-pH draft permit logic used for C89."
        ),
        "scaqmd_response": (
            "SCAQMD said it still views the existing permit as controlling, but based on the records supporting SOx CEMS operation during the relevant period, it was willing "
            "to accept compliance only for this allegation."
        ),
        "offered_penalty": "Compliance only; no monetary penalty stated.",
    },
    {
        "notice": "P79172",
        "violation_date": "2022-01-01",
        "issue_date": "2024-02-29",
        "status": "NOV",
        "rules": "Permit D322.2",
        "violation_description": "Rotary dryer weekly inspection and 24-hour internal build-up removal allegations.",
        "ecobat_response": (
            "Ecobat said it located reports for the cited weeks and that kiln cleaning typically occurs during compliance downtime within 24 hours of inspection, though it "
            "could not confirm every cited removal event from the records."
        ),
        "scaqmd_response": (
            "SCAQMD accepted compliance only for one weekly-inspection allegation but said the records did not show internal build-up was removed within 24 hours of discovery "
            "and that Ecobat had not documented timely cleaning."
        ),
        "offered_penalty": "$5,000 for the build-up-removal allegation; compliance only for the weekly-inspection allegation.",
    },
    {
        "notice": "P79172",
        "violation_date": "2022-01-01",
        "issue_date": "2024-02-29",
        "status": "NOV",
        "rules": "Permit C8.6; 40 CFR 63.548i",
        "violation_description": "WESP packed-bed scrubber water-flow allegations, including low flow, missing flow records, and alleged federal flow-monitoring applicability.",
        "ecobat_response": (
            "Ecobat argued C8.6 should be read together with D12.17, requiring a minimum of four WESPs in full operation, and disputed that 40 CFR 63.548i applies to the "
            "WESP packed-bed scrubbers."
        ),
        "scaqmd_response": (
            "SCAQMD limited its penalty theory to times when two or more of five scrubbers were below 1,200 gpm or when flow was missing for all scrubbers, and accepted "
            "compliance only for the alleged 40 CFR 63.548i applicability issue."
        ),
        "offered_penalty": "$14,500 for the low-flow / missing-flow allegations; compliance only for the alleged 40 CFR 63.548i applicability issue.",
    },
]
