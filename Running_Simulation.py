import numpy as np
from colorama import Fore, Style

class Supermarket():

    def __init__(self, max_sol = 11, cajas = 1):
        self.lambda_max = max_sol  # cantidad máxima de solicitudes que se recibirán (lambda)/ minuto 
        self.cajas = cajas # cantidad de cajases que tiene el sistema 
    
    def next_ts(self, t): # No hace gran cosa, pero existe porque los eventos serán procesos de poisson homogeneos
        return t - (np.log(np.random.uniform())/self.lambda_max)

    def get_exponential(self, lamda):
        return -(1 / lamda)*np.log(np.random.uniform())

    def simulate(self):
        t = 0 
        n = 0 # estado del sistema, numero de solicitudes en t
        T = 60*8 # T = t0 + 60min 

        # contadores
        Na = 0 # llegadas 

        i_llegada = [] # tiempos de llegada de la i-esima solicitud, ids son indices
        i_salida = [] # tiempos de salida de la i-esima solicitud, ids son indices
        cliente_TE = [] # Tiempos de cada cliente en espera

        # eventos
        prox_llegada = self.next_ts(t) # tiempo de la proxima llegada
        setTiempo = np.zeros(self.cajas) + np.infty # set de tiempos de salida de cada caja, hay un setTiempo por cada caja disponible
        tiempoOcupado = np.zeros(self.cajas) # tiempo que cada caja estuvo ocupado
        cajasNo = [] # se guardan cuales solicitudes fueron atendidas por cual caja
        cajases = np.zeros(self.cajas) # para llevar registro de cual está ocupado

        while t < T: # Mientras no acceda el tiempo de cierre
            if prox_llegada <= min(setTiempo):
                # si el proximo tiempo de llegada es antes del proximo tiempo de salida, se encola
                t = prox_llegada 
                Na += 1 
                prox_llegada = self.next_ts(t) # siguiente tiempo de llegada
                i_llegada.append(t)
                if n < self.cajas: # si hay menos clientes dentro que cajas, se le asigna uno que esté disponible
                    for i in range(self.cajas):
                        if cajases[i] == 0: 
                            cliente_TE = np.append(cliente_TE,t - i_llegada[len(i_llegada)-1])
                            cajasNo.append(i)
                            setTiempo[i] = t + np.random.exponential(25) 
                            tiempoOcupado[i] += setTiempo[i]-t 
                            cajases[i] = 1 
                            break;
                n += 1 # Se agrega al nuevo cliente en el sistema
            
            else:
                # si el proximo tiempo de llegada es después del próximo tiempo de salida, se atiende ya que
                cajasPED = np.argmin(setTiempo) 
                t = setTiempo[cajasPED] 
                i_salida.append(t)
                if n <= self.cajas: # Si hay menos o igual cantidad de clientes que cajas
                    cajases[cajasPED] = 0
                    setTiempo[cajasPED] = np.infty
                else: # Hay mas clientes por atender
                    cajasNo.append(cajasPED) 
                    cliente_TE = np.append(cliente_TE,t - i_llegada[len(i_llegada)-1])

                    setTiempo[i] = t + np.random.exponential(25) 

                    tiempoOcupado[cajasPED] += setTiempo[cajasPED]-t
                    cajases[i] = 1 
                n -= 1 # Descontamos al cliente atendido del sistema
                
        # se calcula cuantas solicitudes atendio cada caja 
        numSolicitudes = np.zeros(self.cajas)
        for i in range(len(cajasNo)):
            numSolicitudes[cajasNo[i]] += 1

        return { 
            "en_cola": cliente_TE, "numSolicitudes": numSolicitudes, "setTiempo": setTiempo, "i_llegada": i_llegada, "i_salida": i_salida, "tiempoOcupado": tiempoOcupado
        }


counter = 9 # Numero de cajas

# ## Pizzita Computing
FdS = Supermarket(max_sol=6, cajas=counter)
resultados_FdS = FdS.simulate()
print(Fore.GREEN + ">>>>>>>  Flor de Septiembre" + Style.RESET_ALL)
print(Fore.GREEN + ">>>>>>>  6 solicitudes máximas" + Style.RESET_ALL)
print(Fore.GREEN + ">>>>>>>  Simulación de 8 horas laborales" + Style.RESET_ALL)
print("1. ¿Cuántas solicitudes atendió cada cajas?")
print(resultados_FdS["numSolicitudes"][0], "min")
print("\n2. ¿Cuánto tiempo estuvo cada cajas ocupado?")
print(resultados_FdS["tiempoOcupado"][0], "min")
print("\n3. ¿Cuánto tiempo estuvo cada cajas desocupado (idle)?")
print(np.maximum(np.ones(FdS.cajas)*60 - resultados_FdS["tiempoOcupado"],0)[0], "min")
print("\n4. Cuánto tiempo en total estuvieron las solicitudes en cola?")
print(np.round(sum(resultados_FdS["en_cola"]),5), "min")
print("\n5. En promedio ¿cuánto tiempo estuvo cada solicitud en cola?")
print(np.round(np.mean(resultados_FdS["en_cola"]),5), "min")
print("\n6. En promedio, ¿cuántas solicitudes estuvieron en cola cada minuto?")
sol_psec = [ 1/num if num != 0 else 0 for num in resultados_FdS["en_cola"] ]
print(np.round(np.mean(sol_psec),5), "min")
print("\n7. ¿Cuál es el momento de la salida de la última solicitud?")
print(np.round(resultados_FdS["setTiempo"][-1],5), "min")

