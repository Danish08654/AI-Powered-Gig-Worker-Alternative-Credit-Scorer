import streamlit as st
import requests
import plotly.graph_objects as go

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Gig Worker Credit Scorer",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Gig Worker Credit Scorer")

#  Sidebar: Applicant Input 
st.sidebar.header("Applicant Profile")

platform_tenure = st.sidebar.slider("Platform tenure (months)", 1, 72, 18)
monthly_income = st.sidebar.number_input("Avg monthly income ($)", 500, 10000, 3000, step=100)
income_std = st.sidebar.number_input("Income volatility ($)", 0, 5000, 600, step=50)
income_trend = st.sidebar.slider("Income trend", -0.3, 0.3, 0.05, step=0.01)
active_platforms = st.sidebar.slider("Active platforms", 1, 5, 2)
payment_rate = st.sidebar.slider("On-time payment rate", 0.0, 1.0, 0.85, step=0.01)
expense_ratio = st.sidebar.slider("Expense ratio", 0.1, 1.0, 0.65, step=0.01)
debt_to_income = st.sidebar.slider("Debt-to-income ratio", 0.0, 0.8, 0.25, step=0.01)
savings_buffer = st.sidebar.slider("Savings buffer (months)", 0.0, 12.0, 2.0, step=0.5)
total_history = st.sidebar.slider("Total gig history (months)", 1, 120, 24)

score_btn = st.sidebar.button("Run Credit Assessment", type="primary", use_container_width=True)

#  Main Panel 
if score_btn:
    payload = {
        "platform_tenure_months": platform_tenure,
        "monthly_income_mean": monthly_income,
        "monthly_income_std": income_std,
        "income_trend": income_trend,
        "active_platforms": active_platforms,
        "on_time_payment_rate": payment_rate,
        "expense_ratio": expense_ratio,
        "debt_to_income": debt_to_income,
        "savings_buffer_months": savings_buffer,
        "total_gig_history_months": total_history
    }

    with st.spinner("Scoring applicant..."):
        try:
            resp = requests.post(f"{API_URL}/score", json=payload)
            result = resp.json()
        except Exception as e:
            st.error(f"API connection failed: {e}")
            st.stop()

    # Decision banner
    decision = result["decision"]
    color = "green" if decision == "APPROVED" else "red"
    st.markdown(
        f"<div style='background:{color};padding:16px;border-radius:10px;"
        f"text-align:center;color:white;font-size:24px;font-weight:600'>"
        f"{decision}</div>", unsafe_allow_html=True
    )
    st.markdown("")

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Credit Score", result["credit_score"])
    col2.metric("Default Probability", f"{result['default_probability']*100:.1f}%")
    col3.metric("Risk Tier", result["risk_tier"])
    col4.metric("Applicant ID", result["applicant_id"][:8] + "...")

    st.divider()

    # Gauge chart
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Credit Score Gauge")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["credit_score"],
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [300, 850]},
                "bar": {"color": "steelblue"},
                "steps": [
                    {"range": [300, 500], "color": "#ffcccc"},
                    {"range": [500, 650], "color": "#fff3cc"},
                    {"range": [650, 750], "color": "#d4edda"},
                    {"range": [750, 850], "color": "#b8daff"},
                ],
                "threshold": {"line": {"color": "black", "width": 3}, "value": result["credit_score"]}
            }
        ))
        fig.update_layout(height=280, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("SHAP — Key Factors")

        risk = result["top_risk_factors"]
        protect = result["top_protective_factors"]

        if risk:
            st.markdown("**🔴 Top Risk Factors**")
            for item in risk:
                st.markdown(f"- `{item['feature']}` — impact: +{item['impact']}")

        if protect:
            st.markdown("**🟢 Top Protective Factors**")
            for item in protect:
                st.markdown(f"- `{item['feature']}` — impact: -{item['impact']}")
