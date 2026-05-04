import dash
from dash import html, dcc, dash_table, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import (
    load_regression_metrics,
    load_classification_metrics,
    load_final_model_coefficients,
    load_final_predictions,
)

dash.register_page(__name__, name="Major Findings")

regression_metrics = load_regression_metrics().copy()
classification_metrics = load_classification_metrics().copy()
coefficients = load_final_model_coefficients().copy()
website_predictions = load_final_predictions().copy()

for df in [regression_metrics, classification_metrics]:
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].round(3)

coefficients["coefficient"] = coefficients["coefficient"].round(3)

lag_heatmap_df = pd.DataFrame(
    {
        "lag_0": [-0.011, 0.59, -0.38, -0.44, 0.76],
        "lag_1": [-0.31, 0.61, -0.29, -0.46, 0.50],
        "lag_2": [-0.41, 0.59, -0.23, -0.39, 0.47],
        "lag_3": [-0.44, 0.55, -0.15, -0.32, 0.39],
    },
    index=[
        "ca_unemployment_rate",
        "fed_funds_rate",
        "indeed_job_postings_index",
        "news_tone",
        "news_volume",
    ],
)

risk_summary = pd.DataFrame(
    {
        "risk_level": ["Low", "Medium", "High"],
        "avg_warn_layoffs": [3185.85, 5774.75, 11521.15],
        "avg_ca_unemployment_rate": [5.91, 5.11, 5.35],
        "avg_indeed_job_postings_index": [131.53, 108.96, 107.49],
        "avg_news_volume": [14036.30, 15242.80, 24990.50],
        "avg_news_tone": [-1.51, -1.63, -1.74],
    }
)

best_reg_row = regression_metrics.loc[regression_metrics["test_rmse"].idxmin()]
best_reg_name = best_reg_row["model_name"]
best_reg_rmse = best_reg_row["test_rmse"]

coef_fig = px.bar(
    coefficients,
    x="feature",
    y="coefficient",
    title="Final Deployed Model Coefficients",
)
coef_fig.update_layout(
    template="plotly_white",
    xaxis_title="Feature",
    yaxis_title="Coefficient",
    showlegend=False,
)

heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=lag_heatmap_df.values,
        x=["0 months", "1 month", "2 months", "3 months"],
        y=list(lag_heatmap_df.index),
        colorscale="RdBu_r",
        zmid=0,
        zmin=-0.8,
        zmax=0.8,
        colorbar_title="corr",
    )
)
heatmap_fig.update_layout(
    title="Lead-Lag Correlation Heatmap",
    xaxis_title="Lag",
    yaxis_title="Predictor",
    template="plotly_white",
)

risk_fig = px.bar(
    risk_summary,
    x="risk_level",
    y="avg_news_volume",
    title="Average News Volume by Risk Level",
    text="avg_news_volume",
    color="risk_level",
)
risk_fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
risk_fig.update_layout(
    template="plotly_white",
    xaxis_title="Risk level",
    yaxis_title="Average news volume",
    showlegend=False,
)

graph_config = {
    "displayModeBar": False,
    "responsive": True,
}

table_style = {
    "style_table": {"overflowX": "auto"},
    "style_cell": {
        "textAlign": "left",
        "padding": "10px",
        "fontFamily": "Arial",
        "fontSize": "14px",
        "whiteSpace": "normal",
        "height": "auto",
    },
    "style_header": {
        "backgroundColor": "#0f172a",
        "color": "white",
        "fontWeight": "bold",
    },
    "style_data": {
        "backgroundColor": "white",
        "border": "1px solid #e5e7eb",
    },
}

layout = html.Div(
    [
        html.H1("Major Findings"),
        html.P(
            "This page brings together the strongest results from the project: lead-lag patterns, model comparison, risk-level findings, and the final deployed model."
        ),

        html.Div(
            [
                html.Div([html.H3("Final Model"), html.P(best_reg_name)], className="finding-card"),
                html.Div([html.H3("Best Test RMSE"), html.P(f"{best_reg_rmse:.3f}")], className="finding-card"),
                html.Div([html.H3("Risk Engine"), html.P("Regression-based")], className="finding-card"),
                html.Div([html.H3("Strongest Lead Signal"), html.P("Fed funds (1 month)")], className="finding-card"),
            ],
            className="finding-grid",
        ),

        html.Section(
            [
                html.H2("Interactive Actual vs Predicted Layoffs"),

                dcc.RadioItems(
                    id="line-toggle",
                    options=[
                        {"label": "Actual Only", "value": "actual"},
                        {"label": "Predicted Only", "value": "pred"},
                        {"label": "Both", "value": "both"},
                    ],
                    value="both",
                    labelStyle={"display": "inline-block", "margin-right": "15px"},
                ),

                dcc.Graph(id="layoff-line-chart"),
            ],
            className="chart-section",
        ),

        html.Section(
            [
                html.H2("Lead-lag relationships"),
                dcc.Graph(figure=heatmap_fig),
            ],
            className="chart-section",
        ),

        html.Section(
            [
                html.H2("Regression model comparison"),
                dash_table.DataTable(
                    data=regression_metrics.to_dict("records"),
                    columns=[{"name": c, "id": c} for c in regression_metrics.columns],
                    **table_style,
                ),
            ],
            className="table-block",
        ),

        html.Section(
            [
                html.H2("Classification model comparison"),
                dash_table.DataTable(
                    data=classification_metrics.to_dict("records"),
                    columns=[{"name": c, "id": c} for c in classification_metrics.columns],
                    **table_style,
                ),
            ],
            className="table-block",
        ),

        html.Section(
            [
                html.H2("Risk-level findings"),
                dash_table.DataTable(
                    data=risk_summary.round(2).to_dict("records"),
                    columns=[{"name": c, "id": c} for c in risk_summary.columns],
                    **table_style,
                ),
                dcc.Graph(figure=risk_fig),
            ],
            className="chart-section",
        ),

        html.Section(
            [
                html.H2("Final deployed model coefficients"),
                dcc.Graph(figure=coef_fig),
            ],
            className="chart-section",
        ),
    ],
    className="text-page",
)

@callback(
    Output("layoff-line-chart", "figure"),
    Input("line-toggle", "value"),
)
def update_layoff_chart(view):
    fig = go.Figure()

    if view in ["actual", "both"]:
        fig.add_trace(go.Scatter(
            x=website_predictions["month"],
            y=website_predictions["warn_layoffs"],
            mode="lines+markers",
            name="Actual"
        ))

    if view in ["pred", "both"]:
        fig.add_trace(go.Scatter(
            x=website_predictions["month"],
            y=website_predictions["pred_warn_layoffs"],
            mode="lines+markers",
            name="Predicted"
        ))

    fig.update_layout(
        title="Actual vs Predicted WARN Layoffs",
        xaxis_title="Month",
        yaxis_title="WARN layoffs",
        template="plotly_white",
    )

    return fig
