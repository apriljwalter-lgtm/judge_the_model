"""Starter app for Streamlit Community Cloud: three plain sections that read results/ and show correct numbers.

Run locally:  bash run_app.sh  (your agent writes it; it runs streamlit run streamlit_app.py)
Build each section up to its required minimum (see the activity website). Keep every number
coming from m11.py, and label every table and plot "Training" or "Test".
"""

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
    "readmission": {"positive": "Readmitted within 30 days of discharge",
                    "had": "were readmitted within 30 days", "not": "were not readmitted within 30 days"},
    "diabetes": {"positive": "Diabetes (reported doctor diagnosis or HbA1c ≥ 6.5%)",
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
    }


def tip(text: str, side: str = "") -> str:
    """A small ⓘ that shows `text` on hover or keyboard focus. side "l"/"r" pins the box's left/right edge."""
    return (f'<span class="jt-tip {side}" tabindex="0" aria-label="{escape(text)}">ⓘ'
            f'<span class="jt-tiptext" role="tooltip">{escape(text)}</span></span>')


def cell(c: dict, k: str) -> str:
    code, _, fg, bg = GROUPS[k]
    return f'<td style="background:{bg};color:{fg}">{code} {c[k]:,}</td>'


def small_matrix(title: str, c: dict) -> str:
    """A compact confusion matrix card: rows are the actual outcome, columns the prediction at the threshold."""
    return (f'<div class="jt-card"><h4>{escape(title)}</h4><table class="jt-mx">'
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
def threshold(res: dict, model: str) -> None:
    starter_note("metrics at 0.50 only.")
    p, y = m11.preds(res, model)
    m = m11.metrics(m11.confusion(p, y, 0.5))
    st.caption(f"{TEST} · {m11.MODEL_LABEL[model]}, threshold 0.50")
    st.table(pd.DataFrame([{"Sensitivity": m11.fmt_pct(m["sensitivity"]), "Specificity": m11.fmt_pct(m["specificity"]),
                            "Precision": m11.fmt_pct(m["precision"]), "Flagged per 100": f"{m['flagged_per_100']:.1f}"}]))


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
section = st.sidebar.radio("Section", SECTIONS)
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
