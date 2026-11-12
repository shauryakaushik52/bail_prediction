import joblib
from fastapi import FastAPI , Depends 
from pydantic import BaseModel 
import numpy as np 

from sqlmodel import Session , select 
from database import create_db_and_tables , get_session 
from models import  PredictionRequest , PredictionInput






app = FastAPI(title = "Bail prediction API ")
model = joblib.load("bail_predict")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()




class PredictionRequest(BaseModel):
    prior: str
    Type: str






prior_mapping = {"Yes": 1, "No": 0}
Type_mapping = {
    "Murder": 0,
    "Attempt to murder": 1,
    "Kidnapping": 2,
    "Sexual offence": 3,
    "Fraud and cheating": 4,
    "Narcotics": 5,
    "Domestic violence": 6,
    "Dowry": 7,
    "Theft or robbery": 8,
    "Other": 9
}




@app.post("/predict")
def predict_bail(data: PredictionRequest , session: Session = Depends(get_session) ):
    try:

        clean_prior = str(data.prior).strip("'\" ").upper()
        clean_Type = str(data.Type).strip("'\" ").title()


        numerical_prior = prior_mapping.get(data.prior)
        numerical_Type = Type_mapping.get(data.Type)

        if numerical_prior is None or numerical_Type is None:
            return {
                "error": "Dictionary look failed",
                "received_prior_text": repr(data.prior),
                "mapped_prior_value": numerical_prior,
                "received_Type_text": repr(data.Type),
                "mapped_Type_value": numerical_Type
            }

        features = np.array([[numerical_prior , numerical_Type]])
        prediction = model.predict(features)
        prediction_value = int(prediction.item())

        result_text = "Bail approve" if prediction_value == 0  else "bail not approve"  

        db_record = PredictionInput(prior=data.prior, Type=data.Type , prediction=result_text)
        try:
            session.add(db_record)
            session.commit()
            session.refresh(db_record)

            return {
                "prediction": result_text ,
                "raw_score": int(prediction.item()),
                "saved_id": db_record.id 
            }

        
        except Exception as e:
            session.rollback()
            return {"error": f"Database operation failed: {str(e)}"}
        


        return {"result" : result_text}
    except Exception as e:     
        return {"error": f"model prediction failed:{str(e)}"}

    