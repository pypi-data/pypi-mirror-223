import os
import tempfile
from typing import List

import pandas as pd
import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from api_mlops_project.data_loader import DataLoader
from api_mlops_project.dataframe_checker import DataFrameChecker
from api_mlops_project.feature_engineering_predict import FeatureEngPredict
from api_mlops_project.pipeline_utils import PipelineCreator
from api_mlops_project.shape import DataInput

app = FastAPI()

CONFIG_PATH = 'artifacts/pipeline.jsonc'
DATA_PATH = 'data/dataset.parquet'


@app.get('/data')
def get_data():
    """
    Retrieve and return the original data from a predefined dataset file.

    This endpoint fetches data from the specified dataset file and returns it
    in a dictionary format. It uses the DataLoader to read the dataset and
    checks for any potential issues, such as an empty DataFrame or loading errors.

    Returns:
        dict: A dictionary representation of the original DataFrame from the dataset.
            The returned dictionary is structured such that column names from the DataFrame
            are keys, and the associated data are the corresponding values.

    Raises:
        HTTPException: Raised in the following scenarios:
            - If there's an issue loading the dataset.
            - If the loaded DataFrame is either empty or None.

    Example:
        Response:
        {
            "column1": [value1, value2, ...],
            "column2": [value1, value2, ...],
            ...
        }
    """
    try:
        dataframe = DataLoader.read_data_dataframe(DATA_PATH)
        if dataframe is None or dataframe.empty:
            e = 'DataFrame is empty or None!'
            DataFrameChecker._log_failure(e)
            raise ValueError(e)
        return JSONResponse(content=dataframe.to_dict())
    except Exception as e:
        return HTTPException(detail=str(e), status_code=400)


@app.post('/process_data')
async def process_data(file: UploadFile = File(...)):
    """
    Endpoint to process data from an uploaded file.

    Args:
        file (UploadFile): The uploaded file containing the data.

    Returns:
        dict: Processed DataFrame output.
    """
    try:
        # Obtendo o nome e a extensão do arquivo
        _, file_extension = os.path.splitext(file.filename)

        # Criando o arquivo temporário com a extensão original
        with tempfile.NamedTemporaryFile(
            suffix=file_extension, delete=False
        ) as temp:
            temp.write(file.file.read())
            temp_filename = temp.name

        # Assuming the uploaded file contains the same data as in DATA_PATH
        dataframe = DataLoader.read_data_dataframe(temp_filename)
        if dataframe is None or dataframe.empty:
            DataFrameChecker._log_failure(e)
            raise ValueError('DataFrame is empty or None!')

        checker = DataFrameChecker(dataframe)
        dataframe_input = checker.pipeline_checker()

        pipeline_transform = PipelineCreator.create_pipeline_from_file(
            CONFIG_PATH
        )
        if pipeline_transform is None:
            DataFrameChecker._log_failure(e)
            raise ValueError('Pipeline creation failed!')

        model_predict, dataframe_output = FeatureEngPredict.process_dataframe(
            dataframe_input, pipeline_transform
        )

        os.remove(temp_filename)

        return {
            'predictions': model_predict.tolist(),
            # "dataframe_output": dataframe_output.to_dict()
        }
    except Exception as e:
        return HTTPException(detail=str(e), status_code=400)


@app.post('/predict')
async def predict(request: Request):
    """
    Endpoint to make predictions based on the provided data in the request body.

    The expected request body should contain a JSON representation of the input data.

    Returns:
        dict: A dictionary containing the status and the predicted class.
            Example:
            {
                "status": "success",
                "predicted_class": "..."
            }

    Raises:
        HTTPException: If there is an issue during the prediction process or data processing.
    """
    try:
        # Convertendo o modelo Pydantic em um DataFrame
        json_data = await request.json()
        dataframe = pd.DataFrame(json_data, index=[0])

        # Processando o dataframe como antes
        checker = DataFrameChecker(dataframe)
        dataframe_input = checker.pipeline_checker()

        pipeline_transform = PipelineCreator.create_pipeline_from_file(
            CONFIG_PATH
        )
        if pipeline_transform is None:
            DataFrameChecker._log_failure(e)
            raise ValueError('Pipeline creation failed!')

        model_predict, _ = FeatureEngPredict.process_dataframe(
            dataframe_input, pipeline_transform
        )

        return JSONResponse(
            {'status': 'success', 'predicted_class': f'{model_predict[0]}'}
        )
    except Exception as e:
        return HTTPException(detail=str(e), status_code=400)


@app.post('/predict_batch')
async def predict_batch(request: Request):
    """
    Endpoint to make batch predictions based on the provided data.

    Args:
        request (Request): FastAPI request object containing the payload.

    Returns:
        dict: A dictionary containing the status of the prediction and the predicted class.
            Example:
            {
                "status": "success",
                "predicted_class": "..."
            }

    Raises:
        HTTPException: If there is an issue during the prediction process or data processing.
    """
    try:
        json_data = await request.json()
        dataframe = pd.DataFrame(json_data)

        checker = DataFrameChecker(dataframe)
        dataframe_input = checker.pipeline_checker()

        pipeline_transform = PipelineCreator.create_pipeline_from_file(
            CONFIG_PATH
        )
        if pipeline_transform is None:
            DataFrameChecker._log_failure('Pipeline creation failed!')
            raise ValueError('Pipeline creation failed!')

        _, dataframe_output = FeatureEngPredict.process_dataframe(
            dataframe_input, pipeline_transform
        )

        return JSONResponse(
            {
                'status': 'success',
                'predicted_class': dataframe_output['svm_predict'].to_json(
                    orient='records'
                ),
            }
        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


@app.post('/predict_path')
async def predict_path():
    """
    Endpoint to make predictions using the provided data from request body.

    Returns:
        dict: Predicted values from the model.
    """
    DATA_PATH = 'data/dataset.parquet'

    try:
        dataframe = DataLoader.read_data_dataframe(DATA_PATH)
        if dataframe is None or dataframe.empty:
            raise ValueError('DataFrame is empty or None!')

        checker = DataFrameChecker(dataframe)
        dataframe_input = checker.pipeline_checker()

        pipeline_transform = PipelineCreator.create_pipeline_from_file(
            CONFIG_PATH
        )
        if pipeline_transform is None:
            raise ValueError('Pipeline creation failed!')

        _, dataframe_output = FeatureEngPredict.process_dataframe(
            dataframe_input, pipeline_transform
        )

        return JSONResponse(
            {
                'status': 'success',
                'predicted_class': dataframe_output['svm_predict'].to_json(
                    orient='records'
                ),
            }
        )
    except Exception as e:
        DataFrameChecker._log_failure(
            e
        )  # This assumes the _log_failure method is static or class-based.
        raise HTTPException(detail=str(e), status_code=400)


if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=8000)
