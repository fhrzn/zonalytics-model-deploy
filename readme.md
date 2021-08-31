# Zonalytics
Zonalytics stands for Zonasi Analytics. This is my bachelor degree thesis project. This project was aimed to classify Indonesian's tweets opinion about Zonasi Sekolah policy which triggered a huge polemic in 2019.

<br>

## Installation
---
```
pip install -r requirements.txt
```

<br>

## Notebooks
---
Contains process of data exploration, data cleaning, data transformation, and modelling.
<br><br>
How to run:
```
* run sequentially
zonalytics.ipynb
```

<br>

## Deployments
---
Deployed best model using FastAPI.
<br><br>
How to run:
```
cd deployment
uvicorn main:app --reload
```
Go to browser and visit `http://127.0.0.1:8000`
<br><br>

### Available API
| Method | Path | Query | Description |
| ------ | ---- | ----- | ----------- |
|  GET   |   /  | None  | root path
|  GET   | /sentiment?text=query | Sentence | Predict tweet sentiment
|  GET   | /sentiment/cleaning?text=query | Sentence | Debug text cleaning output


<br>

## Experiments
---
This experiments using accuracy as metrics and several models as follow.

| No | Model | Accuracy | Best Parameter |
| --- | ---- | ----- | ----------- |
|  1  | MultinomialNB | 63%  | Default
| 2 | KNN | 65% | `K` = 22
| 3 | Random Forest | 67% | `n_estimators` = 200
| 4 | SVM | 64% | `kernel` = rbf