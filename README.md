# 📊 UPI Sentiment Dashboard — Google Pay vs PhonePe

## Folder Structure
```
sentiment_dashboard/
├── app.py
├── analyzer.py
├── data_loader.py
├── charts.py
├── requirements.txt
├── README.md
└── sample_data/
    ├── GooglePayIndia.csv
    └── PhonePayIndia.csv
```

## Setup & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## CSV Column Format
```
,reviewId,userName,userImage,content,score,thumbsUpCount,
reviewCreatedVersion,at,replyContent,repliedAt
```

Key columns used:
| CSV column | Used as |
|---|---|
| `content` | Review text for sentiment |
| `score` | Star rating (1–5) |
| `thumbsUpCount` | Helpful votes |
| `at` | Review date |
| `userName` | Reviewer name |

## Features

| Tab | Charts |
|---|---|
| 🏠 Overview | KPI cards, Donuts, Gauges, Rating distribution, Insights |
| 💙 Google Pay | Donut, Gauge, Rating-vs-Sentiment Box, Top Thumbs-up, Timeline, Reviews |
| 💜 PhonePe | Same as above |
| ⚖️ Compare | Grouped bar, Stacked %, Radar, Histogram, Winner card |
| 📋 Data Explorer | Searchable/filterable table, Download CSV |
