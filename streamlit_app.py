"""Starter app for Streamlit Community Cloud: three plain sections that read results/ and show correct numbers.

Run locally:  bash run_app.sh  (your agent writes it; it runs streamlit run streamlit_app.py)
Build each section up to its required minimum (see the activity website). Keep every number
coming from m11.py, and label every table and plot "Training" or "Test".
"""

import math
from html import escape

import pandas as pd
import streamlit as st

import m11

TRAIN = "Training"
TEST = "Test"
SECTIONS = ["1. Beyond Accuracy", "2. A Threshold for the Job", "3. Training vs. Test"]

# Jewel-tone palette (the base theme colours are in .streamlit/config.toml).
SAPPHIRE, EMERALD, RUBY, TOPAZ, AMETHYST = "#1E4D8C", "#0B6E4F", "#9B1B30", "#7A5200", "#5B2A86"
INK, MUTED = "#2B1D3A", "#5A5266"

st.set_page_config(page_title="Judge the Model", layout="wide")

# Fonts and the shared styles of the custom HTML blocks. Only text elements get the new font, so
# Streamlit's icon font is left alone.
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&display=swap');
.stApp :is(p, li, label, td, th, input) {{font-family: 'DM Sans', sans-serif;}}
.stApp :is(h1, h2, h3, h4) {{font-family: 'Fraunces', serif !important; letter-spacing: -0.01em;}}
.stApp h1 {{background: linear-gradient(90deg, {SAPPHIRE}, {AMETHYST} 55%, {RUBY}); -webkit-background-clip: text;
  background-clip: text; color: transparent;}}
.stApp :is(h2, h3) {{color: {SAPPHIRE};}}
.stApp h4 {{color: {INK}; padding: .2rem 0 0;}}
[data-testid="stMainBlockContainer"] {{padding-top: 2.5rem;}}
.jt-strip {{display: flex; flex-wrap: wrap; gap: .5rem 1rem; background: #F3EEF8; border-left: 6px solid {AMETHYST};
  border-radius: 10px; padding: .55rem 1rem; color: {INK};}}
.jt-strip div {{flex: 1 1 200px;}}
.jt-strip b {{display: block; font-size: .78rem; color: {MUTED}; font-weight: 600;}}
.jt-strip small {{color: {MUTED};}}
[data-testid="stMetric"] {{background: #F3EEF8; border-left: 6px solid {AMETHYST}; border-radius: 10px; padding: .6rem 1rem;}}
[class*="st-key-s1card-"] {{position: relative;}}
[class*="st-key-s1pick-"] {{position: absolute; inset: 0; z-index: 3;}}
[class*="st-key-s1pick-"] :is(div, button) {{width: 100%; height: 100%;}}
[class*="st-key-s1pick-"] button {{background: transparent; border: none; color: transparent; cursor: pointer; border-radius: 12px;}}
[class*="st-key-s1pick-"] button:hover {{background: rgba(91, 42, 134, .07);}}
[class*="st-key-s1pick-"] button:focus-visible {{outline: 3px dashed {AMETHYST}; outline-offset: 2px;}}
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
.jt-table th.chosen {{background: {AMETHYST};}}
.jt-table td.chosen {{background: #F3EEF8; font-weight: 700;}}
.jt-card.selected {{border: 4px solid {AMETHYST}; box-shadow: 0 4px 14px rgba(91, 42, 134, .28);}}
.jt-card h4 {{font-size: 1.05rem; margin: 0 0 .4rem; padding: 0; color: {INK};}}
.jt-mx {{width: 100%; border-collapse: separate; border-spacing: 4px; font-variant-numeric: tabular-nums;}}
.jt-mx th {{font-size: .7rem; color: {MUTED}; font-weight: 600; text-align: center; border: none; padding: 0; line-height: 1.15;}}
.jt-mx td {{text-align: center; border-radius: 8px; padding: .45rem .15rem; font-weight: 700; border: none; font-size: .88rem;
  white-space: nowrap;}}
.jt-card:not(.selected) h4 {{min-height: 2.4em; line-height: 1.2;}}  /* room for a two-line name: every small card the same height */
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


def starter_note(text: str) -> None:
    st.info(f"Starter display: {text} Build this section up to its required minimum.")


def recommendations() -> None:
    d = load("decisions")
    recs = (d or {}).get("recommendations", {})
    with st.container(border=True):
        st.subheader("Recommendations")
        if not any(recs.values()):
            st.caption("No recommendations yet: fill in `Recommendations` in DECISIONS.md, run "
                       "`python -m analysis`, then commit and push.")
        for k in m11.DATASETS:
            if any(recs.values()):
                st.markdown(f"**{m11.DATASET_LABEL[k]}:** {recs.get(k) or '_not written yet_'}")


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
          "fp": ("FP", "False alarm", TOPAZ, "#FBF0D9"), "tn": ("TN", "Correctly not flagged", SAPPHIRE, "#E3EBF6")}


def html(block: str) -> None:
    st.markdown(block, unsafe_allow_html=True)


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


def select_model(name: str) -> None:
    st.session_state.model = name  # the sidebar dropdown shares this key, so it follows


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


def metrics_table(rows: list[dict], selected: str, header_tips: dict) -> str:
    """The comparison table, with the selected model's row outlined and a hover tip on each metric's header."""
    last = list(rows[0])[-1]
    head = "".join(f"<th>{escape(k)}{' ' + tip(header_tips[k], 'r' if k == last else '') if k in header_tips else ''}</th>"
                   for k in rows[0])
    body = "".join(f'<tr{" class=selected" if r["Model"] == selected else ""}>'
                   + "".join(f"<td>{escape(str(v))}</td>" for v in r.values()) + "</tr>" for r in rows)
    return f'<div class="jt-scroll"><table class="jt-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def patient_group(c: dict, k: str, words: str, hint: str) -> str:
    code, name, fg, bg = GROUPS[k]
    side = "r" if k in ("fn", "tn") else ""  # the right-hand column: keep the tip on screen
    return (f'<div class="jt-group" style="background:{bg};border-color:{fg}"><div class="t" style="color:{fg}">'
            f'{name} ({code}) {tip(hint, side)}</div><div class="n" style="color:{fg}">{c[k]:,} <small>patients</small></div>'
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
            + '</div><ul class="jt-facts">'
            + "".join(f"<li><b>{escape(k)}</b> {tip(t[key], 'l')}: {escape(v)}</li>" for k, key, v in facts)
            + "</ul></div>")


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
               "TN correctly not flagged. The selected model's card opens up; **click another card to select it.**")
    model_cards(res, model, o, majority)

    # ---- B. Every model's metrics, full width
    rows = []
    for name in m11.MODELS:
        m = m11.metrics(m11.confusion(*m11.preds(res, name), THRESHOLD))
        rows.append({"Model": m11.MODEL_LABEL[name], "Accuracy": m11.fmt_pct(m["accuracy"]),
                     "Sensitivity (recall, TPR)": m11.fmt_pct(m["sensitivity"]), "Specificity": m11.fmt_pct(m["specificity"]),
                     "FPR (1 − specificity)": m11.fmt_pct(m["fpr"]), "Precision": m11.fmt_pct(m["precision"]),
                     "F1": m11.fmt_num(m["f1"])})
    st.markdown(f"#### Every model's metrics at threshold 0.50 ({TEST})")
    st.caption(f"{TEST} · the selected model is outlined. “undefined” means the metric divides by zero "
               "(for example precision when no patient is flagged).")
    html(metrics_table(rows, m11.MODEL_LABEL[model], {
        "Accuracy": t["accuracy"], "Sensitivity (recall, TPR)": t["sensitivity"], "Specificity": t["specificity"],
        "FPR (1 − specificity)": t["fpr"], "Precision": t["precision"], "F1": t["f1"]}))


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

    # ---- The model buttons, right above the slider (they and the sidebar dropdown stay in step)
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
    st.caption(f"{TEST} · {m11.MODEL_LABEL[model]} at 0.50 and at your threshold. “undefined” means the measure "
               "divides by zero (for example precision when no patient is flagged).")
    html(compare_table(rows, chosen, t))


# ---- 3. Training vs. Test ------------------------------------------------------
def train_vs_test(res: dict, model: str) -> None:
    starter_note("training and test AUROC of every model, in a table.")
    s = m11.auroc_summary(res)
    rows = [{"Model": m11.MODEL_LABEL[m], f"{TRAIN} AUROC": m11.fmt_num(v["train"]), f"{TEST} AUROC": m11.fmt_num(v["test"])}
            for m, v in s.items()]
    st.caption(f"{TRAIN} and {TEST} · AUROC on the rows each model learned from, and on rows it never saw")
    st.table(pd.DataFrame(rows).set_index("Model"))


RENDER = dict(zip(SECTIONS, [beyond_accuracy, threshold, train_vs_test]))

st.title("Judge the Model")
st.caption("Which classifier would you trust for this job, at what threshold, and with what limits?")
recommendations()
# The section is kept in the address (?section=2), so a refresh returns to it.
if "section" not in st.session_state:
    wanted = st.query_params.get("section", "1")
    st.session_state.section = SECTIONS[int(wanted) - 1] if wanted in ("1", "2", "3") else SECTIONS[0]
section = st.sidebar.radio("Section", SECTIONS, key="section")
st.query_params["section"] = str(SECTIONS.index(section) + 1)
key = st.sidebar.selectbox("Dataset", m11.DATASETS, format_func=m11.DATASET_LABEL.get)
res = load(key)
model = st.sidebar.selectbox("Model", m11.MODELS, key="model",  # key: Section 1's table can also set it
                             format_func=lambda m: m11.MODEL_LABEL[m] + ("" if m in res["models"] else " (not trained yet)"))
st.header(section)
st.caption(f"{m11.DATASET_LABEL[key]}: {res['train']['n']:,} training rows ({res['train']['n_pos']:,} positive), "
           f"{res['test']['n']:,} test rows ({res['test']['n_pos']:,} positive).")
if model in res["models"]:
    RENDER[section](res, model)
else:
    st.warning(f"{m11.MODEL_LABEL[model]} has no results yet: run `python -m analysis`, then commit and push `results/`.")
