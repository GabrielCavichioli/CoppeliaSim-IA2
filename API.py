# Autor: Gabriel Antonio Cavichioli | Data: 29/05/24.

#____________________________________________INICIALIZAÇÃO__________________________________________________________________
try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

print ('Program started')
sim.simxFinish(-1) # Como segurança, fecha outras conexões
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Conecta ao CoppeliaSimx, API simples
#clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Conecta ao CoppeliaSim, API contínua, precisa-se configurar a porta, caso contrário não funcionará

print (clientID) # Apresentando o ID do cliente

if clientID!=-1: # Teste para verificar se a conexão foi bem sucedida
    print ('Connected to remote API server')
    
    # sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot) somente em API contínua

    # Tentando coletar dados em modo blocking fashion (i.e. a service call):
    res, objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)

    if res==sim.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)

    time.sleep(2)

    # ______________________________________TENTATIVA_DE_LEITURA_____________________________________________________________

    # "Real time mode"
    startTime=time.time()
    lastTime = startTime
    t=0
    while t < 10:

        now = time.time()
        dt = now - lastTime

        # Handle para o robô
        robotname = 'base'
        returnCode, robotHandle = sim.simxGetObjectHandle(clientID, robotname, sim.simx_opmode_oneshot_wait)   

        # Tentativa de leitura da posição do robô
        returnCode, pos = sim.simxGetObjectPosition(clientID, robotHandle, -1, sim.simx_opmode_oneshot_wait)        
        print('Pos: ', pos)

        t = t + dt  
        lastTime = now

    #____________________________________________FINALIZAÇÃO_________________________________________________________________

    # sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot) somente em API contínua

    sim.simxFinish(clientID) # Finalizando a API
    
else:
    print ('Failed connecting to remote API server')
    
print ('Program ended')