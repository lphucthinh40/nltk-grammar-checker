# Grammar-checker
Rule-based grammar checker for real-time speech recognition
-   The POS tagger is a Conditional Random Field (CRF) ML model. Please check the python script "train_tagger.py" to see how the tagger was trained. This ML model is stored in "POStagger.joblib" for latter usage.
-   nltk-trainer folder & conll2000_ub.pickle are necessary for initializing chunker model. Chunker used in this project is generated from python script provided by nltk-trainer
    (for more info regarding the chunker: https://nltk-trainer.readthedocs.io/en/latest/index.html)
