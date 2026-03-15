---
application_number: 22169
plant_id: 14628
plant_name: Golden Eagle Refinery, 150 Solano Way, Martinez, Ca 94553
evaluation_date: September 16, 2010
source_pdf: C:\Users\aaw\Codex\BAAD Engr Evals\split_evals_2015_11\application_22169.pdf
source_json: JSON/baad_eval_to_json_bulk_2026-03-05/application_22169__eval.json
---

# Engineering Evaluation (Application 22169)
**Plant**: 14628 Golden Eagle Refinery, 150 Solano Way, Martinez, Ca 94553
**Evaluation Date**: September 16, 2010

## background
JSONPath: `$.background.text`

BACKGROUND
The Tesoro Refining and Marketing Company (Tesoro) is applying for an Authority to Construct 
and/or Permit to Operate the following equipment:  
 
 S-1553  Backup Steam Boiler #3, 99 MM Btu/hr, Natural Gas Fired, Abated byBACKGROUND
ND  
 
The Tesoro Refining and Marketing Company (Tesoro) is applying for an Authority to Construct 
and/or Permit to Operate the following equipment:  
 
 S-1553  Backup Steam Boiler #3, 99 MM Btu/hr, Natural Gas Fired, Abated by 
A-1553 SCR  
 
This is a third backup boiler.  The other two boilers were permitted via Application 20977:  
 
 S-1550  Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by 
A-1550 SCR  
 S-1551  Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by 
A-1551 SCR  
 
These Backup Boilers are needed to ensure adequate steam supply for the refinery when existing 
boilers S -901 and S -904 are removed from service for turnaround/maintenance.  The third 
boiler S -1553 will be a new source, but emissions will not change for all three boilers by 
keeping the curre nt firing limits and time allowed for unabated operation in Condition 
24491 -4 and 24491 -6: 
 
4.  Except for a time period not to exceed 24 hours per boiler startup or shutdown, the 
owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are only oper ated when 
abated by SCRs A -1550 , and A-1551  and A -1553 , respectively.  The total cumulative 
hours that S-1550  or S-1551 all three boilers  can be  is operated without SCR abatement 
shall not exceed 192 hours per consecutive 12 -month period.  (Basis: Cumulativ e 
Increase, Offsets, Toxics)  
 
6.  The owner/operator shall ensure that the total fuel fired in S -1550 , and S-1551  and S -1553  
shall not exceed 4,277,000 therms in any 12 consecutive month period.  (Basis: 
Cumulative Increase, Offsets, Toxics)  
   
By using this permitting rationale, the application qualifies for the Accelerated Permitting 
Program and the Temporary Permit to Operate was granted August 3, 2010.  
 
In addition, Tesoro has requested that Condition 24491 -3 be deleted.  The time limit can be an 
operating problem and emissions are effectively capped by conditions 24491 -4 and 24491 -
6. 
 
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  87 November 3 , 2015  3.  The owner/operator shall ensure each boiler S -1550 and S -1551 is not operated for more 
than 2160 hours in any consecutive 12 -month period.   (Basis: Cumulative Incre ase, 
Offsets, Toxics)

## emission_calculations
JSONPath: `$.emission_calculations.text`

EMISSION CALCULATIONS
IONS  
 
Emission Factors  
 
The following emissions factors are used to calculate emissions from Backup Boiler S -1553, which are the same as 
Boilers S -1550 an S -1551.  
 
NOx:   7 ppm @ 3% O2 when abated by SCR (BACT)  
 30 ppm @ 3% O2 without SCR operation (192 hrs/yr per boiler)  
CO: 50 ppm @ 3% O2 (BACT)  
PM10  7.45E -3 lb/MMBtu  
VOC  5.39E -3 lb/MMBtu (assume to be all POC)  
SO2 5.88E -4 lb/MMBtu  
Emission factors for PM10, POC, and SO2 are from Chapter 1, Table 1.4 -2 of the EPA Do cument AP -42, 
Compilation of Air Pollutant Emission Factors (lb/106scf / 1020).  
 
Exhaust flow:  (8710 dscf/MMBtu)*(20.95/(20.95 -3))=10165.7 dscf/MMBtu at 3% O2  
 
At atmospheric pressure and low temperatures, the ideal gas law will provide the necessary calc ulation accuracy:  
n = PV/RT = (1atm*10165.7 dscf/MMBtu) /((0.7302 atm -cf/lb-mol R)*(68 + 460 R))  
= 26.367 lb -mol/MMBtu  
 
NOx w/ SCR:  26.367 lb -mol/MMBtu(7 lb -mol NOx/1E6 lb -mol)(46 lb NOx/lb -mol NOx)  
= 0.00849 lb/MMBtu  
NOx w/o SCR:  26.367 lb -mol/MMBtu(30 lb -mol NOx/1E6 lb -mol)(46 lb NOx/lb -mol NOx)  
= 0.0364 lb/MMBtu  
CO:  26.367 lb -mol/MMBtu(50 lb -mol NOx/1E6 lb -mol)(28 lb CO/lb -mol CO)  
= 0.0369 lb/MMBtu  
 
Annual Emissions:  
 
Emissions from S -1553 Backup Boiler:  
NOx (SCR)    =(99 MMBtu /hr)(0.00849 lb NOx/MMBtu)(2160 -192 hrs) = 1654 lb = 0.827 
tons 
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(192 hrs) = 692 lb = 0.346 tons  
NOx (total)   = 1654 + 692 = 2346 lbs = 1.173 tons  
CO   =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(2160 hrs) = 7891 lb = 3.945 tons  
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MMBtu)(2160 hrs) = 1593 lb = 0.797 tons  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(2160 hrs) = 1153 lb = 0.576 tons  
SO2   =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(2160 hrs) = 126 lb = 0.063 tons  
 
However, as e xplained above, the total annual fuel throughput for all three boilers will not change, so there will not 
be any emissions increase (any emissions from S -1553 will cause a reduction in emissions from the other boilers S -
1550 and S -1551).  
 
 
Cumulative Incre ase: 
 
There is no cumulative increase in emissions.  
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  88 November 3 , 2015   
Maximum Daily Emissions:  
 
NOx (SCR)   =(99 MMBtu/hr)(0.00849 lb NOx/MMBtu)(24 hrs) = 20.1 lb  
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(24 hrs) = 86 lb  
CO   =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(24 hrs) = 88 lb  
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MMBtu)(24 hrs) = 17.7 lb  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(24 hrs) = 12.8 lb  
SO2   =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(24 hrs) = 1.4 lb  
 
 
 
 
 
Toxic Risk S creening  
 
 
The following toxic emissions were calculated for each boiler.  
 
TAC  Emission Factor 
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
IONS  
 
Emission Factors  
 
The following emissions factors are used to calculate emissions from Backup Boiler S -1553, which are the same as 
Boilers S -1550 an S -1551.  
 
NOx:   7 ppm @ 3% O2 when abated by SCR (BACT)  
 30 ppm @ 3% O2 without SCR operation (192 hrs/yr per boiler)  
CO: 50 ppm @ 3% O2 (BACT)  
PM10  7.45E -3 lb/MMBtu  
VOC  5.39E -3 lb/MMBtu (assume to be all POC)  
SO2 5.88E -4 lb/MMBtu  
Emission factors for PM10, POC, and SO2 are from Chapter 1, Table 1.4 -2 of the EPA Do cument AP -42, 
Compilation of Air Pollutant Emission Factors (lb/106scf / 1020).  
 
Exhaust flow:  (8710 dscf/MMBtu)*(20.95/(20.95 -3))=10165.7 dscf/MMBtu at 3% O2  
 
At atmospheric pressure and low temperatures, the ideal gas law will provide the necessary calc ulation accuracy:  
n = PV/RT = (1atm*10165.7 dscf/MMBtu) /((0.7302 atm -cf/lb-mol R)*(68 + 460 R))  
= 26.367 lb -mol/MMBtu  
 
NOx w/ SCR:  26.367 lb -mol/MMBtu(7 lb -mol NOx/1E6 lb -mol)(46 lb NOx/lb -mol NOx)  
= 0.00849 lb/MMBtu  
NOx w/o SCR:  26.367 lb -mol/MMBtu(30 lb -mol NOx/1E6 lb -mol)(46 lb NOx/lb -mol NOx)  
= 0.0364 lb/MMBtu  
CO:  26.367 lb -mol/MMBtu(50 lb -mol NOx/1E6 lb -mol)(28 lb CO/lb -mol CO)  
= 0.0369 lb/MMBtu  
 
Annual Emissions:  
 
Emissions from S -1553 Backup Boiler:  
NOx (SCR)    =(99 MMBtu /hr)(0.00849 lb NOx/MMBtu)(2160 -192 hrs) = 1654 lb = 0.827 
tons 
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(192 hrs) = 692 lb = 0.346 tons  
NOx (total)   = 1654 + 692 = 2346 lbs = 1.173 tons  
CO   =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(2160 hrs) = 7891 lb = 3.945 tons  
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MMBtu)(2160 hrs) = 1593 lb = 0.797 tons  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(2160 hrs) = 1153 lb = 0.576 tons  
SO2   =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(2160 hrs) = 126 lb = 0.063 tons  
 
However, as e xplained above, the total annual fuel throughput for all three boilers will not change, so there will not 
be any emissions increase (any emissions from S -1553 will cause a reduction in emissions from the other boilers S -
1550 and S -1551).  
 
 
Cumulative Incre ase: 
 
There is no cumulative increase in emissions.  
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  88 November 3 , 2015   
Maximum Daily Emissions:  
 
NOx (SCR)   =(99 MMBtu/hr)(0.00849 lb NOx/MMBtu)(24 hrs) = 20.1 lb  
NOx (w/o SCR)   =(99 MMBtu/hr)(0.0364 lb NOx/MMBtu)(24 hrs) = 86 lb  
CO   =(99 MMBtu/hr)(0.0369 lb CO/MMBtu)(24 hrs) = 88 lb  
PM10    =(99 MMBtu/hr)(7.45E -3 lb PM10/MMBtu)(24 hrs) = 17.7 lb  
POC    =(99 MMBtu/hr)(5.39E -3 lb POC/MMBtu)(24 hrs) = 12.8 lb  
SO2   =(99 MMBtu/hr)(5.88E -4 lb SO2/MMBtu)(24 hrs) = 1.4 lb  
 
 
 
 
 
Toxic Risk S creening  
 
 
The following toxic emissions were calculated for each boiler.  
 
TAC  Emission Factor 
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
 
 
However, since the toxic emissions are based on boiler firing duty, and the overall annual duty of 
the three boilers will not change, the overall toxic emissions will not change, and a risk 
screen is not required.  The risk screen conducted for the first two boilers showed the 
project risk is considered acceptable with a Maximum Cancer Risk of 0.004 in a million, 
the chronic hazard index of 0.00008 and the acute hazard index of 0.003.  
 
BEST AVAILABLE CONTROL TECHNOLOGY   
 
In accordance with Regulation 2, Rule 2, Section 301, BACT i s triggered for any new or 
modified source with the potential to emit 10 pounds or more per highest day of POC, 
NPOC, NOx, CO, SO 2 or PM 10.  Emissions from S -1553 trigger BACT for the following 
pollutants:  NOx, CO, PM10, and POC.   
 
A BACT Determination f or these backup boilers was made in Application 20977. The Achieved 
in Practice BACT for these Backup Boilers was determined as follows:  
 
NOx:  7 ppm @ 3% O2  
CO: 50 ppm @ 3% O2  
POC emissions comply with BACT when Good Combustion Practices are followed.  
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  89 November 3 , 2015  PM10  emissions comply with BACT by the use of Natural Gas Fuel.

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

(empty)

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

(empty)

## offsets
JSONPath: `$.offsets.narrative`

OFFSETS
TS    
 
There are no increase in annual emissions due to this application, so Offsets are not required.  A summary of the 
offsets for Application 20977 follows:  
 
Description  NOx (tons)  POC (tons)  
S-1550 Emissions  1.173  0.576  
S-1551 Emissions  1.173  0.576  
Total Emissions     2.346     1.152  
Adjusted for Offset Ratio of 1.15  2.698  1.325  
Return of S -1494 &  S-1495 credits when taken out of service 
via Application 7642  -1.208  -0.101  
Offset Requirements  1.490  1.224  
Offset via Bank 968  -1.490  -1.224  
The total POC offsets from Bank 968 are 2.714 tons.OFFSETS
TS    
 
There are no increase in annual emissions due to this application, so Offsets are not required.  A summary of the 
offsets for Application 20977 follows:  
 
Description  NOx (tons)  POC (tons)  
S-1550 Emissions  1.173  0.576  
S-1551 Emissions  1.173  0.576  
Total Emissions     2.346     1.152  
Adjusted for Offset Ratio of 1.15  2.698  1.325  
Return of S -1494 &  S-1495 credits when taken out of service 
via Application 7642  -1.208  -0.101  
Offset Requirements  1.490  1.224  
Offset via Bank 968  -1.490  -1.224  
The total POC offsets from Bank 968 are 2.714 tons.  
 
 
 
NSPS    
 
S-1553 is not Subject to  NSPS Subpart Ja because it is not a Fuel Gas Combustion Devices (natural gas is excluded 
from the definition of Fuel Gas in 40 CFR 60.101a unless it is commingled with refinery fuel gas).  
 
S-1553 is not Subject to NSPS Subpart Db (Standards of Performance  for Industrial -Commercial -Institutional Steam 
Generating Units) because the firing rate is less than 100 MMBtu/hr.  The Backup Boilers is subject to NSPS 
Subpart Dc because the boiler firing rate is greater than 10 MMBtu/hr and less than 100 MMBtu/hr.  Em ission 
Standards in Subpart Dc do not apply to S -1553 because the boiler is only fired on Natural Gas.  S -1553 is only 
subject to the notification and recordkeeping requirements of 40 CFR 60.48c.  
 
NESHAPs and MACT  
 
S-1553 is not subject to NESHAPs and MACT  because they are fired exclusively on Natural Gas 
and are not used as a control device of any HAPs emissions.   
 
PREVENTION OF SIGNIFICANT DETERIORATION (PSD)  
 
The Tesoro facility is an existing major stationary source.  To determine the applicability of PSD, 40 CFR 
52.21(b)(2)(i) requires a two -step evaluation.  The first step is to determine if the project will result in a significant 
emissions increase.  The second step it to determine if the project will result in a significant net emissions increase.  
Both steps need to result in emissions that exceed significance levels for PSD to apply.  
 
The emissions increases need to be determined and compared to the following significance levels 
[40CFR52.21(b)(23)(i)]:  
Carbon monoxide: 100 tons per year (tpy)  
Nitrogen oxides: 40 tpy  
Sulfur dioxide: 40 tpy  
Particulate matter: 25 tpy of particulate matter emissions  
PM10: 15 tpy  
PM2.5: 10 tpy of direct PM2.5emissions; 40 tpy of sulfur dioxide emissions; 40 tpy of nitrogen oxide 
emissions unless demonstrated not to be a PM2.5precursor under paragraph (b)(50) of this section  
Ozone: 40 tpy of volatile organic compounds or nitrogen oxides  
Sulfuric acid mist: 7 tpy  
Hydrogen sulfide (H2S): 10 tpy  
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  90 November 3 , 2015  Total reduced sulfur (including H2S): 10 tpy  
Reduced sulfur compounds (includin g H2S): 10 tpy  
 
The ‘project’ for this application is to install backup boilers to provide process steam while the Main Boilers are 
shutdown.  The baseline actual emissions for steam production would decrease since the backup boilers, rated at 99 
MMBtu/hr each, are operating while one of the main boilers are shutdown (S -901 @ 668MM Btu/hr and S -904 @ 
775 MM Btu/hr).  Even if all three backup boilers are fired a full rate, the 3x99 = 297 MMBtu/hr duty would be less 
than half the duty on the shutdown boiler.  Consequently, the net emissions change would be a reduction.  Therefore, 
PSD does not apply.

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

PREVENTION OF SIGNIFICANT DETERIORATION (PSD)
D)  
 
The Tesoro facility is an existing major stationary source.  To determine the applicability of PSD, 40 CFR 
52.21(b)(2)(i) requires a two -step evaluation.  The first step is to determine if the project will result in a significant 
emissions increase.  The second step it to determine if the project will result in a significant net emissions increase.  
Both steps need to result in emissions that exceed significance levels for PSD to apply.  
 
The emissions increases need to be determined and compared to the following significance levels 
[40CFR52.21(b)(23)(i)]:  
Carbon monoxide: 100 tons per year (tpy)  
Nitrogen oxides: 40 tpy  
Sulfur dioxide: 40 tpy  
Particulate matter: 25 tpy of particulate matter emissions  
PM10: 15 tpy  
PM2.5: 10 tpy of direct PM2.5emissions; 40 tpy of sulfur dioxide emissions; 40 tpy of nitrogen oxide 
emissions unless demonstrated not to be a PM2.5precursor under paragraph (b)(50) of this section  
Ozone: 40 tpy of volatile organic compounds or nitrogen oxides  
Sulfuric acid mist: 7 tpy  
Hydrogen sulfide (H2S): 10 tpy  
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  90 November 3 , 2015  Total reduced sulfur (including H2S): 10 tpy  
Reduced sulfur compounds (includin g H2S): 10 tpy  
 
The ‘project’ for this application is to install backup boilers to provide process steam while the Main Boilers are 
shutdown.  The baseline actual emissions for steam production would decrease since the backup boilers, rated at 99 
MMBtu/hr each, are operating while one of the main boilers are shutdown (S -901 @ 668MM Btu/hr and S -904 @ 
775 MM Btu/hr).  Even if all three backup boilers are fired a full rate, the 3x99 = 297 MMBtu/hr duty would be less 
than half the duty on the shutdown boiler.  Consequently, the net emissions change would be a reduction.  Therefore, 
PSD does not apply.

## CEQA
JSONPath: `$.CEQA.narrative`

(empty)

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General
STATEMENT OF COMPLIANCE
CE  
 
The owner/operator of S-1553 Backup Boiler shall comply with Regulation 6, Rule 1 (Particulate 
Matter General Requirements).  The owner/operator is expected to comply with Regulation 
6 since the unit is only fueled with natural gas.  Thus for any period aggregating more than 
three minutes in any hour, there should be no visible emission as dark or darker than No. 1 
on the Ringlemann Chart (Regulation 6 -1-301) and no visible emission to exceed 20% 
opacity (Regulation 6 -1-302).   
 
The owner/operator of S -1553 Backup Boiler shall c omply with Reg. 9 -1-301 (Inorganic 
Gaseous Pollutants:  Sulfur Dioxide for Limitations on Ground Level Concentrations).  
 
The owner/operator is not subject to Regulation 9 Rule 7:  Nitrogen Oxides and Carbon 
Monoxide from Industrial, Institutional, and Comm ercial Boilers, Steam Generators, and 
Process Heaters as per Regulation 9 -7-110.3 since S -1553 will be operated at the Tesoro 
Refinery.   
 
The owner/operator is not subject to Regulation 9 Rule 10:  Nitrogen Oxides and Carbon 
Monoxide from Boilers, Steam G enerators, and Process Heaters in Petroleum Refineries 
because S -1553 is not a “Unit” as defined by Regulation 9 -10-220.  S -1553 did not have an 
Authority to Construct or Permit to Operate prior to January 5, 2004.   
 
The owner/operator is subject to Regul ation 8, Rule 18.  The natural gas fuel lines and 
components will be constructed in accordance with the requirements of the 8 -18 standards 
and added to the facility fugitive emissions monitoring program.  
 
The project is considered to be ministerial under t he District's CEQA regulation 2 -1-311 and therefore is not subject 
to CEQA review.   
 
The project is over 1000 feet from the nearest school and therefore not subject to the public notification 
requirements of Reg. 2 -1-412. 
 
The owner/operator of S -1553 Backup Boiler shall comply with BACT and NSPS.  
 
Offsets, Toxics, PSD and NESHAPS do not apply.STATEMENT OF COMPLIANCE
CE  
 
The owner/operator of S-1553 Backup Boiler shall comply with Regulation 6, Rule 1 (Particulate 
Matter General Requirements).  The owner/operator is expected to comply with Regulation 
6 since the unit is only fueled with natural gas.  Thus for any period aggregating more than 
three minutes in any hour, there should be no visible emission as dark or darker than No. 1 
on the Ringlemann Chart (Regulation 6 -1-301) and no visible emission to exceed 20% 
opacity (Regulation 6 -1-302).   
 
The owner/operator of S -1553 Backup Boiler shall c omply with Reg. 9 -1-301 (Inorganic 
Gaseous Pollutants:  Sulfur Dioxide for Limitations on Ground Level Concentrations).  
 
The owner/operator is not subject to Regulation 9 Rule 7:  Nitrogen Oxides and Carbon 
Monoxide from Industrial, Institutional, and Comm ercial Boilers, Steam Generators, and 
Process Heaters as per Regulation 9 -7-110.3 since S -1553 will be operated at the Tesoro 
Refinery.   
 
The owner/operator is not subject to Regulation 9 Rule 10:  Nitrogen Oxides and Carbon 
Monoxide from Boilers, Steam G enerators, and Process Heaters in Petroleum Refineries 
because S -1553 is not a “Unit” as defined by Regulation 9 -10-220.  S -1553 did not have an 
Authority to Construct or Permit to Operate prior to January 5, 2004.   
 
The owner/operator is subject to Regul ation 8, Rule 18.  The natural gas fuel lines and 
components will be constructed in accordance with the requirements of the 8 -18 standards 
and added to the facility fugitive emissions monitoring program.  
 
The project is considered to be ministerial under t he District's CEQA regulation 2 -1-311 and therefore is not subject 
to CEQA review.   
 
The project is over 1000 feet from the nearest school and therefore not subject to the public notification 
requirements of Reg. 2 -1-412. 
 
The owner/operator of S -1553 Backup Boiler shall comply with BACT and NSPS.  
 
Offsets, Toxics, PSD and NESHAPS do not apply.

## conditions
JSONPath: `$.conditions.text`

PERMIT CONDITIONS
IONS   
 
Condition 24491 will be revised as follows:  
 
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  91 November 3 , 2015  Application 20977 (November 2009)  
Modified by Application 22169 (September 2010) .  Added S-1553 and deleted Part 3.  
 
S-1550   Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1550 
SCR  
S-1551   Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1551 
SCR  
S-1553   Backup Steam Boiler #3, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1553 
SCR  
 
1. The owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are fired 
exclusively on natural gas at a rate not to exceed 99 MMBtu/hr each.  (Basis: Cumulative 
Increase, Offsets, Toxics, NSPS, BACT)  
 
2. The owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are on site at the 
refinery for no more that 6 consecutive months per 12 consecutive month period.  The 6 -
month period for each boiler begins upon the initial firing of the boiler.  (Basis:  BA CT) 
 
3. Deleted.  (Application 22169) The owner/operator shall ensure each boiler S -1550 and S -
1551 is not operated for more than 2160 hours in any consecutive 12 -month period.   
(Basis: Cumulative Increase, Offsets, Toxics)  
 
4. Except for a time period not to ex ceed 24 hours per boiler startup or shutdown, the 
owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are only operated when 
abated by SCRs A -1550 , and A-1551  and A -1553 , respectively.  The total cumulative 
hours that all three boilers can be S-1550 or S -1551 is  operated without SCR abatement 
shall not exceed 192 hours per consecutive 12 -month period.  (Basis: Cumulative 
Increase, Offsets, Toxics)  
 
5. The owner/operator shall ensure that S -1550 , and S-1551  and S1553  are not operated 
unless they are e ach equipped with a District approved, fuel flow meter that measures the 
total volume of fuel throughput to S -1550 , and S-1551 and S -1553 in units of standard 
cubic feet.  (Basis: Cumulative Increase, Offsets, Toxics)  
 
6. The owner/operator shall ensure that the total fuel fired in S -1550 , and S-1551 and S -
1553 shall not exceed 4,277,000 therms in any 12 consecutive month period.  (Basis: 
Cumulative Increase, Offsets, Toxics)  
 
7. Except for periods of startup and shutdown as allowed in Part 4, the owner operator shall 
not operate S -1550 , or S-1551 or S-1553 unless NOx emissions are less than 7 ppmv, dry, 
@ 3% O2.  (Basis: Cumulative Increase, Offsets, BACT)  
 
8. During for periods of startup and shutdown as allowed in Part 4, the owner operator shall 
not operate S -1550, or S-1551  or S-1553  unless NOx emissions are less than 30 ppmv, 
dry, @ 3% O2.  (Basis: Cumulative Increase, Offsets)  
 
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  92 November 3 , 2015  9. The owner operator shall not operate S -1550 , or S-1551 or S-1553 unless CO emissions 
are less than 50 ppmv, dry, @ 3% O2.  (Basis: Cumu lative Increase, Offsets, BACT)  
 
10. Within 10 days of the first fire date, the owner/operator shall conduct a District approved 
source test of each S -1550 ,  and S-1551  and S -1553 .  The District approved source test 
shall measure the emission rates of NOx, POC , SO2, and PM10, from S -1550 , and S-
1551  and S -1553  while it is operated at not less than 80 MMBtu/hr.  The owner/operator 
shall ensure that within 45 days of the date of completion of the source testing, two 
identical copies of the source tests results (e ach referencing permit application #20977 , 
#22168,  and plant #14628) are received by the District.  One copy shall be sent to Source 
Testing and the other shall be sent to the Engineering Division.  This District approved 
source test shall be repeated with in 5 days of each subsequent boiler startup (or any 
operation without SCR abatement) during the 6 -month period of boiler operation.  (Basis: 
Cumulative Increase, Offsets, BACT)  
 
11. In a District approved log, the owner/operator shall record the manufacturer, make, 
model, and maximum rated firing rate of each boiler used as S -1550 , and S-1551  and S -
1553 , and the following information for each calendar day that either S -1550 , or S-1551 , 
or S-1553  fires fuel.  The District approved log(s) shall be retained by the owner/operator 
on site for at least 5 years from the date of the last entry and made available to District 
staff upon request.  (Basis: Cumulative Increase, Offsets, Toxics, BACT)  
a. The date  and hours that each S -1550 , and S-1551  and S -1553  fire fuel.  
b. The amount of fuel fired at each S -1550 , and S-1551  and S -1553 . 
c. The hours that each S -1550 , and S-1551  and S -1553  operate without abatement 
by a fully functioning SCR.  
d. The amount of steam produced at each boiler S -1550 , and S-1551  and S -1553 .PERMIT CONDITIONS
IONS   
 
Condition 24491 will be revised as follows:  
 
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  91 November 3 , 2015  Application 20977 (November 2009)  
Modified by Application 22169 (September 2010) .  Added S-1553 and deleted Part 3.  
 
S-1550   Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1550 
SCR  
S-1551   Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1551 
SCR  
S-1553   Backup Steam Boiler #3, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1553 
SCR  
 
1. The owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are fired 
exclusively on natural gas at a rate not to exceed 99 MMBtu/hr each.  (Basis: Cumulative 
Increase, Offsets, Toxics, NSPS, BACT)  
 
2. The owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are on site at the 
refinery for no more that 6 consecutive months per 12 consecutive month period.  The 6 -
month period for each boiler begins upon the initial firing of the boiler.  (Basis:  BA CT) 
 
3. Deleted.  (Application 22169) The owner/operator shall ensure each boiler S -1550 and S -
1551 is not operated for more than 2160 hours in any consecutive 12 -month period.   
(Basis: Cumulative Increase, Offsets, Toxics)  
 
4. Except for a time period not to ex ceed 24 hours per boiler startup or shutdown, the 
owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are only operated when 
abated by SCRs A -1550 , and A-1551  and A -1553 , respectively.  The total cumulative 
hours that all three boilers can be S-1550 or S -1551 is  operated without SCR abatement 
shall not exceed 192 hours per consecutive 12 -month period.  (Basis: Cumulative 
Increase, Offsets, Toxics)  
 
5. The owner/operator shall ensure that S -1550 , and S-1551  and S1553  are not operated 
unless they are e ach equipped with a District approved, fuel flow meter that measures the 
total volume of fuel throughput to S -1550 , and S-1551 and S -1553 in units of standard 
cubic feet.  (Basis: Cumulative Increase, Offsets, Toxics)  
 
6. The owner/operator shall ensure that the total fuel fired in S -1550 , and S-1551 and S -
1553 shall not exceed 4,277,000 therms in any 12 consecutive month period.  (Basis: 
Cumulative Increase, Offsets, Toxics)  
 
7. Except for periods of startup and shutdown as allowed in Part 4, the owner operator shall 
not operate S -1550 , or S-1551 or S-1553 unless NOx emissions are less than 7 ppmv, dry, 
@ 3% O2.  (Basis: Cumulative Increase, Offsets, BACT)  
 
8. During for periods of startup and shutdown as allowed in Part 4, the owner operator shall 
not operate S -1550, or S-1551  or S-1553  unless NOx emissions are less than 30 ppmv, 
dry, @ 3% O2.  (Basis: Cumulative Increase, Offsets)  
 
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, 
Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  92 November 3 , 2015  9. The owner operator shall not operate S -1550 , or S-1551 or S-1553 unless CO emissions 
are less than 50 ppmv, dry, @ 3% O2.  (Basis: Cumu lative Increase, Offsets, BACT)  
 
10. Within 10 days of the first fire date, the owner/operator shall conduct a District approved 
source test of each S -1550 ,  and S-1551  and S -1553 .  The District approved source test 
shall measure the emission rates of NOx, POC , SO2, and PM10, from S -1550 , and S-
1551  and S -1553  while it is operated at not less than 80 MMBtu/hr.  The owner/operator 
shall ensure that within 45 days of the date of completion of the source testing, two 
identical copies of the source tests results (e ach referencing permit application #20977 , 
#22168,  and plant #14628) are received by the District.  One copy shall be sent to Source 
Testing and the other shall be sent to the Engineering Division.  This District approved 
source test shall be repeated with in 5 days of each subsequent boiler startup (or any 
operation without SCR abatement) during the 6 -month period of boiler operation.  (Basis: 
Cumulative Increase, Offsets, BACT)  
 
11. In a District approved log, the owner/operator shall record the manufacturer, make, 
model, and maximum rated firing rate of each boiler used as S -1550 , and S-1551  and S -
1553 , and the following information for each calendar day that either S -1550 , or S-1551 , 
or S-1553  fires fuel.  The District approved log(s) shall be retained by the owner/operator 
on site for at least 5 years from the date of the last entry and made available to District 
staff upon request.  (Basis: Cumulative Increase, Offsets, Toxics, BACT)  
a. The date  and hours that each S -1550 , and S-1551  and S -1553  fire fuel.  
b. The amount of fuel fired at each S -1550 , and S-1551  and S -1553 . 
c. The hours that each S -1550 , and S-1551  and S -1553  operate without abatement 
by a fully functioning SCR.  
d. The amount of steam produced at each boiler S -1550 , and S-1551  and S -1553 .

## permit_conditions
JSONPath: `$.permit_conditions`

Condition number: 24491
- Item 1
The owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are fired 
exclusively on natural gas at a rate not to exceed 99 MMBtu/hr each.  (
Basis: Cumulative 
Increase, Offsets, Toxics, NSPS, BACT)

- Item 2
The owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are on site at the 
refinery for no more that 6 consecutive months per 12 consecutive month period.  The 6 -
month period for each boiler begins upon the initial firing of the boiler.  (
Basis: BA CT)

- Item 3
Deleted.  (Application 22169) The owner/operator shall ensure each boiler S -1550 and S -
1551 is not operated for more than 2160 hours in any consecutive 12 -month period.   
(
Basis: Cumulative Increase, Offsets, Toxics)

- Item 4
Except for a time period not to ex ceed 24 hours per boiler startup or shutdown, the 
owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are only operated when 
abated by SCRs A -1550 , and A-1551  and A -1553 , respectively.  The total cumulative 
hours that all three boilers can be S-1550 or S -1551 is  operated without SCR abatement 
shall not exceed 192 hours per consecutive 12 -month period.  (
Basis: Cumulative 
Increase, Offsets, Toxics)

- Item 5
The owner/operator shall ensure that S -1550 , and S-1551  and S1553  are not operated 
unless they are e ach equipped with a District approved, fuel flow meter that measures the 
total volume of fuel throughput to S -1550 , and S-1551 and S -1553 in units of standard 
cubic feet.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 6
The owner/operator shall ensure that the total fuel fired in S -1550 , and S-1551 and S -
1553 shall not exceed 4,277,000 therms in any 12 consecutive month period.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 7
Except for periods of startup and shutdown as allowed in Part 4, the owner operator shall 
not operate S -1550 , or S-1551 or S-1553 unless NOx emissions are less than 7 ppmv, dry, 
@ 3% O2.  (
Basis: Cumulative Increase, Offsets, BACT)

- Item 8
During for periods of startup and shutdown as allowed in Part 4, the owner operator shall 
not operate S -1550, or S-1551  or S-1553  unless NOx emissions are less than 30 ppmv, 
dry, @ 3% O2.  (
Basis: Cumulative Increase, Offsets)  
 
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  92 November 3, 2015  9. The owner operator shall not operate S -1550, or S-1551 or S-1553 unless CO emissions 
are less than 50 ppmv, dry, @ 3% O2.  (Basis: Cumu lative Increase, Offsets, BACT)

- Item 10
Within 10 days of the first fire date, the owner/operator shall conduct a District approved 
source test of each S -1550 ,  and S-1551  and S -1553 .  The District approved source test 
shall measure the emission rates of NOx, POC , SO2, and PM10, from S -1550 , and S-
1551  and S -1553  while it is operated at not less than 80 MMBtu/hr.  The owner/operator 
shall ensure that within 45 days of the date of completion of the source testing, two 
identical copies of the source tests results (e ach referencing permit application #20977 , 
#22168,  and plant #14628) are received by the District.  One copy shall be sent to Source 
Testing and the other shall be sent to the Engineering Division.  This District approved 
source test shall be repeated with in 5 days of each subsequent boiler startup (or any 
operation without SCR abatement) during the 6 -month period of boiler operation.  (
Basis: Cumulative Increase, Offsets, BACT)

- Item 11
In a District approved log, the owner/operator shall record the manufacturer, make, 
model, and maximum rated firing rate of each boiler used as S -1550 , and S-1551  and S -
1553 , and the following information for each calendar day that either S -1550 , or S-1551 , 
or S-1553  fires fuel.  The District approved log(s) shall be retained by the owner/operator 
on site for at least 5 years from the date of the last entry and made available to District 
staff upon request.  (
Basis: Cumulative Increase, Offsets, Toxics, BACT)  
a. The date  and hours that each S -1550, and S-1551  and S -1553  fire fuel.  
b. The amount of fuel fired at each S -1550, and S-1551  and S -1553 . 
c. The hours that each S -1550, and S-1551  and S -1553  operate without abatement 
by a fully functioning SCR.  
d. The amount of steam produced at each boiler S -1550, and S-1551  and S -1553 .PERMIT CONDITIONS
IONS   
 
Condition 24491 will be revised as follows:  
 
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  91 November 3, 2015  Application 20977 (November 2009)  
Modified by Application 22169 (September 2010) .  Added S-1553 and deleted Part 3.  
 
S-1550   Backup Steam Boiler #1, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1550 
SCR  
S-1551   Backup Steam Boiler #2, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1551 
SCR  
S-1553   Backup Steam Boiler #3, 99 MM Btu/hr, Natural Gas Fired, Abated by A -1553 
SCR

- Item 1
The owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are fired 
exclusively on natural gas at a rate not to exceed 99 MMBtu/hr each.  (
Basis: Cumulative 
Increase, Offsets, Toxics, NSPS, BACT)

- Item 2
The owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are on site at the 
refinery for no more that 6 consecutive months per 12 consecutive month period.  The 6 -
month period for each boiler begins upon the initial firing of the boiler.  (
Basis: BA CT)

- Item 3
Deleted.  (Application 22169) The owner/operator shall ensure each boiler S -1550 and S -
1551 is not operated for more than 2160 hours in any consecutive 12 -month period.   
(
Basis: Cumulative Increase, Offsets, Toxics)

- Item 4
Except for a time period not to ex ceed 24 hours per boiler startup or shutdown, the 
owner/operator shall ensure that S -1550 , and S-1551 and S -1553 are only operated when 
abated by SCRs A -1550 , and A-1551  and A -1553 , respectively.  The total cumulative 
hours that all three boilers can be S-1550 or S -1551 is  operated without SCR abatement 
shall not exceed 192 hours per consecutive 12 -month period.  (
Basis: Cumulative 
Increase, Offsets, Toxics)

- Item 5
The owner/operator shall ensure that S -1550 , and S-1551  and S1553  are not operated 
unless they are e ach equipped with a District approved, fuel flow meter that measures the 
total volume of fuel throughput to S -1550 , and S-1551 and S -1553 in units of standard 
cubic feet.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 6
The owner/operator shall ensure that the total fuel fired in S -1550 , and S-1551 and S -
1553 shall not exceed 4,277,000 therms in any 12 consecutive month period.  (
Basis: Cumulative Increase, Offsets, Toxics)

- Item 7
Except for periods of startup and shutdown as allowed in Part 4, the owner operator shall 
not operate S -1550 , or S-1551 or S-1553 unless NOx emissions are less than 7 ppmv, dry, 
@ 3% O2.  (
Basis: Cumulative Increase, Offsets, BACT)

- Item 8
During for periods of startup and shutdown as allowed in Part 4, the owner operator shall 
not operate S -1550, or S-1551  or S-1553  unless NOx emissions are less than 30 ppmv, 
dry, @ 3% O2.  (
Basis: Cumulative Increase, Offsets)  
 
Permit Evaluation and Statement of Basis:  Site B2758 & B2759, Tesoro Refining & Marke ting Company, LLC, Golden Eagle Refinery, 150 Solano Way, Martinez, CA  94553  
    
Proposed Rev 5 Statement of Basis  92 November 3, 2015  9. The owner operator shall not operate S -1550, or S-1551 or S-1553 unless CO emissions 
are less than 50 ppmv, dry, @ 3% O2.  (Basis: Cumu lative Increase, Offsets, BACT)

- Item 10
Within 10 days of the first fire date, the owner/operator shall conduct a District approved 
source test of each S -1550 ,  and S-1551  and S -1553 .  The District approved source test 
shall measure the emission rates of NOx, POC , SO2, and PM10, from S -1550 , and S-
1551  and S -1553  while it is operated at not less than 80 MMBtu/hr.  The owner/operator 
shall ensure that within 45 days of the date of completion of the source testing, two 
identical copies of the source tests results (e ach referencing permit application #20977 , 
#22168,  and plant #14628) are received by the District.  One copy shall be sent to Source 
Testing and the other shall be sent to the Engineering Division.  This District approved 
source test shall be repeated with in 5 days of each subsequent boiler startup (or any 
operation without SCR abatement) during the 6 -month period of boiler operation.  (
Basis: Cumulative Increase, Offsets, BACT)

- Item 11
In a District approved log, the owner/operator shall record the manufacturer, make, 
model, and maximum rated firing rate of each boiler used as S -1550 , and S-1551  and S -
1553 , and the following information for each calendar day that either S -1550 , or S-1551 , 
or S-1553  fires fuel.  The District approved log(s) shall be retained by the owner/operator 
on site for at least 5 years from the date of the last entry and made available to District 
staff upon request.  (
Basis: Cumulative Increase, Offsets, Toxics, BACT)  
a. The date  and hours that each S -1550, and S-1551  and S -1553  fire fuel.  
b. The amount of fuel fired at each S -1550, and S-1551  and S -1553 . 
c. The hours that each S -1550, and S-1551  and S -1553  operate without abatement 
by a fully functioning SCR.  
d. The amount of steam produced at each boiler S -1550, and S-1551  and S -1553 .

## recommendation
JSONPath: `$.recommendation.text`

RECOMMENDATION
TION  
Waive an Authority to Construct and grant a Permit to Operate to Tesoro Refining and Marketing Company for the 
following source:  
 
 S-1553  Backup Steam Boiler #3, 99 MM Btu/hr, Natural Gas Fired, Abated byRECOMMENDATION
TION  
Waive an Authority to Construct and grant a Permit to Operate to Tesoro Refining and Marketing Company for the 
following source:  
 
 S-1553  Backup Steam Boiler #3, 99 MM Btu/hr, Natural Gas Fired, Abated by 
A-1553 SCR  
 
EXEMPTIONS  
none  
 
 
 
By:  
 Arthur P Valla  
 Senior Air Quality Engineer  
September 16, 2010
