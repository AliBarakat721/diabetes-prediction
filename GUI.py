import pickle
import streamlit as st
import pandas as pd 

# Load the saved model
model = pickle.load(open("diabetes_prediction.sav", "rb"))

# App Title
st.title("🔍 Diabetes Prediction Web App")
st.info("An easy application for predicting diabetes disease.")


# 📌 **Introduction to Diabetes**
st.header("🩺 What is Diabetes?")
st.write("""
**Diabetes** is a chronic disease that occurs when **blood sugar (glucose) levels are too high**.  
It happens when the body **does not produce enough insulin** or **cannot use insulin effectively**.
""")

with st.expander("📌 **Types of Diabetes**"):
    st.write("""
    🔹 **Type 1 Diabetes**: An autoimmune condition where the immune system attacks insulin-producing cells.  
    🔹 **Type 2 Diabetes**: The most common type, occurring when the body becomes resistant to insulin.  
    🔹 **Gestational Diabetes**: Develops during pregnancy and may disappear after childbirth.
    """)

with st.expander("⚠️ **Risk Factors for Diabetes**"):
    st.write("""
    - 📈 **Obesity and overweight**  
    - 🛑 **Lack of physical activity**  
    - 🧬 **Family history of diabetes**  
    - 🍟 **Unhealthy diet**  
    - 🔄 **High blood pressure or cholesterol**  
    """)

with st.expander("💡 **Tips for Diabetes Prevention & Management**"):
    st.write("""
    ✅ **Eat a healthy diet** rich in vegetables and fruits  
    ✅ **Exercise regularly** (e.g., walking, jogging)  
    ✅ **Reduce sugar and processed food intake**  
    ✅ **Maintain a healthy weight** to lower risk  
    ✅ **Get regular check-ups** to monitor blood sugar levels  
    """)


# 📌 **User Instructions**
st.warning("ℹ️ **To check your diabetes risk, enter your details in the left sidebar.**")
st.write("👉 **Click the small arrow** (`>` in the top-left corner) to open the **sidebar** and input your details.")

# Sidebar for User Input
st.sidebar.header("🔍 **Enter Your Information**")
st.sidebar.write("📌 **Fill in your details below to predict diabetes risk.**")

# Feature Names and Descriptions
features = ['Pregnancies', 'Glucose', 'BloodPressure', 
            'SkinThickness', 'Insulin', 'BMI', 
            'DiabetesPedigreeFunction', 'Age']

feature_descriptions = {
    "Pregnancies": "👶 **Number of times pregnant**.",
    "Glucose": "🍬 **Blood glucose level (mg/dL)**.",
    "BloodPressure": "💉 **Blood pressure (mm Hg)**.",
    "SkinThickness": "🩸 **Skin thickness (mm)**.",
    "Insulin": "🧪 **Insulin level (mu U/ml)**.",
    "BMI": "⚖️ **Body Mass Index (kg/m²)**.",
    "DiabetesPedigreeFunction": "📊 **Diabetes pedigree function** (family history factor).",
    "Age": "🎂 **Age (years)**."
}

# User Input Fields
user_input = []
for feature in features:
    st.sidebar.markdown(feature_descriptions[feature])
    if feature in ["Pregnancies", "Age"]:
        value = st.sidebar.number_input(f"🔹 {feature}", min_value=0, step=1, format="%d", key=feature)
    else:
        value = st.sidebar.number_input(f"🔹 {feature}", min_value=0.0, step=0.1, key=feature)
    user_input.append(value)

# Convert input into a DataFrame
user_df = pd.DataFrame([user_input], columns=features)

# ✅ Avoid showing warnings on app startup
if any(user_input):
    invalid_inputs = []
    if user_df["Glucose"].iloc[0] == 0:
        invalid_inputs.append("Glucose level cannot be 0")
    if user_df["BloodPressure"].iloc[0] == 0:
        invalid_inputs.append("Blood Pressure should be greater than 0")
    if user_df["SkinThickness"].iloc[0] == 0:
        invalid_inputs.append("Skin Thickness cannot be 0")
    if user_df["Insulin"].iloc[0] == 0:
        invalid_inputs.append("Insulin level should be greater than 0")
    if user_df["BMI"].iloc[0] == 0:
        invalid_inputs.append("BMI cannot be 0")

    for warning in invalid_inputs:
        st.warning(f"⚠️ {warning}")

# 🔮 **Diabetes Prediction**
if st.button("🔍 **Predict**"):
    if all(value == 0 for value in user_input):
        st.error("❌ **Please enter valid values before making a prediction.**")
    else:
        try:
            prediction = model.predict(user_df)
            if prediction[0] == 1:
                st.error("⚠️ **The model predicts that the person has diabetes.**")
                st.image(r"C:\Users\ELKHOLEI\Desktop\Project of ML\diabetes_Prediction\diabetes person.png", width=700)
            else:
                st.success("✅ **The model predicts that the person is healthy.**")
                st.image(r"C:\Users\ELKHOLEI\Desktop\Project of ML\diabetes_Prediction\health-day.png", width=700)
        except Exception as e:
            st.error(f"❌ **An error occurred:** {e}")
