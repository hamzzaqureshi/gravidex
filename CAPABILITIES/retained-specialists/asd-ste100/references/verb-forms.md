# ASD-STE100 Verb Forms Matrix & Tense Guide

Section 3 of ASD-STE100 strictly governs verb usage. Misread verbs are the leading cause of procedure errors in aerospace maintenance and LLM instruction parsing.

---

## 1. Approved vs. Unapproved Verb Forms

| Verb Form | Example Sentence | Status | Technical Requirement |
| :--- | :--- | :--- | :--- |
| **Command (Imperative)** | *Close the valve.* | Approved | Required for all procedural steps and direct instructions. |
| **Simple Present** | *The valve closes when pressure rises.* | Approved | Used to describe continuous functions, states, and truths. |
| **Simple Past** | *The safety relay opened.* | Approved | Used to document completed system events and logs. |
| **Simple Future** | *The system will alert the operator.* | Approved | Use *will* only for guaranteed downstream consequences. |
| **Infinitive** | *Turn the knob to release pressure.* | Approved | Allowed to show purpose or condition (*to + verb*). |
| **Past Participle (Adjective)** | *The closed valve stops flow.* | Approved | Allowed only when modifying a noun as an adjective. |
| **Progressive (-ing)** | *The valve is closing.* | NOT approved | Ambiguous timing. Replace with simple present or past. |
| **Present Perfect** | *The valve has closed.* | NOT approved | Ambiguous completion state. Replace with simple past. |
| **Past Perfect** | *The valve had closed before the alarm.* | NOT approved | Compound auxiliary. Replace with *closed* + explicit time connector. |
| **Passive Voice (in steps)** | *The parameter should be set.* | NOT approved | Omits actor. State who performs the action. |

---

## 2. Why Continuous (-ing) Forms Are Forbidden

In English, continuous `-ing` forms (present participle) create three distinct failure modes:
1. **Unclear timing**: Does *"The server is syncing data"* mean the operation is currently taking place, or does it describe a general capability?
2. **Ambiguity between verb and noun**: In *"Flushing buffer causes delay"*, is *flushing* an action or the subject noun?
3. **Parsing overhead for AI agents**: Downstream LLMs frequently misparse dangling participles, attaching them to the wrong subject.

### The Single Exception: Established Technical Nouns
You may use the `-ing` form ONLY when it forms an established technical noun or name:
- Approved: *landing gear*, *operating system*, *clustering algorithm*, *sampling rate*, *indexing service*.
- Forbidden: *The service is clustering the nodes.* (Rewrite: *The service clusters the nodes.*)

---

## 3. Why Perfect Tenses (have/has/had) Are Forbidden

Compound perfect tenses (*has written*, *have received*, *had failed*) introduce uncertainty about when the action concluded and whether it remains valid:
- Non-STE: *The worker service has processed the event.*
- Problem: Did it finish just now? Is it still processing?
- Approved STE: *The worker service processed the event.* (Definite past action)

---

## 4. Passive Voice Disambiguation

Passive voice obscures the actor. In agent execution, omitting the actor causes fatal failures:
- Non-STE: *The authentication token must be refreshed after 3600 seconds.*
  - Agent dilemma: Does the client refresh the token, or does the authentication server refresh it automatically?
- Approved STE: *The client must refresh the authentication token after 3600 seconds.*
  - Actor is explicitly identified as *The client*.

### Allowed Passive Voice in Descriptive Text
Passive voice is permitted ONLY in descriptive text when the actor is genuinely unknown or irrelevant to the reader:
- Example: *The titanium bracket was fabricated in 2023.* (The manufacturing technician does not affect the operation).
- Even in descriptive text, prefer active voice whenever the actor can be named.

---

## 5. Auxiliary and Modal Verbs

ASD-STE100 limits modal verbs to prevent hedging:
- **CAN**: Indicates physical or logical capability (*The pump can deliver 50 liters per minute*).
- **MUST**: Indicates an absolute operational requirement (*You must wear protective gloves*).
- **DO NOT**: Clear operational prohibition (*Do not open the valve*).
- **MAY**: Permitted only to express formal authorization or possibility (*The administrator may grant read permissions*).
- **Avoid**: *should*, *could*, *might*, *ought to*. These indicate subjective advice or weak recommendations that create confusion.

