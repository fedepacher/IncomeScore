"""API creation"""
import logging
from fastapi import FastAPI
from .app.models import PredictionResponse, IncomeRequest
from .app.views import get_prediction, get_models


LOG_FILE = 'logfile.log'
app = FastAPI(docs_url='/')
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
get_models(logging=logging)


@app.post('/v1/prediction')
def make_model_prediction(request: IncomeRequest):
    """API call to predict incoming data.

    Args:
        request (PredictionRequest): Incoming JSON request.

    Returns:
        JSON: JSON format scoring predicted output.
    """
    if request.values_checker():
        score_cliente, cluster_cliente = get_prediction(logging=logging, request=request)
        return PredictionResponse(scoring=round(score_cliente * 1000, 2),
                                  cluster=str(cluster_cliente))
    return {'Error': f'There are some error in fields {request}.'}
