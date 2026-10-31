"""Starter app for Streamlit Community Cloud: three plain sections that read results/ and show correct numbers.

Run locally:  bash run_app.sh  (your agent writes it; it runs streamlit run streamlit_app.py)
Build each section up to its required minimum (see the activity website). Keep every number
coming from m11.py, and label every table and plot "Training" or "Test".
"""

import math
from html import escape

import streamlit as st

import m11

TRAIN = "Training"
TEST = "Test"
SECTIONS = ["Beyond Accuracy", "A Threshold for the Job", "Training vs. Test"]  # ?section=1/2/3 in the address

# Jewel-tone palette (the base theme colours are in .streamlit/config.toml).
SAPPHIRE, EMERALD, RUBY, TOPAZ, AMETHYST = "#1E4D8C", "#0B6E4F", "#9B1B30", "#9A4A00", "#5B2A86"
# Golden topaz: bright gold for fills (with a darker-gold edge so it shows on white); TOPAZ above is its text shade.
TOPAZ_FILL, TOPAZ_EDGE, TOPAZ_TINT = "#F2B705", "#B8860B", "#FFF4CC"
INK, MUTED = "#2B1D3A", "#5A5266"
TRAIN_FILL = TRAIN_TEXT = EMERALD  # Section 3: Training is emerald, Test is sapphire

st.set_page_config(page_title="Judge the Model", layout="wide")

# Fonts and the shared styles of the custom HTML blocks. Only text elements get the new font, so
# Streamlit's icon font is left alone.
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400..600,0..1,0&display=block');
.ms {{font-family: 'Material Symbols Rounded'; font-weight: normal; font-style: normal; font-size: 1.15em; line-height: 1;
  vertical-align: -.2em; font-variation-settings: 'FILL' 1, 'wght' 500; display: inline-block; -webkit-font-smoothing: antialiased;}}
.jt-hero {{position: relative; overflow: hidden; border-radius: 16px; padding: 1.5rem 1.8rem 3.1rem; margin-bottom: .9rem; color: #fff;
  background: linear-gradient(110deg, {EMERALD} 0%, {SAPPHIRE} 52%, {AMETHYST} 100%); box-shadow: 0 8px 24px rgba(43, 29, 58, .18);}}
.jt-hero svg {{position: absolute; left: 0; right: 0; bottom: 6px; width: 100%; height: 38px; opacity: .35; pointer-events: none;}}
.jt-hero .title {{position: relative; font-family: 'Fraunces', serif; font-size: 2.6rem; font-weight: 700; line-height: 1.1;
  display: flex; align-items: center; gap: .6rem;}}
.jt-hero .title .ms {{font-size: 2.6rem; background: rgba(255, 255, 255, .18); border-radius: 50%; padding: .35rem;}}
.jt-hero .sub {{position: relative; margin-top: .45rem; font-size: 1rem; opacity: .95; max-width: 46rem;}}
.jt-group .t .ms {{font-size: 1.25em; margin-right: .15rem;}}
.jt-strip b .ms {{font-size: 1.2em; margin-right: .2rem;}}
.jt-rec {{padding: .5rem .9rem;}} .jt-rec code {{font-size: .78rem;}}
.stApp :is(p, li, label, td, th, input) {{font-family: 'DM Sans', sans-serif;}}
.stApp :is(h1, h2, h3, h4) {{font-family: 'Fraunces', serif !important; letter-spacing: -0.01em;}}
.stApp h1 {{background: linear-gradient(90deg, {EMERALD}, {SAPPHIRE} 50%, {AMETHYST}); -webkit-background-clip: text;
  background-clip: text; color: transparent;}}
.stApp :is(h2, h3) {{color: {EMERALD};}}
.stApp h4 {{color: {INK}; padding: .2rem 0 0;}}
[data-testid="stMainBlockContainer"] {{padding-top: 2.5rem;}}
.jt-strip {{display: flex; flex-wrap: wrap; gap: .5rem 1rem; background: #F3EEF8; border-left: 6px solid {AMETHYST};
  border-radius: 10px; padding: .55rem 1rem; color: {INK};}}
.jt-strip div {{flex: 1 1 200px;}}
.jt-strip b {{display: block; font-size: .78rem; color: {MUTED}; font-weight: 600;}}
.jt-strip small {{color: {MUTED};}}
[data-testid="stMetric"] {{background: #F3EEF8; border-left: 6px solid {AMETHYST}; border-radius: 10px; padding: .6rem 1rem;}}
:is([class*="st-key-s1card-"], [class*="st-key-s3card-"]) {{position: relative;}}
:is([class*="st-key-s1pick-"], [class*="st-key-s3pick-"]) {{position: absolute; inset: 0; z-index: 3;}}
:is([class*="st-key-s1pick-"], [class*="st-key-s3pick-"]) :is(div, button) {{width: 100%; height: 100%;}}
:is([class*="st-key-s1pick-"], [class*="st-key-s3pick-"]) button {{background: transparent; border: none; color: transparent;
  cursor: pointer; border-radius: 12px;}}
:is([class*="st-key-s1pick-"], [class*="st-key-s3pick-"]) button:hover {{background: rgba(91, 42, 134, .07);}}
:is([class*="st-key-s1pick-"], [class*="st-key-s3pick-"]) button:focus-visible {{outline: 3px dashed {AMETHYST}; outline-offset: 2px;}}
.jt-au {{display: flex; flex-wrap: wrap; gap: .5rem 1.6rem; margin: .2rem 0 .6rem;}}
.jt-au > div > span {{display: block; font-size: .74rem; font-weight: 600; text-transform: uppercase; letter-spacing: .04em;
  white-space: nowrap;}}
.jt-au .v {{font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 700; line-height: 1.1;}}
.jt-au .v.sm {{font-size: 1.25rem;}}
.jt-bars {{display: grid; grid-template-columns: auto 1fr auto; gap: .35rem .6rem; align-items: center; font-size: .8rem;
  font-variant-numeric: tabular-nums;}}
.jt-bars .track {{background: #EEE9F3; height: 10px; border-radius: 6px; overflow: hidden;}}
.jt-bars .fill {{height: 100%; border-radius: 6px;}}
.jt-scale {{display: flex; justify-content: space-between; font-size: .7rem; color: {MUTED}; margin: .15rem 0 0;}}
.jt-plain {{margin: .7rem 0 0; font-size: .88rem; color: {INK}; line-height: 1.45;}}
.jt-card {{border: 1px solid #D9D2E3; border-radius: 12px; padding: .7rem; background: #fff;}}
.jt-scroll {{margin-bottom: 1rem;}}
@media (max-width: 900px) {{ .jt-scroll {{overflow-x: auto;}} }}  /* scroll only when narrow, so tips aren't clipped */
.jt-tip {{position: relative; display: inline-block; cursor: help; font-weight: 400; font-size: .9em; opacity: .85;}}
.jt-tip:is(:hover, :focus) {{opacity: 1;}}
.jt-tip:focus-visible {{outline: 2px solid {AMETHYST}; outline-offset: 2px; border-radius: 4px;}}
.jt-tiptext {{visibility: hidden; opacity: 0; transition: opacity .15s; position: absolute; z-index: 50;
  bottom: calc(100% + 6px); left: 50%; transform: translateX(-50%); width: 260px; padding: .55rem .7rem;
  background: {INK}; color: #fff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0, 0, 0, .25);
  font-family: 'DM Sans', sans-serif; font-size: .8rem; font-weight: 400; line-height: 1.4; text-align: left;
  text-transform: none; letter-spacing: normal; white-space: normal;}}
.jt-tip.l .jt-tiptext {{left: 0; transform: none;}}
.jt-tip.r .jt-tiptext {{left: auto; right: 0; transform: none;}}
.jt-tip:is(:hover, :focus, :focus-within) .jt-tiptext {{visibility: visible; opacity: 1;}}
.jt-table {{width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums;}}
.jt-table {{font-size: .92rem;}}
.jt-table th {{background: {SAPPHIRE}; color: #fff; padding: .45rem .6rem; text-align: right; font-weight: 600; line-height: 1.25;}}
.jt-table td {{padding: .4rem .6rem; text-align: right; border-bottom: 1px solid #E6E0EE; color: {INK};}}
.jt-table :is(th, td):first-child {{text-align: left;}}
.jt-table tr.selected td {{font-weight: 700; background: #F3EEF8; border-top: 4px solid {AMETHYST}; border-bottom: 4px solid {AMETHYST};}}
.jt-table tr.selected td:first-child {{border-left: 4px solid {AMETHYST};}}
.jt-table tr.selected td:last-child {{border-right: 4px solid {AMETHYST};}}
.jt-banner {{display: flex; flex-wrap: wrap; justify-content: space-between; gap: .4rem 1.5rem; color: #fff;
  background: linear-gradient(100deg, {AMETHYST}, {SAPPHIRE}); border-radius: 12px; padding: .8rem 1.2rem; margin-bottom: .4rem;}}
.jt-banner span {{font-size: .78rem; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; opacity: .9;}}
.jt-banner .name {{font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 700; line-height: 1.15;}}
.jt-banner small {{display: block; font-size: .8rem; opacity: .9; max-width: 22rem;}}
.jt-banner .note {{flex-basis: 100%; background: rgba(255, 255, 255, .16); border-radius: 8px; padding: .45rem .7rem; font-size: .88rem;}}
.jt-gt {{display: grid; align-items: stretch; font-size: .92rem; font-variant-numeric: tabular-nums; border-radius: 4px;}}
.jt-gt > div {{padding: .45rem .6rem; text-align: right; border-bottom: 1px solid #E6E0EE; color: {INK};}}
.jt-gt > div:first-child {{text-align: left;}}
.jt-gt.head > div {{background: {SAPPHIRE}; color: #fff; font-weight: 600; border-bottom: none; line-height: 1.25;}}
.jt-gt.head > div:first-child {{border-radius: 8px 0 0 0;}} .jt-gt.head > div:last-child {{border-radius: 0 8px 0 0;}}
.jt-gt.sel {{outline: 3px solid {AMETHYST}; outline-offset: -3px; background: #F3EEF8;}}
.jt-gt.sel > div {{font-weight: 700;}}
@media (max-width: 760px) {{ .jt-gt {{font-size: .72rem;}} .jt-gt > div {{padding: .35rem .25rem;}} }}
.jt-table th.chosen {{background: {AMETHYST};}}
.jt-table td.chosen {{background: #F3EEF8; font-weight: 700;}}
.jt-card.selected {{border: 4px solid {AMETHYST}; box-shadow: 0 4px 14px rgba(91, 42, 134, .28);}}
.jt-card h4 {{font-size: 1.05rem; margin: 0 0 .4rem; padding: 0; color: {INK};}}
.jt-mx {{width: 100%; border-collapse: separate; border-spacing: 4px; font-variant-numeric: tabular-nums;}}
.jt-mx th {{font-size: .7rem; color: {MUTED}; font-weight: 600; text-align: center; border: none; padding: 0; line-height: 1.15;}}
.jt-mx td {{text-align: center; border-radius: 8px; padding: .45rem .15rem; font-weight: 700; border: none; font-size: .88rem;
  white-space: nowrap;}}
.jt-card:not(.selected) h4 {{min-height: 2.4em; line-height: 1.2;}}  /* room for a two-line name: every small card the same height */
.jt-mini-title {{font-weight: 700; font-size: .85rem; color: {INK}; margin: .2rem 0 .45rem;}}
.jt-note {{font-size: .72rem; color: {MUTED}; margin-top: .3rem;}}
.jt-split {{display: flex; flex-wrap: wrap; gap: .4rem 1.4rem; align-items: flex-start; margin-top: .7rem;}}
.jt-split .jt-facts {{flex: 1 1 300px; margin-top: 0;}}
.jt-dots-wrap {{flex: 0 0 auto;}}
.jt-dots {{display: grid; grid-template-columns: repeat(10, 13px); gap: 4px; margin-bottom: .55rem;}}
:is(.jt-dots, .jt-legend) i {{display: inline-block; width: 13px; height: 13px; border-radius: 50%; box-sizing: border-box;}}
:is(.jt-dots, .jt-legend) i.tp {{background: {EMERALD};}}
:is(.jt-dots, .jt-legend) i.fn {{background: {RUBY};}}
:is(.jt-dots, .jt-legend) i.fp {{background: {TOPAZ_FILL}; border: 1.5px solid {TOPAZ_EDGE};}}
:is(.jt-dots, .jt-legend) i.tn {{border: 2px solid {SAPPHIRE}; opacity: .55;}}
.jt-legend {{font-size: .78rem; color: {INK}; display: grid; gap: .2rem;}}
.jt-legend div {{display: flex; align-items: center; gap: .4rem;}}
.jt-legend small {{color: {MUTED};}}
.jt-legend.inline {{display: flex; flex-wrap: wrap; gap: .3rem 1.2rem; margin: .4rem 0 1rem;}}
.jt-legend i.dot-train {{background: {TRAIN_FILL};}}
.jt-legend i.dot-test {{background: {SAPPHIRE};}}
.jt-hb-row {{display: grid; grid-template-columns: 11rem 1fr; gap: .8rem; align-items: center; margin: .3rem 0;}}
.jt-hb-row .lbl {{font-size: .85rem; font-weight: 600; color: {INK};}}
.jt-hb {{display: flex; height: 30px; border-radius: 8px; overflow: hidden; font-size: .8rem; font-weight: 700;
  font-variant-numeric: tabular-nums; transition: all .2s;}}
.jt-hb div {{display: flex; align-items: center; justify-content: center; color: #fff; transition: width .25s ease;}}
.jt-hb .tp {{background: {EMERALD};}} .jt-hb .fn {{background: {RUBY};}} .jt-hb .fp {{background: {TOPAZ_FILL}; color: {INK};}}
.jt-hb .tn {{background: #E3EBF6; color: {SAPPHIRE};}}
.jt-hb-row {{row-gap: .2rem;}}
.jt-hb-vals {{font-size: .78rem; color: {INK}; font-variant-numeric: tabular-nums; margin-bottom: .35rem;}}
.jt-hb-vals small {{color: {MUTED};}}
.jt-hb-vals i {{display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: .3rem; vertical-align: -1px;}}
.jt-hb-vals i.tp {{background: {EMERALD};}} .jt-hb-vals i.fn {{background: {RUBY};}}
.jt-hb-vals i.fp {{background: {TOPAZ_FILL}; border: 1px solid {TOPAZ_EDGE};}} .jt-hb-vals i.tn {{background: #E3EBF6; border: 1px solid {SAPPHIRE};}}
.jt-legend.inline i.tp {{background: {EMERALD};}} .jt-legend.inline i.fn {{background: {RUBY};}}
.jt-legend.inline i.fp {{background: {TOPAZ_FILL}; border: 1.5px solid {TOPAZ_EDGE};}} .jt-legend.inline i.tn {{background: #E3EBF6; border: 1px solid {SAPPHIRE};}}
.jt-ab {{margin-bottom: 1rem;}}
.jt-ab-row {{display: grid; grid-template-columns: 11rem 1fr 4.2rem 1fr 7rem; gap: .7rem; align-items: center;
  padding: .3rem .5rem; border-radius: 8px; font-size: .85rem; font-variant-numeric: tabular-nums;}}
.jt-ab-row.head {{font-size: .75rem; font-weight: 600; color: {MUTED}; padding-bottom: 0;}}
.jt-ab-row.sel {{outline: 3px solid {AMETHYST}; background: #F3EEF8; font-weight: 700;}}
.jt-ab-row .val {{text-align: right;}}
.jt-track {{position: relative; height: 14px; background: #EEE9F3; border-radius: 7px;}}
.jt-track .fill {{height: 100%; border-radius: 7px;}}
.jt-track .fill.acc {{background: {SAPPHIRE};}}
.jt-track .fill.catch {{background: {EMERALD};}}
.jt-track .mark {{position: absolute; top: -4px; bottom: -4px; border-left: 2px dashed {INK};}}
.jt-db {{margin-bottom: .2rem;}}
.jt-db-row {{display: grid; grid-template-columns: 11rem 1fr 17rem; gap: .9rem; align-items: center; padding: .3rem .5rem;
  border-radius: 8px; font-size: .85rem; font-variant-numeric: tabular-nums;}}
.jt-db-row.sel {{outline: 3px solid {AMETHYST}; background: #F3EEF8; font-weight: 700;}}
.jt-db-row .val {{font-size: .8rem; color: {INK};}}
.jt-db-row .val .tr {{color: {MUTED};}} .jt-db-row .val .te {{color: {SAPPHIRE}; font-weight: 700;}}
.jt-db-track {{position: relative; height: 22px; margin: 0 9px;}}
.jt-db-track::before {{content: ""; position: absolute; left: 0; right: 0; top: 50%; border-top: 1px dashed #D9D2E3;}}
.jt-db-track .line {{position: absolute; top: 50%; height: 4px; transform: translateY(-50%); background: #C9BFD8; border-radius: 2px;}}
.jt-db-track .dot {{position: absolute; top: 50%; width: 16px; height: 16px; border-radius: 50%; transform: translate(-50%, -50%);
  border: 2px solid #fff; box-shadow: 0 0 0 1px rgba(0, 0, 0, .18);}}
.jt-db-track .dot.train {{background: {TRAIN_FILL};}}
.jt-db-track .dot.test {{background: {SAPPHIRE};}}
.jt-db-row .val .tr {{color: {TRAIN_TEXT}; font-weight: 600;}}
.jt-db-row.axis {{padding-top: 0;}}
.jt-db-ticks {{position: relative; height: 1.1rem; margin: 0 9px; font-size: .7rem; color: {MUTED};}}
.jt-db-ticks span {{position: absolute; transform: translateX(-50%);}}
.jt-db-row.axis .val {{font-size: .7rem; color: {MUTED};}}
@media (max-width: 760px) {{ .jt-ab-row, .jt-db-row {{grid-template-columns: 1fr;}} .jt-hb-row {{grid-template-columns: 1fr;}} }}
.jt-tag {{font-family: 'DM Sans', sans-serif; font-size: .72rem; font-weight: 600; color: #fff; background: {AMETHYST};
  border-radius: 999px; padding: .15rem .55rem; vertical-align: middle; margin-left: .3rem;}}
.jt-facts {{margin: .7rem 0 0; padding-left: 1.1rem; font-size: .85rem; color: {INK};}}
.jt-facts li {{margin: .15rem 0;}}
.jt-fm {{display: grid; grid-template-columns: minmax(80px, .8fr) 1fr 1fr; gap: .5rem; align-items: stretch; font-size: .85rem;}}
.jt-fm .jt-head {{font-weight: 700; color: {INK}; align-self: end; line-height: 1.25;}}
.jt-fm .jt-head span, .jt-fm .jt-row span {{display: block; font-weight: 400; color: {MUTED}; font-size: .78rem;}}
.jt-fm .jt-row {{font-weight: 700; color: {INK}; align-self: center; line-height: 1.25;}}
.jt-group {{border-radius: 10px; padding: .5rem .7rem; border-left: 6px solid;}}
.jt-group .t {{font-weight: 700; font-size: .74rem; text-transform: uppercase; letter-spacing: .04em;}}
.jt-group .n {{font-family: 'Fraunces', serif; font-size: 1.55rem; font-weight: 700; line-height: 1.15;}}
.jt-group .n small {{font-family: 'DM Sans', sans-serif; font-size: .8rem; font-weight: 400;}}
.jt-group .d {{color: {INK}; font-size: .78rem; line-height: 1.3;}}
@media (max-width: 640px) {{ .jt-fm {{grid-template-columns: 1fr;}} .jt-fm :is(.jt-blank, .jt-head) {{display: none;}} }}
</style>""", unsafe_allow_html=True)


@st.cache_data
def load(name: str):
    return m11.load(name)


def recommendation(dataset: str) -> None:
    """The selected dataset's line from results/decisions.json (read fresh, so a rerun of the analysis shows up)."""
    recs = (m11.load("decisions") or {}).get("recommendations", {})
    text = recs.get(dataset)
    body = (escape(text) if text else
            "<small>Not written yet: fill in <code>Recommendations</code> in DECISIONS.md, run "
            "<code>python -m analysis</code>, then commit and push.</small>")
    html(f'<div class="jt-strip jt-rec"><div><b>{icon("clinical_notes")}Recommendation · '
         f'{escape(m11.DATASET_LABEL[dataset])}</b>{body}</div></div>')


# ---- 1. Beyond Accuracy ------------------------------------------------------
THRESHOLD = 0.5

# Words only (no numbers): the positive class of each job, and how to say "had it" / "didn't" in a sentence.
OUTCOME = {
    "readmission": {"positive": "Readmitted within 30 days of discharge", "unit": "patients",
                    "had": "were readmitted within 30 days", "not": "were not readmitted within 30 days"},
    "diabetes": {"positive": "Diabetes (reported doctor diagnosis or HbA1c ≥ 6.5%)", "unit": "adults",
                 "had": "had diabetes", "not": "did not have diabetes"},
}


# The four groups of patients: code, name, jewel tone, tint behind it.
GROUPS = {"tp": ("TP", "Caught", EMERALD, "#E2F3EC"), "fn": ("FN", "Missed", RUBY, "#F8E3E7"),
          "fp": ("FP", "False alarm", TOPAZ, TOPAZ_TINT), "tn": ("TN", "Correctly not flagged", SAPPHIRE, "#E3EBF6")}


def html(block: str) -> None:
    st.markdown(block, unsafe_allow_html=True)


# Material Symbols icons (the set Streamlit itself uses): in HTML blocks via icon(), in labels as :material/name:.
SECTION_ICON = dict(zip(SECTIONS, ["fact_check", "tune", "school"]))
DATASET_ICON = {"readmission": "bed", "diabetes": "bloodtype"}
GROUP_ICON = {"tp": "check_circle", "fn": "cancel", "fp": "notifications_active", "tn": "verified_user"}


def icon(name: str) -> str:
    return f'<span class="ms" aria-hidden="true">{name}</span>'


def tips(o: dict) -> dict:
    """Hover text for each number: what it means, its denominator in words, and what higher or lower means.
    Words only: no number is typed here."""
    return {
        "prevalence": f"Of all the test patients, the share who {o['had']}. The rarer the outcome, the easier it is "
                      "for a model to look accurate while rarely flagging anyone.",
        "majority": "The accuracy you get by giving every patient the more common answer, without looking at any "
                    "patient data. A model's accuracy only means something when compared with this.",
        "accuracy": "Of all patients, the share the model put in the right group (caught or correctly not flagged). "
                    "When the outcome is rare, a model can score high accuracy while missing most of the patients "
                    "who have it, so compare it with “the most common class for everyone”.",
        "sensitivity": f"Also called recall or true positive rate (TPR). Of the patients who {o['had']}, the share the "
                       "model flagged. Higher means fewer missed patients, usually at the cost of more false alarms.",
        "specificity": f"Of the patients who {o['not']}, the share the model did not flag. Higher means fewer false "
                       "alarms, usually at the cost of more missed patients.",
        "fpr": f"False positive rate, equal to 1 − specificity. Of the patients who {o['not']}, the share the model "
               "flagged anyway. Lower means fewer false alarms.",
        "precision": f"Of the patients the model flagged, the share who {o['had']}. Higher means fewer of the flags "
                     "are false alarms, so less follow-up effort goes to patients who didn't need it. Undefined when "
                     "no one is flagged.",
        "f1": "Combines precision and sensitivity into one score from 0 to 1 (their harmonic mean). It is high only "
              "when both are high, and it ignores the patients correctly not flagged.",
        "tp": f"Patients who {o['had']} and were flagged: the cases the model catches.",
        "fn": f"Patients who {o['had']} but were not flagged: missed cases. None of them would get the follow-up a "
              "flag would trigger.",
        "fp": f"Patients who {o['not']} but were flagged: false alarms. Each may get follow-up they didn't need.",
        "tn": f"Patients who {o['not']} and were not flagged: correctly left alone.",
        "flagged100": f"Out of every 100 {o['unit']}, how many the model flags for follow-up. Higher means more "
                      "follow-up work: more patients caught, but also more false alarms.",
        "fa100": f"Out of every 100 {o['unit']}, how many are flagged although they {o['not']}. Each is follow-up "
                 "that turns out not to be needed. Lower is better, but lowering it usually means missing more patients.",
        "auroc": f"AUROC describes ranking. Pick one of the patients who {o['had']} and one of those who {o['not']}: "
                 "AUROC is how often the first gets the higher probability. It is not accuracy, and it doesn't choose "
                 "a threshold. The slider can't change it, because no probability changes.",
    }


def tip(text: str, side: str = "") -> str:
    """A small ⓘ that shows `text` on hover or keyboard focus. side "l"/"r" pins the box's left/right edge."""
    return (f'<span class="jt-tip {side}" tabindex="0" aria-label="{escape(text)}">ⓘ'
            f'<span class="jt-tiptext" role="tooltip">{escape(text)}</span></span>')


def cell(c: dict, k: str) -> str:
    code, _, fg, bg = GROUPS[k]
    return f'<td style="background:{bg};color:{fg}">{code} {c[k]:,}</td>'


def small_matrix(title: str, c: dict, selected: bool = False) -> str:
    """A compact confusion matrix card: rows are the actual outcome, columns the prediction at the threshold."""
    return (f'<div class="jt-card{" selected" if selected else ""}"><h4>{escape(title)}</h4><table class="jt-mx">'
            '<tr><th></th><th>Predicted +</th><th>Predicted −</th></tr>'
            f'<tr><th>Actual +</th>{cell(c, "tp")}{cell(c, "fn")}</tr>'
            f'<tr><th>Actual −</th>{cell(c, "fp")}{cell(c, "tn")}</tr></table></div>')


ORDER = ("tp", "fn", "fp", "tn")  # patients with the outcome first (caught, missed), then those without


def per_100_whole(c: dict) -> dict:
    """The four counts scaled to 100 patients and rounded to whole patients so they add up to exactly 100
    (largest remainder: the leftover patients go to the groups whose exact share was rounded down the most)."""
    n = sum(c[k] for k in ORDER)
    exact = {k: 100 * c[k] / n for k in ORDER}
    whole = {k: math.floor(exact[k]) for k in ORDER}
    for k in sorted(ORDER, key=lambda k: whole[k] - exact[k])[:100 - sum(whole.values())]:
        whole[k] += 1
    return whole


def patient_dots(c: dict, unit: str) -> str:
    """100 dots, one per patient out of every 100, coloured by group, with a legend giving the exact counts."""
    n = sum(c[k] for k in ORDER)
    w = per_100_whole(c)
    dots = "".join(f'<i class="{k}"></i>' * w[k] for k in ORDER)
    legend = "".join(f'<div><i class="{k}"></i><b>{GROUPS[k][1]}</b> {w[k]} <small>({c[k]:,} of {n:,})</small></div>'
                     for k in ORDER)
    return (f'<div class="jt-dots-wrap"><div class="jt-mini-title">Out of every 100 {TEST} {unit}</div>'
            f'<div class="jt-dots">{dots}</div><div class="jt-legend">{legend}</div>'
            '<div class="jt-note">Rounded to whole patients.</div></div>')


def hundred_bar(label: str, c: dict) -> str:
    """One stacked bar: the four groups as shares of all patients, with the share per 100 written inside."""
    n = sum(c[k] for k in ORDER)
    segs = "".join(f'<div class="{k}" style="width:{100 * c[k] / n:.3f}%">{f"{100 * c[k] / n:.1f}" if 100 * c[k] / n >= 4 else ""}'
                   f"</div>" for k in ORDER if c[k])
    # Every group's exact value under the bar, so a segment too thin to label is never hidden
    values = " · ".join(f'<span><i class="{k}"></i>{GROUPS[k][1]} <b>{100 * c[k] / n:.1f}</b> <small>({c[k]:,})</small></span>'
                        for k in ORDER)
    return (f'<div class="jt-hb-row"><div class="lbl">{escape(label)}</div><div class="jt-hb">{segs}</div>'
            f'<div></div><div class="jt-hb-vals">{values} <small>per 100 (patients out of {n:,})</small></div></div>')


def group_legend() -> str:
    return '<div class="jt-legend inline">' + "".join(
        f'<div><i class="{k}"></i>{GROUPS[k][1]} ({GROUPS[k][0]})</div>' for k in ORDER) + "</div>"


def clickable_rows(prefix: str, kind: str, names: list, model: str, render) -> None:
    """One row per model from render(name, selected); every row but the selected one is clickable and selects its
    model. The "<prefix>card-"/"<prefix>pick-" keys reuse the cards' invisible click button."""
    for name in names:
        if name == model:
            html(render(name, True))
            continue
        with st.container(key=f"{prefix}card-{kind}-{name}"):
            html(render(name, False))
            st.button(f"Select {m11.MODEL_LABEL[name]}", key=f"{prefix}pick-{kind}-{name}", on_click=select_model,
                      args=(name,))


def grid_row(cells: list, cols: str, cls: str = "") -> str:
    """One table row drawn as a grid, so each row can be its own clickable block yet line up with the others."""
    return f'<div class="jt-gt {cls}" style="grid-template-columns:{cols}">' + "".join(f"<div>{c}</div>" for c in cells) + "</div>"


def clickable_table(prefix: str, rows: dict, model: str, header_tips: dict, cols: str) -> None:
    """A table with one row per model (rows: model → {column: value}); click a row to select that model.
    The selected model's row is outlined; each metric's header has a hover tip."""
    keys = list(next(iter(rows.values())))
    html(grid_row([escape(k) + (" " + tip(header_tips[k], "r" if k == keys[-1] else "") if k in header_tips else "")
                   for k in keys], cols, "head"))
    clickable_rows(prefix, "trow", list(rows), model,
                   lambda name, sel: grid_row([escape(str(v)) for v in rows[name].values()], cols, "sel" if sel else ""))


def ab_head(o: dict, majority) -> str:
    return ('<div class="jt-ab-row head"><div></div><div>Accuracy · dashed line = “the most common class for '
            f'everyone” ({m11.fmt_pct(majority)})</div><div></div><div>Caught: of the patients who {escape(o["had"])}, '
            'the share flagged</div><div></div></div>')


def ab_row(res: dict, name: str, selected: bool, majority) -> str:
    """Accuracy as a bar with a dashed line at 'the most common class for everyone', next to the share of patients
    with the outcome that the model catches (sensitivity), with the count."""
    pct = lambda v: 0 if v is None else max(0.0, min(1.0, v)) * 100
    c = m11.confusion(*m11.preds(res, name), THRESHOLD)
    m = m11.metrics(c)
    return (f'<div class="jt-ab-row{" sel" if selected else ""}"><div class="nm">{escape(m11.MODEL_LABEL[name])}</div>'
            f'<div class="jt-track"><div class="fill acc" style="width:{pct(m["accuracy"]):.2f}%"></div>'
            f'<div class="mark" style="left:{pct(majority):.2f}%"></div></div><div class="val">{m11.fmt_pct(m["accuracy"])}</div>'
            f'<div class="jt-track"><div class="fill catch" style="width:{pct(m["sensitivity"]):.2f}%"></div></div>'
            f'<div class="val">{c["tp"]:,} of {m["positives"]:,}</div></div>')


def auroc_pos(v: float) -> float:
    """Where an AUROC sits on the 0.5 (chance) to 1.0 (perfect ranking) scale, in percent."""
    return max(0.0, min(1.0, (v - 0.5) / 0.5)) * 100


def by_test_auroc(summary: dict) -> list:
    return sorted(summary, key=lambda m: -1 if summary[m]["test"] is None else summary[m]["test"], reverse=True)


def db_row(summary: dict, name: str, selected: bool) -> str:
    """One chart row: emerald Training dot and sapphire Test dot joined by a line that fades from one colour to the other;
    the longer the line, the bigger the gap."""
    v = summary[name]
    track = ""
    if v["train"] is not None and v["test"] is not None:
        tr, te = auroc_pos(v["train"]), auroc_pos(v["test"])
        left, right = (TRAIN_FILL, SAPPHIRE) if tr < te else (SAPPHIRE, TRAIN_FILL)
        track = (f'<div class="line" style="left:{min(tr, te):.2f}%;width:{abs(tr - te):.2f}%;'
                 f'background:linear-gradient(90deg, {left}, {right})"></div>'
                 f'<div class="dot train" style="left:{tr:.2f}%" title="{TRAIN} {m11.fmt_num(v["train"])}"></div>'
                 f'<div class="dot test" style="left:{te:.2f}%" title="{TEST} {m11.fmt_num(v["test"])}"></div>')
    return (f'<div class="jt-db-row{" sel" if selected else ""}"><div class="nm">{escape(m11.MODEL_LABEL[name])}</div>'
            f'<div class="jt-db-track">{track}</div><div class="val"><span class="tr">{TRAIN} {m11.fmt_num(v["train"])}</span> · '
            f'<span class="te">{TEST} {m11.fmt_num(v["test"])}</span> · gap {m11.fmt_num(v["gap"])}</div></div>')


def db_axis() -> str:
    ticks = "".join(f'<span style="left:{auroc_pos(t):.0f}%">{t:.1f}</span>' for t in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
    return (f'<div class="jt-db-row axis"><div></div><div class="jt-db-ticks">{ticks}</div>'
            '<div class="val">0.5 = chance · 1.0 = perfect ranking</div></div>'
            f'<div class="jt-legend inline"><div><i class="dot-train"></i>{TRAIN}: patients it learned from</div>'
            f'<div><i class="dot-test"></i>{TEST}: patients it never saw</div></div>')


def select_model(name: str) -> None:
    st.session_state.model = name  # one selected model, shared by every section's picker


def model_cards(res: dict, model: str, o: dict, majority) -> None:
    """The selected model's card on the left, opened up into its four groups of patients in words; the other four
    models in a 2×2 grid on the right. Clicking a small card selects it (an invisible button is stretched over it)."""
    left, right = st.columns([3, 2], gap="medium")
    with left:
        html(featured_card(m11.MODEL_LABEL[model], m11.confusion(*m11.preds(res, model), THRESHOLD), o, majority))
    others = [name for name in m11.MODELS if name != model]
    with right:
        for pair in (others[:2], others[2:]):
            for col, name in zip(st.columns(2, gap="small"), pair):
                with col, st.container(key=f"s1card-{name}"):
                    html(small_matrix(m11.MODEL_LABEL[name], m11.confusion(*m11.preds(res, name), THRESHOLD)))
                    st.button(f"Select {m11.MODEL_LABEL[name]}", key=f"s1pick-{name}", on_click=select_model,
                              args=(name,))




def patient_group(c: dict, k: str, words: str, hint: str) -> str:
    code, name, fg, bg = GROUPS[k]
    side = "r" if k in ("fn", "tn") else ""  # the right-hand column: keep the tip on screen
    edge = TOPAZ_FILL if k == "fp" else fg  # the edge can be bright gold; the text needs the darker shade
    return (f'<div class="jt-group" style="background:{bg};border-color:{edge}"><div class="t" style="color:{fg}">'
            f'{icon(GROUP_ICON[k])}{name} ({code}) {tip(hint, side)}</div><div class="n" style="color:{fg}">{c[k]:,} <small>patients</small></div>'
            f'<div class="d">{escape(words)}</div></div>')


def featured_card(title: str, c: dict, o: dict, majority) -> str:
    """The selected model's card: its confusion matrix as four groups of patients, then each metric in words."""
    m = m11.metrics(c)
    t = tips(o)
    precision = (f"of the {m['flagged']:,} patients flagged, {c['tp']:,} {o['had']}." if m["flagged"]
                 else "no patient was flagged, so there is no share to compute.")
    facts = [
        (f"Sensitivity {m11.fmt_pct(m['sensitivity'])}", "sensitivity",
         f"of the {m['positives']:,} patients who {o['had']}, the model flagged {c['tp']:,}."),
        (f"Specificity {m11.fmt_pct(m['specificity'])}", "specificity",
         f"of the {m['negatives']:,} patients who {o['not']}, the model did not flag {c['tn']:,}."),
        (f"Precision {m11.fmt_pct(m['precision'])}", "precision", precision),
        (f"Accuracy {m11.fmt_pct(m['accuracy'])}", "accuracy",
         f"of all {m['n']:,} patients, the model put {c['tp'] + c['tn']:,} in the right group, against "
         f"{m11.fmt_pct(majority)} for “the most common class for everyone”."),
    ]
    return ('<div class="jt-card selected">'
            f'<h4>{escape(title)} <span class="jt-tag">Selected · {TEST}</span></h4><div class="jt-fm">'
            '<div class="jt-blank"></div>'
            '<div class="jt-head">Predicted: flagged<span>probability ≥ 0.50</span></div>'
            '<div class="jt-head">Predicted: not flagged<span>probability &lt; 0.50</span></div>'
            f'<div class="jt-row">Actual: positive<span>{m["positives"]:,} patients {o["had"]}</span></div>'
            + patient_group(c, "tp", f"{o['had'].capitalize()}, and the model flagged them.", t["tp"])
            + patient_group(c, "fn", f"{o['had'].capitalize()}, but the model did not flag them.", t["fn"])
            + f'<div class="jt-row">Actual: negative<span>{m["negatives"]:,} patients {o["not"]}</span></div>'
            + patient_group(c, "fp", f"{o['not'].capitalize()}, but the model flagged them.", t["fp"])
            + patient_group(c, "tn", f"{o['not'].capitalize()}, and the model did not flag them.", t["tn"])
            + '</div><div class="jt-split"><ul class="jt-facts">'
            + "".join(f"<li><b>{escape(k)}</b> {tip(t[key], 'l')}: {escape(v)}</li>" for k, key, v in facts)
            + f"</ul>{patient_dots(c, o['unit'])}</div></div>")


def beyond_accuracy(res: dict, model: str) -> None:
    o = OUTCOME[res["dataset"]]
    sel = m11.confusion(*m11.preds(res, model), THRESHOLD)  # the selected model's four counts
    base = m11.metrics(sel)
    majority = m11.majority_accuracy(res["test"]["y"])

    # ---- One slim strip: what "positive" means, how common it is, and the accuracy of guessing the common class
    t = tips(o)
    html(f'<div class="jt-strip"><div><b>Positive class</b>{escape(o["positive"])}</div>'
         f'<div><b>Prevalence ({TEST}) {tip(t["prevalence"])}</b>{m11.fmt_pct(base["prevalence"])} '
         f'<small>of {base["n"]:,} patients {o["had"]}</small></div>'
         f'<div><b>Accuracy of “the most common class for everyone” ({TEST}) {tip(t["majority"], "r")}</b>'
         f'{m11.fmt_pct(majority)}</div></div>')
    always_no = (f" Most test patients {o['not']}, so that means **“always no”**: it flags no one and catches none of "
                 f"the {base['positives']:,} patients who {o['had']}, yet scores the accuracy above. "
                 "Read every model's accuracy against it." if base["prevalence"] is not None and base["prevalence"] < 0.5
                 else "")
    st.caption(f"A model **flags** a patient (predicts positive) when their probability is 0.50 or more.{always_no}")

    # ---- A. Every model side by side; the cards double as the model picker
    st.subheader(f"All five models at threshold 0.50 ({TEST})")
    st.caption(f"{TEST} · {base['n']:,} patients the models never saw. Rows are what actually happened "
               f"(+ = {o['positive'].lower()}), columns the prediction: TP caught, FN missed, FP false alarm, "
               "TN correctly not flagged. The selected model's card opens up; **click a card, a table row or a bar "
               "row below to select a model** (they all stay in step).")
    model_cards(res, model, o, majority)

    # ---- B. Every model's metrics, full width; click a row to select that model
    rows = {}
    for name in m11.MODELS:
        m = m11.metrics(m11.confusion(*m11.preds(res, name), THRESHOLD))
        rows[name] = {"Model": m11.MODEL_LABEL[name], "Accuracy": m11.fmt_pct(m["accuracy"]),
                      "Sensitivity (recall, TPR)": m11.fmt_pct(m["sensitivity"]), "Specificity": m11.fmt_pct(m["specificity"]),
                      "FPR (1 − specificity)": m11.fmt_pct(m["fpr"]), "Precision": m11.fmt_pct(m["precision"]),
                      "F1": m11.fmt_num(m["f1"])}
    st.markdown(f"#### Every model's metrics at threshold 0.50 ({TEST})")
    st.caption(f"{TEST} · the selected model is outlined; **click a row to select that model**. “undefined” means the "
               "metric divides by zero (for example precision when no patient is flagged).")
    clickable_table("s1", rows, model, {
        "Accuracy": t["accuracy"], "Sensitivity (recall, TPR)": t["sensitivity"], "Specificity": t["specificity"],
        "FPR (1 − specificity)": t["fpr"], "Precision": t["precision"], "F1": t["f1"]},
        cols="minmax(10rem, 1.6fr) repeat(6, minmax(0, 1fr))")

    # ---- C. Why accuracy alone misleads: accuracy against "always no", next to how many each model catches
    st.markdown(f"#### Accuracy against “always no”, and how many each model catches ({TEST})")
    st.caption(f"{TEST} · threshold 0.50. A model can match the accuracy of flagging no one while catching almost "
               f"none of the patients who {o['had']}: read the two bars together. **Click a row to select that model.**")
    html(ab_head(o, majority))
    clickable_rows("s1", "arow", m11.MODELS, model, lambda name, sel: ab_row(res, name, sel, majority))


# ---- 2. A Threshold for the Job ------------------------------------------------
STEP = 0.01  # the slider's step


def fmt_value(v, kind: str) -> str:
    if kind == "count":
        return f"{v:,}"
    if kind == "per100":
        return "undefined" if v is None else f"{v:.1f}"
    return m11.fmt_pct(v) if kind == "pct" else m11.fmt_num(v)


def fmt_change(a, b, kind: str) -> str:
    """b − a, signed: counts as whole patients, percentages in percentage points."""
    if a is None or b is None:
        return "undefined"
    d = b - a
    text = {"count": f"{d:+,}", "pct": f"{d * 100:+.1f} pts", "per100": f"{d:+.1f}"}.get(kind, f"{d:+.3f}")
    return text.replace("-", "−")


def compare_table(rows: list[tuple], chosen: float, t: dict) -> str:
    """Each measure at the chosen threshold (tinted amethyst), at 0.50, and the change, with a hover tip per measure.
    The column order matches the matrices above: yours on the left, 0.50 on the right."""
    head = (f"<th>Measure ({TEST})</th><th class=chosen>At your threshold, {chosen:.2f}</th><th>At 0.50</th>"
            "<th>Change vs 0.50</th>")
    body = "".join(
        f"<tr><td>{escape(label)} {tip(t[key], 'l')}</td><td class=chosen>{fmt_value(b, kind)}</td>"
        f"<td>{fmt_value(a, kind)}</td><td>{fmt_change(a, b, kind)}</td></tr>"
        for label, key, a, b, kind in rows)
    return f'<div class="jt-scroll"><table class="jt-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def threshold(res: dict, model: str) -> None:
    o = OUTCOME[res["dataset"]]
    t = tips(o)
    p, y = m11.preds(res, model)
    n = len(y)
    st.session_state.setdefault("s2_threshold", 0.5)

    st.subheader(f"What moving the threshold gains and gives up ({TEST})")

    # ---- Which model: a banner naming it, with what the slider can't change (its AUROC and probabilities)
    same = sorted(set(p))
    note = (f'<div class="note">This model gives every patient the same probability, {same[0]:.4f}, so moving the '
            f'slider changes nothing until it goes below {same[0]:.4f}; then everyone is flagged at once.</div>'
            if len(same) == 1 else "")
    html(f'<div class="jt-banner"><div><span>Model ({TEST})</span><div class="name">{escape(m11.MODEL_LABEL[model])}</div></div>'
         f'<div><span>AUROC ({TEST}) {tip(t["auroc"], "r")}</span><div class="name">{m11.fmt_num(m11.auroc(p, y))}</div>'
         "<small>the same at every threshold: the slider changes only the cut-off, never a probability</small></div>"
         f"{note}</div>")

    # ---- The model buttons, right above the slider (they and the other sections' cards share one selected model)
    st.session_state.s2_model = model
    st.segmented_control("Choose a model", m11.MODELS, required=True, format_func=m11.MODEL_LABEL.get,
                         key="s2_model", on_change=lambda: select_model(st.session_state.s2_model), width="stretch")

    # ---- The one control, with what it changes summed up right beside it
    left, right = st.columns([3, 2], gap="large", vertical_alignment="center")
    with left:
        chosen = st.slider("Your threshold: flag a patient when their probability is at least", 0.0, 1.0, step=STEP,
                           format="%.2f", key="s2_threshold")
    c50, ct = m11.confusion(p, y, 0.5), m11.confusion(p, y, chosen)
    m50, mt = m11.metrics(c50), m11.metrics(ct)
    with right:
        if math.isclose(chosen, 0.5):
            html('<div class="jt-strip"><div><b>Compared with 0.50</b>Move the slider to see what a different threshold '
                 'gains and gives up. Everything below follows it.</div></div>')
        else:
            per100 = {k: 100 * (ct[k] - c50[k]) / n for k in ("tp", "fp", "fn")}
            html(f'<div class="jt-strip"><div><b>Moving from 0.50 to {chosen:.2f}, per 100 {o["unit"]} ({TEST})</b>'
                 f'flagged {fmt_change(m50["flagged_per_100"], mt["flagged_per_100"], "per100")} · '
                 f'caught {fmt_change(0, per100["tp"], "per100")} · '
                 f'false alarms {fmt_change(0, per100["fp"], "per100")} · '
                 f'missed {fmt_change(0, per100["fn"], "per100")}</div></div>')

    # ---- The two confusion matrices side by side: yours under the slider, 0.50 on the right for comparison
    yours, fixed = st.columns([3, 2], gap="large")
    yours.markdown(small_matrix(f"At your threshold, {chosen:.2f} ({TEST})", ct, selected=not math.isclose(chosen, 0.5)),
                   unsafe_allow_html=True)
    fixed.markdown(small_matrix(f"At 0.50 ({TEST})", c50), unsafe_allow_html=True)

    # ---- The same two matrices as 100 patients: the coloured parts grow and shrink as the slider moves
    html(f'<div class="jt-mini-title">Out of every 100 {TEST} {o["unit"]}</div>'
         + hundred_bar(f"At your threshold, {chosen:.2f}", ct) + hundred_bar("At 0.50", c50) + group_legend())

    # ---- Every measure side by side
    rows = [
        ("Caught (TP)", "tp", c50["tp"], ct["tp"], "count"),
        ("Missed (FN)", "fn", c50["fn"], ct["fn"], "count"),
        ("False alarms (FP)", "fp", c50["fp"], ct["fp"], "count"),
        ("Correctly not flagged (TN)", "tn", c50["tn"], ct["tn"], "count"),
        (f"Flagged per 100 {o['unit']}", "flagged100", m50["flagged_per_100"], mt["flagged_per_100"], "per100"),
        (f"False alarms per 100 {o['unit']}", "fa100", 100 * c50["fp"] / n, 100 * ct["fp"] / n, "per100"),
        ("Sensitivity (recall, TPR)", "sensitivity", m50["sensitivity"], mt["sensitivity"], "pct"),
        ("Specificity", "specificity", m50["specificity"], mt["specificity"], "pct"),
        ("FPR (1 − specificity)", "fpr", m50["fpr"], mt["fpr"], "pct"),
        ("Precision", "precision", m50["precision"], mt["precision"], "pct"),
        ("F1", "f1", m50["f1"], mt["f1"], "num"),
        ("Accuracy", "accuracy", m50["accuracy"], mt["accuracy"], "pct"),
    ]
    st.markdown(f"#### Every measure at your threshold and at 0.50 ({TEST})")
    st.caption(f"{TEST} · {m11.MODEL_LABEL[model]} at 0.50 and at your threshold. “undefined” means the measure "
               "divides by zero (for example precision when no patient is flagged).")
    html(compare_table(rows, chosen, t))


# ---- 3. Training vs. Test ------------------------------------------------------
TV_TIPS = {
    "train": "AUROC on the patients the model learned from. It flatters every model, because the model has already "
             "seen these patients and their outcomes. It is never what to expect on new patients.",
    "test": "AUROC on patients the model never saw while learning: the figure to expect on new patients. Like any "
            "AUROC it describes ranking (how often a patient with the outcome gets a higher probability than one "
            "without), not accuracy.",
    "gap": "Training AUROC minus Test AUROC. A big gap means the model memorised its training patients: it looks far "
           "better on patients it has already seen than on new ones. A gap near zero, or just below it, means it does "
           "about as well on new patients as on the ones it learned from.",
}


def ordinal(k: int) -> str:
    return f"{k}{'th' if 11 <= k % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"


def place(summary: dict, model: str, part: str) -> int:
    """1 = the highest AUROC of the five models on that set (Training or Test)."""
    values = sorted((v[part] for v in summary.values() if v[part] is not None), reverse=True)
    return values.index(summary[model][part]) + 1 if summary[model][part] is not None else None


def auroc_bars(v: dict) -> str:
    """Training (emerald) and Test (sapphire) AUROC as bars on a 0.5 (chance) to 1.0 (perfect ranking) scale."""
    def bar(label, value, fill, text):
        width = 0 if value is None else auroc_pos(value)
        return (f'<span style="color:{text};font-weight:600">{label}</span>'
                f'<div class="track"><div class="fill" style="width:{width:.1f}%;background:{fill}"></div></div>'
                f'<span>{m11.fmt_num(value)}</span>')
    return (f'<div class="jt-bars">{bar(TRAIN, v["train"], TRAIN_FILL, TRAIN_TEXT)}{bar(TEST, v["test"], SAPPHIRE, SAPPHIRE)}</div>'
            '<div class="jt-scale"><span>0.5 = chance</span><span>1.0 = perfect ranking</span></div>')


def tv_featured(res: dict, summary: dict, model: str) -> str:
    """The selected model's card: Training and Test AUROC in large type, the gap, bars, and the gap in plain words."""
    v = summary[model]
    n_train, n_test = res["train"]["n"], res["test"]["n"]
    places = [place(summary, model, part) for part in ("train", "test")]
    words = (f"On the {n_train:,} {TRAIN.lower()} patients it learned from, its AUROC is {m11.fmt_num(v['train'])}; "
             f"on the {n_test:,} {TEST.lower()} patients it never saw, {m11.fmt_num(v['test'])}. "
             f"Expect something like the {TEST.lower()} figure on new patients.")
    if all(places):
        words += (f" Among the {len(summary)} models it places <b>{ordinal(places[0])} on {TRAIN}</b> and "
                  f"<b>{ordinal(places[1])} on {TEST}</b>.")
    return ('<div class="jt-card selected">'
            f'<h4>{escape(m11.MODEL_LABEL[model])} <span class="jt-tag">Selected</span></h4><div class="jt-au">'
            f'<div><span style="color:{TRAIN_TEXT}">{TRAIN} AUROC {tip(TV_TIPS["train"], "l")}</span>'
            f'<div class="v" style="color:{TRAIN_TEXT}">{m11.fmt_num(v["train"])}</div></div>'
            f'<div><span style="color:{SAPPHIRE}">{TEST} AUROC {tip(TV_TIPS["test"])}</span>'
            f'<div class="v" style="color:{SAPPHIRE}">{m11.fmt_num(v["test"])}</div></div>'
            f'<div><span style="color:{AMETHYST}">Gap ({TRAIN} − {TEST}) {tip(TV_TIPS["gap"], "r")}</span>'
            f'<div class="v" style="color:{AMETHYST}">{m11.fmt_num(v["gap"])}</div></div></div>'
            f'{auroc_bars(v)}<p class="jt-plain">{words}</p></div>')


def tv_small(summary: dict, name: str) -> str:
    v = summary[name]
    return (f'<div class="jt-card"><h4>{escape(m11.MODEL_LABEL[name])}</h4>{auroc_bars(v)}'
            f'<div style="font-size:.8rem;color:{AMETHYST};font-weight:700;margin-top:.3rem">'
            f'Gap {m11.fmt_num(v["gap"])}</div></div>')


def train_vs_test(res: dict, model: str) -> None:
    s = m11.auroc_summary(res)
    o = OUTCOME[res["dataset"]]
    tr, te = res["train"], res["test"]

    # ---- How many patients each AUROC rests on
    html(f'<div class="jt-strip"><div><b>{icon("school")}{TRAIN} patients</b>{tr["n"]:,} <small>({tr["n_pos"]:,} {o["had"]}): '
         f'the models learned from these</small></div>'
         f'<div><b>{icon("person_search")}{TEST} patients</b>{te["n"]:,} <small>({te["n_pos"]:,} {o["had"]}): never seen while '
         f'learning, so these are the ones to judge by</small></div></div>')
    st.caption(f"Every AUROC below comes in a pair: **{TRAIN}** (green, on patients the model learned from, which "
               f"flatters it) and **{TEST}** (sapphire, on patients it never saw: what to expect on new patients).")

    # ---- The selected model's big card, the other four as clickable cards in a 2×2 grid
    st.subheader(f"{TRAIN} vs. {TEST} AUROC for each model")
    left, right = st.columns([3, 2], gap="medium")
    with left:
        html(tv_featured(res, s, model))
    others = [name for name in m11.MODELS if name != model]
    with right:
        st.caption("Click a card to select that model.")
        for pair in (others[:2], others[2:]):
            for col, name in zip(st.columns(2, gap="small"), pair):
                with col, st.container(key=f"s3card-{name}"):
                    html(tv_small(s, name))
                    st.button(f"Select {m11.MODEL_LABEL[name]}", key=f"s3pick-{name}", on_click=select_model,
                              args=(name,))

    # ---- Every model at a glance; click a row to select that model (the card above follows)
    st.subheader(f"{TRAIN} vs. {TEST} AUROC at a glance")
    st.caption(f"Sorted by {TEST} AUROC, because that is what to expect on new patients. The longer the line between "
               f"the green {TRAIN} dot and the sapphire {TEST} dot, the more the model memorised its training patients. "
               "**Click a row to select that model.**")
    clickable_rows("s3", "row", by_test_auroc(s), model, lambda name, sel: db_row(s, name, sel))
    html(db_axis())

    # ---- Every model in one table
    st.markdown(f"#### Every model's {TRAIN} and {TEST} AUROC")
    st.caption(f"{TRAIN} AUROC on {tr['n']:,} patients · {TEST} AUROC on {te['n']:,} patients · the selected model is "
               "outlined; click a row to select that model. Only the Test column is what to expect on new patients.")
    rows = {m: {"Model": m11.MODEL_LABEL[m], f"{TRAIN} AUROC": m11.fmt_num(v["train"]), f"{TEST} AUROC": m11.fmt_num(v["test"]),
                f"Gap ({TRAIN} − {TEST})": m11.fmt_num(v["gap"])} for m, v in s.items()}
    clickable_table("s3", rows, model, {f"{TRAIN} AUROC": TV_TIPS["train"], f"{TEST} AUROC": TV_TIPS["test"],
                                        f"Gap ({TRAIN} − {TEST})": TV_TIPS["gap"]},
                    cols="minmax(10rem, 1.6fr) repeat(3, minmax(0, 1fr))")


RENDER = dict(zip(SECTIONS, [beyond_accuracy, threshold, train_vs_test]))
# Each section has its own jewel tone (headings, strips, banner, active tab) and a pale tint of it.
ACCENT = dict(zip(SECTIONS, [(EMERALD, "#E6F4EE"), (SAPPHIRE, "#E6EDF7"), (AMETHYST, "#F3EEF8")]))

# ---- The hero banner: title, the central question, and a faint heartbeat line across the jewel-tone gradient
ECG = ("0,40 90,40 105,40 112,28 120,52 128,40 160,40 172,40 180,6 190,70 198,40 230,40 245,32 262,40 360,40 375,40 "
       "382,28 390,52 398,40 430,40 442,40 450,6 460,70 468,40 500,40 515,32 532,40 630,40 645,40 652,28 660,52 668,40 "
       "700,40 712,40 720,6 730,70 738,40 770,40 785,32 802,40 900,40")
html(f'<div class="jt-hero"><svg viewBox="0 0 900 80" preserveAspectRatio="none" aria-hidden="true">'
     f'<polyline points="{ECG}" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/></svg>'
     f'<div class="title" role="heading" aria-level="1">{icon("stethoscope")}Judge the Model</div>'
     '<div class="sub">Which classifier would you trust for this job, at what threshold, and with what limits?</div></div>')

# ---- Navigation on the page (no sidebar): section tabs, then the dataset toggle.
# The section is kept in the address (?section=2), so a refresh returns to it.
if "section" not in st.session_state:
    wanted = st.query_params.get("section", "1")
    st.session_state.section = SECTIONS[int(wanted) - 1] if wanted in ("1", "2", "3") else SECTIONS[0]
st.session_state.setdefault("dataset", m11.DATASETS[0])
st.session_state.setdefault("model", m11.MODELS[0])  # each section has its own model picker on the page
with st.container(key="nav-section"):
    section = st.segmented_control("Section", SECTIONS, key="section", required=True, width="stretch",
                                   format_func=lambda s: f":material/{SECTION_ICON[s]}: {s}",
                                   label_visibility="collapsed")
st.query_params["section"] = str(SECTIONS.index(section) + 1)
toggle_col, rec_col = st.columns([1, 2], gap="medium", vertical_alignment="bottom")
with toggle_col, st.container(key="nav-dataset"):
    key = st.segmented_control("Dataset", m11.DATASETS, key="dataset", required=True,
                               format_func=lambda d: f":material/{DATASET_ICON[d]}: {m11.DATASET_LABEL[d]}")
with rec_col:
    recommendation(key)  # only the selected dataset's recommendation, right beside the toggle

accent, tint = ACCENT[section]
html(f"""<style>
.stApp :is(h2, h3), .stApp h4:not(.jt-card *) {{color: {accent};}}
.jt-strip {{border-left-color: {accent}; background: {tint};}}
.jt-banner {{background: linear-gradient(100deg, {accent}, {INK});}}
.jt-table th, .jt-gt.head > div {{background: {accent};}}
:is(.st-key-nav-section, .st-key-nav-dataset, .st-key-s2_model) button[aria-checked="true"] {{
  background: {accent} !important; border-color: {accent} !important;}}
:is(.st-key-nav-section, .st-key-nav-dataset, .st-key-s2_model) button[aria-checked="true"] * {{color: #fff !important;}}
.st-key-nav-section button {{padding: .5rem 1rem;}}
.st-key-nav-section button p {{font-family: 'Fraunces', serif !important; font-weight: 700; font-size: 1.05rem;}}
</style>""")

res = load(key)
model = st.session_state.model
st.header(f":material/{SECTION_ICON[section]}: {section}")
st.caption(f"{m11.DATASET_LABEL[key]}: {res['train']['n']:,} training rows ({res['train']['n_pos']:,} positive), "
           f"{res['test']['n']:,} test rows ({res['test']['n_pos']:,} positive).")
if model in res["models"]:
    RENDER[section](res, model)
else:
    st.warning(f"{m11.MODEL_LABEL[model]} has no results yet: run `python -m analysis`, then commit and push `results/`.")
