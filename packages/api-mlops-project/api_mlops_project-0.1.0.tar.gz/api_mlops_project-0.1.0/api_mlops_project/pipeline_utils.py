import json
import pickle
from typing import Union

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    PolynomialFeatures,
    QuantileTransformer,
    StandardScaler,
)


class PipelineCreator:

    """
    A utility class for creating scikit-learn pipelines from configuration files.

    This class provides a mechanism to build scikit-learn pipelines based on
    configurations specified in a JSONC formatted file. The configuration file
    details the sequence of preprocessing steps and model settings for the pipeline.

    Supported preprocessing steps include:
    - Polynomial feature generation
    - Quantile transformation
    - Polynomial feature generation
    - Standard scaling
    The final model used in the pipeline is loaded from a pickle file specified in the configuration.

    Raises:
        ValueError: If an unknown step is encountered in the configuration.

    Returns:
        Pipeline: A scikit-learn pipeline based on the provided configuration.

    Usage:
        pipeline = PipelineCreator.create_pipeline_from_file('path_to_config.jsonc')
    """

    @staticmethod
    def create_pipeline_from_file(jsonc_file_path: str) -> Pipeline:
        """
        Create a scikit-learn pipeline from a configuration file.

        This function constructs a pipeline by reading a JSONC formatted configuration file.
        The configuration file specifies preprocessing steps and model settings in the order
        they should appear in the pipeline. Supported steps include dimension reduction, quantile
        transformation, polynomial feature generation, and standard scaling. The model is loaded
        from a pickle file specified in the configuration.

        Args:
            jsonc_file_path (str): Path to the JSONC file containing the pipeline configuration.

        Raises:
            ValueError: If an unknown step is encountered in the configuration.

        Returns:
            Pipeline: A scikit-learn pipeline constructed based on the provided configuration.
        """
        with open(jsonc_file_path, 'rb') as json_file:
            config = json.load(json_file)

        pipeline_steps = []
        for step_name, step_params in config['steps'].items():
            if step_name == 'expand_features':
                step = (
                    'expand_features',
                    PolynomialFeatures(
                        degree=step_params['PolynomialFeatures']['degree']
                    ),
                )
            elif step_name == 'qtransf':
                step = (
                    'qtransf',
                    QuantileTransformer(
                        output_distribution=step_params['QuantileTransformer'][
                            'output_distribution'
                        ]
                    ),
                )
            elif step_name == 'poly_feature':
                step = (
                    'poly_feature',
                    PolynomialFeatures(
                        degree=step_params['PolynomialFeatures']['degree']
                    ),
                )
            elif step_name == 'stdscaler':
                step = (
                    'stdscaler',
                    StandardScaler(
                        with_mean=step_params['StandardScaler']['with_mean'],
                        with_std=step_params['StandardScaler']['with_std'],
                    ),
                )
            elif step_name == 'model':
                with open(step_params, 'rb') as file:
                    model = pickle.load(file)
                step = ('model', model)
            else:
                raise ValueError(f'Unknown step: {step_name}')

            pipeline_steps.append(step)

        return Pipeline(pipeline_steps)

    def create_partial_pipeline(pipeline: Pipeline) -> Pipeline:
        # Remove a última etapa se for o modelo
        if 'model' == pipeline.steps[-1][0]:
            return Pipeline(pipeline.steps[:-1])
        return pipeline
