import json
import requests
import streamlit as st
import streamlit.components.v1 as components
from utils.get_url import get_service_url


url = get_service_url()
with open('./frontend/config.json', 'r', encoding='utf-8') as file:
    services_file = json.load(file)
api_url = url.replace(services_file['frontend-service-name'], services_file['api-service-name'])

CLUSTER_A = 'Segmento de altos ingresos y baja rotación laboral'
CLUSTER_B = 'Segmento de ingresos medios con estabilidad laboral'
CLUSTER_C = 'Segmento de jóvenes con bajos ingresos y poca estabilidad'
CLUSTER_D = 'Segmento actualmente desocupado y pocas posibilidades de reinserción'
LIMIT_LOWER = '300'
LIMIT_A = '400'
LIMIT_B = '500'
LIMIT_C = '560'
LIMIT_D = '680'
LIMIT_E = '850'

Entities = ['0-Aguascalientes', '1-Baja California', '2-Baja California Sur',
			'3-Campeche', '4-Coahuila de Zaragoza', '5-Colima', '6-Chiapas', '7-Chihuahua',
			'8-Ciudad de México', '9-Durango', '10-Guanajuato', '11-Guerrero', '12-Hidalgo',
			'13-Jalisco', '14-México', '15-Michoacán de Ocampo', '16-Morelos', '17-Nayarit',
			'18-Nuevo León', '19-Oaxaca', '20-Puebla', '21-Querétaro', '22-Quintana Roo',
			'23-San Luis Potosí', '24-Sinaloa', '25-Sonora', '26-Tabasco', '27-Tamaulipas',
			'28-Tlaxcala', '29-Veracruz de Ignacio de la Llave', '30-Yucatán', '31-Zacatecas']

variable = {
            "ingreso": 45000,
			"antiguedad_laboral_meses": 50,
			"tiempo_desempleado": 0,
			"trabajos_ultimos_5": 1,
			"semanasCotizadas": 1000,
			"edad": 32,
			"crecimiento_ingreso": 265.38,
			"lugar_actual": "Aguascalientes"
            }


def post():
	base_url = f'{api_url}/v1/prediction'
	resp = requests.post(base_url, json=variable)
	return resp.json()
	

def btn_disable(state):
    st.session_state['disabled'] = state


# Get gauge
with open('./frontend/code/gauge.html', 'r', encoding='utf-8') as file:
	html_var = file.read()
html_var = html_var.replace('LIMIT_LOWER', LIMIT_LOWER)
html_var = html_var.replace('LIMIT_A', LIMIT_A)
html_var = html_var.replace('LIMIT_B', LIMIT_B)
html_var = html_var.replace('LIMIT_C', LIMIT_C)
html_var = html_var.replace('LIMIT_D', LIMIT_D)


# Get components style
with open('./frontend/code/style.css', 'r', encoding='utf-8') as file:
	st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)


def main():
	left_col, cent_col, right_col = st.columns(3)
	with cent_col:
		st.image('./frontend/images/logo.jpg', use_column_width=True)
	st.markdown("<h1 style='text-align: center; color: grey;'>Income Scoring</h1>",
	     		unsafe_allow_html=True)
	st.markdown("<hr class='my-4'>", unsafe_allow_html=True)

	left_col, right_col = st.columns(2)
	with left_col:
		income = st.number_input("Ingreso", value=0.0, step=100.0)
		seniority_employment_months = st.number_input("Antigüedad Laboral (meses)", value=0, step=1)
		time_unemployed = st.number_input("Tiempo Desempleado (meses)", value=0, step=1)
		last_5_jobs = st.number_input("Trabajos Últimos 5 años", value=0, step=1)
		

		# Check invalid values
		if not isinstance(income, float) or income < 0:
			st.error("Ingreso invalido")

		if not isinstance(seniority_employment_months, int) or seniority_employment_months < 0:
			st.error("Antigüedad Laboral (meses) invalido")
		
		if not isinstance(time_unemployed, int) or time_unemployed < 0:
			st.error("Tiempo Desempleado (meses) invalido")
		
		if not isinstance(last_5_jobs, int) or last_5_jobs < 0:
			st.error("Trabajos Últimos 5 años invalido")

		if (seniority_employment_months > 0 and time_unemployed > 0):
			st.error("Tiempo Desempleado y Antigüedad Laboral no pueden ser ambos mayor a 0")

	with right_col:
		weekwage = st.number_input("Semanas Cotizadas", value=0, step=1)
		age = st.number_input("Edad", value=18, step=1)
		income_growth = st.number_input("Crecimiento de Ingreso", value=0.0, step=1.0)
		lugar_actual = st.selectbox("Seleccione Entidad Federativa", Entities)
		lugar = Entities.index(lugar_actual)

		# Check invalid values
		if not isinstance(weekwage, int) or weekwage < 0:
			st.error("Semanas Cotizadas invalido")

		if not isinstance(age, int) or age < 18 or age > 80:
			st.error("Edad invalida, debe ser entre 18 y 80 años")

		if not isinstance(income_growth, float) or (income == 0 and income_growth != 0):
			st.error("Crecimiento de Ingreso invalido o Ingreso igual a 0")

	if income < 0 or seniority_employment_months < 0 or time_unemployed < 0 or last_5_jobs < 0 or \
	   weekwage < 0 or age < 18 or age > 80 or \
	   income == 0 and income_growth != 0 or \
	   (seniority_employment_months > 0 and time_unemployed > 0):
		btn_disable(True)
	else:
		btn_disable(False)

	variable["ingreso"] = float(income)
	variable["antiguedad_laboral_meses"] = int(seniority_employment_months)
	variable["tiempo_desempleado"] = int(time_unemployed)
	variable["trabajos_ultimos_5"] = int(last_5_jobs)
	variable["semanasCotizadas"] = int(weekwage)
	variable["edad"] = int(age)
	variable["crecimiento_ingreso"] = float(income_growth)
	variable["lugar_actual"] = lugar

	col1, col2, col3, col4, col5 = st.columns(5)
	with col3:
		consult_btn = st.button("Consultar", disabled=st.session_state.get("disabled", False))
	
	left_col, cent_col, right_col = st.columns(3)
	with cent_col:
		if consult_btn:
			results = post()
			st.markdown(f'<h2 style=\'text-align: center; color: grey;\'>Cluster: {results["cluster"]}</h2>', unsafe_allow_html=True)
			if results["cluster"].lower() == 'a':
				cluster = CLUSTER_A
			elif results["cluster"].lower() == 'b':
				cluster = CLUSTER_B
			elif results["cluster"].lower() == 'c':
				cluster = CLUSTER_C
			else:
				cluster = CLUSTER_D
			
			st.markdown(f'<p style=\'text-align: center; color: black;\'>{cluster}</p>',
	       				unsafe_allow_html=True)
			
			value = float(results["scoring"]) * (1/550) - (300/550)
			var = html_var.replace('value_arg', str(value))
			# st.write(var)
			components.html(var,
							width=230,
							height=400
							)


if __name__ == '__main__':
	main()
