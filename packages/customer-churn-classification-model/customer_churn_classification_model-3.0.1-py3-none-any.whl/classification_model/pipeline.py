# import packages and custom feature
# for building our models
from sklearn.pipeline import Pipeline

# from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from classification_model.config.core import config
from classification_model.processing import custom_feature as cf

# set up the pipeline
customer_churn_pipeline = Pipeline(
    [
        # == CATEGORICAL ENCODING ======
        # encode categorical variables using one hot encoding into k-1 variables
        (
            "categorical_encoder",
            cf.CategoricalEncoder(variables=config.model_config.cat_vars),
        ),
        # ==== FEATURE SELECTION ========
        (
            "selected_features",
            cf.SelectedFeatures(variables=config.model_config.selected_features),
        ),
        # ==== SCALING OUR data ========
        (
            "scaler",
            cf.FeatureNormalizer(variables=config.model_config.selected_features),
        ),
        (
            "xgb",
            XGBClassifier(
                eta=config.model_config.eta,
                alpha=config.model_config.alpha,
                random_state=config.model_config.random_state,
            ),
        ),
    ]
)
