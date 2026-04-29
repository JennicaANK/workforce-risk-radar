import dash
from dash import html

dash.register_page(__name__, name="Analysis Methods")

layout = html.Div(
    [
        html.H1("Analysis Methods"),
        html.P(
            "This page explains how the project moved from raw source data to the final deployed dashboard model."
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.H3("Unit of analysis"),
                        html.P("Monthly statewide observations", className="finding-value"),
                    ],
                    className="finding-card",
                ),
                html.Div(
                    [
                        html.H3("Final deployed model"),
                        html.P("Linear Regression (Macro only)", className="finding-value"),
                    ],
                    className="finding-card",
                ),
                html.Div(
                    [
                        html.H3("Risk label logic"),
                        html.P("Derived from predicted layoffs", className="finding-value"),
                    ],
                    className="finding-card",
                ),
                html.Div(
                    [
                        html.H3("Evaluation style"),
                        html.P("Time-based train/test split", className="finding-value"),
                    ],
                    className="finding-card",
                ),
            ],
            className="finding-grid",
        ),

        html.Section(
            [
                html.H2("Modeling workflow"),
                html.Ol(
                    [
                        html.Li("Collect and clean California WARN layoff notices"),
                        html.Li("Aggregate WARN records into monthly California layoff totals"),
                        html.Li("Merge WARN with macroeconomic indicators and layoff-related news features"),
                        html.Li("Create lagged predictors to support the early-warning goal"),
                        html.Li("Split the data into train and test periods by time"),
                        html.Li("Compare multiple regression and classification models"),
                        html.Li("Choose the deployed model based on test-period performance"),
                        html.Li("Convert predicted layoffs into Low / Medium / High risk labels"),
                    ]
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.H2("Why the project uses monthly data"),
                html.P(
                    "The final modeling dataset uses monthly statewide observations. This keeps the modeling target interpretable and matches the dashboard goal of tracking broad layoff risk over time."
                ),
                html.P(
                    "The project began with much more raw WARN detail, but the final dashboard focuses on monthly California layoff totals so the trend, model output, and risk level are easier to explain."
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.H2("Why we used lagged features"),
                html.P(
                    "The project is framed as an early-warning system, so we focused on lagged predictors rather than only same-month associations."
                ),
                html.Ul(
                    [
                        html.Li("Unemployment at lag 3"),
                        html.Li("Federal funds rate at lag 1"),
                        html.Li("Indeed job postings at lag 1"),
                        html.Li("News volume at lag 1"),
                        html.Li("News tone at lag 1"),
                    ]
                ),
                html.P(
                    "These lag choices were guided by the earlier lead-lag analysis, where federal funds rate, unemployment, and news tone showed meaningful relationships one to three months before WARN changes."
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.H2("Models tested"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Regression models"),
                                html.Ul(
                                    [
                                        html.Li("Linear Regression"),
                                        html.Li("Ridge Regression"),
                                        html.Li("Random Forest Regressor"),
                                    ]
                                ),
                            ],
                            className="method-card",
                        ),
                        html.Div(
                            [
                                html.H3("Classification models"),
                                html.Ul(
                                    [
                                        html.Li("Logistic Regression"),
                                        html.Li("Random Forest Classifier"),
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
                html.H2("How we evaluated the models"),
                html.P(
                    "We did not use a random split. Instead, we kept the last 12 months as the test period so evaluation would better reflect future forecasting conditions."
                ),
                html.P(
                    "For regression, we compared models using test RMSE and training metrics to check whether more complex models were overfitting. For classification, we compared accuracy, precision, recall, and macro F1."
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.H2("Why Linear Regression was chosen"),
                html.P(
                    "The final deployed model is Linear Regression (Macro only). It was chosen because it had the best test RMSE among the regression models and generalized better than the more complex alternatives."
                ),
                html.P(
                    "This choice matters because the larger models looked better in some training metrics, but they did not perform better on unseen months. For the deployed dashboard, reliability mattered more than complexity."
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.H2("Why the website risk label is not classifier-based"),
                html.P(
                    "The classification models were still useful as comparison experiments, but they were not strong enough to serve as the main deployed website engine."
                ),
                html.P(
                    "Instead, the site uses the stronger regression output and converts predicted layoffs into Low / Medium / High risk levels using thresholds defined from the training period."
                ),
            ],
            className="text-section",
        ),

        html.Section(
            [
                html.H2("Final deployment logic"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Input"),
                                html.P("Cleaned monthly dataset with lagged macro predictors"),
                            ],
                            className="method-card",
                        ),
                        html.Div(
                            [
                                html.H3("Prediction"),
                                html.P("Monthly WARN layoffs from the final macro-only linear regression"),
                            ],
                            className="method-card",
                        ),
                        html.Div(
                            [
                                html.H3("Risk label"),
                                html.P("Low / Medium / High based on predicted layoffs"),
                            ],
                            className="method-card",
                        ),
                        html.Div(
                            [
                                html.H3("Website output"),
                                html.P("Latest risk level, predicted layoffs, trend chart, and supporting findings"),
                            ],
                            className="method-card",
                        ),
                    ],
                    className="method-grid",
                ),
            ],
            className="text-section",
        ),
    ],
    className="text-page",
)