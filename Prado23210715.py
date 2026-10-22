"""
Práctica 1: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Briseida Prado Acosta
Número de control: 23210715
Correo institucional: 23210715@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control numpy matplotlib
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import control as ctrl 
from scipy import signal
import matplotlib.pyplot as plt 
import pandas as pd

# Datos de la simulación
u= np.array (pd.read_excel('senal.xlsx',header=None))
x0,t0,tend,dt,w,h = 0,0,15,1E-3,10,5
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u = np. reshape(signal.resample(u,len(t)),-1)

def cardio (Z,L,R,C):
    num = [L*R,R*Z]
    den = [C*L*R*Z , L*R+L*Z,R*Z]
    sys = ctrl.tf (num, den)
    L = np.roots(den)
    return sys,L

#Funcion de transferencia: Hipotenso 
Z,L,R,C = 0.010, 0.001, 1.00,3.500
syshipo,L= cardio (Z,L,R,C)
print (f'Funcióm de transferencia del hipotenso (caso 1): {syshipo}')
print (f"Polos del sistema L1 = {L[0]:.3e}, L2 = {L[1]: .3e}\n")

#Funcion de transferencia: Normotenso 
Z,L,R,C = 0.010, 0.001, 1.00,3.500
sysnormo,L= cardio (Z,L,R,C)
print (f'Funcióm de transferencia del normotenso (caso 1): {sysnormo}')
print (f"Polos del sistema L1 = {L[0]:.3e}, L2 = {L[1]: .3e}\n")

#Funcion de transferencia: Hipertenso 
Z,L,R,C = 0.010, 0.001, 1.00,3.500
syshiper,L= cardio (Z,L,R,C)
print (f'Funcióm de transferencia del hipertenso (caso 2): {syshiper}')
print (f"Polos del sistema : L1 = {L[0]:.3e}, L2 = {L[1]: .3e}\n")

#Respuestas en lazo abierto
_,PpN = ctrl.forced_response(sysnormo,t,u,x0)
_,PpL = ctrl.forced_response(syshipo,t,PpN,x0)
_,PpH = ctrl.forced_response(syshiper,t,PpN,x0)

clr1 = np.array([66,91,154])/255;
clr2 = np.array([40,122,116])/255;
clr3 = np.array([151,40,40])/255;

fg1 = plt.figure()
plt.plot(t,PpN,'-',linewidth=0.5,color= clr1,label= 'Pp(t):Normotenso')
plt.plot(t,PpL,'-',linewidth=0.5,color= clr2,label= 'Pp(t):Hipertenso')
plt.plot(t,PpH,'-',linewidth=0.5,color= clr3,label= 'Pp(t):Hipotenso')
plt.grid(False)
plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))
plt.xlabel('t(s)')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.2), loc = 'center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('individuos_python.pdf')

#Controlador PID
def controlador(kP,kI,kD, sys):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    Ce = kD /Rr
    numPID = [Re*Rr*Ce*Cr,(Re*Ce+Rr*Cr),1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID, denPID)
    sysPID = ctrl.feedback (ctrl.series(PID,sys),1,sign=-1)
    return sysPID
hipoPID = controlador(458.483, 1112094.736,0.00627, syshipo)
print(f'Función de transferencia del hipotenso en lazo cerrado: syshipo')
hiperPID = controlador (126.595, 293327.703,0.00140, syshiper)
print(f'Función de transferencia del hipertenso en lazo cerrado: syshiperPID')

#Respuestas del sistema de control en lazo cerrado
_,PIDL = ctrl.forced_response(hipoPID,t,PpN,x0)
_,PIDH = ctrl.forced_response(hiperPID,t,PpN,x0)

fg2 = plt.figure()
plt.plot(t,PpL,'-',linewidth=0.5,color= clr1,label= 'Pp(t):Hipotenso')
plt.plot(t,PpN,'-',linewidth=0.5,color= clr2,label= 'Pp(t):Normotenso')
plt.plot(t,PpH,'-',linewidth=0.5,color= clr3,label= 'Pp(t):Hipotenso')
plt.grid(False)
plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))
plt.xlabel('t(s)')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.2), loc = 'center',ncol=3)
plt.show()
fg2.set_size_inches(w,h)
fg2.tight_layout()
fg2.savefig('hipotenso_python.pdf')

fg3 = plt.figure()
plt.plot(t,PpL,'-',linewidth=0.5,color= clr1,label= 'Pp(t):Hipertenso')
plt.plot(t,PpN,'-',linewidth=0.5,color= clr2,label= 'Pp(t):Normotenso')
plt.plot(t,PpH,'-',linewidth=0.5,color= clr3,label= 'Pp(t):Hipotenso')
plt.grid(False)
plt.xlim(0,15); plt.xticks(np.arange(0,16,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))
plt.xlabel('t(s)')
plt.ylabel('Pp(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.2), loc = 'center',ncol=3)
plt.show()
fg3.set_size_inches(w,h)
fg3.tight_layout()
fg3.savefig('hipertenso_python.pdf')


