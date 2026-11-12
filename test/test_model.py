import os
import pytest 
from fastapi.testclient import TestClient
from sqlmodel import Session , select , delete
from api import app 
from database import engine , create_db_and_tables
from models import PredictionInput

client = TestClient(app)

@pytest.fixture(autouse=True)


def setup_and_clean_db():
    create_db_and_tables()
    yield
    with Session(engine) as session:
        session.exec(delete(PredictionInput))
        session.commit()


def test_create_bail_prediction():

    sample_input={
     "prior" : "No",
     "Type": "Murder"

    }



    response = client.post("/predict", json=sample_input)
    assert response.status_code in [200,201]

    with Session(engine) as session:
        statement = select(PredictionInput)
        saved_record = session.exec(statement).first()

        assert saved_record is not None
        assert saved_record.prior == "No"


def test_get_preictions_from_db():

    with Session(engine) as session:

        test_record = PredictionInput(
             prior = "No",
             Type = "Murder",
             prediction = "Bail approve"

             )
        session.add(test_record)
        session.commit()
        results = session.exec(select(PredictionInput)).all()
        assert len(results) >=1
        assert results[0].prediction == "Bail approve"


def test_invalid_bail_prediction():
    response = client.post("/predict" , json={"prior":"UNKNOWN","Type":"UNKNOWN"})
    assert response.status_code ==200
    assert "error" in response.json()    

     


