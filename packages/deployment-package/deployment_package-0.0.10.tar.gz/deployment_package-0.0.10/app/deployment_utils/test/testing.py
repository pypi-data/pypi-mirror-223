from unittest import TestCase, mock 
import deployment_utils.src.preprocessing as prep
import pandas as pd
import os

class DataPreprocessTest(TestCase):
    def test_drop_columns_function(self):
        instance = prep.DataPreprocess("","","")
        data = pd.DataFrame(columns=["age","sex","on_thyroxine","query_on_thyroxine","on_antithyroid_medication","sick","pregnant","thyroid_surgery","I131_treatment",
                                            "query_hypothyroid","query_hyperthyroid","lithium","goitre","tumor","hypopituitary","psych","TSH_measured","TSH","T3_measured","T3",
                                            "TT4_measured","TT4","T4U_measured","T4U","FTI_measured","FTI","TBG_measured","TBG","referral_source","Class"])
        expected = ["age","sex","on_thyroxine","on_antithyroid_medication","sick","pregnant","thyroid_surgery","I131_treatment",
                            "lithium","goitre","tumor","hypopituitary","psych","TSH","T3","TT4","T4U","FTI","Class"]
                
        actual = instance.dropColumns(data).columns.to_list()
        self.assertEqual(expected, actual)

    def test_wrong_artifact_path(self):
        instance = prep.DataPreprocess("wrongPath","wrongPath","wrongPath")
        with self.assertRaises(FileNotFoundError):
            encoder, scaler = instance.loadTransformers()

    def test_good_artifact_path(self):
        this_dir, this_filename = os.path.split(__file__)
        DATA_PATH = os.path.join(this_dir, "data", "test.pkl")

        instance = prep.DataPreprocess(model_path=DATA_PATH,
                                       encoder_path=DATA_PATH,
                                       scaler_path=DATA_PATH)
        scaler, encoder = instance.loadTransformers()
        self.assertIsNotNone(scaler)
        self.assertIsNotNone(encoder)