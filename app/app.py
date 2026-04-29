from dash import Dash, html, dcc, page_container, page_registry

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Workforce Risk Radar"
)

def build_navbar():
    nav_links = []
    desired_order = ["Home", "EDA", "Analysis Methods", "Major Findings"]

    for page_name in desired_order:
        for page in page_registry.values():
            if page["name"] == page_name:
                nav_links.append(
                    dcc.Link(
                        page["name"],
                        href=page["relative_path"],
                        className="nav-link"
                    )
                )

    return html.Nav(
        [
            html.Div("Workforce Risk Radar", className="nav-brand"),
            html.Div(nav_links, className="nav-links")
        ],
        className="navbar"
    )

app.layout = html.Div(
    [
        build_navbar(),
        html.Main(page_container, className="page-content")
    ],
    className="app-shell"
)

server = app.server

if __name__ == "__main__":
    app.run(debug=True)