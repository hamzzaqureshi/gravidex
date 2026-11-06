# ASD-STE100 Writing Rules (Issue 9 Summary)

ASD-STE100 (Simplified Technical English) is an international standard maintained by the Simplified Technical English Maintenance Group (STEMG). It comprises 53 writing rules divided into 9 functional sections.

---

## Section 1: Words

- **STE 1.1 — Approved words only**: Use only words approved in the dictionary or declared as valid technical nouns or verbs.
- **STE 1.2 — One word, one part of speech**: Use each approved word only as the part of speech listed in the dictionary. For example, *close* is approved only as a verb; use *near* when an adjective is required.
- **STE 1.3 — One word, one meaning**: Use each approved word only with its defined dictionary meaning. Do not use words with multiple meanings that rely on reader inference.
- **STE 1.4 — Consistency**: Use the same word for the same concept throughout the document. Do not rotate elegant synonyms (e.g., alternating between *check*, *verify*, *confirm*, and *validate*).
- **STE 1.5 — Technical nouns**: Organizations may declare necessary domain nouns (e.g., *transponder*, *actuator*, *API*, *microservice*).
- **STE 1.6 — Technical verbs**: Organizations may declare domain verbs with precise operational definitions (e.g., *quarantine*, *reindex*).
- **STE 1.7 — Unapproved words**: Never use unapproved words when an approved equivalent exists (e.g., replace *utilize* with *use*, *commence* with *start*).
- **STE 1.8 — Phrasal verbs**: Do not construct phrasal verbs by combining a verb and a preposition (e.g., avoid *spin up*, *touch base*, *kick off*, *reach out*). Use a direct verb (*start*, *contact*, *begin*).
- **STE 1.9 — Slang and buzzwords**: Do not use marketing adjectives, buzzwords, or colloquial idioms (e.g., avoid *state-of-the-art*, *seamlessly*, *game-changer*, *robust*).
- **STE 1.10 — Latin abbreviations**: Avoid Latin abbreviations such as *e.g.*, *i.e.*, *etc.* Write full English equivalents (*for example*, *that is*).
- **STE 1.11 — Contractions**: Do not use contractions (*don't*, *can't*, *it's*). Write the full forms (*do not*, *cannot*, *it is*).
- **STE 1.12 — Vague qualifiers**: Avoid vague quantities (*approximately*, *nearly*, *almost*). Use exact values or bounds (*about 10 minutes*, *at least 5 units*).

---

## Section 2: Noun Clusters

- **STE 2.1 — Maximum noun cluster length**: Limit noun clusters (strings of nouns modifying each other) to a maximum of 3 words.
  - Non-STE: *hydraulic reservoir pressure relief valve cover plate* (7 words)
  - Approved STE: *cover plate of the pressure relief valve on the hydraulic reservoir*
- **STE 2.2 — Prepositional relief**: Break long noun chains using explicit prepositions (*of*, *for*, *on*) or hyphens for standard compound adjectives.

---

## Section 3: Verbs

- **STE 3.1 — Imperative mood**: Use the command form (imperative) for instructions and procedural steps (*Close the valve*, *Run the test*).
- **STE 3.2 — Simple present tense**: Use simple present tense to describe normal system states or properties (*The pump supplies fuel*).
- **STE 3.3 — Simple past tense**: Use simple past tense to describe completed operational events (*The safety switch opened*).
- **STE 3.4 — Simple future tense**: Use simple future tense with *will* for expected downstream effects (*The engine will shut down*).
- **STE 3.5 — Infinitive form**: Use the infinitive (*to + verb*) to show purpose or condition (*Turn the key to start the motor*).
- **STE 3.6 — Past participle as adjective**: Use past participles only as descriptive adjectives (*the closed switch*, *the damaged cable*).
- **STE 3.7 — No progressive tenses**: Do not use continuous `-ing` verb tenses (*is running*, *was monitoring*). Use simple present or past (*runs*, *monitored*).
- **STE 3.8 — No perfect tenses**: Do not use compound auxiliary tenses (*has closed*, *had completed*). Use simple past (*closed*, *completed*).
- **STE 3.9 — Active voice in procedures**: Always use active voice in procedures. Passive voice is forbidden in steps.
- **STE 3.10 — Passive voice limits**: Use passive voice in descriptive text only when the actor is unknown or irrelevant (*The unit was installed in 2024*).

---

## Section 4: Sentences

- **STE 4.1 — Procedural sentence length**: Maximum 20 words per sentence in procedures and step-by-step instructions.
- **STE 4.2 — Descriptive sentence length**: Maximum 25 words per sentence in descriptive and explanatory sections.
- **STE 4.3 — Single thought**: Express only one primary instruction or concept per sentence. Split multi-clause compounds into distinct sentences.
- **STE 4.4 — Complete syntax**: Do not omit articles (*a*, *an*, *the*) or subjects to shorten sentences. Omission creates ambiguity.

---

## Section 5: Procedures

- **STE 5.1 — Numbered steps**: Present multi-step procedures in numbered sequential lists.
- **STE 5.2 — Condition before action**: Put conditions, triggers, or prerequisites before the command action.
  - Non-STE: *Disconnect the battery if the temperature exceeds 50 degrees.*
  - Approved STE: *If the temperature exceeds 50 degrees, disconnect the battery.*
- **STE 5.3 — Single action per step**: Give only one action in each procedural step, unless two actions must happen simultaneously.
- **STE 5.4 — Clear feedback**: State the expected confirmation or system feedback immediately after the action step.

---

## Section 6: Descriptive Writing

- **STE 6.1 — Paragraph limit**: Maximum 6 sentences per descriptive paragraph.
- **STE 6.2 — Single topic**: Dedicate each paragraph to exactly one topic.
- **STE 6.3 — Topic sentence first**: Begin each descriptive paragraph with a clear topic sentence.
- **STE 6.4 — Transition logic**: Use simple, explicit logical connectors (*Because*, *Although*, *Then*) rather than archaic phrases (*in view of the fact that*).

---

## Section 7: Safety Instructions

- **STE 7.1 — WARNING**: Use WARNING only when non-compliance creates a risk of death, injury, or severe personal harm.
- **STE 7.2 — CAUTION**: Use CAUTION only when non-compliance creates a risk of equipment damage, data loss, or system outage.
- **STE 7.3 — NOTE**: Use NOTE to provide supplementary operational context without safety implications.
- **STE 7.4 — Command first**: In safety warnings, state the explicit command or prohibition first.
- **STE 7.5 — Risk second**: State the specific consequence or hazard immediately after the command.
  - Format: `WARNING: Do not open the enclosure. High voltage will cause injury.`

---

## Section 8: Punctuation and Word Counts

- **STE 8.1 — Semicolons forbidden**: Semicolons are prohibited in ASD-STE100. Split compound thoughts into separate sentences.
- **STE 8.2 — Standard punctuation**: Use periods, commas, colons, hyphens, and parentheses strictly according to standard rules.
- **STE 8.3 — Hyphenation in modifiers**: Hyphenate compound adjectives preceding nouns (*high-pressure line*, *low-latency link*).
- **STE 8.4 — Lists**: Use vertical bulleted or numbered lists for items in a series of 3 or more.

---

## Section 9: Writing Practices

- **STE 9.1 — Nominalization forbidden**: Do not convert active verbs into heavy Latinate nouns.
  - Non-STE: *Conduct an analysis of the log files.*
  - Approved STE: *Analyze the log files.*
- **STE 9.2 — Pronoun clarity**: Ensure all pronouns (*it*, *this*, *they*) have unmistakable referents within the same sentence or immediate context.
- **STE 9.3 — Standard terminology**: Never invent ad-hoc abbreviations or non-standard acronyms without first defining them.

