import openpyxl

""" Ojo que openpyxl hay que instalarlo, se puede con pip:
    
    pip install openpyxl
"""

class Documentador:

    def __init__(self, inmobiliaria):
        self.documento = openpyxl.Workbook()
        self.hoja1 = self.documento.create_sheet("Casas Vendidas")
        self.hoja2 = self.documento.create_sheet("Casas Sin Vender")
        self.inmobiliaria = inmobiliaria

        #Se definen los titulos de la hoja 1 y un contador
        self.hoja1['A1'] = 'Tiempo'
        self.hoja1['B1'] = 'Casa'
        self.hoja1['C1'] = 'Precio'
        self.contador = 2

    def casa_vendida(self, casa, tiempo):
        self.hoja1['A' + str(self.contador)] = tiempo
        self.hoja1['B' + str(self.contador)] = casa.identificador
        self.hoja1['C' + str(self.contador)] = casa.precio
        self.contador += 1
        

    def fin_simulacion(self):
        i = 2
        for k in range(100):
            if not self.inmobiliaria.casas[k].vendida:
                casa = [str(self.hoja2['A' + str(i)].value), 1, 1, 0, 1, 0] 
                self.hoja2['A' + str(i)] = self.inmobiliaria.casas[k].identificador
                columnas = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
                for j in range(9):
                    self.hoja2[columnas[j] + str(i)] = self.inmobiliaria.casas[k].atributos[j + 5]
                i += 1

        self.documento.save('Resultados.xlsx')