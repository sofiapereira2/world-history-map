import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import pycountry
import anthropic

# ── data ──────────────────────────────────────────────────────────
import random
random.seed(42)
countries_list = list(pycountry.countries)
random.shuffle(countries_list)
df = pd.DataFrame([
    {"iso": c.alpha_3, "name": c.name, "color": i}
    for i, c in enumerate(countries_list)
])

# ── colors ────────────────────────────────────────────────────────
_BG       = "#050a14"
_LAND     = "#1a3a5c"
_LAND2    = "#22496e"
_OCEAN    = "#0a1628"
_SELECTED = "#f59e0b"
_BORDER   = "#2a4a6a"
_PANEL    = "#080f1c"
_ACCENT   = "#f59e0b"
_BLUE     = "#38bdf8"
_TEXT     = "#cbd5e1"
_DIM      = "#334155"
_GRAT     = "#112236"


def build_figure(selected_iso: str | None = None) -> go.Figure:
    fig = go.Figure()

    # base layer — each country gets a unique color
    fig.add_trace(go.Choropleth(
        locations=df["iso"],
        z=df["color"],
        colorscale="HSV",
        showscale=False,
        text=df["name"],
        hovertemplate="<b>%{text}</b><extra></extra>",
        marker_line_color="rgba(0,0,0,0.4)",
        marker_line_width=0.5,
    ))

    # highlighted country
    if selected_iso:
        sel = df[df["iso"] == selected_iso]
        if not sel.empty:
            fig.add_trace(go.Choropleth(
                locations=sel["iso"],
                z=[1],
                colorscale=[[0, _SELECTED], [1, _SELECTED]],
                showscale=False,
                text=sel["name"],
                hovertemplate="<b>%{text}</b><extra></extra>",
                marker_line_color="#fcd34d",
                marker_line_width=1.5,
            ))

    fig.update_layout(
        paper_bgcolor=_BG,
        geo=dict(
            bgcolor=_OCEAN,
            landcolor=_LAND,
            showocean=True,      oceancolor=_OCEAN,
            showlakes=True,      lakecolor=_OCEAN,
            showcoastlines=True, coastlinecolor=_BORDER, coastlinewidth=0.4,
            showframe=False,
            projection_type="orthographic",   # ← globo rotacionável
            projection_scale=1,
        ),
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        uirevision="world-map",
        dragmode="pan",
    )
    return fig


# ── layout ────────────────────────────────────────────────────────
_placeholder = html.Div(
    style={
        "display": "flex", "flexDirection": "column",
        "alignItems": "center", "justifyContent": "center",
        "height": "100%", "color": _DIM, "textAlign": "center", "gap": "10px",
    },
    children=[
        html.Div("🌐", style={"fontSize": "52px"}),
        html.P("Click any country", style={"margin": 0, "fontSize": "15px", "color": "#475569"}),
        html.P("to explore its history", style={"margin": 0, "fontSize": "12px", "color": "#334155"}),
        html.P("Drag the globe to rotate • Scroll to zoom",
               style={"margin": "16px 0 0", "fontSize": "11px", "color": "#1e3a5f"}),
    ],
)

app = dash.Dash(__name__, title="World History Globe")

app.index_string = """
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: """ + _BG + """; overflow: hidden; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: """ + _PANEL + """; }
        ::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
        .country-title {
            font-size: 22px; font-weight: 300; color: """ + _ACCENT + """;
            letter-spacing: 1px; padding-bottom: 12px;
            border-bottom: 1px solid #0f2a44; margin-bottom: 16px;
            min-height: 40px;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
"""

app.layout = html.Div(
    style={
        "backgroundColor": _BG, "height": "100vh",
        "fontFamily": "'Inter', 'Segoe UI', sans-serif",
        "color": _TEXT, "display": "flex", "flexDirection": "column",
    },
    children=[
        # ── header ──────────────────────────────────────────────
        html.Div(
            style={
                "textAlign": "center", "padding": "14px 0 10px",
                "borderBottom": "1px solid #0f2a44", "flexShrink": 0,
                "background": "linear-gradient(180deg, #080f1c 0%, #050a14 100%)",
            },
            children=[
                html.H1("World History Globe",
                    style={"fontSize": "22px", "color": _BLUE,
                           "letterSpacing": "4px", "fontWeight": "300"}),
                html.P("Click any country · Drag to rotate · Scroll to zoom",
                    style={"color": "#1e3a5f", "fontSize": "11px", "marginTop": "4px",
                           "letterSpacing": "1px"}),
            ],
        ),

        # ── body ────────────────────────────────────────────────
        html.Div(
            style={"display": "flex", "flex": 1, "minHeight": 0},
            children=[
                # globe
                html.Div(
                    style={"flex": "3", "minWidth": 0, "position": "relative"},
                    children=[
                        dcc.Graph(
                            id="world-map",
                            figure=build_figure(),
                            config={"scrollZoom": True, "displayModeBar": False},
                            style={"height": "100%"},
                        ),
                    ],
                ),

                # history panel
                html.Div(
                    style={
                        "width": "420px", "flexShrink": 0,
                        "backgroundColor": _PANEL,
                        "borderLeft": "1px solid #0f2a44",
                        "padding": "24px 22px",
                        "overflowY": "auto",
                        "display": "flex", "flexDirection": "column",
                    },
                    children=[
                        html.Div(id="country-title", className="country-title"),
                        dcc.Loading(
                            type="circle",
                            color=_BLUE,
                            style={"flex": 1},
                            children=html.Div(
                                id="history-content",
                                style={"flex": 1},
                                children=_placeholder,
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# ── callback ──────────────────────────────────────────────────────
@app.callback(
    Output("world-map", "figure"),
    Output("country-title", "children"),
    Output("history-content", "children"),
    Input("world-map", "clickData"),
    prevent_initial_call=True,
)
def on_country_click(click_data):
    if not click_data or not click_data.get("points"):
        raise dash.exceptions.PreventUpdate

    pt  = click_data["points"][0]
    iso = pt.get("location", "")
    if not iso:
        raise dash.exceptions.PreventUpdate

    name = pt.get("text", iso)
    try:
        obj = pycountry.countries.get(alpha_3=iso)
        if obj:
            name = obj.name
    except Exception:
        pass

    # ── Claude API ──────────────────────────────────────────────
    try:
        client = anthropic.Anthropic()
        prompt = (
            f"Write an engaging and educational historical summary about {name}. "
            "Cover: ancient origins and peoples, decisive historical periods, "
            "formation of the modern state, and cultural legacy. "
            "No markdown or asterisks. 4 well-developed paragraphs."
        )
        with client.messages.stream(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            msg = stream.get_final_message()

        text  = next((b.text for b in msg.content if b.type == "text"), "")
        paras = [p.strip() for p in text.split("\n\n") if p.strip()] or [text.strip()]

        content = [
            html.P(p, style={
                "lineHeight": "1.85", "marginBottom": "14px",
                "fontSize": "13.5px", "color": _TEXT, "textAlign": "justify",
            })
            for p in paras
        ]

    except Exception as exc:
        content = [html.P(f"Error: {exc}", style={"color": "#f87171", "fontSize": "13px"})]

    return build_figure(selected_iso=iso), name, content


if __name__ == "__main__":
    app.run(debug=False, port=8050)
