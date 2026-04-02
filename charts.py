# charts.py
from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go

COLORS = {
    "Positive": "#00e676",
    "Neutral":  "#40c4ff",
    "Negative": "#ff5252",
}
GPAY_COLOR   = "#00d4ff"
PHONPE_COLOR = "#aa00ff"
FONT_COLOR   = "#e2e8f0"
GRID_COLOR   = "rgba(255,255,255,0.07)"

_BASE = dict(
    plot_bgcolor  = "rgba(0,0,0,0)",
    paper_bgcolor = "rgba(0,0,0,0)",
    font          = dict(color=FONT_COLOR, family="Inter, sans-serif"),
    margin        = dict(l=20, r=20, t=60, b=20),
)

_LEG = dict(
    bgcolor     = "rgba(30,30,50,0.8)",
    bordercolor = "rgba(255,255,255,0.10)",
    borderwidth = 1,
)


def _pct(df: pd.DataFrame, s: str) -> float:
    if df.empty:
        return 0.0
    return (df["Sentiment"] == s).sum() / len(df) * 100


# ─────────────────────────────────────────────────────────────────────────────
# 1. DONUT
# ─────────────────────────────────────────────────────────────────────────────
def donut_chart(df: pd.DataFrame, brand: str, accent: str) -> go.Figure:
    order  = ["Positive", "Neutral", "Negative"]
    counts = df["Sentiment"].value_counts().reindex(order, fill_value=0)

    fig = go.Figure(go.Pie(
        labels        = counts.index.tolist(),
        values        = counts.values.tolist(),
        hole          = 0.60,
        marker        = dict(
            colors = [COLORS[l] for l in counts.index],
            line   = dict(color="#0a0a14", width=4),
        ),
        textinfo      = "label+percent",
        textposition  = "outside",
        textfont      = dict(size=12, color=FONT_COLOR),
        hovertemplate = (
            "<b>%{label}</b><br>"
            "Count: %{value:,}<br>"
            "Share: %{percent}<extra></extra>"
        ),
        rotation  = 120,
        pull      = [0.03, 0.03, 0.03],
        automargin= True,
    ))

    fig.add_annotation(
        text=(
            f"<b>{len(df):,}</b><br>"
            "<span style='font-size:11px;color:#718096'>reviews</span>"
        ),
        x=0.5, y=0.5,
        font=dict(size=18, color=accent),
        showarrow=False,
    )

    fig.update_layout(
        title=dict(
            text    = f"<b>{brand}</b>",
            font    = dict(size=16, color=accent),
            x       = 0.5,
            y       = 0.97,
            xanchor = "center",
            yanchor = "top",
        ),
        showlegend = True,
        legend     = dict(
            **_LEG,
            orientation = "h",
            y           = -0.08,
            xanchor     = "center",
            x           = 0.5,
        ),
        height = 420,
        margin = dict(l=40, r=40, t=80, b=40),
        plot_bgcolor  = "rgba(0,0,0,0)",
        paper_bgcolor = "rgba(0,0,0,0)",
        font          = dict(color=FONT_COLOR, family="Inter, sans-serif"),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 2. GAUGE
# ─────────────────────────────────────────────────────────────────────────────
def gauge_chart(score: float, brand: str, accent: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode   = "gauge+number",
        value  = score,
        number = dict(
            valueformat = ".3f",
            font        = dict(color=accent, size=32, family="Inter"),
        ),
        gauge  = dict(
            axis        = dict(
                range     = [-1, 1],
                tickcolor = FONT_COLOR,
                tickfont  = dict(color=FONT_COLOR, size=11),
            ),
            bar         = dict(color=accent, thickness=0.22),
            bgcolor     = "rgba(0,0,0,0)",
            bordercolor = "rgba(255,255,255,0.08)",
            steps       = [
                dict(range=[-1,    -0.05], color="rgba(255,82,82,0.10)"),
                dict(range=[-0.05,  0.05], color="rgba(64,196,255,0.07)"),
                dict(range=[ 0.05,  1   ], color="rgba(0,230,118,0.10)"),
            ],
            threshold   = dict(
                line      = dict(color=accent, width=3),
                thickness = 0.82,
                value     = score,
            ),
        ),
        title  = dict(
            text=(
                f"<b>{brand}</b><br>"
                "<span style='font-size:12px;color:#718096'>Avg VADER Score</span>"
            ),
            font=dict(color=FONT_COLOR, size=14),
        ),
    ))
    fig.update_layout(height=270, **_BASE)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 3. GROUPED BAR
# ─────────────────────────────────────────────────────────────────────────────
def grouped_bar(gpay: pd.DataFrame, phonpe: pd.DataFrame) -> go.Figure:
    cats  = ["Positive", "Neutral", "Negative"]
    g_cnt = gpay["Sentiment"].value_counts().reindex(cats, fill_value=0)
    p_cnt = phonpe["Sentiment"].value_counts().reindex(cats, fill_value=0)

    fig = go.Figure()
    for counts, name, color in [
        (g_cnt, "Google Pay", GPAY_COLOR),
        (p_cnt, "PhonePe",   PHONPE_COLOR),
    ]:
        fig.add_trace(go.Bar(
            name          = name,
            x             = cats,
            y             = counts.values,
            marker_color  = color,
            marker_line   = dict(width=0),
            text          = counts.values,
            textposition  = "outside",
            hovertemplate = "<b>%{x}</b><br>Count: %{y:,}<extra>" + name + "</extra>",
        ))

    fig.update_layout(
        title   = dict(text="<b>Sentiment Count Comparison</b>",
                       font=dict(size=15), x=0.5),
        barmode = "group",
        xaxis   = dict(showgrid=False),
        yaxis   = dict(showgrid=True, gridcolor=GRID_COLOR),
        legend  = _LEG,
        **_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 4. STACKED % BAR
# ─────────────────────────────────────────────────────────────────────────────
def stacked_pct_bar(gpay: pd.DataFrame, phonpe: pd.DataFrame) -> go.Figure:
    cats   = ["Positive", "Neutral", "Negative"]
    brands = {"Google Pay": gpay, "PhonePe": phonpe}

    fig = go.Figure()
    for sentiment in cats:
        y_vals = [round(_pct(df, sentiment), 2) for df in brands.values()]
        fig.add_trace(go.Bar(
            name             = sentiment,
            x                = list(brands.keys()),
            y                = y_vals,
            marker_color     = COLORS[sentiment],
            text             = [f"{v:.1f}%" for v in y_vals],
            textposition     = "inside",
            insidetextanchor = "middle",
            hovertemplate    = f"<b>{sentiment}</b>: %{{y:.1f}}%<extra></extra>",
        ))

    fig.update_layout(
        title   = dict(text="<b>Sentiment Share (%) by Brand</b>",
                       font=dict(size=15), x=0.5),
        barmode = "stack",
        xaxis   = dict(showgrid=False),
        yaxis   = dict(showgrid=True, gridcolor=GRID_COLOR,
                       ticksuffix="%", range=[0, 105]),
        legend  = _LEG,
        **_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 5. RADAR
# ─────────────────────────────────────────────────────────────────────────────
def radar_chart(gpay: pd.DataFrame, phonpe: pd.DataFrame) -> go.Figure:
    cats = ["Positive", "Neutral", "Negative"]
    fig  = go.Figure()

    for df, name, color, fill in [
        (gpay,   "Google Pay", GPAY_COLOR,  "rgba(0,212,255,0.15)"),
        (phonpe, "PhonePe",   PHONPE_COLOR, "rgba(170,0,255,0.15)"),
    ]:
        vals = [_pct(df, s) for s in cats]
        fig.add_trace(go.Scatterpolar(
            r          = vals + [vals[0]],
            theta      = cats + [cats[0]],
            fill       = "toself",
            name       = name,
            line_color = color,
            fillcolor  = fill,
        ))

    fig.update_layout(
        title  = dict(text="<b>Sentiment Radar</b>",
                      font=dict(size=15), x=0.5),
        polar  = dict(
            bgcolor     = "rgba(0,0,0,0)",
            radialaxis  = dict(
                visible    = True,
                range      = [0, 100],
                color      = FONT_COLOR,
                gridcolor  = GRID_COLOR,
                ticksuffix = "%",
            ),
            angularaxis = dict(color=FONT_COLOR),
        ),
        legend = _LEG,
        **_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 6. SCORE HISTOGRAM
# ─────────────────────────────────────────────────────────────────────────────
def score_histogram(gpay: pd.DataFrame, phonpe: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for df, name, color in [
        (gpay,   "Google Pay", GPAY_COLOR),
        (phonpe, "PhonePe",   PHONPE_COLOR),
    ]:
        if df.empty:
            continue
        fig.add_trace(go.Histogram(
            x             = df["Score"],
            name          = name,
            marker_color  = color,
            opacity       = 0.72,
            nbinsx        = 50,
            hovertemplate = "Score: %{x:.2f}<br>Count: %{y}<extra>" + name + "</extra>",
        ))

    for x_val, color, label, pos in [
        ( 0.05, COLORS["Positive"], "Pos", "top right"),
        (-0.05, COLORS["Negative"], "Neg", "top left"),
    ]:
        fig.add_vline(
            x                     = x_val,
            line_dash             = "dash",
            line_color            = color,
            opacity               = 0.7,
            annotation_text       = label,
            annotation_position   = pos,
            annotation_font_color = color,
        )

    fig.update_layout(
        title   = dict(text="<b>VADER Score Distribution</b>",
                       font=dict(size=15), x=0.5),
        barmode = "overlay",
        xaxis   = dict(title="Compound Score", showgrid=False,
                       range=[-1.05, 1.05]),
        yaxis   = dict(title="Count", showgrid=True, gridcolor=GRID_COLOR),
        legend  = _LEG,
        **_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 7. RATING vs SENTIMENT box
# ─────────────────────────────────────────────────────────────────────────────
def rating_vs_sentiment(df: pd.DataFrame, brand: str, accent: str) -> go.Figure:
    if "rating" not in df.columns or df["rating"].isna().all():
        return go.Figure()

    fig = go.Figure()
    for sentiment in ["Positive", "Neutral", "Negative"]:
        sub = df[df["Sentiment"] == sentiment]["rating"].dropna()
        if sub.empty:
            continue
        fig.add_trace(go.Box(
            y             = sub,
            name          = sentiment,
            marker_color  = COLORS[sentiment],
            line_color    = COLORS[sentiment],
            boxmean       = True,
            hovertemplate = f"<b>{sentiment}</b><br>Rating: %{{y}}<extra></extra>",
        ))

    fig.update_layout(
        title  = dict(text=f"<b>{brand} – Star Rating by Sentiment</b>",
                      font=dict(size=15), x=0.5),
        yaxis  = dict(title="Star Rating", showgrid=True,
                      gridcolor=GRID_COLOR, range=[0.5, 5.5]),
        xaxis  = dict(showgrid=False),
        legend = _LEG,
        **_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 8. TIMELINE  –  fully robust version
# ─────────────────────────────────────────────────────────────────────────────
def sentiment_timeline(df: pd.DataFrame, brand: str, accent: str) -> go.Figure:
    # guard: column must exist
    if "date" not in df.columns:
        return go.Figure()

    tmp = df.copy()

    # ensure datetime
    tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
    tmp = tmp.dropna(subset=["date"])

    if tmp.empty:
        return go.Figure()

    # strip timezone so everything is tz-naive
    if hasattr(tmp["date"].dt, "tz") and tmp["date"].dt.tz is not None:
        tmp["date"] = tmp["date"].dt.tz_localize(None)

    # build clean year-month string  e.g. "2021-11"
    tmp["month_str"] = tmp["date"].dt.strftime("%Y-%m")

    # keep only rows where strftime produced a valid YYYY-MM pattern
    tmp = tmp[tmp["month_str"].str.match(r"^\d{4}-\d{2}$", na=False)]

    if tmp.empty:
        return go.Figure()

    # aggregate by month + sentiment
    monthly = (
        tmp.groupby(["month_str", "Sentiment"])
           .size()
           .reset_index(name="count")
    )
    totals  = tmp.groupby("month_str").size().reset_index(name="total")
    monthly = monthly.merge(totals, on="month_str")
    monthly["pct"]   = (monthly["count"] / monthly["total"] * 100).round(2)

    # convert back to datetime for proper axis
    monthly["month"] = pd.to_datetime(
        monthly["month_str"] + "-01", format="%Y-%m-%d"
    )
    monthly = monthly.sort_values("month").reset_index(drop=True)

    # need at least 2 distinct months to draw a line
    if monthly["month"].nunique() < 2:
        return go.Figure()

    # build traces
    fig = go.Figure()
    for sentiment in ["Positive", "Neutral", "Negative"]:
        sub = (
            monthly[monthly["Sentiment"] == sentiment]
            .sort_values("month")
            .reset_index(drop=True)
        )
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x             = sub["month"],
            y             = sub["pct"],
            name          = sentiment,
            mode          = "lines+markers",
            line          = dict(color=COLORS[sentiment], width=2.5),
            marker        = dict(size=7, color=COLORS[sentiment]),
            hovertemplate = "%{x|%b %Y}<br>%{y:.1f}%<extra>" + sentiment + "</extra>",
            stackgroup    = "one",
        ))

    # choose tick density based on date span
    span_months = (
        monthly["month"].max() - monthly["month"].min()
    ).days / 30.0

    if span_months <= 12:
        dtick = "M1"
    elif span_months <= 36:
        dtick = "M3"
    else:
        dtick = "M6"

    fig.update_layout(
        title  = dict(
            text = f"<b>{brand} – Sentiment Trend Over Time</b>",
            font = dict(size=15),
            x    = 0.5,
        ),
        xaxis  = dict(
            title         = "Month",
            showgrid      = False,
            tickformat    = "%b %Y",
            tickangle     = -30,
            dtick         = dtick,
            ticklabelmode = "period",
        ),
        yaxis  = dict(
            title      = "Share (%)",
            showgrid   = True,
            gridcolor  = GRID_COLOR,
            ticksuffix = "%",
            range      = [0, 102],
        ),
        legend = _LEG,
        **_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 9. TOP THUMBS-UP
# ─────────────────────────────────────────────────────────────────────────────
def top_thumbsup_bar(df: pd.DataFrame, brand: str, accent: str,
                     n: int = 10) -> go.Figure:
    if "thumbsUp" not in df.columns or df["thumbsUp"].isna().all():
        return go.Figure()

    top          = (
        df[["text", "thumbsUp", "Sentiment"]]
        .dropna(subset=["thumbsUp"])
        .nlargest(n, "thumbsUp")
    )
    top["short"] = top["text"].str[:55] + "…"
    bar_colors   = [COLORS[s] for s in top["Sentiment"]]

    fig = go.Figure(go.Bar(
        x             = top["thumbsUp"],
        y             = top["short"],
        orientation   = "h",
        marker_color  = bar_colors,
        text          = top["thumbsUp"].astype(int),
        textposition  = "outside",
        hovertext     = top["text"],
        hovertemplate = "%{hovertext}<br>👍 %{x:,}<extra></extra>",
    ))

    fig.update_layout(
        title  = dict(text=f"<b>{brand} – Top {n} Most-Liked Reviews</b>",
                      font=dict(size=15), x=0.5),
        xaxis  = dict(title="Thumbs Up", showgrid=True, gridcolor=GRID_COLOR),
        yaxis  = dict(autorange="reversed", showgrid=False,
                      tickfont=dict(size=11)),
        height = 420,
        **_BASE,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 10. RATING DISTRIBUTION
# ─────────────────────────────────────────────────────────────────────────────
def rating_distribution(gpay: pd.DataFrame, phonpe: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for df, name, color in [
        (gpay,   "Google Pay", GPAY_COLOR),
        (phonpe, "PhonePe",   PHONPE_COLOR),
    ]:
        if "rating" not in df.columns:
            continue
        cnt = df["rating"].value_counts().sort_index()
        fig.add_trace(go.Bar(
            x             = cnt.index,
            y             = cnt.values,
            name          = name,
            marker_color  = color,
            opacity       = 0.85,
            text          = cnt.values,
            textposition  = "outside",
            hovertemplate = "⭐ %{x}<br>Count: %{y:,}<extra>" + name + "</extra>",
        ))

    fig.update_layout(
        title   = dict(text="<b>Star Rating Distribution</b>",
                       font=dict(size=15), x=0.5),
        barmode = "group",
        xaxis   = dict(title="Stars ⭐", showgrid=False,
                       tickvals=[1, 2, 3, 4, 5]),
        yaxis   = dict(title="Count", showgrid=True, gridcolor=GRID_COLOR),
        legend  = _LEG,
        **_BASE,
    )
    return fig