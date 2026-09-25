# 6 Robot Construction Rules (R)

The rules in this section govern the design and construction of every ROBOT competing in SUMMIT PUSH. A ROBOT is the electromechanical assembly, including all BUMPERS and all attached COMPONENTS and MECHANISMS, that a team places on the FIELD to play the game. Unless a rule states otherwise, compliance is assessed at INSPECTION and must be maintained for the duration of the event.

> *Commentary:* These rules follow the construction conventions most competitive robotics teams already build to. Where SUMMIT PUSH departs from those conventions, most notably by having no in-match height limit, the rule says so. Commentary explains why a rule exists, which is the quickest way to understand what it does and does not prohibit.

## 6.1 Size, Weight, and Extension (R1xx)

**R101** *Stay under the weight limit.* The ROBOT weight must not exceed 115 lb (52.2 kg). When determining weight, the basic ROBOT structure and all elements of all additional MECHANISMS that might be used in a single configuration of the ROBOT are weighed together. The ROBOT battery with its associated half of the Anderson SB connector, and the BUMPERS with any BUMPER attachment hardware that remains with them when removed, are excluded from ROBOT weight.

*Violation:* ROBOT will not pass INSPECTION.

**R102** *BUMPERS have their own weight limit.* The total weight of all BUMPERS, weighed together as removed from the ROBOT, must not exceed 20 lb (9.1 kg).

*Violation:* ROBOT will not pass INSPECTION.

**R103** *Fixed FRAME PERIMETER, 120 in maximum.* The FRAME PERIMETER of a ROBOT is defined by the outermost set of exterior vertices on the ROBOT (excluding BUMPERS) that are within the BUMPER ZONE. The FRAME PERIMETER must be a fixed, non-articulated structure, and its total length must not exceed 120 in (304.8 cm). To determine the FRAME PERIMETER, wrap a piece of string around the ROBOT at the level of the BUMPER ZONE and pull it taut; the string outlines the FRAME PERIMETER, and its length is the measured perimeter. Minor protrusions no greater than 0.25 in (bolt heads, rivets, weld beads) are excused from this measurement.

*Violation:* ROBOT will not pass INSPECTION.

> *Commentary:* With the string-wrap method, concave features cost nothing because the string bridges them, but every convex feature counts. A 30 in × 30 in square and a 27 in × 33 in long chassis each measure 120 in, the maximum.

**R104** *Start inside the FRAME PERIMETER, at most 42 in tall.* In its STARTING CONFIGURATION (the physical state of the ROBOT at the start of a MATCH), no part of the ROBOT may extend beyond the vertical projection of the FRAME PERIMETER, except its BUMPERS and minor protrusions per **R103**, and the ROBOT's height must not exceed 42 in (106.7 cm).

*Violation:* ROBOT will not pass INSPECTION. If discovered at the start of a MATCH, the ROBOT will not be permitted to start until it is compliant.

**R105** *Extend no more than 18 in.* ROBOTS may not extend more than 18 in (45.7 cm) horizontally beyond their FRAME PERIMETER at any time during a MATCH, in any direction, measured as a horizontal distance from the vertical projection of the FRAME PERIMETER.

*Violation:* ROBOT will not pass INSPECTION; maximum extension is demonstrated at INSPECTION per Section 7.2. Over-extension during a MATCH is penalized under **G404**.

> *Commentary:* The FIELD is dimensioned so that 18 in of extension reaches every scoring position on the CRAG. A ROBOT with its BUMPERS against the DEPOT lip has its FRAME PERIMETER 19.75 in from the SHELF FACE plane, so a Shelf 1 slot center is 12.75 in of extension away, and the Summit Socket rim, 8.0 in outboard of that face at 72 in, is 11.75 in away. From the PEG FACE, a High Peg root is 17.0 in away and its tip only 9.9 in. The two sockets on a SOCKET FACE are reached from different standoffs. The Mid Socket sits on the PEG FACE side, clear of the DEPOT, so BUMPERS can come to the face and the rim is 5.0 in of extension away. The Low Socket sits on the SHELF FACE side above the DEPOT's corner arm, which holds the FRAME PERIMETER 19.75 in off the face and puts that rim 11.75 in away. Nothing on the CRAG requires more than 18 in; the design problem is vertical reach.

**R106** *No in-match height limit.* Once a MATCH begins, there is no limit on ROBOT height.

> *Commentary:* The High Pegs sit at 78 in, the Summit Socket rim at 72 in, and the SUMMIT RUNG at 78 in. Each of these tasks needs substantial vertical reach, and a hanging ROBOT carries its geometry well above any plausible cap. Any published limit would become the height every competitive design builds to, so SUMMIT PUSH publishes none. Teams accept the corresponding risk: a fully extended, high-CG ROBOT may be defended wherever defense is legal (see G4xx), and tall ROBOTS tip. Design elevators and arms with the CRAG APRON protection, and its limits, in mind.

## 6.2 Safety and Materials (R2xx)

**R201** *No sharp edges.* ROBOT parts must not pose undue hazards. Protrusions and exposed edges likely to cut or snag SUPPLIES, FIELD elements, or people (unfinished sheet-metal edges, exposed lead-screw ends, forks or spears without radiused tips) must be guarded, deburred, or radiused.

*Violation:* ROBOT will not pass INSPECTION.

**R202** *No shattering hazards.* Materials liable to shatter or produce loose debris on impact are prohibited, including glass, brittle cast acrylic in structural or impact-exposed applications, and unshielded incandescent lamps. Polycarbonate is the expected transparent material.

*Violation:* ROBOT will not pass INSPECTION.

**R203** *No liquids.* ROBOTS may not contain liquids of any kind, including hydraulic fluids, ballast liquids, and liquid coolants. Grease and lubricant are permitted only where used to reduce friction within the ROBOT, and only in quantities that cannot contaminate the FIELD carpet, SUPPLIES, or other ROBOTS.

*Violation:* ROBOT will not pass INSPECTION. A ROBOT observed depositing lubricant on the FIELD during a MATCH: MAJOR FOUL, and re-inspection is required.

**R204** *No hazardous or field-damaging materials.* The following are prohibited anywhere on the ROBOT: flammable gases or solids intended for combustion; untreated hazardous materials (for example, lead weights not fully encapsulated); high-intensity lasers above Class 2; exposed untethered projectiles; and traction devices that could damage the FIELD carpet or SUPPLIES (metal cleats, adhesive wheels, hook-side hook-and-loop material in contact with carpet).

*Violation:* ROBOT will not pass INSPECTION.

**R205** *Contain stored energy.* Stored-energy devices (springs, latex tubing, gas struts, counterweights, pneumatics per R8xx) are permitted, but the ROBOT must be designed so that stored energy is released in a controlled fashion and can be safely neutralized (spring to rest, vented, or mechanically locked) when the ROBOT is disabled or powered off.

*Violation:* ROBOT will not pass INSPECTION.

**R206** *Stored energy at MATCH start.* At the start of a MATCH, the only sources of stored energy on the ROBOT are:

- **a.** electrical energy from the ROBOT battery (**R601**);
- **b.** compressed air stored in the pneumatic system in compliance with **R802**–**R805**, at no more than 120 psi (**R803**);
- **c.** a change in the altitude of the ROBOT's center of gravity within its STARTING CONFIGURATION (**R104**); and
- **d.** energy stored by deformation of springs, latex tubing, gas struts, and equivalent elastic elements, either (i) in the element's installed at-rest state (a belt or chain tensioner, a gas strut counterbalancing an arm, a spring retaining a MECHANISM inside the FRAME PERIMETER), or (ii) deliberately charged before the MATCH, provided the element is held by a positive mechanical restraint and its release cannot, by itself, propel a SUPPLY or move the ROBOT across the carpet.

Any element charged under (d)(ii) must be declared at INSPECTION, and the team must demonstrate its restraint and its neutralization per **R205**.

*Violation:* ROBOT will not pass INSPECTION. If discovered at the start of a MATCH, the ROBOT will not be permitted to start until it is compliant.

**R207** *Decorations must not imitate the FIELD.* Non-functional decorations are permitted provided they are COTS items or FABRICATED ITEMS made of materials legal under R2xx, do not affect the outcome of a MATCH, and do not obscure the BUMPERS or the team numbers required by **R404**. In addition, no ROBOT may carry, display, or project:

- **a.** any image from the AprilTag 36h11 family, or any high-contrast square fiducial pattern that a vision system could resolve as a FIELD tag (see Section 3.7);
- **b.** any feature that a referee, DRIVE TEAM, or vision system could mistake for a FIELD element or a SUPPLY, including a horizontal ring of ALLIANCE-colored lighting positioned to resemble a CRAG tier ring, a lamp resembling the SUMMIT BEACON, a white block display resembling the FORECAST indication, or an ALLIANCE-colored block display resembling the ROUTE indication (Sections 3.1.2 and 3.3.5); or
- **c.** light of any kind, including LEDs and lasers of any class, directed so as to interfere with an opponent's cameras or with the view from any driver station.

ALLIANCE-colored and white ROBOT lighting is otherwise permitted, including status and SUPPLY indicators, provided it is not arranged as a horizontal row of one, two, or three equal, discrete, separated lit blocks resembling the FIELD LED indication of Section 3.1.2. Continuous strips, single indicator lamps, and any lighting that does not present a countable block pattern are permitted. The amber ROBOT SIGNAL LIGHT required by **R706** never violates this rule, and neither does lighting that merely shares a hue with a SUPPLY.

*Violation:* ROBOT will not pass INSPECTION. Use in a MATCH of a decoration prohibited by this rule: MAJOR FOUL, and the ROBOT may not play again until re-inspected.

## 6.3 Fabrication and Budget (R3xx)

**R301** *COTS defined.* A COTS (Commercial-Off-The-Shelf) item is a standard, unmodified part or assembly commonly available from a VENDOR and available to all teams. A part that has been modified beyond its published, vendor-supported configuration (machined, bent, cut, or reprogrammed outside vendor firmware) is no longer COTS; it is a FABRICATED ITEM.

**R302** *FABRICATED ITEMS defined.* A FABRICATED ITEM is any COMPONENT or MECHANISM that has been altered, built, cast, printed, or assembled by or for the team into its final form. Custom parts may be fabricated by any method (machining, additive manufacturing, composites, weldments) from any material not prohibited by R2xx.

**R303** *Budget realism.* SUMMIT PUSH does not require a costed Bill of Materials. Instead, one realism standard applies: every COTS item on the ROBOT must be purchasable by a competing team (no one-off, discontinued and unobtainable, or sponsor-exclusive COMPONENTS as load-bearing elements), and no single COTS item may exceed $600 USD at published VENDOR pricing. Design-challenge entries must also satisfy the self-inspection checklist in Section 7.4, including a stated weight budget.

*Violation:* An entry is penalized at judging per the published rubric; at a physical event, the ROBOT will not pass INSPECTION.

> *Example:* A team designs a custom two-stage elevator using COTS bearing blocks, COTS motors, and waterjet-cut aluminum side plates. The plates are FABRICATED ITEMS; the bearing blocks and motors are COTS. All are legal. The same team may not specify a $2,400 industrial harmonic-drive actuator as its wrist joint, because it exceeds the **R303** single-item limit.

## 6.4 BUMPERS (R4xx)

**R401** *BUMPERS all the way around.* ROBOTS must be equipped with BUMPERS that protect the entire FRAME PERIMETER. Each individual gap in BUMPER coverage around the FRAME PERIMETER must be less than 1.25 in (3.2 cm), and each FRAME PERIMETER corner must be fully protected: BUMPER segments must meet or overlap at corners so that the corner vertex is backed by BUMPER structure.

*Violation:* ROBOT will not pass INSPECTION. A ROBOT whose BUMPER is damaged during a MATCH so that this rule is no longer met may be DISABLED at the HEAD REFEREE's discretion.

**R402** *BUMPER construction.* Each BUMPER must be constructed as follows:

**Table 6-1: BUMPER construction**

| Requirement | Specification |
|---|---|
| Backing | 0.75 in (nominal) plywood or solid wood, 4.5 in tall (full height of the BUMPER cross-section) where hardware permits; hard backing continuous behind all foam |
| Foam | Two stacked 2.25 in (nominal) pool-noodle-class foam cylinders, or equivalent solid foam, giving a 2.25 in (5.7 cm) minimum foam depth in front of the backing |
| Height | 4.5 in (11.4 cm) nominal vertical cross-section |
| Cover | Rugged, smooth cloth (1000D Cordura-class) fully enclosing the foam; solid red or solid blue, matching the ALLIANCE of the current MATCH |
| Corners | Foam must wrap or be mitered so corners are filled; no hard backing exposed at corners |
| Profile | No wedge shapes: the BUMPER cross-section must be approximately rectangular, and BUMPER faces must be approximately vertical |

*Violation:* ROBOT will not pass INSPECTION.

**R403** *BUMPERS fill the BUMPER ZONE.* BUMPERS must completely fill the BUMPER ZONE, the volume between horizontal planes 2.5 in (6.4 cm) and 5.75 in (14.6 cm) above the floor, everywhere the BUMPER protects the FRAME PERIMETER, with the ROBOT standing normally on a flat floor. The bottom edge of the BUMPER must be at or below 2.5 in and its top edge at or above 5.75 in, so a BUMPER of the 4.5 in cross-section required by **R402** sits with its bottom edge between 1.25 in and 2.5 in above the floor. No part of the BUMPER may be more than 7.0 in (17.8 cm) above the floor. BUMPERS must continue to fill the BUMPER ZONE while the ROBOT's drive base is on the carpet; articulating or dropping BUMPERS are prohibited.

*Violation:* ROBOT will not pass INSPECTION.

**R404** *Display team numbers.* Team numbers must be displayed on the BUMPERS in white characters at least 3.75 in (9.5 cm) tall, in at least 3 locations spaced around the FRAME PERIMETER, legible from 60 ft. Numbers may be fabric, paint, or iron-on; they may not be handwritten in marker.

*Violation:* ROBOT will not pass INSPECTION.

**R405** *BUMPERS must be removable.* BUMPERS must attach to the FRAME PERIMETER with a rigid mounting system and must be removable using no tools other than common hand tools, so that weight (**R101**/**R102**) and FRAME PERIMETER (**R103**) can be verified at INSPECTION.

*Violation:* ROBOT will not pass INSPECTION.

## 6.5 Motors and Actuators (R5xx)

**R501** *Legal motors only.* The only motors and actuators permitted on the ROBOT are those listed in Table 6-2, in any quantity unless otherwise restricted, plus exactly one compressor per **R802**.

**Table 6-2: Legal Motors and Actuators**

| Motor | Vendor / Part No. |
|---|---|
| Kraken X60 | WCP-0940 |
| Kraken X44 | WCP-1735 |
| Falcon 500 | CTRE 217-6515 |
| Minion | CTRE / WCP WCP-1691 |
| NEO Brushless V1.0 / V1.1 | REV-21-1650 |
| NEO Vortex | REV-21-1652 |
| NEO 550 | REV-21-1651 |
| CIM | am-0255 / 217-2000 |
| Mini CIM | am-2964a / 217-3371 |
| BAG | 217-3351 |
| 775pro | 217-4347 |
| RS775-5 / RS775-18V | am-2161 / banebots RS775 |
| Thrifty Pulsar 775 | TTB-0775 |
| Venom (integral controller) | Playing With Fusion BDC-10001 |
| AndyMark 9015 | am-0912 |
| NeveRest series | am-3104 (and gearmotor variants) |
| AndyMark PG series gearmotors | am-2765 / am-2766 |
| AndyMark RedLine | am-3775 |
| Snow Blower motor | am-2235 / am-2235a |
| Automotive accessory motors (window, door, throttle, seat) | Denso / Johnson Electric OEM units |
| COTS hobby servos | any, per **R504** |
| ELECTRIC SOLENOID ACTUATORS | ≤1 in stroke, ≤10 W each |
| Compressor (exactly one, per **R802**) | any COTS, ≤1.1 cfm at 12 VDC |

*Violation:* ROBOT will not pass INSPECTION.

**R502** *Do not modify motors.* Legal motors may not be modified except for mounting hardware, output shaft or pinion changes, wire and connector changes at the motor pigtail, insulating the case, and installing vendor-supplied firmware. The integral controller of a Venom and the stator/rotor internals of any motor may not be altered.

*Violation:* ROBOT will not pass INSPECTION.

**R503** *No more than 4 propulsion motors.* No more than 4 motors may deliver torque, directly or indirectly, to elements of the ROBOT that contact the carpet for propulsion (drive wheels, treads, or equivalent). Motors used solely to steer or azimuth a wheel module (motors whose torque changes the pointing direction of a wheel but does not propel the ROBOT across the carpet) are exempt from this count.

*Violation:* ROBOT will not pass INSPECTION.

> *Commentary:* A four-module swerve drivetrain is legal: its 4 drive motors count against the cap and its 4 azimuth motors do not. An eight-motor tank drive is not legal. The cap limits pushing-match energy and top speed in a game whose midfield corridor guarantees traffic, and it leaves motor budget and weight for the elevators, arms, and climbers the game requires.

**R504** *Servo limits.* COTS hobby servos are legal only if rated at or below 4 A stall current and 8 W continuous output power at 6 V. Servos must be powered from the roboRIO's integrated servo power rail or from the Servo Power Module listed in Table 6-4. Servos may not be used to propel the ROBOT.

*Violation:* ROBOT will not pass INSPECTION.

**R505** *One actuator per power output.* Each motor controller output, relay output, and roboRIO PWM output may power exactly one motor, servo, or ELECTRIC SOLENOID ACTUATOR. Exception: multiple servos or solenoids may share one channel of the Servo Power Module listed in Table 6-4, within that channel's rating.

*Violation:* ROBOT will not pass INSPECTION.

## 6.6 Power Distribution (R6xx)

**R601** *One battery.* The sole electrical energy source for the ROBOT is exactly one non-spillable 12 V sealed lead-acid (SLA) battery, rated 17–18.2 Ah, with nominal dimensions of 7.1 in × 3.0 in × 6.6 in (for example MK ES17-12, Duracell SLAA12-18NB, Interstate SLA1116, or EnerSys NP18-12). The battery must be secured against the forces of MATCH play, including inverted or hanging orientations on the HEADWALL.

*Violation:* ROBOT will not pass INSPECTION.

> *Commentary:* Inspectors check battery retention closely for this game because a ROBOT that climbs to the SUMMIT RUNG hangs nose-up at 78 in. Zip ties alone are not adequate retention for a climbing ROBOT; use a positive mechanical restraint.

**R602** *One main breaker.* ROBOT power must flow through a single 120 A main circuit breaker (for example Carling / am-0282) that is readily accessible and clearly labeled. Where practical, it must be positioned so that FIELD STAFF can disable the ROBOT without reaching into MECHANISMS or under a hanging ROBOT.

*Violation:* ROBOT will not pass INSPECTION.

**R603** *Main power run.* The battery, main breaker, and power distribution device must be connected with 6 AWG or larger copper wire, using an Anderson SB-class connector (SB50 or equivalent) at the battery.

*Violation:* ROBOT will not pass INSPECTION.

**R604** *Legal power distribution.* All branch circuits must originate from exactly one of the following devices: CTRE Power Distribution Panel (PDP, 217-4244), CTRE PDP 2.0, REV Power Distribution Hub (PDH, REV-11-1850), or AndyMark AMPD (am-5596). Each branch circuit must be protected at the distribution device, in a breaker position or fused channel of that device, and no branch circuit may be protected at more than 40 A. Branch protection must be a Snap-Action VB3-series circuit breaker (or an equivalent manual-reset thermal automotive blade breaker), or the fuse type specified by the distribution device manufacturer for its fused channels. Self-resetting (auto-reset) breakers are prohibited.

*Violation:* ROBOT will not pass INSPECTION.

**R605** *Wire gauge by protection rating.* Copper wire on each protected circuit must meet the minimum size in Table 6-3, from the protection device to the load.

**Table 6-3: Minimum Wire Size**

| Circuit protection | Minimum wire size |
|---|---|
| 120 A main breaker | 6 AWG |
| Over 30 A, up to 40 A | 12 AWG |
| Over 20 A, up to 30 A | 14 AWG |
| Over 10 A, up to 20 A | 18 AWG |
| 10 A and below (breaker or fuse) | 22 AWG |

Wire must be appropriately insulated. Wire connected to the +12 V side of a circuit must be red, white, brown, or yellow; wire connected to the ground (common) side must be black or blue. Striped wire takes the color of its base insulation, and no wire may carry a base color from both lists. Splices and connections must be insulated and strain-relieved.

*Violation:* ROBOT will not pass INSPECTION.

**R606** *Frame isolation.* The ROBOT frame must not be used as an electrical conductor. Resistance between either battery terminal and the frame must exceed 120 Ω, verified at INSPECTION.

*Violation:* ROBOT will not pass INSPECTION.

## 6.7 Control System (R7xx)

**R701** *One roboRIO.* ROBOT control must be performed by exactly one NI roboRIO or roboRIO 2.0, powered from a dedicated protected circuit on the power distribution device. No other controller may issue actuation commands, except as an intermediary explicitly commanded by the roboRIO.

*Violation:* ROBOT will not pass INSPECTION.

**R702** *One radio.* Wireless communication must be performed by exactly one Vivid-Hosting VH-109 radio, powered per manufacturer specification from a legal power source, mounted so its status LEDs are visible to FIELD STAFF, and shielded from SUPPLY and ROBOT impact. A device with integrated wireless capability that is carried for a non-wireless purpose (for example a vision coprocessor) is permitted only if that capability is disabled in software or firmware so that the device neither transmits nor associates during a MATCH. No other device on the ROBOT may transmit or receive RF during a MATCH.

*Violation:* ROBOT will not pass INSPECTION. Operation of any other RF device during a MATCH: YELLOW CARD.

> *Commentary:* Vision coprocessors and smart cameras often ship with onboard Wi-Fi. Turning it off in the device's own settings satisfies this rule; Wi-Fi-capable hardware is not itself a violation.

**R703** *Legal controllers and power modules.* Motors other than servos, integral-controller motors, and the compressor must be controlled by devices listed in Table 6-4.

**Table 6-4: Legal Motor Controllers, Pneumatics Controllers, and Power Modules**

| Device | Vendor / Part No. | Notes |
|---|---|---|
| Talon FX | CTRE (integral to Falcon 500, Kraken X60/X44) | CAN/PWM |
| Talon FXS | CTRE 25-2445140 | CAN/PWM; pairs with Minion |
| Talon SRX | CTRE 217-8080 | CAN/PWM |
| Victor SPX | CTRE 217-9191 | CAN/PWM |
| Victor SP | CTRE 217-9090 | PWM only |
| Spark MAX | REV-11-2158 | CAN/PWM |
| Spark Flex | REV-11-2159 | CAN/PWM; pairs with NEO Vortex |
| Thrifty Nova | TTB-0100 | CAN |
| Koors40 | AndyMark am-5593 | CAN/PWM |
| Venom (integral) | Playing With Fusion BDC-10001 | CAN/PWM, motor-integrated |
| Pneumatics Control Module | CTRE 217-4243 | CAN; compressor and solenoid outputs only |
| Pneumatic Hub | REV-11-1852 | CAN; compressor and solenoid outputs only |
| Servo Power Module | REV-11-1144 | 6 V servo/solenoid power, 6 channels; not a propulsion controller |

ELECTRIC SOLENOID ACTUATORS and non-actuator custom circuits and loads (LEDs, sensors, coprocessors) may also be powered from Spike H-Bridge relays (217-0220) or from the switched/fused low-current channels of the PDH/PDP, within their ratings. The compressor is powered and switched only by the pneumatics controller (**R807**).

*Violation:* ROBOT will not pass INSPECTION.

**R704** *CAN commands come from the roboRIO.* All actuation commands carried on the CAN bus must originate from the roboRIO. Coprocessors (for example vision processors) may publish data to the roboRIO over CAN, Ethernet, USB, or serial, but may not command motor controllers directly.

*Violation:* ROBOT will not pass INSPECTION.

**R705** *Do not defeat safety firmware.* Motor controllers, the roboRIO, the radio, and the power distribution device must run vendor-released firmware. Modifying firmware or hardware to bypass disable, brownout, or watchdog behavior is prohibited.

*Violation:* ROBOT will not pass INSPECTION. If the modification is used in a MATCH, the team may be referred to the HEAD REFEREE for a RED CARD.

**R706** *Fit one ROBOT SIGNAL LIGHT.* The ROBOT must include exactly one ROBOT SIGNAL LIGHT (RSL): a COTS solid-state amber indicator wired to the roboRIO's RSL port and powered only from that port. It must be mounted upright on the main ROBOT structure, not on an articulating MECHANISM, and must be visible from any horizontal direction at 30 ft with the ROBOT in its STARTING CONFIGURATION, unobstructed by BUMPERS or by any MECHANISM in any configuration the ROBOT will use, including a HEADWALL hang. The RSL must be continuously lit when the ROBOT is powered on and disabled, including when it is not connected to the FMS, and must blink when the ROBOT is enabled.

*Violation:* ROBOT will not pass INSPECTION.

> *Commentary:* **R106** sets no in-match height limit, and ROBOTS hang from the SUMMIT RUNG at 78 in during ENDGAME. FIELD STAFF working under a hanging ROBOT need a clear answer to whether it is live. Providing that answer is the only job of the RSL, which is why an RSL mounted on an elevator carriage or an arm does not satisfy this rule.

**R707** *OPERATOR CONSOLE.* The OPERATOR CONSOLE is the assembly of controls, computers, and wiring a DRIVE TEAM connects to the FMS at its driver station. It must fit within the driver-station shelf, connect to the FMS by the standard Ethernet connection, and contain no wireless transmitter other than a single COTS wireless controller receiver dongle. The OPERATOR CONSOLE may not be connected to any device outside the driver station other than the FIELD-provided FMS connection point (Section 3.1).

*Violation:* The team may not connect to the FMS until compliant.

## 6.8 Pneumatics (R8xx)

**R801** *Legal pneumatic COMPONENTS only.* Pneumatic COMPONENTS must be COTS parts rated by their manufacturer for at least their maximum expected working pressure, and may not be modified except for supported fitting and thread changes and mounting.

*Violation:* ROBOT will not pass INSPECTION.

**R802** *One onboard compressor.* Compressed air must be supplied by exactly one compressor, mounted on the ROBOT, with a flow rating of ≤1.1 cfm. Off-board pre-charging is permitted only through the ROBOT's own compressor circuit or a legal fill port upstream of the primary regulator.

*Violation:* ROBOT will not pass INSPECTION.

**R803** *Pressure limits.* Stored pressure must not exceed 120 psi (827 kPa). Working pressure (everything downstream of the primary regulator) must not exceed 60 psi (414 kPa).

*Violation:* ROBOT will not pass INSPECTION.

**R804** *One relieving regulator.* Working pressure must be provided through a single primary relieving pressure regulator, set to ≤60 psi. Additional regulators downstream may only further reduce pressure.

*Violation:* ROBOT will not pass INSPECTION.

**R805** *Required safety devices.* The pneumatic circuit must include a safety relief valve set between 125 psi and 130 psi, plumbed rigidly to the compressor output; pressure gauges, readable without moving MECHANISMS, showing stored and working pressure; and a manually operated vent plug valve that can vent the entire stored-pressure circuit to atmosphere and be left open.

*Violation:* ROBOT will not pass INSPECTION.

**R806** *Pneumatics use atmospheric air only.* The pneumatic system may act only on air drawn from the atmosphere, and pneumatic COMPONENTS may not be used for any purpose other than their manufacturer's intent (no cylinders as structural springs charged beyond rating, no vacuum generation beyond COTS venturi devices operating within rating).

*Violation:* ROBOT will not pass INSPECTION.

**R807** *Pneumatics control.* The compressor and every pneumatic solenoid valve must be connected to and commanded by exactly one legal pneumatics controller (CTRE Pneumatics Control Module 217-4243 or REV Pneumatic Hub REV-11-1852), powered from a dedicated protected circuit on the power distribution device per **R604** and commanded only by the roboRIO. The compressor may not be connected to a motor controller output.

*Violation:* ROBOT will not pass INSPECTION.

**R808** *Closed-loop compressor control.* Compressor operation must be governed by closed-loop control from a pressure switch or pressure transducer connected to the pneumatics controller, configured to stop the compressor at or below 115 psi, so that stored pressure never reaches the **R803** limit of 120 psi and never approaches the relief valve's cracking pressure. A compressor that runs without closed-loop pressure feedback is not legal.

*Violation:* ROBOT will not pass INSPECTION.

---

# 7 Inspection & Eligibility

Every ROBOT must pass INSPECTION before participating in a Qualification or Playoff MATCH. INSPECTION verifies compliance with all R-rules in the configuration(s) the ROBOT will use during MATCHES. If a ROBOT plays in multiple configurations, each must be inspected. Teams must declare all MECHANISMS they intend to use during the event, and re-inspection is required after any substantive modification.

## 7.1 Weigh-In

The ROBOT is weighed without its battery and without BUMPERS (**R101**), and the BUMPERS are then weighed separately (**R102**). Inspectors record both values. A ROBOT may be re-weighed at any time at the request of the HEAD REFEREE or the Lead Inspector, including between Playoff MATCHES.

## 7.2 Sizing

The ROBOT, in its declared STARTING CONFIGURATION and without BUMPERS, must fit within a sizing box with interior dimensions equal to the team's declared frame envelope and a height of 42 in, or be verified by string-wrap (**R103**) plus height measurement. Inspectors also ask the team to demonstrate the ROBOT's maximum horizontal extension and verify that it does not exceed 18 in beyond the FRAME PERIMETER (**R105**). Teams should be prepared to drive each MECHANISM to its commanded (software-limited) maximum reach on request. Mechanical hard stops are not required; **G404** governs commanded motion during a MATCH.

## 7.3 Bumper, Electrical, and Pneumatic Checks

- **BUMPERS:** construction and cross-section per **R402**, coverage and corners per **R401**, BUMPER ZONE fill per **R403** with the ROBOT on a flat floor, numbers per **R404**, and both color sets present.
- **Electrical:** battery retention and connector security (**R601**), main breaker accessibility (**R602**), branch breaker ratings and type per **R604** (≤40 A, manual-reset only), wire gauge spot-checks against Table 6-3 (**R605**), frame isolation >120 Ω (**R606**), one radio and one roboRIO (**R701**, **R702**), RSL mounting and visibility (**R706**), and all motor controllers on the legal list (**R703**).
- **Decorations:** no prohibited imagery, lighting, or FIELD-imitating features per **R207**.
- **Pneumatics (if fitted):** component ratings, relief valve, gauges, vent plug, regulator setting demonstrated with the system charged, pneumatics controller, and closed-loop pressure control (**R801**–**R808**).
- **Power-on check:** the ROBOT connects to a driver station and responds to enable and disable; the RSL behaves per **R706**; every motor is verified to be under control (no uncommanded motion on enable); and stored energy at MATCH start is verified per **R206**, with any deliberately charged element declared, its restraint shown, and its neutralization demonstrated.

## 7.4 Design-Entry Self-Inspection Checklist

Design-challenge entries are judged from their submissions. In place of physical INSPECTION, every entry must include a self-inspection page in its submission that demonstrates the items below. Judges treat a missing or unsupported item as an inspector treats a failed check.

**Table 7-1: Design-entry self-inspection checklist**

| # | Item | Evidence required |
|---|---|---|
| 1 | Weight budget | A table of every major subsystem with estimated mass, summing to ≤115 lb, with margin stated. CAD mass properties (with materials assigned) or a per-part estimate table are both acceptable. |
| 2 | Frame perimeter | Stated perimeter dimension ≤120 in, with a CAD sketch or measurement showing the string-wrap outline at BUMPER ZONE height. |
| 3 | Starting configuration | A CAD view of the ROBOT in STARTING CONFIGURATION inside a 42-in-tall bounding box, with all MECHANISMS within the FRAME PERIMETER projection. |
| 4 | Extension limit | CAD views of each MECHANISM at its commanded maximum reach, with a dimension showing ≤18 in of horizontal extension beyond the FRAME PERIMETER. |
| 5 | BUMPERS | BUMPERS modeled at 4.5 in cross-section, filling the 2.5–5.75 in BUMPER ZONE (bottom edge ≤2.5 in, top edge ≥5.75 in above the floor), full perimeter, corners filled. |
| 6 | Propulsion motor count | Drivetrain motor list showing ≤4 propulsion motors (azimuth motors identified separately for swerve). |
| 7 | Legal components | All motors from Table 6-2 and all controllers from Table 6-4; battery, main breaker, branch breaker ratings, power distribution device, and RSL identified in the CAD or BOM. |
| 8 | R303 realism | No single COTS item over $600; any uncommon COTS part named with its vendor. |
| 9 | Reach proof | CAD evidence that the ROBOT can reach its claimed scoring targets, for example a 78-in High Peg reach or a 72-in Summit Socket insertion, shown with the extension and height geometry that achieves it. Measure from the standoff the FIELD imposes: 19.75 in from the SHELF FACE; from a SOCKET FACE, 19.75 in at the Low Socket (the ROBOT cannot drive over the BASE DEPOT corner arm below it) and 3.0 in at the Mid Socket; and 3.0 in from the PEG FACE. |
| 10 | Climb proof | If the entry claims a CAMP RUNG or SUMMIT RUNG climb, CAD evidence of the route: the ROBOT engaging the LEDGE RUNG from the FIELD side per **G416**, then reaching a higher rung from that hang. The higher rung is either the CAMP RUNG (24 in up, 6.4 in back, and 24 in laterally offset) or the SUMMIT RUNG directly (48 in up and 12.9 in back, at the same lateral offset as the LEDGE RUNG). Either route is legal; show the one the design uses. |

> *Example:* A swerve entry lists 4× Kraken X60 (drive) + 4× Kraken X44 (azimuth) in item 6. This passes: only the four drive motors deliver propulsion torque, and azimuth motors are exempt under **R503**.

## 7.5 Eligibility

A ROBOT that has not passed INSPECTION may not participate in a Qualification or Playoff MATCH; in a judged design challenge, neither may an entry whose submission lacks the Section 7.4 checklist. If a ROBOT is found to violate an R-rule during an event, the HEAD REFEREE may review the relevant MATCHES. Deliberately violating a construction rule to gain a competitive advantage is a RED CARD offense.
