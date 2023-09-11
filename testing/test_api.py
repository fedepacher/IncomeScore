from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_null_prediction():
    response = client.post('/v1/prediction', json={
                                                   "ingreso": 45000,
                                                   "antiguedad_laboral_meses": 50,
                                                   "tiempo_desempleado": 0,
                                                   "trabajos_ultimos_5": 1,
                                                   "semanasCotizadas": 1000,
                                                   "edad": 32,
                                                   "crecimiento_ingreso": 265.38,
                                                   "lugar_actual": 18
                                                   })
    assert response.status_code == 200
    # assert response.json()['scoring'] == 678.17
    # assert response.json()['cluster'] == 0


def test_random_prediction():
    response = client.post('/v1/prediction', json={
                                                   "ingreso": 1000,
                                                   "antiguedad_laboral_meses": 0,
                                                   "tiempo_desempleado": 13,
                                                   "trabajos_ultimos_5": 2,
                                                   "semanasCotizadas": 198,
                                                   "edad": 29,
                                                   "crecimiento_ingreso": 0,
                                                   "lugar_actual": 5
                                                   })
    assert response.status_code == 200
    # assert response.json()['scoring'] == 433.33
    # assert response.json()['cluster'] == 1
