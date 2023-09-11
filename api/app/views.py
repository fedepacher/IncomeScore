"""API view that gives the predicted elements"""
from .models import IncomeRequest
from .utils import get_model, convert_input_data


def get_models(logging=''):
    """Get model from DVC storage

    Args:
        logging (str, optional): Logging format.
    """
    global scaler
    global model_reg
    global model_clf
    scaler = get_model(logging, filenema='model_scaler')
    model_reg = get_model(logging, filenema='model_reg')
    model_clf = get_model(logging, filenema='model_clf')


def get_prediction(logging, request: IncomeRequest):
    """Get the scoring and cluster prediction based on request.

    Args:
        logging (loggin): Loggin format.
        request (IncomeRequest): Objet to be predicted.

    Returns:
        tuple: scoring and cluster predicted
    """
    try:
        client = convert_input_data(logging=logging, request=request)
        logging.info('Dataframe parsed correctly')
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    try:
        cliente_scaled = scaler.transform(client)
        logging.info('Dataframe scaled correctly')
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    puntuacion_credito = model_reg.predict(cliente_scaled)[0]
    cluster_predicho = model_clf.predict(cliente_scaled)[0]

    return puntuacion_credito, cluster_predicho
