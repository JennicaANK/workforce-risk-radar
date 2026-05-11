import dash
from dash import Input, Output, callback, dcc, html


dash.register_page(__name__, path="/live-demo", name="Live Demo")


DEFAULT_FED_FUNDS_RATE_LAG_1 = 5.25
DEFAULT_CA_UNEMPLOYMENT_RATE_LAG_3 = 5.1
DEFAULT_INDEED_JOB_POSTINGS_LAG_1 = 109
DEFAULT_LATEST_ACTUAL_LAYOFFS = 5095


def predict_warn_layoffs(fed_rate: float, unemployment_rate: float, postings_index: int) -> int:
    """Simple demo formula calibrated so the example inputs return about 5,095 layoffs."""
    prediction = 2500 + 280 * fed_rate + 620 * unemployment_rate - 18 * postings_index
    return max(0, round(prediction))


def classify_risk(predicted_layoffs: int) -> tuple[str, str]:
    """Convert the predicted layoff count into a presentation-friendly risk label."""
    if predicted_layoffs >= 6500:
        return (
            "High",
            "The model predicts a high layoff environment. Risk is near levels associated "
            "with spike periods, so workforce conditions may be under significant stress.",
        )
    if predicted_layoffs >= 4000:
        return (
            "Medium",
            "The model predicts a moderate layoff environment. Risk is elevated compared "
            "with low-risk months but below high-risk spike periods.",
        )
    return (
        "Low",
        "The model predicts a relatively low layoff environment. Risk appears contained "
        "compared with moderate or high-risk months.",
    )


def slider_block(slider_id: str, label: str, value_id: str, min_value, max_value, step, value, marks):
    return html.Div(
        [
            html.Div(
                [
                    html.Label(label, className="slider-label"),
                    html.Span(id=value_id, className="slider-value"),
                ],
                className="slider-header",
            ),
            dcc.Slider(
                id=slider_id,
                min=min_value,
                max=max_value,
                step=step,
                value=value,
                marks=marks,
                tooltip={"placement": "bottom", "always_visible": False},
            ),
        ],
        className="input-slider-block",
    )


layout = html.Div(
    [
        html.Section(
            [
                html.P("Interactive layoff-risk scenario tool", className="hero-kicker"),
                html.H1("Live Risk Scenario", className="hero-title"),
                html.P(
                    "Adjust the lagged model inputs to estimate California WARN layoffs and "
                    "see how the predicted risk level changes in real time."
                ),
                html.Div(
                    [
                        html.Span("Federal funds rate, 1-month lag", className="meta-chip"),
                        html.Span("CA unemployment rate, 3-month lag", className="meta-chip"),
                        html.Span("Indeed postings index, 1-month lag", className="meta-chip"),
                    ],
                    className="meta-chip-row",
                ),
            ],
            className="hero-section",
        ),

        html.Section(
            [
                html.Div(
                    [
                        html.H2("Scenario inputs"),
                        html.P(
                            "Tune each lagged signal to compare macroeconomic conditions and hiring demand.",
                            className="section-note",
                        ),
                        slider_block(
                            "fed-funds-rate-lag-1",
                            "Federal funds rate, 1-month lag",
                            "fed-funds-rate-display",
                            0.0,
                            8.0,
                            0.05,
                            DEFAULT_FED_FUNDS_RATE_LAG_1,
                            {0: "0%", 2: "2%", 4: "4%", 6: "6%", 8: "8%"},
                        ),
                        slider_block(
                            "ca-unemployment-rate-lag-3",
                            "CA unemployment rate, 3-month lag",
                            "ca-unemployment-rate-display",
                            2.0,
                            12.0,
                            0.1,
                            DEFAULT_CA_UNEMPLOYMENT_RATE_LAG_3,
                            {2: "2%", 4: "4%", 6: "6%", 8: "8%", 10: "10%", 12: "12%"},
                        ),
                        slider_block(
                            "indeed-job-postings-lag-1",
                            "Indeed postings index, 1-month lag",
                            "indeed-job-postings-display",
                            60,
                            160,
                            1,
                            DEFAULT_INDEED_JOB_POSTINGS_LAG_1,
                            {60: "60", 80: "80", 100: "100", 120: "120", 140: "140", 160: "160"},
                        ),
                    ],
                    className="summary-card live-demo-input-card",
                ),
                html.Div(
                    [
                        html.H2("Forecast output"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3("Predicted layoffs"),
                                        html.P(id="predicted-layoffs", className="card-value"),
                                    ],
                                    className="summary-card live-demo-metric-card",
                                ),
                                html.Div(
                                    [
                                        html.H3("Risk level"),
                                        html.Div(id="risk-level-output", className="risk-pill-wrapper"),
                                    ],
                                    className="summary-card live-demo-metric-card",
                                ),
                            ],
                            className="home-card-grid live-demo-output-grid",
                        ),
                        html.Div(
                            [
                                html.H3("Interpretation"),
                                html.P(id="risk-interpretation", className="small-note live-demo-interpretation"),
                            ],
                            className="summary-card home-highlight-card",
                        ),
                    ],
                    className="live-demo-output-column",
                ),
            ],
            className="live-demo-grid",
        ),

        html.Section(
            [
                html.Div(
                    [
                        html.H3("Comparison to latest actual month"),
                        html.P("Latest actual WARN layoffs", className="small-note"),
                        html.P(f"{DEFAULT_LATEST_ACTUAL_LAYOFFS:,.0f}", className="card-value"),
                    ],
                    className="summary-card home-summary-card",
                ),
                html.Div(
                    [
                        html.H3("Scenario forecast error"),
                        html.P(id="gap-direction", className="gap-label"),
                        html.P(id="gap-display", className="card-value"),
                        html.P(
                            "Predicted layoffs minus the latest actual WARN layoffs.",
                            className="small-note",
                        ),
                    ],
                    className="summary-card home-highlight-card",
                ),
            ],
            className="home-card-grid",
        ),

        html.Section(
            [
                html.H2("Scenario guide"),
                html.Ul(
                    [
                        html.Li("Raise the fed funds rate or unemployment rate to test a higher-stress scenario."),
                        html.Li("Lower the Indeed postings index to simulate weaker hiring demand."),
                        html.Li("Compare the forecast error card against the latest observed WARN layoff month."),
                        html.Li("Use the risk label and interpretation as a quick read on the scenario."),
                    ]
                ),
            ],
            className="text-section",
        ),
    ]
)


@callback(
    Output("fed-funds-rate-display", "children"),
    Output("ca-unemployment-rate-display", "children"),
    Output("indeed-job-postings-display", "children"),
    Output("predicted-layoffs", "children"),
    Output("risk-level-output", "children"),
    Output("risk-interpretation", "children"),
    Output("gap-direction", "children"),
    Output("gap-direction", "className"),
    Output("gap-display", "children"),
    Input("fed-funds-rate-lag-1", "value"),
    Input("ca-unemployment-rate-lag-3", "value"),
    Input("indeed-job-postings-lag-1", "value"),
)
def update_live_demo(fed_rate, unemployment_rate, postings_index):
    predicted_layoffs = predict_warn_layoffs(fed_rate, unemployment_rate, postings_index)
    risk_level, interpretation = classify_risk(predicted_layoffs)
    risk_class = f"risk-pill risk-{risk_level.lower()}"

    difference = predicted_layoffs - DEFAULT_LATEST_ACTUAL_LAYOFFS
    if difference > 0:
        gap_direction = "Overprediction"
        gap_class = "gap-label gap-positive"
        gap_display = f"{difference:+,.0f}"
    elif difference < 0:
        gap_direction = "Underprediction"
        gap_class = "gap-label gap-negative"
        gap_display = f"{difference:+,.0f}"
    else:
        gap_direction = "No forecast error"
        gap_class = "gap-label gap-neutral"
        gap_display = "0"

    return (
        f"{fed_rate:.2f}",
        f"{unemployment_rate:.1f}",
        f"{postings_index:.0f}",
        f"{predicted_layoffs:,.0f}",
        html.Span(risk_level, className=risk_class),
        interpretation,
        gap_direction,
        gap_class,
        gap_display,
    )
