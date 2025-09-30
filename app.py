import streamlit as st
import numpy as np
import pickle
from keras.models import load_model
from keras.preprocessing import image
import os

# -----------------------
# Load Models & Scaler
# -----------------------
@st.cache_resource
def load_models():
    keras_model, clinical_model, scaler = None, None, None

    # Load DL model
    if os.path.exists("Kidney_Disease_Model.h5"):
        keras_model = load_model("Kidney_Disease_Model.h5", compile=False)
    else:
        st.warning("DL model 'Kidney_Disease_Model.h5' not found. DL predictions will be disabled.")

    # Load ML model
    if os.path.exists("clinical_model.pkl"):
        with open("clinical_model.pkl", "rb") as f:
            clinical_model = pickle.load(f)
    else:
        st.warning("ML model 'clinical_model.pkl' not found. ML predictions will be disabled.")

    # Load scaler
    if os.path.exists("scaler.pkl"):
        with open("scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
    else:
        st.warning("Scaler 'scaler.pkl' not found. ML predictions will be disabled.")

    # Class labels (DL)
    idx_to_label = {0: "Normal", 1: "Cyst", 2: "Stone", 3: "Tumor"}

    # Class labels (ML)
    ml_idx_to_label = {
        0: "AKI",
        1: "CKD",
        2: "uti_affecting_kidney",
        3: "Kidney_Stone",
        4: "Nephrotic_Syndrome",
        5: "Renal_Tubular_Acidosis",
        6: "ESRD",
        7: "Glomerulonephritis"
    }

    return keras_model, clinical_model, scaler, idx_to_label, ml_idx_to_label


# Load models
keras_model, clinical_model, scaler, idx_to_label, ml_idx_to_label = load_models()

# -----------------------
# Recommendations
# -----------------------
recommendations = {
    "Normal": "Your kidney appears normal. Maintain a healthy lifestyle and regular check-ups.",
    "Cyst": "Kidney cyst detected. Usually benign but follow up with a nephrologist is advised.",
    "Stone": "Kidney stone detected. Consult a urologist for treatment options and hydration advice.",
    "Tumor": "Kidney tumor detected. Immediate consultation with a nephrologist/oncologist is strongly advised."
}

# -----------------------
# Disease solutions
# -----------------------
disease_solutions = {
    "AKI": "Acute Kidney Injury: Maintain hydration, consult nephrologist, avoid nephrotoxic drugs.",
    "CKD": "Chronic Kidney Disease: Low-salt diet, blood pressure control, dialysis/nephrologist care.",
    "uti_affecting_kidney": "Urinary Tract Infection: Antibiotics, hydration, avoid holding urine.",
    "Kidney_Stone": "Kidney Stone: Hydration (3-4L/day), pain management, lithotripsy if needed.",
    "Nephrotic_Syndrome": "Nephrotic Syndrome: Steroids, salt restriction, protein monitoring.",
    "Renal_Tubular_Acidosis": "RTA: Bicarbonate therapy, potassium supplements.",
    "ESRD": "End Stage Renal Disease: Regular dialysis or kidney transplant.",
    "Glomerulonephritis": "Glomerulonephritis: Immunosuppressive drugs, blood pressure control."
}

# -----------------------
# Streamlit UI
# -----------------------
st.title("🩺 Kidney Disease & Tumor Prediction System")

option = st.radio("Choose Model Type:", ["Numerical (ML)", "Image (DL)"])

# -----------------------
# ML Prediction
# -----------------------
if option == "Numerical (ML)":
    if clinical_model is None or scaler is None:
        st.info("ML model or scaler missing. Cannot make predictions.")
    else:
        st.subheader("Enter Clinical Data")

        age = st.number_input("Age", 1, 120, 30)
        bp = st.number_input("Blood Pressure", 50, 200, 80)
        sc = st.number_input("Serum Creatinine", 0.1, 15.0, 1.2)
        urea = st.number_input("Blood Urea", 5.0, 300.0, 40.0)
        sodium = st.number_input("Sodium", 100.0, 200.0, 140.0)
        potassium = st.number_input("Potassium", 2.0, 8.0, 4.5)

        features = np.array([[age, bp, sc, urea, sodium, potassium]])

        if st.button("Predict (ML)"):
            features_scaled = scaler.transform(features)
            pred_class = clinical_model.predict(features_scaled)[0]  # numeric index
            pred_label = ml_idx_to_label.get(pred_class, "Unknown")
            solution = disease_solutions.get(pred_label, "No recommendation available.")

            st.success(f"🔮 Predicted Disease: {pred_label}")
            st.info(f"💊 Suggested Solution: {solution}")

# -----------------------
# DL Prediction
# -----------------------
elif option == "Image (DL)":
    if keras_model is None:
        st.info("DL model missing. Cannot make predictions.")
    else:
        st.subheader("Upload Kidney Image")
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            if st.button("Predict (DL)"):
                input_height, input_width = keras_model.input_shape[1], keras_model.input_shape[2]

                img = image.load_img(uploaded_file, target_size=(input_height, input_width))
                img_array = image.img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                pred = keras_model.predict(img_array)
                pred_class = np.argmax(pred, axis=1)[0]
                pred_label = idx_to_label[pred_class]
                solution = recommendations.get(pred_label, "No recommendation available.")

                st.success(f"🔮 Predicted Disease: {pred_label}")
                st.info(f"💊 Suggested Solution: {solution}")
