from Insurance.entity import config_entity, artifacts_entity
from Insurance.exception import InsuranceException
from Insurance.logger import logging
import os
import sys
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
import pandas as pd
import numpy as np
from Insurance import config
from sklearn.preprocessing import LabelEncoder
from Insurance import utils
from typing import Optional
#from imblearn.combine import SMOTETomek since regression task


# Missing values.
# Handling outliers.
# Handling imbalance data.
# Handling categorical varialbles.



class Data_Transformation():
    def __init__(self, data_transformation_config : config_entity.DataTransformationConfig,
                 data_ingestion_artifact :  artifacts_entity.DataIngestionArtifact ):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            logging.info("Leaving Data tranformation constructor")    
        except Exception as e:
            raise InsuranceException(e,sys)
        
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            robust_scaler = RobustScaler()
            pipeline = Pipeline(steps=[
                    ("Imputer",simple_imputer),
                    ("RobustScaler",robust_scaler)
                ])
            
            return pipeline
           
        except Exception as e:
            raise InsuranceException(e,sys)
    
    
    def initiate_data_transformation(self,)->artifacts_entity.DataTransformationArtifact:
        try :
            logging.info("# Reading the data")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            logging.info("#Dividing the data into dependwnt and independent features")
            input_feature_train_df = train_df.drop(config.TARGET_COLUMN,axis=1)
            input_feature_test_df = test_df.drop(config.TARGET_COLUMN,axis=1) 
            
            target_feature_train_df = train_df[config.TARGET_COLUMN]
            target_feature_test_df= test_df[config.TARGET_COLUMN] 
            
            label_encoder = LabelEncoder()
            
            logging.info("#transformation on target columns --> np.array")
            target_feature_train_arr= target_feature_train_df.squeeze()
            target_feature_test_arr = target_feature_test_df.squeeze()
            
            logging.info("#transformation on categorical columns")
            for col in input_feature_train_df.columns:
                if input_feature_test_df[col].dtypes=="O":
                    input_feature_train_df[col] = label_encoder.fit_transform(input_feature_train_df[col])
                    input_feature_test_df[col]= label_encoder.fit_transform(input_feature_test_df[col])
                    logging.info("#Exiting if statement")
                else:
                    logging.info("#Entering else statement")
                    input_feature_train_df[col] = input_feature_train_df[col]
                    input_feature_test_df[col]= input_feature_test_df[col]
            
            logging.info("making transformation_pipeline")        
            transformation_pipeline = Data_Transformation.get_data_transformer_object() 
            logging.info("fitting/training transformation_pipeline")  
            transformation_pipeline.fit(input_feature_train_df)
            
            logging.info("transforming input features--> np.array")
            input_feature_train_arr=  transformation_pipeline.transform(input_feature_train_df)    
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)
            
            logging.info("#concate feature and target array")
            train_array= np.c_[input_feature_train_arr,np.array(target_feature_train_arr)]
            test_array= np.c_[input_feature_test_arr,np.array(target_feature_test_arr)]
            
            #print(test_array[:,:-1])
            #print(test_array[:,-1])
            
            logging.info("#Saving train and test numpy file")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array =train_array )
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_array)
            
            logging.info("#save numpy array TRANSFORM_OBJECT_FILE_NAME and TARGET_ENCODER_OBJECT_FILE_NAME")
            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path, obj= label_encoder)
            
            data_transformation_artifact= artifacts_entity.DataTransformationArtifact(
                                    transform_object_path =self.data_transformation_config.transform_object_path,
                                    transformed_train_path = self.data_transformation_config.transformed_train_path,
                                    transformed_test_path = self.data_transformation_config.transformed_test_path,
                                    target_encoder_path = self.data_transformation_config.target_encoder_path
                                )
            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        
        except Exception as e:
            raise InsuranceException(e,sys)
                
        
              
         



