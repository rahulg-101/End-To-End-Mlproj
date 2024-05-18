"""
Any functionalities that we are probably writing in a common way
which will be used in entire application
like calling database client, saving model code etc
"""

import os
import sys
import numpy as np
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException



def save_object(filepath,obj):
    try:
        dir_path = os.path.dirname(filepath)

        os.makedirs(dir_path,exist_ok=True)

        with open(filepath,'wb') as f:
            dill.dump(obj,f)

    except Exception as e:
        raise CustomException(e,sys)
    

def evaluate_models(x,y,xt,yt,models,param):
    try:
        report ={}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = list(param.values())[i]

            gs = GridSearchCV(model,param_grid=param,cv=5,n_jobs=-1)
            gs.fit(x,y)

            model.set_params(**gs.best_params_)
            model.fit(x,y)

            ytrain_pred  = model.predict(x)
            ytest_pred  = model.predict(xt)

            train_model_score = r2_score(y,ytrain_pred)

            test_model_score = r2_score(yt,ytest_pred)

            report[list(models.keys())[i]] = test_model_score

            return report
        
    except Exception as e:
        raise CustomException(e,sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)