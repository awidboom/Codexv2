---
application_number: 722891
plant_name: California Department of Technology (Hut 193)
plant_address: San Mateo, CA 94403
evaluation_date: September 4, 2025
source_json: data/permit_evaluations_json/2025/2025-722891-California_Department_of_Technology_Hut_193__fid203871_nsr_722891_eval_091625_pdf__application_722891__eval_01.json
---

# Engineering Evaluation (Application 722891)
**Plant**:  California Department of Technology (Hut 193)
**Address**: San Mateo, CA 94403
**Evaluation Date**: September 4, 2025

## background
JSONPath: `$.background.text`

Background
ound    
California Department of Technology (Hut 193) is applying for an Authority to Construct 
(AC) for the following equipment:  
 
S-1 Emergency Standby Liquefied Petroleum Gas (LPG) Engine 
Make: Kohler Co., Model: KG6208, Model Year: 2023 
103 BHP, 1.05 MMBTU/hr Abated by A-1 
 
A-1 Nett Technologies Inc.- TG Series Catalytic Converter

## emission_calculations
JSONPath: `$.emission_calculations.text`

Emission Calculations
ns 
Emission factors for nitrogen oxides (NOx), precursor organic compounds (POC), and carbon 
monoxide (CO) were obtained from the engine manufacturer.  Particulate matter (PM 10/PM2.5) and 
sulfur dioxide (SO 2) emission factors are based on AP 42, Fifth Edition, Volume I, Chapter 3: 
Stationary Internal Combustion Sources, Section 3.2.4.1 Control Techniques for 4-Cycle Rich-
Burn Engines and Table 3.2-3 Uncontrolled Emission Factors for 4-Stroke Rich-Burn 
Engines.1  The engine will operate for emergency purposes and will be limited to a maximum of 
50 hours per year for maintenance and testing.  
 
Table 1.  Hourly, Daily, and Annual Emissions from S-1 
Pollutant Unabated 
Emission 
Factor (g/hp-
hr) Abateme
nt 
Efficiency 
(% w/w) Abated 
Emission 
Factor 
(g/hp-hr)  
HourlyEmissions
(lb/hr) Maximum 
Daily 
Emissions 
(lb/day) Annual 
Emissions 
(lb/yr) Annual 
Emissions 
(TPY) 
NOx 5.00 98 0.10 0.02 0.54 1.13 0.001 
POC 1.19 50 0.60 0.14 3.25 6.77 0.003 
CO 22.69 94 1.36 0.31 7.41 15.44 0.008 
PM10/PM2.5 0.09 N/A N/A 0.02 0.49 1.02 0.001 
SO2 N/A N/A N/A 0.00 0.01 0.03 0.000 
Basis:  
 103 bhp Max Rated Output 
 410 scf/hr Max fuel use Rate = 1.05 MMBTU/hr 
 NOx, POC and CO emission factors are from the engine manufacturer. 
 NOx and CO abatement efficiencies are from the abatement device manufacturer and are 98% and 94% by 
weight, respectively.  POC abatement efficiency is assumed to be 50% by weight. 
 
  PM10/PM2.5 and SO 2 emission factors are from EPA AP-42, Table 3.2-3 Uncontrolled Emission Factors for  
4-Stroke Rich-Burn Engines.  The PM 10/PM2.5 emission factor is the total of filterable and condensable 
particulates. 
 Annual Emissions are based on an annual limit (50 hr/yr) for testing and maintenance. 
 Max daily emissions are based on 24 hr/day since no daily limits are imposed on emergency operations. 
 SO2 Emission Factor = 5.88 E-04 lb /MMBtu; calculations assume 100% of fuel sulfur conversion with the content 
in CA natural gas = 10,000 gr/106scf.   
 PM10/PM2.5 fuel input emission factor = 9.50E-03 lb/MMBtu (filterable) + 9.91E-03 lb/MMBtu (condensable) = 
1.94E-02 lb/MMBtu; aerodynamic particle diameter =< 1 µm, for the purposes of filterable emissions PM 10= PM2.5.  
These emissions are expected to be negligible but included for completeness.

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

Plant Cumulative Emissions
Table 3 summarizes the cumulative increase in criteria pollutant emissions that will result from the 
operation of S-1. 
Table 3.  Plant Cumulative Emissions Increase, Post 4/5/91  
Pollutant Existing Emissions 
Post 4/5/91 
(ton/yr) Application 
Emissions 
(ton/yr) Cumulative 
Emissions 
(ton/yr) 
NOx 0.000 0.001 0.001 
POC 0.000 0.003 0.003 
CO 0.000 0.008 0.008 
PM10/PM2.5 0.000 0.001 0.001 
SO2 0.000 0.001 0.001

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

Health Risk Assessment (HRA)
A) 
Pursuant to Regulation 2-5-110, a project, including all new or modified sources of toxic air 
contaminants (TAC) within a 5-year period, is not subject to this rule if the total project emissions 
are below the acute and chronic trigger levels listed in Table 2-5-1 “Toxic Air Contaminant Trigger 
Levels” of this regulation. 
The emission factors are from the California Air Toxics Emission Factors (CATEF) and the 
Compilation of Air Pollutant Emissions Factor: AP-42.  CATEF emission factors are preferentially 
chosen over AP-42 factors.  If the AP-42 emission factor is based on the detection limit, the 
emission factor will equal 1/2 of the AP-42 emission factor.Table 2.  Toxic Air Contaminant Review for Engine
Compound Emission 
Factor 
(lb/MMB
tu) Basis Hourly 
Emission 
Rate 
(lb/hr) Acute 
Trigger 
Level 
(lb/hr) Annual 
Emission 
Rate 
(lb/yr) Chronic 
Trigger 
Level 
(lb/yr) Exceeds 
Acute or 
Chronic 
Trigger 
Level? 
1,1,2,2-Tetrachloroethane 2.38E-03 AP-42 1.3E-05 None 6.7E-04 1.4E+00 No 
1,1,2-Trichloroethane 1.44E-03 AP-42 8.1E-06 None 4.0E-04 5.0E+00 No 
1,1-Dichloroethane 1.06E-03 AP-42 5.9E-06 None 3.0E-04 5.0E+01 No 
1,3-Butadiene 1.04E-04 CATEF 5.8E-07 1.5E+00 2.9E-05 4.8E-01 No 
Acetaldehyde 8.83E-04 CATEF 4.9E-06 1.0E+00 2.5E-04 2.9E+01 No 
Acrolein 5.47E-04 CATEF 3.1E-06 5.5E-03 1.5E-04 1.4E+01 No 
Benzene (no control) 1.91E-03 CATEF 1.1E-05 6.0E-02 5.3E-04 2.9E+00 No 
Carbon Tetrachloride 1.66E-03 AP-42 9.3E-06 4.2E+00 4.7E-04 1.9E+00 No 
Chlorobenzene 1.21E-03 AP-42 6.8E-06 None 3.4E-04 3.9E+04 No 
Chloroform 1.29E-03 AP-42 7.2E-06 3.3E-01 3.6E-04 1.5E+01 No 
Ethylbenzene 1.16E-05 CATEF 6.5E-08 None 3.2E-06 3.3E+01 No 
Ethylene Dibromide 2.00E-03 AP-42 1.1E-05 None 5.6E-04 1.1E+00 No 
Formaldehyde (no control) 2.35E-03 CATEF 1.3E-05 1.2E-01 6.6E-04 1.4E+01 No 
Methanol 2.88E-01 AP-42 1.6E-03 6.2E+01 8.1E-02 1.5E+05 No 
Methylene Chloride 3.87E-03 AP-42 2.2E-05 3.1E+01 1.1E-03 8.2E+01 No 
Naphthalene 7.65E-05 CATEF 4.3E-07 None 2.1E-05 2.4E+00 No 
PAH 1.82E-07 CATEF 1.0E-09 None 5.1E-08 3.3E-03 No 
Propylene 1.60E-02 CATEF 9.0E-05 None 4.5E-03 1.2E+05 No 
 
 Compound Emission 
Factor 
(lb/MMB
tu) Basis Hourly 
Emission 
Rate 
(lb/hr) Acute 
Trigger 
Level 
(lb/hr) Annual 
Emission 
Rate 
(lb/yr) Chronic 
Trigger 
Level 
(lb/yr) Exceeds 
Acute or 
Chronic 
Trigger 
Level? 
Styrene 1.12E-03 AP-42 6.3E-06 4.6E+01 3.1E-04 3.5E+04 No 
Toluene 1.07E-03 CATEF 6.0E-06 8.2E+01 3.0E-04 1.2E+04 No 
Vinyl Chloride 6.75E-04 AP-42 3.8E-06 4.0E+02 1.9E-04 1.1E+00 No 
Xylene (total) 6.58E-04 CATEF 3.7E-06 4.9E+01 1.8E-04 2.7E+04 No 
Basis: 
 Abatement efficiency by add-on catalyst is assumed to be 50% by weight for each TAC above and has been 
applied to the emission calculations in Table 2 above. 
 
The project does not exceed any acute or chronic trigger level.  Therefore, the project is not subject 
to the requirements of Regulation 2-5-110.

## BACT
JSONPath: `$.BACT.text`

Best Available Control Technology (BACT)
Pursuant to Regulation 2-2-301, Best Available Control Technology (BACT) shall apply to new or 
modified sources with a Potential to Emit equal to or greater than 10 lb per highest day of the 
pollutants in Table 1.   
BACT is not triggered for any pollutant since the maximum daily emission of each pollutant does 
not exceed 10 lb/day.

## offsets
JSONPath: `$.offsets.narrative`

Offsets
ts 
Per Regulation 2-2-302, offsets must be provided for any new or modified source at a facility that has the 
potential to emit (PTE) more than 10 tons/yr of POC or NOx.  The PTE for emergency-use engines will 
include the hours allowed for test and maintenance, as well as an assumed 100 hours per year for 
emergencies.  Based on the emission calculations in Table 4, offsets are not required for this application.  
 
Table 4. Potential to Emit for Plant# 203871 
 
 Pollutant Existing 
Annual 
Emissions 
(ton/yr) Application 
Annual 
Emission 
(ton/yr) Facility 
Annual 
Emissions 
(ton/yr) Offset 
Requirement 
(ton/yr) Offset 
Required?  
NOx 0.000 0.002 0.002 10 N 
POC 0.000 0.010 0.010 10 N 
CO 0.000 0.023 0.023 - N 
PM10/PM2.5 0.000 0.002 0.002 100 N 
SO2 0.000 0.000 0.000 100 N 
 
New Source Performance Standards 
The New Source Performance Standard (NSPS) in 40 CFR 60, Subpart JJJJ apply because the engine will 
be installed after June 12, 2006 and manufactured after January 1, 2009.  The engine will comply with the 
following limits in 40 CFR 1048, pursuant to 40 CFR 60, Subpart JJJJ Section 60.4231(C) for emergency 
spark-ignited, rich burn, LPG engines less than 130 hp: 
 
Pollutant S-1 Emission Factor 
(Abated) NSPS Standard 
NOx              0.10 g/bhp-hr 10 g/bhp-hr 
CO               1.36 g/bhp-hr 387 g/bhp-hr 
  
As the information above shows, S-1 is in compliance with these NSPS emission requirements. 
National Emission Standards for Hazardous Air Pollutants (NESHAP) 
This engine will be operated at a hazardous air pollutant (HAP) area source.  Therefore, the engine 
will be subject to the Reciprocating Internal Combustion Engine (RICE) National Emission 
Standards for Hazardous Air Pollutants (NESHAP) (40 CFR Part 63, Subpart ZZZZ) because it is 
a new source and installed after 2007.  A new RICE at an area source that is subject to 40 CFR 
Part 60, Subpart JJJJ, has no further requirements under 40 CFR Part 63, Subpart ZZZZ pursuant 
to 40 CFR Part 63.6590(c).  Therefore, S-1 complies with the NESHAP by meeting the 
requirements under 40 CFR Part 60, Subpart JJJJ.

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

(empty)

## CEQA
JSONPath: `$.CEQA.narrative`

This permit application is not subject to the California Environmental Quality Act (CEQA) 
because the Air District’s evaluation is a ministerial action (Public Resources Code Section 
21080(b)(1) and CEQA Guidelines Section 15268(a)) conducted using the fixed standards and 
objective measurements in the Air District’s rules and regulations.  
 
 
 
 Regulation 2-1 Public Notice Requirements 
Because this equipment will be located within 1,000 feet of College Park Elementary School, 
located at 1001 Bermuda Dr, San Mateo, CA 94403. The project is subject to the public 
notification requirements of Regulation 2-1-412 due to the increase in emissions from the 
project. A public notice will be sent to all parents of students of the above mentioned school(s) 
and all residents within 1,000 feet of the facility. There will be a 30-day public comment period.

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
Statement of Compliance
ce 
Regulation 6-1 
The owner/operator of S-1 shall comply with Regulation 6, Rule 1 ( Particulate Matter and Visible 
Emissions Standards ). 
6-1-310.1 No person shall emit TSP from any source in excess of 343 mg per dscm (0.15gr per 
dscf) of exhaust gas volume. 
6-1-310.2 Effective July 1, 2020, Table 6-1-310.2 emission limits shall apply to any source with a 
Potential to Emit TSP (as defined in Regulation 2-1-217) greater than 1,000 kg per year. No 
applicable source shall emit TSP at a concentration in excess of the limit indicated for the source’s 
Exhaust Gas Rate in Table 6-1-310.2. 
 
 The engine does not emit more than 1000 kg/year of PM 10. Therefore, only section 6-1-310.1 
applies to this project. The engine’s maximum exhaust flow rate is 478 acfm = 7667.012 dscf/hr 
and the PM 10 emissions are equal to 143.04 gr/hr.  
TSP Concentration can be calculated using the formula below: 
𝐸𝑛𝑔𝑖𝑛𝑒 𝑃𝑀10 𝐻𝑜𝑢𝑟𝑙𝑦 𝐸𝑚𝑖𝑠𝑠𝑖𝑜𝑛𝑠  (𝑔𝑟
ℎ𝑟)
ቆ𝐷𝑟𝑦 𝐸𝑛𝑔𝑖𝑛𝑒 𝑀𝑎𝑥𝑖𝑚𝑢𝑚  𝐸𝑥ℎ𝑎𝑢𝑠𝑡 𝐹𝑙𝑜𝑤 𝑅𝑎𝑡𝑒൬𝑑𝑠𝑐𝑓
ℎ𝑟൰ቇ=𝑇𝑆𝑃 𝐶𝑜𝑛𝑐𝑒𝑛𝑡𝑟𝑎𝑡𝑖𝑜𝑛  (𝑔𝑟
𝑑𝑠𝑐𝑓) 
Thus, TSP Concentration for the engine is: 
143.04 (𝑔𝑟
ℎ𝑟)
ቆ7667൬𝑑𝑠𝑐𝑓
ℎ𝑟൰ቇ= 0.019 𝑔𝑟/𝑑𝑠𝑐𝑓 
 
The TSP Concentration is below the allowable limit of 0.15 gr/dscf for the source within the 
project. 
Regulation 9-1 
Regulation 9-1-301 ( Inorganic Gaseous Pollutants: Sulfur Dioxide for Limitations on Ground 
Level Concentrations ). From Regulation 9-1-301, the ground level concentrations of SO 2 will not 
exceed 0.5 ppm continuously for 3 consecutive minutes or 0.25 ppm averaged over 60 consecutive 
minutes, or 0.05 ppm averaged over 24 hours. 
 
Regulation 9-8 
S-1 is an emergency standby generator; from Regulation 9, Rule 8 ( NOx and CO from Stationary 
Internal Combustion Engines ), Section 110.5 ( Emergency Standby Engines ), S-1 is exempt from 
the requirements of Regulations 9-8-301 ( Emission Limits on Fossil Derived Fuel Gas ), 9-8-302 
(Emission Limits on Waste Derived Fuel Gas ), 9-8-303 ( Emissions Limits – Delayed Compliance, 
Existing Spark-Ignited Engines, 51 to 250 bhp or Model Year 1996 or Later ), 9-8-304 ( Emission 
Limits – Compression-Ignited Engines ), 9-8-305 ( Emission Limits – Delayed Compliance, Existing 
Compression-Ignited Engines, Model Year 1996 or Later ), 9-8-501 ( Initial Demonstration of 
Compliance ) and 9-8-503 ( Quarterly Demonstration of Compliance ). 
 
Allowable operating hours and the corresponding record keeping in Regulations 9-8-330 
(Emergency Standby Engines, Hours of Operation ) or Regulation 9-8-331 (Essential Public 
Service, Hours of Operation) and 9-8-530 ( Emergency Standby Engines, Monitoring and 
Recordkeeping ) will be included in the Permit Conditions below. 
Regulation 2-1 CEQA Review 
This permit application is not subject to the California Environmental Quality Act (CEQA) 
because the Air District’s evaluation is a ministerial action (Public Resources Code Section 
21080(b)(1) and CEQA Guidelines Section 15268(a)) conducted using the fixed standards and 
objective measurements in the Air District’s rules and regulations.  
 
 
 
 Regulation 2-1 Public Notice Requirements 
Because this equipment will be located within 1,000 feet of College Park Elementary School, 
located at 1001 Bermuda Dr, San Mateo, CA 94403. The project is subject to the public

## public_notification
JSONPath: `$.public_notification.text`

notification requirements of Regulation 2-1-412 due to the increase in emissions from the
project. A public notice will be sent to all parents of students of the above mentioned school(s) 
and all residents within 1,000 feet of the facility. There will be a 30-day public comment period.triggers the public notification requirements of Air District Regulation 2-1-412. After the
comments are received and reviewed, the Air District will make a final determination on the 
permit.  
 
I recommend that the Air District initiate a public notice and consider any comments received 
prior to taking any final action on issuance of an Authority to Construct for the following. 
 
S-1 Emergency Standby Liquefied Petroleum Gas (LPG) Engine  
Make: Kohler Co., Model: KG6208, Model Year: 2023 
103 BHP, 1.05 MMBTU/hr Abated by A-1 
 
A-1 Nett Technologies Inc.- TG Series Catalytic Converter 
 
 
Prepared by: Udval Argo 
Air Quality Technician I  
September 4, 2025       
 
 Table 1 to Subpart JJJJ of Part 60—NO X, CO, and VOC Emission Standards for Stationary Non-Emergency 
SI Engines ≥100 HP (Except Gasoline and Rich Burn LPG), Stationary SI Landfill/Digester Gas Engines, and 
Stationary Emergency Engines >25 HP

## conditions
JSONPath: `$.conditions.text`

Permit Conditions
Permit Condition No. 23113 for S-1  
    1.  Operating for reliability-related activities are limited 
    to 50 hours per year per engine (Basis: Regulation 9-8- 
    330.3) 
2.  The owner/operator shall operate the stationary 
    emergency standby engine only for the following 
    purposes: to mitigate emergency conditions, for emission 
    testing to demonstrate compliance with a District, State 
    or Federal emission limit, or for reliability related 
    activities (maintenance and other testing but excluding 
    emission testing). Operating while mitigating emergencyconditions or while emission testing to show compliance
ance 
    with District, State, or Federal emission limits is not 
    limited. (Basis: Regulation 9-8-330) 
3.  The owner/operator shall operate each emergency standby 
    engine(s) only when a non-resettable totalizing meter 
    (with a minimum display capability of 9,999 hours) that 
    measures hours of operation for the engine is installed, 
    operated, and properly maintained. (Basis: Regulation 9- 
    8-530) 
4.  The owner/operator shall not operate the liquid 
    petroleum gas fired engine unless it is abated with an 
    integral or add-on three-way catalyst, or other approved 
    abatement device. (Basis: Cumulative Increase) 
5.  Records: The owner/operator shall maintain the following 
    monthly records in a District approved log for at least 
    24 months from the date of entry (60 months if the 
    facility has been issued a Title V Major Facility Review 
    Permit or a Synthetic Minor Operating Permit). Log 
    entries shall be retained on site, either at a central 
    location or at the engine's location, and made 
    immediately available to the District staff upon 
    request. 
    a.  Hours of operation for reliability related 
        activities (maintenance and testing). 
    b.  Hours of operation for emission testing. 
 
     c.  Hours of operation (emergency). 
    d.  For each emergency, the nature of the emergency 
        condition. 
    e.  Fuel usage or operating hours for engine. 
   (Basis: Regulations 9-8-502 and 9-8-530) 
 
End of Conditions

## permit_conditions
JSONPath: `$.permit_conditions`

Condition number: 23113
- Item 1
Operating for reliability-related activities are limited 
    to 50 hours per year per engine (
Basis: Regulation 9-8-

- Item 330
3)

- Item 2
The owner/operator shall operate the stationary 
    emergency standby engine only for the following 
    purposes: to mitigate emergency conditions, for emission 
    testing to demonstrate compliance with a District, State 
    or Federal emission limit, or for reliability related 
    activities (maintenance and other testing but excluding 
    emission testing). Operating while mitigating emergencyconditions or while emission testing to show compliance
ance 
    with District, State, or Federal emission limits is not 
    limited. (
Basis: Regulation 9-8-330)

- Item 3
The owner/operator shall operate each emergency standby 
    engine(s) only when a non-resettable totalizing meter 
    (with a minimum display capability of 9,999 hours) that 
    measures hours of operation for the engine is installed, 
    operated, and properly maintained. (
Basis: Regulation 9- 
    8-530)

- Item 4
The owner/operator shall not operate the liquid 
    petroleum gas fired engine unless it is abated with an 
    integral or add-on three-way catalyst, or other approved 
    abatement device. (
Basis: Cumulative Increase)

- Item 5
Records: The owner/operator shall maintain the following 
    monthly records in a District approved log for at least 
    24 months from the date of entry (60 months if the 
    facility has been issued a Title V Major Facility Review 
    Permit or a Synthetic Minor Operating Permit). Log 
    entries shall be retained on site, either at a central 
    location or at the engine's location, and made 
    immediately available to the District staff upon 
    request. 
    a.  Hours of operation for reliability related 
        activities (maintenance and testing). 
    b.  Hours of operation for emission testing. 
 
     c.  Hours of operation (emergency). 
    d.  For each emergency, the nature of the emergency 
        condition. 
    e.  Fuel usage or operating hours for engine. 
   (
Basis: Regulations 9-8-502 and 9-8-530) 
 
End of Conditions

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

Recommendation
The Air District has reviewed the material contained in the permit application for the proposed 
project and has made a preliminary determination that the project is expected to comply with all 
applicable requirements of Air District, state and federal air quality-related regulations. The 
preliminary recommendation is to issue an Authority to Construct for the equipment listed 
below. However, the proposed source will be located within 1,000 feet on a K-12 school  which
