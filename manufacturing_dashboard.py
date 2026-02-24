"""
US Manufacturing Carrying Cost Dashboard
Techno-Economic Sensitivity Analysis — Phase 2
Author: Research Project | February 2026
Run: python manufacturing_dashboard.py
Visit: http://127.0.0.1:8050
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# REAL DATA — Corrected per professor feedback
# Sources: FRED/BEA, SUSB 2022, BLS Dec 2025
# ─────────────────────────────────────────────

# NAICS Industry Data — Output corrected from FRED
industry_data = pd.DataFrame([
    {"naics": "311", "name": "Food Manufacturing",         "firms": 27000,  "employment": 1700000, "output_b": 347,  "ccc_low": 45,  "ccc_high": 75,  "margin_low": 3,  "margin_high": 8,  "small_pct": 80, "credit_dep": "Moderate"},
    {"naics": "312", "name": "Beverage & Tobacco",         "firms": 4500,   "employment": 180000,  "output_b": 89,   "ccc_low": 60,  "ccc_high": 90,  "margin_low": 12, "margin_high": 25, "small_pct": 72, "credit_dep": "Moderate"},
    {"naics": "313", "name": "Textile Mills",              "firms": 2800,   "employment": 94000,   "output_b": 18,   "ccc_low": 60,  "ccc_high": 100, "margin_low": 5,  "margin_high": 10, "small_pct": 88, "credit_dep": "High"},
    {"naics": "314", "name": "Textile Product Mills",      "firms": 4100,   "employment": 124000,  "output_b": 16,   "ccc_low": 60,  "ccc_high": 90,  "margin_low": 6,  "margin_high": 12, "small_pct": 85, "credit_dep": "High"},
    {"naics": "315", "name": "Apparel Manufacturing",      "firms": 7200,   "employment": 94000,   "output_b": 12,   "ccc_low": 90,  "ccc_high": 150, "margin_low": 15, "margin_high": 30, "small_pct": 93, "credit_dep": "Very High"},
    {"naics": "316", "name": "Leather & Allied Products",  "firms": 2100,   "employment": 26000,   "output_b": 5,    "ccc_low": 90,  "ccc_high": 120, "margin_low": 10, "margin_high": 18, "small_pct": 90, "credit_dep": "High"},
    {"naics": "321", "name": "Wood Product Manufacturing", "firms": 12000,  "employment": 395000,  "output_b": 60,   "ccc_low": 45,  "ccc_high": 75,  "margin_low": 5,  "margin_high": 12, "small_pct": 88, "credit_dep": "Moderate"},
    {"naics": "322", "name": "Paper Manufacturing",        "firms": 3600,   "employment": 340000,  "output_b": 75,   "ccc_low": 30,  "ccc_high": 60,  "margin_low": 8,  "margin_high": 15, "small_pct": 78, "credit_dep": "Moderate"},
    {"naics": "323", "name": "Printing & Related",         "firms": 22000,  "employment": 390000,  "output_b": 70,   "ccc_low": 45,  "ccc_high": 75,  "margin_low": 8,  "margin_high": 15, "small_pct": 91, "credit_dep": "Moderate"},
    {"naics": "324", "name": "Petroleum & Coal Products",  "firms": 2800,   "employment": 115000,  "output_b": 380,  "ccc_low": 15,  "ccc_high": 30,  "margin_low": 2,  "margin_high": 5,  "small_pct": 55, "credit_dep": "Low"},
    {"naics": "325", "name": "Chemical Manufacturing",     "firms": 13500,  "employment": 552000,  "output_b": 450,  "ccc_low": 45,  "ccc_high": 90,  "margin_low": 12, "margin_high": 22, "small_pct": 78, "credit_dep": "High"},
    {"naics": "326", "name": "Plastics & Rubber",          "firms": 15000,  "employment": 730000,  "output_b": 195,  "ccc_low": 60,  "ccc_high": 90,  "margin_low": 8,  "margin_high": 14, "small_pct": 86, "credit_dep": "High"},
    {"naics": "327", "name": "Nonmetallic Mineral",        "firms": 12000,  "employment": 410000,  "output_b": 115,  "ccc_low": 30,  "ccc_high": 60,  "margin_low": 10, "margin_high": 18, "small_pct": 84, "credit_dep": "Moderate"},
    {"naics": "331", "name": "Primary Metal Manufacturing","firms": 4800,   "employment": 385000,  "output_b": 130,  "ccc_low": 45,  "ccc_high": 90,  "margin_low": 4,  "margin_high": 9,  "small_pct": 75, "credit_dep": "High"},
    {"naics": "332", "name": "Fabricated Metal Products",  "firms": 30000,  "employment": 1470000, "output_b": 190,  "ccc_low": 60,  "ccc_high": 120, "margin_low": 8,  "margin_high": 16, "small_pct": 97, "credit_dep": "Very High"},
    {"naics": "333", "name": "Machinery Manufacturing",    "firms": 24000,  "employment": 1120000, "output_b": 198,  "ccc_low": 90,  "ccc_high": 150, "margin_low": 10, "margin_high": 20, "small_pct": 90, "credit_dep": "Very High"},
    {"naics": "334", "name": "Computer & Electronics",     "firms": 14000,  "employment": 1060000, "output_b": 505,  "ccc_low": 60,  "ccc_high": 120, "margin_low": 12, "margin_high": 25, "small_pct": 82, "credit_dep": "High"},
    {"naics": "335", "name": "Electrical Equipment",       "firms": 8000,   "employment": 390000,  "output_b": 140,  "ccc_low": 60,  "ccc_high": 120, "margin_low": 8,  "margin_high": 16, "small_pct": 84, "credit_dep": "High"},
    {"naics": "336", "name": "Transportation Equipment",   "firms": 7500,   "employment": 1710000, "output_b": 925,  "ccc_low": 90,  "ccc_high": 180, "margin_low": 4,  "margin_high": 10, "small_pct": 86, "credit_dep": "Very High"},
    {"naics": "337", "name": "Furniture & Related",        "firms": 18000,  "employment": 390000,  "output_b": 58,   "ccc_low": 45,  "ccc_high": 90,  "margin_low": 8,  "margin_high": 15, "small_pct": 91, "credit_dep": "Moderate"},
    {"naics": "339", "name": "Miscellaneous Manufacturing","firms": 22000,  "employment": 545000,  "output_b": 145,  "ccc_low": 60,  "ccc_high": 120, "margin_low": 12, "margin_high": 22, "small_pct": 88, "credit_dep": "High"},
])
industry_data["ccc_mid"] = (industry_data["ccc_low"] + industry_data["ccc_high"]) / 2
industry_data["margin_mid"] = (industry_data["margin_low"] + industry_data["margin_high"]) / 2
industry_data["carrying_12pct"] = round(12 * industry_data["ccc_mid"] / 365, 2)

# Interest rate data — corrected per FRED (Feb 2026)
rate_data = {
    "Fed Funds Rate": 4.375,
    "Bank Prime Rate": 7.50,
    "AAA Corporate (Large Firm)": 5.30,
    "Small Mfg C&I Loan": 10.25,
    "SBA 7(a) Variable": 11.25,
    "Asset-Based Lending": 16.0,
    "SBA MARC Program": 12.0,
}

# Top state data (SUSB 2022 / IndustrySelect 2025)
state_data = pd.DataFrame([
    {"state": "California",     "firms": 22052,  "employment": 1340647},
    {"state": "Texas",          "firms": 16839,  "employment": 1107501},
    {"state": "Ohio",           "firms": 13907,  "employment": 851775},
    {"state": "Illinois",       "firms": 13597,  "employment": 724309},
    {"state": "Pennsylvania",   "firms": 13005,  "employment": 693521},
    {"state": "New York",       "firms": 12441,  "employment": 611490},
    {"state": "Michigan",       "firms": 11515,  "employment": 700780},
    {"state": "Wisconsin",      "firms": 8966,   "employment": 576757},
    {"state": "North Carolina", "firms": 8710,   "employment": 540289},
    {"state": "Indiana",        "firms": 7772,   "employment": 581280},
])

# ─────────────────────────────────────────────
# CORE CALCULATION FUNCTIONS
# ─────────────────────────────────────────────
def calculate_carrying_cost(revenue, interest_rate, dpo, dio, dsio, gross_margin, opex_ratio, tariff_shock=0):
    ccc = dio + dsio - dpo + tariff_shock
    working_capital = revenue * (ccc / 365)
    carrying_cost_usd = working_capital * (interest_rate / 100)
    carrying_cost_pct = (interest_rate / 100) * (ccc / 365) * 100
    true_net_margin = gross_margin - opex_ratio - carrying_cost_pct
    net_profit = revenue * (true_net_margin / 100)
    roc = (net_profit / working_capital * 100) if working_capital > 0 else 0
    return {
        "ccc": round(ccc, 1),
        "working_capital": round(working_capital, 0),
        "carrying_cost_usd": round(carrying_cost_usd, 0),
        "carrying_cost_pct": round(carrying_cost_pct, 2),
        "true_net_margin": round(true_net_margin, 2),
        "net_profit": round(net_profit, 0),
        "roc": round(roc, 2),
    }

# ─────────────────────────────────────────────
# APP LAYOUT
# ─────────────────────────────────────────────
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
app.title = "US Manufacturing Carrying Cost Dashboard"

COLORS = {
    "primary": "#1F3864",
    "accent": "#2E75B6",
    "warning": "#C00000",
    "success": "#375623",
    "light": "#EEF2F7",
    "white": "#FFFFFF",
}

def kpi_card(title, value, subtitle="", color=COLORS["accent"]):
    return dbc.Card([
        dbc.CardBody([
            html.P(title, className="text-muted mb-1", style={"fontSize": "12px", "fontWeight": "600", "textTransform": "uppercase"}),
            html.H4(value, style={"color": color, "fontWeight": "700", "marginBottom": "2px"}),
            html.P(subtitle, className="text-muted mb-0", style={"fontSize": "11px"}),
        ])
    ], style={"borderLeft": f"4px solid {color}", "borderRadius": "6px"})

# ── TABS ──────────────────────────────────────
tab_calculator = dbc.Tab(label="💰 Carrying Cost Calculator", tab_id="tab-calc")
tab_sensitivity = dbc.Tab(label="📊 Sensitivity Analysis", tab_id="tab-sens")
tab_industry    = dbc.Tab(label="🏭 Industry Breakdown", tab_id="tab-ind")
tab_states      = dbc.Tab(label="🗺️ State Overview", tab_id="tab-state")
tab_rates       = dbc.Tab(label="📈 Interest Rates", tab_id="tab-rates")

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H2("🏭 US Manufacturing Carrying Cost Dashboard", style={"color": COLORS["primary"], "fontWeight": "700", "marginBottom": "4px"}),
            html.P("Techno-Economic Sensitivity Analysis | Phase 2 | February 2026 | Sources: FRED, BEA, SUSB 2022, NAM Jan 2026, BLS Dec 2025",
                   className="text-muted mb-0", style={"fontSize": "12px"}),
        ])
    ], className="mb-3 mt-3"),

    # Top KPIs
    dbc.Row([
        dbc.Col(kpi_card("Total US Mfg Firms", "239,265", "SUSB 2022 / NAM Jan 2026", COLORS["primary"]), width=3),
        dbc.Col(kpi_card("Small Firms (< 500 emp)", "98.25%", "235,088 firms", COLORS["accent"]), width=3),
        dbc.Col(kpi_card("Mfg Employment", "12.69M", "BLS December 2025", COLORS["success"]), width=3),
        dbc.Col(kpi_card("Total Mfg Output", "$2.951T", "BEA Q3 2025 annualized", COLORS["warning"]), width=3),
    ], className="mb-3"),

    # Tabs
    dbc.Tabs([tab_calculator, tab_sensitivity, tab_industry, tab_states, tab_rates],
             id="tabs", active_tab="tab-calc", className="mb-3"),
    html.Div(id="tab-content"),

], fluid=True, style={"backgroundColor": "#F8F9FA", "minHeight": "100vh", "fontFamily": "Arial, sans-serif"})


# ─────────────────────────────────────────────
# TAB CONTENT ROUTER
# ─────────────────────────────────────────────
@app.callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab(tab):
    if tab == "tab-calc":   return layout_calculator()
    if tab == "tab-sens":   return layout_sensitivity()
    if tab == "tab-ind":    return layout_industry()
    if tab == "tab-state":  return layout_states()
    if tab == "tab-rates":  return layout_rates()
    return html.Div()


# ─────────────────────────────────────────────
# TAB 1: CALCULATOR
# ─────────────────────────────────────────────
def layout_calculator():
    preset_options = [{"label": f"{r['naics']} — {r['name']}", "value": r['naics']} for _, r in industry_data.iterrows()]
    preset_options.insert(0, {"label": "Custom (manual entry)", "value": "custom"})

    return dbc.Row([
        # LEFT — Inputs
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H6("📋 Business Inputs", className="mb-0 text-white"), style={"backgroundColor": COLORS["primary"]}),
                dbc.CardBody([
                    html.Label("Industry Preset (auto-fills typical values)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Dropdown(id="preset-dropdown", options=preset_options, value="custom", clearable=False, className="mb-3"),

                    html.Label("Annual Revenue ($)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Input(id="inp-revenue", type="number", value=2000000, min=100000, step=100000,
                              className="form-control mb-3", style={"fontSize": "13px"}),

                    html.Label("Gross Margin (%)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Slider(id="inp-margin", min=3, max=40, step=0.5, value=15,
                               marks={i: f"{i}%" for i in [3, 10, 20, 30, 40]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-3"),

                    html.Label("Annual Interest Rate (%)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Slider(id="inp-rate", min=4, max=36, step=0.25, value=10,
                               marks={i: f"{i}%" for i in [4, 8, 12, 18, 24, 36]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-3"),

                    html.Label("Days Inventory Outstanding — DIO (days)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Slider(id="inp-dio", min=15, max=180, step=5, value=60,
                               marks={i: str(i) for i in [15, 45, 90, 135, 180]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-3"),

                    html.Label("Days Sales Outstanding — DSO (days)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Slider(id="inp-dso", min=15, max=180, step=5, value=75,
                               marks={i: str(i) for i in [15, 45, 90, 135, 180]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-3"),

                    html.Label("Days Payable Outstanding — DPO (days)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Slider(id="inp-dpo", min=10, max=90, step=5, value=30,
                               marks={i: str(i) for i in [10, 30, 60, 90]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-3"),

                    html.Label("Operating Expense Ratio (%)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Slider(id="inp-opex", min=5, max=30, step=0.5, value=12,
                               marks={i: f"{i}%" for i in [5, 10, 20, 30]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-3"),

                    html.Hr(),
                    html.Label("⚠️ Tariff Shock — Extra DIO Days", style={"fontSize": "12px", "fontWeight": "600", "color": COLORS["warning"]}),
                    dcc.Slider(id="inp-tariff", min=0, max=60, step=5, value=0,
                               marks={i: str(i) for i in [0, 15, 30, 45, 60]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-2"),
                    html.P("Simulates inventory hoarding due to tariff uncertainty (per Fed Jan 2026 note)",
                           style={"fontSize": "11px", "color": "#888"}),
                ])
            ])
        ], width=4),

        # RIGHT — Outputs
        dbc.Col([
            html.Div(id="calc-outputs"),
        ], width=8),
    ])


@app.callback(
    [Output("inp-dio", "value"), Output("inp-dso", "value"),
     Output("inp-dpo", "value"), Output("inp-margin", "value"), Output("inp-rate", "value")],
    Input("preset-dropdown", "value")
)
def apply_preset(naics):
    if naics == "custom":
        return 60, 75, 30, 15, 10
    row = industry_data[industry_data["naics"] == naics].iloc[0]
    dio = int(row["ccc_mid"] * 0.5)
    dso = int(row["ccc_mid"] * 0.6)
    dpo = 30
    margin = row["margin_mid"]
    return dio, dso, dpo, margin, 10


@app.callback(
    Output("calc-outputs", "children"),
    [Input("inp-revenue", "value"), Input("inp-margin", "value"), Input("inp-rate", "value"),
     Input("inp-dio", "value"), Input("inp-dso", "value"), Input("inp-dpo", "value"),
     Input("inp-opex", "value"), Input("inp-tariff", "value")]
)
def update_calculator(revenue, margin, rate, dio, dso, dpo, opex, tariff):
    if not all([revenue, margin, rate, dio, dso, dpo, opex]):
        return html.P("Please fill in all inputs.")

    r = calculate_carrying_cost(revenue, rate, dpo, dio, dso, margin, opex, tariff)

    # Large firm comparison
    large = calculate_carrying_cost(revenue, 5.3, 60, 30, 30, margin, opex, 0)

    margin_color = COLORS["success"] if r["true_net_margin"] > 3 else (COLORS["warning"] if r["true_net_margin"] < 0 else "#E67E22")
    margin_label = "✅ Healthy" if r["true_net_margin"] > 5 else ("⚠️ Tight" if r["true_net_margin"] > 0 else "🚨 LOSS")

    # Waterfall chart
    waterfall = go.Figure(go.Waterfall(
        name="Margin Waterfall", orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Gross Margin", "Operating Expenses", "Carrying Cost", "Tariff Impact", "True Net Margin"],
        y=[margin, -opex, -(r["carrying_cost_pct"] - (tariff * rate / 36500)),
           -(tariff * rate / 36500), 0],
        connector={"line": {"color": COLORS["primary"]}},
        decreasing={"marker": {"color": "#C00000"}},
        increasing={"marker": {"color": "#375623"}},
        totals={"marker": {"color": COLORS["primary"]}},
        text=[f"{margin}%", f"-{opex}%", f"-{round(r['carrying_cost_pct'] - (tariff*rate/36500), 2)}%",
              f"-{round(tariff*rate/36500, 2)}%", f"{r['true_net_margin']}%"],
        textposition="outside"
    ))
    waterfall.update_layout(title="Margin Waterfall Analysis", height=300,
                            margin=dict(t=40, b=20, l=20, r=20),
                            plot_bgcolor="white", paper_bgcolor="white")

    # Small vs Large comparison bar
    comparison = go.Figure(data=[
        go.Bar(name="Your Business (Small)", x=["Borrowing Rate", "CCC Days", "Carrying Cost %", "True Net Margin %"],
               y=[rate, r["ccc"], r["carrying_cost_pct"], max(r["true_net_margin"], 0)],
               marker_color=COLORS["accent"]),
        go.Bar(name="Large Firm (AAA, 5.3%)", x=["Borrowing Rate", "CCC Days", "Carrying Cost %", "True Net Margin %"],
               y=[5.3, 37, large["carrying_cost_pct"], large["true_net_margin"]],
               marker_color=COLORS["success"]),
    ])
    comparison.update_layout(barmode="group", title="Small vs Large Firm Comparison",
                             height=300, margin=dict(t=40, b=20, l=20, r=20),
                             plot_bgcolor="white", paper_bgcolor="white",
                             legend=dict(orientation="h", yanchor="bottom", y=1.02))

    return html.Div([
        # KPI Row
        dbc.Row([
            dbc.Col(kpi_card("Cash Conversion Cycle", f"{r['ccc']} days", "DIO + DSO − DPO + Tariff", COLORS["primary"]), width=3),
            dbc.Col(kpi_card("Working Capital Required", f"${r['working_capital']:,.0f}", "Cash tied up at all times", COLORS["accent"]), width=3),
            dbc.Col(kpi_card("Annual Carrying Cost", f"${r['carrying_cost_usd']:,.0f}", f"{r['carrying_cost_pct']}% of revenue", COLORS["warning"]), width=3),
            dbc.Col(kpi_card("True Net Margin", f"{r['true_net_margin']}% {margin_label}", f"After carrying cost | ROC: {r['roc']}%", margin_color), width=3),
        ], className="mb-3"),

        # Alert if losing money
        dbc.Alert(f"🚨 This business is structurally losing money despite a {margin}% gross margin. The carrying cost alone consumes more than the available margin.",
                  color="danger", is_open=r["true_net_margin"] < 0, className="mb-3"),

        dbc.Alert(f"⚠️ Tariff shock adds ${round(tariff * rate / 36500 * revenue / 100):,.0f}/year in additional carrying cost ({round(tariff*rate/36500, 2)}% of revenue).",
                  color="warning", is_open=tariff > 0, className="mb-3"),

        # Charts
        dbc.Row([
            dbc.Col(dcc.Graph(figure=waterfall), width=6),
            dbc.Col(dcc.Graph(figure=comparison), width=6),
        ]),

        # Formula breakdown
        dbc.Card([
            dbc.CardHeader(html.H6("📐 Formula Breakdown", className="mb-0 text-white"), style={"backgroundColor": COLORS["primary"]}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.P(f"CCC = {int(dio)} + {int(dso)} − {int(dpo)} + {tariff} = {r['ccc']} days", style={"fontFamily": "monospace", "fontSize": "13px"}),
                        html.P(f"Working Capital = ${revenue:,.0f} × ({r['ccc']} ÷ 365) = ${r['working_capital']:,.0f}", style={"fontFamily": "monospace", "fontSize": "13px"}),
                        html.P(f"Carrying Cost ($) = ${r['working_capital']:,.0f} × {rate}% = ${r['carrying_cost_usd']:,.0f}/yr", style={"fontFamily": "monospace", "fontSize": "13px"}),
                    ], width=6),
                    dbc.Col([
                        html.P(f"Carrying Cost (%) = {rate}% × ({r['ccc']} ÷ 365) = {r['carrying_cost_pct']}%", style={"fontFamily": "monospace", "fontSize": "13px"}),
                        html.P(f"True Net Margin = {margin}% − {opex}% − {r['carrying_cost_pct']}% = {r['true_net_margin']}%", style={"fontFamily": "monospace", "fontSize": "13px"}),
                        html.P(f"ROC = ${r['net_profit']:,.0f} ÷ ${r['working_capital']:,.0f} = {r['roc']}%", style={"fontFamily": "monospace", "fontSize": "13px"}),
                    ], width=6),
                ])
            ])
        ], className="mt-3"),
    ])


# ─────────────────────────────────────────────
# TAB 2: SENSITIVITY ANALYSIS
# ─────────────────────────────────────────────
def layout_sensitivity():
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H6("⚙️ Sensitivity Settings", className="mb-0 text-white"), style={"backgroundColor": COLORS["primary"]}),
                dbc.CardBody([
                    html.Label("Gross Margin (%)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Slider(id="sens-margin", min=3, max=40, step=1, value=15,
                               marks={i: f"{i}%" for i in [3, 10, 20, 30, 40]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-3"),
                    html.Label("Operating Expense Ratio (%)", style={"fontSize": "12px", "fontWeight": "600"}),
                    dcc.Slider(id="sens-opex", min=5, max=25, step=1, value=8,
                               marks={i: f"{i}%" for i in [5, 10, 15, 20, 25]}, tooltip={"always_visible": True}),
                    html.Div(className="mb-2"),
                    html.P("Heatmap shows True Net Margin (%) across all rate × CCC combinations. Red = loss, green = profitable.",
                           style={"fontSize": "11px", "color": "#888"}),
                ])
            ]),
            dbc.Card([
                dbc.CardHeader(html.H6("📊 Rate Hike Impact", className="mb-0 text-white"), style={"backgroundColor": COLORS["accent"]}),
                dbc.CardBody([html.Div(id="rate-hike-impact")])
            ], className="mt-3"),
        ], width=3),
        dbc.Col([
            dcc.Graph(id="sensitivity-heatmap", style={"height": "550px"}),
        ], width=9),
    ])


@app.callback(
    [Output("sensitivity-heatmap", "figure"), Output("rate-hike-impact", "children")],
    [Input("sens-margin", "value"), Input("sens-opex", "value")]
)
def update_sensitivity(margin, opex):
    rates = np.arange(4, 25, 1)
    cccs = np.arange(30, 270, 15)
    z = []
    for ccc in cccs:
        row = []
        for rate in rates:
            carrying = rate * ccc / 365
            net = margin - opex - carrying
            row.append(round(net, 2))
        z.append(row)

    fig = go.Figure(data=go.Heatmap(
        z=z, x=[f"{r}%" for r in rates], y=[f"{c}d" for c in cccs],
        colorscale=[[0, "#C00000"], [0.3, "#FF6B6B"], [0.5, "#FFD700"], [0.7, "#90EE90"], [1, "#375623"]],
        zmid=0, zmin=-10, zmax=15,
        text=[[f"{v}%" for v in row] for row in z],
        texttemplate="%{text}", textfont={"size": 9},
        hovertemplate="Rate: %{x}<br>CCC: %{y}<br>True Net Margin: %{z}%<extra></extra>",
        colorbar=dict(title="True Net Margin %", ticksuffix="%")
    ))
    fig.update_layout(
        title=f"Sensitivity: True Net Margin | Gross Margin={margin}% | OpEx={opex}%",
        xaxis_title="Annual Interest Rate", yaxis_title="Cash Conversion Cycle (Days)",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=50, b=50, l=80, r=80)
    )

    # Rate hike impact text
    base_rate = 10
    hike_rates = [10, 12, 14, 16, 18]
    ccc_120 = 120
    impacts = []
    for r in hike_rates:
        carrying = r * ccc_120 / 365
        net = margin - opex - carrying
        color = "success" if net > 3 else ("warning" if net > 0 else "danger")
        impacts.append(dbc.Badge(f"{r}% → Net: {net:.1f}%", color=color, className="me-1 mb-1", style={"fontSize": "11px"}))

    impact_div = html.Div([
        html.P("At 120-day CCC:", style={"fontSize": "12px", "fontWeight": "600", "marginBottom": "6px"}),
        html.Div(impacts),
        html.P("Source: Federal Reserve SLOOS; carrying cost formula.", style={"fontSize": "10px", "color": "#888", "marginTop": "8px"}),
    ])
    return fig, impact_div


# ─────────────────────────────────────────────
# TAB 3: INDUSTRY BREAKDOWN
# ─────────────────────────────────────────────
def layout_industry():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="industry-bubble", style={"height": "420px"}),
            ], width=8),
            dbc.Col([
                dcc.Graph(id="industry-carrying", style={"height": "420px"}),
            ], width=4),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="industry-bar-output", style={"height": "380px"}),
            ], width=6),
            dbc.Col([
                dcc.Graph(id="industry-small-pct", style={"height": "380px"}),
            ], width=6),
        ]),
    ])


@app.callback(
    [Output("industry-bubble", "figure"), Output("industry-carrying", "figure"),
     Output("industry-bar-output", "figure"), Output("industry-small-pct", "figure")],
    Input("tabs", "active_tab")
)
def update_industry(tab):
    df = industry_data.copy()
    short_names = df["name"].str.replace(" Manufacturing", "").str.replace(" Products", "").str[:20]

    # Bubble: CCC vs Margin vs Output
    bubble = px.scatter(df, x="ccc_mid", y="margin_mid", size="output_b", color="credit_dep",
                        hover_name="name", text=df["naics"],
                        color_discrete_map={"Low": "#375623", "Moderate": "#2E75B6",
                                            "High": "#E67E22", "Very High": "#C00000"},
                        labels={"ccc_mid": "Avg CCC (days)", "margin_mid": "Avg Gross Margin (%)", "output_b": "Output $B"},
                        title="CCC vs Margin vs Output (bubble size = output $B)")
    bubble.update_traces(textposition="top center", textfont_size=9)
    bubble.update_layout(plot_bgcolor="white", paper_bgcolor="white", margin=dict(t=50, b=40))

    # Carrying cost bar
    carrying_fig = go.Figure(go.Bar(
        x=df["carrying_12pct"], y=short_names, orientation="h",
        marker_color=[COLORS["warning"] if v > 4 else COLORS["accent"] if v > 2.5 else COLORS["success"] for v in df["carrying_12pct"]],
        text=[f"{v}%" for v in df["carrying_12pct"]], textposition="outside"
    ))
    carrying_fig.update_layout(title="Carrying Cost @ 12% Rate (% of Revenue)",
                                xaxis_title="Carrying Cost %", height=420,
                                plot_bgcolor="white", paper_bgcolor="white",
                                margin=dict(t=40, b=20, l=160, r=60))

    # Output bar (corrected)
    df_sorted = df.sort_values("output_b", ascending=True)
    output_fig = go.Figure(go.Bar(
        x=df_sorted["output_b"], y=df_sorted["name"].str[:25], orientation="h",
        marker_color=COLORS["accent"],
        text=[f"${v}B" for v in df_sorted["output_b"]], textposition="outside"
    ))
    output_fig.update_layout(title="Output by Subsector ($B) — Corrected FRED/BEA Data",
                              xaxis_title="Output ($B)", height=380,
                              plot_bgcolor="white", paper_bgcolor="white",
                              margin=dict(t=40, b=20, l=200, r=80))

    # Small firm %
    df_sp = df.sort_values("small_pct", ascending=True)
    small_fig = go.Figure(go.Bar(
        x=df_sp["small_pct"], y=df_sp["name"].str[:25], orientation="h",
        marker_color=[COLORS["warning"] if v > 90 else COLORS["accent"] for v in df_sp["small_pct"]],
        text=[f"{v}%" for v in df_sp["small_pct"]], textposition="outside"
    ))
    small_fig.update_layout(title="Small Firm Concentration by Subsector (%)",
                             xaxis_title="% Small Firms (< 500 emp)", height=380,
                             plot_bgcolor="white", paper_bgcolor="white",
                             margin=dict(t=40, b=20, l=200, r=80))

    return bubble, carrying_fig, output_fig, small_fig


# ─────────────────────────────────────────────
# TAB 4: STATE OVERVIEW
# ─────────────────────────────────────────────
def layout_states():
    return dbc.Row([
        dbc.Col([dcc.Graph(id="state-firms-bar", style={"height": "420px"})], width=6),
        dbc.Col([dcc.Graph(id="state-employment-bar", style={"height": "420px"})], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Top 10 States — Key Facts", className="text-white mb-2"),
                    html.P("• California leads with 22,052 firms and 1.34M workers", style={"fontSize": "12px", "color": "white"}),
                    html.P("• Top 10 states account for ~60% of all US mfg employment", style={"fontSize": "12px", "color": "white"}),
                    html.P("• OH, MI, PA most vulnerable to Fed rate & tariff policy changes", style={"fontSize": "12px", "color": "white"}),
                    html.P("Source: IndustrySelect/MNI 2025 (Top 10); SUSB 2022", style={"fontSize": "10px", "color": "#CCC"}),
                ])
            ], style={"backgroundColor": COLORS["primary"]}, className="mt-3")
        ], width=12),
    ])


@app.callback(
    [Output("state-firms-bar", "figure"), Output("state-employment-bar", "figure")],
    Input("tabs", "active_tab")
)
def update_states(tab):
    df = state_data.sort_values("firms", ascending=True)
    firms_fig = go.Figure(go.Bar(
        x=df["firms"], y=df["state"], orientation="h",
        marker_color=COLORS["accent"],
        text=[f"{v:,}" for v in df["firms"]], textposition="outside"
    ))
    firms_fig.update_layout(title="Manufacturing Firms by State (Top 10)",
                             xaxis_title="Number of Firms", height=420,
                             plot_bgcolor="white", paper_bgcolor="white",
                             margin=dict(t=40, b=20, l=120, r=80))

    df2 = state_data.sort_values("employment", ascending=True)
    emp_fig = go.Figure(go.Bar(
        x=df2["employment"], y=df2["state"], orientation="h",
        marker_color=COLORS["primary"],
        text=[f"{v:,.0f}" for v in df2["employment"]], textposition="outside"
    ))
    emp_fig.update_layout(title="Manufacturing Employment by State (Top 10)",
                           xaxis_title="Employment", height=420,
                           plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(t=40, b=20, l=120, r=80))
    return firms_fig, emp_fig


# ─────────────────────────────────────────────
# TAB 5: INTEREST RATES
# ─────────────────────────────────────────────
def layout_rates():
    labels = list(rate_data.keys())
    values = list(rate_data.values())
    colors = [COLORS["success"] if v < 7 else COLORS["accent"] if v < 12 else COLORS["warning"] for v in values]

    rate_fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=colors,
        text=[f"{v}%" for v in values], textposition="outside"
    ))
    rate_fig.update_layout(title="US Lending Rate Landscape — February 2026 (Source: FRED)",
                            xaxis_title="Annual Interest Rate (%)", height=380,
                            xaxis=dict(range=[0, 25]),
                            plot_bgcolor="white", paper_bgcolor="white",
                            margin=dict(t=50, b=40, l=220, r=80))

    spread_fig = go.Figure()
    ccc_range = list(range(30, 270, 30))
    for label, rate in [("Small Mfg (10.25%)", 10.25), ("SBA 7(a) (11.25%)", 11.25),
                         ("AAA Large Firm (5.3%)", 5.3), ("Asset-Based (16%)", 16)]:
        spread_fig.add_trace(go.Scatter(
            x=ccc_range, y=[round(rate * c / 365, 2) for c in ccc_range],
            name=label, mode="lines+markers",
        ))
    spread_fig.update_layout(title="Carrying Cost % vs CCC — By Borrower Type",
                              xaxis_title="Cash Conversion Cycle (Days)",
                              yaxis_title="Carrying Cost (% of Revenue)",
                              height=380, plot_bgcolor="white", paper_bgcolor="white",
                              margin=dict(t=50, b=40))

    return dbc.Row([
        dbc.Col([dcc.Graph(figure=rate_fig)], width=6),
        dbc.Col([dcc.Graph(figure=spread_fig)], width=6),
        dbc.Col([
            dbc.Alert([
                html.Strong("Capital Structure Asymmetry: "),
                "A large AAA-rated firm borrows at 5.3% (FRED Jan 2026). A small manufacturer pays 10–12%. "
                "On $1M working capital for 120 days, this spread costs the small firm $12,466–$17,808 MORE "
                "than its large competitor — annually, for doing identical work. Source: FRED AAA series; Bankrate SBA rates."
            ], color="warning", className="mt-2")
        ], width=12),
    ])


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  US Manufacturing Carrying Cost Dashboard")
    print("  Techno-Economic Sensitivity Analysis — Phase 2")
    print("="*60)
    print("  Open your browser and go to: http://127.0.0.1:8050")
    print("="*60 + "\n")
    app.run(debug=True, port=8050)
