---
application_number: 20977
plant_id: 14628
plant_name: Tesoro Refining and Marketing Company
evaluation_date: November 5, 2009
source_pdf: C:\Users\aaw\Codex\BAAD Engr Evals\split_evals_2011_04\application_20977.pdf
source_json: JSON/baad_eval_to_json_bulk_2026-03-05/application_20977__eval-1.json
---

# Engineering Evaluation (Application 20977)
**Plant**: 14628 Tesoro Refining and Marketing Company
**Evaluation Date**: November 5, 2009

## background
JSONPath: `$.background.text`

BACKGROUND
The Tesoro Refining a nd Marketing Company (Tesoro) is applying for an Authority to Construct 
and/or Permit to Operate the following equipment:  
 
 S-1550  Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated byBACKGROUND
ND  
 
The Tesoro Refining a nd Marketing Company (Tesoro) is applying for an Authority to Construct 
and/or Permit to Operate the following equipment:  
 
 S-1550  Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by 
A-1550 SCR  
 S-1551  Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by 
A-1551 SCR  
 
These Backup Boilers are needed to ensure adequate steam supply for the refinery when existing 
boilers S -901 and S -904 are removed from service for turnaround/maintenance.  A boiler 
maintenance program is required a t Tesoro and previous applications (#7642 in 2003 and 
#15773 in 2007) have permitted similar backup boilers.  These previous applications have 
permitted the boilers, and then when the need was completed, the permits were surrendered.   
These previous applic ations were for Temporary Operations under Regulation 2 -1-302.3.   
 
This application is for a permanent permit to operate.  The permit will be structured to allow up 
to three months (90 days = 2160 hours) of operation over a 6 -month period each year.  The 
permit will also allow for up to 384 hours (192 hrs/boiler) of operation without SCR 
abatement to allow for startup and shutdown (48 hours per SU/SD event, 4 events per 
boiler, 2 boilers).  
 
BACT and Offsets will apply to this application.  In the previous  applications for Temporary 
Operations BACT and Offsets were addressed differently.  2007 Application 15773 for S -
1530 and S -1531 BACT did not apply and contemporary emissions reductions were 
allowed from the boilers being maintained, resulting in no offse ts required.  For 2003 
Application 7642, BACT applied and Application 14405 was an emission credit banking 
application for back -up boilers S1494 and S -1495 when they were removed from service.  
This application was never completed.  Tesoro requested that A pplication 14405 be 
cancelled and that the emission credits be applied to this application.  To avoid the 
Regulation 2 -2-605 calculation and verification requirement for Contemporary Emissions 
Reductions, offsets will apply to the total S -1550 and S -1551 b ackup boiler emissions.

## emission_calculations
JSONPath: `$.emission_calculations.text`

EMISSION CALCULATIONS
NS  
 
Emission Factors  
 
The following emissions factors are used to calculate emissions from Backup Boilers S -1550 an S -1551.  
 
NOx:   7 ppm @ 3% O2 when abated by SCR (BACT)  
 30 ppm @ 3% O2 without SCR operation (1 92 hrs/yr per boiler)  
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 652 of 1354  
    
 652 CO: 50 ppm @ 3% O2 (BACT)  
PM10  7.45E -3 lb/MMBtu  
VOC  5.39E -3 lb/MMBtu (assume to be all POC)  
SO2 5.88E -4 lb/MMBtu  
Emission factors for PM10, POC, and SO2 are from Chapter 1, Table 1.4 -2 of the EPA Document AP -42, 
Compilation of Air Pol lutant Emission Factors (lb/106scf / 1020).  
 
Exhaust flow:  (8710 dscf/MMBtu)*(20.95/(20.95 -3))=10165.7 dscf/MMBtu at 3% O2  
 
At atmospheric pressure and low temperatures, the ideal gas law will provide the necessary calculation accuracy:  
n = PV/RT = (1atm* 10165.7 dscf/MMBtu) /((0.7302 atm -cf/lb-mol R)*(68 + 460 R))  
= 26.367 lb -mol/MMBtu  
 
NOx w/ SCR:  26.367 lb -mol/MMBtu(7 lb -mol NOx/1E6 lb -mol)(46 lb NOx/lb -mol NOx)  
= 0.00849 lb/MMBtu  
NOx w/o SCR:  26.367 lb -mol/MMBtu(30 lb -mol NOx/1E6 lb -mol)(46 lb NOx/lb -mol NOx)  
= 0.0364 lb/MMBtu  
CO:  26.367 lb -mol/MMBtu(50 lb -mol NOx/1E6 lb -mol)(28 lb CO/lb -mol CO)  
= 0.0369 lb/MMBtu  
 
Annual Emissions:  
 
Emissions from S -1550 Backup Boiler:  
NOx (SCR)    =(99 MMBtu/hr)(0.00849 lb NOx/MMBtu)(2160 -192 hrs) = 1654 lb = 
0.827 t ons 
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(192 hrs) = 692 lb = 0.346 tons  
NOx (total)   = 1654 + 692 = 2346 lbs = 1.173 tons  
CO    =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(2160 hrs) = 7891 lb = 3.945 tons  
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MMBtu)(2 160 hrs) = 1593 lb = 0.797 tons  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(2160 hrs) = 1153 lb = 0.576 tons  
SO2    =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(2160 hrs) = 126 lb = 0.063 tons  
 
Emissions from  S -1551 Backup Boiler:  
NOx (SCR)    =(99 MMBtu/hr)(0.0084 9 lb NOx/MMBtu)(2160 -192 hrs) = 1654 lb = 
0.827 tons  
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(192 hrs) = 692 lb = 0.346 tons  
NOx (total)   = 1654 + 692 = 2346 lbs = 1.173 tons  
CO    =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(2160 hrs) = 7891 lb = 3.945 to ns 
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MMBtu)(2160 hrs) = 1593 lb = 0.797 tons  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(2160 hrs) = 1153 lb = 0.576 tons  
SO2    =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(2160 hrs) = 126 lb = 0.063 tons  
 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 653 of 1354  
    
 653  
Cumulative Increase:  
NOx = 1564 lb + 1564 lb + 692 lb + 692 lb = 4512 lb = 2.256 tons  
CO = 7891 lb + 7891 lb = 15782 lb = 7.891 tons  
PM10 = 1593 lb + 1593 lb = 3186 lb = 1.593 tons  
POC = 1153 lb + 1153 lb = 2306 lb = 1.153 tons  
SO2 = 126 lb + 126 lb = 252 lb = 0.126 tons  
 
 
Max imum Daily Emissions:  
 
NOx (SCR)    =(99 MMBtu/hr)(0.00849 lb NOx/MMBtu)(24 hrs) = 20.1 lb  
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(24 hrs) = 86 lb  
CO    =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(24 hrs) = 88 lb  
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MM Btu)(24 hrs) = 17.7 lb  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(24 hrs) = 12.8 lb  
SO2    =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(24 hrs) = 1.4 lb  
 
 
 
Toxic Risk Screening  
 
 
The following toxic emissions were calculated for each boiler.  
 
 
TAC  Emission Fact or 
(lb/mmscf)  Emission Factor 
(lb/MMBtu
) Emissions 
(lb/hr)  Emissions 
(lb/yr)  
Benzene  2.10E -03 2.1E-06 2.1E-04 4.5E-01 
Dichlorobenzene  6.00E -07 6.0E-10 5.9E-08 1.3E-04 
Formaldehyde  7.50E -02 7.5E-05 7.4E-03 1.6E+01  
Hexane  1.80E00  1.8E-03 1.8E-01 3.8E+02  
Naphthalene  6.10E -04 6.10E -07 6.0E-05 1.3E-01 
Toluene  3.40E -03 3.4E-06 3.4E-04 7.3E-01EMISSION CALCULATIONS
NS  
 
Emission Factors  
 
The following emissions factors are used to calculate emissions from Backup Boilers S -1550 an S -1551.  
 
NOx:   7 ppm @ 3% O2 when abated by SCR (BACT)  
 30 ppm @ 3% O2 without SCR operation (1 92 hrs/yr per boiler)  
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 652 of 1354  
    
 652 CO: 50 ppm @ 3% O2 (BACT)  
PM10  7.45E -3 lb/MMBtu  
VOC  5.39E -3 lb/MMBtu (assume to be all POC)  
SO2 5.88E -4 lb/MMBtu  
Emission factors for PM10, POC, and SO2 are from Chapter 1, Table 1.4 -2 of the EPA Document AP -42, 
Compilation of Air Pol lutant Emission Factors (lb/106scf / 1020).  
 
Exhaust flow:  (8710 dscf/MMBtu)*(20.95/(20.95 -3))=10165.7 dscf/MMBtu at 3% O2  
 
At atmospheric pressure and low temperatures, the ideal gas law will provide the necessary calculation accuracy:  
n = PV/RT = (1atm* 10165.7 dscf/MMBtu) /((0.7302 atm -cf/lb-mol R)*(68 + 460 R))  
= 26.367 lb -mol/MMBtu  
 
NOx w/ SCR:  26.367 lb -mol/MMBtu(7 lb -mol NOx/1E6 lb -mol)(46 lb NOx/lb -mol NOx)  
= 0.00849 lb/MMBtu  
NOx w/o SCR:  26.367 lb -mol/MMBtu(30 lb -mol NOx/1E6 lb -mol)(46 lb NOx/lb -mol NOx)  
= 0.0364 lb/MMBtu  
CO:  26.367 lb -mol/MMBtu(50 lb -mol NOx/1E6 lb -mol)(28 lb CO/lb -mol CO)  
= 0.0369 lb/MMBtu  
 
Annual Emissions:  
 
Emissions from S -1550 Backup Boiler:  
NOx (SCR)    =(99 MMBtu/hr)(0.00849 lb NOx/MMBtu)(2160 -192 hrs) = 1654 lb = 
0.827 t ons 
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(192 hrs) = 692 lb = 0.346 tons  
NOx (total)   = 1654 + 692 = 2346 lbs = 1.173 tons  
CO    =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(2160 hrs) = 7891 lb = 3.945 tons  
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MMBtu)(2 160 hrs) = 1593 lb = 0.797 tons  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(2160 hrs) = 1153 lb = 0.576 tons  
SO2    =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(2160 hrs) = 126 lb = 0.063 tons  
 
Emissions from  S -1551 Backup Boiler:  
NOx (SCR)    =(99 MMBtu/hr)(0.0084 9 lb NOx/MMBtu)(2160 -192 hrs) = 1654 lb = 
0.827 tons  
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(192 hrs) = 692 lb = 0.346 tons  
NOx (total)   = 1654 + 692 = 2346 lbs = 1.173 tons  
CO    =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(2160 hrs) = 7891 lb = 3.945 to ns 
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MMBtu)(2160 hrs) = 1593 lb = 0.797 tons  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(2160 hrs) = 1153 lb = 0.576 tons  
SO2    =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(2160 hrs) = 126 lb = 0.063 tons  
 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 653 of 1354  
    
 653  
Cumulative Increase:  
NOx = 1564 lb + 1564 lb + 692 lb + 692 lb = 4512 lb = 2.256 tons  
CO = 7891 lb + 7891 lb = 15782 lb = 7.891 tons  
PM10 = 1593 lb + 1593 lb = 3186 lb = 1.593 tons  
POC = 1153 lb + 1153 lb = 2306 lb = 1.153 tons  
SO2 = 126 lb + 126 lb = 252 lb = 0.126 tons  
 
 
Max imum Daily Emissions:  
 
NOx (SCR)    =(99 MMBtu/hr)(0.00849 lb NOx/MMBtu)(24 hrs) = 20.1 lb  
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(24 hrs) = 86 lb  
CO    =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(24 hrs) = 88 lb  
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MM Btu)(24 hrs) = 17.7 lb  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(24 hrs) = 12.8 lb  
SO2    =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(24 hrs) = 1.4 lb

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

(empty)

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

Toxic Risk Screening
eening  
 
 
The following toxic emissions were calculated for each boiler.  
 
 
TAC  Emission Fact or 
(lb/mmscf)  Emission Factor 
(lb/MMBtu
) Emissions 
(lb/hr)  Emissions 
(lb/yr)  
Benzene  2.10E -03 2.1E-06 2.1E-04 4.5E-01 
Dichlorobenzene  6.00E -07 6.0E-10 5.9E-08 1.3E-04 
Formaldehyde  7.50E -02 7.5E-05 7.4E-03 1.6E+01  
Hexane  1.80E00  1.8E-03 1.8E-01 3.8E+02  
Naphthalene  6.10E -04 6.10E -07 6.0E-05 1.3E-01 
Toluene  3.40E -03 3.4E-06 3.4E-04 7.3E-01 
PAH  2.45E -05 2.45E -08 7.0E -06 
 1.5E -02 
 
 
A risk screen is required for this application due to PAH emissions.  The risk screen was 
conducted and the results transm itted October 26, 2009.  The project risk is considered 
acceptable with a Maximum Cancer Risk of 0.004 in a million, the chronic hazard index of 
0.00008 and the acute hazard index of 0.003.

## BACT
JSONPath: `$.BACT.text`

BEST AVAILABLE CONTROL TECHNOLOGY
GY   
 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 654 of 1354  
    
 654 In accordance with Regulatio n 2, Rule 2, Section 301, BACT is triggered for any new or 
modified source with the potential to emit 10 pounds or more per highest day of POC, 
NPOC, NOx, CO, SO 2 or PM 10.  Emissions from both S -1550 and S -1551 trigger BACT 
for the following pollutants:  N Ox, CO, PM10, and POC.  There are two pages in the 
BACT Guideline that are pertinent to this application.  Documents 16.1 and 17.3.1 are 
shown below.  The 1994 version of Document 17.1.3 was applied to the 2003 permits for 
S-1494 and S -1495.  Document 16.1  was applied to the 2007 permits for S -1530 and S -
1531.BEST AVAILABLE CONTROL TECHNOLOGY
GY   
 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 654 of 1354  
    
 654 In accordance with Regulatio n 2, Rule 2, Section 301, BACT is triggered for any new or 
modified source with the potential to emit 10 pounds or more per highest day of POC, 
NPOC, NOx, CO, SO 2 or PM 10.  Emissions from both S -1550 and S -1551 trigger BACT 
for the following pollutants:  N Ox, CO, PM10, and POC.  There are two pages in the 
BACT Guideline that are pertinent to this application.  Documents 16.1 and 17.3.1 are 
shown below.  The 1994 version of Document 17.1.3 was applied to the 2003 permits for 
S-1494 and S -1495.  Document 16.1  was applied to the 2007 permits for S -1530 and S -
1531.  
 
 
BAY AREA AIR QUALITY MANAGEMENT DISTRICT  
Best Available Control Technology (BACT) Guideline  
Source Category  
Source:  Boiler, Rental  Revision:  1 
Document 
#: 16.1 
Class: On-site < 6 consecutive mo nths from the date of initial 
operation  Date: 1/26/9
9 
Determination  
POLLUTANT  BACT  
1. Technologically Feasible/ Cost 
Effective  
2. Achieved in Practice  TYPICAL TECHNOLOGY  
POC 1. n/d 
2. n/s 1. n/d 
2. Good Combustion Practicea 
NOx 1. n/d 
2. 25 ppmv @ 3% O 2 Dry, a,b,c 1. n/d  
2. Low NO x Burners + Flue Gas 
Recirculationa 
SO 2 1. Natural Gas, or Treated Refinery 
Gas Fuel w/ < 50 ppmv Hydrogen 
Sulfide and <100 ppmv Total 
Reduced Sulfur a,b 
2. Natural Gas, or Treated Refinery 
Gas Fuel w/ <100 ppmv Total 
Reduced S ulfur a,b 1. Fuel Selection a,b 
 
 
2. Fuel Selection a,b 
CO 1. n/d 
2. 100 ppmv @ 3% O 2 Dry a,b,d 1. n/d 
2. Good Combustion Practice a,b,d 
PM 10 1. n/d 
2. Natural Gas or Treated Refinery 
Gas Fuel a,b 1.  n/d 
2.  Fuel Selection a,b 
NPOC  1. n/a 
2. n/a 1. n/a 
2. n/a 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 655 of 1354  
    
 655 References  
a. BAAQMD staff report  
b. BACT is 25 ppmvd NO x @ 3% O 2 and 100 ppmvd CO @ 3 % O 2 regardless of fuel.   
However, emergency backup fuel oil w/ < 0.05 wt. % sulfur may be permitted to emit up to 
60 NO x ppmvd @ 3% O 2 and 100 ppmvd CO @ 3 % O 2 during natural gas curtailment.  
c. NO x  determination by BAAQMD Source Test method ST -13A (average of three 30 -minute 
sampling runs), or BAAQMD approved equivalent.  
d. CO determination by BAAQMD Source Test Method ST -6 (average of three 30 minute 
samplin g runs), or BAAQMD approved equivalent.  
 
  
BAY AREA AIR QUALITY MANAGEMENT DISTRICT  
Best Available Control Technology (BACT) Guideline  
Source Category  
Source:  Boiler  Revision:  4 
Document #:  17.3.1  
Class:  > 50 MM BTU/hour Heat Input  Date: 9/22/05  
Determination  
POLLUTANT  BACT  
1. Technologically Feasible/ Cost 
Effective  
2. Achieved in Practice  TYPICAL TECHNOLOGY  
POC 1. n/d 
2. n/s 1. n/d f 
2. Good Combustion Practice (GCP) a 
NOx 1.  7 ppmv @ 3% O 2, Dry b, c, d 
2. 9 ppmv @ 3% O 2, Dry a, c, d 1. Selecti ve Catalytic Reduction (SCR) 
+ Low NO x Burners (LNB) + Flue 
Gas Recirculation (FGR) b, c, d 
2. Ultra Low NO x Burners (ULNB) + 
FGR a, c, d  
SO 2 1. Natural Gas or Treated Refinery 
Gas Fuel w/ <50 ppmv Hydrogen 
Sulfide and <100 ppmv Total 
Reduced Sulfur a, c 
2. Natural Gas or Treated Refinery 
Gas Fuel w/ <100 ppmv Total 
Reduced Sulfur a, c 1. Fuel Selection a, c 
 
 
2. Fuel Selection a, c 
CO 1. 10 ppmv @ 3% O 2 Dry f 
2. 50 ppmv @ 3% O 2 Dry a, c, e 1. Oxidation Catalyst f 
2. Good Combustion Practice in Con -
junct ion with SCR System or Ultra 
Low NO x Burners and FGR a, c, e 
PM 10 1. n/d 
2. Natural Gas or Treated Refinery 
Gas Fuel a, c 1. n/d 
2. Fuel Selection a, c 
NPOC  1. n/a 1. n/a 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 656 of 1354  
    
 656 2. n/a 2. n/a 
References  
a. BAAQMD  
b. SCAQMD. Cost effectiveness evaluations shall  be based on emissions from firing 
primary fuels but not emergency backup fuels.  
c. BACT limits above apply  to all fuels except for emergency backup fuel oil used during 
natural gas curtailment.  For emergency backup fuel oil, BACT(1) for NO x and CO 
(achie ved using LNB+ FGR+ SCR and GCP) is 25 ppmvd NO x @ 3% O 2; 100 ppmvd 
CO @ 3% O 2, and 5 ppmvd NH 3 @ 3% O 2; BACT(2) for NO x and CO (achieved using 
ULNB+ FGR and GCP) is 40 ppmvd NO x @ 3% O 2 and 100 ppmvd CO @ 3% O 2; 
BACT(2) for SO 2 and PM 10 is the use of low sulfur fuel with < 0.05 wt. % S; and 
BACT(2) for POC is GCP.  
d. NO x determination by Continuous Emission Monitor (3 -hour average), or BAAQMD 
approved equivalent.  
e. CO determination by Continuous Emission Monitor (3 -hour average), or BAAQMD 
approved equiva lent. 
f. The BACT(1) CO limit does not apply to boilers smaller than 250 MM BTU/hour unless 
an oxidation catalyst is found to be cost effective or is necessary for TBACT or POC 
Control.  
  
 
The ‗Rental Boiler‘ guideline does not apply because this applicat ion is for a permanent permit, 
not one for a boiler that will be out of service within 6 months.  Each 
turnaround/maintenance events would be less that 6 months, so if one were to argue that for 
each maintenance event that requires these backup boilers, th e boilers would be on site less 
than 6 months after the initial operation, it should be noted that this document 16.1 
guideline is over 10 years old and a current BACT determination is necessary.   
 
For both documents, POC emissions comply with BACT when G ood Combustion Practices are 
followed, and PM10 emissions comply with BACT by the use of Natural Gas Fuel.   
 
For NOx and CO, a current BACT determination is required.  The following information is 
compiled for the previous Tesoro applications for backup b oilers:  
 
Backup Boiler  Application 7642 (2003)  Application 15773 (2007)  
Source  Pollutan
t Emission Limit  
(Condition 
20683)  June 2003 
Source 
Test Emission Limit  
(Condition 
24340)  Feb/Mar 2007 
Source 
Test 
S-
1
4
9
4 NOx  7 ppm @ 3% 
O2 2.4 ppm @ 3% 
O2  
CO 50 pp m @ 3% 
O2 32 ppm @ 3% 
O2 
S-
1NOx  7 ppm @ 3% 
O2 3.0 ppm @ 3% 
O2 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 657 of 1354  
    
 657 4
9
5 CO 50 ppm @ 3% 
O2 8.6 ppm @ 3% 
O2 
S-
1
5
3
0 NOx   7 ppm @ 3% 
O2 4.5 ppm @ 3% 
O2 
CO 100 ppm @ 3% 
O2 1.0 ppm @ 3% 
O2 
S-
1
5
3
1 NOx  7 ppm @ 3% 
O2 4.4 ppm @ 3% 
O2 
CO 100 ppm @ 3% 
O2 21 ppm @ 3% 
O2 
 
Based on these data, Achieved in Practice BACT for these Backup Boilers is as follows:  
 
NOx:  7 ppm @ 3% O2  
CO: 50 ppm @ 3% O2  
 
The source tests show that the limits could be lower, but the limits above allow the necessary 
operating flexibility .  S-1550 and S -1551 are expected to comply with these BACT 2 limits.

## offsets
JSONPath: `$.offsets.narrative`

OFFSETS
TS    
 
Offsets are required as per Regulation 2 -2-302 because Tesoro emits more than 35 tpy of POC and 35 tpy of NOx 
emissions.   Regulation 2 -2-302 requires that offsets for POC an d NOx be provided at a ratio of 1.15 to 1.0.  
Regulation 2 -2-303 requires that a Major Facility must pay offsets for PM10 and SO2 in excess of 1.0 ton per new or 
modified source.  PM10 and SO2 emissions for S -1550 and S -1551 do not exceed 1.0 ton, so offse ts are only 
required for NOx and POC.  POC emission credits will be used to offset both POC and NOx emissions, as allowed 
by Regulation 2 -2-302.2.  In addition, Since S -1494 and S -1495 are no longer in service, emission offsets provided 
for Application 764 2 will be credited for this application (not including the 15% ratio).  A summary of the offsets for 
this application follows:  
 
Description  NOx (tons)  POC (tons)  
S-1550 Emissions  1.173  0.576  
S-1551 Emissions  1.173  0.576  
Total Emissions     2.346     1.152  
Adjusted for Offset Ratio of 1.15  2.698  1.325  
Return of S -1494 & S -1495 credits when taken out of service via 
Application 7642  -1.208  -0.101  
Offset Requirements  1.490  1.224  
Offset via Bank  968 -1.490  -1.224  
The total POC offsets from Bank 968 are 2.714 tons.OFFSETS
TS    
 
Offsets are required as per Regulation 2 -2-302 because Tesoro emits more than 35 tpy of POC and 35 tpy of NOx 
emissions.   Regulation 2 -2-302 requires that offsets for POC an d NOx be provided at a ratio of 1.15 to 1.0.  
Regulation 2 -2-303 requires that a Major Facility must pay offsets for PM10 and SO2 in excess of 1.0 ton per new or 
modified source.  PM10 and SO2 emissions for S -1550 and S -1551 do not exceed 1.0 ton, so offse ts are only 
required for NOx and POC.  POC emission credits will be used to offset both POC and NOx emissions, as allowed 
by Regulation 2 -2-302.2.  In addition, Since S -1494 and S -1495 are no longer in service, emission offsets provided 
for Application 764 2 will be credited for this application (not including the 15% ratio).  A summary of the offsets for 
this application follows:  
 
Description  NOx (tons)  POC (tons)  
S-1550 Emissions  1.173  0.576  
S-1551 Emissions  1.173  0.576  
Total Emissions     2.346     1.152  
Adjusted for Offset Ratio of 1.15  2.698  1.325  
Return of S -1494 & S -1495 credits when taken out of service via 
Application 7642  -1.208  -0.101  
Offset Requirements  1.490  1.224  
Offset via Bank  968 -1.490  -1.224  
The total POC offsets from Bank 968 are 2.714 tons.  
 
NSPS    
 
S-1550 and S -1551 are not Subject to NSPS Subpart Ja because they are not Fuel Gas 
Combustion Devices (natural gas is excluded from the definition of Fuel Gas in 40 CFR 
60.101 a unless it is commingled with refinery fuel gas).  
 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 658 of 1354  
    
 658 S-1550 and S -1551 are not subject to NSPS Subpart Db (Standards of Performance for 
Industrial -Commercial -Institutional Steam Generating Units) because the firing rate is less 
than 100 MMBtu/hr.  The Backu p Boilers are subject to NSPS Subpart Dc because the 
boiler firing rate is greater than 10 MMBtu/hr and less than 100 MMBtu/hr.  Emission 
Standards in Subpart Dc do not apply to S -1550 and S -1551 because the boilers are only 
fired on Natural Gas.  S -1550 a nd S-151 are only subject to the notification and 
recordkeeping requirements of 40 CFR 60.48c.  
 
NESHAPs and MACT  
 
S-1550 and S -1551 are not subject to NESHAPs and MACT because they are fired exclusively 
on Natural Gas and are not used as a control device o f any HAPs emissions.

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
ANCE  
 
The owner/operator of S -1550 and S -1551 Backup Boilers shall comply with Regulation 6, Rule 
1 (Particulate Matter General Requirements).  The owner/operator is expected to comply 
with Regulation 6 since th e unit is only fueled with natural gas.  Thus for any period 
aggregating more than three minutes in any hour, there should be no visible emission as 
dark or darker than No. 1 on the Ringlemann Chart (Regulation 6 -1-301) and no visible 
emission to exceed 20 % opacity (Regulation 6 -1-302).   
 
The owner/operator of S -1550 and S -1551 Backup Boilers shall comply with Reg. 9 -1-301 
(Inorganic Gaseous Pollutants:  Sulfur Dioxide for Limitations on Ground Level 
Concentrations).  
 
The owner/operator is not subject to R egulation 9 Rule 7:  Nitrogen Oxides and Carbon 
Monoxide from Industrial, Institutional, and Commercial Boilers, Steam Generators, and 
Process Heaters as per Regulation 9 -7-110.3 since S -1550 and S -1551 will be operated at 
the Tesoro Refinery.   
 
The owner /operator is not subject to Regulation 9 Rule 10:  Nitrogen Oxides and Carbon 
Monoxide from Boilers, Steam Generators, and Process Heaters in Petroleum Refineries 
because neither S -1530 or S -1531 are a ―Unit‖ as defined by Regulation 9 -10-220.  Neither 
S-1530 nor S -1531 had an Authority to Construct or Permit to Operate prior to January 5, 
2004.   
 
The owner/operator is subject to Regulation 8, Rule 18.  The natural gas fuel lines and 
components will be constructed in accordance with the requirements of the  8-18 standards 
and added to the facility fugitive emissions monitoring program.  
 
The project is considered to be ministerial under the District's CEQA regulation 2 -1-311 and 
therefore is not subject to CEQA review.   
 
The project is over 1000 feet from th e nearest school and therefore not subject to the public 
notification requirements of Reg. 2 -1-412. 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 659 of 1354  
    
 659  
The owner/operator of S -1550 and S -1551 Backup Boilers shall comply with BACT, Offsets 
NSPS and the Toxic Risk Management Policy.  
 
PSD and NESHAPS do not a pply.STATEMENT OF COMPLIANCE
ANCE  
 
The owner/operator of S -1550 and S -1551 Backup Boilers shall comply with Regulation 6, Rule 
1 (Particulate Matter General Requirements).  The owner/operator is expected to comply 
with Regulation 6 since th e unit is only fueled with natural gas.  Thus for any period 
aggregating more than three minutes in any hour, there should be no visible emission as 
dark or darker than No. 1 on the Ringlemann Chart (Regulation 6 -1-301) and no visible 
emission to exceed 20 % opacity (Regulation 6 -1-302).   
 
The owner/operator of S -1550 and S -1551 Backup Boilers shall comply with Reg. 9 -1-301 
(Inorganic Gaseous Pollutants:  Sulfur Dioxide for Limitations on Ground Level 
Concentrations).  
 
The owner/operator is not subject to R egulation 9 Rule 7:  Nitrogen Oxides and Carbon 
Monoxide from Industrial, Institutional, and Commercial Boilers, Steam Generators, and 
Process Heaters as per Regulation 9 -7-110.3 since S -1550 and S -1551 will be operated at 
the Tesoro Refinery.   
 
The owner /operator is not subject to Regulation 9 Rule 10:  Nitrogen Oxides and Carbon 
Monoxide from Boilers, Steam Generators, and Process Heaters in Petroleum Refineries 
because neither S -1530 or S -1531 are a ―Unit‖ as defined by Regulation 9 -10-220.  Neither 
S-1530 nor S -1531 had an Authority to Construct or Permit to Operate prior to January 5, 
2004.   
 
The owner/operator is subject to Regulation 8, Rule 18.  The natural gas fuel lines and 
components will be constructed in accordance with the requirements of the  8-18 standards 
and added to the facility fugitive emissions monitoring program.  
 
The project is considered to be ministerial under the District's CEQA regulation 2 -1-311 and 
therefore is not subject to CEQA review.   
 
The project is over 1000 feet from th e nearest school and therefore not subject to the public 
notification requirements of Reg. 2 -1-412. 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 659 of 1354  
    
 659  
The owner/operator of S -1550 and S -1551 Backup Boilers shall comply with BACT, Offsets 
NSPS and the Toxic Risk Management Policy.  
 
PSD and NESHAPS do not a pply.

## public_notification
JSONPath: `$.public_notification.text`

(empty)

## conditions
JSONPath: `$.conditions.text`

PERMIT CONDITIONS
IONS   
Application 20977 (November 2009)  
 
 S-1550  Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1550 SCR  
 S-1551  Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1551 SCR  
 
1. The owner/operator s hall ensure that S -1550 and S -1551 are fired exclusively on natural gas at a rate not to 
exceed 99 MMBtu/hr each.  (Basis: Cumulative Increase, Offsets, Toxics, NSPS, BACT)  
 
2. The owner/operator shall ensure that S -1550 and S -1551 are on site at the refinery  for no more that 6 
consecutive months per 12 consecutive month period.  The 6 -month period for each boiler begins upon the 
initial firing of the boiler.  (Basis:  BACT)  
 
3. The owner/operator shall ensure each boiler S -1550 and S -1551 is not operated for mor e than 2160 hours in 
any consecutive 12 -month period.   (Basis: Cumulative Increase, Offsets, Toxics)  
 
4. Except for a time period not to exceed 24 hours per boiler startup or shutdown, the owner/operator shall 
ensure that S -1550 and S -1551 are only operated when abated by SCRs A -1550 and A -1551, respectively.  
The total hours that S -1550 or S -1551 is operated without SCR abatement shall not exceed 192 hours per 
consecutive 12 -month period.  (Basis: Cumulative Increase, Offsets, Toxics)  
 
5. The owner/operator sha ll ensure that S -1530 and S -1531 are not operated unless they are each equipped 
with a District approved, fuel flow meter that measures the total volume of fuel throughput to S -1530 and S -
1531 in units of standard cubic feet.  (Basis: Cumulative Increase, Offsets, Toxics)  
 
6. The owner/operator shall ensure that the total fuel fired in S -1530 and S -1531 shall not exceed 4,277,000 
therms in any 12 consecutive month period.  (Basis: Cumulative Increase, Offsets, Toxics)  
 
7. Except for periods of startup and shutdow n as allowed in Part 4, the owner operator shall not operate S -
1550 or S -1551 unless NOx emissions are less than 7 ppmv, dry, @ 3% O2.  (Basis: Cumulative Increase, 
Offsets, BACT)  
 
8. During for periods of startup and shutdown as allowed in Part 4, the owner operator shall not operate S -
1550 or S -1551 unless NOx emissions are less than 30 ppmv, dry, @ 3% O2.  (Basis: Cumulative Increase, 
Offsets)  
 
9. The owner operator shall not operate S -1550 or S -1551 unless CO emissions are less than 50 ppmv, dry, @ 
3% O2.  (B asis: Cumulative Increase, Offsets, BACT)  
 
10. Within 10 days of the first fire date, the owner/operator shall conduct a District approved source test of each 
S-1550 and S -1551.  The District approved source test shall measure the emission rates of NOx, POC, S O2, 
and PM10, from S -1550 and S -1551 while it is operated at not less than 80 MMBtu/hr.  The owner/operator 
shall ensure that within 45 days of the date of completion of the source testing, two identical copies of the 
source tests results (each referencing  permit application #20977 and plant #14628) are received by the 
District.  One copy shall be sent to Source Testing and the other shall be sent to the Engineering Division.  
This District approved source test shall be repeated within 5 days of each subseq uent boiler startup (or any 
operation without SCR abatement) during the 6 -month period of boiler operation.  (Basis: Cumulative 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 660 of 1354  
    
 660 Increase, Offsets, BACT)  
 
11. In a District approved log, the owner/operator shall record the manufacturer, make, model, and maximum  
rated firing rate of each boiler used as S -1550 and S -1551, and the following information for each calendar 
day that either S -1550 or S -1551 fires fuel.  The District approved log(s) shall be retained by the 
owner/operator on site for at least 5 years fro m the date of the last entry and made available to District staff 
upon request.  (Basis: Cumulative Increase, Offsets, Toxics, BACT)  
a. The date and hours that each S -1550 and S -1551 fire fuel.  
b. The amount of fuel fired at each S -1550 and S -1551.  
c. The hours tha t each S -1550 and S -1551 operate without abatement by a fully functioning SCR.  
d. The amount of steam produced at each boiler S -1550 and S -1551.PERMIT CONDITIONS
IONS   
Application 20977 (November 2009)  
 
 S-1550  Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1550 SCR  
 S-1551  Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1551 SCR  
 
1. The owner/operator s hall ensure that S -1550 and S -1551 are fired exclusively on natural gas at a rate not to 
exceed 99 MMBtu/hr each.  (Basis: Cumulative Increase, Offsets, Toxics, NSPS, BACT)  
 
2. The owner/operator shall ensure that S -1550 and S -1551 are on site at the refinery  for no more that 6 
consecutive months per 12 consecutive month period.  The 6 -month period for each boiler begins upon the 
initial firing of the boiler.  (Basis:  BACT)  
 
3. The owner/operator shall ensure each boiler S -1550 and S -1551 is not operated for mor e than 2160 hours in 
any consecutive 12 -month period.   (Basis: Cumulative Increase, Offsets, Toxics)  
 
4. Except for a time period not to exceed 24 hours per boiler startup or shutdown, the owner/operator shall 
ensure that S -1550 and S -1551 are only operated when abated by SCRs A -1550 and A -1551, respectively.  
The total hours that S -1550 or S -1551 is operated without SCR abatement shall not exceed 192 hours per 
consecutive 12 -month period.  (Basis: Cumulative Increase, Offsets, Toxics)  
 
5. The owner/operator sha ll ensure that S -1530 and S -1531 are not operated unless they are each equipped 
with a District approved, fuel flow meter that measures the total volume of fuel throughput to S -1530 and S -
1531 in units of standard cubic feet.  (Basis: Cumulative Increase, Offsets, Toxics)  
 
6. The owner/operator shall ensure that the total fuel fired in S -1530 and S -1531 shall not exceed 4,277,000 
therms in any 12 consecutive month period.  (Basis: Cumulative Increase, Offsets, Toxics)  
 
7. Except for periods of startup and shutdow n as allowed in Part 4, the owner operator shall not operate S -
1550 or S -1551 unless NOx emissions are less than 7 ppmv, dry, @ 3% O2.  (Basis: Cumulative Increase, 
Offsets, BACT)  
 
8. During for periods of startup and shutdown as allowed in Part 4, the owner operator shall not operate S -
1550 or S -1551 unless NOx emissions are less than 30 ppmv, dry, @ 3% O2.  (Basis: Cumulative Increase, 
Offsets)  
 
9. The owner operator shall not operate S -1550 or S -1551 unless CO emissions are less than 50 ppmv, dry, @ 
3% O2.  (B asis: Cumulative Increase, Offsets, BACT)  
 
10. Within 10 days of the first fire date, the owner/operator shall conduct a District approved source test of each 
S-1550 and S -1551.  The District approved source test shall measure the emission rates of NOx, POC, S O2, 
and PM10, from S -1550 and S -1551 while it is operated at not less than 80 MMBtu/hr.  The owner/operator 
shall ensure that within 45 days of the date of completion of the source testing, two identical copies of the 
source tests results (each referencing  permit application #20977 and plant #14628) are received by the 
District.  One copy shall be sent to Source Testing and the other shall be sent to the Engineering Division.  
This District approved source test shall be repeated within 5 days of each subseq uent boiler startup (or any 
operation without SCR abatement) during the 6 -month period of boiler operation.  (Basis: Cumulative 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 660 of 1354  
    
 660 Increase, Offsets, BACT)  
 
11. In a District approved log, the owner/operator shall record the manufacturer, make, model, and maximum  
rated firing rate of each boiler used as S -1550 and S -1551, and the following information for each calendar 
day that either S -1550 or S -1551 fires fuel.  The District approved log(s) shall be retained by the 
owner/operator on site for at least 5 years fro m the date of the last entry and made available to District staff 
upon request.  (Basis: Cumulative Increase, Offsets, Toxics, BACT)  
a. The date and hours that each S -1550 and S -1551 fire fuel.  
b. The amount of fuel fired at each S -1550 and S -1551.  
c. The hours tha t each S -1550 and S -1551 operate without abatement by a fully functioning SCR.  
d. The amount of steam produced at each boiler S -1550 and S -1551.

## permit_conditions
JSONPath: `$.permit_conditions`

- Item 1
The owner/operator s hall ensure that S -1550 and S -1551 are fired exclusively on natural gas at a rate not to 
exceed 99 MMBtu/hr each.  (
Basis: Cumulative Increase, Offsets, Toxics, NSPS, BACT)

- Item 2
The owner/operator shall ensure that S -1550 and S -1551 are on site at the refinery  for no more that 6 
consecutive months per 12 consecutive month period.  The 6 -month period for each boiler begins upon the 
initial firing of the boiler.  (
Basis: BACT)

- Item 3
The owner/operator shall ensure each boiler S -1550 and S -1551 is not operated for mor e than 2160 hours in 
any consecutive 12 -month period.   (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 4
Except for a time period not to exceed 24 hours per boiler startup or shutdown, the owner/operator shall 
ensure that S -1550 and S -1551 are only operated when abated by SCRs A -1550 and A -1551, respectively.  
The total hours that S -1550 or S -1551 is operated without SCR abatement shall not exceed 192 hours per 
consecutive 12 -month period.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 5
The owner/operator sha ll ensure that S -1530 and S -1531 are not operated unless they are each equipped 
with a District approved, fuel flow meter that measures the total volume of fuel throughput to S -1530 and S -
1531 in units of standard cubic feet.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 6
The owner/operator shall ensure that the total fuel fired in S -1530 and S -1531 shall not exceed 4,277,000 
therms in any 12 consecutive month period.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 7
Except for periods of startup and shutdow n as allowed in Part 4, the owner operator shall not operate S -
1550 or S -1551 unless NOx emissions are less than 7 ppmv, dry, @ 3% O2.  (
Basis: Cumulative Increase, Offsets, BACT)

- Item 8
During for periods of startup and shutdown as allowed in Part 4, the owner operator shall not operate S -
1550 or S -1551 unless NOx emissions are less than 30 ppmv, dry, @ 3% O2.  (
Basis: Cumulative Increase, Offsets)

- Item 9
The owner operator shall not operate S -1550 or S -1551 unless CO emissions are less than 50 ppmv, dry, @ 
3% O2.  (B asis: Cumulative Increase, Offsets, BACT)

- Item 10
Within 10 days of the first fire date, the owner/operator shall conduct a District approved source test of each 
S-1550 and S -1551.  The District approved source test shall measure the emission rates of NOx, POC, S O2, 
and PM10, from S -1550 and S -1551 while it is operated at not less than 80 MMBtu/hr.  The owner/operator 
shall ensure that within 45 days of the date of completion of the source testing, two identical copies of the 
source tests results (each referencing  permit application #20977 and plant #14628) are received by the 
District.  One copy shall be sent to Source Testing and the other shall be sent to the Engineering Division.  
This District approved source test shall be repeated within 5 days of each subseq uent boiler startup (or any 
operation without SCR abatement) during the 6 -month period of boiler operation.  (
Basis: Cumulative 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 660 of 1354  
    
 660 Increase, Offsets, BACT)

- Item 11
In a District approved log, the owner/operator shall record the manufacturer, make, model, and maximum  
rated firing rate of each boiler used as S -1550 and S -1551, and the following information for each calendar 
day that either S -1550 or S -1551 fires fuel.  The District approved log(s) shall be retained by the 
owner/operator on site for at least 5 years fro m the date of the last entry and made available to District staff 
upon request.  (
Basis: Cumulative Increase, Offsets, Toxics, BACT)  
a. The date and hours that each S -1550 and S -1551 fire fuel.  
b. The amount of fuel fired at each S -1550 and S -1551.  
c. The hours tha t each S -1550 and S -1551 operate without abatement by a fully functioning SCR.  
d. The amount of steam produced at each boiler S -1550 and S -1551.PERMIT CONDITIONS
IONS   
Application 20977 (November 2009)  
 
 S-1550  Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1550 SCR  
 S-1551  Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1551 SCR

- Item 1
The owner/operator s hall ensure that S -1550 and S -1551 are fired exclusively on natural gas at a rate not to 
exceed 99 MMBtu/hr each.  (
Basis: Cumulative Increase, Offsets, Toxics, NSPS, BACT)

- Item 2
The owner/operator shall ensure that S -1550 and S -1551 are on site at the refinery  for no more that 6 
consecutive months per 12 consecutive month period.  The 6 -month period for each boiler begins upon the 
initial firing of the boiler.  (
Basis: BACT)

- Item 3
The owner/operator shall ensure each boiler S -1550 and S -1551 is not operated for mor e than 2160 hours in 
any consecutive 12 -month period.   (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 4
Except for a time period not to exceed 24 hours per boiler startup or shutdown, the owner/operator shall 
ensure that S -1550 and S -1551 are only operated when abated by SCRs A -1550 and A -1551, respectively.  
The total hours that S -1550 or S -1551 is operated without SCR abatement shall not exceed 192 hours per 
consecutive 12 -month period.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 5
The owner/operator sha ll ensure that S -1530 and S -1531 are not operated unless they are each equipped 
with a District approved, fuel flow meter that measures the total volume of fuel throughput to S -1530 and S -
1531 in units of standard cubic feet.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 6
The owner/operator shall ensure that the total fuel fired in S -1530 and S -1531 shall not exceed 4,277,000 
therms in any 12 consecutive month period.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 7
Except for periods of startup and shutdow n as allowed in Part 4, the owner operator shall not operate S -
1550 or S -1551 unless NOx emissions are less than 7 ppmv, dry, @ 3% O2.  (
Basis: Cumulative Increase, Offsets, BACT)

- Item 8
During for periods of startup and shutdown as allowed in Part 4, the owner operator shall not operate S -
1550 or S -1551 unless NOx emissions are less than 30 ppmv, dry, @ 3% O2.  (
Basis: Cumulative Increase, Offsets)

- Item 9
The owner operator shall not operate S -1550 or S -1551 unless CO emissions are less than 50 ppmv, dry, @ 
3% O2.  (B asis: Cumulative Increase, Offsets, BACT)

- Item 10
Within 10 days of the first fire date, the owner/operator shall conduct a District approved source test of each 
S-1550 and S -1551.  The District approved source test shall measure the emission rates of NOx, POC, S O2, 
and PM10, from S -1550 and S -1551 while it is operated at not less than 80 MMBtu/hr.  The owner/operator 
shall ensure that within 45 days of the date of completion of the source testing, two identical copies of the 
source tests results (each referencing  permit application #20977 and plant #14628) are received by the 
District.  One copy shall be sent to Source Testing and the other shall be sent to the Engineering Division.  
This District approved source test shall be repeated within 5 days of each subseq uent boiler startup (or any 
operation without SCR abatement) during the 6 -month period of boiler operation.  (
Basis: Cumulative 
Tesoro Refining and Marketing Company   Application #20977  
Plant # 14628   Page 660 of 1354  
    
 660 Increase, Offsets, BACT)

- Item 11
In a District approved log, the owner/operator shall record the manufacturer, make, model, and maximum  
rated firing rate of each boiler used as S -1550 and S -1551, and the following information for each calendar 
day that either S -1550 or S -1551 fires fuel.  The District approved log(s) shall be retained by the 
owner/operator on site for at least 5 years fro m the date of the last entry and made available to District staff 
upon request.  (
Basis: Cumulative Increase, Offsets, Toxics, BACT)  
a. The date and hours that each S -1550 and S -1551 fire fuel.  
b. The amount of fuel fired at each S -1550 and S -1551.  
c. The hours tha t each S -1550 and S -1551 operate without abatement by a fully functioning SCR.  
d. The amount of steam produced at each boiler S -1550 and S -1551.

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

RECOMMENDATION
DATION  
Waive an Authority to Construct and grant a Permit to Operate to Tesoro Refining and Marketing C ompany for the 
following sources:  
 
 S-1550  Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated byRECOMMENDATION
DATION  
Waive an Authority to Construct and grant a Permit to Operate to Tesoro Refining and Marketing C ompany for the 
following sources:  
 
 S-1550  Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by 
A-1550 SCR  
 S-1551  Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by 
A-1551 SCR  
 
 
EXEMPTIONS  
none  
 
 
 
By:  
 Arthur P Valla  
 Senio r Air Quality Engineer  
November 5, 2009
