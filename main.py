from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import pickle
import mysql.connector
import numpy as np

app = FastAPI()

templates = Jinja2Templates(directory="templates")

model = pickle.load(open("diabetes_model.pkl", "rb"))

db = mysql.connector.connect(
    host= "localhost",  #"host.docker.internal",
    user="root",
    password="mohini",
    database="diabetes_db"
)

cursor = db.cursor()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    pregnancies: float = Form(...),
    glucose: float = Form(...),
    bloodpressure: float = Form(...),
    skinthickness: float = Form(...),
    insulin: float = Form(...),
    bmi: float = Form(...),
    pedigree: float = Form(...),
    age: float = Form(...)
):

    data = np.array([
        pregnancies,
        glucose,
        bloodpressure,
        skinthickness,
        insulin,
        bmi,
        pedigree,
        age
    ]).reshape(1, -1)

    prediction = model.predict(data)

    result = "Diabetic" if prediction[0] == 1 else "Not Diabetic"

    sql = """
    INSERT INTO predictions(
        pregnancies, glucose, bloodpressure,
        skinthickness, insulin, bmi,
        pedigree, age, prediction
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        pregnancies,
        glucose,
        bloodpressure,
        skinthickness,
        insulin,
        bmi,
        pedigree,
        age,
        result
    )

    cursor.execute(sql, values)
    db.commit()

    return templates.TemplateResponse(
    request=request,
    name="result.html",
    context={
        "prediction": result
    }
    )

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):

    cursor.execute(
        "SELECT * FROM predictions ORDER BY id DESC"
    )

    records = cursor.fetchall()

    return templates.TemplateResponse(
    request=request,
    name="history.html",
    context={
        "records": records
    }
    )