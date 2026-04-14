---
application_number: 722501
plant_name: SOHA Property Holdings LLC
plant_address: Menlo Park, CA 94025
evaluation_date: January 1, 2011
source_json: data/permit_evaluations_json/2025/2025-722501-SOHA_Property_Holdings_LLC__fid203856_nsr_722501_eval_070225_pdf__application_722501__eval_01.json
---

# Engineering Evaluation (Application 722501)
**Plant**:  SOHA Property Holdings LLC
**Address**: Menlo Park, CA 94025
**Evaluation Date**: January 1, 2011

## background
JSONPath: `$.background.text`

Background
ound    
SOHA Property Holdings LLC  is applying for an Authority to Construct (AC) for the 
following equipment:  
S-1 Emergency Standby Natural  Gas Engine   
Make: Kohler Co., Model: KG 6208 , Model Year: 2024 
95.14  BHP, 1.064  MMBTU/hr Abated by A -1 
 
A-1 Nett Technologies Inc. - TG Series Catalytic Converter

## emission_calculations
JSONPath: `$.emission_calculations.text`

Emission Calculations
ns  
Emission factors for nitrogen oxides (NOx), precursor organic compounds (POC), and carbon 
monoxide (CO) were obtained from the engine manufacturer.   Particulate matter (PM 10/PM 2.5) and 
sulfur dioxide (SO 2) emission factors are based on AP 42, Fifth Edition, V olume I, Chapter 3: 
Stationary Internal Combustion Sources, Section 3.2.4.1 Control Techniques for 4 -Cycle Rich -
Burn Engines and Table 3.2 -3 Uncontrolled Emission Factors for 4 -Stroke Rich -Burn 
Engines .1  The engine will operate for emergency purposes and will be limited to a maximum of 
50 hours per year for maintenance and testing.   
 
Table 1 .  Hourly, Daily, and Annual Emissions from S -1 
Pollutant  Unabated 
Emission 
Factor (g/hp -
hr) Abatement 
Efficiency 
(% w/w)  Abated 
Emission 
Factor 
(g/hp -hr) HourlyEmissions
(lb/hr)  Maximum Daily 
Emissions 
(lb/day)  Annual 
Emissions 
(lb/yr)  Annual 
Emissions 
(TPY)  
NOx  5.22 98 0.10 0.02 0.53 1.09 0.0005  
POC  0.22 50 0.11 0.02 0.56 1.17 0.0006  
CO 15.67  94 0.94 0.20 4.73 9.85 0.0049  
PM 10/PM 2.5 0.10 N/A 0.10 0.02 0.50 1.03 0.000 5 
SO 2 0.00 N/A 0.00 0.00 0.02 0.03 0.0000  
Basis :  
• 95.14  bhp Max Rated Output  
• 1013  scf/hr Max fuel use Rate = 1.064  MMBTU/hr  
• NOx, POC and CO emission factors are from the engine manufacturer.  
• NOx and CO abatement efficiencies are from the abatement device manufacturer and are 98% and 94% by 
weight, respectively.  POC abatement efficiency is assumed to be 50% by weight.  
• PM 10/PM 2.5 and SO 2 emission factors are from EPA AP -42, Table 3.2 -3 Uncontrolled Emission Factors for   
4-Stroke Rich -Burn Engines.  The PM 10/PM 2.5 emission factor is the total of filterable and condensable 
particulates.  
• Annual Emissions are based on an annual limit (50 hr/yr) for testing and maintenance.  
• Max daily emissions are based on 24 hr/day since no daily limits are imposed on emergency operations.  
 
 • SO 2 Emission Factor = 5.88 E -04 lb/MMBtu; calculations assume 100% of fuel sulfur conversion with the content 
in CA natural gas = 10,000 gr/106scf.   
• PM 10/PM 2.5 fuel input emission factor = 9.50E -03 lb/MMBtu (filterable) + 9.91E -03 lb/MMBtu (condensable) = 
1.94E -02 lb/MMBtu; aerodynamic particle diameter =< 1 µm, for the purposes of filterable emissions PM 10= PM 2.5.  
These emissions are expected to be negligible but included for completeness.

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

Plant Cumulative Emissions
Table 3 summarizes the cumulative increase in criteria pollutant emissions that will result from the 
operation of S-1. 
 
Table 3.  Plant Cumulative Emissions Increase, Post 4/5/91  
Pollutant  Existing Emissions  
Post 4/5/91  
(ton/yr)  Application  
Emissions  
(ton/yr)  Cumulative  
Emissions  
(ton/yr)  
NOx  0.000  0.0005  0.0005  
POC  0.000  0.0006  0.0006  
CO 0.000  0.0049  0.0049  
PM 10/PM 2.5 0.000  0.000 5 0.000 5 
SO 2 0.000  0.0000  0.0000

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

Toxic Risk Screen Analysis
Pursuant to Regulation 2 -5-110, a project, including all new or modified sources of toxic air 
contaminants (TAC) within a five-year period, is not subject to this rule if the total project 
emissions are below the acute and chronic trigger levels listed in Table 2 -5-1 “Toxic Air 
Contaminant Trigger Levels” of this regulation.  
 
The emission factors are from the California Air Toxics Emission Factors (CATEF) and the 
Compilation of Air Pollutant Emissions Factor: AP -42.  CATEF emission factors are preferentially 
chosen over AP -42 factors.  If the AP -42 emission factor is based on t he detection limit, the 
emission factor will equal 1/2 of the AP -42 emission factor.Table 2.  Toxic Air Contaminant Review for Engin e
Compound  Emission 
Factor 
(lb/MMB
tu) Basis  Hourly 
Emission 
Rate  
(lb/hr)  Acute 
Trigger 
Level  
(lb/hr)  Annual 
Emission 
Rate  
(lb/yr)  Chronic 
Trigger 
Level 
(lb/yr)  Exceeds 
Acute or 
Chronic 
Trigger 
Level?  
1,1,2,2 -Tetrachloroethane  2.53E -05 AP-42 1.3E-05 None  6.7E-04 1.4E+00  No 
1,1,2 -Trichloroethane  7.65E -06 AP-42 8.1E-06 None  4.1E-04 5.0E+00  No 
1,1-Dichloroethane  5.65E -06 AP-42 6.0E-06 None  3.0E-04 5.0E+01  No 
1,3-Butadiene  1.02E -04 CATEF  5.4E-05 2.9E-01 2.7E-03 4.8E-01 No 
Acetaldehyde  8.66E -04 CATEF  4.6E-04 2.1E-01 2.3E-02 2.9E+01  No 
Acrolein  5.36E -04 CATEF  2.9E-04 1.1E-03 1.4E-02 1.4E+01  No 
Benzene (no control)  1.87E -03 CATEF  1.0E-03 1.2E-02 5.0E-02 2.9E+00  No 
Carbon Tetrachloride  8.85E -06 AP-42 9.4E-06 8.4E-01 4.7E-04 1.9E+00  No 
Chlorobenzene  6.45E -06 AP-42 6.9E-06 None  3.4E-04 3.9E+04  No 
Chloroform  6.85E -06 AP-42 7.3E-06 6.6E-02 3.6E-04 1.5E+01  No 
Ethylbenzene  1.14E -05 CATEF  6.0E-06 None  3.0E-04 3.3E+01  No 
Ethylene Dibromide  1.07E -05 AP-42 1.1E-05 None  5.7E-04 1.1E+00  No 
Formaldehyde (no control)  2.30E -03 CATEF  1.2E-03 2.4E-02 6.1E-02 1.4E+01  No 
Methanol  3.06E -03 AP-42 1.6E-03 1.2E+01  8.1E-02 1.5E+05  No 
Methylene Chloride  4.12E -05 AP-42 2.2E-05 6.2E+00  1.1E-03 8.2E+01  No 
Naphthalene  7.50E -05 CATEF  4.0E-05 None  2.0E-03 2.4E+00  No 
PAH  2.12E -07 CATEF  9.5E-08 None  4.7E-06 3.3E-03 No 
Propylene  1.57E -02 CATEF  8.3E-03 None  4.2E-01 1.2E+05  No 
Styrene  5.95E -06 AP-42 6.3E-06 9.3E+00  3.2E-04 3.5E+04  No 
Toluene  1.05E -03 CATEF  5.6E-04 2.2E+00  2.8E-02 1.6E+04  No 
Vinyl Chloride  3.59E -06 AP-42 3.8E-06 8.0E+01  1.9E-04 1.1E+00  No 
Xylene (total)  6.45E -04 CATEF  3.4E-04 9.7E+00  1.7E-02 2.7E+04  No 
Basis:  
 
 • Abatement efficiency is assumed to be 50% by weight for each TAC above.  
 
The project does not exceed any acute or chronic trigger level and there are not any related projects 
in the last five years. Therefore, the project is not subject to the requirements of Regulation 2 -5-

## BACT
JSONPath: `$.BACT.text`

110. 
Best Available Control Technology (BACT)
Pursuant to Regulation 2 -2-301, Best Available Control Technology (BACT) shall apply to new or 
modified sources with a Potential to Emit equal to or greater than 10 lb per highest day of the 
pollutants in Table 1.   
 
BACT is not triggered for any pollutant since the maximum daily emission of each pollutant does 
not exceed 10 lb/day.

## offsets
JSONPath: `$.offsets.narrative`

Offsets
ts  
Per Regulation 2 -2-302, offsets must be provided for any new or modified source at a facility 
that has the potential to emit (PTE) more than 10 tons/yr of POC or NO x and 100 tons for 
particulate matter and SO 2.  The PTE for emergency -use engines will include the hours allowed 
for testing and maintenance, as well as an assumed 100 hours per year for emergencies.  
 
Table 4. Potential to Emit for Plant# 203856  
Pollutant  Existing 
Annual 
Emissions 
(ton/yr)  Application 
Annual 
Emission 
(ton/yr)  Facility 
Annual 
Emissions  
(ton/yr)  Offset 
Requirement 
(ton/yr)  Offset 
Required?  
NOx  0.000  0.0016  0.0016  10 N 
POC  0.000  0.0018  0.0018  10 N 
CO 0.000  0.0148  0.0148  - N 
PM 10/PM 2.5 0.000  0.001 5 0.001 5 100 N 
SO 2 0.000  0.0000  0.0000  100 N 
 
Based on the emission calculations in Table 4, offsets are not required for this application.  
 
  
 
 
New Source Performance Standards  
The New Source Performance Standard (NSPS)  in 40 CFR 60, Subpart JJJJ apply because the 
engine will be installed after January 1, 2011.   The engine will comply with the following limits 
in Table 1 for emergency spark -ignited engines greater than 25 hp but less than 130 hp:  
 
Pollutant  S-1 Emission Factor 
(Abated)  NSPS Standard  
NO x              0.10 g/bhp -hr 10 g/bhp -hr 
CO               0.94 g/bhp -hr 387 g/bhp -hr 
  
As the information above shows , S-1 is in compliance with these NSPS emission requirements.  
National Emission Standards for Hazardous Air Pollutants (NESHAP)  
This engine will be operated at a hazardous air pollutant (HAP) area source.  Therefore, the engine 
will be subject to the Reciprocating Internal Combustion Engine (RICE) National Emission 
Standards for Hazardous Air Pollutants (NESHAP) (40 CFR Part 63, Subpart ZZZZ) because it is 
a new source and installed after 2007.  A new RICE at an area source that is subject to 40 CFR 
Part 60, Subpart JJJJ, has no further requirements under 40 CFR Part 63, Subpart ZZZZ pursuant 
to 40 CFR Part 63.6590(c).  Therefore, S -1 complies with the NESHAP by meeting the 
requirements under 40 CFR Part 60, Subpart JJJJ.

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

(empty)

## CEQA
JSONPath: `$.CEQA.narrative`

This permit application is not subject to the California Environmental Quality Act (CEQA) 
because the Air District’s evaluation is a ministerial action (Public Resources Code Section 
21080(b)(1) and CEQA Guidelines Section 15268(a)) conducted using the fix ed standards and 
objective measurements in the Air District’s rules and regulations.  
 
Public Notification (Regulation 2 -1-412)  
The proposed source is located less than 1,000 feet from K -12 school, with more than 1 2 
students enrolled.  
Therefore, the proposed source is subject to the public notification requirements of Regulation 2 -
1-412. A public notice was prepared and sent to all addresses within 1,000 feet of the proposed 
source and parents and guardians of students of the following school:  
Sacred Heart Schools, Atherton - Catholic school  
150 Valparaiso Ave, Atherton, CA 94027  
All comments will be  responded to in the same manner they are received.

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
Statement of Compliance
ce  
The owner/operator of S -1 shall comply with Regulation 6, Rule 1 (Particulate Matter and Visible 
Emissions Standards) and Regulation 9 -1-301 (Inorganic Gaseous Pollutants: Sulfur Dioxide for 
Limitations on Ground Level Concentrations). From Regulation 9 -1-301, the ground level 
concentrations of SO2 will not exceed 0.5 ppm continuously for 3 co nsecutive minutes or 0.25 
ppm averaged over 60 consecutive minutes, or 0.05 ppm averaged over 24 hours.  
 
Sections 6 -1-310.1 and 6 -1-310.2 limit total suspended particulate (TSP) emissions to 0.15 
grains/dscf of exhaust gas volume or less depending on the exhaust gas rate (see Table 6 -1-310.2 
for the corresponding TSP concentration limit). As shown in the emis sion calculations in the table 
below, the certified particulate emission rate from this engine is 0.10 grams per bhp -hour, which 
results in an outlet grain loading of 0.015 grains per dscf. Since this emission rate is less than the 
limit in Section 6 -1-310, compliance with this section is expected through use of the certified 
engine.  
Table 5. Section 6 -1-310 Emissions Calculations  
Engine Maximum Exhaust Flow 
Rate 580 acfm = 162.0  dscf/min  = 9717.9  dscf/hr  
Engine Maximum Exhaust 
Temperature  1200  F       
Water (H2O) Content (%)  12.50%         
PM10 abatement for Engine  0.00%         
Engine PM10 emissions  0.02 lb/hr = 82.11  kg/yr  = 144.52  gr/hr 
 
 Are Engine PM10 Emissions > 
1000 kg/yr?  NO        
Applicable Regulation 6 -1-310 
section?  6-1-310.1         
TSP Concentration for Engine  0.015 gr/dscf        
Corresponding Regulation 6 -1 
TSP Limit  0.15 gr/dscf        
PM10 emissions < Corresponding 
Reg 6 -1 TSP Limit?  YES         
* dscfm = acfm x (460 R + 70 F)/(460 R + Engine Maximum Exhaust Temperature in F) x (1 - water (H2O 
Content))   
 
S-1 is an emergency standby generator; from Regulation 9, Rule 8 (NOx and CO from Stationary 
Internal Combustion Engines), Section 110.5 (Emergency Standby Engines), S -1 is exempt from 
the requirements of Regulations 9 -8-301 (Emission Limits on Fossil Derived Fuel Gas), 9 -8-302 
(Emission Limits on Waste Derived Fuel Gas), 9 -8-303 (Emissions Limits – Delayed Complianc e, 
Existing Spark -Ignited Engines, 51 to 250 bhp or Model Year 1996 or Later), 9 -8-304 (Emission 
Limits – Compression -Ignited Engines), 9 -8-305 (Emission Limits – Delayed Compliance, 
Existing Compression -Ignited Engines, Model Year 1996 or Later), 9 -8-501 (Initial Demonstration 
of Compliance) and 9 -8-503 (Quarterly Demonstration of Compliance).  
 
Allowable operating hours and the corresponding record keeping in Regulations 9 -8-330 
(Emergency Standby Engines, Hours of Operation) or Regulation 9 -8-331 (Essential Public 
Service, Hours of Operation) and 9 -8-530 (Emergency Standby Engines, Monitoring an d 
Recordkeeping) will be included in the Permit Conditions below.  
 
This permit application is not subject to the California Environmental Quality Act (CEQA) 
because the Air District’s evaluation is a ministerial action (Public Resources Code Section 
21080(b)(1) and CEQA Guidelines Section 15268(a)) conducted using the fix ed standards and 
objective measurements in the Air District’s rules and regulations.compliance  with District, state, or Federal emission limits is not  limited. (Basis:
Regulat ion 9 -8-330) 
3. The owner/operator shall operate each emergency standb y engine(s) only when a non -
resettable totalizing mete r (with a minimum display capability of 9,999 hours) that  
measures the hours of operation for the engine is  installed, operated and properly 
maintained.  (Basis: Regulation 9 -8-530) 
4. The owner/operator shall not operate the natural gas  fired engine unless it is abated with 
an integral or  add-on three -way catalyst, or other approved abatement  
device. (Basis: Cumulative Increase)  
5. Records: The owner/operator shall maintain the following  monthly records in a District 
approved log for at least  24 months from the date of entry (60 months if the  facility has 
been issued a Title V Major Facility Review  Permit or a Synthetic Minor Operating 
Permit). Log  entries shall be retained on site, either at a centr al location or at the engine's 
location and  made  immediately available to the District staff upo n request.  
         a.  Hours of operation for reliability - related  activities (maintenance and testing).  
         b.  Hours of operation for emission testing.  
         c.  Hours of operation (emergency).  
         d.  For each emergency, the nature of the emergency  condition.  
         e.  Fuel usage or operating hours for engine.  
          (Basis: Regulations 9 -8-502 and 9 -8-530) 
 
End of Conditions

## public_notification
JSONPath: `$.public_notification.text`

Public Notification (Regulation 2 -1-412)
The proposed source is located less than 1,000 feet from K -12 school, with more than 1 2 
students enrolled.  
Therefore, the proposed source is subject to the public notification requirements of Regulation 2 -
1-412. A public notice was prepared and sent to all addresses within 1,000 feet of the proposed 
source and parents and guardians of students of the following school:  
Sacred Heart Schools, Atherton - Catholic school  
150 Valparaiso Ave, Atherton, CA 94027  
All comments will be  responded to in the same manner they are received.the public notification requirements of Regulation 2 -1-412. After the comments are received from
the public and reviewed, the Air District will make a final determination on the permit.  
I recommend that the Air District initiate a public notice and consider any comments received prior 
to taking any final action on issuance of an Authority to Construct and/or a Permit to Operate for 
the following equipment:  
 
S-1 Emergency Standby Natural  Gas Engine   
Make: Kohler Co., Model: KG6208, Model Year: 202 4 
95.14  BHP, 1.064  MMBTU/hr Abated by A -1 
 
A-1 Nett Technologies Inc. - TG Series Catalytic Converter  
 
Prepared by: Brittany McIntosh  
Air Quality Technician  II 
     
 
 
 
 
 
 
Table 1 to Subpart JJJJ of Part 60 —NO X, CO, and VOC Emission Standards for Stationary Non -Emergency 
SI Engines ≥100 HP (Except Gasoline and Rich Burn LPG), Stationary SI Landfill/Digester Gas Engines, and 
Stationary Emergency Engines >25 HP

## conditions
JSONPath: `$.conditions.text`

Permit Conditions
onditions  
Permit Condition No. 231 07 for S -1    
 
1. Operating time for reliability related activities is  limited to 50 hours per year per engine.  
(Basis: Regulation 9-8-330.3)  
2. The owner/operator shall operate the stationary  emergency standby engine only for the 
following  purposes: to mitigate emergency conditions, for emission  testing to 
demonstrate compliance with a District, State  or Federal emission limit, or for reliability 
related  activities (maintenance and other testing but excluding  emission testing).  
Operating while mitigating emergency  conditions or while emission testing to show

## permit_conditions
JSONPath: `$.permit_conditions`

Condition number: 231
- Item 1
Operating time for reliability related activities is  limited to 50 hours per year per engine.  
(
Basis: Regulation 9-8-330.3)

- Item 2
The owner/operator shall operate the stationary  emergency standby engine only for the 
following  purposes: to mitigate emergency conditions, for emission  testing to 
demonstrate compliance with a District, State  or Federal emission limit, or for reliability 
related  activities (maintenance and other testing but excluding  emission testing).  
Operating while mitigating emergency  conditions or while emission testing to show

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

Recommendation
Recommendation  
The Air District has reviewed the material contained in the permit application for the proposed 
project and has made a preliminary determination that the project is expected to comply with all 
applicable requirements of Air District, state, and federal air quality -related regulations.  The 
preliminary recommendation is to issue an Authority to Construct for the equipment listed below. 
However, the proposed source will be located within 1,000 feet of a K -12 school which trigge rs
