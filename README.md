An end-to-end ML system that scores gig workers for credit eligibility using non-traditional financial signals income patterns,
platform tenure, payment behaviour with full SHAP explainability and a live API.

What It Does

1) Scores a gig worker's default risk using 14 engineered financial features
2) Returns a 300–850 credit score, a risk tier, and a loan decision
3) Explains every decision with SHAP — listing exact risk and protective factors
4) Serves predictions via a FastAPI REST endpoint
5) Visualises results on a Streamlit dashboard with a live gauge chart

1) Start the API 

1.1 cd api

1.2 pip install -r requirements.txt

1.3 uvicorn main:app --reload

2) Start the dashboard

2.1 cd frontend

2.2 pip install streamlit plotly requests

2.3 streamlit run app.py

Model Performance

MetricValue

ROC-AUC

~0.84

EvaluationStratified 80/20

splitImbalance 

handlingscale_pos_weight

StoppingEarly stopping (50 rounds)

What I Learned

1) End-to-end ML pipeline from raw data to deployed API
   
2) Feature engineering for financial signals
   
3) Class imbalance handling with scale_pos_weight
   
4) SHAP global and local explainability
   
5) FastAPI schema-first API design with Pydantic
   
6) Training/serving consistency — avoiding skew
   
7) Model serialisation and metadata management
   
8) Streamlit dashboard with live API integration
