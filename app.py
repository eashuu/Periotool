import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_risk_category(value, thresholds):
    """Assign risk level based on thresholds"""
    if value < thresholds[0]:
        return 1  # Low risk
    elif value < thresholds[1]:
        return 2  # Moderate risk
    else:
        return 3  # High risk

# Streamlit UI
st.title("Periodontal Risk Assessment (PRA)")

st.sidebar.header("Enter Your Parameters")

# User Inputs
bop = st.sidebar.slider("Bleeding on Probing (%)", 0, 100, 10)
residual_pockets = st.sidebar.slider("Residual Pockets (≥5mm)", 0, 15, 4)
teeth_lost = st.sidebar.slider("Teeth Lost (out of 28)", 0, 15, 2)
bl_age = st.sidebar.slider("Bone Loss / Age Factor", 0.0, 2.0, 0.5, 0.05)
systemic_risk = st.sidebar.selectbox("Systemic & Genetic Risk (e.g., Diabetes, IL-1)", ["None", "Present"])
smoking = st.sidebar.selectbox("Smoking Habits", ["Non-Smoker", "Former Smoker (>5 years)", "<10 Cigarettes/Day", "10-19 Cigarettes/Day", "≥20 Cigarettes/Day"])

# Define thresholds for risk categorization
bop_thresholds = [10, 25]
pockets_thresholds = [4, 8]
teeth_loss_thresholds = [4, 8]
bl_age_thresholds = [0.5, 1.0]

# Compute risk scores
bop_risk = calculate_risk_category(bop, bop_thresholds)
pockets_risk = calculate_risk_category(residual_pockets, pockets_thresholds)
teeth_loss_risk = calculate_risk_category(teeth_lost, teeth_loss_thresholds)
bl_age_risk = calculate_risk_category(bl_age, bl_age_thresholds)

# Systemic & Smoking Risk
systemic_risk_value = 3 if systemic_risk == "Present" else 1
smoking_risk_values = {"Non-Smoker": 1, "Former Smoker (>5 years)": 1, "<10 Cigarettes/Day": 2, "10-19 Cigarettes/Day": 2, "≥20 Cigarettes/Day": 3}
smoking_risk = smoking_risk_values[smoking]

# Aggregate Risk Scores
risk_scores = [bop_risk, pockets_risk, teeth_loss_risk, bl_age_risk, systemic_risk_value, smoking_risk]
labels = ["BOP", "Residual Pockets", "Tooth Loss", "Bone Loss/Age", "Systemic Risk", "Smoking"]

# Determine overall risk level
high_risk_count = sum(1 for r in risk_scores if r == 3)
moderate_risk_count = sum(1 for r in risk_scores if r == 2)
if high_risk_count >= 2:
    overall_risk = "High Risk"
elif moderate_risk_count >= 2:
    overall_risk = "Moderate Risk"
else:
    overall_risk = "Low Risk"

# Radar Chart
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
risk_scores += risk_scores[:1]
angles += angles[:1]
ax.fill(angles, risk_scores, 'b', alpha=0.3)
ax.plot(angles, risk_scores, 'b', linewidth=2)
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["Low", "Moderate", "High"])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_title(f"Periodontal Risk Assessment: {overall_risk}")

st.pyplot(fig)
st.write(f"### Overall Risk Category: {overall_risk}")
