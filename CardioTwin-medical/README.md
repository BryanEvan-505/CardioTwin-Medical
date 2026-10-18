# CardioTwin Medical Intelligence + Care

This folder is the **Medical Intelligence + Care** module for the CardioTwin healthcare prototype.

## Prototype status

This is a **prototype**. It is **not a diagnostic system**. It does not diagnose patients, prescribe treatment, or replace professional medical care, clinical judgment, or emergency services.

Future outputs from this module should use cautious wording such as “possible concern”, “potentially relevant condition”, or “medical evaluation may be appropriate”. They must never claim that the system has diagnosed a patient.

## Current scope

The current scope is the **module shell**, a **reusable knowledge-entry data structure**, and an **empty disease collection file**:

- a reusable prototype disclaimer
- a JSON schema for knowledge-base entries, with required source fields
- a Python `KnowledgeEntry` type in `medical_care/knowledge.py`
- `data/diseases.json` — structure only; `entries` is empty (no diseases yet)
- tests for the disclaimer, required sources, allowed categories, and the empty disease file

There is **no** filled disease list, symptom lookup, red-flag engine, problem analyzer, injury guidance, exercise checker, medication system, diet system, API, or frontend in this version. No real medical facts have been added.

## Knowledge-entry structure

Future knowledge (diseases, symptoms, and so on) will use one shared record shape. Each entry has:

- `id` — a stable name for the record
- `category` — one of: `disease`, `symptom`, `red_flag`, `injury`, `diet_guidance`, `general_health_guidance`
- `title` — a short label
- `summary` — short text (not a diagnosis)
- `source_name` — **required** name of a reliable source
- `source_url` — **required** URL of that source

An entry is rejected if source information is missing or if the category is not in the list above. This file describes the shape only; it does not contain medical claims.

## Disease collection (structure only)

`data/diseases.json` is the future home for cardiovascular disease knowledge. Right now it is an **empty** `entries` list.

When records are added later, each one must use `category` = `disease` and must include sources. Planned extra fields (not filled in yet) include `common_symptoms`, `risk_factors`, `relevant_measurements`, `warning_signs`, `general_lifestyle_information`, and `when_medical_evaluation_is_appropriate`.

## Future work

Other components will be added **incrementally**, one small step at a time, including (later):

1. Cardiovascular disease knowledge base
2. Symptom knowledge base
3. Medical red-flag / safety rules
4. Problem analyzer
5. Minor injury / first-aid guidance
6. Exercise safety checker
7. Doctor-confirmed disease management
8. Medication schedule / reminder logic (only for user- or clinician-entered prescriptions)
9. General condition-aware diet guidance
10. Tests for each new component
11. An API-ready interface for the rest of CardioTwin

Medical facts will not be invented. Knowledge-base entries will keep their sources.

## How to run tests

From this folder:

```text
python -m unittest discover -s tests -v
```
