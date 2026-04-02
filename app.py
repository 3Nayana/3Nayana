# app.py
from __future__ import annotations
import pandas as pd
import streamlit as st
from data_loader import load_all
import charts as ch

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title            = "UPI Sentiment Dashboard",
    page_icon             = "📊",
    layout                = "wide",
    initial_sidebar_state = "collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family:'Inter',sans-serif; color:#e2e8f0; }
.main .block-container {
    background:#080b14;
    padding:2rem 2.5rem 5rem;
    max-width:1600px;
}
section[data-testid="stAppViewContainer"] {
    background:#080b14 !important;
}
section[data-testid="stAppViewContainer"] > div {
    background:#080b14 !important;
}

/* hero */
.hero {
    background:linear-gradient(135deg,#0d1b2a,#1a0a2e,#0a1628);
    border-radius:22px;
    padding:2.5rem 3rem 2rem;
    border:1px solid rgba(255,255,255,0.05);
    box-shadow:0 20px 60px rgba(0,0,0,0.5);
    margin-bottom:2rem;
}
.hero-title {
    font-size:2.6rem; font-weight:900; margin:0 0 .45rem;
    background:linear-gradient(90deg,#00d4ff,#aa00ff,#ff4081);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    line-height:1.15;
}
.hero-sub  { color:#8892a4; font-size:1rem; margin:0; }
.hero-badges { display:flex; gap:.55rem; margin-top:1rem; flex-wrap:wrap; }
.badge {
    font-size:.70rem; font-weight:700; padding:.25rem .75rem;
    border-radius:999px; letter-spacing:.6px; text-transform:uppercase;
}
.badge-blue {
    background:rgba(0,212,255,0.10); color:#00d4ff;
    border:1px solid rgba(0,212,255,0.25);
}
.badge-purple {
    background:rgba(170,0,255,0.10); color:#aa00ff;
    border:1px solid rgba(170,0,255,0.25);
}
.badge-green {
    background:rgba(0,230,118,0.10); color:#00e676;
    border:1px solid rgba(0,230,118,0.25);
}
.badge-red {
    background:rgba(255,82,82,0.10); color:#ff5252;
    border:1px solid rgba(255,82,82,0.25);
}

/* st.metric */
div[data-testid="metric-container"] {
    background:linear-gradient(145deg,#111827,#0d1520);
    border-radius:14px; padding:1.1rem .9rem;
    border:1px solid rgba(255,255,255,0.06);
    box-shadow:0 4px 20px rgba(0,0,0,0.3);
}
div[data-testid="metric-container"] > label,
div[data-testid="metric-container"] label p {
    font-size:.68rem !important; font-weight:700 !important;
    text-transform:uppercase; letter-spacing:.9px;
    color:#a0aec0 !important;
}
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] > div,
div[data-testid="stMetricValue"] p {
    font-size:1.75rem !important; font-weight:800 !important;
    color:#ffffff !important;
}
div[data-testid="stMetricDelta"] svg { display:none; }
div[data-testid="stMetricDelta"] > div {
    font-size:.72rem !important; color:#4a5568 !important;
}

/* section heading */
.sh {
    font-size:1.05rem; font-weight:700; color:#cbd5e0;
    margin:1.8rem 0 .9rem; display:flex; align-items:center; gap:.5rem;
}
.sh::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(90deg,rgba(170,0,255,0.20),transparent);
}

/* insight card */
.ic {
    background:linear-gradient(145deg,#111827,#0d1520);
    border-radius:12px; padding:1rem 1.2rem;
    border:1px solid rgba(255,255,255,0.05);
    margin-bottom:.65rem;
}
.ic-t {
    font-size:.72rem; font-weight:700; color:#718096;
    text-transform:uppercase; letter-spacing:.7px;
}
.ic-b { font-size:.90rem; color:#e2e8f0; margin-top:.25rem; }

/* winner */
.winner {
    border-radius:18px; padding:1.8rem 2rem;
    text-align:center; margin-top:1.5rem;
}
.w-emoji { font-size:3rem; }
.w-name  { font-size:1.8rem; font-weight:900; margin:.3rem 0 .15rem; }
.w-sub   { color:#8892a4; font-size:.85rem; }
.w-stats {
    display:flex; justify-content:center;
    gap:2.5rem; margin-top:1.2rem; flex-wrap:wrap;
}
.ws-v { font-size:1.2rem; font-weight:800; }
.ws-l { font-size:.72rem; color:#718096; margin-top:.12rem; }

/* review chip */
.chip {
    background:#111827; border-radius:9px;
    padding:.7rem .95rem; margin-bottom:.5rem;
    font-size:.84rem; color:#cbd5e0; line-height:1.5;
}
.chip-m { font-size:.70rem; color:#4a5568; margin-top:.25rem; }

/* tabs */
.stTabs [data-baseweb="tab-list"] {
    background:#111827; border-radius:12px;
    padding:4px; gap:3px;
    border:1px solid rgba(255,255,255,0.05);
}
.stTabs [data-baseweb="tab"] {
    color:#718096; font-weight:600;
    border-radius:9px; padding:.42rem 1.1rem; font-size:.86rem;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#7b2ff7,#00d4ff) !important;
    color:#fff !important;
}
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-thumb { background:#7b2ff7; border-radius:3px; }
[data-testid="stSidebar"] {
    background:#080b14;
    border-right:1px solid rgba(255,255,255,0.05);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def pct(df: pd.DataFrame, sentiment: str) -> float:
    if df.empty:
        return 0.0
    return (df["Sentiment"] == sentiment).sum() / len(df) * 100


def sh(title: str) -> None:
    st.markdown(f'<div class="sh">{title}</div>', unsafe_allow_html=True)


def insight(title: str, body: str, color: str = "#aa00ff") -> None:
    st.markdown(
        f'<div class="ic" style="border-left:3px solid {color}">'
        f'<div class="ic-t">{title}</div>'
        f'<div class="ic-b">{body}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def chips(df: pd.DataFrame, sentiment: str, color: str, n: int = 7) -> None:
    sub = df[df["Sentiment"] == sentiment].head(n)
    if sub.empty:
        st.caption("No reviews here.")
        return
    for _, row in sub.iterrows():
        r = (f"⭐{int(row['rating'])}  ·  "
             if "rating"   in row and pd.notna(row.get("rating"))   else "")
        t = (f"👍{int(row['thumbsUp'])}  ·  "
             if "thumbsUp" in row and pd.notna(row.get("thumbsUp")) else "")
        d = (row["date"].strftime("%d %b %Y")
             if "date"     in row and pd.notna(row.get("date"))     else "")
        st.markdown(
            f'<div class="chip" style="border-left:3px solid {color}">'
            f'{row["text"]}'
            f'<div class="chip-m">{r}{t}{d}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("⚡ Analysing reviews…"):
    gpay_df, phonpe_df = load_all()

if gpay_df.empty and phonpe_df.empty:
    st.error("❌ No data found. Check the sample_data/ folder.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    sent_f = st.multiselect(
        "Sentiment",
        ["Positive", "Neutral", "Negative"],
        default=["Positive", "Neutral", "Negative"],
    )

    rat_f: list[int] = []
    if "rating" in gpay_df.columns or "rating" in phonpe_df.columns:
        rat_f = st.multiselect(
            "Star Rating ⭐", [1, 2, 3, 4, 5],
            default=[1, 2, 3, 4, 5],
        )

    lo, hi = st.slider(
        "VADER Score Range",
        min_value=-1.0, max_value=1.0,
        value=(-1.0, 1.0), step=0.05,
    )

    st.markdown("---")
    st.caption(
        "Auto-loaded from\n\n"
        "`sample_data/GooglePayIndia.csv`\n\n"
        "`sample_data/PhonePayIndia.csv`"
    )


def filt(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    m = df["Sentiment"].isin(sent_f) & df["Score"].between(lo, hi)
    if rat_f and "rating" in df.columns:
        m &= df["rating"].isin(rat_f)
    return df[m].reset_index(drop=True)


gpay   = filt(gpay_df)
phonpe = filt(phonpe_df)


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
total = len(gpay) + len(phonpe)
st.markdown(f"""
<div class="hero">
    <div class="hero-title">📊 UPI Sentiment Dashboard</div>
    <p class="hero-sub">VADER-powered analysis of <b>{total:,} reviews</b>
       — Google Pay vs PhonePe — Kaggle data</p>
    <div class="hero-badges">
        <span class="badge badge-blue">Google Pay</span>
        <span class="badge badge-purple">PhonePe</span>
        <span class="badge badge-green">{len(gpay):,} GPay reviews</span>
        <span class="badge badge-red">{len(phonpe):,} PPe reviews</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
T1, T2, T3, T4, T5 = st.tabs([
    "🏠 Overview",
    "💙 Google Pay",
    "💜 PhonePe",
    "⚖️ Compare",
    "📋 Data Explorer",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with T1:
    g_pos = pct(gpay,   "Positive")
    g_neg = pct(gpay,   "Negative")
    p_pos = pct(phonpe, "Positive")
    p_neg = pct(phonpe, "Negative")
    g_avg = float(gpay["Score"].mean())   if not gpay.empty   else 0.0
    p_avg = float(phonpe["Score"].mean()) if not phonpe.empty else 0.0

    sh("📈 Key Performance Indicators")
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("📦 GPay Reviews",   f"{len(gpay):,}")
    k2.metric("📦 PPe Reviews",    f"{len(phonpe):,}")
    k3.metric("😊 GPay Positive",  f"{g_pos:.1f}%")
    k4.metric("😊 PPe Positive",   f"{p_pos:.1f}%")
    k5.metric("🎯 GPay Avg Score", f"{g_avg:+.3f}")
    k6.metric("🎯 PPe Avg Score",  f"{p_avg:+.3f}")

    st.divider()

    sh("🥧 Sentiment Breakdown")
    d1, d2 = st.columns(2)
    with d1:
        if not gpay.empty:
            st.plotly_chart(
                ch.donut_chart(gpay, "Google Pay", ch.GPAY_COLOR),
                use_container_width=True,
                key="overview_donut_gpay",
            )
    with d2:
        if not phonpe.empty:
            st.plotly_chart(
                ch.donut_chart(phonpe, "PhonePe", ch.PHONPE_COLOR),
                use_container_width=True,
                key="overview_donut_phonpe",
            )

    sh("🎯 Average VADER Score")
    g1, g2 = st.columns(2)
    with g1:
        if not gpay.empty:
            st.plotly_chart(
                ch.gauge_chart(g_avg, "Google Pay", ch.GPAY_COLOR),
                use_container_width=True,
                key="overview_gauge_gpay",
            )
    with g2:
        if not phonpe.empty:
            st.plotly_chart(
                ch.gauge_chart(p_avg, "PhonePe", ch.PHONPE_COLOR),
                use_container_width=True,
                key="overview_gauge_phonpe",
            )

    if "rating" in gpay.columns or "rating" in phonpe.columns:
        sh("⭐ Star Rating Distribution")
        st.plotly_chart(
            ch.rating_distribution(gpay, phonpe),
            use_container_width=True,
            key="overview_rating_dist",
        )

    sh("💡 Quick Insights")
    lp  = "Google Pay" if g_pos >= p_pos else "PhonePe"
    lpc = ch.GPAY_COLOR if g_pos >= p_pos else ch.PHONPE_COLOR
    ls  = "Google Pay" if g_avg >= p_avg else "PhonePe"
    lsc = ch.GPAY_COLOR if ls == "Google Pay" else ch.PHONPE_COLOR

    insight("🏆 Positivity Leader",
            f"<b>{lp}</b> leads in positive sentiment "
            f"({max(g_pos,p_pos):.1f}% vs {min(g_pos,p_pos):.1f}%)", lpc)
    insight("📊 Average VADER Score",
            f"<b>{ls}</b> has the higher average score "
            f"(GPay <b>{g_avg:+.3f}</b> · PPe <b>{p_avg:+.3f}</b>)", lsc)
    insight("⚠️ Negativity",
            f"Google Pay: <b>{g_neg:.1f}%</b> negative  ·  "
            f"PhonePe: <b>{p_neg:.1f}%</b> negative",
            ch.COLORS["Negative"])



# 2 — GOOGLE PAY

with T2:
    sh("💙 Google Pay – Deep Dive")

    if gpay.empty:
        st.warning("No Google Pay data with current filters.")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(
                ch.donut_chart(gpay, "Google Pay", ch.GPAY_COLOR),
                use_container_width=True,
                key="gpay_donut",
            )
        with col_b:
            st.plotly_chart(
                ch.gauge_chart(float(gpay["Score"].mean()),
                               "Google Pay", ch.GPAY_COLOR),
                use_container_width=True,
                key="gpay_gauge",
            )

        col_c, col_d = st.columns(2)
        with col_c:
            fig_rb = ch.rating_vs_sentiment(gpay, "Google Pay", ch.GPAY_COLOR)
            if fig_rb.data:
                st.plotly_chart(fig_rb, use_container_width=True, key="gpay_rating_box")
            else:
                st.info("Star-rating data not available for Google Pay.")
        with col_d:
            fig_tb = ch.top_thumbsup_bar(gpay, "Google Pay", ch.GPAY_COLOR)
            if fig_tb.data:
                st.plotly_chart(fig_tb, use_container_width=True, key="gpay_thumbsup")
            else:
                st.info("Thumbs-up data not available for Google Pay.")

        sh("💬 Sample Reviews")
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("### 🟢 Positive")
            chips(gpay, "Positive", ch.COLORS["Positive"])
        with r2:
            st.markdown("### 🔵 Neutral")
            chips(gpay, "Neutral",  ch.COLORS["Neutral"])
        with r3:
            st.markdown("### 🔴 Negative")
            chips(gpay, "Negative", ch.COLORS["Negative"])



# 3 — PHONEPE

with T3:
    sh("💜 PhonePe – Deep Dive")

    if phonpe.empty:
        st.warning("No PhonePe data with current filters.")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(
                ch.donut_chart(phonpe, "PhonePe", ch.PHONPE_COLOR),
                use_container_width=True,
                key="phonpe_donut",
            )
        with col_b:
            st.plotly_chart(
                ch.gauge_chart(float(phonpe["Score"].mean()),
                               "PhonePe", ch.PHONPE_COLOR),
                use_container_width=True,
                key="phonpe_gauge",
            )

        col_c, col_d = st.columns(2)
        with col_c:
            fig_rb = ch.rating_vs_sentiment(phonpe, "PhonePe", ch.PHONPE_COLOR)
            if fig_rb.data:
                st.plotly_chart(fig_rb, use_container_width=True, key="phonpe_rating_box")
            else:
                st.info("Star-rating data not available for PhonePe.")
        with col_d:
            fig_tb = ch.top_thumbsup_bar(phonpe, "PhonePe", ch.PHONPE_COLOR)
            if fig_tb.data:
                st.plotly_chart(fig_tb, use_container_width=True, key="phonpe_thumbsup")
            else:
                st.info("Thumbs-up data not available for PhonePe.")

        sh("💬 Sample Reviews")
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("### 🟢 Positive")
            chips(phonpe, "Positive", ch.COLORS["Positive"])
        with r2:
            st.markdown("### 🔵 Neutral")
            chips(phonpe, "Neutral",  ch.COLORS["Neutral"])
        with r3:
            st.markdown("### 🔴 Negative")
            chips(phonpe, "Negative", ch.COLORS["Negative"])



# 4 — COMPARE

with T4:
    sh("⚖️ Head-to-Head Comparison")

    if gpay.empty or phonpe.empty:
        st.warning("Need data for both brands. Adjust sidebar filters.")
    else:
        st.plotly_chart(ch.grouped_bar(gpay, phonpe),
                        use_container_width=True, key="compare_grouped_bar")
        st.plotly_chart(ch.stacked_pct_bar(gpay, phonpe),
                        use_container_width=True, key="compare_stacked_bar")

        col_l, col_r = st.columns(2)
        with col_l:
            st.plotly_chart(ch.radar_chart(gpay, phonpe),
                            use_container_width=True, key="compare_radar")
        with col_r:
            st.plotly_chart(ch.score_histogram(gpay, phonpe),
                            use_container_width=True, key="compare_histogram")

        gp   = pct(gpay,   "Positive")
        pp   = pct(phonpe, "Positive")
        ga   = float(gpay["Score"].mean())
        pa   = float(phonpe["Score"].mean())
        wins = int(gp > pp) + int(ga > pa)

        if wins == 2:
            wname, wemoji = "Google Pay", "💙"
            wbg  = "rgba(0,212,255,0.10)"
            wbdr = "rgba(0,212,255,0.25)"
            wnc  = ch.GPAY_COLOR
        elif wins == 0:
            wname, wemoji = "PhonePe", "💜"
            wbg  = "rgba(170,0,255,0.10)"
            wbdr = "rgba(170,0,255,0.25)"
            wnc  = ch.PHONPE_COLOR
        else:
            wname, wemoji = "It's a Tie!", "🤝"
            wbg  = "rgba(246,173,85,0.10)"
            wbdr = "rgba(246,173,85,0.25)"
            wnc  = "#f6ad55"

        st.markdown(
            f'<div class="winner" '
            f'style="background:{wbg};border:1px solid {wbdr}">'
            f'  <div class="w-emoji">{wemoji}</div>'
            f'  <div class="w-name" style="color:{wnc}">{wname}</div>'
            f'  <div class="w-sub">Based on positive-% and average VADER score</div>'
            f'  <div class="w-stats">'
            f'    <div><div class="ws-v" style="color:{ch.GPAY_COLOR}">{gp:.1f}%</div>'
            f'         <div class="ws-l">GPay Positive</div></div>'
            f'    <div><div class="ws-v" style="color:{ch.PHONPE_COLOR}">{pp:.1f}%</div>'
            f'         <div class="ws-l">PPe Positive</div></div>'
            f'    <div><div class="ws-v" style="color:{ch.GPAY_COLOR}">{ga:+.3f}</div>'
            f'         <div class="ws-l">GPay Avg Score</div></div>'
            f'    <div><div class="ws-v" style="color:{ch.PHONPE_COLOR}">{pa:+.3f}</div>'
            f'         <div class="ws-l">PPe Avg Score</div></div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DATA EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with T5:
    sh("📋 Raw Data Explorer")

    brand  = st.radio("Brand", ["Google Pay", "PhonePe"], horizontal=True)
    edf    = gpay.copy() if brand == "Google Pay" else phonpe.copy()

    col_s, col_f = st.columns([3, 1])
    with col_s:
        kw = st.text_input(
            "Search reviews",
            placeholder="Type keyword…",
            label_visibility="collapsed",
        )
    with col_f:
        sf_v = st.selectbox(
            "Filter sentiment",
            ["All", "Positive", "Neutral", "Negative"],
            label_visibility="collapsed",
        )

    if kw:
        edf = edf[edf["text"].str.contains(kw, case=False, na=False)]
    if sf_v != "All":
        edf = edf[edf["Sentiment"] == sf_v]

    base = len(gpay if brand == "Google Pay" else phonpe)
    st.caption(f"Showing **{len(edf):,}** of **{base:,}** rows")

    show = [c for c in
            ["text", "Sentiment", "Score", "rating",
             "thumbsUp", "date", "userName"]
            if c in edf.columns]

    def _hl(v: str) -> str:
        return {
            "Positive": "background-color:rgba(0,230,118,0.10)",
            "Negative": "background-color:rgba(255,82,82,0.10)",
            "Neutral":  "background-color:rgba(64,196,255,0.08)",
        }.get(v, "")

    fmt: dict = {"Score": "{:+.3f}"}
    if "rating"   in edf.columns:
        fmt["rating"]   = lambda v: f"⭐{int(v)}" if pd.notna(v) else "—"
    if "thumbsUp" in edf.columns:
        fmt["thumbsUp"] = lambda v: f"👍{int(v)}" if pd.notna(v) else "—"
    if "date"     in edf.columns:
        fmt["date"]     = lambda v: v.strftime("%d %b %Y") if pd.notna(v) else "—"

    st.dataframe(
        edf[show].style
                 .applymap(_hl, subset=["Sentiment"])
                 .format(fmt, na_rep="—"),
        use_container_width=True,
        height=480,
    )

    st.download_button(
        label     = f"⬇️ Download {brand} CSV",
        data      = edf.to_csv(index=False).encode(),
        file_name = f"{brand.replace(' ', '_')}_sentiment.csv",
        mime      = "text/csv",
    )
