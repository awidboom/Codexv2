# Regulation 2, Rule 2 — NSR Review After the Rule 1 Offramp

## Core point

`Regulation 2, Rule 2` is the substantive NSR rule you reach after the `Rule 1` analysis concludes that the project requires permitting as a new or modified source. In that sense, `Rule 1` is the gatekeeper and `Rule 2` is the main engineering review framework.

The sequence is:

1. complete the `Rule 1` analysis and determine that the project is a permitted `new` or `modified` source;
2. enter `Rule 2` to determine which substantive NSR requirements apply;
3. perform the `Rule 2` emission calculations, which are different from the `Rule 1` modification test;
4. apply `BACT`, offsets, `PSD Project` review, and related requirements on a pollutant-specific basis;
5. separately determine whether `Rule 5` adds a toxics overlay.

The key practical distinction is that `Rule 1` asks whether the project is in NSR at all, while `Rule 2` asks what NSR obligations attach once it is in.

For the `Rule 1` gateway analysis, refer to `outputs/reg2_rule1_nsr_applicability_analysis.md:1`.

## Rule excerpts that control the analysis

### Rule 2 scope

> `2-2-101`: "This Rule applies to all new and modified sources that are subject to the requirements of Section 2-1-301 and/or 2-1-302."

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:27`

### BACT

> `2-2-301.1`: A new source requires `BACT` if it will have `10 lb/day` or more of a District `BACT` pollutant.

> `2-2-301.2`: A modified source requires `BACT` for each District `BACT` pollutant for which the source is modified, if the post-project source is `10 lb/day` or more and the modification causes an increase above baseline levels calculated under `2-2-604`.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:345`

### Offsets

> `2-2-302`: `NOx` and `POC` offsets apply once facility `PTE` exceeds `10 tpy`, with `1:1` or `1.15:1` treatment depending on the post-project facility level and whether the Small Facility Banking Account applies.

> `2-2-303`: `PM2.5`, `PM10`, and `SO2` offsets apply at `100 tpy` post-project facility `PTE`, with offsets for un-offset cumulative increase above `1 tpy`.

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:367`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:407`

### PSD

> `2-2-304`: A `PSD Project` requires federal `PSD BACT` for each `PSD` pollutant with a significant net increase.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:427`

### Emission calculations

> `2-2-603`: baseline-period and adjusted-baseline procedures.

> `2-2-604`: new-source increase = `PTE`; existing-source change = post-project `PTE` minus adjusted baseline emissions.

> `2-2-606` through `2-2-608`: cumulative increase and un-offset cumulative increase procedures.

> `2-2-610`: cargo-carrier emissions are included for offsets and cumulative increase, but not for `BACT` and `PSD`.

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:703`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:775`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:839`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:883`

## Information needed up front

Before doing the `Rule 2` review, assemble at least the following:

- the completed `Rule 1` classification showing which units are `new`, `modified`, or otherwise carried into substantive `Rule 2` review;
- current permit conditions, enforceable limits, prior offsets, prior emission reduction credits, and any earlier NSR history for each affected source;
- current and post-project `PTE` for each regulated pollutant relevant to `BACT`, offsets, and `PSD`;
- baseline-period operating data and emissions data needed for `2-2-603`;
- enough throughput data to establish baseline throughput and the appropriate throughput-correlated emissions basis;
- enough emissions data to establish baseline emissions and adjusted baseline emissions;
- records sufficient to support any `RACT`, `BARCT`, federal-rule, or District-rule downward adjustments to baseline emission rates;
- information on prior offsets already provided for the source, because that changes the cumulative-increase math under `2-2-606.2`;
- any enforceable decreases associated with the project that may qualify under `2-2-605` and `2-2-607`;
- cargo-carrier information where directly associated with loading or unloading sources, because those emissions are counted for offsets and cumulative increase under `2-2-610`;
- for `PSD` review, the information needed to evaluate whether the project is a `PSD Project`, including netting inputs and any required source-impact / additional-impact analyses.

Practical evidence point: `Barr Approach.docx` stresses that BAAD expects **verifiable records**, ideally source tests, `CEMS`, or similarly strong evidence. Negotiation may be required if the analysis depends on `AP-42`, generic factors, or derived calculations.

## Recommended decision sequence

### 1. Confirm the Rule 1 offramp into Rule 2

Do not start with `Rule 2` in isolation. First confirm that the `Rule 1` analysis concluded that the source is in the permitting program as a `new` or `modified` source, or otherwise reached the point where substantive NSR review is required.

This is important because if the project is not a `new` or `modified` source under `Rule 1`, then `Rule 2` generally does not apply at all.

Source: `outputs/reg2_rule1_nsr_applicability_analysis.md:1`

### 2. Identify which Rule 2 calculations you need

A key practical point from the NSR guidance and `Barr Approach.docx` is that `Rule 2` uses more than one emissions calculation framework.

At minimum, distinguish between:
- `Rule 2-1` modification / federal backstop concepts from the gateway analysis;
- `Rule 2-2-603` / `604` emission-increase calculations for `BACT` and `PSD Project` review;
- `Rule 2-2-606` / `607` / `608` cumulative-increase calculations for offsets.

These are related, but they are not interchangeable.

### 3. Establish baseline emissions correctly under `2-2-603`

This is the foundation of the `Rule 2` review.

Under `2-2-603`:
- the baseline-period ending date is generally the application completeness date for a new or modified source;
- for pollutants other than `GHGs`, the baseline period is generally the `3 years` immediately preceding that date;
- for `GHGs`, certain existing-source categories use a `24-month` baseline within the last `5` or `10` years, depending on source type;
- baseline throughput is the lesser of actual average annual throughput or average permitted throughput if permit-limited;
- baseline emissions are actual average annual emissions during the baseline period, excluding emissions above regulatory or permit limits;
- adjusted baseline emissions are then adjusted downward, if necessary, to reflect the most stringent of `RACT`, `BARCT`, and applicable federal and District requirements, subject to the `PSD Project` limitation in `2-2-603.6`.

A practical summary from `Barr Approach.docx` is:
- determine baseline throughput;
- determine baseline emissions;
- determine the `RACT` / `BARCT` / federal / District adjustment;
- determine adjusted baseline emissions.

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:703`, `NSR guidance/Barr Approach.docx:35`

### 4. Calculate post-project emissions and emission change under `2-2-604`

This is the main `Rule 2` project-change calculation.

> `2-2-604.1`: for a new source, the emissions increase is the source's `PTE`.

> `2-2-604.2`: for a change at an existing source, the emissions increase or decrease is post-project `PTE` minus adjusted baseline emissions.

That means the standard practical shorthand is:
- **new units**: emissions increase = `PTE`;
- **existing units**: emissions change = post-project `PTE` minus adjusted baseline emissions.

This is the calculation Barr summarizes for `BACT` and `PSD Project` review, and it is different from the gateway `Rule 1` analysis.

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:775`, `NSR guidance/Barr Approach.docx:35`

### 5. Apply `BACT` under `2-2-301`

Once the `2-2-604` calculations are done, evaluate `BACT` on a pollutant-specific basis.

- A **new source** requires `BACT` if the source will emit `10 lb/day` or more of the District `BACT` pollutant.
- A **modified source** requires `BACT` for a pollutant only if:
  - the post-project source will emit `10 lb/day` or more of that pollutant; and
  - the modification produces an increase above baseline for that pollutant.

A practical BAAD point from `Barr Approach.docx` is to start with the `BACT/TBACT Workbook`, then evaluate whether top controls must be considered for cost-effectiveness and whether other California district determinations should also be reviewed.

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:345`, `NSR guidance/Barr Approach.docx:45`

### 6. Determine whether the project is a `PSD Project`

Do not assume that the federal backstop test and the District `PSD Project` test are the same.

The guidance specifically notes that:
- the federal backstop test uses an `actual-to-projected-actual` style methodology; but
- the District `PSD Project` test uses the pre-NSR-Reform `actual-to-potential` style methodology.

So after the `Rule 1` gateway analysis, you still need the separate `PSD Project` review under `Rule 2-2`.

A practical sequence from `Barr Approach.docx` is:
- sum the `Rule 2-2` emission increases for the relevant units;
- compare to `SERs` / significance levels;
- if exceeded, complete the netting analysis;
- if still exceeded, perform the `PSD` review under `2-2-304` through `2-2-307`.

Sources: `NSR guidance/_text/Complex NSR Permitting Handbook_Sept 2016 pdf.txt:275`, `NSR guidance/Barr Approach.docx:49`

### 7. If the project is a `PSD Project`, apply the PSD requirements

If the project meets the `PSD Project` criteria, then move through the PSD-specific sections:

- `2-2-304` federal `PSD BACT`;
- `2-2-305` PSD air quality analysis;
- `2-2-306` PSD additional impact analysis;
- `2-2-307` Class I Area protection;
- `2-2-308` NAAQS protection requirement;
- `2-2-309` major facility compliance certification;
- `2-2-310` permit denial if conditions are not met.

The practical point is that this is a separate, elevated review tier, not just a more detailed version of ordinary offsets / `BACT` review.

Sources: `NSR guidance/_text/Reg 2 NSR Permitting Presentation_Sept 30 2016 pdf.txt:0`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:427`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:485`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:493`

### 8. Calculate cumulative increase for offsets under `2-2-606` through `2-2-608`

This is a separate emissions-accounting exercise from the `2-2-604` increase calculation.

Under the rule:
- `2-2-606` determines the project-level increase in `PTE` for cumulative-increase purposes;
- `2-2-607` calculates cumulative increase as project increase minus contemporaneous onsite emission reduction credits;
- `2-2-608` calculates the facility's un-offset cumulative increase by adding the project cumulative increase to prior un-offset cumulative increases after the baseline date and subtracting offsets already provided.

A crucial practical point from `Barr Approach.docx` is that if offsets were previously provided for an existing unit, the cumulative-increase math changes: instead of using adjusted baseline emissions, the analysis starts from the unit's prior `PTE` and adjusts that downward to `RACT` / `BARCT` as required.

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:839`, `NSR guidance/Barr Approach.docx:53`

### 9. Apply the offset rules

Once cumulative increase is established, apply the offset provisions:

- `2-2-302` for `NOx` and `POC` once post-project facility `PTE` exceeds `10 tpy`;
- `2-2-303` for `PM2.5`, `PM10`, and `SO2` at the higher post-project facility `PTE` threshold.

Important practical points:
- the offset ratio depends on the post-project facility level and whether the Small Facility Banking Account applies;
- enforceable decreases can matter if they qualify under the rule;
- the offset analysis is pollutant-specific;
- cargo-carrier emissions tied to loading or unloading must be included for offsets and cumulative increase.

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:367`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:407`, `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:883`, `NSR guidance/Barr Approach.docx:53`

### 10. Include cargo carriers where required, but not everywhere

`2-2-610` is easy to miss.

For offsets and cumulative increase, cargo-carrier emissions associated with the source must be included. The rule specifically says those emissions are included for offset purposes when the facility includes cargo loading or unloading from cargo carriers other than motor vehicles.

But the rule also says those cargo-carrier emissions are **not** included for other `Rule 2` purposes, including `BACT` and `PSD` requirements.

This is one of the most important scope distinctions in the rule.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-2.md:883`

### 11. Tie Rule 2 back to Rule 5 where toxics are present

`Rule 2` does not replace the toxics review. If the project includes `TACs`, then after the `Rule 2` NSR analysis you still need the separate `Rule 5` review.

That means:
- `Rule 2` handles substantive NSR requirements for criteria and PSD-type review;
- `Rule 5` separately handles `TBACT`, project risk, and `HRA` issues for toxics.

For the detailed toxics memo, refer to `outputs/reg2_rule5_toxics_applicability_analysis.md:1`.

## Practical checklist

A defensible `Rule 2` review usually answers these questions in order:

1. What sources reached `Rule 2` from the `Rule 1` analysis?
2. What pollutants are relevant for `BACT`, offsets, and `PSD`?
3. What is the correct baseline period and adjusted baseline under `2-2-603`?
4. What is the `2-2-604` emissions increase for each new or modified source?
5. Which pollutants trigger `BACT`?
6. Is the project a `PSD Project`?
7. If so, what PSD-specific analyses are required?
8. What is the project cumulative increase and facility un-offset cumulative increase?
9. Are offsets required, and at what ratio?
10. Do cargo-carrier emissions need to be included for offsets?
11. Does the project also require a separate `Rule 5` toxics review?

## Bottom line

The clean way to think about `Rule 2` is:

- `Rule 1` tells you whether the project enters NSR;
- `Rule 2` tells you how to quantify the substantive NSR consequences of that project;
- and the same project can require several separate `Rule 2` calculations that should not be collapsed into one number.

The main practical mistake to avoid is treating `Rule 1`, `Rule 2-2-604`, offsets / cumulative increase, and `PSD Project` review as if they all use the same emissions test. They do not.
