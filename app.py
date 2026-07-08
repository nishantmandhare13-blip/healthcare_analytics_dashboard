
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Healthcare Analytics Dashboard",layout="wide")

st.markdown("""
<style>
.stApp {background:#0f172a;color:white;}
div[data-testid="stMetric"]{background:#1e293b;padding:12px;border-radius:10px;}
</style>
""",unsafe_allow_html=True)

st.title("🏥 Healthcare Analytics Dashboard")
st.caption("Upload patient CSV to explore healthcare metrics.")

with st.sidebar:
    st.header("Upload")
    file=st.file_uploader("Patient CSV",type="csv")
    st.markdown("Expected columns: Age, Gender, Disease, BMI, SystolicBP, DiastolicBP")

if file:
    df=pd.read_csv(file)
else:
    np.random.seed(42)
    diseases=["Diabetes","Hypertension","Asthma","Heart Disease","Flu","Healthy"]
    genders=["Male","Female","Other"]
    df=pd.DataFrame({
        "Age":np.random.randint(18,90,300),
        "Gender":np.random.choice(genders,300,p=[0.48,0.48,0.04]),
        "Disease":np.random.choice(diseases,300),
        "BMI":np.round(np.random.normal(26,4,300),1),
        "SystolicBP":np.random.randint(95,180,300),
        "DiastolicBP":np.random.randint(60,110,300)
    })

st.sidebar.header("Filters")
g=st.sidebar.multiselect("Gender",df["Gender"].unique(),default=list(df["Gender"].unique()))
d=st.sidebar.multiselect("Disease",df["Disease"].unique(),default=list(df["Disease"].unique()))
age=st.sidebar.slider("Age",int(df.Age.min()),int(df.Age.max()),(int(df.Age.min()),int(df.Age.max())))
f=df[df.Gender.isin(g)&df.Disease.isin(d)&df.Age.between(age[0],age[1])]

c1,c2,c3,c4,c5=st.columns(5)
c1.metric("Patients",len(f))
c2.metric("Avg Age",round(f.Age.mean(),1))
c3.metric("Avg BMI",round(f.BMI.mean(),1))
c4.metric("Avg Sys BP",round(f.SystolicBP.mean(),1))
c5.metric("Avg Dia BP",round(f.DiastolicBP.mean(),1))

r1c1,r1c2=st.columns(2)
with r1c1:
    st.plotly_chart(px.histogram(f,x="Age",nbins=15,title="Age Distribution",
                                 template="plotly_dark"),use_container_width=True)
with r1c2:
    st.plotly_chart(px.pie(f,names="Gender",title="Gender Distribution",
                           template="plotly_dark"),use_container_width=True)

r2c1,r2c2=st.columns(2)
with r2c1:
    st.plotly_chart(px.bar(f["Disease"].value_counts().reset_index(),
                           x="Disease",y="count",
                           title="Disease Distribution",
                           template="plotly_dark"),
                    use_container_width=True)
with r2c2:
    st.plotly_chart(px.histogram(f,x="BMI",color="Gender",title="BMI Analysis",
                                 template="plotly_dark"),use_container_width=True)

r3c1,r3c2=st.columns(2)
with r3c1:
    st.plotly_chart(px.scatter(f,x="SystolicBP",y="DiastolicBP",
                               color="Disease",size="BMI",
                               title="Blood Pressure Analysis",
                               template="plotly_dark"),
                    use_container_width=True)
with r3c2:
    bins=[0,18.5,25,30,100]
    labels=["Underweight","Normal","Overweight","Obese"]
    tmp=f.copy()
    tmp["BMI Category"]=pd.cut(tmp["BMI"],bins=bins,labels=labels)
    st.plotly_chart(px.bar(tmp["BMI Category"].value_counts().reset_index(),
                           x="BMI Category",y="count",
                           title="BMI Categories",
                           template="plotly_dark"),
                    use_container_width=True)

with st.expander("Patient Data"):
    st.dataframe(f,use_container_width=True)
