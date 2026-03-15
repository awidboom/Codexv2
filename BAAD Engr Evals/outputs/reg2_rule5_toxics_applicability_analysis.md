# Regulation 2, Rule 5 Toxics Applicability Analysis

## Core point

A `Rule 2-5` applicability analysis is not just a trigger-level screen. The correct sequence is:

1. determine whether there is a **new source** or **modified source** of TACs;
2. determine what sources are in the **project**;
3. calculate emissions using `Sections 2-5-601` and `2-5-602`;
4. explicitly evaluate the available exemptions and limited exemptions, including at least:
   - `2-5-110` low-emission exemption;
   - `2-5-114` limited exemption for a modified source with no increase in toxicity-weighted emissions;
   - `2-5-115` limited exemption for contemporaneous health risk reduction projects, where relevant;
5. compare emissions to `Table 2-5-1` to determine whether the project is exempt from the rule, whether a source is exempt from the `2-5-401` `HRA` requirement, or whether the project remains fully subject to `Rule 2-5`;
6. if not exempt, perform the `HRA` and apply `TBACT` and project risk standards.

That sequence matters because a source can still be a **modified source** even where the increase is below `Table 2-5-1` trigger levels. Being below the trigger levels can satisfy the `2-5-110` low-emission exemption or the `Section 2-5-401` `HRA` exemption for a source, and `2-5-114` can remove the `HRA` requirement for certain modified sources, but those exemption outcomes do **not** mean the source was never modified. The analysis therefore needs two separate determinations: first, whether the source is new or modified; second, whether an exemption or limited exemption changes the level of `Rule 2-5` review that is required.

## Information request

Before doing the `Rule 2-5` applicability analysis, assemble the following information:

- a list of all affected equipment, identifying which units are:
  - new;
  - undergoing a physical change;
  - undergoing an operational change;
- for each existing unit, all current permit conditions and any permit limits relevant to TAC emissions, throughput, hours of operation, or control efficiency;
- current `PTE` for each affected source and each emitted TAC;
- future or post-project `PTE` for each affected source and each emitted TAC;
- for each existing source, the last `3 years` of actual emissions and throughput data, plus any supporting operating records needed to establish the `2-5-602` baseline period;
- any existing toxics-specific permit limits, because for existing permitted units an existing toxics limit may control the baseline analysis instead of the default 3-year actuals approach, while still requiring downward adjustment for `MACT` where applicable;
- where BAAD practice matters, note whether the source is a combustion unit relying only on generic combustion `HAP` factors, because `Barr Approach.docx` notes that BAAD has not typically focused on combustion `HAPs` from `AP-42` in the same way as source-specific toxics emissions;
- source-specific emission factors, source test data, vendor guarantees, certified emission rates, or other technical basis for the emissions calculations;
- identification of each TAC emitted and whether it has acute trigger levels, chronic trigger levels, or both under `Table 2-5-1`;
- if HRA modeling is required:
  - stack parameters, fugitive-release characteristics, abatement-device information, and operating schedules needed for `HRA` modeling if the project is not exempt;
  - a facility plot plan showing source locations, property boundary, nearby residences, businesses, schools, and other potential receptor locations.

These inputs are needed because:

- whether an existing source is **modified** often cannot be decided until you compare post-project emissions against the applicable pre-project baseline under `2-5-214`, `2-5-601`, and `2-5-602`;
- whether `2-5-110` or `2-5-114` applies depends on the emissions calculations;
- if no exemption applies, the same dataset will feed the `HRA`.

## Rule excerpts that control the analysis

### Applicability

> `2-5-102.1`: This rule applies to a new or modified source of toxic air contaminants for which an application is submitted on or after July 1, 2005.

> `2-5-102.2`: This rule also applies to certain TAC sources constructed or modified after January 1, 1987 without required District permits.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:31`

### Low-emission exemption

> `2-5-110`: "A project (and each new or modified source included in this project) shall not be subject to this rule if, for each toxic air contaminant, total project emissions are below the acute and chronic trigger levels listed in Table 2-5-1 ... For the purposes of Regulation 2-1-316, a source shall not be subject to the Section 2-5-401 HRA requirements of this rule if ... the emissions from the source are below the acute and chronic trigger levels..."

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:47`

### Modified source definition

> `2-5-214`: A modified source is an existing source that undergoes a change resulting or potentially resulting in an increase in daily or annual TAC emissions, an increase above ATC/PTO-approved levels, or, for some never-permitted sources, an increase above authorized or functional capacity.

> `2-5-214.4`: A modified source also includes emission of a TAC not previously emitted in a quantity that would result in a cancer risk greater than `1.0 in a million` or a chronic hazard index greater than `0.20`.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:173`

### Project definition and anti-circumvention

> `2-5-216`: All new or modified TAC sources in a single permit application are a project, and the project also includes certain TAC sources permitted within the prior five years and unexpired ATCs unless the applicant shows the current change was not reasonably foreseeable and not an integral part of the earlier project.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:245`

### Emission calculations

> `2-5-601.2`: New-source emissions are based on maximum emitting potential or the maximum permitted emission level, subject to enforceable limiting conditions.

> `2-5-601.3`: Modified-source emissions are based on post-modification emissions and pre-modification emissions calculated using `2-5-602`.

> `2-5-601.4`: Project emissions are the sum of emissions from all new TAC sources and the post-modification emissions from all modified TAC sources in the project.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:503`

### Baseline emissions

> `2-5-602.1`: If a permit condition contains an emission cap or emission rate limit, baseline throughput and baseline emission rate are based on those allowed levels.

> `2-5-602.2`: If no cap or rate limit exists, use a 3-year baseline period immediately preceding application completeness, with baseline throughput equal to the lowest of actual average throughput, authorized capacity, or functional capacity.

> `2-5-602.3` and `2-5-602.4`: The baseline emission rate must be adjusted downward as needed to comply with the most stringent applicable `MACT`, `ATCM`, or District rule, and adjusted baseline emissions equal adjusted baseline emission rate times baseline throughput.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:539`

### HRA and standards

> `2-5-401`: Any project subject to the rule must include an `HRA` or information sufficient for the APCO to prepare one.

> `2-5-301`: `TBACT` is required where source risk exceeds `1.0E-6` cancer risk and/or `0.20` chronic hazard index.

> `2-5-302`: The APCO must deny a permit if project risk exceeds `10 in a million` cancer risk, or `6 in a million` in an `Overburdened Community`, or exceeds `1.0` chronic or acute hazard index.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:349`, `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:399`

## Definitions that should be applied explicitly

### `Modified Source of Toxic Air Contaminants`

The rule defines this term in `2-5-214`. The practical consequence is that you do **not** decide modification status by looking only at `Table 2-5-1`. You first decide whether the source change creates an emissions or capacity increase of the kind described in `2-5-214`. That requires doing the emissions calculations.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:173`

### `New Source of Toxic Air Contaminants`

`2-5-215` covers sources never previously permitted, sources out of operation for at least a year without a valid PTO, relocations to non-contiguous property, and replacements.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:217`

### `Project`

`2-5-216` is important because the toxics analysis is often broader than the equipment line item in the current application. The five-year lookback can pull prior TAC work into the analysis.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:245`

### `Health Risk Assessment (HRA)` / `Project Risk` / `Receptor Location`

These defined terms matter because the rule is not satisfied by emission calculations alone once the trigger-level exemption is lost. The rule requires a receptor-based health risk analysis.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:153`, `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:253`, `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:259`

## Recommended analysis sequence

### 1. Determine whether the permit action involves TAC-emitting sources

List every source in the permit action that emits one or more TACs. Then determine whether each source is potentially a `new source` or `modified source` under `2-5-214` and `2-5-215`.

### 2. Do the emission calculations before deciding whether the source is modified

A source is "modified" under `2-5-214` only if the change results or may result in the specified increase. That means the emission calculations are part of the modification determination, not something done only afterward.

For a modified-source analysis, calculate:
- **post-modification emissions** under `2-5-601.3.1`; and
- **pre-modification emissions** using the adjusted baseline methodology in `2-5-602`.

If post-project emissions exceed pre-project emissions in the way described in `2-5-214`, the source can be modified even if the increase is below `Table 2-5-1` trigger levels.

### 3. Define baseline emissions correctly

Baseline emissions are not simply the most recent actual year.

- If there is an enforceable cap or emission rate limit in a permit condition, baseline values come from that allowed level.
- If there is no cap or emission rate limit, the baseline period is usually the 3 years before application completeness.
- Baseline throughput is the **lowest** of actual average throughput, authorized capacity, or functional capacity.
- The baseline emission rate is the average actual rate during the baseline period, excluding periods above regulatory or permit limits.
- Then adjust the baseline emission rate downward if a more stringent `MACT`, `ATCM`, or District limit applies.

A practical point from `Barr Approach.docx` is that, for existing permitted units, an existing toxics limit can be used in place of the 3-year actuals baseline, but it still needs to be adjusted downward for `MACT` where applicable.

That adjusted baseline is what you compare against post-modification emissions.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:539`

### 4. Define post-project emissions correctly

For a modified source, post-modification emissions are based on the source's **maximum emitting potential** or **maximum permitted emission level**, subject to enforceable limiting conditions. This is not necessarily the applicant's expected average operations.

For the project, sum:
- emissions from all **new** TAC sources; and
- **post-modification** emissions from all modified TAC sources included in the project.

For new units, the practical shorthand from `Barr Approach.docx` is that the emission increase is generally `PTE`. For existing permitted units, the comparison is post-project `PTE` against the properly established baseline emissions.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:503`

### 5. Compare emissions to `Table 2-5-1`

After determining what is new or modified and what belongs in the project, compare emissions to the acute and chronic trigger levels in `Table 2-5-1`.

This is where the common mistake occurs: the trigger-level comparison is an exemption screen, not the definition of modification.

- If the source or project is below the applicable trigger levels, `2-5-110` can remove the project from the rule or remove the source from the `2-5-401` `HRA` requirement.
- But a source can still be a **modified source** because modification status is determined under `2-5-214`, not by `Table 2-5-1`.

This point is also reflected in the NSR guidance, which explains that trigger levels are used to determine whether the new or modified source must comply with `Rule 2-5`, not to determine whether the change qualifies as a modification in the first place.

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:47`, `NSR guidance/_text/20211209_17_FSR_RG0201andRG0205 pdf.txt:1178`

### 6. Check limited exemptions for modified sources

Even if the source is modified, `2-5-114` can remove the `HRA` requirement where post-modification toxicity-weighted emissions are less than or equal to pre-modification toxicity-weighted emissions.

That is different from saying the source is not modified. It means the modified source satisfies a limited exemption from `2-5-401`.

A practical implementation point from `Barr Approach.docx` is that if emissions go up for some toxics but down for others, this is the stage to evaluate the toxicity-weighted approach rather than looking only at pollutant-by-pollutant directional changes.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:71`

### 7. If not exempt, perform the `HRA`

If the project remains subject to the rule after the trigger-level and limited-exemption screens, then `2-5-401` requires an `HRA`, and `2-5-603` requires that it follow the District's HRA Guidelines.

A practical point from `Barr Approach.docx` is that if any trigger is exceeded, the `HRA` should be performed for all units and pollutants in the `Rule 2-5` project, not just the specific unit or compound that first exceeded the trigger. `Barr Approach.docx` also notes that exempt units with `TACs` may still need to be included in the project `HRA`, even if their impacts can also be looked at separately.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:399`, `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:587`

### 8. Apply `TBACT` and project risk standards

Once the `HRA` is done:
- apply `TBACT` if source risk exceeds `1.0E-6` cancer risk or `0.20` chronic HI;
- deny if project risk exceeds `10 in a million` cancer risk, or `6 in a million` in an `Overburdened Community`, or exceeds `1.0` chronic or acute HI.

Source: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:349`

## Practical conclusion

The clean way to state the analysis is:

- **Modification status** is decided under the definitions in `2-5-214` and the emission-calculation procedures in `2-5-601` / `2-5-602`.
- **Rule 2-5 exemption / HRA applicability** is then screened using `2-5-110` and any limited exemptions such as `2-5-114`.
- Therefore, a source can be **modified** even where the increase is below `Table 2-5-1`; in that case, the source may avoid the `HRA` requirement or the project may be exempt from the rule, but the modification determination is still real.

## Supporting guidance

The NSR guidance is consistent with this reading:

> Trigger levels are used to determine whether new and modified sources that are subject to permit requirements must comply with `Regulation 2, Rule 5`.

> In general, a health risk screening analysis is required for permit applications involving new or modified sources where TAC emissions exceed one or more trigger levels.

Sources: `NSR guidance/_text/20211209_17_FSR_RG0201andRG0205 pdf.txt:1178`, `NSR guidance/_text/20211209_17_FSR_RG0201andRG0205 pdf.txt:1530`

## Additional detail � required procedures for performing the `HRA`

The rule itself is short on procedure, but it expressly incorporates the Air District `HRA Guidelines`, which in turn incorporate the OEHHA methodology. So the right reading is:

- `2-5-401` tells you **when** an `HRA` is required;
- `2-5-402` tells you to use the Air District `HRA Guidelines`;
- `2-5-603` says each `HRA` must be prepared following those guidelines.

That means the procedural requirements are not optional supporting material. They are the operative method for performing the `HRA` once the rule applies.

### Rule excerpts

> `2-5-401`: "An application for an Authority to Construct or Permit to Operate for any project subject to this rule shall contain an HRA conducted in accordance with Section 2-5-603 or the information necessary for the APCO to conduct an HRA."

> `2-5-402`: "The APCO shall publish Health Risk Assessment Guidelines that specify the procedures to be followed for estimating health risks including acute hazard index, chronic hazard index, and cancer risk."

> `2-5-603`: "Each HRA shall be prepared following the District's Health Risk Assessment Guidelines."

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:399`, `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:407`, `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:587`

### What the HRA has to accomplish

Under the rule definitions, the `HRA` must quantify:
- **source risk** for each new or modified source;
- **project risk** for the project as a whole;
- risk at appropriate **receptor locations**;
- cancer risk, chronic hazard index, and acute hazard index.

Relevant defined terms:

> `2-5-217 Project Risk`: "The health risk resulting from the emissions of toxic air contaminants from a given project, as indicated by an HRA for the MEI."

> `2-5-218 Receptor Location`: locations where a person may live, work, or otherwise reasonably be expected to be exposed, including some on-site residences.

> `2-5-221 Source Risk`: "The health risk resulting from the emissions of all toxic air contaminants from a new or modified source ... as indicated by an HRA for the MEI."

Sources: `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:253`, `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:259`, `baaqmd_rules/rag_md/rule-regulation-2-rule-5.md:277`

### Required HRA workflow

#### 1. Define the scope of the HRA correctly

The HRA is performed for a **project**, not just the single unit that first triggered concern. That means the analysis boundary should match the `2-5-216` project definition used in the applicability analysis.

Practically, that means:
- include all new TAC sources in the project;
- include all modified TAC sources in the project;
- include related prior permitted TAC sources if they are pulled into the project by the `2-5-216` anti-circumvention rule.

#### 2. Develop emissions inputs in the format required for health risk work

The HRA is only as good as the emissions inventory. The District guidance and `MOP Vol. II, Part 4` make clear that the applicant must provide enough information for the District to determine maximum hourly and/or annual emissions for each TAC.

> The applicant must supply sufficient information for the District to determine maximum hourly and/or maximum annual emissions for any TAC listed in Table 2-5-1.

> Maximum hourly emissions are needed for TACs with acute trigger levels; maximum annual emissions are needed for TACs with chronic trigger levels.

> Emissions subject to Rule 2-5 include routine and reasonably predictable emissions, including intermittent releases and predictable upsets or leaks, subject to enforceable limits.

Sources: `NSR guidance/_text/vol2_pt4.txt:540`, `NSR guidance/_text/vol2_pt4.txt:550`

In practice, the emissions package should identify for each emission point:
- each TAC emitted;
- maximum hourly emission rate where acute analysis is required;
- annual average or maximum annual emission rate where chronic/cancer analysis is required;
- stack or release characteristics;
- operating schedule and temporal variation;
- enforceable limits used in the calculations.

#### 3. Identify each emission point and source type for modeling

The `MOP` guidance says one `HRSA` form should be completed for each source with TAC emissions, and where a source has multiple emission points, the information should be organized by stack or emission point. Fugitive releases should be treated as area or volume sources, not forced into a stack format.

It also requires site layout information sufficient to evaluate nearby receptors and building downwash.

The submittal should include:
- source locations;
- facility boundary;
- nearest businesses and residences;
- receptor locations;
- stack dimensions and nearby building dimensions, generally within 250 feet, where relevant;
- operating schedule by time of day / season if emissions vary.

Source: `NSR guidance/_text/vol2_pt4.txt:574`

#### 4. Use the Air District / OEHHA exposure assumptions

The Air District HRA Guidelines state that all stationary-source HRAs are to be done following the OEHHA 2015 Hot Spots methodology and ARB/CAPCOA risk management breathing-rate guidance.

> All HRAs for stationary source facilities shall be completed by following the procedures described in the OEHHA Health Risk Assessment Guidelines ... and using the recommended breathing rates described in the ARB/CAPCOA Risk Management Guidance...

Source: `NSR guidance/_text/20211215_HRAGuidelines pdf.txt:54`

Key default assumptions from the Air District HRA Guidelines are:
- **Residential cancer risk**: exposure assumed `24 hours/day`, `350 days/year`, `30-year duration`.
- **Worker cancer risk**: exposure assumed `250 days/year`, `25-year duration`.
- **School / student exposure**: generally `180 days/year`; default `9-year` duration for a `K-8` school, subject to refinement for the actual school type.
- **Breathing rates**: use ARB/CAPCOA breathing-rate policy; for offsite workers the guideline states `230 L/kg-8 hours`; for school children the default is `520 L/kg-8 hours` for ages `2<16` unless refined.

Source: `NSR guidance/_text/20211215_HRAGuidelines pdf.txt:138`

#### 5. Use the health values in `Table 2-5-1`

The Air District HRA Guidelines say the health effects values for District HRAs are consolidated into `Rule 2-5, Table 2-5-1`, including the OEHHA health values used for the analysis.

That means the HRA should be anchored to the District's current adopted `Table 2-5-1` values for:
- cancer potency;
- chronic `REL` / weighting values;
- acute `REL` / weighting values.

Source: `NSR guidance/_text/20211215_HRAGuidelines pdf.txt:214`

#### 6. Perform cancer risk calculations using OEHHA age-adjusted procedures

The Guidelines are explicit that cancer risk calculations should include:
- **age sensitivity factors (`ASFs`)**;
- **fraction of time at home (`FAH`)** factors where applicable;
- the most sensitive age groups for residential exposure.

The initial residential analysis assumes `FAH = 1.0` for younger age groups to see whether school receptors fall inside the risk isopleths. If schools are not inside those isopleths, the analysis may then be refined using age-specific `FAH` factors.

For worker receptors, the analysis assumes work begins at age `16`.

Source: `NSR guidance/_text/20211215_HRAGuidelines pdf.txt:223`

#### 7. Perform noncancer calculations using hazard-index methodology

The Guidelines require noncancer impacts to be calculated using the hazard-index approach consistent with OEHHA's 2015 methodology.

This means the HRA should separately produce:
- **acute hazard index**; and
- **chronic hazard index**.

The Air District guidance also notes that background criteria-pollutant respiratory impacts are not required in Air District HRAs.

Source: `NSR guidance/_text/20211215_HRAGuidelines pdf.txt:273`

#### 8. Apply acute vs. chronic analysis correctly

The acute analysis is driven by short-term emissions and acute receptor impacts. The chronic and cancer analyses are driven by annualized emissions and longer-term exposure assumptions.

This matters because:
- acute modeling should track the `one-hour` or other short-term emission basis used in `2-5-601` and the applicable acute health values;
- chronic/cancer modeling should track the annualized emissions basis and the chronic / cancer values in `Table 2-5-1`.

The Air District's refinement option for **spatial averaging** may be used for chronic analyses, but the Guidelines explicitly say spatial averaging is **not appropriate for acute analysis**.

Source: `NSR guidance/_text/20211215_HRAGuidelines pdf.txt:285`

#### 9. Consider refinements only after a defensible screening analysis

The guidance allows refinement, but only after the basic model identifies the key impact locations. Examples include:
- refined `FAH` factors;
- school-specific age/duration assumptions;
- spatial averaging for chronic analysis;
- stochastic multipathway assessment where relevant.

For stochastic multipathway HRAs, the guideline says risk-management decisions should be based on the `95th percentile` cancer risk.

Source: `NSR guidance/_text/20211215_HRAGuidelines pdf.txt:312`

#### 10. Report results in the form needed for permit decisions

The HRA output should be organized so the permitting decision can directly test:
- whether any source exceeds the `2-5-301` `TBACT` threshold;
- whether the project exceeds the `2-5-302` project risk limits;
- whether a receptor is in an `Overburdened Community`, because that changes the cancer-risk standard from `10 in a million` to `6 in a million`.

That means the final HRA should clearly identify:
- the `MEI` / maximum impact receptor;
- receptor type (`residential`, `worker`, `student`);
- source risk by source, where needed for `TBACT`;
- project risk by receptor;
- acute, chronic, and cancer values;
- any refinements used;
- any enforceable operating limits relied upon.

### What the applicant normally has to submit

Based on the rule and `MOP` guidance, a defensible submittal package usually includes:
- TAC emission calculations by source and emission point;
- hourly and annual emission rates, as applicable;
- plot plan / scaled map with source, property boundary, and nearby receptor locations;
- stack parameters and nearby building dimensions where downwash matters;
- operating schedule and temporal assumptions;
- completed `HRSA` forms or equivalent information;
- electronic model input files for larger projects;
- for larger or unusual projects, a modeling protocol submitted for District review before the final analysis is completed.

Source: `NSR guidance/_text/vol2_pt4.txt:574`

### Important practical point

The District guidance describes the HRA as a modeling exercise based on project location, proximity of nearby residents and workers, weather patterns, terrain, and emissions data. That is a useful reminder that the HRA is not just a spreadsheet comparison to `Table 2-5-1`; it is a receptor-based risk analysis that must integrate emissions, release characteristics, meteorology, and receptor geometry.

Source: `NSR guidance/_text/20211209_17_FSR_RG0201andRG0205 pdf.txt:1680`

### Bottom line

A procedurally correct `Rule 2-5` HRA should therefore be done as follows:
- build a complete TAC emissions inventory for the entire `2-5-216` project;
- organize emissions by release point and by acute/chronic basis;
- identify all relevant receptor categories and locations;
- model concentrations using the Air District / OEHHA framework;
- calculate cancer, chronic HI, and acute HI using current District health values and exposure assumptions;
- refine only where the guidance allows and where the refinement is justified;
- report source risk and project risk in a form that can be tested directly against `2-5-301` and `2-5-302`.
