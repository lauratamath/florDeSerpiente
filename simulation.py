from project import *
import numpy as np
from colorama import Fore, Style

class Store:
  def __init__(self, N, lambdaOne, lambdaTwo):
    self.cashierNumber = N
    self.avgClientsPerHour = lambdaOne
    self.cashierClientsPerHour = lambdaTwo

  def simulate(self):
    for cash in range(self.cashierNumber):
      queue = Queue()

    ###################################################
    # TODO Update parameters and fullfill new requisites
    ###################################################
    
    t = 0 
    n = 0 # estado del sistema, numero de solicitudes en t
    T = 60 # T = t0 + 60min 

    # contadores
    Na = 0 # llegadas 

    i_llegada = [] # tiempos de llegada de la i-esima solicitud, ids son indices
    i_salida = [] # tiempos de salida de la i-esima solicitud, ids son indices
    cliente_TE = [] # Tiempos de cada cliente en espera

    # eventos
    prox_llegada = self.next_ts(t) # tiempo de la proxima llegada
    setTiempo = np.zeros(self.serviSist) + np.infty # set de tiempos de salida de cada servidor, hay un setTiempo por cada server disponible
    tiempoOcupado = np.zeros(self.serviSist) # tiempo que cada server estuvo ocupado
    servidorNo = [] # se guardan cuales solicitudes fueron atendidas por cuales server
    servidores = np.zeros(self.serviSist) # para llevar registro de cual está ocupado

    while t < T: # Mientras no acceda el tiempo de cierre
        if prox_llegada <= min(setTiempo):
            # si el proximo tiempo de llegada es antes del proximo tiempo de salida, se encola
            t = prox_llegada 
            Na += 1 
            prox_llegada = self.next_ts(t) # siguiente tiempo de llegada
            i_llegada.append(t)
            if n < self.serviSist: # si hay menos clientes dentro que servidores, se le asigna uno que esté disponible
                for i in range(self.serviSist):
                    if servidores[i] == 0: 
                        cliente_TE = np.append(cliente_TE,t - i_llegada[len(i_llegada)-1])
                        servidorNo.append(i)
                        setTiempo[i] = t + np.random.exponential(1/(self.potencia*60)) 
                        tiempoOcupado[i] += setTiempo[i]-t 
                        servidores[i] = 1 
                        break;
            n += 1 # Se agrefa al nuevo cliente en el sistema
        
        else:
            # si el proximo tiempo de llegada es después del próximo tiempo de salida, se atiende ya que
            servidorPED = np.argmin(setTiempo) 
            t = setTiempo[servidorPED] 
            i_salida.append(t)
            if n <= self.serviSist: # Si hay menos o igual cantidad de clientes que servidores
                servidores[servidorPED] = 0
                setTiempo[servidorPED] = np.infty
            else: # Hay mas clientes por atender
                servidorNo.append(servidorPED) 
                cliente_TE = np.append(cliente_TE,t - i_llegada[len(i_llegada)-1])
                setTiempo[servidorPED] = t + np.random.exponential(1/(self.potencia*60)) 
                tiempoOcupado[servidorPED] += setTiempo[servidorPED]-t
                servidores[i] = 1 
            n -= 1 # Descontamos al cliente atendido del sistema
            
    # se calcula cuantas solicitudes atendio cada servidor 
    numSolicitudes = np.zeros(self.serviSist)
    for i in range(len(servidorNo)):
        numSolicitudes[servidorNo[i]] += 1

    return { 
        "en_cola": cliente_TE, "numSolicitudes": numSolicitudes, "setTiempo": setTiempo, "i_llegada": i_llegada, "i_salida": i_salida, "tiempoOcupado": tiempoOcupado
    }

    ###########################################################