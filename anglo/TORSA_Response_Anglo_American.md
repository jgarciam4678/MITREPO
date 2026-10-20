# TORSA – Response to Anglo American Technical Queries

*Augmented Operation: Interaction Analysis (CMS) and Operator Behaviour & Attention (FAS)*

## Introduction

At TORSA we do not see collision avoidance and fatigue detection as separate products. We address them together under our **Augmented Operation** concept: a portfolio of technologies that gives the mine control of its critical risks and helps the operator through the shift.

**Interaction Analysis (CMS).** Our Collision Management System does not aim only to avoid collisions. It aims to avoid the *situations of risk* that can end in a collision. To do that, we need to know in detail how heavy equipment interacts with other equipment: speeds, directions, gradients, vehicle types, activities and traffic priorities. That is why we speak of Interaction Analysis, not just collision avoidance.

**Operator Behaviour & Attention (FAS).** Our fatigue system is not only an anti-fatigue tool. It evaluates the operator's behaviour and level of attention to the operation: drowsiness, distraction and the way the vehicle is being driven.

**Protocol compliance.** In both systems, we also evaluate whether the operator is working under the mine's own protocols. When these protocols are followed, risk drops substantially.

**Reporting that triggers action.** Our reporting is designed to trigger concrete actions: a corrective action if an alert reveals a breach, or a correction of the system if it reveals a definition or algorithm error. We do not want large volumes of empty information.

This document answers your queries for Level 9 intervention (Part A) and the Fatigue and Attention System (Part B).

---

# Part A – Interaction Analysis and Level 9 Intervention (CMS)

### A1. What was the pilot-to-scale path, and how long did it take?

We run two phases in parallel.

**Technical deployment**

1. We install the system in **shadow mode**, collecting data without alerting the operator, until we identify the baseline.
2. We carry out manoeuvres in a controlled environment with the operators to demonstrate how the system works.
3. Once validated and with a clear baseline, we install the full fleet in shadow mode, collecting data from the whole fleet.
4. Go-live.

**Consultancy with the customer (in parallel)**

We analyse your Traffic Management Plan in detail to characterise the algorithm. This covers everything from traffic priorities to the behaviour of the system in risky interactions, such as floor cleaning around shovels. In doing so we bring to your site the many developments we have made with other customers by taking their needs into real field conditions in an effective and robust way.

**[PENDING: typical duration of each phase.]**

### A2. What are the false-intervention and nuisance-alarm rates, and how are they tuned?

Our MOSH certificate, issued through the University of Pretoria, guarantees that the system alerts when it must alert, as demonstrated by the *Surface CxD Detection and Tracking* and *CxD Effective Warning* requirements.

For operations beyond those validated in the certificate, and after the consultancy phase described in A1, we analyse the alerts generated. We combine objective data (recorded by the system) with subjective data (the operator's opinion). Each type of alert must trigger an action: a corrective action if it is a protocol breach, or a correction if it is a definition or algorithm error. Our goal is operational excellence and **zero false alerts**.

### A3. What happened to cycle time and productivity after intervention went live?

We cannot share specific customer data. What we can say is that our solution uses a different strategy: **our system does not perform abrupt stops**, just as a person does not brake abruptly in their own car.

The system acts on the accelerator, inhibiting it, or on the accelerator and the retarder. The result is a subtle reduction in speed that the operator barely perceives and that has no notable effect on production.

We do not hold customer reports of productivity loss. During shadow mode we can analyse the interventions we would have made on your trucks. We can also run simulations on our simulators so that you see first-hand how the system acts without causing discomfort or affecting production. The simulators are easy to move and install, and can be set up in your offices.

### A4. What is the sensing architecture, and how does it handle dust, GNSS shadow and pit walls?

Our base system combines GPS with our advanced **dead-reckoning** system to determine both own and remote vehicle position. Vehicle-to-vehicle (V2V) communication provides the interaction data between equipment.

We also have additional technologies for specific risks: **3D LiDAR with AI cameras** for vehicle-to-pedestrian (V2P) and vehicle-to-object (V2O) interactions, and **personal tags**, available from 2027.

Our system is certified by MOSH from the Base version, so the certification covers the base system and a variety of interactions: not only truck–truck or truck–light vehicle, but also clearance requests between a front-end loader and a shovel, and speed limits through geofences.

**[PENDING: specific handling of dust, rain, snow, GNSS shadow and pit walls, to be provided by the GNSS/engineering team.]**

### A5. Who approves the machine-side intervention, and how does the OEM keep control of warranty and the safety case?

TORSA holds the University of Pretoria certification for **ISO/TS 21815-2**, which defines the communication interface with the vendor's braking module. Where the OEM or a third-party module is used, the intervention is executed by that module, so the OEM keeps control of it.

Where the TORSA ISA module is required, the particular conditions are negotiated with you.

### A6. What is the fail-safe behaviour when the system or communications fail?

From the collision-management side, the system operates according to MOSH requirements.

For the ISA module, if it fails it becomes "invisible": it returns control to the operator and notifies the operator of the failure. After this type of event, the action protocol for unprotected equipment, in addition to what MOSH specifies, is analysed in detail with the operation.

How each module becomes invisible depends on the specific vehicle. So that you have all the information, we share an intervention manual with the customer. We attach one as an example.

### A7. How does it integrate with FMS, dispatch and OT networks?

Our system operates **independently of the network**. The network is used for reporting and as an additional communication path, but not as the only one.

There are several routes for FMS integration. With Modular Mining we can do a native integration, because we have access to the Modular API. Where no API is available, we can use exchange files on the server.

### A8. What is the local presence in Johannesburg and the Northern Cape: spares, field engineers, response times?

We have our own office in Johannesburg with specialised staff, and an authorised partner in the Northern Cape. We also have engineering offices in Spain and Peru, and soon in Argentina, Chile, Colombia, Australia and Saudi Arabia.

### A9. How would it work in a mixed-OEM fleet with legacy equipment?

Yes. Our Level 8 works on all vehicle types. For Level 9, our braking module also works across vehicle types. We share the inventory of vehicles for which we have a module. Our team designs the module for each specific vehicle, carries out an intervention analysis and shares that information with the customer. This covers everything from modern vehicles to older vehicles with pneumatic braking circuits.

### A10. How does it align with MOSH, MHSA requirements and ICMM commitments?

We hold the MOSH certification, attached to this document.

**[PENDING: wording on MHSA requirements and ICMM commitments.]**

### A11. Is there a local South African reference site, and can we speak to its operators?

Yes. We can share contacts at operations in South Africa.

### A12. What pilot scope, success criteria and go/no-go gates are recommended/possible?

We share references of pilots with anonymised data. The phases in A1 provide the natural gates: baseline established, controlled manoeuvres validated, fleet-wide shadow data, and go-live.

### A13. Who owns the event data, and can it feed our analytics platform?

The data belongs to the customer. We can provide it in several ways: ready to use on our **TORSA Cloud** platform, through an **API**, or through a **Data Lake**.

### A14. Which specific machine makes and models in South Africa have you commissioned with Level 9 slow-down/stop in production that meets MHSA Regulation 8.10 requirements? Please list site, OEM, model, and go-live date.

We have several projects being installed and in test run, with the aim of having the operations commissioned in **Q1 2027**. In these projects we have installed our collision-management system and connected it to the braking modules of various manufacturers. That is why we hold so many certifications.

**[PENDING: list of sites, OEMs and models, if the customer wants it by name.]**

### A15. Is Level 9 delivered through the native ISO/TS 21815-2 interface, your ISA module, or a third-party Machine Interface Controller? Who supplies and warrants each?

We offer both options.

- **Native ISO 21815-2 interface** (certified by the University of Pretoria), where the intervention module is available from the manufacturer or from a third party compliant with the ISO. TORSA is responsible for generating and sending the alert signal; the customer is responsible for having the intervention module.
- **TORSA ISA module**, for vehicles without such an intervention module. It is designed to the type and model of the vehicle and works in constant communication with the manufacturer. In this case TORSA supplies the solution from the assessment of the risk situation to the intervention on the vehicle itself.

### A16. If the CMS-to-machine-controller link fails mid-shift, what is the fail-safe state? Does the machine stop, slow, or continue with a fault alert, and how is this logged for the mine's risk assessment?

According to ISO 21815, when the connection with the machine controller is lost, a **controlled emergency stop** is carried out. The situation must be assessed together with your safety committee, so that by location or activity the response is kept or the override is enabled.

See also A6 for the behaviour of the ISA module.

### A17. How are stopping distances validated for loaded haul trucks on ramps and wet roads? Do slow-down and stop zones adjust dynamically for speed, payload and gradient?

Yes. The base CMS performs a dynamic analysis using the formulas of **Atkinson** and **Kaufman & Ault**, taking into account speed, direction, gradient, vehicle dimensions, vehicle type and the probability of visibility with respect to the other vehicle.

The TORSA CMS is multimodal: the vehicle type and model, and the activity it is carrying out, are considered when assessing the interaction risk.

Add-ons increase the information on the vehicle context: connection to the weighing system, CAN bus interface, and assessment of operator attention or distraction (FAS).

### A18. What override or bypass functions exist (for recovery, maintenance, or tramming), who can authorise them, and are all bypass events logged and reportable?

Recovering control of the vehicle is as important as the intervention. The **override** function lets the operator carry out the movements needed to make sure the vehicle is out of collision risk. The safety protocol and governance of recovering control are defined by the customer's safety committee.

- **Road-risk cases:** the operator recovers control with their operating credentials. It makes no sense to add bureaucracy to the return to operation when the machine is working and generating more risk. The operator must know that they can return to operation.
- **Vehicle in the workshop for maintenance:** a business rule by location gives movement control to the maintenance team.

Everything is recorded before, during and after each incident and activity, and sent to the platform for analytics.

### A19. Does Level 9 apply to vehicle-to-pedestrian interactions as Reg 8.10 requires, or only vehicle-to-vehicle? What pedestrian tag or detection technology triggers the intervention?

The system analyses V2V situations with every instrumented vehicle. On top of the base kit we have accessories for V2O and V2P detection: **LiDAR, AI cameras and personal tags** (from 2027). All risk events detected with these add-ons can be escalated to Level 9 intervention.

### A20. How do you handle older machines without CAN or electronic controls?

TORSA provides detailed engineering for vehicles without electronic controls or CAN bus. We share a sample intervention manual we have developed.

### A21. What is the liability and responsibility split between TORSA, the OEM, and the mine if a Level 9 intervention fails or causes an incident (for example, a sudden stop on a ramp)?

**[PENDING: to be answered with legal.]**

### A22. Has any DMPR inspector or Section 54 investigation reviewed a TORSA Level 9 installation? If so, what was the outcome?

**[PENDING: to be answered with legal.]**

### A23. Is there a hardware and software as a service option?

Yes, a service-type solution is possible. The details must be reviewed between the parties.

### A24. What local support, spares holding and technician presence do you have in South Africa and what are your guaranteed response times there?

We have an office in Johannesburg with an established structure and set service levels for the operations already implemented (Level 8 implementations, with the upgrade to Level 9 in Q1 2027). We also have warehouses and spare-parts stock. Spares holding and the corresponding SLAs will be negotiated when the contract is concluded.

### A25. Has any company implemented using completely tag-less features?

**[PENDING: to be answered. Context: V2P detection with LiDAR and AI cameras is available as an add-on; personal tags from 2027.]**

### A26. What are TORSA's future digital mining objectives?

TORSA's objective is to be the technology partner of mining companies that commit to safety, walking together towards autonomy.

The Augmented Operation portfolio delivers the technological capabilities to control critical risks: interaction between industrial vehicles, cab conditions (drowsiness, distraction) and environmental conditions (particles, noise, gases, temperature), among others. We will add more as a normal evolution (GETS, Truck Spotting, Traffic Management, FMS), until we reach real autonomy between different types of vehicles, ensuring a proper transition with the communities.

---

# Part B – Operator Behaviour & Attention (FAS)

### B1. How does the infrared camera cope with night shifts, sun glare, dust, vibration, sunglasses, glasses and masks?

We start with how event detection in the cab works. The system does not depend on a single detection model: we use **[PENDING: number]** models in parallel, which lets us identify events with high reliability in different contexts. For example, to detect fatigue we do not rely only on eye opening but also on posture, yawning and hand movement. Even when the operator wears accessories, the risk analysis is still possible.

For night shifts we use infrared LEDs, which solve visibility with dark glasses and masks. The system has accumulated more than **750,000 operating hours** in real operating scenarios, on different vehicle types, exposed to vibration, sun glare and dust, evaluating cab events correctly.

### B2. The custom AI model is trained per environment and operator. How much site data and calibration time does it need, and how does it behave with new operators?

Our FAS has models trained for risk assessment in the cab. There are two important points: model training and calibration of the attention window.

- **Training** incorporates the new context of the environment. We do it proactively to maintain and continuously improve the model at each site (for example, to take account of the regional physiology of operators).
- **Calibration** defines the operator's attention window. It is carried out during commissioning and after each major vehicle maintenance, to make sure the configured parameters hold.

For a new implementation we need a **"white-run" period of two weeks of data** to train the models and make the adjustments needed for go-live.

### B3. How does it distinguish true microsleeps from normal glances (mirror checks, dispatch screen)?

As explained in B1, the model does not evaluate only the eyes. It takes into account posture relative to the attention window, vehicle speed and how long the action lasts.

The system confirms a state only after a sustained pattern across consecutive frames, not from a single image. This separates a task that belongs to the activity (turning the vehicle requires looking at the mirror for a few seconds, but not keeping the gaze to the right for two minutes) from a microsleep (eye closure, yawning, face position).

### B4. How do the progressive alerts escalate, and what happens if the operator ignores them?

The system offers an audible alert, visual signals and escalation to notification by email, SMS or call to the security contacts defined. The alert types, escalation and notification of key users are defined in the FAS protocol during site commissioning. Escalation can be integrated with Level 9 vehicle intervention if the customer requests it.

### B5. Does it ever act on the machine (speed limit, parking), or only alert and report? Is a link to L9 intervention planned?

The TORSA system integrates with the ISA vehicle-intervention system. Depending on the level of attention, it can reduce speed and stop the vehicle.

If it is integrated with the TORSA CMS, the attention level becomes a parameter in the analysis of interaction conditions between vehicles. In this way all TORSA solutions interoperate and feed each other to assist the operator during the shift.

### B6. Who gets real-time notifications (supervisor, control room), and what is the expected response protocol?

The system carries out the in-cab actions needed to recover the operator's attention (visual and audible alerts). Escalation to a supervisor uses the channel agreed with the customer (SMS, call, email) and triggers the response protocol defined together with the safety committee.

It is essential that the customer leads the definition of this response protocol. TORSA will advise on its definition or comply with the existing protocol, but it will not be TORSA's sole responsibility to define and implement it. The protocol lives and matures within the customer's organisational culture, so its implementation is the safety committee's responsibility. TORSA's FAS is the management tool on which the response protocol operates. Real-time visibility on the platform depends on network quality.

### B7. Is video stored or only event clips, where, for how long, and who can view it?

Alert records are supported by visual evidence (video) that is stored locally on the on-board equipment. Viewing it on the platform depends on the data-security rules of the region and the customer, and its availability depends on network availability and quality.

As standard we offer:

- **3 months** of hot data persistence,
- **5 years** of backup of the alert tables,
- **1 year** of backup of multimedia events (alert clips).

If the customer wants different retention and security terms, this must be requested during project definition and budgeting. Who can view the footage is described in B15.

### B8. How do facial recognition and biometric processing comply with GDPR/POPIA?

**[PENDING: to be answered with legal.]**

### B9. Is the system enforceable under our labour agreements and union consultation requirements, and how have sites handled worker acceptance?

**[PENDING: to be answered with legal.]**

### B10. Can data be used for discipline, and what safeguards prevent misuse?

The base objective of the FAS is to evaluate the operator's level of attention (whether they show drowsiness or are distracted). It can also evaluate compliance with the customer's safety protocol (whether the operator uses a mobile phone, consumes tobacco, or wears the seat belt during the trip). For additional behaviours, the recording and consultancy for any additional safety behaviours to be assessed must be agreed with TORSA.

Access to media is restricted to the supervisors or monitoring staff defined by the customer, protected with MFA, and every action generates auditable logs (see B15).

**[PENDING: confirm wording on use for discipline, to be agreed with legal.]**

### B11. Is live in-cab video streamed in real time to a control room, or only clipped and uploaded after a triggered event? What latency should we expect?

The FAS evaluates the operator's condition from **clips**. Whether additional clips or, in specific cases, video streaming are needed to assess further behaviours depends on the agreement with the customer. Network availability and quality are required to send alert and behaviour clips. The maximum network latency required for live streaming is **500 ms**.

### B12. What connectivity and bandwidth does live monitoring need per vehicle, and how does it degrade on sites with patchy LTE or Wi-Fi coverage?

All processing runs on the on-board equipment and the corresponding alerts are triggered in the cab. Alert clips are stored and sent to the server hosting TORSA Cloud when the network is recovered. The alert and the action on the operator are always executed in the cab. Live streaming requires a maximum latency of 500 ms.

**[PENDING: bandwidth per vehicle in Mbps.]**

### B13. How is footage handled under POPIA: lawful basis, operator notification, retention period, access controls, and deletion?

If the operation requires it, we adapt the data-management layer. Retention periods are described in B7 and access controls in B15.

**[PENDING: POPIA lawful basis, operator notification and deletion, to be answered with legal.]**

### B14. Where is video stored and processed?

Clip processing and alert generation, as well as the action towards the operator (alarm), are performed on the on-board equipment. The later structure (reporting and analytics) is built on the TORSA Cloud platform, which, depending on what is agreed with the customer, can be:

- **Deployed on the customer's servers in their data centres.** The customer is responsible for the servers and their maintenance, and must provide remote access to this environment for implementation and service maintenance.
- **Hosted in TORSA's cloud.** TORSA takes care of server and service maintenance, access, backups and information security.

### B15. Who can view live and recorded footage, and is every access logged and auditable?

Following the safety protocol, access to the system's media is granted to the supervisors or monitoring personnel the customer defines. Access is secured with **MFA**, and every action generates auditable logs. If the service runs on TORSA's cloud infrastructure, it is built to the highest security standards (ISO 27001 is in progress, see B22).

### B16. Have you implemented cab monitoring at sites with union representation? What consultation process and agreements were needed, and how did you address surveillance concerns?

**[PENDING: to be answered.]**

### B17. Can footage be used in disciplinary or incident investigations, and does your system preserve chain of custody and tamper evidence?

Yes. The alert clips, together with the event context (vehicle activity, speed, direction), serve as a basis for an investigation. They cannot be treated as clinical evidence: the system evaluates what is within its field of view and has no clinical information about the operator that would support such a conclusion.

**[PENDING: chain of custody and tamper evidence mechanisms.]**

### B18. Do the cameras provide infrared night vision, and how do they hold up against vibration, dust and heat in South African surface operations?

Yes, the cameras use infrared LEDs for night vision (see B1). We do not yet have operations with the FAS implemented in South Africa, but the solution has been validated in different extreme climates (flat deserts, high snowy terrain), keeping its response reliable.

### B19. What happens if recognition fails (false rejects, PPE, injury)? Is there a safe fallback to avoid production delays?

**[PENDING: to be answered.]**

### B20. Does it fit into a broader fatigue risk management system (rosters, sleep data, wearables), or is it camera-only?

The TORSA FAS is based on visual evidence of the operator in the cab and the operating traffic context (when it escalates to or works with the CMS). As part of the Augmented Operation roadmap, we plan to implement **wearables** that assess the operator's sleep condition, to identify attention deviations preventively. No release date has been set.

We also complement FAS data with records from other sources to enrich the feedback within the safety protocol that the customer implements. TORSA can advise on and consult on data integration and analytics.

### B21. Which KPIs does the platform report, and can we export them to our own analytics?

We provide histograms, criticality history, and safety and productivity indicators. The data belongs to the customer, and we can provide it in several ways: ready to use on **TORSA Cloud**, through an **API**, or through a **Data Lake**.

### B22. What are the security certifications?

We hold the ISO 9001, ISO 14001 and ISO 45001 triple standard, and we are in the process of implementing **ISO 27001**.

### B23. What is the offline behaviour?

All processing runs on the on-board equipment and the corresponding alerts are triggered. Alert clips are stored and, when the network is recovered, sent to the server hosting TORSA Cloud. Connectivity makes the data available for later management and analytics. The alert and its action are always executed in the cab.

### B24. Can this product share one in-cab unit and network with the collision avoidance system to save capex and installation downtime?

Yes. TORSA systems are scalable with each other to minimise components in the cab, minimise points of failure and make field maintenance easier. Installation time is optimised by reusing components, which also saves maintenance downtime.

### B25. Which South African/Other reference customers can we speak to about fatigue monitoring specifically?

We share data from **EPSA**. **[PENDING: EPSA data to attach and permission to name the customer.]**

### B26. What are the pilot design, success criteria and exit terms?

We share a standard pilot SOW (Statement of Work), attached.

### B27. What detection method does FAS use (eye closure, head pose, facial analysis, steering behaviour), and what is its validated accuracy for microsleep and distraction events?

Our FAS uses computer vision with active infrared illumination, and works in five steps:

1. **Instant (observation):** the camera analyses the cab frame by frame in real time, capturing several indicators at once: eye orientation, eyelid opening, head position, and specific behaviours such as mobile phone use, tobacco or distracting objects.
2. **Action (validation):** a single frame is not enough to confirm an event. The system analyses several consecutive frames and requires a sustained pattern in ratio, duration and movement speed before confirming an action.
3. **State (operator state):** with the actions confirmed, the system determines whether the operator is fatigued, distracted or at risk. Events follow a clear hierarchy between states; fatigue and distraction do not compete, they are resolved with defined rules.
4. **Alert:** if the state exceeds the threshold defined by the operation, the alert is triggered immediately.
5. **Platform:** everything is recorded in TORSA Cloud with full history, video evidence for each event and exportable reports.

**Validated accuracy.** In a pilot (June 2026), precision was **98% over 162 reviewed alerts**, with 100% for fatigue, mobile phone use and distraction, and 91% for tobacco. Precision is the proportion of valid alerts over the total alerts generated, calculated by reviewing the video evidence of each event.

### B28. How does it perform for operators wearing safety glasses, tinted lenses or dust masks, and in night shifts, direct sunlight and dusty cabs?

Answered in B1.

### B29. What is the measured false-alarm rate in production, and how is it tuned per site to avoid operator alarm fatigue?

The false-alarm rate is below **[PENDING: XY%]**. It is controlled through the maintenance of the AI models and by the TORSA monitoring centre, which constantly evaluates the conditions of use of the system.

### B30. What is the alert escalation path: in-cab audio, seat vibration, supervisor notification, control-room callout? Can it be configured to match each mine's fatigue management Code of Practice?

As in B6, all these actions must be defined in the response protocol by the customer's safety committee. The TORSA FAS is the management tool that gives effect to the protocol.

### B31. Can FAS integrate with CMS so that collision warning thresholds tighten when an operator shows fatigue?

Yes. When integrated with the TORSA CMS, the operator's attention level becomes a parameter in the analysis of interaction conditions between vehicles (see B5 and B24).

### B32. Can FAS ingest roster, shift-length and overtime data to support risk-based fatigue management rather than event detection alone?

Yes. Shifts and operators can be loaded through local files or via API.

### B33. Do you have any South African fatigue-reduction outcome data (named site, before/after event rates)?

We do not have metrics in South Africa. At EPSA, the fatigue index reduction has been **[PENDING: XY]**.

### B34. Do voice alerts and operator interfaces support local languages?

Yes, the system supports local languages. Today we have Spanish, English and Portuguese.

### B35. Is FAS available for light vehicles and contractor vehicles, including portable or temporary installation?

Yes. We have light versions without a screen for light vehicles.

### B36. What connectivity and bandwidth does live monitoring need per vehicle, and how does it degrade on sites with patchy LTE or Wi-Fi coverage?

See B12.

### B37. What local support, spares holding and technician presence do you have in South Africa and what are your guaranteed response times there?

We have our own office in Johannesburg with specialised staff, and an authorised partner in the Northern Cape. We also have engineering offices in Spain and Peru, and soon in Argentina, Chile, Colombia, Australia and Saudi Arabia. Spares holding and the corresponding SLAs will be negotiated when the contract is concluded (see A24).

### B38. Is there a hardware and software as a service option?

Yes, a service-type solution is possible. The details must be reviewed between the parties (see A23).

### B39. What is the liability and responsibility of TORSA if a fatigue event is missed?

**[PENDING: to be answered with legal.]**

---

## Annexes

1. MOSH certificate (University of Pretoria).
2. ISO/TS 21815-2 certificate (University of Pretoria).
3. OEM and independent certificates (Bell, Volvo, Nerospec).
4. Sample intervention manual.
5. Inventory of vehicles with a TORSA braking module.
6. Sample pilot SOW.
7. EPSA data.
8. ISO 9001, ISO 14001 and ISO 45001 certificates.
