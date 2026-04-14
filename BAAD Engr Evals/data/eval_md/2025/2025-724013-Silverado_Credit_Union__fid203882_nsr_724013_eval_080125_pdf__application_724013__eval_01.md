---
application_number: 724013
plant_name: Silverado Credit Union
plant_address: Angwin, CA 94508
evaluation_date: July 1, 2020
source_json: data/permit_evaluations_json/2025/2025-724013-Silverado_Credit_Union__fid203882_nsr_724013_eval_080125_pdf__application_724013__eval_01.json
---

# Engineering Evaluation (Application 724013)
**Plant**:  Silverado Credit Union
**Address**: Angwin, CA 94508
**Evaluation Date**: July 1, 2020

## background
JSONPath: `$.background.text`

Background
Silverado Credit Union is applying for an Authority to Construct (AC) for the following 
equipment:  
 
S-1 Emergency Standby Liquefied Petroleum Gas Generator  
Make: Kohler Co., Model: KG6208, Model Year: 2024  
103 BHP, 0.85 MMBTU/hr Abated by A-1  
 
A-1 Non-Selective Catalytic Reduction System 
            Make: Nett Technologies Inc., Model: TG Series Catalytic Converter

## emission_calculations
JSONPath: `$.emission_calculations.text`

Emissions Calculations
ons 
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
Factor 
(g/hp-hr) Abatement 
Efficiency 
(% w/w) Abated 
Emission 
Factor 
(g/hp-hr) HourlyEmissions
(lb/hr) Maximum Daily 
Emissions 
(lb/day) Annual 
Emissions 
(lb/yr) Annual 
Emissions 
(TPY) 
NOx 5.00 98 0.10 0.02 0.54 1.13 0.001 
POC 1.19 50 0.60 0.14 3.25 6.77 0.003 
CO 22.69 94 1.36 0.31 7.41 15.44 0.008 
PM10/PM2.5 0.07 N/A N/A 0.02 0.40 0.82 0.000 
SO2 0.00 N/A N/A 0.00 0.01 0.03 0.000 
Basis:  
 103 bhp Max Rated Output 
 9.0 gal/hr Max fuel use Rate = 0.85 MMBTU/hr 
 NOx, POC and CO emission factors are from the engine manufacturer. 
 NOx and CO abatement efficiencies are from the abatement device manufacturer and are 98% and 94% by 
weight, respectively.  POC abatement efficiency is assumed to be 50% by weight. 
 PM10/PM2.5 and SO 2 emission factors are from EPA AP-42, Table 3.2-3 Uncontrolled Emission Factors for  
4-Stroke Rich-Burn Engines.  The PM 10/PM2.5 emission factor is the total of filterable and condensable 
particulates. 
 Annual Emissions are based on an annual limit (50 hr/yr) for testing and maintenance. 
 Max daily emissions are based on 24 hr/day since no daily limits are imposed on emergency operations. 
FID203882   AN724013   
 
  SO2 Emission Factor = 5.88 E-04 lb/MMBtu; calculations assume 100% of fuel sulfur conversion with the content 
in CA natural gas = 10,000 gr/106scf.   
 PM10/PM2.5 fuel input emission factor = 9.50E-03 lb/MMBtu (filterable) + 9.91E-03 lb/MMBtu (condensable) = 
1.94E-02 lb/MMBtu; aerodynamic particle diameter =< 1 µm, for the purposes of filterable emissions PM 10= PM2.5.  
These emissions are expected to be negligible but included for completeness.

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

Plant Cumulative Emissions
Table 3 summarizes the cumulative increase in criteria pollutant emissions that will result from 
the operation of S-1. 
 
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
PM10/PM2.5 0.000 0.000 0.000 
SO2 0.000 0.000 0.000

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

Health Risk Assessment
nt 
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
(lb/MMBtu)  Basis Hourly 
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
1,1,2,2-Tetrachloroethane 2.53E-05 AP-42 1.1E-05 None 5.4E-04 1.40E+00 No 
1,1,2-Trichloroethane 7.65E-06 AP-42 6.5E-06 None 3.3E-04 5.00E+00 No 
1,1-Dichloroethane 5.65E-06 AP-42 4.8E-06 None 2.4E-04 5.00E+01 No 
1,3-Butadiene 1.02E-04 CATEF 4.7E-07 1.50E+00 2.4E-05 4.80E-01 No 
Acetaldehyde 8.66E-04 CATEF 4.0E-06 1.00E+00 2.0E-04 2.90E+01 No 
Acrolein 5.36E-04 CATEF 2.5E-06 5.50E-03 1.2E-04 1.40E+01 No 
Benzene (no control) 1.87E-03 CATEF 8.6E-06 6.00E-02 4.3E-04 2.90E+00 No 
Carbon Tetrachloride 8.85E-06 AP-42 7.5E-06 4.20E+00 3.8E-04 1.90E+00 No 
Chlorobenzene 6.45E-06 AP-42 5.5E-06 None 2.7E-04 3.90E+04 No 
Chloroform 6.85E-06 AP-42 5.8E-06 3.30E-01 2.9E-04 1.50E+01 No 
Ethylbenzene 1.14E-05 CATEF 5.2E-08 None 2.6E-06 3.30E+01 No 
Ethylene Dibromide 1.07E-05 AP-42 9.1E-06 None 4.5E-04 1.10E+00 No 
Formaldehyde (no control) 2.30E-03 CATEF 1.1E-05 1.20E-01 5.3E-04 1.40E+01 No 
Methanol 3.06E-03 AP-42 1.3E-03 6.20E+01 6.5E-02 1.50E+05 No 
Methylene Chloride 4.12E-05 AP-42 1.8E-05 3.10E+01 8.8E-04 8.20E+01 No 
Naphthalene 7.50E-05 CATEF 3.5E-07 None 1.7E-05 2.40E+00 No 
PAH 2.12E-07 CATEF 8.2E-10 None 4.1E-08 3.30E-03 No 
Propylene 1.57E-02 CATEF 7.2E-05 None 3.6E-03 1.20E+05 No 
Styrene 5.95E-06 AP-42 5.1E-06 4.60E+01 2.5E-04 3.50E+04 No 
Toluene 1.05E-03 CATEF 4.8E-06 8.20E+01 2.4E-04 1.20E+04 No 
Vinyl Chloride 3.59E-06 AP-42 3.1E-06 4.00E+02 1.5E-04 1.10E+00 No 
Xylene (total) 6.45E-04 CATEF 3.0E-06 4.90E+01 1.5E-04 2.70E+04 No 
FID203882   AN724013   
 
 The project does not exceed any acute or chronic trigger level and there are not any related projects 
in the last five years. Therefore, the project is not subject to the requirements of Regulation 2-5-APCO as a toxic air contaminant or a hazardous air contaminant or which is on the list
required to be prepared pursuant to subdivision (a) of Section 25532 or Section 44321 
subsections(a) to (f) inclusive of the Health and Safety Code. 
 
(ii) A new or modified source located within an OBC as defined in Section 2-1-243 and 
for which a Health Risk Assessment is required pursuant to Section 2-5-401 
 
The project did not trigger an HRA and it is not located within an OBC. The proposed source will 
operate within 1,000 feet from the following K-12 schools:  
 
Pacific Union College – Preparatory School located at 1 Angwin Avenue, Angwin, CA 94508 and 
Pacific Union College – Elementary School located at 135 Neilsen Ct, Angwin, CA 94508 
FID203882   AN724013   
 
  
Therefore, the proposed source is subject to the public notification requirements of Regulation 2-
1-412. A public notice was prepared and sent to all addresses within 1,000 feet of the proposed 
source and parents and guardians of students of the aforementioned schools: 
 
All comments will be responded to in the same manner they are received.

## BACT
JSONPath: `$.BACT.text`

110. 
 
Best Available Control Technology (BACT)
Pursuant to Regulation 2-2-301, Best Available Control Technology (BACT) shall apply to new 
or modified sources with a Potential to Emit equal to or greater than 10 lb per highest day of the 
pollutants in Table 1.   
 
BACT is not triggered for any pollutant since the maximum daily emission of each pollutant does 
not exceed 10 lb/day.

## offsets
JSONPath: `$.offsets.narrative`

Offsets
ts 
Per Regulation 2-2-302, offsets must be provided for any new or modified source at a facility that 
has the potential to emit (PTE) more than 10 tons/yr of POC or NO x and 100 tons for particulate 
matter and SO 2.  The PTE for emergency-use engines will include the hours allowed for testing 
and maintenance, as well as an assumed 100 hours per year for emergencies.  
 
Table 4. Potential to Emit for Plant# 203882 
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
NOx 0.000 0.003 0.003 10 No 
POC 0.000 0.010 0.010 10 No 
CO 0.000 0.024 0.024 - N/A 
PM10/PM2.5 0.000 0.001 0.001 100 No 
SO2 0.000 0.000 0.000 100 No 
 
Based on the emission calculations in Table 4, offsets are not required for this application.  
 
New Source Performance Standards 
The New Source Performance Standard (NSPS) in 40 CFR 60, Subpart JJJJ apply because the 
FID203882   AN724013   
 
 engine will be installed after January 1, 2011.  The engine will comply with the following limits 
in Table 1 for emergency spark-ignited engines greater than 25 hp but less than 130 hp:  
 
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
California Health & Safety Code §42301.6 and Regulation 2-1-412 (Public Notice, Schools & 
Overburdened Communities) 
Prior to approving an application for an authority to construct or permit to operate, a public notice, 
fully describing the potential emissions, shall be prepared for the following cases: 
 
(i) A new or modified source located within 1000 feet of the outer boundary of a K-12 
school site and which results in the increase in emissions of any substance into the 
ambient air which has been identified by the California Air Resources Board or the 
APCO as a toxic air contaminant or a hazardous air contaminant or which is on the list 
required to be prepared pursuant to subdivision (a) of Section 25532 or Section 44321 
subsections(a) to (f) inclusive of the Health and Safety Code. 
 
(ii) A new or modified source located within an OBC as defined in Section 2-1-243 and 
for which a Health Risk Assessment is required pursuant to Section 2-5-401 
 
The project did not trigger an HRA and it is not located within an OBC. The proposed source will 
operate within 1,000 feet from the following K-12 schools:  
 
Pacific Union College – Preparatory School located at 1 Angwin Avenue, Angwin, CA 94508 and 
Pacific Union College – Elementary School located at 135 Neilsen Ct, Angwin, CA 94508 
FID203882   AN724013   
 
  
Therefore, the proposed source is subject to the public notification requirements of Regulation 2-
1-412. A public notice was prepared and sent to all addresses within 1,000 feet of the proposed 
source and parents and guardians of students of the aforementioned schools: 
 
All comments will be responded to in the same manner they are received.

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
Statement of Compliance
ce 
Regulation 6-1 
Regulation 6-1-303 ( Ringelmann No. 2 Limitation )  
Regulation 6-1-310 (Total Suspended Particulate (TSP))  
Concentration Limits: 
6-1-310.1 No person shall emit TSP from any source in excess of 343 mg per dscm (0.15 gr per 
dscf) of exhaust gas volume. 
6-1-310.2 Effective July 1, 2020, Table 6-1-310.2 emission limits shall apply to any source with a 
Potential to Emit TSP (as defined in Regulation 2-1-217) greater than 1,000 kg per year. No 
applicable source shall emit TSP at a concentration in excess of the limit indicated for the source’s 
Exhaust Gas Rate in Table 6-1-310.2. 
 
The engine emits 65.6 Kg/yr. Therefore, only section 6-1-310.1 applies to this project.  
 
TSP Concentration can be calculated using the formula below: 
൬𝐸𝑛𝑔𝑖𝑛𝑒 𝑃𝑀10 𝐻𝑜𝑢𝑟𝑙𝑦 𝐸𝑚𝑖𝑠𝑠𝑖𝑜𝑛𝑠 ቀ𝑔𝑟
ℎ𝑟ቁ൰
𝐷𝑟𝑦 𝐸𝑛𝑔𝑖𝑛𝑒 𝑀𝑎𝑥𝑖𝑚𝑢𝑚  𝐸𝑥ℎ𝑎𝑢𝑠𝑡 𝐹𝑙𝑜𝑤 𝑅𝑎𝑡𝑒 (𝑑𝑠𝑐𝑓
ℎ𝑟)=𝑇𝑆𝑃 𝐶𝑜𝑛𝑐𝑒𝑛𝑡𝑟𝑎𝑡𝑖𝑜𝑛  (𝑔𝑟
𝑑𝑠𝑐𝑓) 
 
Engine Maximum Exhaust Flow Rate: 580 acfm = 9717.87 dscf/hr 
Engine Maximum Exhaust Temperature: 1200 F       
Water (H2O) Content (%): 12.5%        
PM10 abatement for Engine: N/A        
Engine PM 10 emissions: 115.47 gr/hr 
TSP Concentration for Engine: 0.012 gr/dscf, therefore the source complies with section 6-1-
310.1. 
 
FID203882   AN724013   
 
 Regulation 9-1 
Regulation 9-1-301 ( Inorganic Gaseous Pollutants:  Sulfur Dioxide for Limitations on Ground 
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

## public_notification
JSONPath: `$.public_notification.text`

California Health & Safety Code §42301.6 and Regulation 2-1-412 (Public Notice, Schools &
Overburdened Communities) 
Prior to approving an application for an authority to construct or permit to operate, a public notice, 
fully describing the potential emissions, shall be prepared for the following cases: 
 
(i) A new or modified source located within 1000 feet of the outer boundary of a K-12 
school site and which results in the increase in emissions of any substance into the 
ambient air which has been identified by the California Air Resources Board or thethe public notification requirements of Regulation 2-1-412. After the comments are received from
the public and reviewed, the Air District will make a final determination on the permit. 
 
I recommend that the Air District initiate a public notice and consider any comments received prior 
to taking any final action on issuance of an Authority to Construct and/or a Permit to Operate for 
the following equipment:   
 
S-1 Emergency Standby Liquefied Petroleum Gas Generator  
Make: Kohler Co., Model: KG6208, Model Year: 2024  
103 BHP, 0.85 MMBTU/hr Abated by A-1  
 
A-1 Non-Selective Catalytic Reduction System 
            Make: Nett Technologies Inc., Model: TG Series Catalytic Converter 
 
 
Prepared by: Isis Virrueta 
Air Quality Engineer II 
July 2025      
 
  Table 1 to Subpart JJJJ of Part 60—NO X, CO, and VOC Emission Standards for 
Stationary Non-Emergency SI Engines ≥100 HP (Except Gasoline and Rich Burn LPG), 
Stationary SI Landfill/Digester Gas Engines, and Stationary Emergency Engines >25 HP  
FID203882   AN724013

## conditions
JSONPath: `$.conditions.text`

Permit Conditions
ns 
 
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
FID203882   AN724013   
 
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
FID203882   AN724013   
 
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
endation 
The Air District has reviewed the material contained in the permit application for the proposed 
project and has made a preliminary determination that the project is expected to comply with all 
applicable requirements of Air District, state, and federal air quality-related regulations. The 
preliminary recommendation is to issue an Authority to Constructfor the equipment listed below. 
However, the proposed source will be located within 1,000 feet of a K-12 school which triggers
