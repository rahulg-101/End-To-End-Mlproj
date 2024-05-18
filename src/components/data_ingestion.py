# Ingesting data from different data sources

import os, sys, pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.exception import CustomerException
from src.logger import logging
from src.components.data_transformation import DataTransformation,DataTransformationConfig


@dataclass
class DataIngestionConfig:
    train_dat_path = str=os.path.join("artifact",'train.csv')  # file location or path for our input train data
    test_dat_path = str=os.path.join("artifact",'test.csv')  # file location or path for our input test data
    raw_dat_path = str=os.path.join("artifact",'raw_data.csv')  # file location or path for our input raw data

class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig() #So whenever we call DataIngestion, ingestion_config will save path to train,test and raw data

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion block")
        try :
            df =pd.read_csv(r'C:\Users\rahul gupta\Documents\Learning\Projects\End to End MLProj\notebook\data\stud.csv')
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_dat_path),exist_ok=True)

            """
            os.path.dirname(self.ingestion_config.train_dat_path): This part of the code retrieves the directory path from the 
            "self.ingestion_config.train_dat_path" value. 
            The os.path.dirname() function returns the directory component of a given path. For example, if 
            self.ingestion_config.train_dat_path is "/path/to/data/train.csv", then os.path.dirname() will return "/path/to/data".

            Basically the above line creates the parent directory "artifacts" in which all three datasets will be stored.
            """
            df.to_csv(self.ingestion_config.raw_dat_path,index=False,header=True)

            logging.info("Train-Test Split Initiated")
            
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_dat_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_dat_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_dat_path,
                self.ingestion_config.test_dat_path
            )
        except Exception as e:
            raise CustomerException(e,sys)
        

if __name__=="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transform(train_data,test_data)

    