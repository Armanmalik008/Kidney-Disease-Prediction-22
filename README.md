<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Kidney Disease Prediction System — README</title>
  <style>
    :root{
      --bg:#0f1724;
      --card:#0b1220;
      --accent:#06b6d4;
      --muted:#94a3b8;
      --text:#e6eef6;
      --glass: rgba(255,255,255,0.03);
      --maxw: 1100px;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    html,body{height:100%; margin:0; background:linear-gradient(180deg,#071124 0%, #071827 100%); color:var(--text);}
    .wrap{max-width:var(--maxw); margin:36px auto; padding:28px; background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border-radius:12px; box-shadow:0 6px 30px rgba(2,6,23,0.6); border:1px solid rgba(255,255,255,0.03);}
    h1{font-size:28px; margin:0 0 6px; color:#fff}
    h2{font-size:18px; margin-top:22px; color:var(--accent);}
    p{color:var(--muted); line-height:1.6;}
    pre{background:var(--card); padding:14px; border-radius:8px; overflow:auto; color:#dbeafe; font-size:13px; line-height:1.45; border:1px solid rgba(255,255,255,0.02)}
    code{background:rgba(255,255,255,0.02); padding:2px 6px; border-radius:6px; color:#a7f3d0;}
    ul{color:var(--muted)}
    .badge{display:inline-block; padding:6px 10px; border-radius:999px; background:linear-gradient(90deg,var(--accent),#7c3aed); color:#021124; font-weight:600; margin-right:8px;}
    .grid{display:grid; grid-template-columns: 1fr 1fr; gap:18px;}
    .card{background:var(--glass); padding:14px; border-radius:10px; border:1px solid rgba(255,255,255,0.02);}
    .muted{color:var(--muted); font-size:14px}
    .note{background:#052333; padding:10px; border-radius:8px; color:#bfe6ef; border:1px solid rgba(255,255,255,0.02)}
    a.link{color:var(--accent); text-decoration:none}
    @media(max-width:900px){ .grid{grid-template-columns:1fr} }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>🩺 Kidney Disease Prediction System</h1>
    <p class="muted">Dual-model system (ML + CNN) for predicting kidney diseases from clinical data and kidney images — with suggested solutions. This HTML README is a developer-friendly guide to run, extend and deploy the project.</p>

    <h2>📌 Features</h2>
    <ul>
      <li>✅ <strong>Dual models</strong>: ML model for clinical/numerical data, CNN for image-based predictions.</li>
      <li>✅ <strong>Recommendations</strong>: Predefined treatment / next-step suggestions for predictions.</li>
      <li>✅ <strong>Streamlit web UI</strong> for easy demo and testing.</li>
      <li>✅ <strong>Resilient</strong>: App handles missing files gracefully (warnings + disabled features).</li>
    </ul>

    <h2>📂 Project Structure</h2>
    <pre>
Kidney-Disease-Prediction/
│
├── app.py                     # Streamlit app (ML + DL prediction system)
├── clinical_model.pkl         # Trained ML model (scikit-learn)
├── scaler.pkl                 # Scaler used for preprocessing ML features
├── Kidney_Disease_Model.h5    # Trained CNN (Keras/TensorFlow)
├── README.md                  # Documentation (this file / HTML)
└── requirements.txt           # Python dependencies
    </pre>

    <h2>⚙️ Installation</h2>
    <p class="muted">Run locally in a virtual environment (recommended):</p>
    <pre>
git clone https://github.com/your-username/Kidney-Disease-Prediction.git
cd Kidney-Disease-Prediction

python -m venv venv
# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

pip install -r requirements.txt
    </pre>

    <p class="muted">Example <code>requirements.txt</code>:</p>
    <pre>
streamlit
numpy
pandas
scikit-learn
tensorflow
keras
Pillow
    </pre>

    <h2>🚀 Run the App</h2>
    <pre>
streamlit run app.py
# open http://localhost:8501 in your browser
    </pre>

    <h2>📊 ML Prediction (Clinical Data)</h2>
    <p class="muted">The ML model expects these input features (example order):</p>
    <ul>
      <li>Age</li>
      <li>Blood Pressure</li>
      <li>Serum Creatinine</li>
      <li>Blood Urea</li>
      <li>Sodium</li>
      <li>Potassium</li>
    </ul>

    <h2>🖼️ CNN Prediction (Image Data)</h2>
    <p class="muted">Upload a CT/MRI kidney image. The app automatically reads the model input shape and resizes the image to the expected size to avoid Flatten/Dense mismatch errors.</p>
    <p class="muted">Typical CNN architecture used during development:</p>

    <pre>
model = Sequential([
  Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
  MaxPooling2D(2,2),

  Conv2D(64, (3,3), activation='relu'),
  MaxPooling2D(2,2),

  Conv2D(128, (3,3), activation='relu'),
  MaxPooling2D(2,2),

  Flatten(),
  Dense(128, activation='relu'),
  Dropout(0.5),
  Dense(5, activation='softmax')  # classes: Normal, Cyst, Stone, Tumor, Healthy
])
    </pre>

    <h2>💊 Disease Solutions (example)</h2>
    <p class="muted">A sample mapping from model labels to textual suggestions:</p>
    <pre>
disease_solutions = {
  "AKI": "Acute Kidney Injury: Hydration maintain karo, nephrologist consult karo, avoid nephrotoxic drugs.",
  "CKD": "Chronic Kidney Disease: Low-salt diet, blood pressure control, dialysis/join nephrologist plan.",
  "uti_affecting_kidney": "Urinary Tract Infection: Antibiotics course, hydration, avoid holding urine.",
  "Kidney_Stone": "Kidney Stone: Hydration (3-4L/day), pain management, lithotripsy if needed.",
  "Nephrotic_Syndrome": "Nephrotic Syndrome: Steroids, salt restriction, protein monitoring.",
  "Renal_Tubular_Acidosis": "RTA: Bicarbonate therapy, potassium supplements.",
  "ESRD": "End Stage Renal Disease: Regular dialysis or kidney transplant.",
  "Glomerulonephritis": "Glomerulonephritis: Immunosuppressive drugs, blood pressure control."
}
    </pre>

    <h2>🔧 Important Implementation Notes</h2>
    <div class="card">
      <p class="muted"><strong>1) ML model outputs:</strong> If your ML model returns string labels (e.g. <code>"uti_affecting_kidney"</code>), do <em>not</em> cast predictions to <code>int</code>. Use the returned string to lookup solutions.</p>

      <p class="muted"><strong>2) DL input-shape mismatch:</strong> Always resize uploaded images to the model's input shape using <code>model.input_shape</code>. Example:</p>
      <pre>
# detect input size automatically
h, w = model.input_shape[1], model.input_shape[2]
img = image.load_img(uploaded_file, target_size=(h, w))
      </pre>

      <p class="muted"><strong>3) Unknown classes:</strong> If the model predicts a class not present in your label dictionary, handle it gracefully:
      <pre>
label = class_map.get(pred_idx, f"Unknown Class ({pred_idx})")
      </pre>
      </p>
    </div>

    <h2>📌 Example ML prediction snippet (Streamlit)</h2>
    <pre>
# assume clinical_model & scaler are loaded
features_scaled = scaler.transform(features)
pred_label = clinical_model.predict(features_scaled)[0]   # string label
solution = disease_solutions.get(pred_label, "No recommendation available.")
st.success(f"🔮 Predicted Disease: {pred_label}")
st.info(f"💊 Suggested Solution: {solution}")
    </pre>

    <h2>🛠️ Troubleshooting</h2>
    <ul>
      <li><strong>FileNotFoundError: scaler.pkl / clinical_model.pkl / Kidney_Disease_Model.h5</strong> — make sure these files are in the project root or update file paths in <code>app.py</code>.</li>
      <li><strong>ValueError about Flatten/Dense mismatch</strong> — the fix is to resize images to the model's expected input shape.</li>
      <li><strong>KeyError / Unknown Class</strong> — ensure your label mapping matches the model's outputs (strings or indices exactly).</li>
    </ul>

    <h2>🏥 Example workflow</h2>
    <ol>
      <li>User enters numeric clinical data → ML model predicts e.g. <code>uti_affecting_kidney</code> → app displays solution.</li>
      <li>User uploads CT image → CNN predicts e.g. <code>Tumor</code> → app displays recommendation to consult specialist.</li>
    </ol>

    <h2>📈 Future Improvements</h2>
    <ul>
      <li>Multi-modal fusion (combine image + clinical features) for more accurate predictions.</li>
      <li>Model explainability (Grad-CAM for CNN, SHAP for ML model).</li>
      <li>Cloud deployment (Streamlit Cloud, AWS/GCP) with secure storage for uploaded images.</li>
    </ul>

    <h2>👨‍💻 Author</h2>
    <p class="muted">Developed by <strong>Arman</strong>. For questions or collaboration — add your contact details here.</p>

    <div class="note">
      <strong>Disclaimer:</strong> This project is for research and educational purposes only. It is <em>not</em> medical advice. Always consult qualified healthcare professionals.
    </div>

    <p style="margin-top:18px; color:var(--muted)">Saved this file? Great — open it in your browser or use the VSCode HTML preview to see the formatted README. If you want a printable / PDF version, I can generate a ready-to-download PDF for you next.</p>
  </div>
</body>
</html>
#   K i d n e y - D i s e a s e - P r e d i c t i o n  
 