import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

from utils.data_loader import load_master_monthly

dash.register_page(__name__, name="EDA")

master = load_master_monthly().copy()
warn_df = master.dropna(subset=["warn_layoffs"]).copy()
warn_df["year_num"] = warn_df["month"].dt.year
warn_df["year_label"] = warn_df["year_num"].astype(str)
warn_df.loc[warn_df["year_num"] == 2025, "year_label"] = "2025 YTD"

timeline_start = warn_df["month"].min().strftime("%Y-%m")
timeline_end = warn_df["month"].max().strftime("%Y-%m")
num_months = warn_df.shape[0]
total_warn_layoffs = warn_df["warn_layoffs"].sum()
avg_warn_layoffs = warn_df["warn_layoffs"].mean()

warn_trend_fig = px.line(
    warn_df,
    x="month",
    y="warn_layoffs",
    title="Monthly California WARN Layoffs",
)
warn_trend_fig.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="WARN layoffs",
    showlegend=False,
    margin=dict(l=40, r=20, t=60, b=40),
)

yearly_warn = warn_df.groupby("year_label", as_index=False)["warn_layoffs"].sum()
year_order = ["2020", "2021", "2022", "2023", "2024", "2025 YTD"]
yearly_warn["year_label"] = pd.Categorical(yearly_warn["year_label"], categories=year_order, ordered=True)
yearly_warn = yearly_warn.sort_values("year_label")

yearly_warn_fig = px.bar(
    yearly_warn,
    x="year_label",
    y="warn_layoffs",
    title="Total WARN Layoffs by Year",
    text="warn_layoffs",
)
yearly_warn_fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
yearly_warn_fig.update_layout(
    template="plotly_white",
    xaxis_title="Year",
    yaxis_title="Total layoffs",
    showlegend=False,
    margin=dict(l=40, r=20, t=60, b=40),
)

news_df = master.dropna(subset=["news_volume"]).copy()

news_volume_fig = px.line(
    news_df,
    x="month",
    y="news_volume",
    title="Monthly Layoff-Related News Volume",
)
news_volume_fig.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="News volume",
    showlegend=False,
    margin=dict(l=40, r=20, t=60, b=40),
)

graph_config = {
    "displayModeBar": False,
    "responsive": True,
}

layout = html.Div(
    [
        html.H1("EDA"),
        html.P(
            "This page summarizes the data sources, cleaning work, and early exploratory patterns used to build the Workforce Risk Radar project."
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.H3("Project timeline"),
                        html.P(f"{timeline_start} to {timeline_end}", className="finding-value"),
                    ],
                    className="finding-card",
                ),
                html.Div(
                    [
                        html.H3("Months in dataset"),
                        html.P(f"{num_months}", className="finding-value"),
                    ],
                    className="finding-card",
                ),
                html.Div(
                    [
                        html.H3("Total WARN layoffs"),
                        html.P(f"{total_warn_layoffs:,.0f}", className="finding-value"),
                    ],
                    className="finding-card",
                ),
                html.Div(
                    [
                        html.H3("Average monthly layoffs"),
                        html.P(f"{avg_warn_layoffs:,.0f}", className="finding-value"),
                    ],
                    className="finding-card",
                ),
            ],
            className="finding-grid",
        ),

        html.Section(
            [
                html.H2("Data sources"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("California WARN"),
                                html.P(
                                    "The main layoff target. WARN notices were cleaned from PDF source files and aggregated into monthly layoff totals."
                                ),
                            ],
                            className="source-card",
                        ),
                        html.Div(
                            [
                                html.H3("FRED Indicators"),
                                html.P(
                                    "Macroeconomic context, including unemployment, federal funds rate, and Indeed job postings indicators."
                                ),
                            ],
                            className="source-card",
                        ),
                        html.Div(
                            [
                                html.H3("GDELT News Features"),
                                html.P(
                                    "Layoff-related news activity measured through monthly news volume and tone."
                                ),
                            ],
                            className="source-card",
                        ),
                    ],
                    className="source-grid",
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.H2("What we cleaned"),
                html.P(
                    "The WARN data required the most cleaning because the original source came from PDFs rather than a ready-to-use dataset."
                ),
                html.Ul(
                    [
                        html.Li("Extracted WARN tables from PDF source files"),
                        html.Li("Validated rows and removed parsing errors"),
                        html.Li("Built monthly California layoff totals"),
                        html.Li("Merged WARN with macroeconomic and news-based features"),
                    ]
                ),
                html.P(
                    "Final modeling uses monthly statewide observations built from cleaned WARN notices, macroeconomic indicators, and layoff-related news features."
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.H2("Monthly WARN layoffs over time"),
                html.P("This chart shows the cleaned monthly California WARN layoffs used as the main project target."),
                dcc.Graph(figure=warn_trend_fig, config=graph_config),
                html.P(
                    "Takeaway: layoffs were much higher at the start of the timeline, then settled into a lower but still variable monthly pattern.",
                    className="section-note",
                ),
            ],
            className="chart-section",
        ),

        html.Section(
            [
                html.H2("Total WARN layoffs by year"),
                html.P("This yearly summary helps show how the overall scale of layoffs changes across the project window."),
                dcc.Graph(figure=yearly_warn_fig, config=graph_config),
                html.P(
                    "Takeaway: 2020 and 2023–2024 had the largest totals. The 2025 value is shown as year-to-date, so it should not be compared as a full year.",
                    className="section-note",
                ),
            ],
            className="chart-section",
        ),

        html.Section(
            [
                html.H2("Monthly news volume trend"),
                html.P(
                    "This chart shows how layoff-related news activity changes over time. It gives context for later comparisons between layoffs and news signals."
                ),
                dcc.Graph(figure=news_volume_fig, config=graph_config),
                html.P(
                    "Takeaway: news volume was highest early in the timeline and spiked again around major layoff periods, which supports using it as a contextual signal.",
                    className="section-note",
                ),
            ],
            className="chart-section",
        ),
    ],
    className="text-page",
)