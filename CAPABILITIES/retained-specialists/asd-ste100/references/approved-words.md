# ASD-STE100 Approved Words & Vocabulary Guide

Part 2 of the ASD-STE100 specification provides the dictionary of controlled words. This reference summarizes dictionary conventions, common word substitutions, and technical domain allowances.

---

## 1. Dictionary Conventions

- **UPPERCASE**: In the specification, approved words are written in capital letters (*CLOSE*, *START*, *USE*).
- **lowercase**: Unapproved words are written in lowercase with their approved alternatives listed (*commence* -> *START*, *utilize* -> *USE*).
- **One Word, One Part of Speech**: An approved word belongs to exactly one part of speech.
  - *CLOSE* is approved ONLY as a verb (*Close the door*).
  - *close* is NOT approved as an adjective. Use *NEAR* (*Put the tool near the panel*).
  - *TEST* is approved as a verb (*Test the circuit*). Use *CHECK* or *INSPECTION* if a noun is needed.

---

## 2. High-Frequency Word Substitutions

| Unapproved Word | Approved STE Word | Approved Example |
| :--- | :--- | :--- |
| **commence** (v) | **START** | *Start the pump.* |
| **initiate** (v) | **START** | *Start the backup procedure.* |
| **terminate** (v) | **STOP** | *Stop the background process.* |
| **abort** (v) | **STOP** | *Stop the deployment immediately.* |
| **ensure** (v) | **MAKE SURE** | *Make sure that the switch is on.* |
| **prior to** (prep) | **BEFORE** | *Disconnect power before you open the box.* |
| **subsequent to** (prep) | **AFTER** | *Check the pressure after the test finishes.* |
| **replenish** (v) | **FILL** | *Fill the reservoir with clean fluid.* |
| **utilize** (v) | **USE** | *Use a calibrated torque wrench.* |
| **employ** (v) | **USE** | *Use the standard protocol.* |
| **approximately** (adv) | **ABOUT** | *Wait for about 10 minutes.* |
| **in order to** (prep) | **TO** | *Remove the cover to get access.* |
| **for the purpose of** | **TO** | *Send a ping to verify connectivity.* |
| **in view of the fact that** | **BECAUSE** | *Replace the seal because it is worn.* |
| **in the event that** | **IF** | *If an error occurs, alert the team.* |
| **as well as** | **AND** | *Save the log file and restart the service.* |
| **obtain** (v) | **GET** | *Get a replacement part from storage.* |
| **retrieve** (v) | **GET** | *Get the latest version from the repository.* |
| **modify** (v) | **CHANGE** | *Change the configuration parameter.* |
| **alter** (v) | **CHANGE** | *Do not change the default settings.* |
| **transmit** (v) | **SEND** | *Send the data over the network.* |
| **indicate** (v) | **SHOW** | *The red light shows high temperature.* |
| **display** (v) | **SHOW** | *The monitor will show the status.* |
| **verify / validate** | **CHECK** | *Check the checksum before execution.* |

---

## 3. Technical Nouns and Verbs Allowance

ASD-STE100 permits organizations to declare specialized vocabulary beyond the base ~900 approved words:

### Technical Nouns
Specific physical parts, software entities, components, and tools:
- Aerospace: *fuselage*, *transponder*, *hydraulics*, *altimeter*, *rudder*.
- Software: *API*, *container*, *database*, *microservice*, *thread*, *buffer*, *socket*, *payload*, *JSON*, *endpoint*.

### Technical Verbs
Verbs that have a precise technical or operational definition:
- *compile*, *authenticate*, *encrypt*, *reindex*, *quarantine*, *serialize*, *instantiate*, *decompress*.

---

## 4. Prohibited Phrasal Verbs

Phrasal verbs (verb + preposition) cause confusion for translation tools, non-native readers, and AI parsing engines. Replace them with single plain verbs:

| Unapproved Phrasal Verb | Approved Replacement | Example |
| :--- | :--- | :--- |
| *spin up* | **start / deploy** | *Deploy three worker instances.* |
| *reach out* | **contact / message** | *Contact the database administrator.* |
| *dive into* | **examine / analyze** | *Analyze the crash dump file.* |
| *kick off* | **start / begin** | *Start the nightly build job.* |
| *circle back* | **review / discuss** | *We will review this issue tomorrow.* |
| *touch base* | **meet / speak** | *Speak with the team lead.* |
| *set up* | **install / configure** | *Configure the development environment.* |
| *carry out* | **perform / execute** | *Execute the diagnostic test.* |

---

## 5. Prohibited AI & Corporate Slop Words

Delete meaningless marketing superlatives, or replace them with measurable empirical facts:

| Prohibited Buzzword | Issue | Remedy |
| :--- | :--- | :--- |
| *seamless / seamlessly* | Vague marketing claim | Delete, or state specific latency / zero-error rate. |
| *robust / robustly* | Overused filler adjective | State exact resilience bounds (e.g., *handles 5,000 req/s*). |
| *cutting-edge* | Meaningless hype | Delete. Name the specific algorithm or standard. |
| *effortless / effortlessly*| Subjective claim | State the number of steps required (*completed in 2 steps*). |
| *blazing-fast* | Subjective filler | State the exact latency in milliseconds (*response time < 15ms*). |
| *state-of-the-art* | Unsubstantiated boast | Delete. Name the benchmark or version. |
| *game-changer* | Empty hyperbole | Delete. State the specific performance delta. |

