from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from classification_model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """check model inputs for na values and filter"""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_config.features
        if validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """check model inputs for unprocessable values."""
    relevant_data = input_data[config.model_config.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate input
        MultipleCustomerDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class CustomerDataInputSchema(BaseModel):
    customerid: Optional[str]
    gender: Optional[str]
    seniorcitizen: Optional[str]
    partner: Optional[str]
    dependents: Optional[str]
    tenure: Optional[int]
    phoneservice: Optional[str]
    multiplelines: Optional[str]
    internetservice: Optional[str]
    onlinesecurity: Optional[str]
    onlinebackup: Optional[str]
    deviceprotection: Optional[str]
    techsupport: Optional[str]
    streamingtv: Optional[str]
    streamingmovies: Optional[str]
    contract: Optional[str]
    paperlessbilling: Optional[str]
    paymentmethod: Optional[str]
    monthlycharges: Optional[float]
    totalcharges: Optional[float]


class MultipleCustomerDataInputs(BaseModel):
    inputs: List[CustomerDataInputSchema]
