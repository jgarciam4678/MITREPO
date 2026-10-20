**Document control:** Version: 1.0 · Status: Draft · Date: 2026-10-20 · Classification: Confidential · Portfolio: CMS · Type: PROC · Minimum level: L2

| **Document** | **EN-CMS-PROC-PRUEBAS-L8** |
| --- | --- |
| Version | 1.0 |
| Date | 2026-10-20 |
| Classification | Confidential · Minimum level L2 |
| Applies to | Functional validation of CMS Level 8 (alert controls) on an operating mine |

*****

## 1. OBJECTIVE

Validate the performance of the TORSA Collision Management System (CMS) at EMESRT Level 8 in critical mining interaction scenarios, in a controlled and repeatable way. The tests check that the system detects the interaction, generates progressive visual and audible alerts to the operator, and notifies the monitoring platform.

The protocol is part of the formal validation process with the customer. It gives an objective and auditable basis for deciding whether the system can go live.

*****

## 2. SCOPE

This procedure applies to:

- Vehicle-to-vehicle (V2V) interactions between instrumented vehicles on haul roads, curves and intersections
- The digital cleaning request and authorisation flow between an auxiliary vehicle and a shovel
- Vehicle-to-object (V2O) detection of a safety berm, only where the AI camera add-on is installed (optional)

**Does not apply to:**

- Level 9 intervention tests (shovel swing lock, truck braking). They are covered by a separate protocol (see ES-CMS-PROC-ISA-INTERVENCION)
- Interactions with non-instrumented vehicles or pedestrians

*****

## 3. BEFORE STARTING

### 3.1 Key Definitions

| **Term** | **Definition** |
| --- | --- |
| LO (Local Object) | Instrumented vehicle with the greater capacity to manoeuvre or the primary responsibility for mitigating the risk in an interaction |
| RO (Remote Object) | Vehicle involved in the interaction whose preventive capacity is secondary to the LO |
| V2V (Vehicle-to-Vehicle) | Interaction between two instrumented vehicles |
| V2O (Vehicle-to-Object) | Interaction between an instrumented vehicle and an object, including a dump edge or safety berm detected by cameras |
| Level 8 (EMESRT) | Alert controls: the system warns the operator and notifies the platform |
| Level 9 (EMESRT) | Intervention controls: the system acts on the vehicle to avoid or mitigate a collision |
| EMESRT | International reference organisation in mining safety that defines the hierarchy of controls for collision systems |

### 3.2 Equipment and Materials

| **Item** | **Specification** | **Notes** |
| --- | --- | --- |
| Instrumented vehicles | Trucks, auxiliary vehicle (tractor) and shovel, as required by each scenario | CMS installed, commissioned and registered on the platform |
| Cones and markers | As shown in the layouts of Annexes A to G | Distances marked from 0 m |
| Communications | V2V communication between vehicles; platform connection | Verified before each scenario |
| Recording | Event logging active on the vehicles and on the platform | Needed for the evidence of each repetition |
| Radio | Link between TORSA supervisor, mine supervisor and operators | Test perimeter control |

### 3.3 Roles and Responsibilities

| **Role** | **Responsibility** |
| --- | --- |
| TORSA supervisor | Technical execution and documentary support |
| Mine supervisor | Validation in the field |
| Operator | Controlled driving |
| Safety | Authorisation and perimeter control |
| QA | Consolidation of metrics and final report |

### 3.4 General Rules

- The supervisor follows each test and makes sure it is **repeated at least three times**.
- Test speeds can be adjusted to the operating requirements of each customer.
- Before each scenario, confirm that the vehicles are registered and communicating.

> ⚠️ **NOTE**: Distances and speeds below are reference values. Agree them with the customer's safety area before starting.

*****

## 4. EXECUTION

### 4.1 V2V: Haul Roads (Straight)

**Test L1: Head-on approach (Annex A)**

*Objective:* validate detection and alert progression for a frontal approach. *Equipment:* LO = truck; RO = truck (stationary). *Initial separation:* 100 m. *LO speeds:* 10, 20 and 30 km/h.

| **Step** | **Action** | **Expected Result** |
| --- | --- | --- |
| 4.1.1 | Confirm V2V communications | Both vehicles visible to each other |
| 4.1.2 | Position LO and RO | Vehicles at the initial separation |
| 4.1.3 | LO advances at a stable speed | Progressive alerts to the LO operator before the vehicles meet |
| 4.1.4 | Repeat 3 times for each speed | Alert levels and distances recorded per repetition |

{{FIG:A}}

**Test L2: Reversing (Annex B)**

*Objective:* validate detection of the RO during reversing manoeuvres. *Equipment:* LO = truck (reversing); RO = stationary truck behind. *Initial separation:* 100 m. *LO reversing speeds:* 5 and 10 km/h.

| **Step** | **Action** | **Expected Result** |
| --- | --- | --- |
| 4.1.5 | Start recording | Event logging active |
| 4.1.6 | LO starts reversing; the operator monitors alerts | Progressive alerts to the operator while approaching the RO |

{{FIG:B}}

**Test L5: Passing head-on (Annex C)**

*Objective:* validate detection of a vehicle crossing on parallel roads in opposite directions. *Equipment:* LO = truck; RO = truck.

| **Step** | **Action** | **Expected Result** |
| --- | --- | --- |
| 4.1.7 | LO and RO keep 20 km/h at 100 m frontal separation | Detection and alerts according to the configuration |
| 4.1.8 | LO and RO keep 20 km/h at 5 m and 10 m lateral separation | Lateral separation evaluated; alerts consistent with the configured zones |

{{FIG:C}}

### 4.2 V2V: Curves and Reduced Visibility

**Test C1: Head-on curve (Annex E)**

*Objective:* anticipate and alert before direct visibility. *Equipment:* LO = truck; RO = stationary truck. Place the vehicles at the ends of a curve without line of sight. *LO speeds:* 10, 20 and 30 km/h.

| **Step** | **Action** | **Expected Result** |
| --- | --- | --- |
| 4.2.1 | Both vehicles advance until they meet; evaluate the first instant of warning | First warning recorded |
| 4.2.2 | Record whether the warning occurs before the operators have direct vision | Warning before direct visibility |

{{FIG:E}}

### 4.3 Intersections and Crossings

**Test T4: 90° intersection (Annex D)**

*Objective:* validate the crossing-priority calculation and alert prioritisation at a 90° crossing. *Equipment:* LO = crossing vehicle; RO = main road vehicle. Place the vehicles more than 100 m from the crossing. *Speeds:* 10, 20 and 30 km/h.

| **Step** | **Action** | **Expected Result** |
| --- | --- | --- |
| 4.3.1 | LO approaches with the intention of crossing; RO keeps its speed | Alerts prioritised according to who has priority |
| 4.3.2 | Record the moment of each alert level | Level timings recorded |

{{FIG:D}}

**Test R2: Cleaning flow, request and authorisation (Annex F)**

*Objective:* validate the digital authorisation for the cleaning tractor.

| **Step** | **Action** | **Expected Result** |
| --- | --- | --- |
| 4.3.3 | Tractor (LO) requests permission from the CMS screen | Request reaches the shovel |
| 4.3.4 | Shovel operator receives the request and denies it | Request denied |
| 4.3.5 | Validate that, without approval, the tractor receives an alert and does not enter | Alert to the tractor |
| 4.3.6 | Tractor (LO) requests permission again | Request reaches the shovel |
| 4.3.7 | Shovel operator receives the request and approves it | Request approved |
| 4.3.8 | Validate that, if the tractor enters the risk zone, the shovel receives an alert | Alert to the shovel operator |

{{FIG:F}}

### 4.4 V2O: Safety Berm (Optional)

**Test O1: Reversing toward a berm (Annex G)**

*Objective:* validate distance measurement and alerts when reversing toward a berm. Only where the AI camera add-on is installed. *Speeds:* 5 and 10 km/h, reversing. Three repetitions per speed. Record at cones placed at 15, 10 and 5 m.

| **Step** | **Action** | **Expected Result** |
| --- | --- | --- |
| 4.4.1 | Truck reverses toward the berm at the test speed | Berm detected and distance measured |
| 4.4.2 | Record the alert at the cones at 15, 10 and 5 m | Progressive alerts as the distance decreases |

{{FIG:G}}

*****

## 5. VALIDATION

### 5.1 Performance Criteria (KPIs)

| **KPI** | **Target** |
| --- | --- |
| Effectiveness of V2V alert detection | ≥ 95 % |
| Effectiveness of V2O alert detection (optional module) | ≥ 90 % |
| Alert latency to the operator | ≤ 1 s |
| Cleaning requests sent successfully | ≥ 95 % |

> ⚠️ **NOTE**: KPIs are measured only during functional tests.

### 5.2 Verification Checklist

|  | **Verification** | **GO** | **NO-GO** |
| --- | --- | --- | --- |
| 1 | L1: three repetitions per speed with progressive alerts | ☐ | ☐ |
| 2 | L2: alerts while reversing at 5 and 10 km/h | ☐ | ☐ |
| 3 | L5: detection at frontal and lateral separations | ☐ | ☐ |
| 4 | C1: warning before direct visibility | ☐ | ☐ |
| 5 | T4: alert prioritisation at the crossing | ☐ | ☐ |
| 6 | R2: denial, approval and risk-zone alerts | ☐ | ☐ |
| 7 | O1 (if applicable): alerts at 15, 10 and 5 m | ☐ | ☐ |
| 8 | Events notified to the platform | ☐ | ☐ |
| 9 | KPIs met | ☐ | ☐ |

*****

## 6. IF IT FAILS

| **Symptom** | **Probable Cause** | **Corrective Action** | **Verification** |
| --- | --- | --- | --- |
| A vehicle is not seen by the other | Missing registration or dimensions in the local configuration; system or communication fault | Check both configuration entries and the system status messages | Vehicle detected |
| Registered vehicle seen but no alert | Alert evaluation or configured parameters | Review the evaluation on the display and the parameters with the CMS specialist | Alert generated |
| Local alerts without records on the platform | Sending or communications to the platform | Check the platform communication | Events visible on the platform |
| KPI not met | Parameters or positioning conditions | Review the configuration with the CMS specialist and repeat the scenario | KPI met |

*****

## 7. TENTATIVE SCHEDULE

Reference schedule for a Level 8 phase with one shovel, one tractor and two trucks. Durations depend on the fleet and the site.

| **Activity** | **Owner** | **W1** | **W2** | **W3** | **W4** | **W5** | **W6** | **W7** | **W8** | **W9** | **W10** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pre-installation reports | Installation team | ■ | ■ | ■ | ■ |  |  |  |  |  |  |
| Support design | Installation team | ■ | ■ | ■ | ■ |  |  |  |  |  |  |
| Material delivery | TORSA project manager | ■ | ■ | ■ | ■ |  |  |  |  |  |  |
| Platform deployment | Infrastructure | | | ■ | ■ |  |  |  |  |  |  |
| Pre-configuration | Installation team |  |  | ■ | ■ |  |  |  |  |  |  |
| Shovel installation | Installation team |  |  |  |  | ■ |  |  |  |  |  |
| Tractor installation | Installation team |  |  |  |  |  | ■ |  |  |  |  |
| Truck installation (x2) | Installation team |  |  |  |  |  |  | ■ |  |  |  |
| Commissioning | CMS specialist |  |  |  |  | ■ | ■ | ■ |  |  |  |
| Validation and phase close (this protocol) | Installation team / CMS specialist |  |  |  |  |  |  |  | ■ | ■ | ■ |

*****

## ANNEX A to G: TEST LAYOUTS

The reference layouts for scenarios L1, L2, L5, T4, C1, R2 and O1 are included in the PDF version of this document.

## ANNEX H: TEST RECORD FORMAT

| **Scenario** | **Repetition** | **LO speed (km/h)** | **Separation (m)** | **First alert (m / s)** | **Alert level reached** | **Platform notification** | **Result (GO / NO-GO)** |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | 1 |  |  |  |  | ☐ |  |
|  | 2 |  |  |  |  | ☐ |  |
|  | 3 |  |  |  |  | ☐ |  |

*****

## 8. REVISION CONTROL

| **Version** | **Date** | **Prepared by** | **Approved by** | **Changes** |
| --- | --- | --- | --- | --- |
| 1.0 | 2026-10-20 | TORSA Engineering | — | Generic CMS L8 protocol, anonymised from a customer test protocol; L9 tests removed; tentative schedule added |

*****

**End of document**

*TORSA Worldwide S.L. - Severo Ochoa, 19 - Parque Tecnológico de Andalucía - 29590 Málaga, Spain*
