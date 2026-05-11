from dash import Dash, html, dcc, page_container, page_registry, Input, Output, callback

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Workforce Risk Radar",
)

def build_navbar():
    return html.Nav(
        [
            html.Div("Workforce Risk Radar", className="nav-brand"),
            html.Div(id="navbar-links", className="nav-links"),
        ],
        className="navbar",
    )

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        build_navbar(),
        html.Main(page_container, className="page-content"),
    ],
    className="app-shell",
)

@callback(
    Output("navbar-links", "children"),
    Input("url", "pathname"),
)
def update_nav_links(pathname):
    if not pathname:
        pathname = "/"

    desired_order = ["Home", "Project Objective", "EDA", "Analysis Methods", "Major Findings", "Live Demo"]
    links = []

    for page_name in desired_order:
        page = next((p for p in page_registry.values() if p["name"] == page_name), None)
        if page is None:
            continue

        href = page["relative_path"]

        if href == "/":
            is_active = pathname in ["/", ""]
        else:
            is_active = pathname.rstrip("/") == href.rstrip("/")

        class_name = "nav-link active" if is_active else "nav-link"

        links.append(
            dcc.Link(
                page["name"],
                href=href,
                className=class_name,
            )
        )

    return links

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
