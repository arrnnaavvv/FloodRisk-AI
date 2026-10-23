# FloodRisk AI
### Satellite-Based Flood Inundation Analysis and Exploratory Predictive Analytics

FloodRisk AI is a research prototype exploring satellite-based flood-candidate
mapping in Dibrugarh, Assam, India. It combines Sentinel-1 SAR backscatter
change, terrain variables and regional rainfall indicators in a scientific
dashboard.

> **Important:** This is an independent research prototype, not an official
> ISRO product, an operational flood forecast, or an emergency-warning system.
> Satellite-derived candidate pixels are not equivalent to verified floodwater.

## Dashboard
The Streamlit dashboard provides:
- Project overview and workflow
- Map and figure explorer
- Regional rainfall time-series exploration
- Random versus spatial holdout model evaluation
- Data, methodology and limitations

## Study design
The pilot candidate-detection workflow compares Sentinel-1 VV backscatter
observations from 6 June and 18 June 2022, using matching ascending-orbit
observations. A decrease of approximately 3 dB is used as a candidate
inundation indicator, with a permanent-water exclusion step.

Radar changes can also result from soil moisture, vegetation, surface
roughness, acquisition geometry and other effects. The resulting mask is
therefore treated as a candidate layer rather than definitive flood truth.

## Model evaluation
Previously computed exploratory results:

| Evaluation split | Accuracy | Balanced accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| Random holdout | 0.853 | 0.853 | 0.815 | 0.913 | 0.862 |
| Eastern spatial holdout | 0.681 | 0.691 | 0.823 | 0.503 | 0.624 |

These metrics compare predictions with labels derived from a candidate-detection
rule. They do **not** measure accuracy against independently verified flood
observations. The weaker spatial holdout results also indicate that geographic
generalisation remains challenging.

An exploratory external-reference comparison produced an IoU of approximately
3.48%. Reference footprints may differ in date, coverage and mapping method;
this score should not be interpreted as a definitive validation result.

## Data and reproducibility
Only selected, lightweight figures and regional rainfall CSV files are
included in this repository. Large satellite rasters, raw data and intermediate
files are intentionally excluded. Not every original analytical input is
packaged here, so the repository is not a complete reproduction archive.

## Run locally
Use Python 3.10 or later, then install dependencies:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard looks for optional files in `data/processed/` and
`results/figures/`. If a figure or data file is absent, some panels may show
a missing-file message.

## Technologies
- Python
- Streamlit
- Pandas and NumPy
- Plotly
- Sentinel-1 SAR and terrain/rainfall data workflows

## Responsible interpretation
This project is for portfolio and exploratory research purposes. It should not
be used for evacuation decisions, emergency response or real-world flood
warnings without rigorous independent validation.
