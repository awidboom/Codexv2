---
application_number: 12975
plant_name: Chevron USA, Inc. has applied for a CARB-certifie d diesel engine (S-7013), which will be used
plant_address: 841 Chevron Way
evaluation_date: October 6, 2005
source_pdf: C:\Users\aaw\Codex\BAAD Engr Evals\Chevron SOBs\extracted_evaluations\application_12975.pdf
source_json: data/permit_evaluations_json/Chevron/application_12975__eval.json
---

# Engineering Evaluation (Application 12975)
**Plant**:  Chevron USA, Inc. has applied for a CARB-certifie d diesel engine (S-7013), which will be used
**Address**: 841 Chevron Way
**Evaluation Date**: October 6, 2005

## background
JSONPath: `$.background.text`

BACKGROUND
D
 
 Chevron USA, Inc. has applied for a CARB-certifie d diesel engine (S-7013), which will be used 
to power a standby generator at their 841 Chevron Way, Richmond, CA refinery.   S-7013 SRU Stationary Standby Generator Set:  Diesel Engine; Make:  Cummins; Model:  
QSX15-G9; Rated Horsepower:  750 HP

## emission_calculations
JSONPath: `$.emission_calculations.text`

EMISSIONS
S
 
 Annual Average Emissions:  
 Basis:          -  750 hp output rating 
- 50 hr/yr operation for testing and maintenance (ATCM limit)  - NOx, VOC, CO and PM10 emission factors from CARB certification data:   
  NOx:  4.463 g/hp-hr   VOC:  0.235 g/hp-hr (assume all POC compounds)   CO:  0.447 g/hp-hr   P M
10:             0.075 g/hp-hr 
   SO2 emission factor is from EPA AP- 42, Table 3.4-1 ("Large Stationary Diesel 
and Dual-Fuel Engines"), which is based on full conversion of fuel sulfur to SO2 
and which will therefore be considered applicable to any diesel engine (sulfur content will be assumed to be the California limit of 0.05 wt% sulfur): 
   S O
2:  8.09E-3(0.05) lb/hp-hr (454 g/lb) = 0.184 g/hp-hr 
 NOx:  (50 hr/yr)(750 hp)(4.463 g/hp-hr)(lb/454 g)/(365 day/yr) = 368.65 lb/yr = 0.185 TPY 
 POC:  (50 hr/yr)(750 hp)(0.235 g/hp-hr)(lb/454 g)/(365 day/yr) = 19.40 lb/yr = 0.010 TPY  
 CO: (50 hr/yr)(750 hp)(0.447 g/hp-hr)(lb/454 g)/(365 day/yr) = 36.96 lb/yr = 0.018 TPY  
 PM10: (50 hr/yr)(750 hp)(0.075 g/hp-hr)(lb/454 g)/(365 day/yr)  = 6.16 lb/yr = 0.003 TPY 
 SO2:  (50 hr/yr)(750 hp)(0.184 g/hp-hr)(lb/454 g)/(365 day/yr) = 15.20 lb/yr = 0.008 TPY 
 Daily Emissions:  
 Daily emissions are calculated to establish whet her a source triggers the requirement for BACT 
(10 lb/highest day total source emissions for any class of pollutants). 24-hr/day operation will be 
assumed since no daily limits are imposed on intermittent and unexpected operations.  NOx:  (24 hr/day)(750 hp)(4.463 g/hp-hr)(lb/454 g) = 176.95 lb/day  
 POC:  (24 hr/day)(750 hp)(0.235 g/hp-hr)(lb/454 g) = 9.31 lb/day  
 CO: (24 hr/day)(750 hp)(0.447 g/hp-hr)(lb/454 g) = 17.74 lb/day  
 PM10:  (24 hr/day)(750 hp)(0.075 g/hp-hr)(lb/454 g) = 2.96 lb/day  
 SO2:  (24 hr/day)(750 hp)(0.184 g/hp-hr)(lb/454 g) = 7.30 lb/day

## cumulative_increase
JSONPath: `$.cumulative_increase.text`

(empty)

## toxic_risk_screening_analysis
JSONPath: `$.toxic_risk_screening_analysis.narrative`

TOXIC RISK SCREENING ANALYSIS
YSIS  
 
The cancer risk is calculated based on the emissi on rate of diesel exhaust particulate matter. 
Diesel exhaust particulate matter is used as a su rrogate for all toxic contaminants found in diesel 
exhaust. Because the proposed emissions exceed the risk screening trigger level for diesel 
exhaust particulate matter in Table 2-5-1, a risk screening was performed.   Per the attached October 6, 2005 memo from Daphne  Chong, District Toxicologist, results from 
the health risk screening analysis indicate that the maximum cancer risk is estimated at 0.3 in a 
million if the engine were to run for 50 hours/ year. In accordance with the District’s Risk 
Management Policy, this risk level is considered acceptable.

## BACT
JSONPath: `$.BACT.text`

BACT
BACT is triggered for NOx and CO as maximum daily emissions exceed 10 lb/day, as calculated 
on page 1 (Daily Emissions).   BACT for th is source is presented in the current BAAQMD 
BACT/TBACT Workbook for this source category as shown below:  
Source:  IC En gine - Compression Ignition  Revision:  5 
  Document #:  96.1.2  
Class:  > or = 175 horsepower output rating  Date: 01/11/02  
Determination

## offsets
JSONPath: `$.offsets.narrative`

OFFSETS
TS
 
 Offsets are required for POC, NOx, and PM10.  Per the instructions received from Chevron, 
Certificate of Deposit 904 will be used to provide the offsets needed for this application.  POC = 0.01 TPY x 1.00 = 0.01 TPY NOx = 0.185 TPY x 1.15 = 0.213 TPY PM10 = 0.003 TPY x 1.15 = 0.003 TPY  STATEMENT OF COMPLIANCE
 
 S-7013 will be operated as an emergency standby e ngine and therefore is not subject to the 
emission rate limits in Regulation 9, Rule 8 ("NOx  and CO from Stationary Internal Combustion 
Engines"). S-7013 is subject to the monitoring a nd record keeping requirements of Regulation 9-
8-530 and the SO2 limitations of 9-1-301 (ground- level concentration) and 9-1-304 (0.5% by 
weight in fuel). Regulation 9-8-530 requirement s are incorporated into the proposed permit 
conditions. Compliance with Regulation 9-1 is ve ry likely since diesel fuel with a 0.05% by 
 4weight sulfur is mandated for use in California.  Like all combustion sources, S-7013 is subject to 
Regulation 6 ("Particulate and Vi sible Emissions"). This engine is not expected to produce 
visible emissions or fallout in violation of this regulation and will be assumed to be in 
compliance with Regulation 6 pending a regular inspection.  This application is considered to be minist erial under the District's Regulation 2-1-311 and 
therefore is not subject to CEQA review.  The e ngineering review for this project requires only 
the application of standard permit conditions a nd standard emission factors in accordance with 
Permit Handbook Chapter 2.3.  This facility is over 1,000 feet from  the nearest school and therefore is not subject to the public 
notification requirements of Regulation 2-1-412.  PSD, NSPS and NESHAPS are not triggered.   PERMIT CONDITIONS
 
 
1. The owner or operator shall operate each emergency standby engine only for the 
following purposes:  to mitigate emergency conditions, for emission testing to demonstrate compliance with a District, state or Federal emission limit, or for reliability-related activities (maintenance and other testing, but excluding emission testing).  Operating while mitigating emergency conditions or while emission testing to show compliance with District, state or Federal emission limits does not have an annual hourly limit.  Operating for reliability-related activities is limited to 50 hours per year per emergency standby engine. 
 
(Basis:  “Stationary Diesel Engine ATCM” section 93115, title 17, CA Code of Regulations, subsection (e)(2)(A)(3) 
 
2. The owner/operator shall operate each emergency standby engine only when a non-
resettable totalizing meter (with a minimum display capability of 9,999 hours) that measures the hours of operation for the engine is installed and properly maintained. 
 
(Basis: “Stationary Diesel Engine ATCM” section 93115, title 17, CA Code of Regulations, subsection (e)(4)(G)(1)                            
 3. Records: The owner/operator shall maintain the following monthly records in a District-
approved log for at least 36 months from the date of entry.  For Title V facilities, the following monthly records shall be maintained for 5 years.  Log entries shall be retained on-site, either at a central location or at the engine’s locations, and made immediately available to the District staff upon request.   
a. Hours of operation for reliability-related activities (maintenance and testing). b. Hours of operation for emission testing to show compliance with emission limits. c. Hours of operation (emergency). d. For each emergency, the nature of the emergency condition. e. Fuel usage for engine(s).   
 (Basis: “Stationary Diesel Engine ATCM” section 93115, title 17, CA Code of Regulations, Regulation 1-441) 
 
 54. The owner or operator shall not operate each stationary emergency standby diesel-fueled 
engine for non-emergency use, including maintenance and testing, during the following periods:  a. Whenever there is a school sponsored activity (if the engine is located on school grounds) b. Between 7:30 a.m. and 3:30 p.m. on days when school is in session (if the engine is 
located within 500 feet of school grounds). 
 
(Basis:  “Stationary Diesel Engine ATCM” section 93115, title 17, CA Code of Regulations, subsection (e)(2)(A)(1)

## PSD_applicability
JSONPath: `$.PSD_applicability.narrative`

(empty)

## CEQA
JSONPath: `$.CEQA.narrative`

(empty)

## Statement_of_Compliance
JSONPath: `$.Statement_of_Compliance`

### General

## public_notification
JSONPath: `$.public_notification.text`

(empty)

## conditions
JSONPath: `$.conditions.text`

(empty)

## permit_conditions
JSONPath: `$.permit_conditions`

(empty)

## TitleV_permit
JSONPath: `$.TitleV_permit.narrative`

(empty)

## recommendation
JSONPath: `$.recommendation.text`

RECOMMENDATION
TION  
 Waive the Authority to Construct and Issue the Permit to Operate to Chevron USA for for:  S-7013 SRU Stationary Standby Generator Set:  Diesel Engine; Make:  Cummins; Model:  
QSX15-G9; Rated Horsepower:  750 HP 
   By:  ______________________________     Date:  ___________ 
 Barry G. Young 
 Supervising Air Quality Engineer
