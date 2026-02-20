import random
import numpy as np
import copy

class gen:
    def __init__(self, ancho,largo, tipo, rango_max=256, rango_min=0, aptitud=0, fenotipo=0, prob_cruce=0):
        self.largo = largo
        self.ancho = ancho
        self.tipo = tipo
        self.aptitud = aptitud
        self.rango_max = rango_max
        self.rango_min = rango_min
        self.fenotipo = fenotipo
        self.prob_cruce = prob_cruce
        if tipo == "binario":
            self.value = np.random.randint(0, 2, size=(largo, ancho))
        elif tipo == "entero":
            self.value = np.random.randint(rango_min, rango_max, size=(largo, ancho))
        elif tipo == "flotante":
            self.value = np.random.uniform(rango_min, rango_max, size=(largo, ancho))

    def mutacion(self):
        l_i=random.randint(0, self.largo-1)
        a_i=random.randint(0, self.ancho-1)
        if self.tipo == "binario":
            self.value[l_i,a_i]=int(not self.value[l_i,a_i])
        elif self.tipo == "entero":
            self.value[l_i,a_i]=random.randint(self.rango_min, self.rango_max)
        elif self.tipo == "flotante":
            self.value[l_i,a_i]=random.uniform(self.rango_min, self.rango_max)

    def cruce(self, pareja, mascara=None):
        if mascara is None:
            mascara = np.zeros((self.largo, self.ancho))
        for i in range(self.largo):
            for j in range(self.ancho):
                if mascara[i,j] == 1:
                    self.value[i,j] = self.value[i,j]
                else:
                    self.value[i,j] = pareja.value[i,j]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class poblacion:
    def __init__(self, tamano, ancho,largo, tipo, rango_max=256, rango_min=0):
        self.tamano = tamano
        self.tamano_inicial = tamano
        self.ancho = ancho
        self.largo = largo
        self.tipo = tipo
        self.rango_max = rango_max
        self.rango_min = rango_min
        self.genes = [gen(ancho,largo, tipo, rango_max, rango_min) for _ in range(tamano)]
        self.aptitud_poblacion = 0
        self.prob_maxima=0
        self.aptitud_maxima=0
        self.mejor_fenotipo=0

    def ordenar(self):
        self.genes.sort(key=lambda x: x.aptitud, reverse=True)

    def aptitud_total(self):
        self.aptitud_poblacion = 0
        for i in range(self.tamano):
            self.aptitud_poblacion += self.genes[i].aptitud

    def prob_cruce_poblacion(self):
        self.aptitud_total()
        for i in range(self.tamano):
            self.genes[i].prob_cruce = self.genes[i].aptitud / self.aptitud_poblacion

    def prob_max(self):
        self.prob_maxima = max(self.genes, key=lambda x: x.prob_cruce).prob_cruce

    def aptitud_max(self):
        self.aptitud_maxima = max(self.genes, key=lambda x: x.aptitud).aptitud

    def fenotipo_max(self):
        self.ordenar()
        self.mejor_fenotipo = self.genes[0].fenotipo

    def elitismo(self, n):
        seleccionados = poblacion(0, self.ancho, self.largo, self.tipo, self.rango_max, self.rango_min)
        self.ordenar()
        for i in range(n):
            seleccionados.add_gen(self.genes[i])
            #self.del_gen(self.genes[self.tamano-i-1])
        #self.aptitud_total()
        #self.prob_cruce_poblacion()
        return seleccionados

    def actualizar(self):
        self.aptitud_total()
        self.prob_cruce_poblacion()
        self.prob_max()
        self.aptitud_max()
        self.fenotipo_max()

    def seleccion_torneo(self, seleccionados=None):
        self.prob_max()
        self.aptitud_max()
        self.prob_cruce_poblacion()
        if seleccionados is None:
            seleccionados = poblacion(0, self.ancho, self.largo, self.tipo, self.rango_max, self.rango_min)
        while seleccionados.tamano < self.tamano_inicial:
            baremo = random.uniform(0, self.prob_maxima)
            for i in range(self.tamano):
                if self.genes[i].prob_cruce > baremo:
                    seleccionados.add_gen(self.genes[i])
                    if seleccionados.tamano == self.tamano_inicial:
                        break
        return seleccionados

    def cruce(self):
        lista=np.arange(self.tamano/2)*2
        lista=lista.astype(int)
        for i in lista:
            mascara=np.random.randint(0, 2, size=(self.largo, self.ancho))
            #print(self.genes[i].value, self.genes[i+1].value, mascara)
            self.genes[i].cruce(self.genes[i+1], mascara)
            self.genes[i+1].cruce(self.genes[i], mascara)
            #print(self.genes[i].value, self.genes[i+1].value)

    def add_gen(self, gen):
        self.genes.append(copy.deepcopy(gen))  # Hace una copia real e independiente del gen
        self.tamano += 1

    def del_gen(self, gen):
        self.genes.remove(gen)
        self.tamano -= 1

    def __str__(self):
        return str(self.genes)

    def __repr__(self):
        return str(self.genes)

def binario_a_entero_rango(gen, rango_max, rango_min):
    entero=gen.value[0].dot(1 << np.arange(gen.value.shape[1])[::-1])
    return rango_min + (entero / (2**gen.value.shape[1] - 1)) * (rango_max - rango_min)
