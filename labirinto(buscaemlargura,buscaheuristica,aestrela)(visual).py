from tkinter import *
from heapq import heappush, heappop,heapify
import time
import numpy as np

root = Tk()
root.title("Labirinto")
root.geometry("650x500+320+120")
root.configure(bg='white')
root.resizable(False, False)

def pisosEmVolta(piso,matriz):                          # salvando as posições possiveis em volta do piso atual
   pisos=[]
   x,y=piso     
   xm=len(matriz)   
   ym=len(matriz[0])
   if(x+1 <xm and matriz[x+1][y]!='blue'):
      pisos.append((x+1,y))
   if(y+1 <ym and matriz[x][y+1]!='blue'):
      pisos.append((x,y+1))
   if(x-1 >=0 and matriz[x-1][y]!='blue'):
      pisos.append((x-1,y))
   if(y-1 >= 0 and matriz[x][y-1]!='blue'):
      pisos.append((x,y-1))
   return pisos

def paraString(proximopiso):                            #convertendo posição para string para ultilizala como indice
   return str(proximopiso[0])+","+str(proximopiso[1])      


def pintarMatriz(percorridos,corcaminho,i):
    h=horizontal.get()                    # tamanho horizontal
    v=vertical.get()                      # tamanho vertical
    quadrados=root.winfo_children()       # lendo toda tela
    quadrados=quadrados[-(v*h):]          # pegando ultimos valores relacionados a matriz
    m = np.reshape(quadrados, (v, h))     # convertendo a lista em uma matriz

    for pisos in percorridos:             # percorrendo pelo caminho correto
        x,y=pisos                         # extraindo a posição do piso
        quadrado=m[x][y]                  # procurando o piso na matriz de botões
        if(quadrado['background']!='red' 
        and quadrado['background']!='green'): # se o quadrado nao for verde ou veremlho entao pinte
            quadrado['background']=corcaminho # pintando o botao com a cor, desenhando o caminho

def h1(inicio,fim): # distancia 
  x1,y1=inicio
  x2,y2=fim
  soma= (x2-x1)**2 + (y2-y1)**2    
  distancia=soma **(1/2)           #raiz quadrada
  return distancia  


def busca_heuristica(inicio,fim,matriz,heuristica):
   global tempo
   fila     =[]        
   heappush(fila,(heuristica(inicio,fim),inicio))              
   visitados=[inicio]
   caminhos =dict()
   while(len(fila)>0):
      (_,piso)=heappop(fila)
      root.after(tempo,None)                            # pausa
      pintarMatriz(visitados,"gray",0)                  # printa matriz
      root.update()                                     # depois atualiza a tela do usuario
      for proximopiso in pisosEmVolta(piso,matriz):       
         if proximopiso not in visitados:            
            visitados.append(proximopiso)
            caminhos[paraString(proximopiso)]=piso
            print('proximopiso=',proximopiso,'fim=',fim)
            if proximopiso == fim:
               caminho=[]
               passo=proximopiso
               while(passo!=inicio):
                  caminho.append(passo)
                  passo=caminhos[paraString(passo)]         
                  root.after(tempo,None)             #pausa
                  pintarMatriz(caminho,"orange",0)     #printa matriz
                  root.update()                        #atualiza tela usuario
               caminho.append(inicio)
               caminho.reverse()
               pintarMatriz(caminho,"orange",0)
               print(caminho)
               return 
            else:
               heappush(fila,(heuristica(proximopiso,fim),proximopiso))

def busca_em_largura(inicio,fim,matriz):
   global tempo
   fila     =[inicio]                      
   visitados=[inicio]
   caminhos =dict()
   while(len(fila)>0):
      piso=fila[0]
      del fila[0]
      root.after(tempo,None)                            # pausa
      pintarMatriz(visitados,"gray",0)                  # printa matriz
      root.update()                                     # depois atualiza a tela do usuario
      for proximopiso in pisosEmVolta(piso,matriz):       
         if proximopiso not in visitados:            
            visitados.append(proximopiso)
            caminhos[paraString(proximopiso)]=piso
            print('proximopiso=',proximopiso,'fim=',fim)
            if proximopiso == fim:
               caminho=[]
               passo=proximopiso
               while(passo!=inicio):
                  caminho.append(passo)
                  passo=caminhos[paraString(passo)]         
                  root.after(tempo,None)             #pausa
                  pintarMatriz(caminho,"orange",0)     #printa matriz
                  root.update()                        #atualiza tela usuario
               caminho.append(inicio)
               caminho.reverse()
               pintarMatriz(caminho,"orange",0)
               print(caminho)
               return 
            else:
               fila.append(proximopiso)
def a_estrela(inicio,fim,matriz,heuristica):
   global tempo
   fila     =[]
   custo=0        
   heappush(fila,(heuristica(inicio,fim),inicio,custo))              
   visitados=[inicio]
   caminhos =dict()
   while(len(fila)>0):
      (_,piso,custo)=heappop(fila)
      root.after(tempo,None)                            # pausa
      pintarMatriz(visitados,"gray",0)                  # printa matriz
      root.update()                                     # depois atualiza a tela do usuario
      for proximopiso in pisosEmVolta(piso,matriz):       
         if proximopiso not in visitados:            
            visitados.append(proximopiso)
            caminhos[paraString(proximopiso)]=piso
            print('proximopiso=',proximopiso,'fim=',fim)
            if proximopiso == fim:
               caminho=[]
               passo=proximopiso
               while(passo!=inicio):
                  caminho.append(passo)
                  passo=caminhos[paraString(passo)]         
                  root.after(tempo,None)             #pausa
                  pintarMatriz(caminho,"orange",0)     #printa matriz
                  root.update()                        #atualiza tela usuario
               caminho.append(inicio)
               caminho.reverse()
               pintarMatriz(caminho,"orange",0)
               print(caminho)
               return 
            else:
               heappush(fila,(heuristica(proximopiso,fim)+custo+1,proximopiso,custo+1))                 
           

def lerMatriz():
    ini=None
    fim=None
    h=horizontal.get()                          # tamanho horizontal
    v=vertical.get()                            # tamanho vertical
    quadrados=root.winfo_children()             # lendo toda tela
    quadrados=quadrados[-(v*h):]                # pegando ultimos valores relacionados a matriz
    matriz = np.reshape(quadrados, (v, h))      # convertendo a lista em uma matriz
    
    for i in range (v):                 
        for j in range (h):
            if(matriz[i][j]['background']=='gray' or matriz[i][j]['background']=='orange'):
                matriz[i][j]['background']= 'white' 
            quadrado=matriz[i][j]
            quadrado=quadrado['background']     # convertendo a matriz em cores
            matriz[i][j]= quadrado
            if(quadrado=='red'):
                ini=(i,j)                       # pegando a posição inicial
            if(quadrado=='green'):              
                fim=(i,j)                       # pegando a posição final
        
    return ini,fim,matriz

metodo="busca em largura"
def alterarMetodo(botao):
    global metodo
    if(botao['text']=="busca em largura"):
        metodo="busca heuristica"
    elif(botao['text']=="busca heuristica"):
        metodo="    a estrela    "
    elif(botao['text']=="    a estrela    "):
        metodo="busca em largura"
    botao['text']=metodo

def encontrarCaminho():
    global metodo
    (inicio,fim,matriz)=lerMatriz()
    if metodo == "busca em largura":
        busca_em_largura(inicio,fim,matriz)
    elif metodo == "busca heuristica":
        busca_heuristica(inicio,fim,matriz,h1)
    elif metodo == "    a estrela    ":
        a_estrela(inicio,fim,matriz,h1)


cor='white'
def corVerde():                 # funções para alterar cores pintadas
    global cor
    cor='green'
def corVermelha():
    global cor
    cor='red'
def corAzul():
    global cor
    cor='blue'
def corBranca():
    global cor
    cor='white'

botaoVerde=None                # variavel que salva botão anterior, para não existir dois inicios ou finais
botaoVermelho=None

def setCor(botao):             #função para alterar a cor dos pisos
    global cor
    global botaoVerde
    global botaoVermelho
    if(cor=='green'):
        if(botaoVerde!=None):
            botaoVerde.configure(bg="white")
        botaoVerde=botao
    if(cor=='red'):
        if(botaoVermelho!=None):
            botaoVermelho.configure(bg="white")
        botaoVermelho=botao
    botao.configure(bg=cor)

clicando=False
def modo_arrastar(e):                               #função ativada ao arrastar
    global cor
    if(clicando==True):
        if(cor!='red' and cor!= 'green' ):
            e.widget['background'] = cor           # muda cor do objeto com o mouse em cima

def ativa_modo_arrastar(e):                         #função que ativa a função de arrastar após o clique
    global clicando
    if(clicando==True):
        clicando=False
    elif(clicando==False):
        if(cor!='red' and cor!= 'green' ):
            clicando=True


def slide(var):
    global botaoVerde
    global botaoVermelho
    
    h=horizontal.get()                          # tamanho horizontal
    v=vertical.get()                            # tamanho vertical
    quadrados=root.winfo_children()
    quadrados=quadrados[(10):]                 

    for quadrado in quadrados:        
            quadrado.destroy()                  # destruindo todos os quadrados quadrados

    GD=Label(root, text="   " ,font=('arial', 28, 'bold')) # label auxiliar(excluir depois...)
    GD.grid(row=0,column=0)
    
    for i in range(0,v):
        for j in range (0,h):
            button1 = Button(root,text="   ",bg="white") #criando os botões de pisos
            if(i==0 and j==0):              #Iniciando botao vermelho
                button1["background"]='red'
                botaoVermelho=button1
            elif(i==v-1 and j==h-1):        #Iniciando botao verde
                button1["background"]='green'
                botaoVerde=button1 
            button1.config(command=lambda button=button1:setCor(button)) 
            button1.bind("<Enter>", modo_arrastar)            #inicializando eventos
            button1.bind("<Button>", ativa_modo_arrastar)     #inicializando eventos
            GD=button1 
            GD.grid(row=i+1,column=j+1)         # adicionando o botão no grid
tempo=0
def alterartempo(var): #tempo de pausa da função de busca
    global tempo
    tempo=velocidade.get()

#configuração dos botões e sliders da tela 
horizontal = Scale(root,from_=0,to=30,orient= HORIZONTAL,length=600)
horizontal.bind("<ButtonRelease>",slide)
horizontal.place(x=30,y=0)
vertical = Scale(root,from_=0,to=15,orient= VERTICAL,length=400)
vertical.bind("<ButtonRelease>",slide)
vertical.place(x=0,y=40)
velocidade = Scale(root,from_=0,to=1000,orient= HORIZONTAL,command=alterartempo,length=250)
velocidade.place(x=390,y=450)
Inicio=Button(root,text="Inicio",bg='red',command=corVermelha)
Inicio.place(x=0,y=450,height=50)
Fim=Button(root,text="Fim",bg='green',command=corVerde)
Fim.place(x=40,y=450,height=50)
Obstaculo=Button(root,text="Obstaculo",bg='blue',command=corAzul)
Obstaculo.place(x=70,y=450,height=50)
Branco=Button(root,text="Branco",bg='white',command=corBranca)
Branco.place(x=130,y=450,height=50)
escolherMetodo=Button(root,text="busca em largura",bg='gray')
escolherMetodo.config(command=lambda button=escolherMetodo:alterarMetodo(button)) 
escolherMetodo.place(x=177,y=450,height=50)
encontrarCaminho=Button(root,text="Encontrar Caminho",bg='orange',command=encontrarCaminho)
encontrarCaminho.place(x=278,y=450,height=50)
labelVelocidade=Label(root,text="Lentidão")
labelVelocidade.place(x=500,y=435)

horizontal.set(3)
vertical.set(3)
velocidade.set(32)
slide(None)

root.mainloop()


    
