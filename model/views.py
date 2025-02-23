from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import csv
import pandas as pd
import joblib
import numpy as np


def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def model(request):
  years = range(2016, 2031)
  cve_ent_nom_ent_list = []

# Ruta al archivo CSV
  csv_file_path = '/app/municipios.csv'
  # Leer el archivo CSV
  df = pd.read_csv(csv_file_path)
  # Filtrar los datos eliminando entidades duplicadas
  df_filtered = df.drop_duplicates(subset=['CVE_ENT'])
  cve_ent_nom_ent_list = df_filtered.to_dict('records')

  #Obtener los datos generales para posteriormente filtrarlos por entidad
  municipios = df.to_dict('records')


  context = {
    'years': years,
    'cve_ent_nom_ent_list': cve_ent_nom_ent_list,
    'municipios': municipios
  }
  return render(request, 'formulario.html', context)

def result(request):
  # Cargar el modelo random forest
  model_path = '/app/rf_model.pkl'  
  model = joblib.load(model_path)

  #cargar modelo de regresion lineal
  model_path_rl = '/app/linear_regression_model.pkl'  
  model_rl = joblib.load(model_path_rl)

  # Obtener los datos del formulario
  form_data = request.POST

  # Preprocesar los datos del formulario según sea necesario
  # Aquí debes ajustar el preprocesamiento según tu modelo

  ano=int(form_data.get('ano'))

  input_data = {
      'año': ano,
      'cve_ent': int(form_data.get('cve_ent')),
      'cve_mun': int(form_data.get('cve_mun')),
      'modalidad': int(form_data.get('modalidad')),
      'ingresos_rango': int(form_data.get('ingresos_rango')),
      'vivienda_valor': int(form_data.get('vivienda_valor'))
  }

  # Convertir el diccionario en un DataFrame de pandas
  input_df = pd.DataFrame([input_data])

  # Realizar la predicción
  if ano <= 2024:
      prediction = model.predict(input_df)
      observacion="La estimación se realizó mediante un modelo de bosques aleatorios, la presición de este modelo es mae: 170,538.13 R^2 Score: 0.82"
  else:
      prediction = model_rl.predict(input_df)
      observacion="La estimación se realizó mediante un modelo de regresión lineal, la presición de este modelo es mae: 326,842.82 R^2 Score: 0.56"

  # Formatear la predicción como moneda
  formatted_prediction = "${:,.2f}".format(prediction[0])

  # Preparar el contexto con el resultado
  context = {
      'prediction': formatted_prediction,
      'observacion': observacion
  }

  return render(request, 'result.html', context)
