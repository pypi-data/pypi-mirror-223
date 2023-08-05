import pandas as pd
import numpy as np
import pickle
import sklearn

class DataPreprocess():
    def __init__(self, encoder_path:str, scaler_path:str, model_path:str) -> None:
        self.ENCODER_PATH = encoder_path
        self.MODEL_PATH = model_path
        self.SCALER_PATH = scaler_path
    
    def dropColumns(self, inputData:pd.DataFrame):
        return inputData.drop(labels=["TBG", "referral_source", "TBG_measured", "FTI_measured", "query_on_thyroxine", "query_hyperthyroid", 
                            "query_hypothyroid", "T4U_measured", "TT4_measured", "T3_measured", "TSH_measured"], 
                            axis=1)
    
    def preprocessInput(self, inputData:pd.DataFrame):
        cleaned_input = self.dropColumns(inputData)
        encoder, scaler = self.loadTransformers()
        numeric_features = cleaned_input.select_dtypes("number").columns
        categorical_features = cleaned_input.select_dtypes(object).columns

        numericProcessed = pd.DataFrame(data=scaler.transform(cleaned_input[numeric_features]),
                                        columns=numeric_features)

        categoricalPreprocessed = pd.DataFrame(encoder.transform(cleaned_input[categorical_features]).toarray(), 
                                columns = encoder.get_feature_names_out(categorical_features))
        
        final_data = numericProcessed.join(categoricalPreprocessed)
        return final_data

    def loadTransformers(self):
        encoder = pickle.load(open(self.ENCODER_PATH, 'rb'))
        scaler = pickle.load(open(self.SCALER_PATH, 'rb'))
        return encoder, scaler
        
    def makePrediction(self, inputData:pd.DataFrame):
        processedInput = self.preprocessInput(inputData)
        model = pickle.load(open(self.MODEL_PATH, 'rb'))
        
        result = model.predict(processedInput)

        result_df = pd.DataFrame(data=result, columns=["label"])
        return result_df
 
    