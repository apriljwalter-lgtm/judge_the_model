# Decisions

<!-- Fill in each section at the step the activity website gives, then commit and push.
     Write each answer after its label. Keep the headings and labels exactly as they are:
     `python -m analysis` reads them. Limit: 150 words for Before results.
     Fill in Recommendations and Design choice and AI use last, once your app is built. -->

## Before results
For each dataset: positive class; which error matters more for the job (missed positive or false alarm) and why.
- readmission: Postive class is patient readmitted within 30 days; false alarm is more costly to the hospital based on the follow up that may occur. If a patient is missed to be flagged for readmission it won't matter because they can still get readmitted and receive the care they would need. 
- diabetes: Positive class is (`target` = 1):** Diabetes (reported doctor diagnosis or HbA1c ≥ 6.5%); missed positive is more costly to the patient's health overall because there can be serious consequences to missing a diabetes diagnosis related to the impacts the disease has on the body when not treated. 

## Recommendations
- readmission: <model and threshold, or "none is adequate for this job"> because ...
- diabetes: ...

## Design choice and AI use
A few sentences each. The design choice must be your own idea, not an AI tool's.
- design choice: <one thing you chose to show, or leave out, for your clinical lead> because ...
- AI suggestion I turned down: <what an AI tool suggested, and why you didn't use it, or "no AI tools used">
