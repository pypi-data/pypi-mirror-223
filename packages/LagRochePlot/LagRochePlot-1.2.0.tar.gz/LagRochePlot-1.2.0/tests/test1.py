# Importación del módulo:
from LagRochePlot import LagRoche

# Variables a utilizar:
# Se escogen m1, m2 y distancia(por defecto en 100, 20 y 1 respectivamente):
    
m1 = 5.97219e24      # Masa tierra [kg]
m2 = 7.3477e22       # Masa luna [kg]
dist= 0.00256955529  # Distancia tierra-luna[UA]

# Restricción: m1>= m2
# Ejecución del módulo:
LagRoche.Plot(m1,m2,dist)