"""
CardioTwin Frontend

Streamlit dashboard for the CardioTwin healthcare prototype.
"""

import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="CardioTwin",
    page_icon="❤️",
    layout="wide",
)


def get_api_health():
    """Check whether the CardioTwin API is available."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=3,
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.RequestException:
        return None


def get_dashboard_data():
    """Fetch dashboard data from the CardioTwin API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/dashboard",
            timeout=3,
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.RequestException:
        return None


def get_patient_data():
    """Fetch the current patient data from the API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/patient",
            timeout=3,
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.RequestException:
        return None


# -------------------------
# Load API data
# -------------------------

api_health = get_api_health()
dashboard_data = get_dashboard_data()
patient_response = get_patient_data()


# -------------------------
# Page header
# -------------------------

st.title("❤️ CardioTwin")
st.subheader("Your Cardiovascular Digital Twin")

st.info(
    "Prototype only — CardioTwin is not a diagnostic system "
    "and does not replace professional medical care."
)


# -------------------------
# Backend status
# -------------------------

if api_health:
    st.success("🟢 CardioTwin API connected")
else:
    st.error("🔴 CardioTwin API is not available")


# -------------------------
# Sidebar
# -------------------------

st.sidebar.title("CardioTwin")

if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Digital Twin",
        "Risk Prediction",
        "Medical Care",
        "Medications",
        "Alerts",
        "Environment",
    ],
)


# -------------------------
# Dashboard
# -------------------------

if page == "Dashboard":
    heart_rate = dashboard_data.get("heart_rate")

blood_pressure = dashboard_data.get(
    "blood_pressure",
    {},
)

systolic = blood_pressure.get("systolic")
diastolic = blood_pressure.get("diastolic")


# Use patient measurements when dashboard measurements
# are not available yet.
if patient_response is not None:
    patient = patient_response.get(
        "patient",
        {},
    )

    patient_measurements = patient.get(
        "measurements",
        {},
    )

    if systolic is None:
        systolic = patient_measurements.get(
            "systolic_bp"
        )

    if diastolic is None:
        diastolic = patient_measurements.get(
            "diastolic_bp"
        )

    if heart_rate is None:
        heart_rate = patient_measurements.get(
            "heart_rate"
        )

    risk_status = dashboard_data.get(
        "risk_status",
        "not_available",
    )

    twin_status = dashboard_data.get(
        "digital_twin_status",
        "waiting_for_data",
    )

    alerts = dashboard_data.get(
        "alerts",
        [],
    )

    # -------------------------
    # Main health metrics
    # -------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if heart_rate is None:
            st.metric("Heart Rate", "Not available")
        else:
            st.metric(
                "Heart Rate",
                f"{heart_rate} bpm",
            )

    with col2:
        if systolic is None or diastolic is None:
            st.metric("Blood Pressure", "Not available")
        else:
            st.metric(
                "Blood Pressure",
                f"{systolic}/{diastolic}",
            )

    with col3:
        st.metric(
            "Risk Status",
            risk_status.replace(
                "_",
                " ",
            ).title(),
        )

    with col4:
        st.metric(
            "Twin Status",
            twin_status.replace(
                "_",
                " ",
            ).title(),
        )

    st.divider()

    # -------------------------
    # Patient information
    # -------------------------

    st.subheader("👤 Current Patient Data")

    if patient_response is None:
        st.warning(
            "Patient data could not be loaded."
        )

    else:
        patient = patient_response.get(
            "patient",
            {},
        )

        profile = patient.get(
            "profile",
            {},
        )

        symptoms = patient.get(
            "symptoms",
            [],
        )

        measurements = patient.get(
            "measurements",
            {},
        )

        lifestyle = patient.get(
            "lifestyle",
            {},
        )

        environment = patient.get(
            "environment",
            {},
        )

        patient_id = patient.get(
            "patient_id",
            "Unknown",
        )

        st.caption(
            f"Patient ID: {patient_id}"
        )

        if patient.get("is_demo_data"):
            st.warning(
                "This is synthetic demo data. "
                "It is not a real patient's medical record."
            )

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Profile")

            if profile:
                st.json(profile)
            else:
                st.info(
                    "No profile data available."
                )

            st.write("### Symptoms")

            if symptoms:
                for symptom in symptoms:
                    st.write(f"• {symptom}")
            else:
                st.info(
                    "No symptoms recorded."
                )

        with col2:
            st.write("### Measurements")

            if measurements:
                st.json(measurements)
            else:
                st.info(
                    "No measurements available."
                )

            st.write("### Lifestyle")

            if lifestyle:
                st.json(lifestyle)
            else:
                st.info(
                    "No lifestyle data available."
                )

        st.write("### Environment")

        if environment:
            st.json(environment)
        else:
            st.info(
                "No environment data available."
            )

    st.divider()

    # -------------------------
    # Today's overview
    # -------------------------

    st.subheader("Today's Overview")

    left, right = st.columns(2)

    with left:
        st.write("### ❤️ Cardiovascular Status")

        if (
            heart_rate is None
            and systolic is None
            and diastolic is None
        ):
            st.write(
                "No cardiovascular measurements "
                "are connected to the dashboard yet."
            )
        else:
            st.write(
                "Measurements are available from "
                "the CardioTwin API."
            )

    with right:
        st.write("### 🚨 Alerts")

        if alerts:
            for alert in alerts:
                st.warning(str(alert))
        else:
            st.write("No alerts available.")


# -------------------------
# Digital Twin
# -------------------------

elif page == "Digital Twin":
    st.header("🧬 My Digital Twin")

    try:
        response = requests.get(
            f"{API_BASE_URL}/digital-twin",
            timeout=3,
        )

        if response.status_code == 200:
            twin_data = response.json()

            st.success(
                "🟢 Digital Twin API connected"
            )

            twin_status = twin_data.get(
                "status",
                "waiting_for_data",
            )

            st.metric(
                "Twin Status",
                twin_status.replace(
                    "_",
                    " ",
                ).title(),
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.write("### 👤 Patient Profile")

                profile = twin_data.get(
                    "patient_profile",
                    {},
                )

                if profile:
                    st.json(profile)
                else:
                    st.info(
                        "Patient profile data is not "
                        "connected yet."
                    )

                st.write("### ❤️ Health History")

                history = twin_data.get(
                    "health_history",
                    [],
                )

                if history:
                    st.json(history)
                else:
                    st.info(
                        "Health history is not "
                        "connected yet."
                    )

            with col2:
                st.write("### ⌚ Wearable Data")

                wearable = twin_data.get(
                    "wearable_data",
                    {},
                )

                if wearable:
                    st.json(wearable)
                else:
                    st.info(
                        "Wearable data is not "
                        "connected yet."
                    )

                st.write("### 🌤️ Environment Data")

                environment = twin_data.get(
                    "environment_data",
                    {},
                )

                if environment:
                    st.json(environment)
                else:
                    st.info(
                        "Environment data is not "
                        "connected yet."
                    )

            st.write("### 🏃 Lifestyle Data")

            lifestyle = twin_data.get(
                "lifestyle_data",
                {},
            )

            if lifestyle:
                st.json(lifestyle)
            else:
                st.info(
                    "Lifestyle data is not "
                    "connected yet."
                )

        else:
            st.error(
                "Digital Twin API returned an error."
            )

    except requests.RequestException:
        st.error(
            "🔴 Digital Twin API is not available."
        )


# -------------------------
# Risk Prediction
# -------------------------

elif page == "Risk Prediction":
    st.header("📊 Cardiovascular Risk")

    try:
        response = requests.get(
            f"{API_BASE_URL}/risk",
            timeout=3,
        )

        if response.status_code == 200:
            risk_data = response.json()

            st.success(
                "🟢 Risk Prediction API connected"
            )

            risk_status = risk_data.get(
                "risk_status",
                "not_available",
            )

            risk_score = risk_data.get(
                "risk_score",
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Risk Status",
                    risk_status.replace(
                        "_",
                        " ",
                    ).title(),
                )

            with col2:
                if risk_score is None:
                    st.metric(
                        "Risk Score",
                        "Not available",
                    )
                else:
                    st.metric(
                        "Risk Score",
                        f"{risk_score}%",
                    )

            st.divider()

            st.info(
                risk_data.get(
                    "message",
                    "Risk prediction is not available.",
                )
            )

            st.caption(
                "Risk prediction will be provided by "
                "Person 1's cardiovascular ML system."
            )

        else:
            st.error(
                "Risk Prediction API returned an error."
            )

    except requests.RequestException:
        st.error(
            "🔴 Risk Prediction API is not available."
        )


# -------------------------
# Medical Care
# -------------------------

elif page == "Medical Care":
    st.header("🩺 Medical Care")

    try:
        response = requests.get(
            f"{API_BASE_URL}/medical-care",
            timeout=3,
        )

        if response.status_code == 200:
            medical_data = response.json()

            st.success(
                "🟢 Medical Care API connected"
            )

            st.write(
                "### Available Medical Care Features"
            )

            capabilities = medical_data.get(
                "capabilities",
                [],
            )

            for capability in capabilities:
                st.write(
                    f"• {capability.replace('_', ' ').title()}"
                )

            st.divider()

            st.info(
                medical_data.get(
                    "message",
                    "Medical Care data is not available.",
                )
            )

        else:
            st.error(
                "Medical Care API returned an error."
            )

    except requests.RequestException:
        st.error(
            "🔴 Medical Care API is not available."
        )


# -------------------------
# Medications
# -------------------------

elif page == "Medications":
    st.header("💊 Medications")

    st.write(
        "Doctor/user-entered medication records "
        "will appear here."
    )

    st.info(
        "Medication records are not connected yet."
    )


# -------------------------
# Alerts
# -------------------------

elif page == "Alerts":
    st.header("🚨 Health Alerts")

    if dashboard_data:
        alerts = dashboard_data.get(
            "alerts",
            [],
        )

        if alerts:
            for alert in alerts:
                st.warning(str(alert))
        else:
            st.success("No active alerts.")

    else:
        st.error(
            "Alert data could not be loaded."
        )


# -------------------------
# Environment
# -------------------------

elif page == "Environment":
    st.header("🌤️ Environment")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Air Quality",
            "Not available",
        )

    with col2:
        st.metric(
            "Temperature",
            "Not available",
        )

    with col3:
        st.metric(
            "Humidity",
            "Not available",
        )

    st.info(
        "Environmental data will be connected later."
    )