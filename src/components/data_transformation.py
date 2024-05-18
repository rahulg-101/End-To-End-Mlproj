# Applying different kinds of data preprocessing and transformation steps on your data

import os
import sys
from src.utils import save_object
from dataclasses import dataclass

import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifact','preprocessor.pkl')


class DataTransformation:
    def __init__(self) -> None:
        self.data_trans_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        """
        This function is responsible for data transformation
        """
        try:
            numerical_cols = ['reading_score', 'writing_score']
            categorical_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']


            num_pipeline = Pipeline(
                [('imputer',SimpleImputer(strategy='median')),
                 ('scaler',StandardScaler())]
            )
            
            
            
            cat_pipeline = Pipeline(
                [
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('ohe',OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info("Numerical cols std scaling completed")

            logging.info("Categorical cols encoding completed")

            preprocessor = ColumnTransformer([
                ('num_pipe',num_pipeline,numerical_cols),
                ('cat_pipe',cat_pipeline,categorical_cols)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transform(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_obj()

            target_column = 'math_score'
            numerical_cols = ['reading_score', 'writing_score']
            categorical_cols = ['gender', 'race_ethnicity', 
                                'parental_level_of_education',
                                  'lunch',
                                    'test_preparation_course']
            
            logging.info(f"My numerical cols are {numerical_cols}")
            logging.info(f"My categorical cols are {categorical_cols}")

            input_feature_train = train_df.drop(target_column,axis = 1)
            target_feature_train = train_df[target_column]

            input_feature_test = test_df.drop(target_column,axis = 1)
            target_feature_test = test_df[target_column]

            logging.info(f"Applying preprocessing object on training and testing dataframes")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test)
            
            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test)]
            logging.info("Saved preprocessing objects")


            save_object(
                    
                    filepath = self.data_trans_config.preprocessor_obj_file_path,
                    obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_trans_config.preprocessor_obj_file_path

            )
        except Exception as e:
            raise CustomException(e,sys)



