import copy

m=[[0,0,0,1,0,0,0,0],
   [0,1,0,1,0,1,1,0],
   [0,1,0,0,0,1,1,0]]

inicio=(0,0)
fim   =(2,7)

def pisosEmVolta(piso,matriz):
   pisos=[]                            
   x,y=piso     
   xm=len(matriz)   
   ym=len(matriz[0])
   if(x+1 <xm and matriz[x+1][y]==0):
      pisos.append((x+1,y))
   if(y+1 <ym and matriz[x][y+1]==0):
      pisos.append((x,y+1))
   if(x-1 >=0 and matriz[x-1][y]==0):
      pisos.append((x-1,y))
   if(y-1 >= 0 and matriz[x][y-1]==0):
      pisos.append((x,y-1))
   return pisos

def paraString(proximopiso):
   return str(proximopiso[0])+","+str(proximopiso[1])

def bfs(inicio,fim,matriz):
   counter  =0
   fila     = [inicio]
   visitados= [inicio]
   caminhos = dict()
   while(len(fila)>0):
      piso=fila[0]
      del fila[0]
      for proximopiso in pisosEmVolta(piso,matriz):         
         printarMatriz(matriz,piso,'x')
         if proximopiso not in visitados:
            visitados.append(proximopiso)
            caminhos[paraString(proximopiso)]=piso
            if proximopiso == fim:
               caminho=[]
               passo=proximopiso
               while(passo!=inicio):
                  caminho.append(passo)
                  passo=caminhos[paraString(passo)]
                  print("Modo Reverso",end='\n\n')
                  printarMatriz(matriz,passo,'s')
               caminho.append(inicio)
               caminho.reverse()
               print ("encontrou")
               print(caminho)
               return 
            else:
               fila.append(proximopiso)
            print("Passo (",counter,")",end='\n\n')
            counter+=1
            
def printarMatriz(matriz,piso,caminho):
   x,y=piso
   xm=len(matriz)   
   ym=len(matriz[0])
   m2=matriz.copy()
   m2[x][y]=caminho
 
   for i in range (0,xm):
      for j in range (0,ym):
         print(m2[i][j],end=' ')
      print("")
   print("")

bfs(inicio,fim,m)