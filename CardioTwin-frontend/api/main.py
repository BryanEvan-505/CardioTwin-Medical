"""
CardioTwin API

Prototype API layer for connecting the frontend
with CardioTwin's health, risk, and medical-care systems.

This API does not diagnose diseases.
"""

import sys
from pathlib import Path

MEDICAL_PROJECT_PATH = Path(r"C:\Users\ADMIN\CardioTwin-medical")

if str(MEDICAL_PROJECT_PATH) not in sys.path:
    sys.path.insert(0, str(MEDICAL_PROJECT_PATH))

from fastapi import FastAPI

from api.models import PatientData

from medical_care.care_interface import MedicalCareEngine


app = FastAPI(
    title="CardioTwin API",
    description="API layer for the CardioTwin healthcare prototype.",
    version="0.1.0",
)


# -------------------------
# Temporary demo storage
# -------------------------

current_patient = PatientData()


# -------------------------
# Basic endpoints
# -------------------------

@app.get("/")
def root():
    return {
        "name": "CardioTwin API",
        "status": "running",
        "is_diagnostic_system": False,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "cardiotwin-api",
    }


# -------------------------
# Dashboard
# -------------------------

@app.get("/dashboard")
def dashboard():
    measurements = current_patient.measurements

    return {
        "heart_rate": measurements.get("heart_rate"),
        "blood_pressure": {
            "systolic": measurements.get("systolic_bp"),
            "diastolic": measurements.get("diastolic_bp"),
        },
        "risk_status": "not_available",
        "digital_twin_status": "waiting_for_data",
        "alerts": [],
        "is_demo_data": current_patient.is_demo_data,
    }


# -------------------------
# Risk
# -------------------------

@app.get("/risk")
def risk():
    return {
        "risk_score": None,
        "risk_status": "not_available",
        "source": "person_1_ml_model",
        "is_prediction": False,
        "message": (
            "Cardiovascular risk prediction is not connected yet."
        ),
    }


# -------------------------
# Digital Twin
# -------------------------

@app.get("/digital-twin")
def digital_twin():
    return {
        "status": "waiting_for_data",
        "patient_profile": {},
        "health_history": [],
        "wearable_data": {},
        "lifestyle_data": {},
        "environment_data": {},
        "source": "person_2_digital_twin",
        "is_diagnosis": False,
        "message": (
            "Digital Twin data is not connected yet."
        ),
    }


# -------------------------
# Medical Care
# -------------------------

@app.get("/medical-care")
def medical_care():
    engine = MedicalCareEngine()

    return {
        "status": "connected",
        "capabilities": [
            "problem_analysis",
            "red_flag_safety",
            "injury_guidance",
            "exercise_safety",
            "diet_guidance",
            "confirmed_condition_management",
            "medication_tracking",
        ],
        "source": "person_3_medical_care",
        "is_diagnosis": False,
        "message": (
            "Medical Care Engine is connected "
            "to the CardioTwin API."
        ),
    }


# -------------------------
# Patient data
# -------------------------

@app.get("/patient")
def get_patient():
    return {
        "status": "available",
        "patient": current_patient.model_dump(),
    }


@app.post("/patient")
def create_patient(patient: PatientData):
    global current_patient

    current_patient = patient

    return {
        "status": "accepted",
        "patient": current_patient.model_dump(),
        "message": (
            "Patient data accepted and stored for "
            "the current CardioTwin demo session."
        ),
    }