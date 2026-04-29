import dash
from dash import html, dcc
import plotly.express as px

from utils.data_loader import (
    load_regression_metrics,
    load_classification_metrics,
    load_final_model_coefficients
)

dash.register_page(__name__, name="Major Findings")

reg_metrics = load_regression_metrics()
clf_metrics = load_classification_metrics()
coef_df = load_final_model_coefficients()

coef_fig = px.bar(
    coef_df,
    x="feature",
    y="coefficient",
    title="Final Model Coefficients"
)
coef_fig.update_layout(template="plotly_white")

layout = html.Div(
    [
        html.H1("Major Findings"),
        html.P(
            "This page summarizes the strongest results from the project."
        ),

        html.H2("Main takeaways"),
        html.Ul(
            [
                html.Li("Some macro and news signals showed short lead relationships with WARN layoffs."),
                html.Li("A simpler macro-only regression generalized better than the more complex models."),
                html.Li("Classification models were weaker, so they were not used as the deployed website engine."),
                html.Li("High-risk months were associated with substantially higher layoff-related news volume.")
            ]
        ),

        html.H2("Regression model comparison"),
        html.Div(
            [
                html.Pre(reg_metrics.to_string(index=False))
            ],
            className="table-block"
        ),

        html.H2("Classification model comparison"),
        html.Div(
            [
                html.Pre(clf_metrics.to_string(index=False))
            ],
            className="table-block"
        ),

        html.H2("Final deployed model coefficients"),
        dcc.Graph(figure=coef_fig)
    ],
    className="text-page"
)