import numpy as np
import matplotlib.pyplot as plt
from gens import *


def funcion(x): 
    """
    Maximizar la función f(x)=x sen(10πx) + 1, con x ∈[0,1].
    """
    #return x**2 - 1.23*x-6.2
    #return np.cos(10*np.pi*x)*np.sin(x-9.5*np.pi*x)
    return x * np.sin(10 * np.pi * x) + 1

#seleccionados = poblacion(0,10,1,"binario",1,0)

tamano_inicial = 10
generaciones = 500

pb = poblacion(tamano_inicial, 20, 1, "binario", 1, 0)
lista_gen = np.arange(generaciones)
lista_aptitud = []
lista_aptitud_max = []

for i in range(generaciones):
    for i in range(pb.tamano):
        pb.genes[i].fenotipo = binario_a_entero_rango(pb.genes[i], 1, 0)
        pb.genes[i].aptitud = funcion(pb.genes[i].fenotipo)

    sl = pb.elitismo(10)
    sl = pb.seleccion_torneo(seleccionados=sl)
    sl.tamano_inicial = pb.tamano_inicial
    sl.cruce()
    mutante=random.randint(0, sl.tamano-1)
    sl.genes[mutante].mutacion()

    for i in range(sl.tamano):
        sl.genes[i].fenotipo = binario_a_entero_rango(sl.genes[i], 1, 0)
        sl.genes[i].aptitud = funcion(sl.genes[i].fenotipo)
        
    sl.actualizar()
    pb.actualizar()
    #
    #print('AP', round(pb.aptitud_poblacion, 6),
    #      'AS', round(sl.aptitud_poblacion, 6),
    #      'MF', round(pb.mejor_fenotipo, 6),
    #      'AM', max(round(pb.aptitud_maxima, 6), round(sl.aptitud_maxima, 6)))

    if sl.aptitud_maxima > pb.aptitud_maxima:
        print("Nueva poblacion", pb.aptitud_maxima)
        pb = sl
    
    pb.actualizar()
    lista_aptitud.append(pb.aptitud_poblacion)
    lista_aptitud_max.append(pb.aptitud_maxima)

plt.subplot(2,1,1)
plt.plot(lista_gen, lista_aptitud)
plt.subplot(2,1,2)
plt.plot(lista_gen, lista_aptitud_max)
plt.show()
