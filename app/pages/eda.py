import dash
from dash import html
from utils.data_loader import load_final_predictions

dash.register_page(__name__, name="EDA")

pred_df = load_final_predictions()

start_month = pred_df["month"].min().strftime("%Y-%m")
end_month = pred_df["month"].max().strftime("%Y-%m")

layout = html.Div(
    [
        html.H1("EDA"),
        html.P(
            "This page explains the exploratory data analysis and the cleaned data used in the project."
        ),

        html.H2("Data sources"),
        html.Ul(
            [
                html.Li("California WARN notices"),
                html.Li("FRED macroeconomic indicators"),
                html.Li("GDELT layoff-related news features")
            ]
        ),

        html.H2("What we cleaned"),
        html.P(
            "The WARN data required the most cleaning. The original source came from PDFs, "
            "so the project involved extracting tables, validating rows, fixing parsing issues, "
            "and building a trustworthy monthly layoff target."
        ),

        html.H2("Current usable timeline"),
        html.P(f"The current final website prediction table spans from {start_month} to {end_month}."),

        html.H2("What this page will show later"),
        html.Ul(
            [
                html.Li("WARN layoffs over time"),
                html.Li("Yearly layoff totals"),
                html.Li("Basic cleaned-data summaries"),
                html.Li("A short explanation of the PDF-to-dataset workflow")
            ]
        )
    ],
    className="text-page"
)