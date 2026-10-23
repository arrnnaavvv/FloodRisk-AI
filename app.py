
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"
RESULTS = ROOT / "results"

st.set_page_config(
    page_title="FloodRisk AI | Research Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Visual system ----------
NAVY = "#17324D"
TEAL = "#138A8A"
BLUE = "#4B83B8"
PALE = "#F3F7FA"
MUTED = "#617386"
BORDER = "#DCE5EC"
ORANGE = "#D68B32"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #203247;
}
.stApp { background: #F5F8FB; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px; }
[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #DCE5EC; }
[data-testid="stSidebar"] * { color: #203247; }
h1, h2, h3 { font-family: 'Manrope', sans-serif !important; color: #17324D; }
h1 { font-weight: 800 !important; letter-spacing: -1px; }
h2 { font-weight: 750 !important; letter-spacing: -0.4px; }
h3 { font-weight: 700 !important; }
[data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid #DCE5EC;
    padding: 18px 20px; border-radius: 12px;
    box-shadow: 0 2px 7px rgba(23,50,77,.035);
}
[data-testid="stMetricLabel"] { color: #617386 !important; font-size: 0.83rem; }
[data-testid="stMetricValue"] { color: #17324D !important; font-weight: 800; }
div[data-testid="stAlert"] { border-radius: 10px; }
hr { border-color: #DCE5EC; }
.stTabs [data-baseweb="tab-list"] { gap: 20px; }
.stTabs [data-baseweb="tab"] { font-weight: 600; }
.small-label {
    text-transform: uppercase; letter-spacing: 1.6px;
    font-size: 11px; font-weight: 700; color: #138A8A;
}
.hero {
    background: linear-gradient(115deg, #FFFFFF 0%, #F0F7F8 100%);
    border: 1px solid #DCE5EC; border-radius: 16px;
    padding: 28px 30px; margin-bottom: 22px;
}
.hero-title { font-family: 'Manrope', sans-serif; font-size: 32px;
    font-weight: 800; color: #17324D; line-height: 1.2; }
.hero-sub { font-size: 15px; color: #617386; margin-top: 9px; line-height: 1.65; }
.note {
    background: #FFFFFF; border: 1px solid #DCE5EC;
    border-left: 4px solid #138A8A; border-radius: 8px;
    padding: 13px 16px; color: #45596D; font-size: 13px;
}
.status {
    display:inline-block; padding:5px 10px; border-radius:20px;
    background:#E4F4F1; color:#13746D; font-size:11px;
    font-weight:700; letter-spacing:.5px;
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ---------- File helpers ----------
def find_file(name, folders=(DATA, RESULTS, ROOT)):
    for folder in folders:
        p = folder / name
        if p.exists():
            return p
    return None

def read_csv(name):
    p = find_file(name)
    if p is None:
        return None
    try:
        return pd.read_csv(p)
    except Exception:
        return None

def show_image(name, caption=None, use_container_width=True):
    p = find_file(name)
    if p:
        try:
            st.image(str(p), caption=caption, use_container_width=use_container_width)
            return True
        except Exception:
            pass
    return False

def chart_layout(fig, height=390):
    fig.update_layout(
        height=height, paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="DM Sans", color="#45596D", size=12),
        margin=dict(l=18, r=18, t=50, b=18),
        title_font=dict(family="Manrope", size=17, color="#17324D"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, linecolor="#DCE5EC")
    fig.update_yaxes(gridcolor="#EAF0F4", zeroline=False)
    return fig

def section_heading(kicker, title, subtitle=None):
    st.markdown(f'<div class="small-label">{kicker}</div>', unsafe_allow_html=True)
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="small-label">REMOTE SENSING • ANALYTICS</div>',
                unsafe_allow_html=True)
    st.markdown("## FloodRisk AI")
    st.caption("Flood inundation research prototype")
    st.divider()
    page = st.radio(
        "NAVIGATION",
        ["Overview", "Map Explorer", "Rainfall Analysis",
         "Model Evaluation", "Data & Methodology"],
        label_visibility="visible"
    )
    st.divider()
    st.markdown("**STUDY AREA**")
    st.write("Dibrugarh pilot, Assam, India")
    st.markdown("**EVENT WINDOW**")
    st.write("16 Jun – 17 Jul 2022")
    st.divider()
    st.caption("Research prototype • Not an operational warning system")

# ---------- Header ----------
st.markdown(
    '<div class="small-label">EARTH OBSERVATION & FLOOD ANALYTICS</div>',
    unsafe_allow_html=True
)
st.markdown("""
<div class="hero">
  <div class="hero-title">FloodRisk AI</div>
  <div class="hero-sub">
    Satellite-based flood inundation analysis and exploratory predictive
    analytics, using Sentinel-1 SAR observations, terrain variables and
    regional rainfall indicators for a pilot study in Assam, India.
  </div>
</div>
""", unsafe_allow_html=True)

if page == "Overview":
    section_heading("01 / PROJECT SUMMARY", "Study overview",
                    "A research workflow for exploring satellite-derived flood candidates and model limitations.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Study region", "Dibrugarh")
    m2.metric("SAR sensor", "Sentinel-1")
    m3.metric("Reference event", "Jun 2022")
    m4.metric("Analysis type", "Exploratory")

    st.markdown("")
    left, right = st.columns([1.45, 1])

    with left:
        section_heading("SPATIAL OUTPUT", "Flood candidate mapping")
        if not show_image("dibrugarh_candidate_map_report_ready.png",
                          "Pilot flood-candidate mapping output"):
            if not show_image("dibrugarh_candidate_map_comparison_fixed.png",
                              "Flood candidate map comparison"):
                if not show_image("dibrugarh_candidate_map_comparison.png",
                                  "Flood candidate map comparison"):
                    st.info("Map image not found. Add a final map image to data/processed or results.")

    with right:
        section_heading("ANALYTICAL WORKFLOW", "From observations to analysis")
        st.markdown("""
        **01 — Earth observation**  
        Sentinel-1 SAR before/during-event comparison.

        **02 — Candidate detection**  
        Radar backscatter change used to flag potential inundation.

        **03 — Environmental context**  
        Elevation, slope and regional rainfall features.

        **04 — Model evaluation**  
        Random and spatial holdout tests to examine generalisation.
        """)
        st.markdown("""
        <div class="note">
        <b>Interpretation:</b> mapped pixels are candidate inundation,
        not independently confirmed flood observations. Model scores
        against derived labels measure agreement with those labels,
        not verified real-world flood accuracy.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    section_heading("EVIDENCE & CONTEXT", "Supporting project outputs")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Satellite comparison**")
        if not show_image("FloodRisk_AI_Premium_Comparison.png",
                          "Candidate detection comparison"):
            if not show_image("dibrugarh_shapefile_reference_comparison.png",
                              "Comparison with an external reference footprint"):
                st.caption("Optional comparison figure not found.")
    with c2:
        st.markdown("**Rainfall context**")
        rainfall = read_csv("assam_rainfall_features_may_july_2022.csv")
        if rainfall is not None and "date" in rainfall.columns:
            rainfall["date"] = pd.to_datetime(rainfall["date"], errors="coerce")
            numeric = [c for c in rainfall.select_dtypes(include=np.number).columns
                       if any(k in c.lower() for k in ["rain", "precip"])]
            if numeric:
                f = px.line(rainfall, x="date", y=numeric[0],
                            title=f"Regional rainfall indicator: {numeric[0]}",
                            labels={"date":"Date", numeric[0]:"Rainfall"})
                st.plotly_chart(chart_layout(f, 300), use_container_width=True)
            else:
                st.caption("Rainfall CSV found, but no recognisable rainfall column was detected.")
        else:
            st.caption("Rainfall time-series file not found.")

elif page == "Map Explorer":
    section_heading("02 / SPATIAL ANALYSIS", "Map explorer",
                    "Review available raster-derived figures and reference comparisons.")
    map_options = [
        ("dibrugarh_candidate_map_report_ready.png", "Candidate map — report-ready"),
        ("dibrugarh_candidate_map_comparison_fixed.png", "Candidate map comparison"),
        ("dibrugarh_shapefile_reference_comparison.png", "External reference comparison"),
        ("NRSC_reference_map_19_June_2022.png", "NRSC reference map"),
        ("NRSC_main_map_crop.png", "NRSC atlas map crop"),
    ]
    available = [(f, label) for f, label in map_options if find_file(f)]
    if available:
        choice = st.selectbox("Select a figure", [x[1] for x in available])
        selected_file = next(x[0] for x in available if x[1] == choice)
        p = find_file(selected_file)
        st.image(str(p), caption=choice, use_container_width=True)
        st.caption(f"Source file: {selected_file}")
    else:
        st.warning("No recognised map images found. Check data/processed and results.")
    st.markdown("""
    <div class="note">
    <b>Map-reading note:</b> raster candidate masks and external reference
    footprints can differ because of acquisition dates, mapping methods,
    spatial coverage and permanent-water handling. They should not be
    interpreted as interchangeable ground truth.
    </div>
    """, unsafe_allow_html=True)

elif page == "Rainfall Analysis":
    section_heading("03 / HYDROMETEOROLOGICAL CONTEXT", "Rainfall analysis",
                    "Regional rainfall indicators for May–July 2022; not pixel-level precipitation.")
    rain = read_csv("assam_rainfall_features_may_july_2022.csv")
    if rain is None:
        rain = read_csv("assam_daily_rainfall_may_july_2022.csv")
    if rain is None:
        st.warning("Rainfall CSV not found in data/processed.")
    else:
        st.write(f"**Records:** {len(rain):,} rows")
        st.dataframe(rain.head(100), use_container_width=True, hide_index=True)
        datecol = next((c for c in rain.columns if c.lower() in ["date", "time"]), None)
        raincols = [c for c in rain.select_dtypes(include=np.number).columns
                    if any(k in c.lower() for k in ["rain", "precip"])]
        if datecol and raincols:
            rain[datecol] = pd.to_datetime(rain[datecol], errors="coerce")
            chosen = st.selectbox("Rainfall variable", raincols)
            fig = px.line(rain, x=datecol, y=chosen, markers=True,
                          title=f"Rainfall indicator over time",
                          labels={datecol:"Date", chosen:chosen})
            fig.add_vrect(x0="2022-06-16", x1="2022-07-17",
                          fillcolor=TEAL, opacity=.10, line_width=0,
                          annotation_text="Reference event window")
            st.plotly_chart(chart_layout(fig, 420), use_container_width=True)
        st.info("Rainfall is regional context. It should not be treated as a spatially resolved flood predictor.")

elif page == "Model Evaluation":
    section_heading("04 / MODEL VALIDATION", "Generalisation & limitations",
                    "Validation design matters: random splits can overstate performance on spatial data.")
    metrics = [
        {"Evaluation":"Random holdout","Accuracy":0.853,"Balanced accuracy":0.853,
         "Precision":0.815,"Recall":0.913,"F1":0.862},
        {"Evaluation":"Eastern spatial holdout","Accuracy":0.681,"Balanced accuracy":0.691,
         "Precision":0.823,"Recall":0.503,"F1":0.624},
    ]
    df = pd.DataFrame(metrics)
    st.dataframe(
        df.style.format({c:"{:.3f}" for c in df.columns if c != "Evaluation"}),
        use_container_width=True, hide_index=True
    )
    st.caption("These are previously computed results against derived candidate labels, not independently verified flood ground truth.")
    fig = go.Figure()
    for metric, color in [("Accuracy", BLUE), ("Balanced accuracy", TEAL),
                          ("Precision", ORANGE), ("Recall", "#8A77B5"), ("F1", "#617386")]:
        fig.add_trace(go.Bar(name=metric, x=df["Evaluation"], y=df[metric]))
    fig.update_layout(barmode="group", title="Random vs spatial holdout performance",
                      yaxis_title="Score", yaxis_range=[0,1])
    st.plotly_chart(chart_layout(fig, 420), use_container_width=True)

    st.markdown("### What the results mean")
    a, b = st.columns(2)
    with a:
        st.markdown("""
        **Random holdout**
        - Randomly held-out samples can resemble training samples spatially.
        - Useful as a baseline, but may give an optimistic view of geographic transfer.
        """)
    with b:
        st.markdown("""
        **Spatial holdout**
        - Holds out an eastern geographic region.
        - Lower performance indicates generalisation remains challenging.
        - More independent flood labels and event-level tests are needed.
        """)
    st.markdown("""
    <div class="note">
    <b>Important:</b> the training labels were derived from a radar-change
    candidate rule. The model therefore learns patterns associated with
    that rule; this is not proof that it detects true floodwater.
    </div>
    """, unsafe_allow_html=True)

elif page == "Data & Methodology":
    section_heading("05 / TECHNICAL NOTES", "Data, methods & reproducibility",
                    "A transparent summary of the prototype's inputs and assumptions.")
    st.markdown("### Data inputs")
    st.markdown("""
    - **Sentinel-1 SAR:** before/during-event VV backscatter observations.
    - **Terrain:** elevation and slope aligned to the pilot raster.
    - **Rainfall:** regional daily and rolling-window indicators.
    - **Reference material:** NRSC flood mapping and an external footprint used for exploratory comparison.
    """)
    st.markdown("### Candidate detection")
    st.markdown("""
    The pilot workflow flags pixels where VV backscatter decreases by more
    than approximately 3 dB between 6 June and 18 June 2022, using matching
    ascending-orbit observations. A permanent-water mask is applied to
    reduce detections over frequently inundated water bodies.
    """)
    st.markdown("### Known limitations")
    st.markdown("""
    1. Radar backscatter change can also be caused by soil moisture, vegetation, geometry and other surface changes.
    2. Candidate masks are not verified inundation labels.
    3. Rainfall inputs are regional rather than pixel-level.
    4. Spatial holdout performance is weaker than random holdout performance.
    5. External reference maps may differ in date, coverage and mapping method.
    6. This prototype is not an operational forecast or an official ISRO product.
    """)
    st.markdown("### Available files")
    files = []
    for folder in [DATA, RESULTS]:
        if folder.exists():
            for p in sorted(folder.iterdir()):
                if p.is_file() and p.suffix.lower() in [".csv", ".png", ".md", ".tif", ".xlsx"]:
                    try:
                        files.append({"Folder":str(p.parent.relative_to(ROOT)),
                                      "File":p.name,
                                      "Size (MB)":round(p.stat().st_size/1024**2, 2)})
                    except Exception:
                        pass
    if files:
        st.dataframe(pd.DataFrame(files), use_container_width=True, hide_index=True)
    else:
        st.caption("No recognised output files were found in the expected folders.")

st.divider()
st.caption(
    "FloodRisk AI • Research prototype • Sentinel-1 SAR and environmental data • "
    "Interpret outputs as exploratory analysis, not official flood warnings."
)
