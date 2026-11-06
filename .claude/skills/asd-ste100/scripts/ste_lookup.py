#!/usr/bin/env python3
"""ASD-STE100 Offline Vocabulary Lookup Tool.

Deterministic lookup tool for approved Simplified Technical English words,
unapproved synonyms, and common replacements under Issue 9 (January 2025).

Zero external dependencies (pure Python standard library).
"""

import argparse
import json
import sys

# High-frequency dictionary mapping:
# Key: unapproved term (lowercase)
# Value: dict of approved replacement, part of speech, notes, and approved example
DICTIONARY = {
    "commence": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "START",
        "approved_pos": "verb",
        "example": "Start the pump.",
        "note": "Use start for all initial actions."
    },
    "initiate": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "START",
        "approved_pos": "verb",
        "example": "Start the backup routine.",
        "note": "Initiate is not approved."
    },
    "terminate": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "STOP",
        "approved_pos": "verb",
        "example": "Stop the background process.",
        "note": "Use stop rather than terminate, abort, or cease."
    },
    "abort": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "STOP",
        "approved_pos": "verb",
        "example": "Stop the test immediately.",
        "note": "Use stop."
    },
    "ensure": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "MAKE SURE",
        "approved_pos": "verb phrase",
        "example": "Make sure that the switch is in the OFF position.",
        "note": "Ensure is not approved in ASD-STE100."
    },
    "prior to": {
        "status": "unapproved",
        "part_of_speech": "preposition",
        "approved": "BEFORE",
        "approved_pos": "preposition / conjunction",
        "example": "Disconnect power before you open the cabinet.",
        "note": "Prior to is unapproved."
    },
    "subsequent to": {
        "status": "unapproved",
        "part_of_speech": "preposition",
        "approved": "AFTER",
        "approved_pos": "preposition / conjunction",
        "example": "Check pressure after the cycle finishes.",
        "note": "Subsequent to is unapproved."
    },
    "replenish": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "FILL",
        "approved_pos": "verb",
        "example": "Fill the reservoir with approved hydraulic fluid.",
        "note": "Replenish is not approved."
    },
    "utilize": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "USE",
        "approved_pos": "verb",
        "example": "Use a calibrated torque wrench.",
        "note": "Never use utilize when use is available."
    },
    "employ": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "USE",
        "approved_pos": "verb",
        "example": "Use the standard procedure.",
        "note": "Employ in the sense of using is unapproved."
    },
    "approximately": {
        "status": "unapproved",
        "part_of_speech": "adverb",
        "approved": "ABOUT",
        "approved_pos": "preposition / adverb",
        "example": "Wait for about 10 minutes.",
        "note": "Approximately is unapproved. Use about or give exact tolerances."
    },
    "in order to": {
        "status": "unapproved",
        "part_of_speech": "prepositional phrase",
        "approved": "TO",
        "approved_pos": "preposition",
        "example": "Remove the cover to get access to the filter.",
        "note": "In order to is unapproved word bloat."
    },
    "for the purpose of": {
        "status": "unapproved",
        "part_of_speech": "prepositional phrase",
        "approved": "TO",
        "approved_pos": "preposition",
        "example": "Send a test ping to verify connectivity.",
        "note": "Use to."
    },
    "in view of the fact that": {
        "status": "unapproved",
        "part_of_speech": "conjunction",
        "approved": "BECAUSE",
        "approved_pos": "conjunction",
        "example": "Replace the o-ring because it is damaged.",
        "note": "Use because."
    },
    "in the event that": {
        "status": "unapproved",
        "part_of_speech": "conjunction",
        "approved": "IF",
        "approved_pos": "conjunction",
        "example": "If the red light illuminates, shut down the engine.",
        "note": "Use if."
    },
    "as well as": {
        "status": "unapproved",
        "part_of_speech": "conjunction",
        "approved": "AND",
        "approved_pos": "conjunction",
        "example": "Inspect the cable and clean the connector.",
        "note": "Use and."
    },
    "obtain": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "GET",
        "approved_pos": "verb",
        "example": "Get a replacement gasket from stores.",
        "note": "Use get."
    },
    "retrieve": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "GET",
        "approved_pos": "verb",
        "example": "Get the file from the remote server.",
        "note": "Use get unless retrieve is a declared technical verb."
    },
    "modify": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "CHANGE",
        "approved_pos": "verb",
        "example": "Change the configuration value to 100.",
        "note": "Use change."
    },
    "alter": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "CHANGE",
        "approved_pos": "verb",
        "example": "Do not change the factory calibration settings.",
        "note": "Use change."
    },
    "transmit": {
        "status": "unapproved",
        "part_of_speech": "verb",
        "approved": "SEND",
        "approved_pos": "verb",
        "example": "Send the diagnostic telemetry packet.",
        "note": "Use send."
    },
    "close (adj)": {
        "status": "unapproved",
        "part_of_speech": "adjective",
        "approved": "NEAR",
        "approved_pos": "adjective / preposition",
        "example": "Put the tool near the inspection hatch.",
        "note": "CLOSE is approved only as a verb ('Close the door'). Use near for proximity."
    },
    "test": {
        "status": "approved",
        "part_of_speech": "verb",
        "approved": "TEST",
        "approved_pos": "verb",
        "example": "Test the emergency brake system.",
        "note": "Approved verb. Use CHECK or INSPECTION if a noun is needed."
    },
    "close": {
        "status": "approved",
        "part_of_speech": "verb",
        "approved": "CLOSE",
        "approved_pos": "verb",
        "example": "Close the access hatch.",
        "note": "Approved verb. To move together or stop flow. Not approved as adjective."
    }
}


def lookup_word(term: str):
    normalized = term.strip().lower()
    if normalized in DICTIONARY:
        return normalized, DICTIONARY[normalized]
    # Check if user entered an approved uppercase word
    upper = term.strip().upper()
    for k, v in DICTIONARY.items():
        if v.get("approved") == upper:
            return k, v
    return None, None


def main():
    parser = argparse.ArgumentParser(
        prog="ste_lookup.py",
        description="Lookup words in the ASD-STE100 Issue 9 vocabulary database."
    )
    parser.add_argument("term", nargs="?", help="Word or phrase to look up")
    parser.add_argument("--all", action="store_true", help="List all registered entries")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.all:
        if args.json:
            print(json.dumps(DICTIONARY, indent=2))
        else:
            print(f"ASD-STE100 Vocabulary Registry ({len(DICTIONARY)} core entries):")
            print("=" * 68)
            for k, v in sorted(DICTIONARY.items()):
                status = v["status"].upper()
                approved = v["approved"]
                print(f"[{status:10}] {k:<25} -> {approved:<12} (e.g. {v['example']})")
        return 0

    if not args.term:
        parser.print_help()
        return 1

    term, entry = lookup_word(args.term)
    if not entry:
        if args.json:
            print(json.dumps({"term": args.term, "found": False}))
        else:
            print(f"Term '{args.term}' not found in high-frequency vocabulary table.")
            print("Under ASD-STE100, if not in the official dictionary, treat as unapproved unless declared as a technical noun/verb.")
        return 1

    if args.json:
        data = {"term": term, "found": True}
        data.update(entry)
        print(json.dumps(data, indent=2))
    else:
        status_label = "APPROVED VERB" if entry["status"] == "approved" else "UNAPPROVED"
        print(f"Term: {term}")
        print(f"Status: {status_label}")
        print(f"Part of Speech: {entry['part_of_speech']}")
        print(f"Approved Alternative: {entry['approved']} ({entry['approved_pos']})")
        print(f"Approved Example: {entry['example']}")
        print(f"Usage Note: {entry['note']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
