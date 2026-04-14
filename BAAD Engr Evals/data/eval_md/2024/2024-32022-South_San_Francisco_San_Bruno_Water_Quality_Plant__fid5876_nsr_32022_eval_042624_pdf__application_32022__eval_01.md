---
application_number: 32022
plant_id: 5876
plant_name: South San Francisco -San Bruno Water Quality Plant
evaluation_date: March 7, 2024
source_json: data/permit_evaluations_json/2024/2024-32022-South_San_Francisco_San_Bruno_Water_Quality_Plant__fid5876_nsr_32022_eval_042624_pdf__application_32022__eval_01.json
---

# Engineering Evaluation (Application 32022)
**Plant**: 5876 South San Francisco -San Bruno Water Quality Plant
**Evaluation Date**: March 7, 2024

## background
JSONPath: `$.background.text`

BACKGROUND
ND  
South San Francisco -San Bruno Water Quality Plant (WQP) has applied to obtain a Permit to 
Operate (P/O) for the following existing equipment:  
 
S-17 Dual -Fueled Digester Gas/Natural Gas Boiler, # 3 
 Make: Cleaver -Brooks,  Model 3700 -60 
 Maximum Input Heat Capacity: 2.51 MMBtu/Hr  
 
The dual -fueled digester gas/natural gas boiler is located at 195 Belle Air Road in South San 
Francisco, California. The boiler is used to provide supplemental heat to the anaerobic digesters, 
S-190. The boiler is fired primarily on digester gas from S -190 that is conditioned by S -12, 
Digester Gas Conditioning System, but also has the capability of using natural gas.   The facility 
indicates that t he boiler was installed without an Authority to Construct around 2000 . 
 
The criteria pollutants associated with S -17 are nitrogen oxides (NO X), precursor organic 
compounds (POC), particulate matter 10 microns in size (PM 10), particulate matter 2.5 microns 
in size (PM 2.5), sulfur dioxide (SO 2), and carbon monoxide (CO).

## emission_calculations
JSONPath: `$.emission_calculations.text`

EMISSIONS CALCULATIONS
NS  
Boiler Operation  
 
Due to the age of the boiler, t he W QP had limited supporting documents for the boiler, but were 
able to include NO x and CO testing conducted by Blue Sky Enviro nmental Inc. on February 23, 
2023. The facility notes that the testing performed on February 23, 2023 is meant to be a 
preliminary /internal  source test to show that the  boiler can meet emission limits as per District 
Regulation 9 -7.  All calculations have been made assuming 3% excess O 2 during combustion.  
 
Natural Gas:  
The emission factor for SO 2 in pipeline natural gas was calculated using AP -42 Chapter 1.4, 
Table 2 and PG&E Gas Rule 21, Section C. AP -42 states an SO 2 emission factor of  
0.6 lb/MMscf, assuming pipeline  sulfur  concentration  of 2,000 gr/MMscf, while PG&E states a 
maximum allowable pipeline sulfur concentration of 10,000 gr/MMscf in Gas Rule 21, Section 
C.  Footnote d of AP -42 Table 1.4 -2 states that the SO 2 emission factor should be multiplied by 
the ratio of actual pipeline sulfur concentration to the ass umed concentration in AP -42 Table  
1.4-2. Therefore, the SO 2 emission factor for pipeline natural gas is assumed to be 3.0 lb/MMscf.  
It is assumed that the sulfur will be converted to SO 2 during combustion according to the 
following equation:  
 
S + O 2 → SO 2  
 
The following table provides a summary of the boiler information, which was provided by the 
applicant.   
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 2 
 Basis:  
Maximum Fuel Rate: 2.51 MMBtu/hr  
   2,461  scfh 
Fuel Heat Value:  1,020 Btu/scf  
Fuel Usage:   60.24  MMBtu/day  
Operating Rate:  8,760 hours/yr  
Fd Factor:   8,710 dscf/MMBtu  
AP-42 Factors:  
 PM:  7.6 lb/106 scf 
 POC:   5.5 lb/106 scf 
  
Table 1 . Daily and Annual Emissions from S -17 (Natural Gas Combustion ) 
Pollutant  Emission 
Factor 
(lb/MMBtu ) Source  Volumetric 
Emission 
(ppm)  Max DailyEmissions
(lb/day)  Annual 
Emissions 
(lb/yr)  Annual 
Emissions 
(tons/yr)  
NOx  -- B 30 @3% O 2 2.19 800 0.400 
POC  5.39E -03 A  0.32 119 0.059 
CO -- B 200 @3% O 2 8.90 3,274 1.624 
PM 2.5 7.45E -03 A  0.45 164 0.082 
PM 10 7.45E -03 A  0.45 164 0.082 
SO 2 2.94E-03 C  0.18 65 0.032 
➢ A: AP-42, 5th edition, Table 1.4 -2  
➢ B: NO X - Regulation 9 -7-307.7, CO – 90% of BACT trigger  
➢ C: AP-42, 5th edition, Table 1.4 -2 and PG&E Gas  Rule 21, Section C  
 
NO x: (21 -0/21-3)*30  
= 35 ppmv, dry at 0% oxygen  
(35 scf NO x/10E6 scf flue gas)*(46 lb NO x/lb-mol NO x)*(8,710 dscf flue gas/MMBtu)*(lb -mol NO x/385.3 scf NO x) 
= 3.64E-02 lb/MMBtu  
POC: (5.5 lb/MMscf)*(MMscf/10E6 scf)/ (scf/1,020 Btu)*(10E6 Btu/MMBtu)  
= 5.39E -03 lb/MMBtu  
CO: (21 -0)/(21 -3)*200  
= 233.3 ppmv, dry at 0% oxygen  
(233.3 scf CO/10E6 scf flue gas)*(28 lb CO/lb -mol CO)*(8,710 dscf flue gas/MMBtu)*(lb -mol CO/385.3 scf CO)  
= 1.48E-01 lb/MMBtu  
PM: (7.6 lb/MMscf)*(MMscf/10E6 scf)/(scf/1,020 Btu)*(10E6 Btu/MMBtu)  
= 7.45E-03 lb/MMBtu  
SO 2: (0.6 lb SO 2/MMscf )*(10,000 gr SO 2 PG&E/106 scf / 2,000 gr SO 2 AP-42/106 scf)*(scf/ 1020 Btu) 
= 2.94E-03 lb/MMBtu  
 
Digester Gas:  
The sulfur content in digester gas fuel, 5 ppm total sulfur, is based on Permit Condition 
#27355.6, which states “ The owner/operator shall ensure that the digester gas fired at S -15 and 
S-16 does not exceed a total sulfur content of 5 ppmv.”. The permit condition will be edited to 
include S -17 as part of this permit application.  It is assumed that all H 2S will be converted to SO 2 
during combustion  for Best Available Control Technology ( BACT ) pollutant emissions review , 
as discussed above.  The following table provides a summary of the boiler information, which 
was provided by the applicant.  
 
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 3 
 Basis:  
Maximum Fuel Rate: 2.51 MMBtu/hr  
   4,736  scfh 
Fuel Heat Value:  530 Btu/scf  
Fuel Usage:   60.24  MMBtu/day  
Operating Rate:  8,760 hours/yr  
Fd Factor:   9,597 dscf/MMBtu  (Assumed Value)  
Digester  Gas Total S:  5 ppm 
AP-42 Factors:  
 PM:  7.6 lb/106 scf 
 POC:   5.5 lb/106 scf 
 
Table 2. Daily and Annual Emissions from S -17 (Digester Gas Combustion ) 
Pollutant  Emission 
Factor 
(lb/MM Btu) Source Volumetric 
Emission 
(ppm)  Max Daily 
Emissions 
(lb/day)  Annual 
Emissions 
(lb/yr)  Annual 
Emissions 
(tons/yr)  
NOx  -- B 30 @3% O 2 2.42 882 0.441 
POC  5.5 A  0.63 228 0.114 
CO -- B 200 @3% O 2 9.80 3,578 1.789 
PM 2.5 7.6 A  0.86 315 0.158 
PM 10 7.6 A  0.86 315 0.158 
SO 2 -- C 5 0.09 34 0.017 
➢ A: AP -42, 5th edition, Table 1.4 -2  
➢ B: NO X - Regulation 9 -7-307.7, CO – 90% of BACT trigger  
➢ C: Permit Condition #27355.6.  
 
NO x: (21 -0/21-3)*30  
= 35 ppmv, dry at 0% oxygen  
(35 scf NO x/10E6 scf flue gas)*(46 lb NO x/lb-mol NO x)*(9,597 dscf flue gas/MMBtu)*(lb -mol NO x/385.3 scf NO x) 
= 4.01E-02 lb/MMBtu  
POC: (5.5 lb/MMscf)*(MMscf/10E6 scf)/ (scf/ 530 Btu)*(10E6 Btu/MMBtu)  
= 1.04E-02 lb/MMBtu  
CO: (21 -0)/(21 -3)*200  
= 233.3 ppmv, dry at 0% oxygen  
(233.3 scf CO/10E6 scf flue gas)*(28 lb CO/lb -mol CO)*( 9,597 dscf flue gas/MMBtu)*(lb -mol CO/385.3 scf CO)  
= 1.63E-01 lb/MMBtu  
PM: (7.6 lb/MMscf)*(MMscf/10E6 scf)/(scf/ 530 Btu)*(10E6 Btu/MMBtu)  
= 1.43E-02 lb/MMBtu  
SO 2: (5 scf SO 2/10E6 scf DG)*(64 lb SO 2/lb-mol SO 2)*(scf/530 Btu)*(lb -mol SO 2/385.3 scf SO 2)*(10E6 Btu/MMBtu)  
= 1.57E-03 lb/MMBtu

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

PLANT CUMULATIVE EMISSION
ON  
The following table summarize s the cumulative increase in BACT pollutant emissions that will 
result from this application.  
 
Table 5. Cumulative Increase  
Pollutant  Existing, tpy  S-17, tpy  Total, tpy  
NOx  9.380  0.441  9.821  
CO 16.842  1.789  18.631  
PM10  0.181  0.158  0.339  
PM2.5  0.180  0.158  0.338  
SO 2 0.019  0.017  0.036  
POC  5.941  0.114  6.055Cumulative Increase]
ase]  
 
2.  The owner/operator of S15 and S16 shall not allow the  
    heat input to each source exceed 13,140 MMBtu during any  
    consecutive 12 month period.  The owner/operator of S17 shall not allow the heat 
input to this source to exceed 21 ,988 MMBtu during any consecutive 12 month 
period.  [Basis: Cumulative  
    Increase]  
 
3.  The owner/operator of S15 , and S16, and S17  shall operate these  
    sources only when a non resettable totalizing fuel meter  
    is installed in each fuel line for each source.   [Basis: 
    Regulation 9 -7-501] 
 
4.  The owner/operator shall ensure that the H2S and  
    siloxane absorption media at S12 is not desorbed onsite.  
    [Basis: Cumulative Increase]

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

TOXIC RISK SCREENING
NG  
The combustion of natural gas and digester gas from S-17 will result in the emissions of toxic air 
contaminants (TACs).  Emission factors from BAAQMD TAC Emission Factor Guidelines, 
Appendix A,  Default TAC Emission Factors for Specific Source Categories, dated August 2020, 
were used to calculate TAC emissions from S -17. 
 
 
 
 
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 4 
 The emission factor for hydrogen sulfide was calculated  assuming  a total sulfur destruction 
efficiency of 98%.  
 
H2S Emission Factor , Digester Gas Combustion:  
 
lb/MMBtu = (1 - destruction eff)*[concentration sulfur]*MW*/ (digester gas heat content* VM), 
lb/MMBtu = (1 -0.98)*[5 ppm sulfur*(1 /106 ppm)]* 34 lb/lb -mole/ (530 Btu/scf *1 MMBtu/106 
Btu* 385.3 scf/lb -mole ), 
lb/MMBtu  = 1.66E-05; 
 
Where: destruction efficiency = 98%, MW = molecular weight of H 2S = 34 lb/lb -mole,   
VM = molar volume = 385.3 scf/mole (corrected to 68 °F), Digester gas heat content =  
530 Btu/scf   
 
The TAC emission factors along with their trigger levels and emissions from the operation of the 
boiler  are summarized below.Table 4. Toxic Air Contaminant  Emissions f or S-17
TAC  E.F. 
(lb/MMBtu ) Emissions 
(lb/hr) Acute 
Trigger 
Level 
(lb/hr) TAC  
Trigger 
(Y/N)  Emissions 
(lb/yr) Chronic 
Trigger 
Level 
(lb/yr) TAC  
Trigger 
(Y/N)  
Acetaldehyde  4.22E -06 1.06E -05 2.10E -01 No 9.28E -02 2.90E+01  No 
Acrolein  2.65E -06 6.65E -06 1.10E -03 No 5.83E -02 1.40E+01  No 
Arsenic  1.96E -07 4.92E -07 8.80E -05 No 4.31E -03 1.60E -03 Yes 
Benzene  7.84E -06 1.97E -05 1.20E -02 No 1.72E -01 2.90E+00  No 
Beryllium  5.88E -09 1.48E -08 -- No 1.29E -04 3.40E -02 No 
Cadmium  1.08E -06 1.08E -06 -- No 2.37E -02 1.90E -02 Yes 
Copper  8.33E -07 2.09E -06 4.40E -02 No 1.83E -02 -- No 
Ethylbenzene  9.31E -06 2.34E -05 -- No 2.05E -01 3.30E+01  No 
Formaldehyde  2.17E -04 5.45E -04 2.40E -02 No 4.77E+00  1.40E+01  No 
n-Hexane  6.18E.06  1.55E -05 -- No 1.36E -01 2.70E+05  No 
Lead  4.90E -07 1.23E -06 -- No 1.08E -02 2.90E -01 No 
Manganese  3.73E -07 9.36E -07 -- No 8.20E -03 3.50E+00  No 
Mercury  2.55E -07 6.40E -07 2.70E -04 No 5.61E -03 2.10E -01 No 
Naphthalene  5.98E -07 1.50E -06 -- No 1.31E -02 2.40E+00  No 
Nickel  2.06E -06 5.17E -06 8.80E -05 No 4.53E -02 3.10E -01 No 
PAH  6.60E -09 1.66E -08 -- No 1.45E -04 3.30E -03 No 
Propylene  7.17E -04 1.80E -03 -- No 1.58E+01  1.20E+05  No 
Selenium  1.18E -08 2.96E -08 -- No 2.59E -04 8.00E+00  No 
Toluene  3.59E -05 9.01E -08 2.2E+00  No 7.89E -01 1.60E+04  No 
Vanadium  2.25E -06 5.65E -06 1.30E -02 No 4.95E -02 -- No 
Xylenes  2.67E -05 6.70E -05 9.7E+00  No 5.87E -01 2.70E+04  No 
Hydrogen Sulfide  1.66E -05 4.18E -05 1.90E -02 No 3.66E -01 3.90E+02  No 
 
The TAC emission factors are on a MMBtu basis because the same factors have been used for 
both digester gas and natural gas.  
 
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 5 
 As shown in Table 4, arsenic and cadmium  emissions from S -17 exceed  the regulatory health 
thresholds of Regulation 2, Rule 5. There is one  related project within the last five years , 
Application #28991. The permit application was for  S-190, Four (4) Anerobic Digesters with  
A-380, Industrial Flare, and S-15 and S -16, Dual -Fueled Digester/Natural Gas Boilers . A health 
screen risk analysis was therefore performed.  
 
The results of the HRA were: a Cancer Risk of  0.055 in a million, a Chronic Hazard Index (HI) 
of 0.019, and an Acute HI of  3.4. In accordance with the District’s Regulation 2 -5-301, S-17 is 
not required to meet TBACT because the source cancer risk does not exceed 1.0 in a million and 
the chronic HI does not exceed 0.20.  The estimated project cancer risk d oes not exceed 10.0 in a 
million and the chronic HI does not exceed 1.0, however the project’s acute HI exceeds 1.0. The 
result indicate that to reduce the acute HI to less than 1.0, the facility would need to limit H2S 
hourly emissions from S -190 to 0.21 lbs/hr. As per Permit Condition #27356, the facility is 
limited to an hourly H2S emis sions rate of 0.08 lbs/hr (rounded to 0.1 lbs/hr in the permit 
condition text). Therefore, S -17 is in compliance with the District’s Regulation 2 -5-302 project 
risk requirements.Permit Handbook and Best Available Control Technologies ( BACT )/BACT for Toxics ( TBACT )
Workbook. This project does not trigger BACT or TBACT, therefore the permit approval is a 
ministerial action, which is a statutory exemption from CEQA review.APCO as a toxic air contaminant or a hazardous air contaminant or which is on the list required
to be prepared pursuant to subdivision (a) of Section 25532 or Section 44321 subsections (a) 
through (f) inclusive to the Health and Sa fety Code, or is located within an Overburdened 
Community (OBC) as defined in Regulation 2 -1-243 and for which a Health Risk Assessment  
(HRA)  is required pursuant to Regulation 2 -5-401, the District shall prepare a public notice as 
detailed in §42301.6.   
 
§42301.9(a) defines a “school” as any public or private school used for the purposes of the 
education of more than 12 children in kindergarten or any grades 1 to 12, inclusive, but does not 
include any private school in which education is primarily conduct ed in private homes.  
Using the GreatSchools.org website and searching with Google Maps, it has been determined 
that t he source will not be located within 1,000 feet of the outer boundary of any K -12 school 
site.   
 
However , the facility is located within an OBC as defined in Regulation 2 -1-243 and a n HRA  
was required as per District Regulation 2 -5-401. Therefore a public notice is required as per

## BACT
JSONPath: `$.BACT.text`

BEST AVAILABLE CONTROL TECHNOLOGY
GY  
In accordance with Regulation 2 -2-301, BACT is triggered for any new or modified source with 
the potential to emit 10 pounds or more per highest day of POC, NPOC, NO X, CO, SO 2, or PM 10, 
PM 2.5. Based on the emissions displayed above, BACT is not triggered for any pollutant.  
 
 
 
 
 
 
 
 
 
 
 
 
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 6

## offsets
JSONPath: `$.offsets.narrative`

OFFSETS
S  
The following table provides a summary of the facility’s potential to emit (PTE).  
 
Table 6. Potential to Emit  
Pollutant  Existing  PTE , 
tpy S-17 - PTE , 
tpy New PTE , 
tpy 
NOx  8.923  0.441  9.364 
POC  16.496  0.114  16.610  
PM10  0.442  0.158  0.600  
PM2.5  0.439  0.158  0.597  
SO 2 0.281  0.017  0.298  
CO 23.795 1.789  25.584  
 
Emission offset requirements for POC and NO x are set out in Regulation 2, Rule 2, Section 302.  
POC and NO x offsets are required for new or modified sources at a facility that emits or will be 
permitted to emit 10 tons per year or more of that pollutant.  The facility has a PTE greater than 
10 ton/ yr of POC , but no more than 35 tons/yr. Pursuant to Regulation 2, Rule 2, Section 302.1, 
the facility is required to provide offsets at a 1:1 ratio . However , Regulation 2, Rule 2, Section 
302.1 also allows the facility to obtain offsets from the District’s S mall Facilities Bank  (SFB), as 
long as the account is not exhausted. Therefore, offsets for POC will be taken from the SFB. 
Offsets for NO x are not required for this application as the PTE for NOx is less than 10 tpy.   
 
The offsets requirements for PM 10, PM 2.5, and SO x are specified in Regulation 2, Rule 2, Section 
303. Per Section 303, PM 10, PM 2.5, and SO x emission offsets are required for any new or 
modified source that is a major facility for PM 10, PM 2.5, or SO x emissions. The WQP  is not a 
major facility for PM 10, PM 2.5, and SO x emissions. Therefore, offsets for PM 10, PM 2.5, and SO x 
are not required for this application.

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

Prevention of Significant Deterioration (PSD)
D)  
The PSD requirements in District Regulation 2, Rule 2, Section 304 and 305 apply to major 
modifications at a major facility. This site is not a major facility. Therefore, Regulation 2 -2-304 
and 2 -2-305 do not apply.  
 
New Source Performance Standards (NSPS)  
NSPS for boilers is covered in 40 Code of Federal Regulations ( CFR ) Part 60 , Subparts Db and 
Dc. As S -17 has a maximum heat input less than 10 MMBtu/hr, neither 40 CFR 60, Subpart Db 
or Dc apply.  
 
National Emission Standards for Hazardous Air Pollutants (NESHAP)  
The following NESHAPs may apply to the facility . 
 
40 CFR Part 63, Subpart DDDDD  
Pursuant to § 63.7485, industrial, commercial, and institutional boilers or process heaters, which 
are located at a major source of hazardous air pollutants  (HAP)s, are subject to the requirements 
of this regulation. The facility is not major for HAPs, and therefore S -17 is not subject to this 
subpart.  
 
 
 
 
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 9 
 40 CFR Part 63 Subpart JJJJJJ  
Pursuant to §63.11193, industrial, commercial, and institutional boilers, which are located at an 
area source of HAPs,  are subject to the requirements of this regulation. The facility is an area 
source of HAPs.  
 
S-17 is a gas -fired boiler. Pursuant to §63.11195, gas-fired  boilers are exempt from the standard.

## CEQA
JSONPath: `$.CEQA.narrative`

California Environmental Quality Act (CEQA) Requirements
Pursuant to Regulation 2 -1-311, an application for a proposed new or modified source will be 
classified as ministerial and will accordingly be exempt from the CEQA requirement of 
Regulation 2 -1-310 if the District’s engineering evaluation and basis for app roval or denial of the 
permit application for the project is limited to the criteria set forth in Regulation 2 -1-428 and to 
the specific procedures, fixed standards, and objective measurements set forth in the District's

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
STATEMENT OF COMPLIANCE
CE  
 
Regulation 6, Rule 1 : Particulate Matter : General Requirements  
Pursuant to Regulations 6 -1-301 and 6 -1-302, a person shall not emit from any source for a 
period or periods aggregating more than three minutes in any hour, a visible emission which is as 
dark or darker than No. 1 on the Ringelmann Chart, or of such opaci ty as to obscure an 
observer’s view to an equivalent or greater degree and/or an emission equal to or greater than 
20% opacity as perceived by an opacity sensing device, where such a device is required by 
District regulations. S-17 is expected to meet the requirements of Regulations 6 -1-301 and  
6-1-302. 
 
The boiler is expected to comply with the 0.15 grain PM/dscf standard in Section 6 -1-310.1 
because it uses gaseous fuels.  
 
Boilers are exempt from Sections 6 -1-310.2 and 6 -1-311.2 per the exemption in Section  
6-1-114.1.  
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 7 
 The boiler is exempt from the testing requirement in Section 6 -1-504 per the exemption in 
Section 6 -1-114.3 because it is a gas-fuel fired indirect heat exchanger .  It is also exempt from 
the testing because it emits less than 2,000 kg of TSP/yr.  
 
Regulation 9, Rule 1 : Inorganic Gaseous Pollutants: Sulfur Dioxide  
Pursuant to Regulation 9 -1-301, the ground level concentrations of S O2 shall not exceed 0.5 ppm 
continuously for 3 consecutive minutes or 0.25 ppm averaged over 60 consecutive minutes, or 
0.05 ppm averaged over 24 hours. Pursuant to Regulation 9 -1-302, a person shall not emit from 
any source, a gas stream containing SO 2 in excess of 300 ppm (dry).  Lastly, pursuant to 
Regulation 9 -1-304, a person shall not burn any liquid fuel having a sulfur content in excess of 
0.5% by weight.  Compliance with Regulation 9 -1 is expected due to a fuel total sulfur limit of 5 
ppm for S -17. 
 
Regulation 9 Rule 2: Inorganic Gaseous Pollutants: Hydrogen Sulfide  
Pursuant to Regulation 9 -2-301, a person shall not emit during any 24 -hour period, H 2S in such 
quantities as to result in ground level concentration in excess of 0.06 ppm average over three  
consecutive minutes or 0.03 ppm averaged over any 60 consecutive minutes. On March 7, 2024, 
the Air District modeled H 2S emissions to determine whet her S -17 will comply with the Rule. 
The results of the dispersion modeling showed a maximum 1 -hour average H 2S concentration of 
0.29 ppm. The results indicate that to reduce the H 2S ground level concentration to below 0.03 
ppm, the facil ity would need to limit H 2S hourly emissions from S -190 to 0.08 lbs/hr. As per 
Permit Condition #27356 , the facility is limited to an hourly H2S emissions rate of 0.08 lbs/hr 
(rounded to 0.1 lbs/hr in the permit condition text). Therefore, S -17 is in compliance with 
Regulation 9 -2-301. 
 
Regulation 9, Rule 7: Inorganic Gaseous Pollutants: Nitrogen Oxides and Carbon Monoxide 
from Industrial, Institutional, and Commercial Boilers, Steam Generators, and Process Heaters  
This rule limits the emissions of NO x and CO from boilers . S-17 is expected to comply with the 
requirements of Regulation 9, Rule 7.  
 
S-17 is subject to the final emissions limits of 9-7-307.7 for NO x (30 ppmv, dry at 3% O 2) and 
CO (400 ppmv, dry at 3% O 2) when firing with digester gas.  However, in order to stay under 
BACT, the facility has agreed to a 200 ppmv, dry at 3% O 2 limit for CO.  This limit will be 
incorporated into the permit condition for S -17. S-17 will comply with 9 -7-307.7 when firing  
digester gas.  
 
The boiler is subject to Regulation 9 -7-311, which states that no person shall operate a boiler or 
steam generator unless the exposed, external surface of the device, including all pipes and ducts 
heated by the device, does not exceed a temperature of 120 °F. S -17 will comply with 9 -7-311. 
 
The stack gas temperature limit for boilers or steam generators of a fire tube  design, burning 
gaseous fuel, is presented in Regulation 9 -7-312 and states that such boilers shall not be operated 
with a stack gas temperature (downstream of any economizer) that exceeds 1 00 °F over saturated 
steam temperature for steam boilers, 1 00 °F over hot water temperature for hot water boilers, or 
250 °F  greater than combustion temperature, whichever is higher. S -17 will comply with 9 -7-
312. 
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 8 
  
Pursuant to Regulation 9 -7-403, an initial demonstration of compliance is required.  The initial 
demonstration specifies that source tests be performed to determine compliance with the 
limitations of Regulation 9 -7-307, unless the device has an input heat rating less than 10 
MMBtu/hr; at which point a portable analyzer may be used.  S -17 has an input heat rating less 
than 10 MMBtu/hr.  Therefore, a portable analyzer may be used.  
 
Lastly, Regulation 9 -7-503 requires the following records to be kept for at least 24 months from 
the date of entry, which are to be made available to District staff upon request.  
• Documentation verifying the hours of equipment testing using non -gaseous fuel, and of total 
operating hours using non -gaseous fuel during each calendar month;  
• Results of any testing required by Regulation 9 -7-506; and,  
• Total operating hours and operating hours firing or co -firing digester gas.

## public_notification
JSONPath: `$.public_notification.text`

California Health & Safety Code §42301.6 and Regulation 2 -1-412
Pursuant to California Health & Safety Code §42301.6(a), prior to approving an application for a 
permit to construct or modif y a source, which is located within 1,000 feet from the outer 
boundary of a school site  and w hich results in the increase in emissions of any substance into the 
ambient air which has been identified by the California Air Resources Board (CARB) or theRegulation 2 -1-412.
Plant No. 5876  (South San Francisco -San Bruno Water Quality Plant )  Application No. 32022  
Page 10requirements of District Regulation 2 -1-412. After the comments are received and reviewed, the
District will make a final determination on the permit.  
 
I recommend that the District initiate a public notice and consider any comments received prior 
to taking any final action on issuance of a Permit to Operate for the following source:  
 
S-17 Dual -Fueled Digester Gas/Natural Gas Boiler, # 3 
 Make: Cleaver -Brooks,  Model 3700 -60 
 Maximum Input Heat Capacity: 2.51 MMBtu/Hr  
 
 
 
By:        Date:      
 Perry Ng  
 Senior Air Quality Engineer

## conditions
JSONPath: `$.conditions.text`

CONDITIONS
S  
COND #27355   --------------------------------------  
 
This permit condition, as initially adopted in New Source Review Application # 28991, 
is further amended within New Source Review Application # 32022.

## permit_conditions
JSONPath: `$.permit_conditions`

- Item
CONDITIONS
S  
COND #27355   --------------------------------------  
 
This permit condition, as initially adopted in New Source Review Application # 28991, 
is further amended within New Source Review Application # 32022.

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

RECOMMENDATION
TION  
The District has reviewed the material contained in the permit application for the proposed 
project and has made a preliminary determination that the project is expected to comply with all 
applicable requirements of Dist rict, state, and federal air quality -related regulations. The 
preliminary recommendation is to issue a Permit to Operate for the equipment listed below. 
However, the proposed source will be located in an OBC, which triggers the public notification
