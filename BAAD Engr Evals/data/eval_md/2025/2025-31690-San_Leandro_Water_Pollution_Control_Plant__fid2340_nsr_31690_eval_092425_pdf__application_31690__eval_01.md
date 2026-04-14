---
application_number: 31690
plant_id: 2340
plant_name: San Leandro Water Pollution Control Plant
evaluation_date: April 11, 2025
source_json: data/permit_evaluations_json/2025/2025-31690-San_Leandro_Water_Pollution_Control_Plant__fid2340_nsr_31690_eval_092425_pdf__application_31690__eval_01.json
---

# Engineering Evaluation (Application 31690)
**Plant**: 2340 San Leandro Water Pollution Control Plant
**Evaluation Date**: April 11, 2025

## background
JSONPath: `$.background.text`

BACKGROUND
ND 
The San Leandro Water Pollution Control Plant (San Leandro) has applied for a Permit to 
Operate (P/O) for the following existing equipment: 
 
S-19 Dual-Fueled Digester Gas/Natural Gas Boiler 
 Make: Burnham, Model 4-4FW, 209A 
 Maximum Input Heat Capacity: 1.75 MMBtu/Hr 
 
S-20 Dual-Fueled Digester Gas/Natural Gas Boiler 
 Make: Burnham, Model 4-4FW, 209A 
 Maximum Input Heat Capacity: 1.75 MMBtu/Hr 
 
The dual-fired digester gas/natural gas boilers are located at 3000 Davis Street in San Leandro.  
 
The criteria pollutants associated with S-19 and S-20 are nitrogen oxides (NO X), precursor 
organic compounds (POC), particulate matter 10 microns in size (PM 10), particulate matter 2.5 
microns in size (PM 2.5), sulfur dioxide (SO 2), and carbon monoxide (CO).

## emission_calculations
JSONPath: `$.emission_calculations.text`

EMISSIONS CALCULATIONS
NS 
Boiler Operation  
Due to the age of the boilers, the facility had limited supporting documents but were able to 
provide tune-up reports from the testing conducted on June 2, 2025, firing on natural gas and 
digester gas. The facility provided these results to show that the boilers can meet the emissions 
limits as per District Regulation 9-7. All calculations assume 3% excess oxygen (O 2) during 
combustion. 
 
Natural Gas: 
The emission factor for SO 2 in pipeline natural gas was calculated using AP-42 Chapter 1.4, 
Table 2 and Pacific Gas and Electric (PG&E) Gas Rule 21, Section C. AP-42 states an SO 2 
emission factor of 0.6 pound (lb)/million standard cubic feet (MMscf), assuming pipeline sulfur 
concentration of 2,000 grams (gr)/MMscf, while PG&E states a maximum allowable pipeline 
sulfur concentration of 10,000 gr/MMscf in Gas Rule 21, Section C.  Footnote d of AP-42 Table 
1.4-2 states that the SO 2 emission factor should be multiplied by the ratio of actual pipeline 
sulfur concentration to the assumed concentration in AP-42 Table 1.4-2. Therefore, the SO 2 
emission factor for pipeline natural gas is assumed to be 2.94E-03 lb/MMBtu. It is assumed that 
the sulfur will be converted to SO 2 during combustion according to the following equation: 
 
S + O2  SO2  
 
The following table provides a summary of the boiler information which was provided by the 
applicant.  
 
Basis: 
Maximum Fuel Rate: 1.75 MMBtu/hour (hr) 
   1,716 standard cubic feet (scf)/hr (scfh) 
Fuel Heat Value: 1,020 British Thermal Unit (Btu)/scf 
Fuel Usage:  42 MMBtu/day 
Operating Rate: 8,760 hours/year 
Fd Factor:  8,710 dry scf (dscf)/MMBtu 
AP-42 Factors: 
 PM:  7.6 lb/106 scf 
 POC:  5.5 lb/106 scf 
  
 
 
 
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 3 
 Table 1. Daily and Annual Emissions from S-19 and S-20 (Natural Gas Combustion, Each) 
Pollutant  Emission 
Factor 
(lb/MMBtu) Source Volumetric 
Emission 
(ppm) Max DailyEmissions
(lb/day) Annual 
Emissions 
(lb/yr) Annual 
Emissions 
(tons/yr) 
NOx -- B 30 @3% O 2 1.53 558 0.279 
POC 5.39E-03 A  0.23 83 0.041 
CO -- B 275 @3% O 2 8.53 3,113 1.557 
PM2.5 7.45E-03 A  0.31 114 0.057 
PM10 7.45E-03 A  0.31 114 0.057 
SO2 2.94E-03 C  0.12 45 0.023 
 A: AP-42, 5th edition, Table 1.4-2  
 B: NOX - Regulation 9-7-307.7, CO – 85% of BACT trigger 
 C: AP-42, 5th edition, Table 1.4-2 and PG&E Gas Rule 21, Section C 
 
NOx: (21-0/21-3)*30  
= 35 parts per million volume (ppmv), dry at 0% oxygen 
(35 scf NO x/10E6 scf flue gas)*(46 lb NO x/pound mole [lb-mol] NO x)*(8,710 dscf flue gas/MMBtu)*(lb-mol NO x/385.3 
scf NO x) 
= 3.64E-02 lb/MMBtu 
POC: (5.5 lb/MMscf)*(MMscf/10E6 scf)/ (scf/1,020 Btu)*(10E6 Btu/MMBtu) 
= 5.39E-03 lb/MMBtu 
CO: (21-0)/(21-3)*275  
= 320.8 ppmv, dry at 0% oxygen  
(320.8 scf CO/10E6 scf flue gas)*(28 lb CO/lb-mol CO)*(8,710 dscf flue gas/MMBtu)*(lb-mol CO/385.3 scf CO) 
= 2.03E-01 lb/MMBtu 
PM: (7.6 lb/MMscf)*(MMscf/10E6 scf)/(scf/1,020 Btu)*(10E6 Btu/MMBtu) 
= 7.45E-03 lb/MMBtu 
SO2: (0.6 lb SO 2/MMscf)*(10,000 gr SO 2 PG&E/106 scf / 2,000 gr SO 2 AP-42/106 scf)*(scf/1020 Btu) 
= 2.94E-03 lb/MMBtu 
 
Digester Gas: 
Permit Condition #24508 Part 3 states that “The owner/operator shall treat the digester gas with 
and A-4 (digester gas iron sponge scrubber) to ensure that the digester gas total sulfur content 
shall not exceed 300 ppm (dry).”.  
 
It is assumed that all H 2S will be converted to SO 2 during combustion for Best Available Control 
Technology (BACT) pollutant emissions review, as discussed above. The following table 
provides a summary of the boiler information which was provided by the applicant. 
 
 
 
 
 
 
 
 
 
 
 
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 4 
 Basis: 
Maximum Fuel Rate: 1.75 MMBtu/hr 
   2,734 scfh 
Fuel Heat Value: 640 Btu/scf 
Fuel Usage:  42 MMBtu/day 
Operating Rate: 8,760 hours/yr 
Fd Factor:  9,273 dscf/MMBtu (Assumed Value) 
Digester Gas Total S: 300 ppm 
AP-42 Factors: 
 PM:  7.6 lb/106 scf 
 POC:  5.5 lb/106 scf 
 
Table 2. Daily and Annual Emissions from S-19 and S-20 (Digester Gas Combustion, Each)  
Pollutant  Emission 
Factor 
(lb/MMBtu)  Source Volumetric 
Emission 
(ppm) Max Daily 
Emissions 
(lb/day) Annual 
Emissions 
(lb/yr) Annual 
Emissions 
(tons/yr) 
NOx -- B 30 @3% O 2 1.63 594 0.297 
POC 8.59E-03 A  0.36 132 0.066 
CO -- B 275 @3% O 2 9.08 3,314 1.657 
PM2.5 1.19E-02 A  0.50 182 0.091 
PM10 1.19E-02 A  0.50 182 0.091 
SO2 -- C 300 3.27 1,194 0.597 
 A: AP-42, 5th edition, Table 1.4-2  
 B: NOX - Regulation 9-7-307.7, CO – 90% of BACT trigger 
 C: Permit Condition #24508.3. 
 
NOx: (21-0/21-3)*30  
= 35 ppmv, dry at 0% oxygen 
(35 scf NO x/10E6 scf flue gas)*(46 lb NO x/lb-mol NO x)*(9,593 dscf flue gas/MMBtu)*(lb-mol NO x/385.3 scf NO x) 
= 3.87E-02 lb/MMBtu 
POC: (5.5 lb/MMscf)*(MMscf/10E6 scf)/ (scf/640 Btu)*(10E6 Btu/MMBtu) 
= 8.59E-03 lb/MMBtu 
CO: (21-0)/(21-3)*275  
= 320.8 ppmv, dry at 0% oxygen  
(320.8 scf CO/10E6 scf flue gas)*(28 lb CO/lb-mol CO)*(9,593 dscf flue gas/MMBtu)*(lb-mol CO/385.3 scf CO) 
= 2.16E-01 lb/MMBtu 
PM: (7.6 lb/MMscf)*(MMscf/10E6 scf)/(scf/640 Btu)*(10E6 Btu/MMBtu) 
= 1.19E-02 lb/MMBtu 
SO2: (300 scf SO 2/10E6 scf DG)*(64 lb SO 2/lb-mol SO 2)*(scf/640 Btu)*(lb-mol SO 2/385.3 scf SO 2)*(10E6 Btu/MMBtu) 
= 7.79E-02 lb/MMBtu

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

PLANT CUMULATIVE EMISSION
ON  
The following table summarizes the cumulative increase in BACT pollutant emissions that will 
result from this application. 
 
Table 5. Cumulative Increase 
Pollutant Existing, tpy  S-19, tpy S-20, tpy Total, tpy  
NOx 4.885 0.297 0.297 5.479 
CO 6.972 1.657 1.657 10.286 
PM10  0.108 0.091 0.091 0.290 
PM2.5 0.000 0.091 0.091 0.182 
SO2 0.000 0.597 0.597 1.194 
POC 2.566 0.066 0.066 2.698 
Note:  
1. Existing Cumulative Increase taken from AN 26019.

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

TOXIC RISK SCREENING
NG 
The combustion of natural gas and digester gas from S-19 and S-20 will result in the emissions of 
toxic air contaminants (TACs). Emission factors from BAAQMD TAC Emission Factor 
Guidelines, Appendix A, Default TAC Emission Factors for Specific Source Categories, dated 
August 2020, were used to calculate TAC emissions from S-19 and S-20. 
 
The emission factor for hydrogen sulfide was calculated assuming a total sulfur destruction 
efficiency of 98%. 
 
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 5 
 H2S Emission Factor, Digester Gas Combustion: 
 
lb/MMBtu = (1- destruction eff)*[concentration sulfur]*MW*/(digester gas heat content*V M), 
lb/MMBtu = (1-0.98)*[200 ppm sulfur*(1 /106 ppm)]* 34 lb/lb-mole/(530 Btu/scf *1 MMBtu/106 
Btu*385.3 scf/lb-mole), 
lb/MMBtu  = 8.27E-04 ; 
 
Where: destruction efficiency = 98%, MW = molecular weight of H 2S = 34 lb/lb-mole,  
VM = molar volume = 385.3 scf/mole (corrected to 68 °F), Digester gas heat content =  
640 Btu/scf  
 
The TAC emission factors along with their trigger levels and emissions from the operation of the 
boilers are summarized below.Table 4. Toxic Air Contaminant Emissions for S-19 and S-20
TAC E.F. 
(lb/MMBtu) Project 
Emissions 
(lb/hr) Acute 
Trigger 
Level 
(lb/hr) TAC 
Trigger 
(Y/N) Project 
Emissions 
(lb/yr) Chronic 
Trigger 
Level 
(lb/yr) TAC 
Trigger 
(Y/N) 
Acetaldehyde 4.22E-06 1.48E-05 2.10E-01 No  1.29E-01 2.90E+01 N 
Acrolein 2.65E-06 9.28E-06 1.10E-03 No  8.12E-02 1.40E+01 N 
Arsenic 1.96E-07 6.86E-07 8.80E-05 No 6.01E-03 1.60E-03 Y 
Benzene 7.84E-06 2.74E-05 1.20E-02 No 2.40E-01 2.90E+00  N 
Beryllium  5.88E-09 2.06E-08 -- No 1.80E-04 3.40E-02 N 
Cadmium  1.08E-06 3.78E-06 -- No 3.31E-02 1.90E-02 Y 
Copper 8.33E-07 2.92E-06 4.40E-02 No 2.55E-02 -- -- 
Ethylbenzene  9.31E-06 3.26E-05 -- No 2.85E-01 3.30E+01  N 
Formaldehyde  2.17E-04 7.60E-04 2.40E-02 No 6.65E+00  1.40E+01  N 
n-Hexane 6.18E.06 2.16E-05 -- No 1.89E-01 2.70E+05  N 
Lead 4.90E-07 1.72E-06 -- No 1.50E-02 2.90E-01 N 
Manganese  3.73E-07 1.31E-06 -- No 1.14E-02 3.50E+00  N 
Mercury 2.55E-07 8.93E-07 2.70E-04 No 7.82E-03 2.10E-01 N 
Naphthalene  5.98E-07 2.09E-06 -- No 1.83E-02 2.40E+00  N 
Nickel 2.06E-06 7.21E-06 8.80E-05 No 6.32E-02 3.10E-01 N 
PAH 6.60E-09 2.31E-08 -- No 2.02E-04 3.30E-03 N 
Propylene  7.17E-04 2.51E-03 -- No 2.20E+01  1.20E+05  N 
Selenium  1.18E-08 4.13E-08 -- No 3.62E-04 8.00E+00  N 
Toluene 3.59E-05 1.26E-04 2.2E+00 No 1.10E+00  1.60E+04  N 
Vanadium 2.25E-06 7.88E-06 1.30E-02 No 6.90E-02 -- -- 
Xylenes 2.67E-05 9.35E-05 9.7E+00 No 8.19E-01 2.70E+04  N 
Hydrogen Sulfide 1.66E-05 2.89E-03 1.90E-02 No 2.54E+01 3.90E+02 N 
 
The TAC emission factors are on a MMBtu basis because the same factors have been used for 
both digester gas and natural gas. 
 
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 6 
 As shown in Table 4, arsenic and cadmium emissions from the project exceed the regulatory 
health thresholds of Regulation 2, Rule 5. A health screen risk analysis was therefore performed. 
There were no related projects within the last five years. 
 
The results of the HRA were: a Cancer Risk of  0.046 in a million, a Chronic Hazard Index (HI) 
of 0.020, and an Acute HI of  0.0077. In accordance with the District’s Regulation 2-5-301, S-19 
and S-20 are not required to meet TBACT because the cancer risk does not exceed 1.0 in a 
million and the chronic HI does not exceed 0.20.   
 
The estimated project cancer risk does not exceed 6.0 in a million, the chronic HI does not 
exceed 1.0, and the project’s acute HI does not exceed 1.0. Therefore, S-19 and S-20 are in 
compliance with the District’s Regulation 2-5-302 project risk requirements for an over-
burdened community. 
 
It is noted that a H2S concentration of 200 ppm was used to calculate project emissions for the 
HRA as the initial application had included a gas conditioning system that would reduce the H2S 
concentration to 200 ppm. As the facility had withdrawn the application for the gas conditioning 
system, the H2S concentration reverted to 300 ppm as per existing Permit Condition #24508.3. 
The change from 200 ppm H2S to 300 ppm H2S results in a 33.3% increase in project emissions. 
To be conservative, a 50% increase was assumed which resulted in an estimated modeled H2S 
concentration of 0.00032 ppm, which is below the Reg 9-2 limit of 0.03 ppm. It is therefore 
assumed that S-19 and S-20 will comply with Regulation 9-2.Permit Handbook and Best Available Control Technologies (BACT)/BACT for Toxics (TBACT)
Workbook. This project does not trigger BACT or TBACT, therefore the permit approval is a 
ministerial action, which is a statutory exemption from CEQA review.APCO as a toxic air contaminant or a hazardous air contaminant or which is on the list required
to be prepared pursuant to subdivision (a) of Section 25532 or Section 44321 subsections (a) 
through (f) inclusive to the Health and Safety Code, or is located within an Overburdened 
Community (OBC) as defined in Regulation 2-1-243 and for which a Health Risk Assessment 
(HRA) is required pursuant to Regulation 2-5-401, the District shall prepare a public notice as 
detailed in §42301.6.   
 
§42301.9(a) defines a “school” as any public or private school used for the purposes of the 
education of more than 12 children in kindergarten or any grades 1 to 12, inclusive, but does not 
include any private school in which education is primarily conducted in private homes. 
Using the GreatSchools.org website and searching with Google Maps, it has been determined 
that the source will not be located within 1,000 feet of the outer boundary of any K-12 school 
site.   
 
However, the facility is located within an OBC as defined in Regulation 2-1-243 and an HRA 
was required as per District Regulation 2-5-401. Therefore, a public notice is required as per

## BACT
JSONPath: `$.BACT.text`

BEST AVAILABLE CONTROL TECHNOLOGY
GY 
In accordance with Regulation 2-2-301, BACT is triggered for any new or modified source with 
the potential to emit 10 pounds or more per highest day of POC, NPOC, NO X, CO, SO 2, or PM 10, 
PM2.5. Based on the emissions displayed above, BACT is not triggered for any pollutant. 
 
 
 
 
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 7

## offsets
JSONPath: `$.offsets.narrative`

OFFSETS
S 
The following table provides a summary of the facility’s potential to emit (PTE). 
 
Table 6. Potential to Emit 
Pollutant Existing 
PTE1,  
tpy S-19 PTE, 
tpy S-20 PTE, 
tpy New PTE, 
tpy 
POC 2.564 0.297 0.297 3.158 
NOx 0.084 0.066 0.066 0.216 
SO2 0.707 1.657 1.657 4.022 
PM10 0.046 0.091 0.091 0.228 
PM2.5 0.046 0.091 0.091 0.228 
CO 0.002 0.597 0.597 1.195 
 
Note:  
1. Existing PTE calculation is provided in Attachment #1. 
 
Emission offset requirements for POC and NO x are set out in Regulation 2, Rule 2, Section 302.  
POC and NO x offsets are required for new or modified sources at a facility that emits or will be 
permitted to emit 10 tons per year or more of that pollutant. The facility has a PTE greater than 
10 ton/yr of POC, but no more than 35 tons/yr. Pursuant to Regulation 2, Rule 2, Section 302.1, 
the facility is required to provide offsets at a 1:1 ratio. However, Regulation 2, Rule 2, Section 
302.1 also allows the facility to obtain offsets from the District’s Small Facilities Bank (SFB), as 
long as the account is not exhausted. Offsets for POC and NO x are not required for this 
application as the PTE for NOx is less than 10 tpy.  
 
The offsets requirements for PM 10, PM2.5, and SO x are specified in Regulation 2, Rule 2, Section 
303. Per Section 303, PM 10, PM2.5, and SO x emission offsets are required for any new or 
modified source that is a major facility for PM 10, PM2.5, or SO x emissions. The facility is not a 
major facility for PM 10, PM2.5, and SO x emissions. Therefore, offsets for PM 10, PM2.5, and SO x 
are not required for this application.

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

Prevention of Significant Deterioration (PSD)
D)  
The PSD requirements in District Regulation 2, Rule 2, Section 304 and 305 apply to major 
modifications at a major facility. This site is not a major facility. Therefore, Regulation 2-2-304 
and 2-2-305 do not apply. 
 
New Source Performance Standards (NSPS) 
NSPS for boilers is covered in 40 Code of Federal Regulations (CFR) Part 60, Subparts Db and 
Dc. As S-19 and S-20 have a maximum heat input less than 10 MMBtu/hr, neither 40 CFR 60, 
Subpart Db or Dc apply.  
 
National Emission Standards for Hazardous Air Pollutants (NESHAP)  
The following NESHAPs may apply to the facility. 
 
40 CFR Part 63, Subpart DDDDD 
Pursuant to §63.7485, industrial, commercial, and institutional boilers or process heaters, which 
are located at a major source of hazardous air pollutants (HAP)s, are subject to the requirements 
of this regulation. The facility is not major for HAPs, and therefore S-19 and S-20 are not subject 
to this subpart. 
 
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 10 
 40 CFR Part 63 Subpart JJJJJJ 
Pursuant to §63.11193, industrial, commercial, and institutional boilers, which are located at an 
area source of HAPs, are subject to the requirements of this regulation. The facility is an area 
source of HAPs. 
 
S-19 and S-20 are gas-fired boilers. Pursuant to §63.11195, gas-fired boilers are exempt from the 
standard.

## CEQA
JSONPath: `$.CEQA.narrative`

California Environmental Quality Act (CEQA) Requirements
Pursuant to Regulation 2-1-311, an application for a proposed new or modified source will be 
classified as ministerial and will accordingly be exempt from the CEQA requirement of 
Regulation 2-1-310 if the District’s engineering evaluation and basis for approval or denial of the 
permit application for the project is limited to the criteria set forth in Regulation 2-1-428 and to 
the specific procedures, fixed standards, and objective measurements set forth in the District's

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
STATEMENT OF COMPLIANCE
CE 
 
Regulation 6, Rule 1: Particulate Matter: General Requirements 
Pursuant to Regulations 6-1-301, a person shall not emit from any source for a period or periods 
aggregating more than three minutes in any hour, a visible emission which is as dark or darker 
than No. 1 on the Ringelmann Chart,. S-19 and S-20 are expected to meet the requirements of 
Regulations 6-1-301. 
 
Section 6-1-302 is not invoked if an opacity monitor has not been required. 
 
S-19 and S-20 are expected to comply with the 0.15 grain PM/dscf standard in Section 6-1-310.1 
because they use gaseous fuels. 
 
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 8 
 Boilers are exempt from Sections 6-1-310.2 and 6-1-311.2 per the exemption in Section  
6-1-114.1. 
 
S-19 and S-20 are exempt from the testing requirement in Section 6-1-504 per the exemption in 
Section 6-1-114.3 because it is a gas-fuel fired indirect heat exchanger.  It is also exempt from 
the testing because it emits less than 2,000 kg of TSP/yr. 
 
Regulation 9, Rule 1: Inorganic Gaseous Pollutants: Sulfur Dioxide 
Pursuant to Regulation 9-1-301, the ground level concentrations of SO 2 shall not exceed 0.5 ppm 
continuously for 3 consecutive minutes or 0.25 ppm averaged over 60 consecutive minutes, or 
0.05 ppm averaged over 24 hours. Pursuant to Regulation 9-1-302, a person shall not emit from 
any source, a gas stream containing SO 2 in excess of 300 ppm (dry).  Lastly, pursuant to 
Regulation 9-1-304, a person shall not burn any liquid fuel having a sulfur content in excess of 
0.5% by weight. Compliance with Regulation 9-1 is expected due to a fuel total sulfur limit of 
300 ppm for the digester gas for S-19 and S-20. The sulfur limit is imposed under Permit 
Condition #24508.3 for S-190. Subsequent monitoring requirements for the sulfur limit is 
imposed under Permit Condition #24508.4 for S-190 and therefore no additional monitoring 
requirements will be imposed under this permit application. 
 
Regulation 9 Rule 2: Inorganic Gaseous Pollutants: Hydrogen Sulfide 
Pursuant to Regulation 9-2-301, a person shall not emit during any 24-hour period, H 2S in such 
quantities as to result in ground level concentration in excess of 0.06 ppm average over three 
consecutive minutes or 0.03 ppm averaged over any 60 consecutive minutes. On April 11, 2025, 
the Air District modeled H 2S emissions to determine whether S-19 and S-20 will comply with 
the Rule. The results of the dispersion modeling showed a maximum 1-hour average H 2S 
concentration of 0.00032 ppm. Therefore, S-19 and S-20 are in compliance with Regulation 9-2-
301. 
 
Regulation 9, Rule 7: Inorganic Gaseous Pollutants: Nitrogen Oxides and Carbon Monoxide 
from Industrial, Institutional, and Commercial Boilers, Steam Generators, and Process Heaters  
This rule limits the emissions of NO x and CO from boilers.  
 
S-19 and S-20 are subject to the final emissions limits of Regulation 9-7-307.7 for NO x (30 
ppmv, dry at 3% O 2) and CO (400 ppmv, dry at 3% O 2) when firing with digester gas. However, 
in order to stay under BACT, the facility has agreed to a 275 ppmv, dry at 3% O 2 limit for CO. 
This limit will be incorporated into the permit condition for S-19 and S-20. S-19 and S-20 will 
comply with Regulation 9-7-307.7 when firing digester gas.  
 
The boilers are subject to Regulation 9-7-311, which states that no person shall operate a boiler 
or steam generator unless the exposed, external surface of the device, including all pipes and 
ducts heated by the device, does not exceed a temperature of 120 °F. S-19 and S-20 are expected 
to comply with Regulation 9-7-311. 
 
The stack gas temperature limit for boilers or steam generators of a fire tube design, burning 
gaseous fuel, is presented in Regulation 9-7-312 and states that such boilers shall not be operated 
with a stack gas temperature (downstream of any economizer) that exceeds 100 °F over saturated 
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 9 
 steam temperature for steam boilers, 100 °F over hot water temperature for hot water boilers, or 
250 °F greater than combustion temperature, whichever is higher. S-19 and S-20 are expected to 
comply with Regulation 9-7-312. 
 
Pursuant to Regulation 9-7-403, an initial demonstration of compliance is required.  The initial 
demonstration specifies that source tests be performed to determine compliance with the 
limitations of Regulation 9-7-307, unless the device has an input heat rating less than 10 
MMBtu/hr; at which point a portable analyzer may be used.  S-19 and S-20 have an input heat 
rating less than 10 MMBtu/hr.  Therefore, a portable analyzer may be used. 
 
Lastly, Regulation 9-7-503 requires the following records to be kept for at least 24 months from 
the date of entry, which are to be made available to District staff upon request. 
 Documentation verifying the hours of equipment testing using non-gaseous fuel, and of total 
operating hours using non-gaseous fuel during each calendar month; 
 Results of any testing required by Regulation 9-7-506; and, 
 Total operating hours and operating hours firing or co-firing digester gas.

## public_notification
JSONPath: `$.public_notification.text`

California Health & Safety Code §42301.6 and Regulation 2-1-412
Pursuant to California Health & Safety Code §42301.6(a), prior to approving an application for a 
permit to construct or modify a source, which is located within 1,000 feet from the outer 
boundary of a school site and which results in the increase in emissions of any substance into the 
ambient air which has been identified by the California Air Resources Board (CARB) or theRegulation 2-1-412.
Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 11notification requirements of District Regulation 2-1-412. After the comments are received and
reviewed, the District will make a final determination on the permit. 
 
S-19 Dual-Fueled Digester Gas/Natural Gas Boiler 
 Make: Burnham, Model 4-4FW, 209A 
 Maximum Input Heat Capacity: 1.75 MMBtu/Hr 
 
S-20 Dual-Fueled Digester Gas/Natural Gas Boiler 
 Make: Burnham, Model 4-4FW, 209A 
 Maximum Input Heat Capacity: 1.75 MMBtu/Hr 
 
 
 
 
 
 
By:        Date:   8/6/2025    Perry Ng 
 Senior Air Quality Engineer 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

Plant No. 2340 (San Leandro Water Pollution Control Plant)  Application No. 31690 
Page 13 
 Attachment #1 – PTE Calculation

## conditions
JSONPath: `$.conditions.text`

CONDITIONS
S 
 
I recommend the following permit condition for S-19 and S-20. 
 
COND #100741   --------------------------------------

## permit_conditions
JSONPath: `$.permit_conditions`

- Item
CONDITIONS
S 
 
I recommend the following permit condition for S-19 and S-20. 
 
COND #100741   --------------------------------------

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

RECOMMENDATION
ON  
 
The District has reviewed the material contained in the permit application for the proposed 
project and has made a preliminary determination that the project is expected to comply with all 
applicable requirements of District, state, and federal air quality-related regulations. The 
preliminary recommendation is to issue a Permit to Operate for the equipment listed below. 
However, the proposed source will be located within an OBC, which triggers the public
