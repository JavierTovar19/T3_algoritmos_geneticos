import random
import numpy as np

# -----------------------------
# 1. Datos del problema
# -----------------------------

partidos = ["A", "B", "C", "D", "E"]

# Distribución no uniforme de curules (suma 50)
curules = [18, 12, 9, 7, 4]
total_curules = sum(curules)

# Porcentaje ideal de poder por partido
porcentaje_ideal = [c / total_curules for c in curules]

# Generar 50 entidades con peso aleatorio 1-100
num_entidades = 50
pesos = [random.randint(1, 100) for _ in range(num_entidades)]

poder_total = sum(pesos)
poder_ideal = [p * poder_total for p in porcentaje_ideal]

# -----------------------------
# 2. Algoritmo Genético
# -----------------------------

# Parámetros
tam_poblacion = 100
generaciones = 200
tasa_mutacion = 0.1


# Crear individuo (asignación aleatoria)
def crear_individuo():
    return [random.randint(0, 4) for _ in range(num_entidades)]


# Calcular fitness (error absoluto total)
def fitness(individuo):
    poder_real = [0] * 5
    for i in range(num_entidades):
        poder_real[individuo[i]] += pesos[i]

    error = sum(abs(poder_real[i] - poder_ideal[i]) for i in range(5))
    return error


# Selección por torneo
def seleccion(poblacion):
    torneo = random.sample(poblacion, 3)
    torneo.sort(key=lambda x: fitness(x))
    return torneo[0]


# Cruce
def cruce(padre1, padre2):
    punto = random.randint(1, num_entidades - 1)
    hijo = padre1[:punto] + padre2[punto:]
    return hijo


# Mutación
def mutacion(individuo):
    for i in range(num_entidades):
        if random.random() < tasa_mutacion:
            individuo[i] = random.randint(0, 4)
    return individuo


# Inicializar población
poblacion = [crear_individuo() for _ in range(tam_poblacion)]

# Evolución
for gen in range(generaciones):
    nueva_poblacion = []
    for _ in range(tam_poblacion):
        padre1 = seleccion(poblacion)
        padre2 = seleccion(poblacion)
        hijo = cruce(padre1, padre2)
        hijo = mutacion(hijo)
        nueva_poblacion.append(hijo)
    poblacion = nueva_poblacion

# Mejor solución encontrada
mejor = min(poblacion, key=lambda x: fitness(x))

# Calcular poder final
poder_final = [0] * 5
for i in range(num_entidades):
    poder_final[mejor[i]] += pesos[i]

# -----------------------------
# -----------------------------
# 3. Resultados Finales
# -----------------------------

print("\n================ RESULTADOS FINALES ================\n")

print("Poder total del sistema:", poder_total)
error_total = fitness(mejor)
error_porcentual = (error_total / poder_total) * 100
print("\nPoder IDEAL por partido:")
for i in range(5):
    print(f"Partido {partidos[i]}: {poder_ideal[i]:.2f}")

print("\nPoder REAL asignado por el AG:")
for i in range(5):
    print(f"Partido {partidos[i]}: {poder_final[i]:.2f}")

print("\nDiferencia absoluta por partido:")
for i in range(5):
    diferencia = abs(poder_final[i] - poder_ideal[i])
    print(f"Partido {partidos[i]}: {diferencia:.2f}")

print("\nERROR TOTAL FINAL:", fitness(mejor))
print(f"ERROR PORCENTUAL: {error_porcentual:.2f}%")