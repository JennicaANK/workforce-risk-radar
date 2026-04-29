import dash
from dash import html

dash.register_page(__name__, name="Analysis Methods")

layout = html.Div(
    [
        html.H1("Analysis Methods"),
        html.P(
            "This page explains how the data was transformed into the final modeling pipeline."
        ),

        html.H2("Modeling workflow"),
        html.Ol(
            [
                html.Li("Build a cleaned monthly master dataset"),
                html.Li("Create lagged macroeconomic and news features"),
                html.Li("Use a time-based train/test split"),
                html.Li("Compare multiple regression and classification models"),
                html.Li("Choose the deployed model based on test performance"),
                html.Li("Convert predicted layoffs into Low / Medium / High risk levels")
            ]
        ),

        html.H2("Models tested"),
        html.Ul(
            [
                html.Li("Linear Regression"),
                html.Li("Ridge Regression"),
                html.Li("Random Forest Regressor"),
                html.Li("Logistic Regression"),
                html.Li("Random Forest Classifier")
            ]
        ),

        html.H2("Final model choice"),
        html.P(
            "The final deployed model is Linear Regression (Macro only). "
            "It was chosen because it performed best on unseen test months and was easier to explain "
            "than the more complex alternatives."
        ),

        html.H2("Why the website risk label is not classifier-based"),
        html.P(
            "The classification models were kept as comparison results only. "
            "Their performance was weaker, so the website uses the stronger regression output "
            "and converts predicted layoffs into Low / Medium / High risk."
        )
    ],
    className="text-page"
)