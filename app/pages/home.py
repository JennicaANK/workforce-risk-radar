import dash
from dash import html, dcc
import plotly.express as px

from utils.data_loader import load_final_predictions, load_final_risk_scores

dash.register_page(__name__, path="/", name="Home")

pred_df = load_final_predictions()
risk_df = load_final_risk_scores()

latest_row = risk_df.sort_values("month").iloc[-1]

fig = px.line(
    pred_df,
    x="month",
    y=["warn_layoffs", "pred_warn_layoffs"],
    title="Actual vs Predicted WARN Layoffs"
)

fig.update_layout(
    legend_title_text="Series",
    xaxis_title="Month",
    yaxis_title="WARN layoffs",
    template="plotly_white"
)

layout = html.Div(
    [
        html.Section(
            [
                html.H1("Workforce Risk Radar"),
                html.P(
                    "An early warning dashboard for California layoff trends using WARN data, "
                    "macroeconomic signals, and layoff-related news features."
                )
            ],
            className="hero-section"
        ),

        html.Section(
            [
                html.Div(
                    [
                        html.H3("Latest Predicted Risk"),
                        html.P(str(latest_row["predicted_risk_level"]), className="card-value")
                    ],
                    className="summary-card"
                ),
                html.Div(
                    [
                        html.H3("Latest Predicted Layoffs"),
                        html.P(f'{latest_row["pred_warn_layoffs"]:.0f}', className="card-value")
                    ],
                    className="summary-card"
                ),
                html.Div(
                    [
                        html.H3("Latest Actual Layoffs"),
                        html.P(f'{latest_row["warn_layoffs"]:.0f}', className="card-value")
                    ],
                    className="summary-card"
                ),
            ],
            className="card-grid"
        ),

        html.Section(
            [
                dcc.Graph(figure=fig)
            ],
            className="chart-section"
        ),

        html.Section(
            [
                html.H2("How to read this dashboard"),
                html.P(
                    "The site shows historical California WARN layoffs, the final deployed model's "
                    "predicted layoffs, and a simple Low / Medium / High risk level derived from those predictions."
                )
            ],
            className="text-section"
        )
    ]
)