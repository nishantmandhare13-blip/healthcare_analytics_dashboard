
# Healthcare Analytics Dashboard

## Features
- Patient CSV upload
- KPI cards
- Age distribution
- Disease distribution
- BMI analysis
- Blood pressure analysis
- Gender analysis
- Interactive filters
- Responsive dark theme
- Sample data when no CSV is uploaded

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Expected CSV columns
Age, Gender, Disease, BMI, SystolicBP, DiastolicBP
