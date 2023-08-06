from config.core import config
from pipeline import customer_churn_pipeline
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """train the model."""

    # read the training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    x_train, x_test, y_train, y_test = train_test_split(
        data.drop([config.model_config.target], axis=1),  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    # fit model
    customer_churn_pipeline.fit(x_train, y_train)

    # persist the trained model
    save_pipeline(pipeline_to_persist=customer_churn_pipeline)


if __name__ == "__main__":
    run_training()
