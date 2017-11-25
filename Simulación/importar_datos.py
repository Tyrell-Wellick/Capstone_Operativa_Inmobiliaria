import openpyxl

""" Ojo que openpyxl hay que instalarlo, se puede con pip:
	
	pip install openpyxl
"""

def importar_casas():
	doc = openpyxl.load_workbook('Datos.xlsx')
	hoja = doc.get_sheet_by_name("DatosCasas")
	casas = [] #Lista que tendra los datos de cada casa
	for i in range(2, 102):
		casa = [str(hoja['A' + str(i)].value), 1, 1, 0, 1, 0] 
		"""Los primeros atributos de cada
		casa son los atributos del condominio"""
		columnas = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
		for j in columnas:
			casa.append(int(hoja[j + str(i)].value))

			""" Si llegamos a poner los precios iniciales de las casas
			en el excel habría que descomentar la siguiente linea para
			que los importe. Lo mismo en la definicion de la inmobiliaria"""
			#casa.append(int(hoja['K' + str(i)].value))

		casas.append(casa)
	return casas