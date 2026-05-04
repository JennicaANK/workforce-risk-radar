from dash import html
import dash

dash.register_page(__name__, name="Project Objective")

layout = html.Div(
    [
        html.H2("Project Objective"),
        html.P(
            "The goal of this project is to build a workforce risk radar that "
            "tracks California WARN layoffs using macroeconomic and news signals."
        ),

        html.H3("Main Goals"),
        html.Ul([
            html.Li("Predict monthly layoffs using macro + news signals"),
            html.Li("Identify early warning indicators of layoffs"),
            html.Li("Translate predictions into risk levels"),
        ]),

        html.H3("Data Sources"),
        html.Ul([
            html.Li("California WARN notices"),
            html.Li("FRED macroeconomic indicators"),
            html.Li("GDELT news data"),
        ]),
    ],
    className="text-page"
)
