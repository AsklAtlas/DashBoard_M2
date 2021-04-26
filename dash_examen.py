import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt
import plotly.express as px
from datamanagement import get_dataframe 
import pickle
from sklearn.ensemble import RandomForestRegressor

#import data
data = get_dataframe("./data/export_data.csv")
rs = pd.read_csv("./save_model/df_result.csv")
rs_melt = pd.read_csv('./save_model/df_result_melt.csv')

table = pd.DataFrame({
	'Categorie': [0,1,2,3,4,5,6,7,8,9],
	'Age':[ '0-17 ans',
			'18-29 ans',
			'30-39 ans',
			'40-49 ans',
			'50-59 ans',
			'60-69 ans',
			'70-79 ans',
			'80-89 ans',
			'90-99 ans',
			'100-127 ans']
	})
fig = px.histogram(
			data_frame = data,
			x = 'duree_rea_post_op',
			color = 'service',
			template = 'plotly_dark',
			nbins=50,
			labels={'x':'Temps passé en réanimation', 'y':'Count'},
			marginal="rug"
		)
fig_plot2 = px.scatter(
			data,
			x = 'age',
			y = 'duree_rea_post_op',
			trendline='ols',
			opacity = 0.10,
			template = 'plotly_dark',
			labels={'x':'Age', 'y':'Temps passé en réanimation'}
		)

fig_ft = px.bar(
					rs_melt,
					y = 'variable',
					x = 'value',
					orientation='h',
					template = 'plotly_dark',
					labels={'y':'Importance', 'x':'Variable'}
					)

# css stylesheet
external_stylesheets =  ['https://codepen.io/chriddyp/pen/bWLwgP.css']






# Dash App
app= dash.Dash("Dashboard", external_stylesheets=external_stylesheets)

colors = {
    'background': 'rgb(30, 30, 30)',#'#160800',
    'text': '#FCFCFC' #'#ACBEC087'
    }


# layout HTML 
app.layout = html.Div(style= { 'backgroundColor': colors['background'] }, 
	children=[ 
	html.H1(children="Exploration et prediction de la duree passée en réanimation", 
		style= {'textAlign': 'center', 'color': colors['text'] }),
	#ligne 1 avec l'histogramme
	html.Div( className='row',style={ 'textAlign': 'center', 'color': colors['text'] }, 
		children=[
			html.Div(className= 'four columns div-user-controls',
			children = [
				html.Div(children = [
					dcc.Dropdown(
						id = "Service",
						options=[{'label': i, 'value': i} for i in data['service'].unique()],
						value = ['Bloc Commun'],
						multi = True,
						style={'textAlign': 'center', 'backgroundColor': '#1E1E1E','color':'#1D1E1ECC'},
						placeholder = "Selection des services"
					),
				]),
			html.Div(children = [
				dt.DataTable(
					id='table_categorie_age',
					columns = [
						{'name': 'Categorie', 'id': 'Categorie'},
						{'name': 'Age', 'id': 'Age'}
					],
					data = table.to_dict('records'),
					fill_width = False,
					style_cell={'textAlign': 'center', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white','border': '1px solid grey' },
					style_header={
						'backgroundColor': 'rgb(30, 30, 30)',
						'fontWeight': 'bold',
						'border': '1px solid black' 
					},
				),
				html.P('''Selection du caractere urgent de l'intervention : ''',
					style = {'textAlign':'left','color':'#FDFDFD','fontWeight': 'bold'
					}
				),
				dcc.RadioItems(
					id='Caractere_urgent',
					options = [
						{'label':"urgence","value":1},
						{'label':"pas d'urgence","value":0},
						{'label':"tout confondu","value":2}
					],
					value = 2,
					labelStyle={'display': 'inline-block'}
				),
				dcc.Checklist(
					id = 'Asa',
					options=[{'label': i, 'value': i} for i in data['asa'].unique()],
					value=['ASA1', 'ASA2', 'ASA3', 'ASA4', 'ASA5'],
					labelStyle={'display': 'inline-block'}
				),
			]),
		]),
			html.Div(className='eight columns div-for-charts bg-grey', children=[
			dcc.Graph(id='plot1', figure= fig),
			html.Div(children = [
				html.P('''Selection des categories d'age'''),
				dcc.RangeSlider(
					id = 'Categorie_Age',
					min = 0,
					max = 9,
					marks={ str(a): str(a) for a in data['categorie_age_adulte'].unique().astype(int) },
					step=None,
					value = [0,9]
				),
			]),
		])
	]),
	# ligne 2 avec les scatter facet plot
	html.Div(className='row',style={'textAlign': 'center', 'color': colors['text']}, children=[
		html.Div(className='four columns div-user-controls',
			children = [
				dcc.Dropdown(
					id = "service_bis",
					options=[{'label': i, 'value': i} for i in data['service'].unique()],
					value = ['Bloc Commun'],
					multi = True,
					style={'textAlign': 'center', 'backgroundColor': '#1E1E1E','color':'#1D1E1ECC'},
					placeholder = "Selection des services"
				),
				html.P('''Selection de la variable des abscisses : ''', style = {'textAlign':'left','color':'#FDFDFD','fontWeight': 'bold'}),
				dcc.RadioItems(
					id = 'variable_plot2',
					options = [
						{'label':'Age','value':'age'},
						{'label':'IMC','value':'imc'},
						{'label':'ASA','value':'asa_score'},
						{'label':'Urgence','value':'urgence'}
					],
					value = 'age',
					labelStyle={'display': 'inline-block'}
				),
				html.P('''Selection de la variable de facet : ''',style = {'textAlign':'left','color':'#FDFDFD','fontWeight': 'bold'}),
				dcc.RadioItems(
					id = 'facetcol_plot2',
					options = [
						{'label':'Sexe','value':'sexe'},
						{'label':'ASA','value':'asa'},
						{'label':'Urgence','value':'urgence'},
						{'label':'Annee','value':'annee'}
					],
					value = 'sexe',
					labelStyle={'display': 'inline-block'}
				)

		]),
		html.Div(className='eight columns div-for-charts bg-grey', style={'backgroundColor':'#000102'}, 
			children=[dcc.Graph(id='plot2', figure= fig_plot2)])		
	]),
	# ligne 3 avec les ML
	html.Div(className='row',style={'textAlign': 'center', 'color': colors['text']}, children=[
		html.Div(className='four columns div-user-controls',
			children = [
				dcc.Dropdown(
					id = "service_ter",
					options=[{'label': i, 'value': i} for i in data['service'].unique()],
					value = ['Bloc Commun'],
					multi = True,
					style={'textAlign': 'center', 'backgroundColor': '#1E1E1E','color':'#1D1E1ECC'},
					placeholder = "Selection des services"
				),
				html.Label("Importance des variables pour la prédiction de la durée en Réanimation", 
					style = {'textAlign':'center','color':'#FDFDFD','fontWeight': 'bold'}),
				dt.DataTable(
					id='table_rs',
					columns = [
						{'name': 'Service', 'id': 'index'},
						{'name': 'Age', 'id': 'age'},
						{'name' : 'IMC', 'id' : 'imc' },
						{'name' : 'Score Asa', 'id' : 'asa_score' },
						{'name' : 'Urgence', 'id' : 'urgence' },
						{'name' : 'Sexe', 'id' : 'sexe' },
						{'name' : 'Neg_MAE_Score', 'id' : 'NMAE_Score' }
					],
					data = rs.to_dict('records'),
					fill_width = False,
					style_cell={'textAlign': 'center', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white','border': '1px solid grey' },
					style_header={
						'backgroundColor': 'rgb(30, 30, 30)',
						'fontWeight': 'bold',
						'border': '1px solid black' 
					},
				),
				html.Br(),
				html.Br()
		]),
		html.Div(className='eight columns div-for-charts bg-grey', style={'backgroundColor':'#000102'}, 
			children=[
			dcc.Graph(id='plot3', figure = fig_ft)
			]),
		]),
		html.Div(className='row',style={'textAlign': 'center', 'color': colors['text']}, 
			children=[
				html.Div(className='four columns div-user-controls', 
				children=[
		        	html.Label("Prédire le temps en service de réanimation", 
						style = {'textAlign':'center', 'backgroundColor': '#1D1E1ECC','color':'#FCFCFC','fontWeight': 'bold'}),

					dcc.Dropdown(
						id = "service_ml",
						options=[{'label': i, 'value': i} for i in data['service'].unique()],
						value = 'Bloc Commun',
						multi = False,
						style={'textAlign': 'center', 'backgroundColor': '#1E1E1E','color':'#1D1E1ECC'},
						placeholder = "Selection des services"
					),
					html.P('''Selection de la variable sexe: ''', style = {'textAlign':'left','color':'#FCFCFC','fontWeight': 'bold'}),
					dcc.RadioItems(
						id = 'variable_sexe',
						options = [
							{'label':'Femme','value':2},
							{'label':'Homme','value':1}
						],
						value = None,
						labelStyle={'display': 'inline-block'}
					),
					html.P('''Selection de la variable Urgence: ''', style = {'textAlign':'left','color':'#FCFCFC','fontWeight': 'bold'}),
					dcc.RadioItems(
						id = 'variable_urg',
						options = [
							{'label':"urgence","value":1},
							{'label':"pas d'urgence","value":0}
						],
						value = None,
						labelStyle={'display': 'inline-block'}
					),
					dcc.Dropdown(
						id = "asa_ml",
						options=[{'label': i, 'value': i} for i in data['asa_score'].unique()],
						value = None,
						multi = False,
						style={'textAlign': 'center', 'backgroundColor': '#1E1E1E','color':'#1D1E1ECC'},
						placeholder = "Score ASA"
					),
					 
			        dcc.Input(
			            id="input_IMC",
			            type='number',
			            placeholder="input type IMC",
			        ),
			        dcc.Input(
			            id="input_Age",
			            type='number',
			            placeholder="input type Age",
			        ),   
				]),
				
			html.Div(className= 'eight columns div-for-charts bg-grey',id='result_ml', title = "Random Forest Regressor prediction", 
		        	style={'backgroundColor':'#000102'}, children= [
		        	html.Br(),
					html.Br(),
		        	html.Label("Random Forest Regressor prediction", 
					style = {'textAlign':'center', 'backgroundColor': '#1D1E1ECC','color':'#FCFCFC','fontWeight': 'bold'}),

		        	]),
		]),
])


# call back plot1
@app.callback(
	Output('plot1','figure'),
	Input('Service','value'),
	Input('Categorie_Age','value'),
	Input('Caractere_urgent','value'),
	Input('Asa','value')
	)


def update_figure(service_value,categorie_age_value,caractere_urgent_value,asa_value):
	#service avec selection multiple
	b = data[data['service'].isin(service_value)]
	# categorie age avec slider
	rslider = []
	for i in range(categorie_age_value[0],categorie_age_value[1]):
		rslider.append(i)
	b = b[b['categorie_age_adulte'].isin(rslider)]
	# caractere urgence ou non par radio item
	if caractere_urgent_value != 2:
		b = b[b['urgence']==caractere_urgent_value]
	# checklist asa
	b = b[b['asa'].isin(asa_value)]
	#retrait des valeurs aberrantes qui donnent un graphique illisible
	q3 = b['duree_rea_post_op'].quantile(0.75)
	q1 = b['duree_rea_post_op'].quantile(0.25)
	b = b.dropna()
	interquartile = q3-q1
	valeur_min = q1-(1.5*interquartile)
	valeur_max = q3+(1.5*interquartile) 
	b = b[b['duree_rea_post_op'] >= valeur_min]
	b = b[b['duree_rea_post_op'] <= valeur_max]
	# creation du graph
	if len(service_value) >1:
		fig = px.histogram(
			data_frame = b,
			x = 'duree_rea_post_op',
			color = 'service',
			template = 'plotly_dark',
			nbins=50,
			labels={'x':'Temps passé en réanimation', 'y':'Count'},
			marginal="rug"
		)
	else:
		fig = px.histogram(
			data_frame = b,
			x = 'duree_rea_post_op',
			template = 'plotly_dark',
			nbins=50,
			labels={'x':'Temps passé en réanimation', 'y':'Count'},
			marginal="rug"
		)
	return fig


# call back plot2
@app.callback(
	Output('plot2','figure'),
	Input('service_bis','value'),
	Input('variable_plot2','value'),
	Input('facetcol_plot2','value')
)


def update_fig_plot2(service_bis_value,variable_plot2_value,facetcol_plot2_value):
	#service avec selection multiple
	c = data[data['service'].isin(service_bis_value)]
	#retrait des valeurs aberrantes qui donnent un graphique illisible
	q3 = c['duree_rea_post_op'].quantile(0.75)
	q1 = c['duree_rea_post_op'].quantile(0.25)
	interquartile = q3-q1
	valeur_min = q1-(1.5*interquartile)
	valeur_max = q3+(1.5*interquartile) 
	c = c[c['duree_rea_post_op'] >= valeur_min]
	c = c[c['duree_rea_post_op'] <= valeur_max]
	
	# IQ pour IMC
	q3 = c['imc'].quantile(0.75)
	q1 = c['imc'].quantile(0.25)
	interquartile = q3-q1
	valeur_min = q1-(1.5*interquartile)
	valeur_max = q3+(1.5*interquartile) 
	c = c[c['imc'] >= valeur_min]
	c = c[c['imc'] <= valeur_max]

	# map sexe with letters
	c.sexe = c.sexe.map({ 0 : "F", 1:"M"})

	if variable_plot2_value == 'ASA':
		c["asa"] = c["asa_score"]
	if len(service_bis_value) >1:
		c = c.sort_values(by = variable_plot2_value) 
		fig_plot2 = px.scatter(
			c,
			x = variable_plot2_value,
			facet_col = facetcol_plot2_value,
			y = 'duree_rea_post_op',
			color = 'service',
			trendline='ols',
			opacity = 0.10,
			template = 'plotly_dark',
			labels={'x':'Age', 'y':'Temps passé en réanimation'}
		)
	else:
		c = c.sort_values(by = variable_plot2_value) 
		fig_plot2 = px.scatter(
			c,
			x = variable_plot2_value,
			facet_col = facetcol_plot2_value,
			y = 'duree_rea_post_op',
			trendline='ols',
			opacity = 0.10,
			template = 'plotly_dark',
			labels={'x':'Age', 'y':'Temps passé en réanimation'}
		)
	return fig_plot2

# call back plot3
@app.callback(
	Output('plot3','figure'),
	Input('service_ter','value')
)

def update_plot3(service_ter_value):
	rs_tmp = rs_melt[rs_melt['index'].isin(service_ter_value)]

	if len(service_ter_value)>1:
		fig_ft = px.bar(
					rs_tmp,
					y = 'variable',
					x = 'value',
					orientation='h',
					color = 'index',
					barmode = 'group',
					template = 'plotly_dark',
					labels={'y':'Importance', 'x':'Variable'}
					)
	else:
		fig_ft = px.bar(
					rs_tmp,
					y = 'variable',
					x = 'value',
					orientation='h',
					template = 'plotly_dark',
					labels={'y':'Importance', 'x':'Variable'}
					)
	return fig_ft


# cal back ml model
@app.callback(
Output('result_ml', 'children'),
Input('service_ml', 'value'),
Input('variable_sexe', 'value'),
Input('variable_urg', 'value'),
Input('input_Age', 'value'),
Input('input_IMC','value'),
Input('asa_ml', 'value')
	)

def get_ml_prediction(service_ml_value, variable_sexe_value=None, variable_urg_value=None, input_Age_value=None, input_IMC_value=None, asa_ml_value=None):
	
	if (variable_sexe_value and  variable_urg_value and input_Age_value and input_IMC_value and asa_ml_value):
		sample = np.array([input_Age_value, input_IMC_value, asa_ml_value, variable_urg_value, variable_sexe_value]).reshape(1,-1)

		# open the pickle file with model
		filename = "./save_model/" + str(service_ml_value) + ".sav"
		rfr = pickle.load(open(filename, 'rb'))
		res_t = "Le temps estimé en réanimation par Random Forest est de {0:.2f} jours".format(rfr.predict(sample)[0])
	else:
		res_t = ""
	return res_t




# run script as main and instanciate a flask server
if __name__ == '__main__':
	app.run_server(debug=True)
