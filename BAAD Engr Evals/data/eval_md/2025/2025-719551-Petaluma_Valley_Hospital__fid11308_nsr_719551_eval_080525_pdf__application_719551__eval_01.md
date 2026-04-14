---
application_number: 719551
plant_name: Petaluma Valley Hospital
plant_address: Petaluma, CA 94954
evaluation_date: June 12, 2006
source_json: data/permit_evaluations_json/2025/2025-719551-Petaluma_Valley_Hospital__fid11308_nsr_719551_eval_080525_pdf__application_719551__eval_01.json
---

# Engineering Evaluation (Application 719551)
**Plant**:  Petaluma Valley Hospital
**Address**: Petaluma, CA 94954
**Evaluation Date**: June 12, 2006

## background
JSONPath: `$.background.text`

Background
nd 
 
Petaluma Valley Hospital (“facility” hereafter) is applying for an Authority to Construct 
(ATC)/Permit to Operate (PTO) for the following equipment: 
 
S-10 Emergency Standby Diesel Generator 
Engine Make: Caterpillar, Model: C18, Model Year: 2025,  
EPA Family Name: RCPXL18.1NYS, 900 bhp, 5.77 MMBtu/hr  
 
Abated by 
 
A-10 Rypos Active Diesel Particulate Filter (DPF), Model: Rypos Active  
DPF/C3+TM System, CARB Certified per Executive Order DE-13-002-07 
 
S-11 Emergency Standby Diesel Generator 
Engine Make: Caterpillar, Model: C18, Model Year: 2025,  
EPA Family Name: RCPXL18.1NYS, 900 bhp, 5.77 MMBtu/hr  
 
Abated by 
 
A-11 Rypos Active Diesel Particulate Filter (DPF), Model: Rypos Active  
DPF/C3+TM System, CARB Certified per Executive Order DE-13-002-07 
 
The facility has also requested to archive the following two sources: 
 
S-6 Emergency Standby Diesel Generator, Cummins Model KTA1150GA, 560  
BHP, 400 kW 
 
S-7 Emergency Standby Diesel Generator, Detroit Disel Model 16V-92T, 540  
BHP, 385 kW 
 
On November 26, 2024, the facility submitted this application to install two identical 
emergency standby diesel generators (S-10 and S-11). The project involves removing two 
existing non-operational emergency generators (S-6 and S-7) and replacing them with the 
new units at the same location. 
 
Both S-10 and S-11 are 900 bhp, Tier 2 EPA-Certified, model year 2025, diesel-fired 
engines. S-10 and S-11 will be able to operate unrestricted during emergency use events. 
The engines will be limited to a maximum of 50 hours per year for maintenance and 
testing. The criteria pollutants associated with the source are nitrogen oxides (NO x), 
 
 2carbon monoxide (CO), precursor organic compounds (POC), sulfur dioxide (SO 2), and 
particulate matter (PM 10 and PM 2.5). The Rypos DPF is CARB certified per Executive 
Order DE-13-002-07, which verifies that the DPF reduces emissions of diesel PM by 
greater than or equal to 85%. Therefore, an 85% abatement efficiency is applied to the 
PM emission factor. 
 
S-10 and S-11 meet the Environmental Protection Agency and California Air Resources 
Board (EPA/CARB) Tier 2 Off-road standards. The engines will burn commercially 
available California low sulfur diesel fuel. The sulfur content of the diesel fuel will not 
exceed 0.0015% by weight.

## emission_calculations
JSONPath: `$.emission_calculations.text`

Emissions Calculation
Table 1. Engine Specification and EPA Certified Emission Factors for S-10 and S-11 
Engine Manufacturer  Caterpillar  
Model C18 
Model Year  2024 
Family Name  RCPXL18.1NYS  
Engine Power Rating, hp  900 bhp (671 kW)  
Fuel Consumption, gal/hr  42.1 
Displacement, L  18.12 
NOX, g/kW-hr (g/hp-hr) 5.42 (4.04) 
Non-Methane Hydrocarbon (NMHC), g/kW -hr (g/hp-hr) 0.13 (0.10)  
CO, g/kW -hr (g/hp-hr) 0.90 (0.67) 
PM, g/kW -hr (g/hp-hr) 0.05 (0.04) 
1. Emission factors converted assuming 1kW = 1.341 hp 
2. S-10 and S-11 are identical emergency generators. 
 
Table 2. Annual and Daily Emissions from EPA/CARB Certified Data for S-10 
Pollutant Emission 
Factor 
(g/bhp-hr) Max DailyEmissions1
(lb/day) Annual 
Emissions 
(lb/year) Annual 
Emissions2 
(ton/year) 
NOx 4.04 192.21 400.80 0.200 
POC 0.10 4.76 9.92 0.005 
CO 0.67 31.88 66.47 0.033 
PM10/PM2.53,4 0.006 0.29 0.60 0.000 
SO25 0.006 0.26 0.54 0.000 
Note: S-11 is an identical engine, therefore, annual and daily emissions are the same as S-
10. 
Basis:   
 1Max daily emissions: Assume 24-hour operation: 
 
4.04𝑔  𝑁𝑂௫
𝑏ℎ𝑝−ℎ𝑟∗900 𝑏ℎ𝑝∗24 ℎ𝑟
𝑑𝑎𝑦∗1 𝑙𝑏
454 𝑔= 192.21𝑙𝑏 𝑜𝑓 𝑁𝑂௫
𝑑𝑎𝑦 
 
 
 3 2 Annual emissions: Reliability-related activity, 50 hours is permissible 
for S-10 and S-11.  
 3 Conservative Assumption: All PM 10 emissions are equal to PM 2.5 
emissions. 
 485% abatement efficiency is applied to the PM emission factors from the 
Rypos DPF. 
 5SO2 emission factor from AP-42 Table 3.4-1 
 
𝐶𝐴𝑅𝐵 𝐷𝑖𝑒𝑠𝑒𝑙 𝑆𝑢𝑙𝑓𝑢𝑟 𝐶𝑜𝑛𝑡𝑒𝑛𝑡 =  15 𝑝𝑝𝑚 =  0.0015%  
𝑆𝑂ଶ𝐸𝑚𝑖𝑠𝑠𝑖𝑜𝑛 𝐹𝑎𝑐𝑡𝑜𝑟 ൬𝑔 
ℎ𝑝−ℎ𝑟൰=  8.09𝐸 −03×0.0015× 454 𝑔 
𝑙𝑏 
= 0.006𝑔
ℎ𝑝−ℎ𝑟Emissions Post
4/5/91  
(tons/yr) S-10 
Emissions  
(tons/yr)  S-11 
Emissions  
(tons/yr) Application 
Emissions  
(tons/yr) Cumulative 
Emissions  
(tons/yr) 
NOx 0.873 0.200 0.200 0.401 1.274 
POC 0.106 0.005 0.005 0.010 0.116 

 
 4Pollutant Existing 
Emissions Post 
4/5/91  
(tons/yr) S-10 
Emissions  
(tons/yr)  S-11 
Emissions  
(tons/yr) Application 
Emissions  
(tons/yr) Cumulative 
Emissions  
(tons/yr) 
CO 0.982 0.033 0.033 0.066 1.048 
PM10/PM2.5 0.017 0.000 0.000 0.001 0.018 
SO2 0.007 0.000 0.000 0.001 0.007 
1. As part of this project S-6 and S-7 were shutdown.Emissions1
(TPY) Application 
Annual 
Emissions2 
(TPY) Facility 
Annual 
Emissions 
(TPY) Offset 
Requirement 
(TPY) Offsets 
Required  
NOx 0.873 1.202 2.075 >10 N 
POC 0.106 0.030 0.136 >10 N 
CO 0.982 0.199 1.181 - N 
PM10/PM2.5 0.017 0.002 0.019  ≥100 N 
SO2 0.007 0.002 0.008  ≥100 N 
1. Existing emissions include the following: 
a. Registered boiler (S-1): Emissions from Application 30506, based on operation of 24 
hours/day and 365 days/year. 
b. Loss of exemption emergency engine (S-8): Emissions from Application 4448, based on 
Reliability-related activity of 20 hours. For the sake of the current PTE analysis, the 
 
 7reliability-related emissions have been conservatively based on 50 hr/yr and emergency 
operation of 100 hours.  
2. Annual emissions: Reliability-related activity of 50 hours and emergency operation of 100 hours 
for S-10 and S-11. 
 
Since the facility’s potential to emit is below the offsets trigger levels specified in 
Regulation 2-2, offsets are not required.Emission Standards BACT
Standards S-10 and S-11’s 
EPA Certified 
Emission Rates 
g/hp-hr g/hp-hr (g/hp-hr) (g/hp-hr) 
NOx + NHMC 4.8 4.8 4.8 4.04 
CO 2.6 2.6 2.6 0.67 
PM 0.15 0.15 0.15 0.006 
 
  
 
 12Permit Conditions 
 
Permit Condition #100072 for S-10 and S-11 
 
1. The owner or operator shall operate each emergency standby engine only for the 
following purposes: to mitigate emergency conditions, for emission testing to 
demonstrate compliance with a District, state or Federal emission limit, or for 
reliability-related activities (maintenance and other testing, but excluding emission 
testing). Operating while mitigating emergency conditions or while emission testing 
to show compliance with District, state or Federal emission limits is not limited. 
[Basis: Title 17, California Code of Regulations, section 93115, ATCM for 
Stationary CI Engines] 
 
2. The owner/operator shall operate each emergency standby engine only when a non-
resettable totalizing meter (with a minimum display capability of 9,999 hours) that 
measures the hours of operation for the engine is installed, operated and properly 
maintained. 
[Basis: Title 17, California Code of Regulations, section 93115, ATCM for 
Stationary CI Engines]  
 
3. Records: The owner/operator shall maintain the following monthly records in a 
District-approved log for at least 36 months from the date of entry (60 months if the 
facility has been issued a Title V Major Facility Review Permit or a Synthetic Minor 
Operating Permit). Log entries shall be retained on-site, either at a central location or 
at the engine’s location, and made immediately available to the District staff upon 
request.  
a. Hours of operation for reliability-related activities (maintenance and 
testing).  
b. Hours of operation for emission testing to show compliance with 
emission limits.  
c. Hours of operation (emergency).  
d. I For each emergency, the nature of the emergency condition. Fuel usage 
for each engine(s). 
[Basis: Title 17, California Code of Regulations, section 93115, ATCM 
for Stationary CI Engines] 
 
4. At School and Near-School Operation: If the emergency standby engine is located 
on school grounds or within 500 feet of any school grounds, the following 
requirements shall apply: The owner or operator shall not operate each stationary 
emergency standby diesel-fueled engine for non-emergency use, including 
maintenance and testing, during the following periods:  
a. Whenever there is a school sponsored activity (if the engine is located 
on school grounds)  
b. Between 7:30 a.m. and 3:30 p.m. on days when school is in session. 
'School' or 'School Grounds' means any public or private school used for the 
purposes of the education of more than 12 children in kindergarten or any of grades 
 
 131 to 12, inclusive, but does not include any private school in which education is 
primarily conducted in a private home(s). 'School' or 'School Grounds' includes any 
building or structure, playground, athletic field, or other areas of school property but 
does not include unimproved school property. 
[Basis: Title 17, California Code of Regulations, section 93115, ATCM for Stationary 
CI Engines] 
 
Permit Condition #100073 for S-10 and S-11 
 
The owner/operator shall not exceed the following limits per year per engine for 
reliability-related activities: 
 50 Hours of Diesel fuel (Diesel fuel) 
[Basis: Cumulative Increase; Regulation 2-5; Title 17, California Code 
of Regulations, section 93115, ATCM for Stationary CI Engines] 
 
End of Conditions

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

Plant Cumulative Increase
se 
Table 3 summarizes the criteria air pollutant emissions that will result from this 
application.  
 
Table 3. Plant Cumulative Emissions Increase, Post 4/5/91 
Pollutant Existing

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

S-10 and S-11 meet Airborne Toxic Control Measure (ATCM) Emission Standards of
engine power greater than 750 bhp. Reference: Title 17, California Code of Regulations 
Section 93115.6, ATCM, May 19, 2011, shown below. 
 
Figure 1. Emission Standard for New Stationary Emergency Standby Diesel-Fueled 
CI EnginesToxics Emissions for Health Risk Assessment (HRA)
At a maximum rate of 0.595 lb/year per engine (1.19 lb/yr total), the diesel particulate 
emissions from the project are greater than the toxic trigger level of 0.26 lb/year. All 
PM10 emissions are considered diesel particulate emissions. The PM emissions from this 
application are summarized in Table 2.  
 
A project shall include those new or modified sources of toxic air contaminants (TACs) 
at a facility that have been permitted within the five-year period immediately preceding 
the date a complete application is received. There are no other related projects permitted 
in the last five years.Since the diesel particulate emissions from the project are greater than the toxic trigger
level of 0.26 lb/year, an HRA is required. This application qualifies for a streamlined 
HRA. The nearest receptor is located between 300-800 feet from the proposed engines 
locations and the facility is not located in an Overburdened Comuunity (OBC); therefore, 
the maximum diesel PM emissions to qualify for HRA streamlining is 10 lb/year.  
 
S-10 and S-11 are subject to the District’s HRA streamlining policy for stationary Diesel-
fuel combustion engines used for backup power or fire pumps. The  HRA streamlining 
Microsoft Excel Spreadsheet checklist shows that a refined HRA is not required for this 
permit application.Control Technology for Toxics (TBACT) Workbook for IC Engine – Compression
Ignition: Stationary Emergency, non-Agricultural, non-direct drive fire pump 50 BHP 
and < 1000 BHP Output, Document #96.1.3, Revision 8, dated 12/22/2020. 
 
For NO X and CO, achieved-in-practice BACT has been determined to be meeting the 
CARB Air Toxics Control Measure (ATCM) standard for the respective pollutant at the 
applicable horsepower rating. 
 
Technologically Feasible and Cost-Effective 
The following control technologies and mitigation measures have been found technically 
feasible for abating NOx and CO emissions from internal combustion engines1: 
- Engine ignition timing retard (achievable NOx reduction 20 to 30 percent), and 
- Selective catalytic reduction (achievable NOx reduction of 90 percent) 
- Oxidation Catalyst (achievable CO reduction of 90 percent) 
 
Although Regulation 2-2 does not include a definition for cost-effectiveness, Section 2-2-
414 requires the Air District to publish and periodically update a BACT Workbook and 
that BACT will be determined using the workbook as a guidance document.  
 
Section 1 of the BACT Workbook includes a maximum cost guideline for NOx emissions 
of $17,500 per ton of emissions reduced. The BACT Workbook does not specify a 
maximum cost for CO. Therefore, the most recent published cost-effectiveness value 
from the South Coast Air Quality Management District (SCAQMD), $807 per ton of CO 
reduced (Q4 2023), will be used as a reference. 
 
Using these maximum cost effectiveness values and assuming that 90 percent of the 
emissions in Table 2 could be abated, maximum annualized costs for NOx controls could 
not exceed $3,150 to be deemed cost-effective.  
 
𝑀𝑎𝑥𝑖𝑚𝑢𝑚  𝑁𝑂௑ 𝐶𝑜𝑛𝑡𝑟𝑜𝑙 𝐶𝑜𝑠𝑡= 17,500$
𝑡𝑜𝑛×0.200𝑡𝑜𝑛
𝑦𝑟×0.90 = $3,150  
 
1 United States Environmental Protection Agency. Control Techniques Guidelines for Alternative Control Techniques 
Document – NOx Emissions from Stationary Reciprocating Internal Combustion Engines. EPA-453/R-93-032. July 
1993. Updated September 2000.  
 
 6 
The maximum annualized costs for CO controls could not exceed $23.97 to be deemed 
cost-effective.  
 
𝑀𝑎𝑥𝑖𝑚𝑢𝑚  𝐶𝑂 𝐶𝑜𝑛𝑡𝑟𝑜𝑙 𝐶𝑜𝑠𝑡= 807$
𝑡𝑜𝑛×0.033𝑡𝑜𝑛
𝑦𝑟×0.90 = $23.97  
 
All NOx and CO controls are expected to exceed maximum annualized costs. Therefore, 
requiring more stringent controls than meeting achieved-in-practice requirements is 
deemed not cost-effective.  
 
Consequently, S-10 and S-11 are required to comply with the current achieved-in-
practice standards: 
 
 Pollutant Emission Factor BACT(2) Standard 
 NOx  4.04 g/bhp-hr  4.56 g/bhp-hr 
 CO  0.90 g/bhp-hr  2.6 g/bhp-hr 
 
Note: The standard is expressed as non-methane hydrocarbons (NMHC) + NOx. NOx is 
estimated to be 95% of the combined standard.CARB Airborne Toxic Control Measures (ATCM)
Pursuant to §93115.6(a)(3), a new engine must meet the following requirements as of 
January 1, 2005. 
 
 ATCM “Table 1 Emission Standards for New Stationary Emergency Standby 
Diesel-Fueled CI Engines” for same model year and maximum engine power. 
 
 10 After December 31, 2008, be certified to the new non-road compression-ignition 
engine emission standard for all pollutants for 2007 and later model year engines 
as specified in 40 CFR, Part 60, Subpart IIII; and, 
 Not operate more than 50 hours per year for maintenance and testing purposes, 
except as provided in §93115.6(a)(3)(A)(2). This regulation does not limit engine 
operation for emergency use and for emission testing to show compliance with 
§93115.6(a)(3). 
 
The engines are expected to meet the aforementioned emission requirements as seen in 
Figure 1 and will be limited, through permit condition, to operate unrestricted only for 
emergencies and a maximum of 50 hours per year for maintenance and testing purposes. 
 
New Source Performance Standards (NSPS) 
Subpart IIII - Stationary Compression Ignition Internal Combustion Engines: 
According to §60.4200(a)(1)(i), the engines are subject to the requirements of 40 CFR 
Part 60 Subpart IIII, “Standards of Performance of Stationary Compression Ignition 
Internal Combustion Engines.” 
 
Pursuant to §60.4205(b), owners or operators of 2007 model year and later stationary 
emergency diesel engine-generator sets with a displacement of less than 10 liters per 
cylinder must meet the emission standards established in 40 CFR 1039, Appendix I and 
smoke standards specified in 40 CFR 1039.105.  
 
The engines are also expected to meet the fuel standards of 40 CFR 1090.305. The 
requirement for a non-resettable hour meter (as per §60.4209(a)) will be enforced as a 
permit condition.  
 
National Emissions Standards for Hazardous Air Pollutants (NESHAP) 
Subpart ZZZZ - Stationary Reciprocating Internal Combustion Engines: Pursuant to 
§63.6585, engines located at an area source are subject to the requirements of 40 CFR 
Part 63 Subpart ZZZZ, “National Emission Standards for Hazardous Air Pollutants for 
Stationary Reciprocating Internal Combustion Engines.” However, according to 
§63.6590(a)(1)(iii) & §63.6590(c)(1), diesel engines that commenced construction on 
June 12, 2006 or later and that operate at a facility that emits or has the potential to emit 
any single hazardous air pollutant (HAP) at a rate of less than 10 tons per year or any 
combination of HAPs at a rate of less than 25 tons per year, must comply instead with 40 
CFR Part 60 Subpart IIII, “Standards of Performance of Stationary Compression Ignition 
Internal Combustion Engines.” The engines are expected to meet the requirements of this 
subpart by meeting the standards of 40 CFR Part 60 Subpart IIII, “Standards of 
Performance of Stationary Compression Ignition Internal Combustion Engines.” 
 
 
 11Table 5. Comparison of NSPS, CARB ATCM and BACT Emission Standards with 
the Engine’s Emission Rates  
Pollutant NSPS Emission 
Standards CARB ATCM

## BACT
JSONPath: `$.BACT.text`

Best Available Control Technology (BACT)
T) 
In accordance with Regulation 2-2-301, BACT is triggered for any new or modified 
source with the potential to emit 10 pounds or more per highest day of POC, NPOC, 
NOx, CO, SO 2, or PM 10 /PM2.5.  
 
Per Section 2-2-202, BACT is defined as an emission limitation, control device, or 
control technique applied at a source that is the most stringent of: 
- the most effective device or technique successfully utilized, 
- the most stringent emission limitation achieved by an emission control device or 
technique for the type of equipment comprising such a source, 
- the most effective emission control limitation for the type of equipment 
comprising such a source that is contained in an approved implementation plan of 
any state, or 
- the most effective control device or technique or most stringent emission 
limitation that is technologically feasible, taking into consideration cost-
 
 5effectiveness, any ancillary health and environmental impacts, and energy 
requirements. 
 
These requirements are generally categorized as either technologically feasible and cost-
effective (termed “BACT 1”) or achieved-in-practice (termed “BACT 2”). 
 
BACT 2 is either equal to or less stringent than BACT 1. Because achieved-in-practice is 
required regardless of cost and BACT 1 is more stringent than BACT 2, an evaluation for 
what has been achieved-in-practice is first conducted. 
 
Achieved-in-Practice 
Achieved-in-practice BACT is presented in the current BAAQMD BACT/ Best Available

## offsets
JSONPath: `$.offsets.narrative`

Offsets
ts 
Offset must be provided for any new or modified source at a facility that will have the 
potential to emit more than 10 tons per year of NOx or POC, as specified in Regulation 2-
2-302; 100 tons per year or more of PM 2.5, PM10 or SO 2, as specified in Regulation 2-2- 
303. 
 
In accordance with the Air District’s Policy for Calculating Potential to Emit (PTE) for 
Emergency Backup Power Generators, the PTE for S-10 and S-11 was estimated 
assuming 150 hours of operation per year (50 hours per year for reliability-related and 
testing operation + 100 hours per year for emergency operation).  
 
Table 4. Potential to Emit for FID 11308 
Pollutant Existing 
Annual

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

Prevention of Significant Deterioration (PSD): This facility will not have the potential
to emit more than 100 tons per year of any criteria pollutant, therefore this facility is not a 
“Major Facility” as defined in the Air District Regulation 2-2-217 and is not subject to 
PSD permitting requirements under Regulation 2-2-304. 
 
Regulation 2, Rule 5 
The engines are expected to exceed the diesel exhaust PM trigger level of 0.26 lbs per 
year. Thus, the provisions of this rule apply to S-10 and S-11.  
 
S-10 and S-11 qualified for a streamlined HRA. The assessment resulted in a maximum 
cancer risk of 9.9 in a million, the acute hazard index was 0.10 and the chronic hazard 
index was 0.10. Per Regulation 2-5-301, TBACT applies for any new or modified sources 
if their cancer risk exceeds 1.0 in a million. S-10 and S-11 meet the Air District’s 
TBACT standard of 0.15 g/bhp-hr for diesel PM as it has a certified PM emission factor 
of 0.04 g/bhp-hr. This project is in compliance with Regulation 2-5-302 requirements for 
sources not located within an OBC as defined in Regulation 2-1-243.  
 
Regulation 6, Rule 1 
Ringelmann No. 2 Limitation:  Pursuant to Regulation 6-1-303 a person shall not emit, 
from an internal combustion engine with less than a 25-liter displacement, for a period or 
periods aggregating more than three minutes in any hour, a visible emission that is as 
dark or darker than No. 2 on the Ringelmann Chart, or of such opacity as to obscure an 
observer’s view to an equivalent or greater degree, nor shall said emission, as perceived 
by an opacity sensing device in good working order, where such device is required by Air 
District Regulations, be equal to or greater than 40% opacity. The engines are expected to 
meet the requirements of Regulation 6-1-303. 
 
Visible Particles:  Section 305 prohibits emissions of visible particles from the operator’s 
property causing a nuisance on another property. The facility is expected to comply with 
this standard.  
 
 
 9Total Suspended Particulate (TSP) Concentration Limits:  The TSP concentration limit 
of 0.15 grain per dscf established in Regulation 6-1-310.1 is not expected to be exceeded 
by S-10 or S-11 since the maximum PM emissions from S-10 and S-11 are expected to be 
0.0009 gr/dscf as shown in calculation below.  
 
0.012൬𝑃𝑀 𝑝𝑜𝑢𝑛𝑑
ℎ𝑜𝑢𝑟൰ 𝑥 7,000𝑔𝑟𝑎𝑖𝑛𝑠
𝑝𝑜𝑢𝑛𝑑𝑥 1 ℎ𝑜𝑢𝑟
60 𝑚𝑖𝑛 𝑥1 𝑚𝑖𝑛
1,525 𝑑𝑠𝑐𝑓=  0.0009 𝑔𝑟/𝑑𝑠𝑐𝑓 
 
Regulation 9, Rule 1  
Fuel Burning (Liquid and Solid Fuels): A person shall not burn any liquid fuel having a 
sulfur content in excess of 0.5% by weight, or solid fuel of such sulfur content as would 
result in the emission of a gas stream containing more than 300 ppm (dry) of sulfur 
dioxide. The sulfur content of diesel is expected to be 0.0015%. 
 
Regulation 9, Rule 8  
This rule limits the emissions of NO x and CO from stationary internal combustion 
engines with an output rated by the manufacturer at more than 50 bhp. 
 
The engines are intended to operate at a specific site for more than one year and will be 
attached to a foundation at the site. Therefore, the requirements of this rule apply. 
Pursuant to Regulation 9-8-110.5, emergency standby engines are exempt from the 
requirements of Regulations 9-8-301 through 305, 9-8-501 and 9-8-503. 
 
Per Regulation 9-8-330, S-10 and S-11 will be used for unlimited hours in case of 
emergencies and up to 50 hours per year for reliability related activities.  
 
In accordance with Regulation 9-8-530, the engines shall be equipped with a non-
resettable totalizing meter that measures hours of operation or fuel usage. Monthly 
records for the following shall be kept for at least 2 years and be made available to Air 
District staff upon request. 
 
 Total hours of operation; 
 Emergency hours of operation; and, 
 The nature of the emergency condition for each emergency. 
 
The engines are expected to meet the aforementioned requirements. 
 
State Rules

## CEQA
JSONPath: `$.CEQA.narrative`

California Environmental Quality Act (CEQA): This permit application is categorically
exempt from CEQA because the project has no potential for causing a significant adverse 
environmental impact. In addition, the application is categorically exempt from CEQA 
under CEQA Guidelines Section 15301, Class 1: Existing Facilities (also known as “No 
or Negligible Expansion of Existing Use” or “Minor Alterations to Existing Facilities”). 
In making the determination that this application is categorically exempt: 1) the Air 
District reviewed the CEQA-related information from the applicant in the form of a 
completed Appendix H form (Regulation 2-1-426-1) indicating that there is no potential 
for a significant adverse environmental impact from the project.

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
Statement of Compliance
ce 
The owner/operator is expected to comply with all applicable requirements. Key 
requirements are listed below: 
 
Regulation 1 
The engines are subject to and expected to be in compliance with the requirements of 
Regulation 1-301 (Public Nuisance). 
 
Regulation 2, Rule 1 
Pursuant to Regulation 2-1-114.2.1, internal combustion engines greater than 50 hp are 
subject to the requirements of Regulation 2-1. According to Regulation 2-1-301, prior to 
the installation of the equipment, an ATC must be obtained. The facility has submitted an 
application and is expected to be in compliance with Regulation 2-1.

## public_notification
JSONPath: `$.public_notification.text`

School Notification (Regulation 2-1-412):  The public notification requirements of
Regulation 2-1-412 apply to applications which result in any increase in TACs or 
hazardous air contaminant emissions at facilities within, either 1,000 feet of the boundary 
of a K-12 school, or located in an OBC. The project is located within 1,000 feet of a 
school, therefore, the project is subject to the public notification requirements of 
Regulation 2-1-412. A public notice was prepared and sent to the following school within 
1,000 feet of the project: 
 
Loma Vista Immersion Academy Elementary 
 
207 Maria Dr. 
Petaluma, CA 94954 
 
 
 
 
 8Regulation 2, Rule 2 
BACT: Pursuant to Regulation 2-2-301, BACT is required for a new source with 
potential to emit equal to 10.0 lbs or greater of POC, NPOC, NO x, SO2, PM10, PM2.5, or 
CO per day. The engines exceed the BACT threshold for NO x and CO. However, as 
discussed earlier, the engines meet the BACT requirement for NO x and CO in accordance 
with the Air District’s BACT/TBACT Workbook. 
 
Offsets: Air District Regulation 2-2-302 requires offsets for new or modified sources at a 
facility that has the potential to emit 10 tpy or more of POC and NOx. Air District 
Regulation 2-2-303 requires offsets for new or modified sources at a facility that has the 
potential to emit 100 tpy or more of PM 2.5, PM10, and SO 2. The facility will not exceed 10 
tpy of POC or NOx and 100 tpy of PM 2.5, PM10, or SO 2 and therefore is not subject to 
offsets.Regulation 2-1-412. After the comments are received and reviewed, the Air District will
make a final determination on the permit. 
 
I recommend that the Air District initiate a public notice and consider any comments 
received prior to taking final action on the following: 
 
S-10 Emergency Standby Diesel Generator 
Engine Make: Caterpillar, Model: C18, Model Year: 2025,  
EPA Family Name: RCPXL18.1NYS, 900 bhp, 5.77 MMBtu/hr  
 
Abated by 
 
A-10 Rypos Active Diesel Particulate Filter (DPF), Model: Rypos Active  
DPF/C3+TM System, CARB Certified per Executive Order DE-13-002-07 
 
S-11 Emergency Standby Diesel Generator 
Engine Make: Caterpillar, Model: C18, Model Year: 2025,  
EPA Family Name: RCPXL18.1NYS, 900 bhp, 5.77 MMBtu/hr  
 
Abated by 
 
A-11 Rypos Active Diesel Particulate Filter (DPF), Model: Rypos Active  
 
 14DPF/C3+TM System, CARB Certified per Executive Order DE-13-002-07 
 
I recommend shutting-down the following two sources: 
 
S-6 Emergency Standby Diesel Generator, Cummins Model KTA1150GA, 560  
BHP, 400 kW 
 
S-7 Emergency Standby Diesel Generator, Detroit Disel Model 16V-92T, 540  
BHP, 385 kW 
 
Prepared By:  Emily Schwartz, Air Quality Engineer I  
 
 15Attachment 1 
 
 
 

 
 16

## conditions
JSONPath: `$.conditions.text`

(empty)

## permit_conditions
JSONPath: `$.permit_conditions`

(empty)

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

Recommendation
on 
The Air District has reviewed the material contained in the permit application for the 
proposed project and has made a preliminary determination that the project is expected to 
comply with all applicable requirements of District, state, and federal air quality-related 
regulations. The preliminary recommendation is to issue  an Authority to Construct for 
the equipment listed below. However, the proposed sources will be located within 1,000 
feet of a school which triggers the public notification requirements of Air District
