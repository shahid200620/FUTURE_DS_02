import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Churn Dashboard", layout="wide")

# ===== STYLE =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #f1f5f9);
}
.filter-box {
    background-color: #ffffff;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #cbd5f5;
    margin-bottom: 15px;
}
h1, h2, h3 {
    color: #0f172a;
}
</style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# ===== NAV =====
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", [
    "Overview",
    "Churn Drivers",
    "Retention",
    "Segments",
    "Insights"
])

st.title("📊 Customer Retention & Churn Analysis")

# ===== FILTERS (HIDE IN INSIGHTS PAGE) =====
if page != "Insights":

    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    contract = c1.multiselect("Contract", df["Contract"].unique(), df["Contract"].unique())
    internet = c2.multiselect("Internet", df["InternetService"].unique(), df["InternetService"].unique())
    gender = c3.multiselect("Gender", df["gender"].unique(), df["gender"].unique())

    st.markdown("</div>", unsafe_allow_html=True)

    df = df[(df["Contract"].isin(contract)) &
            (df["InternetService"].isin(internet)) &
            (df["gender"].isin(gender))]

# ================= OVERVIEW =================
if page == "Overview":

    c1, c2, c3 = st.columns(3)
    c1.metric("Customers", len(df))
    c2.metric("Churn %", f"{df['Churn'].mean()*100:.2f}")
    c3.metric("Avg Tenure", f"{df['tenure'].mean():.1f}")

    col1, col2 = st.columns(2)

    churn = df["Churn"].value_counts().reset_index()
    churn.columns = ["Churn", "Count"]

    col1.plotly_chart(px.pie(churn, names="Churn", values="Count", hole=0.4), use_container_width=True)

    contract_data = df.groupby("Contract")["Churn"].mean().reset_index()
    col2.plotly_chart(px.bar(contract_data, x="Contract", y="Churn"), use_container_width=True)

    st.dataframe(df.head(10))

# ================= CHURN DRIVERS =================
elif page == "Churn Drivers":

    col1, col2 = st.columns(2)

    internet = df.groupby("InternetService")["Churn"].mean().reset_index()
    col1.plotly_chart(px.bar(internet, x="InternetService", y="Churn"), use_container_width=True)

    payment = df.groupby("PaymentMethod")["Churn"].mean().reset_index()
    col2.plotly_chart(px.bar(payment, x="PaymentMethod", y="Churn"), use_container_width=True)

    col3, col4 = st.columns(2)

    col3.plotly_chart(px.box(df, x="Churn", y="MonthlyCharges"), use_container_width=True)

    col4.plotly_chart(px.histogram(df, x="tenure", color="Churn"), use_container_width=True)

# ================= RETENTION =================
elif page == "Retention":

    col1, col2 = st.columns(2)

    tenure = df.groupby("tenure")["Churn"].mean().reset_index()
    col1.plotly_chart(px.line(tenure, x="tenure", y="Churn"), use_container_width=True)

    charges = df.groupby("tenure")["MonthlyCharges"].mean().reset_index()
    col2.plotly_chart(px.line(charges, x="tenure", y="MonthlyCharges"), use_container_width=True)

    col3, col4 = st.columns(2)

    col3.plotly_chart(px.histogram(df, x="tenure"), use_container_width=True)

    churn_rate = df.groupby("tenure")["Churn"].mean().reset_index()
    col4.plotly_chart(px.area(churn_rate, x="tenure", y="Churn"), use_container_width=True)

    st.dataframe(tenure.head(20))

# ================= SEGMENTS =================
elif page == "Segments":

    col1, col2 = st.columns(2)

    gender = df.groupby("gender")["Churn"].mean().reset_index()
    col1.plotly_chart(px.bar(gender, x="gender", y="Churn"), use_container_width=True)

    senior = df.groupby("SeniorCitizen")["Churn"].mean().reset_index()
    col2.plotly_chart(px.bar(senior, x="SeniorCitizen", y="Churn"), use_container_width=True)

    col3, col4 = st.columns(2)

    partner = df.groupby("Partner")["Churn"].mean().reset_index()
    col3.plotly_chart(px.pie(partner, names="Partner", values="Churn"), use_container_width=True)

    depend = df.groupby("Dependents")["Churn"].mean().reset_index()
    col4.plotly_chart(px.bar(depend, x="Dependents", y="Churn"), use_container_width=True)

# ================= INSIGHTS =================
elif page == "Insights":

    st.markdown("""
    ## 🔥 Strategic Business Insights

    ### 📉 Critical Churn Drivers
    - Customers on **month-to-month contracts exhibit significantly higher churn**, indicating low commitment and higher volatility.
    - **High monthly charges strongly correlate with churn**, suggesting pricing sensitivity and perceived value gaps.
    - **Low tenure customers (0–12 months)** represent the most vulnerable segment, highlighting onboarding issues.

    ### 📊 Behavioral Patterns
    - Customers using **fiber optic services show elevated churn**, possibly due to pricing or service expectations.
    - Users without long-term engagement (contracts/loyalty) are **more likely to disengage early**.

    ### 🚀 High-Impact Recommendations
    - Introduce **long-term contract incentives** to increase customer commitment.
    - Implement **targeted retention campaigns** for high-risk segments.
    - Optimize pricing strategies for **high-charge users** to improve satisfaction.
    - Strengthen onboarding experience to **reduce early-stage churn**.

    ### 💡 Business Impact
    Reducing churn by even **5–10% can significantly boost revenue and customer lifetime value**, making retention strategies a key growth driver.
    """)