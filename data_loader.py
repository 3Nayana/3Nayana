# data_loader.py
from __future__ import annotations

import os
import traceback
import pandas as pd
import streamlit as st
from analyzer import get_sentiment_label, get_sentiment_score

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")
GPAY_CSV_PATH   = os.path.join(SAMPLE_DATA_DIR, "GooglePayIndia.csv")
PHONPE_CSV_PATH = os.path.join(SAMPLE_DATA_DIR, "PhonePayIndia.csv")


@st.cache_data(show_spinner=False)
def load_brand_csv(filepath: str, brand_label: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        st.error(f"❌ File not found: `{filepath}`")
        return pd.DataFrame()

    try:
        df = pd.read_csv(filepath)

        # ── normalise column names ────────────────────────────────────────────
        df.columns = [c.strip().lower() for c in df.columns]

        if "content" not in df.columns:
            st.error(
                f"❌ 'content' column not found in `{filepath}`. "
                f"Found: {list(df.columns)}"
            )
            return pd.DataFrame()

        # ── rename columns ────────────────────────────────────────────────────
        col_map = {
            "content":              "text",
            "score":                "rating",
            "thumbsupcount":        "thumbsUp",
            "reviewcreatedversion": "version",
            "at":                   "date",
            "username":             "userName",
            "reviewid":             "reviewId",
        }
        df.rename(columns=col_map, inplace=True)

        keep = [c for c in
                ["text", "rating", "thumbsUp", "version",
                 "date", "userName", "reviewId"]
                if c in df.columns]
        df = df[keep].copy()

        # ── clean text ────────────────────────────────────────────────────────
        df["text"] = df["text"].astype(str).str.strip()
        df = df[df["text"].str.len() > 3].reset_index(drop=True)

        # ── sentiment ─────────────────────────────────────────────────────────
        df["Sentiment"] = df["text"].apply(get_sentiment_label)
        df["Score"]     = df["text"].apply(get_sentiment_score)
        df["brand"]     = brand_label

        # ── date parsing ──────────────────────────────────────────────────────
        if "date" in df.columns:
            # Step 1: convert everything to string and strip whitespace
            df["date"] = df["date"].astype(str).str.strip()

            # Step 2: remove timezone suffixes
            df["date"] = (
                df["date"]
                .str.replace(r"\s*(UTC|Z)$",     "", regex=True)
                .str.replace(r"\+\d{2}:\d{2}$",  "", regex=True)
                .str.replace(r"-\d{2}:\d{2}$",   "", regex=True)
                .str.strip()
            )

            # Step 3: try known formats one by one
            formats_to_try = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%d/%m/%Y %H:%M:%S",
                "%m/%d/%Y %H:%M:%S",
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%d-%m-%Y",
                "%m-%d-%Y",
            ]

            parsed = None
            for fmt in formats_to_try:
                try:
                    attempt = pd.to_datetime(
                        df["date"], format=fmt, errors="coerce"
                    )
                    ratio = attempt.notna().sum() / max(len(attempt), 1)
                    if ratio > 0.80:
                        parsed = attempt
                        break
                except Exception:
                    continue

            # Step 4: fallback — let pandas infer
            if parsed is None:
                parsed = pd.to_datetime(
                    df["date"],
                    infer_datetime_format=True,
                    errors="coerce",
                )

            df["date"] = parsed

            # Step 5: strip timezone info so everything is tz-naive
            if (
                hasattr(df["date"], "dt")
                and hasattr(df["date"].dt, "tz")
                and df["date"].dt.tz is not None
            ):
                df["date"] = df["date"].dt.tz_localize(None)

            # Step 6: if almost nothing parsed, drop the column
            valid_ratio = df["date"].notna().sum() / max(len(df), 1)
            if valid_ratio < 0.05:
                df.drop(columns=["date"], inplace=True)

        # ── rating to numeric ─────────────────────────────────────────────────
        if "rating" in df.columns:
            df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

        # ── thumbsUp to numeric ───────────────────────────────────────────────
        if "thumbsUp" in df.columns:
            df["thumbsUp"] = pd.to_numeric(df["thumbsUp"], errors="coerce")

        return df.reset_index(drop=True)

    except Exception:
        st.error(
            f"❌ Failed to load `{filepath}`\n"
            f"```\n{traceback.format_exc()}\n```"
        )
        return pd.DataFrame()


def load_all() -> tuple[pd.DataFrame, pd.DataFrame]:
    gpay_df   = load_brand_csv(GPAY_CSV_PATH,   "Google Pay")
    phonpe_df = load_brand_csv(PHONPE_CSV_PATH, "PhonePe")
    return gpay_df, phonpe_df