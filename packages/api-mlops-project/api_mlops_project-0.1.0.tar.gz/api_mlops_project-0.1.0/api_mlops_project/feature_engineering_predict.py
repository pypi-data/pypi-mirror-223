from typing import Optional, Union

from api_mlops_project.pipeline_utils import PipelineCreator


class FeatureEngPredict:
    """
    A class responsible for processing a dataframe using a provided transformation pipeline
    and a partial pipeline creator to obtain predictions of model OneClassSVM

    Attributes:
        pipeline_transform (Pipeline): The transformation pipeline to process the data.
        partial_pipeline_creator (Any): The utility to create a partial pipeline based on the transformation pipeline.

    Methods:
        process_dataframe(dataframe_input: pd.DataFrame, pipeline_transform: Pipeline) -> Tuple[np.array, pd.DataFrame]:
            Processes the input dataframe and returns the model's predictions along with the updated dataframe.
    """

    def __init__(self, pipeline_transform, partial_pipeline_creator):

        self.pipeline_transform = pipeline_transform
        self.partial_pipeline_creator = partial_pipeline_creator

    def process_dataframe(dataframe_input, pipeline_transform):

        """
        Processes the input dataframe using the transformation pipeline and returns the model's predictions
        along with an updated dataframe containing these predictions.

        Args:
            dataframe_input (pd.DataFrame): The input dataframe to process.
            pipeline_transform (Pipeline): The transformation pipeline to process the data.

        Returns:
            tuple:
                - model_predict (np.array): The predictions of the model.
                - dataframe_output (pd.DataFrame): The updated dataframe containing the predictions.
        """

        feature_engineering_pipe = PipelineCreator.create_partial_pipeline(
            pipeline_transform
        )
        dataframe_feature_engineering = feature_engineering_pipe.fit_transform(
            dataframe_input
        )

        step_name, step_transformer = pipeline_transform.steps[4]
        model_predict = step_transformer.predict(dataframe_feature_engineering)

        dataframe_output = dataframe_input.copy()
        dataframe_output['svm_predict'] = model_predict

        return model_predict, dataframe_output
