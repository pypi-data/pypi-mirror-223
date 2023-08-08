import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from classification_model import __version__ as _version
from classification_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config


# this block of code returns a dataframe
def load_dataset(*, file_name: str) -> pd.DataFrame:

    df = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))

    df.columns = df.columns.str.lower().str.replace(" ", "-")

    df = df.drop("customerid", axis=1)

    # format the values of our data by removing trailing spaces for
    # cat variable and equally changing them to lower case
    cat_var_formatting = [var for var in df.columns if df[var].dtype == "object"]

    for var in cat_var_formatting:
        if df[var].dtype == "object":
            df[var] = df[var].str.lower().str.replace(" ", "_")
        else:
            df[var] = df[var]

    # checking the data types of our feature columns and
    # possibily reformating some like total charges, senior citizen
    df.seniorcitizen = df.seniorcitizen.astype("object")
    df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce")

    df["churn"] = (df.churn == "yes").astype(int)

    df.dropna(inplace=True)

    return df


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:

    # prepare the versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name
    remove_old_pipeline(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    """load a persisted pipeline"""
    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipeline(*, files_to_keep: t.List[str]) -> None:
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
