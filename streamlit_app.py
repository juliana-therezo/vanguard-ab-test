"""Vanguard A/B test - one-page summary (Streamlit).

Run from the repository root:
    streamlit run streamlit_app.py
"""
from pathlib import Path

import html as html_lib
import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------- settings
DATA = Path(__file__).parent / "data" / "tableau"
OLD, NEW = "Old Website", "New Website"
GREY, RED, INK, MUTED = "#A3A3A3", "#96151D", "#262626", "#6B6B6B"
FONT = "DM Sans"
GROUPS = {"Control": OLD, "Test": NEW}
STEPS = ["start", "step_1", "step_2", "step_3"]
STEP_LABELS = {"start": "Start", "step_1": "Step 1", "step_2": "Step 2",
               "step_3": "Step 3", "confirm": "Confirm"}
TABLEAU_URL = ("https://public.tableau.com/app/profile/juliana.therezo/viz/"
               "VanguardABTest_Dashboard/Overview")
GITHUB_URL = "https://github.com/juliana-therezo/vanguard-ab-test"

st.set_page_config(page_title="Vanguard A/B test | Team Ravenclaw",
                   page_icon="📊", layout="wide")

# ---------------------------------------------------------------- styling
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
html, body, [class*="css"], .stMarkdown, .stDataFrame, button, input {{
    font-family: '{FONT}', sans-serif !important; color: {INK};
}}
.block-container {{ padding-top: 2rem; max-width: 1250px; }}
.hero {{ background: {RED}; color: #fff; padding: 22px 28px; border-radius: 4px; }}
.hero h1 {{ color: #fff; font-size: 30px; font-weight: 700; margin: 0; padding: 0; }}
.hero p {{ color: #fff; margin: 6px 0 0 0; font-size: 15px; }}
.kpi {{ background: #F5F5F5; border-radius: 4px; padding: 16px 18px; height: 100%; }}
.kpi .label {{ color: {RED}; font-size: 12px; font-weight: 700; letter-spacing: .04em;
               text-transform: uppercase; }}
.kpi .value {{ font-size: 30px; font-weight: 700; color: {RED}; line-height: 1.2;
               margin: 6px 0 4px 0; }}
.kpi .value.neutral {{ color: {INK}; }}
.kpi .note {{ color: {MUTED}; font-size: 13px; }}
.section {{ color: {RED}; font-size: 13px; font-weight: 700; letter-spacing: .04em;
            text-transform: uppercase; margin: 26px 0 2px 0; }}
.verdict {{ font-size: 24px; font-weight: 700; color: {INK}; margin: 0 0 6px 0; }}
.small {{ color: {MUTED}; font-size: 13px; }}
table.tests {{ width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 6px; }}
table.tests th {{ text-align: left; color: {MUTED}; font-weight: 500; border-bottom: 2px solid {RED};
                 padding: 8px 10px; }}
table.tests td {{ padding: 8px 10px; border-bottom: 1px solid #E6E6E6; }}
table.tests td.yes {{ color: {RED}; font-weight: 700; }}
table.tests td.no {{ color: {MUTED}; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------- data
@st.cache_data
def load_data():
    clients = pd.read_csv(DATA / "tableau_clients.csv")
    steps = pd.read_csv(
        DATA / "tableau_steps.csv",
        usecols=["client_id", "process_step", "is_error", "step_seconds",
                 "valid_time", "month"])
    tests = pd.read_csv(DATA / "tableau_test_results.csv")
    clients["group"] = clients["variation"].map(GROUPS)
    steps = steps.merge(clients[["client_id", "group"]], on="client_id")
    return clients, steps, tests


clients, steps, tests = load_data()

completion = clients.groupby("group")["completed"].mean()
error_rate = steps.groupby("group")["is_error"].mean()
timed = steps[(steps["valid_time"] == 1) & (steps["process_step"].isin(STEPS))]
time_step = (timed.groupby(["process_step", "group"])["step_seconds"]
             .mean().unstack())
faster = int((time_step[NEW] < time_step[OLD]).sum())
p = tests.set_index(["kpi", "step"])["p_value"]
p_thr = p[("Completion vs 5% threshold", "all")]
lift_pp = (completion[NEW] - completion[OLD]) * 100
lift_rel = (completion[NEW] / completion[OLD] - 1) * 100
step1_extra = time_step.loc["step_1", NEW] - time_step.loc["step_1", OLD]

# ---------------------------------------------------------------- header
st.markdown(f"""
<div class="hero">
  <h1>Vanguard digital A/B test: results at a glance</h1>
  <p>Did the new online process help clients finish? {len(clients):,} clients
  randomly split between the Old and New Website, 15 Mar – 20 Jun 2017.</p>
</div>
""", unsafe_allow_html=True)
st.write("")


def kpi(col, label, value, note, neutral=False):
    cls = "value neutral" if neutral else "value"
    col.markdown(f'<div class="kpi"><div class="label">{label}</div>'
                 f'<div class="{cls}">{value}</div>'
                 f'<div class="note">{note}</div></div>', unsafe_allow_html=True)


c1, c2, c3, c4 = st.columns(4)
kpi(c1, "Completion rate",
    f"{completion[NEW]:.1%} vs {completion[OLD]:.1%}",
    f"+{lift_pp:.1f} pts with the New Website, significant (p &lt; 0.001)")
kpi(c2, "Time per step", f"{faster} of 4 faster",
    f"steps faster with the New Website; step 1 takes {step1_extra:.0f} s longer")
kpi(c3, "Error rate", f"{error_rate[NEW]:.1%} vs {error_rate[OLD]:.1%}",
    "of steps are a backward click on the New Website vs Old (p &lt; 0.001)")
kpi(c4, "5% threshold", "Not proven",
    f"+{lift_rel:.1f}% relative lift, not significantly above 5% (p = {p_thr:.3f})",
    neutral=True)

# ---------------------------------------------------------------- verdict
st.markdown('<div class="section">Verdict</div>', unsafe_allow_html=True)
st.markdown('<div class="verdict">Go live with the new design after fixing step 1</div>',
            unsafe_allow_html=True)
st.markdown(
    "The New Website gets significantly more clients to finish and is faster on most "
    "steps. Step 1 causes the extra time and errors, so redesign it and roll out in "
    "phases while tracking completion against the 5% threshold.")


# ---------------------------------------------------------------- charts
# Charts are Vega-Lite specs drawn in the browser (vega-embed), so the app
# doesn't need pyarrow, which Windows App Control may block on some PCs.
GROUP_ORDER = [OLD, NEW]
COLOR_ENC = {"field": "group", "type": "nominal",
             "scale": {"domain": GROUP_ORDER, "range": [GREY, RED]},
             "legend": {"orient": "top", "title": None}}
CONFIG = {
    "font": FONT,
    "title": {"fontSize": 15, "anchor": "start", "color": INK, "fontWeight": 700},
    "axis": {"labelColor": MUTED, "titleColor": MUTED, "gridColor": "#EEEEEE",
             "domainColor": "#BBBBBB", "labelFontSize": 12, "titleFontWeight": 400},
    "legend": {"labelColor": INK, "labelFontSize": 12},
    "view": {"stroke": None},
}


def records(df):
    return json.loads(df.to_json(orient="records", date_format="iso"))


def vega(spec, height=300):
    spec = {"$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "width": "container", "height": height - 100,
            "autosize": {"type": "fit-x", "contains": "padding"}, "config": CONFIG, **spec}
    html = f"""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/vega@5.30.0"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@5.21.0"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@6.26.0"></script>
<style>body{{margin:0;font-family:'{FONT}',sans-serif}} #vis{{width:100%}}</style>
<div id="vis"></div>
<script>
document.fonts.load("12px '{FONT}'").finally(function () {{
  vegaEmbed('#vis', {json.dumps(spec)}, {{actions: false, renderer: 'svg'}});
}});
</script>"""
    components.html(html, height=height)


def grouped_bars(data, x, y, x_order, y_title, y_format, label_format, title):
    tip = [{"field": "group", "title": "Group"}, {"field": x, "title": "Step"},
           {"field": y, "format": label_format, "title": y_title}]
    enc = {"x": {"field": x, "type": "nominal", "sort": x_order, "title": None,
                 "axis": {"labelAngle": 0}},
           "xOffset": {"field": "group", "sort": GROUP_ORDER},
           "y": {"field": y, "type": "quantitative", "title": y_title,
                 "axis": {"format": y_format}}}
    return {"title": title, "data": {"values": records(data)}, "layer": [
        {"mark": "bar", "encoding": {**enc, "color": COLOR_ENC, "tooltip": tip}},
        {"mark": {"type": "text", "dy": -7, "fontSize": 11, "color": INK},
         "encoding": {**enc, "text": {"field": y, "format": label_format}}}]}


# 1. completion rate
comp_df = completion.rename("rate").reset_index()
spec_completion = {
    "title": "Completion rate", "data": {"values": records(comp_df)},
    "encoding": {
        "y": {"field": "group", "type": "nominal", "sort": GROUP_ORDER, "title": None},
        "x": {"field": "rate", "type": "quantitative", "title": "Clients who reached confirm",
              "axis": {"format": "%"}, "scale": {"domain": [0, 0.85]}}},
    "layer": [
        {"mark": {"type": "bar", "size": 30},
         "encoding": {"color": {**COLOR_ENC, "legend": None},
                      "tooltip": [{"field": "group", "title": "Group"},
                                  {"field": "rate", "format": ".1%", "title": "Completion"}]}},
        {"mark": {"type": "text", "align": "left", "dx": 6, "fontSize": 14,
                  "fontWeight": "bold", "color": INK},
         "encoding": {"text": {"field": "rate", "format": ".1%"}}}]}

# 2. clients reaching each step
reach_cols = {f"reached_{s}": STEP_LABELS[s] for s in STEPS + ["confirm"]}
reach = (clients.groupby("group")[list(reach_cols)].mean()
         .rename(columns=reach_cols).reset_index()
         .melt(id_vars="group", var_name="step", value_name="share"))
spec_funnel = grouped_bars(reach, "step", "share", list(reach_cols.values()),
                           "Share of clients", "%", ".0%", "Clients who reach each step")

# 3. average time on each step
ts = time_step.reset_index().melt(id_vars="process_step", var_name="group",
                                  value_name="seconds")
ts["step"] = ts["process_step"].map(STEP_LABELS)
spec_time = grouped_bars(ts, "step", "seconds", [STEP_LABELS[s] for s in STEPS],
                         "Average seconds", "d", ".0f", "Average time on each step")

# 4. step 1 by month (learning effect)
s1 = (timed[timed["process_step"] == "step_1"]
      .groupby(["month", "group"])["step_seconds"].mean().reset_index())
s1["month"] = pd.to_datetime(s1["month"]).dt.strftime("%b")
line_enc = {"x": {"field": "month", "type": "ordinal", "sort": ["Mar", "Apr", "May", "Jun"],
                  "title": None, "axis": {"labelAngle": 0}},
            "y": {"field": "step_seconds", "type": "quantitative", "title": "Average seconds",
                  "scale": {"zero": False}}}
spec_step1 = {
    "title": "Step 1 gets faster as clients learn the new page",
    "data": {"values": records(s1)},
    "layer": [
        {"mark": {"type": "line", "strokeWidth": 3, "point": {"size": 70}},
         "encoding": {**line_enc, "color": COLOR_ENC,
                      "tooltip": [{"field": "group", "title": "Group"},
                                  {"field": "month", "title": "Month"},
                                  {"field": "step_seconds", "format": ".1f",
                                   "title": "Seconds"}]}},
        {"mark": {"type": "text", "dy": -12, "fontSize": 11, "color": INK},
         "encoding": {**line_enc, "text": {"field": "step_seconds", "format": ".1f"}}}]}

st.markdown('<div class="section">Key charts</div>', unsafe_allow_html=True)
left, right = st.columns(2)
with left:
    vega(spec_completion)
with right:
    vega(spec_funnel)
left, right = st.columns(2)
with left:
    vega(spec_time)
with right:
    vega(spec_step1)

# ---------------------------------------------------------------- tests
st.markdown('<div class="section">Hypothesis tests</div>', unsafe_allow_html=True)


def fmt_value(row, col):
    v = row[col]
    return f"{v:.1f} s" if row["kpi"].startswith("Time") else f"{v:.1%}"


table = pd.DataFrame({
    "KPI": tests["kpi"].str.replace(" (s)", "", regex=False)
    + tests["step"].map(lambda s: "" if s == "all" else f" · {STEP_LABELS.get(s, s)}"),
    "Question": tests["question"].str.replace("Test", "New Website", regex=False),
    OLD: tests.apply(fmt_value, axis=1, col="control"),
    NEW: tests.apply(fmt_value, axis=1, col="test"),
    "p-value": tests["p_value"].map(lambda v: "< 0.001" if v < 0.001 else f"{v:.3f}"),
    "Significant": tests["significant"],
})
head = "".join(f"<th>{html_lib.escape(c)}</th>" for c in table.columns)
body = "".join(
    "<tr>" + "".join(
        f'<td class="{"yes" if v == "Yes" else "no" if v == "No" else ""}">{html_lib.escape(str(v))}</td>'
        for v in row) + "</tr>"
    for row in table.itertuples(index=False))
st.markdown(f'<table class="tests"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>',
            unsafe_allow_html=True)
st.markdown('<div class="small">Completion and error rate: two-proportion z-test. '
            'Time on step: one-sided Welch t-test (H1: New Website is faster). '
            'α = 0.05.</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- recommendations
st.markdown('<div class="section">Recommendations</div>', unsafe_allow_html=True)
st.markdown(
    "1. **Fix step 1 first:** it's where clients spend extra time and go back to the start twice as often.\n"
    "2. **Roll out in phases** and track completion against the 5% cost-effectiveness threshold.\n"
    "3. **Run a longer follow-up test** outside the tax season to confirm where step 1 settles.\n"
    "4. **Collect the missing data:** device, in-page events, exit reasons and the value of each completion.")

# ---------------------------------------------------------------- footer
st.divider()
st.markdown(
    f'<div class="small">Source: Vanguard web logs, client profiles and experiment '
    f'roster, 15 Mar – 20 Jun 2017 ({len(clients):,} clients, {len(steps):,} actions). '
    f'Ironhack Data Analytics Project 2 · Team Ravenclaw: Juliana, Raquel, Lervin.<br>'
    f'<a href="{TABLEAU_URL}" target="_blank">Full Tableau dashboard</a> · '
    f'<a href="{GITHUB_URL}" target="_blank">GitHub repository</a></div>',
    unsafe_allow_html=True)
