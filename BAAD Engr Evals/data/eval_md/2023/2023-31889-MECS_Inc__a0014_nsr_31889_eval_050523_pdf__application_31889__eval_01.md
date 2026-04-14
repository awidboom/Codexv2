---
application_number: 31889
plant_name: MECS , Inc.
plant_address: Martinez, CA 94553
evaluation_date: March 17, 2023
source_json: data/permit_evaluations_json/2023/2023-31889-MECS_Inc__a0014_nsr_31889_eval_050523_pdf__application_31889__eval_01.json
---

# Engineering Evaluation (Application 31889)
**Plant**:  MECS , Inc.
**Address**: Martinez, CA 94553
**Evaluation Date**: March 17, 2023

## background
JSONPath: `$.background.text`

BACKGROUND
OUND 
 
MECS  is applying for an Authority to Construct  (AC)/Permit to Operate  (PO)  for the 
following equipment : 
 
S-93 Steam Boiler 
Make: Victory  Engine Model: F2 -DB-574L -300X -S275 
Maximum Firing Rate:  9.33 MM Btu/hr  
Permit Condition No s. 27891 
 
MECS operates within the Marathon Martine oil refinery. As the Marathon refinery began 
to adjust to a renewable fuels refinery in 2020, many of the utilities and services it historically 
provided to the MECS plant were scheduled to shut down. One of the se rvices which were 
shut down was the provision of pressurized steam. MECS must now provide its own 
pressurized steam. Steam is currently being provided to the plant via a temporary mobile 
boiler, but this application is to permit a permanent solution. The purpose of this application 
is to apply for a Permit to Operate for S -93 and to remove the registered temporary mobile 
boiler, S -91. 
 
Even though the proposed boiler is rated at less than 10 MMBtu/hr, which would normally 
only require registration rather th an a Permit to Operate , a certified package boiler could not 
provide steam at the pressure necessary to serve MECS process operations. Therefore, MECS 
contracted to have a boiler built specifically to serve the se process needs. This customized 
boiler cannot be tested for certification purposes. Since the boiler cannot be tested for 
certification, it requires an Authority to Construct and Permit to Operate .  
 
The criteria pollutants are nitrogen oxides (NOx), carbon monoxide (CO), volatile organic 
compounds ( VOC), sulfur dioxide (SO 2) and particulate matter ( PM 2.5 and PM 10).   
 
The facility proposes to use natural gas supplied by Pacific Gas & Electric (PG&E) , which 
is regulated by the California Public Utilities Commission (CPUC),  or natural gas supplied 
by a private entity  (non CPUC -regulated) . Due to the potential fluctuations in the quantity of 
the gas proposed for use, the facility requested that the permitted NOx concentrations be set 
at the regulatory limit of 15 ppmv, dry at 3% (0.0182 lbs/MM  BTU) oxygen pursuant to 
Regulation 9- 7-307.2, as opposed to 9 ppmv, dry at 3% oxygen estimated by the vendor.  
 
The boiler manufacturer guarantees a CO concentration of 55 ppm, dry at 3% oxygen (0.0407 
lbs/MM BTU) .

## emission_calculations
JSONPath: `$.emission_calculations.text`

EMISSIONS
NS  
 
As stated earlier, MECS has indicated that the facility plans to operate S -93 on either 
natural gas supplied by PG&E or natural gas supplied by a private entity. Emissions from 
both scenarios are compared below and the highest emission values will be used to 
determine compliance with Air District regulations.  
 
Emission factors used to determine emissions from NOx and CO are calculated using the 
following formula:  
 
𝐸𝐸𝐸𝐸 �𝑙𝑙𝑙𝑙
𝑀𝑀𝑀𝑀𝑀𝑀𝑀𝑀𝑀𝑀�= 𝑝𝑝𝑝𝑝𝑝𝑝
106 ×𝐸𝐸𝑑𝑑 × �20.9
20.9−%𝑂𝑂2� × 𝑀𝑀𝑀𝑀
𝑀𝑀𝑣𝑣 
 
Where,  
EF = emission factor (lb/MM  Btu)  
Mv = molar volume ( scf/lb-mole ) 
ppm = concentration in parts per million of NOx or CO  
Fd = ratio of gas volume to the heat content of the fuel (dscf /MM Btu heat input)  
MW = molecular weight (lb/lb -mole)  
%O 2 = percentage of oxygen in gas  
 
Basis:   
 Operation Schedule : 24-hours/day , 7-days/week, 52- weeks /year, 8760 hours / year  
 Fuel Heat Value: 1 020 Btu/scf  (CPUC -regulated) or 1022 Btu/scf ( facility tested non 
CPUC -regulated)  
 Max Fuel Rate: 9.334 MMBtu/hour , 9,151 scf/hour  
 Fuel Usage: 817,658 Therms/year, 224 MM  Btu/day, 81,766 MM  Btu/year  
 Conservative Assumption: All PM emissions are PM2.5 
 Fd (CPUC -regulated):  8,710 dscf  exhaust/ MMBtu heat input @ 68 °F and 1 atm  
 Fd (non CPUC -regulated): 8,710 dscf exhaust/MMBtu heat input @ 68 °F and 1 atm  
 Molar Volume: 385.3 scf/ lb-mole at 68  oF and 1 atm  
 Molecular Weight of NOx: 46 lb/ lb-mole  
 Molecular Wei ght of CO: 28 lb/ lb-mole  
 Molecular Weight of VOC as methane: 16 lb/ lb-mole  
Molecular Weight of SO2: 64 lb/ lb-mole  
 
 1 Table 1. Annual and Daily Emissions from CPUC- Regulated Natural Gas Combustion in S- 93 Boiler  
Pollutant  Emission Factor  Post Project Emissions  BACT trigger   
lb/MM cu. ft. 
fuel input  lb/MM  Btu         
fuel input  Reference  max lb/hr  max lb/day  lb/yr  tons/yr  (lb/day)  Yes/No  
NOx   
0.0182  B 0.17 4.08 1489  0.745  10.0 NO 
CO  
0.0407  B 0.38 9.11 3325  1.662  10.0 NO 
VOC  5.5 0.0054  A 0.05 1.21 441 0.220  10.0 NO 
PM10  7.6 0.0075  A 0.07 1.67 609 0.305  10.0 NO 
PM2.5  7.6 0.0075  A 0.07 1.67 609 0.305  10.0 NO 
SO2 0.6 0.0006  A 0.01 0.13 48 0.024  10.0 NO 
Notes:   
 Reference A:  AP-42, 5th Edition, Chapter 1.4  
 Reference B:  Vendor Guaranteed Concentration 
 Reference C:  PG&E limit for pipeline gas, 1 grain per 100 scf of gas  
 Emission factor in lb/MMBtu derived by either divi ding emission factor in lb/MM cu. ft. by fuel heat value or by using F d 
 
Table 2. Annual and Daily Emissions from Non -CPUC Regulated Natural Gas Combustion in S -93 Boiler  
Pollutant  Emission Factor  Post Project Emissions  BACT trigger  
  lb/MM cu. ft. 
fuel input  lb/MM  Btu          
fuel input  Reference  max lb/hr  max 
lb/day  lb/yr   tons/yr  (lb/day)  Yes/No  
NOx    0.0179  B 0.17 4.01 1464  0.732 10.0 NO 
CO    0.0400  B 0.37 8.96 3269  1.634 10.0 NO 
VOC  5.5 0.0054  A 0.05 1.21 440 0.220 10.0 NO 
PM10  7.6 0.0074  A 0.07 1.67 608 0.304 10.0 NO 
PM2.5  7.6 0.0074  A 0.07 1.67 608 0.304 10.0 NO 
SO2  2.85 0.0030  C 0.03 0.67 245 0.123  10.0 NOEmissions  Annual
Emissions  Reg 2 -5 Acute 
Trigger Level  Reg 2 -5 Chronic 
Trigger Level  HRSA 
Triggered?  
    lb/MMBtu fuel 
input  lb/hr  lb/yr  lb/hr  lb/yr  Yes/No  
ACETALDEHYDE  75-07-0 4.22E -06 3.94E -05 3.45E -01 2.10E -01 2.90E+01  No 
ACROLEIN  107-02-8 2.65E -06 2.47E -05 2.17E -01 1.10E -03 1.40E+01  No 
ARSENIC  7440 -38-2 1.96E -07 1.83E -06 1.60E -02 8.80E -05 1.60E -03 Yes 
BENZENE  71-43-2 7.84E -06 7.32E -05 6.41E -01 1.20E -02 2.90E+00  No 
BERYLLIUM  7440 -41-7 5.88E -09 5.49E -08 4.81E -04 NA 3.40E -02 No 
CADMIUM  7440 -43-9 1.08E -06 1.01E -05 8.83E -02 NA 1.90E -02 Yes 
COPPER  7440 -50-8 8.33E -07 7.78E -06 6.81E -02 4.40E -02 NA No 
ETHYLBENZENE  100-41-4 9.31E -06 8.69E -05 7.61E -01 NA 3.30E+01  No 
FORMALDEHYDE  50-00-0 2.17E -04 2.03E -03 1.77E+01  2.40E -02 1.40E+01  Yes 
n-HEXANE  110-54-3 6.18E -06 5.77E -05 5.05E -01 NA 2.70E+05  No 
LEAD  7439 -92-1 4.90E -07 4.57E -06 4.01E -02 NA 2.90E -01 No 
MANGANESE  7439 -96-5 3.73E -07 3.48E -06 3.05E -02 NA 3.50E+00  No 
MERCURY  7439 -97-6 2.55E -07 2.38E -06 2.09E -02 2.70E -04 2.10E -01 No 
NAPHTHALENE  91-20-3 5.98E -07 5.58E -06 4.89E -02 NA 2.40E+00  No 
NICKEL  7440 -02-0 2.06E -06 1.92E -05 1.68E -01 8.80E -05 3.10E -01 No 
PAH (as benzo(a)pyrene -
equiv.)  1150/1151  
6.60E -09 6.16E -08 5.40E -04 NA 3.30E -03 No 
PROPYLENE  115-07-1 7.17E -04 6.69E -03 5.86E+01  NA 1.20E+05  No 
SELENIUM  7782 -49-2 1.18E -08 1.10E -07 9.65E -04 NA 8.00E+00  No 
TOLUENE  108-88-3 3.59E -05 3.35E -04 2.94E+00  2.20E+00  1.60E+04  No 
VANADIUM  7440 -62-2 2.25E -06 2.10E -05 1.84E -01 1.30E -02 NA No 
XYLENES  1330 -20-7 2.67E -05 2.49E -04 2.18E+00  9.70E+00  2.70E+04  No 
Reference  BAAQMD Toxic Air Contaminant (TAC) Emission Factor Guidelines, Appendix A, Default TAC Emission Factors for 
Specific Source Categories, August 2020  
 
 1 According to Regulation 2- 5-216, this project includes two new sources that were permitted 
within the last five  years of AN 31889. New source S -90 was permitted under AN 29516 and new 
source S -92 was permitted under AN 31551.  
 
Emissions from S -90 and S -92 are summarized in Tables 4 and 5, respectively.  
 
Table 4 -  Emissions from S -90/A -24 Permitted Under AN 29516  
Component  CAS No.  Maximum 
Hourly 
Emissions 
(lb/hr)  Annual 
Emissions 
(lb/yr)  
Divanadium pentaoxide  1314 -62-1 9.55E -04 8.36E+00  
Sulfuric acid  7664 -93-9 9.55E -04 8.36E+00  
Total Crystalline Respirable Silica  7631 -86-9 3.44E -03 3.01E+01  
 
 
Table 5 -  Emissions from S -92 Permitted Under AN 31551  
Application #  Source #  Rated 
Power 
Output 
[Bhp]  Annual  
Non-Emergency 
Operating Time 
[hours/year]  Emission 
Factors  
[g/bhp -hr] Diesel Particulate 
Emissions  
[pounds/year]  
31551  S-92 250 50 0.07 1.93

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

CUMULATIVE INCREASE AND OFFSETS
SETS  
 
Pursuant to Regulation 2- 2-302, offsets must be provided for any new or modified source at a 
facility that emits, or ha s a potential to emit (PTE) , more than 10 tons per year of POC or NO x. 
Furthermore, pursuant to Regulation 2- 2-303 offsets must be provided for any new or modified 
source at a major facility with a cumulative increase that exceeds 1.0 ton per year of PM 10, 
PM 2.5, or SO 2. For purposes of Regulation 2- 2-303, a major facility is defined as a facility that 
has a potential to emit 100 tons /yr or more of PM 10, PM 2.5, or SO 2.  
 
Since the facility has yet to determine the type of natural gas that will be used to operate S -93, 
the maximum emissions will be used for the PTE. Comparing the emissions from Table 1 and 
Table 2, the maximum emissions  occur from the use of gas meeting the PG&E  sulfur limit.  
PTE emissions per source are shown in Appendix A of this report.  
 
The cumulative increase and offset determination for the facility is as follows: 
 
 1  
Table 6. Cumulative Increase  
 Pollutant  Permitted 
Emissions  
(since Reg 2 -2-
209 Baseline 
Date)   Offsets 
Previously 
Provided, 
including 
from SFB 
(Reg 2 -2-
608.2.2) TPY  Adjusted 
Actual 
Baseline (Reg 
2-2-603) Post Project 
PTE  
(TPY)) Project 
Cumulative 
Emissions 
Increa se (Reg. 
2-2-607) TotalCumulative 
Increase
(TPY)  (TPY)  (TPY)  (TPY)  (TPY)  (TPY)  
NOx  0.081  0.000  0.000  0.745  0.745  0.826  
CO  0.019  0.000  0.000  1.662  1.662  1.681  
VOC  0.003  0.000  0.000  0.220  0.220  0.223  
PM10  1.193  0.000  0.000  0.305  0.305  1.498  
PM2.5  0.002  0.000  0.000  0.305  0.305  0.307  
SO2  0.000  0.000  0.000  0.123  0.123  0.123  
 
Table 7. Offsets Determination  
Pollutant  Facility -Wide 
Post Project PTE  
(TPY)  Emissions Increase 
with Application (TPY)  Prior Cumulative 
Increase  (TPY ) Total Facility 
Unoffset Cumulative 
Increase  Offset Thresholds (TPY)  Offsets Required?  
NOx  2.354  0.745  0.081  0.826  Post-project Facility -wide 
PTE > 10  No 
CO 13.725  1.662  0.019  1.681  N/A N/A 
VOC  0.642  0.220  0.003  0.223  Post-project Facility -wide 
PTE > 10  No 
PM10  2.240  0.305  1.193  1.498  > 1.0 CI and ≥100 tpy post -
project facility -wide PTE  No 
PM2.5  0.514  0.305  0.002  0.307  > 1.0 CI and ≥ 100 tpy post -
project facility -wide PTE  No 
SO2 2.198 0.123  0.000  0.123  > 1.0 CI and ≥100 tpy post-
project facility -wide PTE  No 
 
 1 NEW SOURCE PERFORMANCE STANDARDS  
 
The following New Source Performance Standards (NSPS) may apply to S -93. 
 
40 CFR Part 60 Subpart D  
Pursuant to §60.40, an affected facility is each fossil fuel -fired steam generating unit of more than 250 
MMB TU/hr. S -93 is  a steam generating unit. However, the input heat rating of S -93 is not greater than 
250 MMB TU/hr. Therefore, S -93 is  not subject to the requirements of this subpart. 
 
40 CFR Part 60 Subpar t Da 
Pursuant to §60.40Da , an affected facility is each electric utility steam generating unit that is capable of 
more than 250 MMBTU/hr, which was constructed after September 18, 1978. Since  
S-93 does not provide steam for the generation of electricity of a utility power distribution system for 
sale, S -93 is not considered electric utility steam generating unit. Furthermore, the input heat rating of S -
93 is less than 250 MMBTU/hr. Therefore, S -93 is not subject to the requirements of this subpart. 
 
40 CFR Part 60 Subpart D b 
Pursuant to §60.40b(a) , an affe cted facility is each steam generating unit that commences construction 
after June 19, 1984 and has a heat input capacity of 100 MMBTU/hr. S -93 is less than 100 MMBTU/hr. 
Therefore, S -93 is not subject to the requirements of this subpart. 
 
40 CFR Part 60 S ubpart D c 
Pursuant to §60.40c(a) , an affected facility is each steam generating unit that commences construction 
after June 9, 1989 and has a heat input capacity in between 10 MMBTU/hr to 100 MMBtu/hr. S -93 is a 
steam generating unit, constructed after June 9, 1989, with a heat input capacity of less than 10 
MMBtu/hr. Therefore, S -93 is  not subject to this subpart.

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

2 Emission factors for PM, SOx, VOC, and toxics are based on the  EPA’s AP -42, 5th Edition,
, 
Chapter 1.4. For the non -CPUC  regulated gas , the sulfur content will be set at the PG&E 
limit of 1 grain of sulfur per 100 cubic feet of gas. The facility will be required to conduct 
startup testing and routinely test the non -CPUC regulated gas to verify that sulfur content  is 
meeting this expected rate prior to PO issuance.  
 
This project is located within an Overburdened Community (OBC) as defined in Regulation 
2-1-243. Therefore, it will be subject to a c ancer risk limit of 6.0 in a million and must satisfy 
the public noticing requirements of the Rule.1 TOXIC RISK SCREENING ANALYSIS
SIS  
 
The t oxic air contaminant (TAC) emission factors were obtained from  BAAQMD Permit Handbook Chapter 2.1, which  are in turn 
obtained from  AP-42 Chapter 1.4, Table 1.4- 3. An annual usage of 8,760 hours per year was used to determine the annual TAC 
emissions.  
Table 3. TAC Emissions from S -93 
TAC  CAS #  Default 
Emission Factor  Max HourlyRegulation 2, Rule 5 (New Source Review of Toxic Air Contaminants)
A health risk assessment (HRA), dated March 17, 2023, indicated that the project cancer risk is 
estimated at 0.19 in a million, the project chronic hazard index is estimated at 0.029, and the project 
acute hazard index is estimated at 0.014.  
 
 3  
In accordance with the District’s Regulation 2 -5-301, the proposed new source (S -93) does not require 
TBACT because the individual source risk does not exceed a cancer risk of 1.0 in a million and/or a 
chronic HI of 0.20. Since the estimated project cancer risk does not exceed 6.0 in a million and hazard 
indices do not exc eed 1.0, this project complies with the District’s Regulation 2 -5-301 project risk 
requirements, for projects located within an Overburden Community, as defined in Regulation 2- 1-243.  
 
Regulation 6, Rule 1 (Particulate Matter – General Requirements)  
 
Pursuant to Regulations 6- 1-301 and 6- 1-302, a person shall not emit from any source for a period or 
periods aggregating more than three minutes in any hour, a visible emission which is as dark or darker 
than No. 1 on the Ringelmann Chart, or of such opacity a s to obscure an observer’s view to an 
equivalent or greater degree and/or an emission equal to or greater than 20% opacity as perceived by an 
opacity sensing device, where such a device is required by District regulations. The project is expected 
to meet the requirements of Regulations 6- 1-301 and 6- 1-302. 
 
As per Regulation 6- 1-305, fall out of visible particles on adjacent properties, in sufficient numbers so as 
to cause annoyance to any other person, is prohibited. The boiler is  expected to meet this regulation as 
the particulate emissions from the boiler  are fairly low.  
 
In accordance with Regulation 6 -1-310, the applicable grain loading limits for a source depend on the  
source’s  potential to emit ( PTE)  for total suspended particulate ( TSP). For this source type , the AP -42 
emission factor of 7.6 lbs/MM scf for total filterable and condensable PM represent s TSP, and the PM is 
estimated to all be emitted as less than PM2.5. The PTE for S -93 is 609 lbs/yr (276 kg/yr) of TSP. Since 
the PTE for S -93 does not exceed 1000 kg, S -93 is subject to the Regulation 6- 1-310.1 grain loading 
limit of 0.15 grains/dscf and is not subject to the more stringent limits  in Regulation 6- 1-310.2. S -93 
satisf ies the total suspended particulate (TSP) requirements of Table 6 -1-310.1, because  S-93 will emit a 
maximum of 0.002 grains per dscf of exhaust gas.  
 
Regulation 9, Rule 1 (Sulfur Dioxide)  
S-93 is  subject to the SO 2 limitations of Regulation 9 -1-301 (Limitations on Ground Level 
Concentrations of Sulfur Dioxide), Regulation 9- 1-302 (Limit ations Sulfur Dioxide Emissions) and 9- 1-
304 (Burning of Solid and Liquid Sulfur Dioxide Fuel).  
 
Pursuant to Regulation 9- 1-301, the ground level concentrations of SO 2 shall not exceed 0.5 ppm 
continuously for 3 consecutive minutes or 0.25 ppm averaged ove r 60 consecutive minutes, or 0.05 ppm 
averaged over 24 hours. Pursuant to Regulation 9- 1-302, a person shall not emit from any source, a gas 
stream containing SO 2 in excess of 300 ppm (dry). Compliance with Regulation 9- 1 is expected as SO 2 
emission from n atural gas contains very little sulfur. The likely SO 2 concentration in the exhaust gas 
from a boiler less than 10 lb/ MM BTU  in size fueled on gas meeting the 1 gr ain/100 scf sulfur limit is 
less than 3 parts per million (ppm).  
 
Regulation 9, Rule 7 (NO x and CO Emissions from Industrial, Institutional, and Commercial, 
Boilers, Steam Generators and Process Heaters)  
 
Pursuant to Regulation 9- 7-307, S -93 is  required to meet the emission limitations for NO x (15 ppmv at 
3% O 2) and CO (400 ppmv at 3% O 2). As per the manufacturer’s guaranteed emission rates, S -93 will 
 
 4 emit 15 ppmv of NO x and 55 ppmv of CO, both at 3% O 2. Thus, S -93 meets the requirements of this 
regulation. 
 
S-93 will be subject to the heat -input weighted average limit of Regulation 9 -7-307.9. S -93 will meet the 
NO x and CO volumetric concentration limits of Regulation 9- 7-307. 
 
In addition, pursuant to Regulation 9- 7-312, no person shall operate a boiler or steam generator with a 
stack temperature that exceeds 100ºF over hot water temperature for hot water boiler or 250ºF greater 
than combustion air temperature, which ever is greater for a firetube boiler such as S -93. The 
manufacturer specifications list the saturated steam temperature as 397  ºF and the combustion air 
temperature is listed as  160 ºF, therefore the stack gas temperature will be limited to 497  ºF (100 ºF plus 
397 ºF). The manufacturer specifications list the exhaust temperature as 437  ºF which meets this 
requirement.  
 
Moreover, pursuant to Regulation 9- 7-403, an initial demonst ration of compliance is required. The 
initial demonstration specifies that source tests be performed to determine compliance with the 
limitations of Regulation 9 -7-307, unless the devices have an input heat rating less than 10 MMBTU/hr; 
at which point a portable analyzer may be used  after the initial compliance demonstration test. S -93 has 
an input heat rating less than 10 MMBTU/hr. Therefore, testing with a portable analyzer may be used 
after the initial start- up test .  
 
Lastly, Regulation 9- 7-503 requires  the following records to be kept for at least 24 months from the date 
of entry, which are to be  made available to District staff upon request.  
 
• Documentation verifying the hours of equipment testing using non- gaseous fuel, and of total 
operating hours using non- gaseous fuel during each calendar month;  
• Results of any testing required by Regulation 9- 7-506; and, 
• Total operating hours.

## BACT
JSONPath: `$.BACT.text`

(empty)

## offsets
JSONPath: `$.offsets.narrative`

(empty)

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

(empty)

## CEQA
JSONPath: `$.CEQA.narrative`

(empty)

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
STATEMENT OF COMPLIANCE
CE  
 
Regulation 2, Rule 1 (General Requirements)

## public_notification
JSONPath: `$.public_notification.text`

California Health & Safety Code §42301.6 and Regulation 2- 1-412: Pursuant to California Health &
Safety Code §42301.6(a), prior to approving an application for a permit to construct or modification of a 
 
 2 source, which is located within 1,000 feet from the outer boundary of a school site, the District shall 
prepare a publ ic notice as detailed in §42301.6. §42301.9(a) defines a “school” as any public or private 
school used for the purposes of the education of more than 12 children in kindergarten or any grades 1 to 
12, inclusive, but does not include any private school in w hich education is primarily conducted in 
private homes. The facility is located more than 1,000 feet away from a school. Therefore, the 
requirements of the California Health & Safety Code §42301.6(a) do not apply. 
 
Regulation 2- 1-412 also requires public noticing and consideration of comments for an application if it 
includes a new or modified source located within an Overburdened Community as defined in Section 2-
1-243 and for which a Health Risk Assessment is required pursuant to Section 2- 5-401. This application 
meets these criteria. Therefore, S -93 is subject to the public notification requirements of Regulation 2- 1-
412 before the Air District issues an Authority to Construct or Permit to Operate . 
 
Regulation 2- 1-312: California Environmental Quality Act (CEQA) : This permit application is exempt 
from CEQA review, because it meets the CEQA exemption outlined in Regulation 2- 1-312.7 since it is a 
replacement of an existing source (S -91) where the new source will  be located on the same site as the 
source replaced and will have substantially the same purpose and capacity as the source replaced.  
 
In addition, this permit application also meets the CEQA exemption outlined in Regulation 2 -1-312.11.4 
since it satisfie s the “no net emissions increase” provisions of the District Regulation 2- 2 for which there 
will be some increase in the emissions of toxic air contaminants but for which the cancer risk is below 
1.0 in a million and the chronic hazard index is below 0.20.  
 
 
Regulation 2, Rule 2 (New Source Review)   
 
Regulation 2- 2-301: BACT : Pursuant to Regulation 2- 2-301, BACT is required for any new or modified 
source with a regulated air pollutant PTE equal to or greater than 10.0 lb per highest day. BACT was not 
trigg ered in this application as shown in Tables 1 and 2. 
 
Regulation 2- 2-302 and 303: Offsets : This project will not result in any emission increases for ozone 
precursor pollutants: NO x or POC  that will cause the facility emissions to exceed the 10 tpy trigger  level . 
Therefore, Regulation 2- 2-302 does not apply to this project, and offsets for ozone precursor pollutants  
are not required.  
 
Regulation 2- 2-303 requires  PM 2.5, PM 10, and SO 2 offsets for sites that are major sources of these 
pollutants. Since site -wide emissions will not exceed 100 tons/year of PM 2.5, PM 10, or 100 tons/year of 
SO 2, this site is not a major facility for either of these pollutants. Therefore, the PM 10 offset 
requirements do not apply to this facility.  
 
Regulation 2- 2-304-309: PSD : Since the maximum permitted site -wide emissions are less than 100 
tons/year for each pollutant, PSD  does not apply to this site.

## conditions
JSONPath: `$.conditions.text`

Permit Conditions
ions  
 
Permit Condition # 27891

## permit_conditions
JSONPath: `$.permit_conditions`

- Item
Permit Conditions
ions  
 
Permit Condition # 27891

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

Recommendation
on  
The District reviewed the material contained in the permit application for the proposed project and has 
made a preliminary determination that the project is expected to comply with all applicable requirements 
of District, state, and federal air quality -related regulat ions.  The preliminary recommendation is to issue 
an Authority to Construct for the equipment listed below. However, the proposed source (s) will be 
located within an Overburdened Community and requires an HRA  which triggers the public notification 
requirem ents of Regulation 2- 1-412. After the comments are received  from the public  and reviewed, the 
District will make a final determination on the permit.  
I recommend that the District initiate a public notice and consider any comments received prior to taking 
any final action on issuance of an Authority to Construct and/or a Permit to Operate for the following 
equipment:  
 
S-93 Steam Boiler 
Make: Victory  Engine Model: F2 -DB-574L -300X -S275 
Maximum Firing Rate:  9.33 MMBtu/hr  
Permit Condition No s. 27891 
 
 
 
Prepared by:  Simrun Dhoot, Supervising Air Quality Engineer  
 
  
 
 7 Appendix A  – Facility PTE  
 
 
 S# Description Nox (lb/yr) CO (lb/yr) VOC (lb/yr) PM10 (lb/yr PM2.5 (lb/yr) SO2 (lb/yr)
24DRYER 1-406 26615 3854 25012
25DRY PELLET HOPPER 1-321 3854 25012
26CALCINER FEEDER  1-339 3854 25012
27OFF SIZE HOPPER  1-323 3854 25012
30PACKAGING STATION NO. 2 1-128 16337 8825 5958 3854 26301
33OFF SIZE BIN 2-219A 8825 5958 3854 26301
34CALCINED FINES BIN 2-219B 8825 5958 3854 26301
35FINISHED PRODUCT HOPPER  1-126 5958 3854 26301
47POTASSIUM SILICATE BATCH DISSOLVER 1-170 26622 1095
48Sulfuric Acid Catalyst Repackaging Station 2-222 26712 26301
5498% Sulfuric Acid Storage Tank                                 [exempt] 28182 0 0 0 0 0 0
55Calciner 1-207;On AC, PO Pending;3,500 lb of catalyst/ hr 30644 20917 22831 28350 28479 28056 2782.15 24013.59 819.58 400.04 400.04 4142.57
61Liquified Sulfur Dioxide Storage                               [exempt] 10177 0.26
62Diesel Generator, Emergency Use Only 10177 88.35 19.04 7.17 6.27 6.27 5.84
63Storage Tank, 25% NaOH                                         [exempt] 10177 0 0 0 0 0 0
64Portable Conveyor 1-241 16337 3854 26301
65Flexible Wall Conveyor, 1-243 16337 3854 26301
66Bulk Packaging Screener 1-244 16337 3854 26301
67Bulk Bag Packaging Station 1-246 16337 3854 26301
68Pellet Screener 1-215 19544 3854 25012
69Finished Product Screener 1-217 19544 3854 26301
70White Pellet Elevator, 1-141 3854 25012
71White Pellet Feeder 1-142 3854 25012
72FP Elevator 1-125 3854 26301
73FP Elevator Feeder 1-121 3854 26301
75DE storage Silo (#4001) 19100 25010
76DE Storage Silo (#4002) 19100 25010
77DE Storage Silo(#4003) 19100 25010
78DE Storage Silo (#4004) 19100 25010
79DE Storage Silo (#4005) 19100 25010
80DE Storage Silo (#4006) 19100 25010
81De Feed Tank 19100 25010
82Batch Mixer Vessel 24303 32.85
83V2O5 Transfer System and Hopper 25011 22.13
84Recycle Conveyor, Horizontal Screw Conveyor/Hopper 26367 0.0039
85Mobile Repack Station 26301 1126
87Calciner Dumpster 28182 2.53 0.4
88Emergency Standby Diesel Engine - Generator Set 28403 280.5 79.8 14.76 7.98 7.98 0.27
90Finish Product Elevator Feeder 29516 8.44 1.28
92Emergency Diesel Fire Pump Engine 31551 68.07 12.4 2.2 1.93 1.93 0.15
1.610 12.062 0.422 1.936 0.209 2.07514.281154Application Number
Total (tpy)
