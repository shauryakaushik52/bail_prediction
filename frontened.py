import streamlit as st 
import requests
 

API_URL = "http://127.0.0.1:8000/predict" 

st.title(" BAIL PREDICTION SYSTEM ")

st.image("C:\\Users\\Shaurya Kaushik\\Downloads\\indialaw.jpg" )

with st.expander("Founder Message ") :
   st.write("""

Greetings! I am Shaurya Kaushik, a B.Tech student in Computer Science and Engineering with a specialization in Artificial Intelligence. Driven by a vision to build AI solutions that solve complex, real-world problems, I constantly bridge the gap between academic theory and practical engineering. Most recently, I developed a Bail Prediction System using Scikit-Learn, which leverages machine learning to bring data-driven insights and efficiency to legal frameworks.
As I look toward the next step in my professional journey, I am actively seeking an internship opportunity where I can contribute my machine learning skills, collaborate with forward-thinking teams, and dive into impactful projects. I am eager to bring my fresh perspective, strong technical foundation, and dedication to innovation to a dynamic organization where I can learn, grow, and deliver measurable value.


""")

prior = st.selectbox("Any prior case ?" , ["Yes", "No"])
Type = st.selectbox("case type list " , ["Murder" ,"Attempt to murder","Kidnapping","Sexual offence","Fraud and cheating","Narcotics", "Domestic violence" , "Dowry" , "Theft or robbery" , "Other"])


PredictionInput = {
"prior" : prior,
"Type" : Type
      
   }
if st.button("Get Decision"):


    try:
           response = requests.post(API_URL , json= PredictionInput)

           if response.status_code == 200:
               st.write( response.json())
               api_result = response.json().get("result")

               #if api_result and "approved" in api_result.lower():
                #st.success(f"Decision:{api_result}")
               #else:
                    #st.error(f"Decision: {api_result}")


           else:
                 st.error(f"Backened Error({response.status_code}) : {response.text}") 
            


    except requests.exceptions.ConnectionError:
          st.error(f"could not connect ")