---
application_number: 678704
plant_id: 203115
plant_name: BHOGC 2225 Bayshore Owner LLC
plant_address: Palo Alto, CA 94303
evaluation_date: June 12, 2006
source_json: data/permit_evaluations_json/2023/2023-678704-BHOGC_2225_Bayshore_Owner_LLC__fid203115_nsr_678704_eval_102023_pdf__application_678704__eval_01.json
---

# Engineering Evaluation (Application 678704)
**Plant**: 203115 BHOGC 2225 Bayshore Owner LLC
**Address**: Palo Alto, CA 94303
**Evaluation Date**: June 12, 2006

## background
JSONPath: `$.background.text`

BACKGROUND
BHOGC 2225 Bayshore Owner LLC  has applied  for an Authority to Construct/ Permit to Operate 
for the following  equipment : 
S-1 Emergency Backup Diesel Generator  
Engine Make:  John Deere , Model: 6135HFG75A , Family  NJDXL13.5132      
Model Year: 2022, 755 BHP , 571 kW, 4.916  MMBtu/h our 
Abated by  
A-1  CARB cert ified Diesel Catalyzed Particulate Filter (DCPF)  
Make: Johnson Matthey Model: JM-CRT(+) -3-N-CS-BIT0 -10/10 -LP 
CARB Executive Order : DE-08-009-12 
S-1 is a Tier 3 engine whose diesel exhaust particulate matter (DEPM) emissions will be abated 
by A-1. The engine  will burn commercially available California low sulfur diesel fuel. The sulfur 
content of the diesel fuel will not exceed 0.0015% by weight.  
S-1 will emit the following pollutants:  
Oxides of nitrogen (NOx), Precursor organic compounds (POC), Carbon monoxide (CO) , 
Particulate matter with aerodynamic diameter smaller than or equal to a nominal 10 microns  
(PM10 ), Particulate matter with aerodynamic diameter smaller than or equal to a nominal 2.5 
microns  (PM2.5 ), and  Sulfur dioxide (SO2) .

## emission_calculations
JSONPath: `$.emission_calculations.text`

EMISSIONS
Table 1. Annual and Daily Emissions  from S-1 
Pollutant  Emission 
Factor(1) Max Daily 
Emissions  Abatement  Annual 
Emissions  Annual 
Emissions  
(g/bhp -hour)  (pounds/day)  (pounds/year)  (tons/year)  
NOx 4.04 161.2 4   335.93 0.168  
POC  0.21 4.19 50%(4) 8.73 0.004 
CO 0.37 5.91 60%(4) 12.31  0.006 
PM 10 0.05 0.30 85%(5) 0.62 0.000  
PM 2.5 N/A(2) 0.30 85%(5) 0.62 0.000  
SO 2 N/A(3) 0.19   0.39 0.000  
Basis:  
• Annual emissions: Reliability -related activity  set at  50 hours  for S-1 
• Maximum  daily emissions: 24-hour operation  
• 1Emission factors for EPA engine family NJDXL13.5132 were not available so they were 
calculated from the EPA certified Carryover family CJDXL13.5132  
 
 
 2 • 2PM 2.5 = PM 10  
• 3SO 2 emission factor calculated based on the following:  
o Complete conversion of sulfur in fuel to SO 2 and a maximum sulfur content of 15 
ppm.  
o Density of Ultra Low Sulfur Diesel Fuel = 7.31 lb/gal  
o Fuel Consumption Rate = 35.5 gal/hr  
o MW(SO 2)=64.066 g/mol e, MW(S)=32.065 g /mol 
o 𝐸𝑆𝑂2=(15 𝑙𝑏 𝑆
10𝐸+06 𝑙𝑏 𝑓𝑢𝑒𝑙)(7.31 𝑙𝑏 𝑓𝑢𝑒𝑙
𝑔𝑎𝑙  𝑓𝑢𝑒𝑙)(35.5𝑔𝑎𝑙  𝑓𝑢𝑒𝑙
ℎ𝑟 )(64.066  𝑔
𝑚𝑜𝑙⁄
32.065  𝑔
𝑚𝑜𝑙⁄)(50ℎ𝑟 
𝑦𝑟) 
𝐸𝑆𝑂2=0.19𝑙𝑏𝑑𝑎𝑦⁄ =0.39𝑙𝑏𝑦𝑟⁄ =0.000𝑡𝑜𝑛𝑦𝑟⁄ 
• 4 POC and CO abatement efficiencies for DICE equipped with DCPF suggested in 
“Engineer Guidelines for Screening Form ICE Prior to Data Entry ”. 
• 5 DCPF abatement efficiency specified in CARB Executive Order DE -08-009-12

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

CUMULATIVE INCREASE
Table 2 summarizes the  cumulative increase in criteria pollutant emissions that will result from this 
application assuming S-1 will operate for 50 hours/year for reliability related testing.  
Table 2. Cumulative Emissions Increase, Post 4/5/91  
Pollutant  Existing Emissions Post 
4/5/91 (tons/year)  S-1 Emissions 
(tons/year)  Cumulative 
Emissions 
(tons/year)  
NOx 0 0.168  0.168  
POC  0 0.004 0.004 
CO 0 0.006 0.006 
PM 10 0 0.000  0.000  
PM 2.5 0 0.000  0.000  
SO 2 0 0.000  0.000

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

HEALTH RISK ASSESSMENT (HRA)
The proposed engine will emit diesel exhaust particulate matter, which is a TAC under BAAQMD 
Regulations. BAAQMD Regulation 2, Rule 5 specifies that diesel exhaust particulate matter will be 
used as a surrogate for all TAC emissions from diesel -fueled comp ression -ignition internal 
combustion engines, as this is the principal driver of the health risk associated with this type of 
equipment. The calculated emissions increase of diesel exhaust particulate matter associated with 
the project are summarized in th e table below. The project does not include any related New Source 
Review applications for new or modified sources permitted within the previous five -year period (per 
BAAQMD Reg 2 -5-216).  
Table 3. Hourly and Annual Project TAC Emissions  
Pollutant  Hourly  Annual  Acute 
Trigger 
(lbs/hr)  Chronic  
Trigger  
(lbs/yr)  Exceeds 
Acute  
Trigger ? Exceeds 
Chronic 
Trigger?  lbs/hr  lbs/year  
Diesel PM  
(diesel exhaust N/A 0.62 N/A 0.26 N/A YES 
 
 
 3 particulate 
matter)  
 
Regulation 2 -5-402 requires a Health Risk Assessment (HRA) if TAC emissions exceed the 
screening thresholds set forth in Table 2 -5-1 in Regulation 2, Rule 5. For this project, the emissions 
of diesel particulate matter exceed the Table 2 -5-1 screening thre shold for chronic risk, respectively.  
This project qualifies for the HRA Streamlining Policy because the facility is not located in an 
overburdened community, the nearest offsite receptor is greater than 300 feet away, and the total 
engine diesel PM emissions are less than 10 pounds/year . Therefore, a refined HRA was not 
required.  
Compliance with Regulation 2 -5 is therefore satisfied.Airborne Toxic Control Measure (ATCM) for Emergency Standby Diesel -Fueled CI Engines
(>50 bhp)  
The Air District is charged with enforcing the requirements of California’s Air Toxic Control 
Measure for Stationary Compression Ignition Engines in Title 17, California Code of Regulations, 
Sections 93115 et seq . (ATCM)  
 
 
 5 Subsection 93115.6(a)(3)(A)(1)(a) requires S-1 to meet the emissions standards specified in Table 
6 below. (These emissions standards expressed as g/bhp -hour are essentially the same as EPA’s 
Tier 2 standards, which are expressed as g/kW -hour.1) The generator will have emission rates that 
comply with these requirements as shown  in Table 6.  
 
Table 6. Engine Emission Rates vs. ATCM Emission Standards (g/bhp -hour)  
Pollutant  Emissions Rate  
S-1 ATCM Emission Standards  
PM 0.05 0.15 
NMHC + NO x 
(NMHC: Non-methane 
hydrocarbon)  4.25 4.8 
CO 0.37 2.6 
 
Subsection 93115.6(a)(3)(A)(1)(b)  requires that the generator be certified to meet EPA’s Tier 2 
emission standards as required under the NSPS discussed below.  The generator meets EPA 
Tier 2 standards.  
Subsection 93115.6(a)(3)(A)(1)(c)  limits the non -emergency operation of the engine to 50 
hours/year for maintenance and testing. Permit Condition 100073  will limit non -emergency 
operation  of S-1 to 50 hours/year and hence will comply with this subsection.Toxics, "ATCM for Stationary Compression Ignition Engines" Sec tion 93115.6(a)(3) or
93115.6(b)(3), title 17, CA Code of Regulations]  
 
 
 8 2. The owner/operator shall comply with requirements for CARB Executive Order DE -08-009-12. 
[Basis: CARB Executive Order  DE-08-009-12, "ATCM for Stationary Compression Ignition 
Engines" Section 93115.13(f), title 17, CA Code of Regulations, Toxics, Section s 2700 through 
2711 of title 13, CA Code of Regulations]  
 
End of Conditionsand federal air quality -related regulations, including the health risks resulting from toxic air
contaminant emissions. The preliminary recommendation is to issue a permit for this project. After 
considering all comments received, the Air District will make a final determination.  
I recommend that the Air District initiate the public comment period and consider any comments 
received prior to taking any final action on issuance of an Authority to Construct for the following 
source:  
S-1 Emergency Backup Diesel Generator  
Engine Make:  John Deere , Model:  6135HFG75A , Family NJDXL13.5132     
Model Year: 202 2, 755 BHP, 571 kW, 4.916  MMBtu/hour  
Abated by  
A-1  CARB cert ified Diesel Catalyzed Particulate Filter (DCPF)  
Make: Johnson Matthey Model: JM-CRT( +)-3-N-CS-BIT0 -10/10 -LP 
CARB Executive Order : DE-08-009-12 
 
 
__________________      Date: _________________         
Chris Thompson  
AQ Engineer I

## BACT
JSONPath: `$.BACT.text`

BEST AVAILABLE CONTROL TECHNOLOGY (BACT)
Per Regulation 2 -2-301, an Authority to Construct and/or Permit to Operate for a new source shall 
require BACT to control emissions of a District BACT pollutant as defined in Regulation 2 -2-210 if 
the source will have the potential to emit (PTE) that pollutant in an amount of 10.0 or more pounds 
on any day, as defined in Regulation 2 -2-301.1.  
Per Table 1, S-1’s PTE for NOx exceeds  10.0 or more pounds on any day  and triggers BACT . 
BACT for S -1 is presented in the current BAAQMD BACT/TBACT Workbook for IC Engine – 
Compression Ignition: Stationary Emergency, non -Agricultural, non -direct drive fire pump, for 
engines greater than or equal to 50 bhp and less than 1,000 bhp: Document #96.1.3, Revisio n 8, 
dated 12/22/2020. For NOx, BACT(2) is 4.56 g/bhp -hour. The more restrictive BACT(1) standards 
are not applicable to S -1 because it will be limited to operate as an emergency standby engine.  
S-1 satisfies the current BACT(2) standards for NOx as shown in Table 4.  
 
Table 4. BACT check  
Pollutant  Emission Factor  BACT(2) Standard  
NOx 4.04 g/bhp -hour 4.56 g/bhp -hour

## offsets
JSONPath: `$.offsets.narrative`

OFFSETS
BHOGC 2225 Bayshore Owner LLC  is a new facility and doesn’t have any sources of air 
emissions. S -1 will be the facility’s first permitted source. In accordance with the District’s Policy 
for Calculating Potential to Emit (PTE) of Emergency Generators, the Potential to Emit for S-1 was 
estimated assuming 150 hours of operation/year as shown in Table 5. 
 
Table 5. Offsets  
Pollutant  Pre-
Application  
PTE 
(tons/year)  S-1’s PTE 
(tons/year)  Facility 
PTE 
(tons/year)  Offset 
Triggers  Offsets 
Required 
(Yes/No) 
NOx 0 0.504  0.504  >10 No 
POC  0 0.013 0.013 >10 No 
 
 
 4 CO 0 0.018 0.018 N/A N/A 
PM 10 0 0.001 0.001 >100  No 
PM 2.5 0 0.001 0.001 >100  No 
SO 2 0 0.001  0.001  >100  No 
 
It can be seen from Table 5 that the facility’s PTE after  S-1 is permitted is below the Regulation 2 -
2 offset trigger levels. Therefore, offsets are not required .

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

Prevention of Significant Deterioration ( PSD)
PSD does not apply to this application.

## CEQA
JSONPath: `$.CEQA.narrative`

California Environmental Quality Act ( CEQA )
This project is ministerial  under the District Regulation 2 -1-311 (Permit Handbook Chapter 2.3 .1) 
and therefore is not subject to CEQA review  per CCR § 15369.  
New Source Performance Standards ( NSPS ) 
40 CFR 60, Subpart IIII (NSPS IIII), Standards of Performance for Stationary Compression Ignition 
Internal Combustion Engines applies to non-fire pump engines  such as S-1 that were manufactured 
after April 1, 2006. Per §60.4205(b), S -1 is subject to the Tier 2 or Tier 3  emissions standards in 40 
CFR 1039, Appendix I for all pollutants.  
Applicable emission  Tier 2 standards found in Appendix I of 40 CFR 1039 that apply to S -1 are:  
NMHC + NOx = 6.4 gram /kW-hour (4.8 gram/bhp -hour);   
CO = 3.5 gram/kW -hour (2.6 gram/bhp -hour); and  
PM = 0.20 gram/kW -hour (0.15 gram/bhp -hour).  
Emission rates for the above pollutants summarized in Table s 1 and 6 in this evaluation shows that 
S-1 complies with the emission standards in NSPS IIII.   
40 CFR 89.113 (a) sets forth the following smoke emission standards for non -road CI engines:  
 
 
1 The conversion factor for converting engine output in horsepower to kilowatts is 1.341 hp/kw. 
Applying this conversion factor to the ATCM standards shows that they are essentially identical to 
EPA’s Tier 2 standards.  
 
 
 6 • 20% during the acceleration mode;  
• 15% during the lugging mode; and  
• 50% during the peaks in either the acceleration or lugging modes.  
The opacity standards in 40 CFR 89.113 it appears, apply to mobile (and not stationary) non -road 
CI engines. Therefore, S-1 is not subject to the above standards. Instead, S-1 is subject to the 
opacity standards in Regulation 6, Rule 1, which was discussed above.  
Per §60.4207(b), S-1 is subject to the following diesel fuel requirements in 40 CFR 80.510(c):  
• Sulfur content ≤ 15 ppm  
• Minimum Cetane index = 40 or maximum aromatic content of 35% by volume  
Diesel fuel sold in California meets the above standards. Therefore, S-1 complies with the diesel 
fuel requirements in NSPS IIII.  
National Emissions Standards for Hazardous Air Pollutants ( NESHAP ) 
S-1 is subject to 40 CFR 63, Subpart ZZZZ (MACT ZZZZ), National Emission Standards for 
Hazardous Air Pollutants for Stationary Reciprocating Internal Combustion Engines because the 
engine will be constructed (~installed) on/after June 12, 2006.  Per §63.6590(c)( 1), “new” sources 
such as S-1 are required to meet the requirements in MACT ZZZZ by meeting the requirements in 
NSPS IIII.  As previously discussed, S-1 will compl y with NSPS IIII and therefore, will comply with 
MACT ZZZZ as well.

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
STATEMENT OF COMPLIANCE
The owner/operator is expected to comply with all applicable requirements. Key requirements are 
listed below:  
Regulation 6 -1 (Particulate Matter – General Requirements ) 
S-1 is subject to Regulation 6, Rule 1 .  Opacity and visible emissions from S-1 is limited by 
Regulation 6-1-303.2 (engine used solely as a standby source of motive power)  to an opacity of No. 
2 on the Ringelmann chart . 
Regulation 6 -1-305 prohibits emission of particles from any operation in sufficient number to cause 
annoyance to any other person where the particles are large enough to be visible as individual 
particles at the emission point, or of such size and nature as to be visible individually as incandescent 
particles.  S-1 is not expected to produce visible emissions or fallout in violation of this regulation and 
will be assumed to be in compliance with Regulation 6 -1-305. 
S-1 compliance with Regulation 6, Rule 1  will be confirmed by the District’s Compliance & 
Enforcement staff during their routine inspections.  
Regulation 9 -1-301 ( Limitations on Ground Level Concentrations ) 
S-1 is subject to and are expected to comply with the applicable SO 2 limitations in Regulation 9, 
Rule 1 (“Inorganic Gaseous Pollutants – Sulfur Dioxide”).  Because SO 2 emissions from S-1 are 
negligible, it is unlikely the APCO will require BHOGC 2225 Bayshore Owner LLC  to conduct ground 
level monitoring.  
Regulation 9 -8 (Nitrogen Oxides and Carbon Monoxide from Stationary Internal 
Combustion Engines ) 
S-1 will be operated as an emergency standby engine and is therefore not subject to the emission 
rate limits in Regulation 9, Rule 8 ("Inorganic Gaseous Pollutants – NOx and CO from Stationary 
Internal Combustion Engines").  S-1 is exempt from the requirements of Sections 9 -8-301 through 
305, 501, and 503 per Reg. 9 -8-110.5 (Emergency Standby Engines).  S-1 is subject to and is 
expected to comply with 9 -8-330.3 (Emergency Standby Engines, Hours of Operation) since  non-
emergency hours of operation will be limited in the permit conditions to 50 hours per year. S-1 is 
also subject to and is expected to comply with monitoring and record keeping requirements of 
Regulations 9 -8-502.1 and 9 -8-530, which are incorporated into the proposed permit conditions.

## public_notification
JSONPath: `$.public_notification.text`

School  Notification  (Regulation  2-1-412)
S-1 is located within 1,000 feet of the outer boundary of a K -12 school site  (Fusion Academy Palo 
Alto located at 2191 E Bayshore Road Suite 100, Palo Alto, CA 94303) .  Therefore, S-1 is subject 
to the public notification requirements of Regulation 2 -1-412. 
Overburdened Communities Notification ( Regulation 2 -1-412) 
S-1 is not located within an Overburdened Community as defined in Regulation 2 -1-243.  Therefore, 
S-1 is not subject to the public notification requirements of Regulation 2 -1-412.

## conditions
JSONPath: `$.conditions.text`

PERMIT CONDITIONS
IONS  
 
 
Permit Condition # 100072  for S-1 
1. The owner or operator shall operate each emergency standby engine only for the following 
purposes: to mitigate emergency conditions, for emission testing to demonstrate 
compliance with a District, state or Federal emission limit, or for reliability -related  activities 
(maintenance and other testing, but excluding emission testing). Operating while 
mitigating emergency conditions or while emission testing to show compliance with 
District, state or Federal emission limits is not limited.  
 
 
 7 [Basis: Title 17, California Code of Regulations, section 93115, ATCM for Stationary CI 
Engines]  
2. The owner/operator shall operate each emergency standby engine only when a non -
resettable totalizing meter (with a minimum display capability of 9,999 hours) that 
measures the hours of operation for the engine is installed, operated and properly 
maintained . 
[Basis: Title 17, California Code of Regulations, section 93115, ATCM for Stationary CI 
Engines]  
3. Records: The owner/operator shall maintain the following monthly records in a District -
approved log for at least 36 months from the date of entry (60 months if the facility has 
been issued a Title V Major Facility Review Permit or a Synthetic Minor Operati ng Permit). 
Log entries shall be retained on -site, either at a central location or at the engine’s location, 
and made immediately available to the District staff upon request.  
a. Hours of operation for reliability -related activities (maintenance and testing).  
b. Hours of operation for emission testing to show compliance with emission limits.  
c. Hours of operation (emergency).  
d. For each emergency, the nature of the emergency condition.  
e. Fuel usage for each engine(s).  
[Basis: Title 17, California Code of Regulations, section 93115, ATCM for 
Stationary CI Engines]  
4. At School and Near -School Operation: If the emergency standby engine is located on 
school grounds or within 500 feet of any school grounds, the following requirements shall 
apply: The owner or operator shall not operate each stationary emergency standby di esel-
fueled engine for non -emergency use, including maintenance and testing, during the 
following periods:  
a. Whenever there is a school sponsored activity (if the engine is located on school 
grounds)  
b. Between 7:30 a.m. and 3:30 p.m. on days when school is in session.  
“School” or “School Grounds” means any public or private school used for the purposes of 
the education of more than 12 children in kindergarten or any of grades 1 to 12, inclusive, 
but does not include any private school in which education is primarily con ducted in a 
private home(s). “School” or “School Grounds” includes any building or structure, 
playground, athletic field, or other areas of school property but does not include 
unimproved school property.  
[Basis: Title 17, California Code of Regulations, s ection 93115, ATCM for Stationary CI 
Engines]  
 
Permit Condition # 100073  for S-1 
The owner/operator shall not exceed the following limits per year per engine for reliability -related 
activities:  
50 Hours of Diesel fuel (Diesel fuel)  
[Basis: Cumulative Increase; Regulation 2 -5; Title 17, California Code of Regulations, section 
93115, ATCM for Stationary CI Engines]  
Permit Condition # 100102  for S-1 
1. The owner/operator shall abate the particulate emissions from the emergency diesel engine by 
the Diesel Oxidation Catalyst/Particulate Filter at all times the engine is in operation. [Basis:

## permit_conditions
JSONPath: `$.permit_conditions`

- Item 1
The owner or operator shall operate each emergency standby engine only for the following 
purposes: to mitigate emergency conditions, for emission testing to demonstrate 
compliance with a District, state or Federal emission limit, or for reliability -related  activities 
(maintenance and other testing, but excluding emission testing). Operating while 
mitigating emergency conditions or while emission testing to show compliance with 
District, state or Federal emission limits is not limited.  
 
 
 7 [
Basis: Title 17, California Code of Regulations, section 93115, ATCM for Stationary CI 
Engines]

- Item 2
The owner/operator shall operate each emergency standby engine only when a non -
resettable totalizing meter (with a minimum display capability of 9,999 hours) that 
measures the hours of operation for the engine is installed, operated and properly 
maintained . 
[
Basis: Title 17, California Code of Regulations, section 93115, ATCM for Stationary CI 
Engines]

- Item 3
Records: The owner/operator shall maintain the following monthly records in a District -
approved log for at least 36 months from the date of entry (60 months if the facility has 
been issued a Title V Major Facility Review Permit or a Synthetic Minor Operati ng Permit). 
Log entries shall be retained on -site, either at a central location or at the engine’s location, 
and made immediately available to the District staff upon request.  
a. Hours of operation for reliability -related activities (maintenance and testing).  
b. Hours of operation for emission testing to show compliance with emission limits.  
c. Hours of operation (emergency).  
d. For each emergency, the nature of the emergency condition.  
e. Fuel usage for each engine(s).  
[
Basis: Title 17, California Code of Regulations, section 93115, ATCM for 
Stationary CI Engines]

- Item 4
At School and Near -School Operation: If the emergency standby engine is located on 
school grounds or within 500 feet of any school grounds, the following requirements shall 
apply: The owner or operator shall not operate each stationary emergency standby di esel-
fueled engine for non -emergency use, including maintenance and testing, during the 
following periods:  
a. Whenever there is a school sponsored activity (if the engine is located on school 
grounds)  
b. Between 7:30 a.m. and 3:30 p.m. on days when school is in session.  
“School” or “School Grounds” means any public or private school used for the purposes of 
the education of more than 12 children in kindergarten or any of grades 1 to 12, inclusive, 
but does not include any private school in which education is primarily con ducted in a 
private home(s). “School” or “School Grounds” includes any building or structure, 
playground, athletic field, or other areas of school property but does not include 
unimproved school property.  
[
Basis: Title 17, California Code of Regulations, s ection 93115, ATCM for Stationary CI 
Engines]  
 
Permit Condition # 100073  for S-1 
The owner/operator shall not exceed the following limits per year per engine for reliability -related 
activities:  
50 Hours of Diesel fuel (Diesel fuel)  
[Basis: Cumulative Increase, Regulation 2 -5, Title 17, California Code of Regulations, section 
93115, ATCM for Stationary CI Engines]  
Permit Condition # 100102  for S-1

- Item 1
The owner/operator shall abate the particulate emissions from the emergency diesel engine by 
the Diesel Oxidation Catalyst/Particulate Filter at all times the engine is in operation. [

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

9 RECOMMENDATION
ENDATION  
 
The Air District has evaluated the permit application for the proposed project and has made a 
preliminary determination that the project is expected to comply with all applicable District, state,
