import openpyxl

""" Ojo que openpyxl hay que instalarlo, se puede con pip:
    
    pip install openpyxl
"""

class Documentador:

    def __init__(self, inmobiliaria):
        self.documento = openpyxl.Workbook()
        self.hoja1 = self.documento.create_sheet("Casas Vendidas")
        self.hoja2 = self.documento.create_sheet("Casas Sin Vender")
        self.hoja3 = self.documento.create_sheet("Precios en el tiempo")
        self.inmobiliaria = inmobiliaria
        self.columnas = iter(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB'])

        #Se definen los titulos de la hoja 1 y un contador
        self.hoja1['A1'] = 'Tiempo'
        self.hoja1['B1'] = 'Casa'
        self.hoja1['C1'] = 'Precio'
        self.contador = 2

        #Se definen los titulos de la hoja 3
        self.hoja3['A1'] = 'Casa'
        for i in range(100):
            self.hoja3['A' + str(i + 2)] = 'Casa ' + str(i + 1)

    def casa_vendida(self, casa, tiempo):
        self.hoja1['A' + str(self.contador)] = tiempo
        self.hoja1['B' + str(self.contador)] = casa.identificador
        self.hoja1['C' + str(self.contador)] = casa.precio
        self.contador += 1

    def cambio_precio(self, semana):
        col = next(self.columnas)
        self.hoja3[col + '1'] = "Semana " + str(semana)
        for i in self.inmobiliaria.casas:
            None

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