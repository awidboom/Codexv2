---
application_number: 32158
plant_id: 3719
plant_name: City of Fairfield
plant_address: Fairfield, CA 94533
evaluation_date: July 1, 2007
source_json: data/permit_evaluations_json/2024/2024-32158-City_of_Fairfield__fid3719_nsr_32158_eval_032924_pdf__application_32158__eval_01.json
---

# Engineering Evaluation (Application 32158)
**Plant**: 3719 City of Fairfield
**Address**: Fairfield, CA 94533
**Evaluation Date**: July 1, 2007

## background
JSONPath: `$.background.text`

BACKGROUND
ND 
The City of Fairfield is applying for an Authority to Construct and Permit to Operate a Prime Generator Set, 
fueled by liquefied petroleum gas (LPG).  
 
S-4 Prime Propane Engine Generator Set 
Make: Power Solutions International, EPA Family: LPSIB21.9NGP, Model 21.9L, 
Model Year 2020, Burn Type: Rich, Rated 582 BHP.  
 
S-4 will be installed at a municipal bus depot located at 420 Gregory Lane in Fairfield, CA. The project will 
reduce air pollution within a disadvantaged community by providing charging capability for electric buses and 
allow the diesel buses serving this area to be retired. 
 
The primary pollutants from LPG engines are the products of combustion, including nitrogen oxides (NO x), 
carbon monoxide (CO), hydrocarbon and other organic compounds (precursor organic compounds, POCs), 
sulfur dioxide (SO 2), and particulate matter (PM 10 and PM 2.5). Various toxic air contaminants (TACs) are also 
emitted during the combustion of LPG. 
 
The new source is located within an overburdened community, and the project required a Health Risk Assessment 
(HRA); therefore, this application is subject to the public notice requirements of BAAQMD Regulation 2-1-412.

## emission_calculations
JSONPath: `$.emission_calculations.text`

EMISSION CALCULATIONS
NS  
Basis and Assumptions: 
- Maximum output rating of 582 brake horsepower (BHP), per EPA certification rating data 
- Liquified propane density of 4.23 lb/gallon 
- Maximum fuel consumption of 162 lb/hr, per manufacturer 
- Maximum volumetric fuel consumption of 38.30 gallons/hr (162 lb/hr / 4.23 lb/gallon) 
- Maximum operation: 1053 hours (40,328 gallons propane) per year, up to 9 hours (344.7 gallons 
propane) per day 
- Heat Conversion: 8063 British thermal units (Btus) per BHP for LPG fuel 
- For the US Environmental Protection Agency (EPA) Certification Emission Rate for “HC+NOx”, the 
portions may be considered 95% NOx and 5% hydrocarbons (HC). For the purposes of this evaluation, 
HC = POC.Emissions
[lb/hr]  Acute 
Trigger 
Level [lb/hr] HRA 
Triggered? 
(Acute) Annual 
Emissions 
[lb/yr] Chronic 
Trigger 
Level [lb/yr] HRA 
Triggered? 
(Chronic)  
1,1,2,2-Tetrachloroethane 2.53E-05 AP-42 1.2E-04 None None 2.8E-01 1.40E+00 No 
1,1,2-Trichloroethane 1.53E-05 AP-42 7.2E-05 None None 1.7E-01 5.00E+00 No 
1,1-Dichloroethane 1.13E-05 AP-42 5.3E-05 None None 1.2E-01 5.00E+01 No 
1,3-Butadiene 1.02E-04 CATEF 4.8E-04 2.90E-01 No 1.1E+00 4.80E-01 YES 
Acetaldehyde 8.66E-04 CATEF 4.1E-03 2.10E-01 No 9.5E+00 2.90E+01 No 
Acrolein 5.36E-04 CATEF 2.5E-03 1.10E-03 YES 5.9E+00 1.40E+01 No 
Benzene (no control) 1.87E-03 CATEF 8.8E-03 1.20E-02 No 2.1E+01 2.90E+00 YES 
Carbon Tetrachloride 1.77E-05 AP-42 8.3E-05 8.40E-01 No 1.9E-01 1.90E+00 No 
Chlorobenzene 1.29E-05 AP-42 6.1E-05 None None 1.4E-01 3.90E+04 No 
Chloroform 1.37E-05 AP-42 6.4E-05 6.60E-02 No 1.5E-01 1.50E+01 No 
Ethylbenzene 1.14E-05 CATEF 5.3E-05 None None 1.3E-01 3.30E+01 No 
Ethylene Dibromide 2.13E-05 AP-42 1.0E-04 None None 2.3E-01 1.10E+00 No 
Formaldehyde (no control) 2.30E-03 CATEF 1.1E-02 2.40E-02 No 2.5E+01 1.40E+01 No 
Methanol 3.06E-03 AP-42 1.4E-02 1.20E+01 No 3.4E+01 1.50E+05 No 
Methylene Chloride 4.12E-05 AP-42 1.9E-04 6.20E+00 No 4.5E-01 8.20E+01 No 
Naphthalene 7.50E-05 CATEF 3.5E-04 None None 8.2E-01 2.40E+00 No 
PAH Equivalent as 
Benzo(a)pyrene  1.78E-07 CATEF 8.4E-07 None None 2.0E-03 3.30E-03 No 
Propylene 1.57E-02 CATEF 7.4E-02 None None 1.7E+02 1.20E+05 No 
Styrene 1.19E-05 AP-42 5.6E-05 9.30E+00 No 1.3E-01 3.50E+04 No 
Toluene 1.05E-03 CATEF 4.9E-03 2.20E+00 No 1.2E+01 1.60E+04 No 
Vinyl Chloride 7.18E-06 AP-42 3.4E-05 8.00E+01 No 7.9E-02 1.10E+00 No 
Xylene (total) 6.45E-04 CATEF 3.0E-03 9.70E+00 No 7.1E+00 2.70E+04 No 
 
1 CATEFs are used when AP-42 EFs are less conservative than CATEFs. Reported mean emission factor values are used in accordance with District procedures.  
 
Based on the calculations in Table 3 below, some TACs exceed the District’s Risk Screening trigger levels set 
forth in Table 1 of Reg. 2-5 (New Source Review for Toxic Air Contaminants). Therefore, a Health Risk 
Assessment (HRA) is required. 
 
The BAAQMD therefore undertook an HRA to evaluate the potential acute, chronic, carcinogenic and non-
carcinogenic health risks from emissions from this project. The HRA evaluated risks to workers and to 
residents in the vicinity of the project. 
 
Results from the HRA indicate that the maximum project cancer risk is 2.2 in a million , the project maximum 
chronic hazard index is 0.017, and the project maximum acute hazard index is 0.057. In accordance with the 
District’s Regulation 2-5-301, this source requires TBACT because the cancer risk exceeds 1.0 in a million. 
Rather than apply TBACT, the applicant instead chose to accept a reduction in permitted usage of the new 
engine. By reducing annual usage from 2,340 hours per year to 1,053 hours per year, the project cancer risk no 
longer exceeds 1.0 in a million. 
 
This project is located in an overburdened community (OBC), as defined by Regulation 2-1-243; therefore, the 
project must comply with the project cancer risk limit of 6 in a million.  Since the estimated project cancer risk 
does not exceed 6 in a million and project hazard indices do not exceed 1.0, this project complies with the 
District’s Regulation 2-5-302 project risk requirements. 
 
Compliance with Regulation 2-5 is therefore satisfied.

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

Plant Cumulative Increase:
Table 2 summarizes the cumulative increase in criteria pollutant emissions resulting from the operation of S-4. 
 
Table 2 – Plant Cumulative Emissions 
Pollutant Emissions (TPY)  
Existing New Total 
NOx 0.000 0.191 0.191 
CO 0.000 0.302 0.302 
POC 0.000 0.010 0.010 
PM10 0.000 0.048 0.048 
PM2.5 0.000 0.048 0.048 
SO2 0.000 0.001 0.001

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

- For the purposes of this evaluation, toxic air contaminant (TAC) emissions from this engine can be
estimated using TAC emission factors from natural gas. 
 
Annual Emissions and Daily Maximum Emissions: 
The following EPA Certification Emission Rates for HC+NO x, and CO emissions from the engine were used for 
the emission calculations: 
 
HC+NO x = 0.4 g/kW-hr (0.30 g/bhp-hr) 
CO = 0.6 g/kW-hr (0.45 g/bhp-hr)  
 
NOx and POC emissions rates were calculated as follows: 
 
NOx = (0.30 g/bhp-hr) * (95%) = 0.28 g/bhp-hr 
POC = (0.30 g/bhp-hr) * (5%) = 0.015 g/bhp-hr 
 
The particulate matter (PM) and SO 2 emissions were calculated using emission factors from AP-42 Chapter 3.2 
Natural Gas-fired Reciprocating Engines, Table 3.2-3 (Uncontrolled Emission Factors For 4-Stroke Rich-Burn 
Engines). The total PM emission factor consists of the sum of filterable plus condensable emission factors in 
AP-42. 
 
City of Fairfield, Plant #3719                                                                Application #32158 
 
  
Page 2 of 7   
The daily maximum emissions were calculated assuming 9-hr/day of operation.  
 
The annual and daily maximum emissions from S-4 are summarized below in Table 1. 
 
Table 1 – Daily and Annual Maximum Emissions for S-4 
Pollutant Emission 
Factor Emission 
Factor 
Unit Emissions 
 Daily (lbs/day) Annual (lbs/yr) Annual (TPY) 
NOx 0.28 g/bhp-hr 3.272 382.80 0.191 
CO 0.45 g/bhp-hr 5.166 604.42 0.302 
POC 0.015 g/bhp-hr 0.172 20.15 0.010 
PM10 1.94E-02 lb/MMBtu 0.820 95.91 0.048 
PM2.5 1.94E-02 lb/MMBtu 0.820 95.91 0.048 
SO2 5.88E-04 lb/MMBtu 0.025 2.91 0.001 
a Emission factors for NO x, CO, and POC per EPA certification. 
b Emission factors for PM 10 and SO 2 were retrieved from AP-42 Chapter 3.2 Natural Gas-fired Reciprocating 
Engines, Table 3.2-3. PM emission factors consist of filterable plus condensable fractions. These numbers are 
uncontrolled (unabated) emissions.TOXIC HEALTH RISK ASSESSMENT
Toxic air contaminant (TAC) emission factors from California Air Toxics Emission Factors (CATEF) are 
generally preferred over those found in AP-42. When available, TAC emission factors were therefore retrieved 
from CATEF for Natural Gas-fired Rich Burn Engines rated < 650 hp. When CATEF factors were unavailable, 
values from AP-42, Table 3.2-3 were used. The TAC emission estimates are based on uncontrolled emission 
factors for natural gas engines, and a factor of 1020 btu/cubic foot was used to convert CATEF factors to units 
of lb/MMBtu. 
 
TACs were calculated assuming an operating schedule of 9 hours per day, 5 days per week, and 52 weeks per 
year (2,340 hours per year). 
 
 
 
Table 3 - TAC Emission Estimates 
Compound  Emission 
Factor 
[lb/MMBt
u] Basis Hourly

## BACT
JSONPath: `$.BACT.text`

Best Available Control Technology (BACT)
T)    
In accordance with Reg. 2-2-301 (Best Available Control Technology Requirement), BACT is triggered for any 
new or modified source with the potential to emit 10 pounds or more per highest day of POC, NPOC, NOx, CO, 
SO2 PM10, or PM 2.5. Based on the emission calculations in Table 1, BACT is not triggered since the maximum 
daily emission for all the criteria pollutants are less than 10 pounds per day.

## offsets
JSONPath: `$.offsets.narrative`

Offsets
ts 
Offsets must be provided for any new or modified source at a facility that emits more than 10 tons per year of 
POC or NO x. Based on the emission calculations in Table 1, offsets are not required for this application per Reg 
2-2-302 (Offset Requirements, Precursor Organic Compounds and Nitrogen Oxides). 
 
New Source Performance Standards (NSPS)  
S-4 is subject to 40 CFR 60, Subpart JJJJ, Standards of Performance for Stationary Spark Ignition (SI) Internal 
Combustion Engines (ICEs), per §60.4230(a)(4)(i) because the owner/operator will commence construction after 
June 12, 2006, and the source is an engine which was manufactured after July 1, 2007 and has a maximum power 
greater than 500 hp.  
 
The engine will comply with the limits in (40 CFR 60 Subpart JJJJ) Table 1 for emergency spark-ignited 
engines greater than 130 hp. 
 
 
City of Fairfield, Plant #3719                                                                Application #32158 
 
  
Page 6 of 7  Table 5. NSPS Emission Standards vs. S-4 Engine Family Emission Rates 
Pollutant NSPS Emission Standard* S-4 Emission Rate  
NOx 2.0 g/bhp-hr  0.3 g/bhp-hr 
CO 4.0 g/bhp-hr  0.4 g/bhp-hr 
VOC 1.0 g/bhp-hr 0.01 g/bhp-hr 
 * https://www.law.cornell.edu/cfr/text/40/appendix-Table_1_to_subpart_JJJJ_of_part_60  
 
Based on the EPA Annual Emission Certification Data, S-4 complies with NSPS requirements.    
 
National Emission Standards for Hazardous Air Pollutants (NESHAP)  
S-4 is subject to 40 CFR 63, Subpart ZZZZ, National Emission Standards for Hazardous Air Pollutants for 
Reciprocating Internal Combustion Engines (RICE). Per 40 CFR 63.6590(c)(1), a new or reconstructed 
stationary RICE located at an area source must meet the requirements of NSPS (40 CFR 60, Subpart JJJJ) for 
spark ignition engines. As stated above in the NSPS section, S-4 meets the emissions requirements of NSPS.

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

Prevention of Significant Deterioration (PSD)
D) 
Regulation 2-2-224 defines a PSD project as one at a facility that has the potential to emit 100 tons or more per 
year of any PSD pollutant. This facility will not have the potential to emit 100 tons or more of any PSD pollutant 
therefore, this project is not a PSD project.

## CEQA
JSONPath: `$.CEQA.narrative`

California Environmental Quality Act (CEQA):
The project is ministerial, under the District's CEQA Reg. 2-1-311, and therefore is not subject to CEQA review. 
The engineering review for this project requires only the application of standard permit conditions and standard 
emissions factors as specified in District permit handbook chapter 2.3.2 (Stationary Natural Gas Engines) and 
therefore is not discretionary as defined by CEQA.

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
STATEMENT OF COMPLIANCE
CE 
The owner/operator of S-4 shall comply with Reg. 6-1 (Particulate Matter and Visible Emissions Standards), 
Reg. 9-1-301 (Inorganic Gaseous Pollutants:  Sulfur Dioxide for Limitations on Ground Level Concentrations), 
and Reg. 9-8 (Nitrogen Oxides and Carbon Monoxide from Stationary ICE).   
 
The owner/operator is expected to comply with Reg. 6-1 since the unit is fueled with LPG.  Because the S-4 
engine has displacement of 21.9L (1336.4 cubic inch), the Ringelmann No. 2 Limitation applies per Section 6-
1-303 (ICE engine of less than 25 L or 1500 cubic inch displacement). Thus, for any period aggregating more 
than three minutes in any hour, there should be no visible emission as dark or darker than No. 2 on the 
Ringelmann Chart or be equal to or greater than 40% opacity. S-4 is expected to comply with this requirement, 
as well as the visible particles requirement of Section 6-1-305.  The emission rate from S-4 results in an outlet 
grain loading of 0.01 grains/dscf, which is less than the limit 0.15 grains/dscf and therefore complies with 
Regulation 6-1-310.1.  The TSP limits in 6-1-310.2 does not apply because the potential to emit TSP is below 
1,000 kg per year. 
 
The owner/operator is expected to comply with Regulation 9-1 by restricting fuel to LPG only. Combustion of 
LPG is expected to produce a SO 2 concentration of no more than 1 ppmv. Therefore, the source is expected to 
comply with Section 9-1-301 (Limitations on Ground Level Concentrations) and 9-1-304 (Fuel Burning). 
 
City of Fairfield, Plant #3719                                                                Application #32158 
 
  
Page 5 of 7   
S-4 is expected to comply with the limits identified in Regulation 9-8-301, as shown below. 
 
Table 4: Regulation 9-8-301 Limits 
Pollutant Standard (ppmvd @ 15% O2) Standard (lb/hr) S-4 Emissions Rate (lb/hr) 
NOx 56 1.0 0.4 
CO 2000 21.0 0.6 
 
Assumptions: 
 
lb/hr = ppm * 10^-6 * (1/molar volume) * (molar mass) * Fd * 20.9/(20.9-%O2) * HHV 10^-6 * bhp 
 
where molar volume = 385.3 dscf/lb/mol, Fd = 8710 dscf/MMBtu, %O2 = 15, HHV = 8063, and bhp = 582 
 
NOx 
56 ppm * 10^-6 * (1/385.3 dscf/lb-mol) * (46 lb/lb-mol) * (8710 dscf/MMBtu) * (20.9)/(20.9-15)  
* (8063 Btu/bhp-hr) * 10^-6 * 582 bhp 
= 1.0 lb/hr 
 
CO 
2000 ppm * 10^-6 * (1/385.3 dscf/lb-mol) * (28 lb/lb-mol) * (8710 dscf/MMBtu) * (20.9)/(20.9-15)  
* (8063 Btu/bhp-hr) * 10^-6 * 582 bhp 
= 21.0 lb/hr

## public_notification
JSONPath: `$.public_notification.text`

Public Notification (Regulation 2-1-412)
The project is not within 1,000 feet from the nearest school; however, the project is located within an 
overburdened community and required an HRA. Therefore, a public notice will be distributed and a thirty-day 
public comment period will be initiated.

## conditions
JSONPath: `$.conditions.text`

PERMIT CONDITIONS
NS 
 
Permit Condition # 100266 (applicable to S-4)  
 
1. The owner/operator of S-4 shall operate this source on propane gas fuel exclusively. (Basis: Cumulative 
Increase; Regulation 2-5) 
2. The owner/operator of S-4 shall not exceed 1,053 hours of operation or 40,328 gallons of propane fuel usage 
in any 12-month period. (Basis: Cumulative Increase, Regulation 2-5) 
3. The owner/operator of S-4 shall not exceed 9 hours of operation or 344.7 gallons of propane fuel usage in 
any day. (Basis: BACT) 
4. To determine compliance with the above parts, the owner/operator of S-4 shall maintain the following 
records: 
 
a. Gallons of propane used in each day. 
b. Gallons of propane used in each month. 
c. Gallons of propane used in each rolling 12-month period. 
 
The owner/operator shall record all records in a District-approved log. The owner/operator shall retain the 
records with the equipment for two years, from the date of entry, and make them available for inspection by 
District staff upon request. These record-keeping requirements shall not replace the record-keeping 
requirements contained in any applicable District Regulations. (Basis: Recordkeeping) 
  
 
City of Fairfield, Plant #3719                                                                Application #32158 
 
  
Page 7 of 7  RECOMMENDATION 
The District has reviewed the material contained in the permit application for the proposed project and has made 
a preliminary determination that the project is expected to comply with all applicable requirements of District, 
state, and federal air quality-related regulations. The preliminary recommendation is to issue an Authority to 
Construct for the equipment listed below. However, the proposed source will be located within an overburdened 
community and an HRA was required, which triggers the public notification requirements of Regulation 2-1-
412. After the comments are received from the public and reviewed, the District will make a final determination 
on the permit. 
 
I recommend that the District initiate a public notice and consider any comments received prior to taking any 
final action on issuance of an Authority to Construct and/or a Permit to Operate for the following equipment: 
 
S-4 Prime Propane Engine Generator Set 
Make: Power Solutions International, EPA Family: LPSIB21.9NGP, Model 21.9L, 
Model Year 2020, Burn Type: Rich, Rated 582 BHP. 
Prepared by:  _______________________________________   Date: ________________ 
Daniel Oliver          03/07/2024 
Senior Air Quality Engineer

## permit_conditions
JSONPath: `$.permit_conditions`

- Item 1
The owner/operator of S-4 shall operate this source on propane gas fuel exclusively. (
Basis: Cumulative 
Increase, Regulation 2-5)

- Item 2
The owner/operator of S-4 shall not exceed 1,053 hours of operation or 40,328 gallons of propane fuel usage 
in any 12-month period. (
Basis: Cumulative Increase, Regulation 2-5)

- Item 3
The owner/operator of S-4 shall not exceed 9 hours of operation or 344.7 gallons of propane fuel usage in 
any day. (
Basis: BACT)

- Item 4
To determine compliance with the above parts, the owner/operator of S-4 shall maintain the following 
records: 
 
a. Gallons of propane used in each day. 
b. Gallons of propane used in each month. 
c. Gallons of propane used in each rolling 12-month period. 
 
The owner/operator shall record all records in a District-approved log. The owner/operator shall retain the 
records with the equipment for two years, from the date of entry, and make them available for inspection by 
District staff upon request. These record-keeping requirements shall not replace the record-keeping 
requirements contained in any applicable District Regulations. (
Basis: Recordkeeping) 
  
 
City of Fairfield, Plant #3719                                                                Application #32158 
 
  
Page 7 of 7  RECOMMENDATION 
The District has reviewed the material contained in the permit application for the proposed project and has made 
a preliminary determination that the project is expected to comply with all applicable requirements of District, state, and federal air quality-related regulations. The preliminary recommendation is to issue an Authority to 
Construct for the equipment listed below. However, the proposed source will be located within an overburdened 
community and an HRA was required, which triggers the public notification requirements of Regulation 2-1-

- Item 412
After the comments are received from the public and reviewed, the District will make a final determination 
on the permit. 
 
I recommend that the District initiate a public notice and consider any comments received prior to taking any 
final action on issuance of an Authority to Construct and/or a Permit to Operate for the following equipment: 
 
S-4 Prime Propane Engine Generator Set 
Make: Power Solutions International, EPA Family: LPSIB21.9NGP, Model 21.9L, 
Model Year 2020, Burn Type: Rich, Rated 582 BHP. 
Prepared by:  _______________________________________   Date: ________________ 
Daniel Oliver          03/07/2024 
Senior Air Quality Engineer

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

(empty)
