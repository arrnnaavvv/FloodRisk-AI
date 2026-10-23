
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# FLOODRISK AI — SATELLITE FLOOD ANALYTICS DASHBOARD
# ============================================================

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"

st.set_page_config(
    page_title="FloodRisk AI | Research Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
NAVY = "#17324D"
TEAL = "#138A8A"
BLUE = "#4B83B8"
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
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #DCE5EC;
}
h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: #17324D !important;
}
h1 { font-weight: 800 !important; letter-spacing: -1px; }
h2, h3 { font-weight: 750 !important; }
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DCE5EC;
    padding: 18px 20px;
    border-radius: 12px;
    box-shadow: 0 2px 7px rgba(23,50,77,.035);
}
[data-testid="stMetricLabel"] { color: #617386 !important; }
[data-testid="stMetricValue"] {
    color: #17324D !important;
    font-weight: 800;
}
.small-label {
    text-transform: uppercase;
    letter-spacing: 1.6px;
    font-size: 11px;
    font-weight: 700;
    color: #138A8A;
}
.hero {
    background: linear-gradient(115deg, #FFFFFF 0%, #F0F7F8 100%);
    border: 1px solid #DCE5EC;
    border-radius: 16px;
    padding: 28px 30px;
    margin-bottom: 22px;
}
.hero-title {
    font-family: 'Manrope', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #17324D;
    line-height: 1.2;
}
.hero-sub {
    font-size: 15px;
    color: #617386;
    margin-top: 9px;
    line-height: 1.65;
}
.note {
    background: #FFFFFF;
    border: 1px solid #DCE5EC;
    border-left: 4px solid #138A8A;
    border-radius: 8px;
    padding: 13px 16px;
    color: #45596D;
    font-size: 13px;
}
hr { border-color: #DCE5EC; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ---------- Robust repository file handling ----------
def find_file(name):
    """Search expected repository locations for a file."""
    candidates = [
        DATA / name,
        RESULTS / name,
        FIGURES / name,
        ROOT / name,
    ]

    for path in candidates:
        if path.exists() and path.is_file():
            return path

    return None


def read_csv(name):
    path = find_file(name)
    if path is None:
        return None

    try:
        return pd.read_csv(path)
    except Exception as exc:
        st.warning(f"Could not read {name}: {exc}")
        return None


def show_image(name, caption=None, use_container_width=True):
    """Display an image from any supported project folder."""
    path = find_file(name)

    if path is None:
        st.warning(
            f"Image not found: {name}. "
            "Upload it into results/figures/ or data/processed/."
        )
        return False

    try:
        st.image(
            str(path),
            caption=caption,
            use_container_width=use_container_width,
        )
        return True
    except Exception as exc:
        st.error(f"Could not display {name}: {exc}")
        return False


def chart_layout(fig, height=390):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="DM Sans", color="#45596D", size=12),
        margin=dict(l=18, r=18, t=55, b=18),
        title_font=dict(family="Manrope", size=17, color=NAVY),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor=BORDER)
    fig.update_yaxes(gridcolor="#EAF0F4", zeroline=False)
    return fig


def section_heading(kicker, title, subtitle=None):
    st.markdown(
        f'<div class="small-label">{kicker}</div>',
        unsafe_allow_html=True,
    )
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        '<div class="small-label">REMOTE SENSING • ANALYTICS</div>',
        unsafe_allow_html=True,
    )
    st.markdown("## FloodRisk AI")
    st.caption("Flood inundation research prototype")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Map Explorer",
            "Rainfall Analysis",
            "Model Evaluation",
            "Data & Methodology",
        ],
    )

    st.divider()
    st.markdown("**STUDY AREA**")
    st.write("Dibrugarh pilot, Assam, India")
    st.markdown("**REFERENCE EVENT**")
    st.write("June–July 2022")
    st.divider()
    st.caption("Exploratory research • Not an operational warning system")


# ---------- Page header ----------
st.markdown(
    '<div class="small-label">EARTH OBSERVATION & FLOOD ANALYTICS</div>',
    unsafe_allow_html=True,
)

st.markdown("""
<div class="hero">
  <div class="hero-title">FloodRisk AI</div>
  <div class="hero-sub">
    Satellite-based flood inundation analysis and exploratory predictive
    analytics using Sentinel-1 SAR observations, terrain variables and
    regional rainfall indicators for a pilot study in Assam, India.
  </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# OVERVIEW
# ============================================================
if page == "Overview":

    section_heading(
        "01 / PROJECT SUMMARY",
        "Study overview",
        "A research workflow for exploring satellite-derived flood candidates.",
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Study region", "Dibrugarh")
    c2.metric("SAR sensor", "Sentinel-1")
    c3.metric("Reference event", "2022")
    c4.metric("Analysis type", "Exploratory")

    st.write("")
    left, right = st.columns([1.45, 1])

    with left:
        section_heading("SPATIAL OUTPUT", "Flood candidate mapping")

        image_found = show_image(
            "dibrugarh_candidate_map_report_ready.png",
            "Pilot flood-candidate mapping output",
        )

        if not image_found:
            image_found = show_image(
                "dibrugarh_candidate_map_comparison_fixed.png",
                "Candidate map comparison",
            )

        if not image_found:
            image_found = show_image(
                "dibrugarh_candidate_map_comparison.png",
                "Candidate map comparison",
            )

        if not image_found:
            st.info(
                "No candidate map image is included in the repository yet. "
                "Upload a PNG to results/figures/."
            )

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
        <b>Scientific interpretation:</b> mapped pixels are candidate
        inundation, not independently confirmed flood observations.
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    section_heading("SUPPORTING EVIDENCE", "Additional project outputs")

    left, right = st.columns(2)

    with left:
        st.markdown("**Satellite and reference comparison**")
        if not show_image("FloodRisk_AI_Premium_Comparison.png"):
            if not show_image("dibrugarh_shapefile_reference_comparison.png"):
                st.caption("Optional comparison figure not included.")

    with right:
        st.markdown("**Regional rainfall context**")
        rainfall = read_csv("assam_rainfall_features_may_july_2022.csv")

        if rainfall is None:
            rainfall = read_csv("assam_daily_rainfall_may_july_2022.csv")

        if rainfall is not None:
            date_col = next(
                (c for c in rainfall.columns
                 if c.lower() in ["date", "time"]),
                None,
            )
            numeric_cols = [
                c for c in rainfall.select_dtypes(include=np.number).columns
                if any(k in c.lower() for k in ["rain", "precip"])
            ]

            if date_col and numeric_cols:
                rainfall[date_col] = pd.to_datetime(
                    rainfall[date_col], errors="coerce"
                )
                fig = px.line(
                    rainfall,
                    x=date_col,
                    y=numeric_cols[0],
                    title="Regional rainfall indicator",
                    labels={date_col: "Date", numeric_cols[0]: "Rainfall"},
                )
                st.plotly_chart(
                    chart_layout(fig, 300),
                    use_container_width=True,
                )
            else:
                st.dataframe(rainfall.head(10), use_container_width=True)
        else:
            st.caption("Rainfall dataset not included in this repository.")


# ============================================================
# MAP EXPLORER
# ============================================================
elif page == "Map Explorer":

    section_heading(
        "02 / SPATIAL ANALYSIS",
        "Map explorer",
        "Review available map figures and reference comparisons.",
    )

    map_options = [
        ("dibrugarh_candidate_map_report_ready.png", "Candidate map — report-ready"),
        ("dibrugarh_candidate_map_comparison_fixed.png", "Candidate map comparison"),
        ("dibrugarh_candidate_map_comparison.png", "Candidate map comparison — original"),
        ("dibrugarh_shapefile_reference_comparison.png", "External reference comparison"),
        ("NRSC_reference_map_19_June_2022.png", "NRSC reference map"),
        ("NRSC_main_map_crop.png", "NRSC atlas map crop"),
        ("FloodRisk_AI_Premium_Comparison.png", "Premium comparison figure"),
    ]

    available = [
        (filename, label)
        for filename, label in map_options
        if find_file(filename) is not None
    ]

    if available:
        selected_label = st.selectbox(
            "Select a figure",
            [label for _, label in available],
        )
        selected_file = next(
            filename
            for filename, label in available
            if label == selected_label
        )
        show_image(selected_file, selected_label)
        st.caption(f"Repository file: {selected_file}")
    else:
        st.warning(
            "No recognised map images were found. "
            "Upload your selected PNG maps to results/figures/."
        )

    st.markdown("""
    <div class="note">
    <b>Map-reading note:</b> candidate masks and external reference
    footprints may differ because of acquisition dates, spatial coverage,
    mapping methods and permanent-water handling.
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# RAINFALL ANALYSIS
# ============================================================
elif page == "Rainfall Analysis":

    section_heading(
        "03 / HYDROMETEOROLOGICAL CONTEXT",
        "Rainfall analysis",
        "Regional rainfall indicators for May–July 2022.",
    )

    rainfall = read_csv("assam_rainfall_features_may_july_2022.csv")

    if rainfall is None:
        rainfall = read_csv("assam_daily_rainfall_may_july_2022.csv")

    if rainfall is None:
        st.warning(
            "Rainfall CSV not found. Upload the CSV into "
            "data/processed/ to enable this page."
        )
    else:
        st.write(f"**Records available:** {len(rainfall):,}")

        date_col = next(
            (c for c in rainfall.columns
             if c.lower() in ["date", "time"]),
            None,
        )

        numeric_cols = [
            c for c in rainfall.select_dtypes(include=np.number).columns
            if any(k in c.lower() for k in ["rain", "precip"])
        ]

        if date_col and numeric_cols:
            rainfall[date_col] = pd.to_datetime(
                rainfall[date_col], errors="coerce"
            )

            selected_var = st.selectbox(
                "Rainfall variable",
                numeric_cols,
            )

            fig = px.line(
                rainfall,
                x=date_col,
                y=selected_var,
                markers=True,
                title="Rainfall indicator over time",
                labels={date_col: "Date", selected_var: selected_var},
            )

            fig.add_vrect(
                x0="2022-06-16",
                x1="2022-07-17",
                fillcolor=TEAL,
                opacity=0.10,
                line_width=0,
                annotation_text="Reference event window",
            )

            st.plotly_chart(
                chart_layout(fig, 420),
                use_container_width=True,
            )
        else:
            st.info(
                "No recognised date and rainfall columns were found. "
                "Inspect the dataset below."
            )

        with st.expander("Inspect rainfall data"):
            st.dataframe(
                rainfall,
                use_container_width=True,
                hide_index=True,
            )

        st.info(
            "Rainfall is regional context, not pixel-level precipitation "
            "or independent proof of flood inundation."
        )


# ============================================================
# MODEL EVALUATION
# ============================================================
elif page == "Model Evaluation":

    section_heading(
        "04 / MODEL VALIDATION",
        "Generalisation and limitations",
        "Random splits can overstate performance when spatial observations are related.",
    )

    metrics = pd.DataFrame([
        {
            "Evaluation": "Random holdout",
            "Accuracy": 0.853,
            "Balanced accuracy": 0.853,
            "Precision": 0.815,
            "Recall": 0.913,
            "F1": 0.862,
        },
        {
            "Evaluation": "Eastern spatial holdout",
            "Accuracy": 0.681,
            "Balanced accuracy": 0.691,
            "Precision": 0.823,
            "Recall": 0.503,
            "F1": 0.624,
        },
    ])

    st.dataframe(
        metrics.style.format({
            "Accuracy": "{:.3f}",
            "Balanced accuracy": "{:.3f}",
            "Precision": "{:.3f}",
            "Recall": "{:.3f}",
            "F1": "{:.3f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Previously computed results against derived candidate labels, "
        "not independently verified flood ground truth."
    )

    fig = go.Figure()

    for metric in [
        "Accuracy",
        "Balanced accuracy",
        "Precision",
        "Recall",
        "F1",
    ]:
        fig.add_trace(
            go.Bar(
                name=metric,
                x=metrics["Evaluation"],
                y=metrics[metric],
            )
        )

    fig.update_layout(
        barmode="group",
        title="Random vs spatial holdout performance",
        yaxis_title="Score",
        yaxis_range=[0, 1],
    )

    st.plotly_chart(
        chart_layout(fig, 420),
        use_container_width=True,
    )

    left, right = st.columns(2)

    with left:
        st.markdown("### Random holdout")
        st.write(
            "Randomly held-out samples may resemble training samples "
            "geographically. This is useful as a baseline but can produce "
            "an optimistic estimate of geographic transfer."
        )

    with right:
        st.markdown("### Spatial holdout")
        st.write(
            "A held-out geographic region tests transfer more directly. "
            "The lower scores indicate that geographic generalisation "
            "remains a challenge."
        )

    st.markdown("""
    <div class="note">
    <b>Important:</b> the model's labels were derived from a radar-change
    candidate rule. Performance against those labels does not establish
    real-world flood detection accuracy.
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DATA & METHODOLOGY
# ============================================================
elif page == "Data & Methodology":

    section_heading(
        "05 / TECHNICAL NOTES",
        "Data, methods and reproducibility",
        "A transparent summary of inputs and assumptions.",
    )

    st.markdown("### Data inputs")
    st.markdown("""
    - **Sentinel-1 SAR:** before/during-event VV backscatter observations.
    - **Terrain:** elevation and slope aligned to the pilot raster.
    - **Rainfall:** regional daily and rolling-window indicators.
    - **Reference material:** NRSC mapping and an external footprint for exploratory comparison.
    """)

    st.markdown("### Candidate detection")
    st.write(
        "The pilot workflow flags pixels where VV backscatter decreases "
        "by approximately 3 dB between 6 June and 18 June 2022, using "
        "matching ascending-orbit observations. A permanent-water exclusion "
        "step reduces detections over frequently inundated water bodies."
    )

    st.markdown("### Known limitations")
    st.markdown("""
    1. Radar changes can result from soil moisture, vegetation, surface roughness and acquisition geometry.
    2. Candidate masks are not verified inundation labels.
    3. Rainfall inputs are regional rather than pixel-level.
    4. Spatial holdout performance is weaker than random holdout performance.
    5. External reference maps may differ in date, coverage and mapping method.
    6. This is not an operational forecast or an official ISRO product.
    """)

    st.markdown("### Repository assets")

    file_rows = []
    for folder in [DATA, RESULTS, FIGURES]:
        if folder.exists():
            for path in sorted(folder.iterdir()):
                if path.is_file():
                    file_rows.append({
                        "Folder": str(path.parent.relative_to(ROOT)),
                        "File": path.name,
                        "Size (MB)": round(
                            path.stat().st_size / (1024 * 1024), 2
                        ),
                    })

    if file_rows:
        st.dataframe(
            pd.DataFrame(file_rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No files found in the expected data and results folders.")


# ---------- Footer ----------
st.divider()
st.caption(
    "FloodRisk AI • Research prototype • Sentinel-1 SAR and environmental data • "
    "Exploratory analysis only; not an official flood-warning system."
)
