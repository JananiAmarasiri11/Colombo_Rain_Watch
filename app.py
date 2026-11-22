# Rainfall forecasting dashboard for Colombo.
from pathlib import Path
import base64

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from catboost import CatBoostRegressor

st.set_page_config(
    page_title="Colombo Rain Watch",
    page_icon=str(Path(__file__).resolve().parent / "Images" / "appimage.jpg"),
    layout="wide",
)

folder = Path(__file__).resolve().parent


@st.cache_data
def load_data():
    weather = (
        pd.read_csv(folder / "colombo_weather_daily.csv", parse_dates=["date"])
        .set_index("date")
        .sort_index()
    )
    scores = pd.read_csv(folder / "model_comparison.csv").set_index("Model")
    predictions = (
        pd.read_csv(folder / "predictions_2025.csv", parse_dates=["date"])
        .set_index("date")
        .sort_index()
    )
    return weather, scores, predictions


@st.cache_resource
def load_model():
    model = CatBoostRegressor()
    model.load_model(str(folder / "colombo_catboost.cbm"))
    return model


weather, scores, predictions = load_data()
model = load_model()


@st.cache_data
def load_hero_images():
    image_folder = folder / "Images"
    supported = {".jpg", ".jpeg", ".png", ".webp"}
    images = []
    for path in sorted(image_folder.iterdir()):
        if path.is_file() and path.suffix.lower() in supported and path.stem.lower() != "appimage":
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else f"image/{path.suffix.lower()[1:]}"
            images.append(f"data:{mime};base64,{encoded}")
    return images


hero_images = load_hero_images()


@st.cache_data
def load_app_image():
    path = folder / "Images" / "appimage.jpg"
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background:
            radial-gradient(circle at 88% 5%, rgba(35, 175, 184, 0.10), transparent 22rem),
            #F4F8F7;
    }
    [data-testid="stSidebar"] {
        background: #123F47;
        border-right: 0;
    }
    [data-testid="stSidebar"] * {
        color: #EFF8F7;
    }
    [data-testid="stSidebar"] .stRadio > label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.11em;
        color: #A8CBCF !important;
        margin-bottom: 0.5rem;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        width: 100%;
        box-sizing: border-box;
        min-height: 48px;
        border-radius: 12px;
        padding: 10px 14px;
        margin: 4px 0;
        background: transparent;
        border: 1px solid transparent;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.07);
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: #E8F4F2;
        border-color: #E8F4F2;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) * {
        color: #123F47 !important;
        font-weight: 700;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] input {
        display: none;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    #MainMenu, footer { visibility: hidden; }
    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 4px 28px;
        border-bottom: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 18px;
    }
    .brand-mark {
        width: 42px;
        height: 42px;
        border-radius: 14px;
        overflow: hidden;
        background: #FFCA72;
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    .brand-mark img {
        width: 100%;
        height: 100%;
        display: block;
        object-fit: cover;
    }
    .brand-name {
        font-family: 'Manrope', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.15;
    }
    .brand-sub {
        color: #A8CBCF !important;
        font-size: 0.72rem;
        margin-top: 4px;
    }
    .sidebar-foot {
        position: fixed;
        bottom: 20px;
        left: 22px;
        color: #A8CBCF;
        font-size: 0.72rem;
    }
    .hero {
        position: relative;
        overflow: hidden;
        min-height: 180px;
        border-radius: 24px;
        padding: 30px 34px;
        margin-bottom: 18px;
        background: #123F47;
        color: white;
        box-shadow: 0 16px 38px rgba(18,63,71,0.12);
    }
    .hero-slide {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 58%;
        width: 42%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        opacity: 0;
        -webkit-mask-image: linear-gradient(90deg, transparent 0, rgba(0,0,0,0.35) 12%, black 28%);
        mask-image: linear-gradient(90deg, transparent 0, rgba(0,0,0,0.35) 12%, black 28%);
        animation: heroCrossfade 20s infinite;
    }
    .hero-slide:nth-child(1) { animation-delay: 0s; }
    .hero-slide:nth-child(2) { animation-delay: 5s; }
    .hero-slide:nth-child(3) { animation-delay: 10s; }
    .hero-slide:nth-child(4) { animation-delay: 15s; }
    .hero:before {
        content: "";
        position: absolute;
        inset: 0;
        z-index: 1;
        background: linear-gradient(90deg, rgba(18,63,71,0.96) 0%, rgba(18,63,71,0.92) 54%, rgba(18,63,71,0.18) 72%, rgba(18,63,71,0.05) 100%);
        pointer-events: none;
    }
    .hero-content {
        position: relative;
        z-index: 2;
    }
    @keyframes heroCrossfade {
        0% { opacity: 0; }
        5% { opacity: 1; }
        20% { opacity: 1; }
        25%, 100% { opacity: 0; }
    }
    .hero-kicker {
        color: #CBEAE6;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }
    .hero h1 {
        color: white;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.04;
        margin: 9px 0 10px;
        letter-spacing: -0.04em;
    }
    .hero p {
        color: #DCF1EE;
        margin: 0;
        max-width: 560px;
    }
    .section-title {
        font-family: 'Manrope', sans-serif;
        color: #173D45;
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 8px 0 12px;
    }
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #DFEAE7;
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 6px 18px rgba(30,72,67,0.04);
    }
    [data-testid="stMetricLabel"] {
        color: #718986;
        font-size: 0.78rem;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: #173D45;
        font-family: 'Manrope', sans-serif;
        font-size: 1.7rem;
    }
    [data-testid="stMetricDelta"] {
        color: #238B8C;
    }
    [data-testid="stForm"], [data-testid="stExpander"] {
        background: white;
        border: 1px solid #DFEAE7;
        border-radius: 18px;
        padding: 18px;
    }
    [data-testid="stExpander"] {
        margin-top: 12px;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border: 1px solid #DFEAE7;
        border-radius: 14px;
        padding: 5px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #718986;
    }
    .stTabs [aria-selected="true"] {
        background: #E5F2EF;
        color: #17666B;
        font-weight: 700;
    }
    .stDataFrame {
        border: 1px solid #DFEAE7;
        border-radius: 14px;
        overflow: hidden;
    }
    .stButton > button, [data-testid="stFormSubmitButton"] button {
        width: 100%;
        border: 0;
        border-radius: 12px;
        min-height: 46px;
        background: #176E73;
        color: white;
        font-weight: 700;
        box-shadow: 0 8px 18px rgba(23,110,115,0.16);
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
        background: #115E63;
        color: white;
    }
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        border-radius: 10px;
        border-color: #D8E6E3;
        background: #FAFCFB;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    app_image = load_app_image()
    st.markdown(
        f"""
        <div class="brand">
            <div class="brand-mark">
                <img src="{app_image}" alt="Colombo Rain Watch">
            </div>
            <div>
                <div class="brand-name">Colombo<br>Rain Watch</div>
                <div class="brand-sub">Forecast intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Workspace",
        ["Overview", "Model comparison", "Date explorer", "Prediction lab"],
        label_visibility="visible",
    )
    st.markdown(
        '<div class="sidebar-foot">ERA5 · Open-Meteo<br>Test year 2025</div>',
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=330):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=25, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="DM Sans", color="#557174"),
        hoverlabel=dict(bgcolor="#173D45", font_color="white"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#E9F0EE", zeroline=False)
    return fig


hero_slides = "".join(
    f'<img class="hero-slide" src="{image}" alt="">'
    for image in hero_images
)

st.markdown(
    f"""
    <header class="hero">
        {hero_slides}
        <div class="hero-content">
            <div class="hero-kicker">Colombo, Sri Lanka · 2025 outlook</div>
            <h1>Rainfall intelligence<br>at a glance.</h1>
            <p>Explore historical rainfall, benchmark forecasting models, and test next-day predictions.</p>
        </div>
    </header>
    """,
    unsafe_allow_html=True,
)

if page == "Overview":
    best = scores["MAE (mm)"].idxmin()
    best_mae = scores["MAE (mm)"].min()
    annual_rain = predictions["Actual rainfall (mm)"].sum()
    wettest = predictions["Actual rainfall (mm)"].idxmax()
    wettest_amount = predictions["Actual rainfall (mm)"].max()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Archive records", f"{len(weather):,}")
    k2.metric("2025 rainfall", f"{annual_rain:.1f} mm")
    k3.metric("Best MAE", f"{best_mae:.2f} mm", best)
    k4.metric("Wettest day", f"{wettest_amount:.1f} mm", wettest.strftime("%d %b"))

    left, right = st.columns([2, 1])
    with left:
        st.markdown('<div class="section-title">2025 rainfall timeline</div>', unsafe_allow_html=True)
        timeline = predictions.loc[
            predictions.index >= pd.Timestamp("2025-01-01"),
            ["Actual rainfall (mm)", "CatBoost"],
        ]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timeline.index,
            y=timeline["Actual rainfall (mm)"],
            name="Observed",
            mode="lines",
            line=dict(color="#91B9B2", width=2),
            fill="tozeroy",
            fillcolor="rgba(145,185,178,0.16)",
        ))
        fig.add_trace(go.Scatter(
            x=timeline.index,
            y=timeline["CatBoost"],
            name="CatBoost",
            mode="lines",
            line=dict(color="#176E73", width=2),
        ))
        fig.update_layout(
            legend=dict(orientation="h", y=1.12, x=0),
            hovermode="x unified",
            yaxis_title="Rainfall (mm)",
        )
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Wettest months</div>', unsafe_allow_html=True)
        monthly = predictions["Actual rainfall (mm)"].resample("ME").sum()
        labels = [d.strftime("%b") for d in monthly.index]
        fig = go.Figure(go.Bar(
            x=labels,
            y=monthly.values,
            marker=dict(
                color=monthly.values,
                colorscale=[[0, "#D6E8E4"], [1, "#176E73"]],
            ),
            text=[f"{v:.0f}" for v in monthly.values],
            textposition="outside",
        ))
        fig.update_layout(yaxis_title="Rainfall (mm)", showlegend=False)
        st.plotly_chart(chart_layout(fig, 330), use_container_width=True)

elif page == "Model comparison":
    st.markdown('<div class="section-title">Model benchmark</div>', unsafe_allow_html=True)
    metric = st.selectbox(
        "Error measure",
        ["MAE (mm)", "Wettest-days MAE (mm)", "RMSE (mm)"],
    )
    ranked = scores.sort_values(metric)
    c1, c2 = st.columns([1, 3])
    with c1:
        st.metric(
            "Top performer",
            ranked.index[0],
            f"{ranked[metric].iloc[0]:.2f} mm",
        )
        st.caption(
            "Lower values indicate smaller forecast errors across the 365-day test."
        )
    with c2:
        fig = go.Figure(go.Bar(
            x=ranked[metric].values,
            y=ranked.index,
            orientation="h",
            marker=dict(
                color=["#176E73" if i == 0 else "#B9D8D2" for i in range(len(ranked))],
            ),
            text=[f"{v:.2f}" for v in ranked[metric].values],
            textposition="outside",
        ))
        fig.update_layout(
            yaxis=dict(autorange="reversed"),
            xaxis_title="Error (mm)",
            showlegend=False,
        )
        st.plotly_chart(chart_layout(fig, 390), use_container_width=True)

    st.markdown('<div class="section-title">All test metrics</div>', unsafe_allow_html=True)
    st.dataframe(ranked.round(3), use_container_width=True)
    with st.expander("Explore the weather archive"):
        st.caption(f"{len(weather):,} daily records from {weather.index.min().year} to {weather.index.max().year}.")
        st.dataframe(weather, use_container_width=True, height=280)

elif page == "Date explorer":
    st.markdown('<div class="section-title">Compare a forecast with observed rainfall</div>', unsafe_allow_html=True)
    controls = st.columns([1, 1, 2])
    with controls[0]:
        chosen = st.date_input(
            "Test date",
            value=pd.Timestamp("2025-11-28").date(),
            min_value=predictions.index.min().date(),
            max_value=predictions.index.max().date(),
        )
    with controls[1]:
        name = st.selectbox("Forecast method", scores.index.tolist())

    day = pd.Timestamp(chosen)
    row = predictions.loc[day]
    observed = row["Actual rainfall (mm)"]
    forecast = row[name]
    error = abs(observed - forecast)

    a, b, c = st.columns(3)
    a.metric("Observed rainfall", f"{observed:.2f} mm")
    b.metric("Forecast rainfall", f"{forecast:.2f} mm")
    c.metric("Absolute error", f"{error:.2f} mm", "Excellent" if error < 5 else "Review")

    week = pd.Timedelta(days=7)
    window = predictions.loc[day - week:day + week, ["Actual rainfall (mm)", name]]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=window.index,
        y=window["Actual rainfall (mm)"],
        name="Observed",
        marker=dict(color="#A8CBCF"),
    ))
    fig.add_trace(go.Scatter(
        x=window.index,
        y=window[name],
        name=name,
        mode="lines+markers",
        line=dict(color="#176E73", width=3),
        marker=dict(size=7),
    ))
    fig.update_layout(
        barmode="group",
        yaxis_title="Rainfall (mm)",
        legend=dict(orientation="h", y=1.12, x=0),
        hovermode="x unified",
    )
    st.plotly_chart(chart_layout(fig, 390), use_container_width=True)

else:
    st.markdown('<div class="section-title">CatBoost prediction workspace</div>', unsafe_allow_html=True)
    example = st.date_input(
        "Load historical weather inputs for",
        value=pd.Timestamp("2025-11-28").date(),
        min_value=predictions.index.min().date(),
        max_value=predictions.index.max().date(),
    )
    target = pd.Timestamp(example)
    prior = weather.loc[weather.index < target].tail(7)
    if len(prior) < 7:
        st.error("Not enough earlier weather records for this date.")
        st.stop()

    defaults = {
        "rain_lag_1": prior["rain_mm"].iloc[-1],
        "rain_lag_2": prior["rain_mm"].iloc[-2],
        "rain_lag_3": prior["rain_mm"].iloc[-3],
        "rain_lag_7": prior["rain_mm"].iloc[-7],
        "rain_avg_7d": prior["rain_mm"].mean(),
        "previous_max_temp_c": prior["max_temp_c"].iloc[-1],
        "previous_min_temp_c": prior["min_temp_c"].iloc[-1],
        "previous_max_wind_kmh": prior["max_wind_kmh"].iloc[-1],
        "month": target.month,
    }
    labels = {
        "rain_lag_1": "Rain yesterday",
        "rain_lag_2": "Rain two days ago",
        "rain_lag_3": "Rain three days ago",
        "rain_lag_7": "Rain seven days ago",
        "rain_avg_7d": "7-day average rainfall",
        "previous_max_temp_c": "Yesterday's maximum temperature",
        "previous_min_temp_c": "Yesterday's minimum temperature",
        "previous_max_wind_kmh": "Yesterday's maximum wind",
        "month": "Forecast month",
    }
    units = {
        "rain_lag_1": "mm",
        "rain_lag_2": "mm",
        "rain_lag_3": "mm",
        "rain_lag_7": "mm",
        "rain_avg_7d": "mm/day",
        "previous_max_temp_c": "°C",
        "previous_min_temp_c": "°C",
        "previous_max_wind_kmh": "km/h",
        "month": "",
    }

    form_col, result_col = st.columns([1.5, 1])
    with form_col:
        with st.form(f"forecast_{example}"):
            inputs = {}
            feature_columns = st.columns(2)
            for index, feature in enumerate(model.feature_names_):
                with feature_columns[index % 2]:
                    label = f"{labels[feature]} ({units[feature]})" if units[feature] else labels[feature]
                    if feature == "month":
                        inputs[feature] = st.number_input(
                            label, min_value=1, max_value=12, value=target.month
                        )
                    else:
                        inputs[feature] = st.number_input(
                            label,
                            value=float(defaults[feature]),
                            format="%.3f",
                        )
            submitted = st.form_submit_button("Generate rainfall forecast")

    with result_col:
        st.markdown('<div class="section-title">Forecast result</div>', unsafe_allow_html=True)
        if submitted:
            if inputs["previous_min_temp_c"] > inputs["previous_max_temp_c"]:
                st.error("Minimum temperature must be at or below maximum temperature.")
            elif any(
                inputs[k] < 0
                for k in inputs
                if k.startswith("rain_") or k == "previous_max_wind_kmh"
            ):
                st.error("Rainfall and wind speed must be zero or higher.")
            else:
                sample = pd.DataFrame([inputs], columns=model.feature_names_)
                estimate = max(0.0, float(model.predict(sample)[0]))
                st.metric("Predicted rainfall", f"{estimate:.2f} mm")
                if estimate < 2:
                    st.success("Low rainfall signal")
                elif estimate < 10:
                    st.info("Moderate rainfall signal")
                else:
                    st.warning("Heavy rainfall signal")
        else:
            st.metric("Predicted rainfall", "-- mm")
            st.caption("Adjust the inputs and generate a forecast.")

    st.markdown('<div class="section-title">Feature influence</div>', unsafe_allow_html=True)
    importance = pd.Series(
        model.get_feature_importance(),
        index=[labels[k] for k in model.feature_names_],
        name="Feature importance",
    ).sort_values(ascending=True)
    fig = go.Figure(go.Bar(
        x=importance.values,
        y=importance.index,
        orientation="h",
        marker=dict(
            color=importance.values,
            colorscale=[[0, "#D6E8E4"], [1, "#176E73"]],
        ),
    ))
    fig.update_layout(
        xaxis_title="Relative importance",
        showlegend=False,
    )
    st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
