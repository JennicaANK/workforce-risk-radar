import dash
from dash import html, dcc
import plotly.express as px

from utils.data_loader import load_final_predictions, load_final_risk_scores

dash.register_page(__name__, path="/", name="Home")

pred_df = load_final_predictions().copy()
risk_df = load_final_risk_scores().copy()

pred_df = pred_df.sort_values("month").reset_index(drop=True)
risk_df = risk_df.sort_values("month").reset_index(drop=True)

latest_row = risk_df.iloc[-1]
latest_month = latest_row["month"].strftime("%B %Y")

predicted_layoffs = float(latest_row["pred_warn_layoffs"])
actual_layoffs = float(latest_row["warn_layoffs"])
predicted_risk = str(latest_row["predicted_risk_level"])

difference = predicted_layoffs - actual_layoffs

if difference > 0:
    gap_direction = "Overprediction"
    gap_class = "gap-positive"
    gap_display = f"{difference:+,.0f}"
elif difference < 0:
    gap_direction = "Underprediction"
    gap_class = "gap-negative"
    gap_display = f"{difference:+,.0f}"
else:
    gap_direction = "No forecast error"
    gap_class = "gap-neutral"
    gap_display = "0"

risk_class = f"risk-pill risk-{predicted_risk.lower()}"

chart_df = pred_df[["month", "warn_layoffs", "pred_warn_layoffs"]].copy()
chart_df = chart_df.rename(
    columns={
        "warn_layoffs": "Actual WARN layoffs",
        "pred_warn_layoffs": "Predicted WARN layoffs",
    }
)

chart_long = chart_df.melt(
    id_vars="month",
    value_vars=["Actual WARN layoffs", "Predicted WARN layoffs"],
    var_name="Series",
    value_name="Layoffs",
)

fig = px.line(
    chart_long,
    x="month",
    y="Layoffs",
    color="Series",
    title="Actual vs Predicted WARN Layoffs",
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="WARN layoffs",
    legend_title_text="Series",
    margin=dict(l=40, r=20, t=60, b=40),
)

graph_config = {
    "displayModeBar": False,
    "responsive": True,
}

layout = html.Div(
    [
        html.Section(
            [
                html.P("California layoff early-warning dashboard", className="hero-kicker"),
                html.H1("Workforce Risk Radar", className="hero-title"),
                html.P(
                    "Tracks California WARN layoff trends using macroeconomic signals and "
                    "layoff-related news features."
                ),
                html.Div(
                    [
                        html.Span("Final model: Linear Regression (Macro only)", className="meta-chip"),
                        html.Span("Risk labels come from predicted layoffs", className="meta-chip"),
                        html.Span("Monthly statewide dashboard", className="meta-chip"),
                    ],
                    className="meta-chip-row",
                ),
            ],
            className="hero-section",
        ),

        html.Section(
            [
                html.H2("Project Objective"),
                html.P(
                    "This project builds a workforce risk radar for California by combining WARN layoff "
                    "records, macroeconomic indicators, and layoff-related news signals into a monthly "
                    "early-warning dashboard."
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Main goals"),
                                html.Ul(
                                    [
                                        html.Li("Predict monthly layoffs using macroeconomic and news signals."),
                                        html.Li("Identify early warning indicators that move before layoff spikes."),
                                        html.Li("Translate model predictions into clear risk levels."),
                                    ]
                                ),
                            ],
                            className="method-card",
                        ),
                        html.Div(
                            [
                                html.H3("Data sources"),
                                html.Ul(
                                    [
                                        html.Li("California WARN notices"),
                                        html.Li("FRED macroeconomic indicators"),
                                        html.Li("GDELT news volume and tone data"),
                                    ]
                                ),
                            ],
                            className="method-card",
                        ),
                    ],
                    className="method-grid",
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.Div(
                    [
                        html.H3("Latest month"),
                        html.P(latest_month, className="card-value"),
                    ],
                    className="summary-card home-summary-card",
                ),
                html.Div(
                    [
                        html.H3("Current risk level"),
                        html.Div(
                            html.Span(predicted_risk, className=risk_class),
                            className="risk-pill-wrapper",
                        ),
                    ],
                    className="summary-card home-summary-card",
                ),
                html.Div(
                    [
                        html.H3("Predicted layoffs"),
                        html.P(f"{predicted_layoffs:,.0f}", className="card-value"),
                    ],
                    className="summary-card home-summary-card",
                ),
                html.Div(
                    [
                        html.H3("Actual layoffs"),
                        html.P(f"{actual_layoffs:,.0f}", className="card-value"),
                    ],
                    className="summary-card home-summary-card",
                ),
            ],
            className="home-card-grid",
        ),

        html.Section(
            [
                html.Div(
                    [
                        html.H3("Latest forecast error"),
                        html.P(gap_direction, className=f"gap-label {gap_class}"),
                        html.P(gap_display, className="card-value"),
                        html.P(
                            "Predicted layoffs minus actual layoffs for the latest month.",
                            className="small-note",
                        ),
                    ],
                    className="summary-card home-highlight-card",
                ),
            ],
            className="single-card-row",
        ),

        html.Section(
            [
                dcc.Graph(figure=fig, config=graph_config),
                html.P(
                    "The chart begins after enough lagged feature history becomes available for the final deployed model.",
                    className="section-note",
                ),
            ],
            className="chart-section home-chart-section",
        ),

        html.Section(
            [
                html.H2("How to read this dashboard"),
                html.Ul(
                    [
                        html.Li("The blue line shows actual California WARN layoffs."),
                        html.Li("The orange line shows layoffs predicted by the final deployed model."),
                        html.Li("The risk level is based on predicted layoffs, not the weaker classification models."),
                        html.Li("This dashboard is designed to track broad monthly risk patterns rather than exact event-level spikes."),
                    ]
                ),
            ],
            className="text-section",
        ),
    ]
)
