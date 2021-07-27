# Algoritmo criado para ajudar a entender os algoritmos de busca
# https://github.com/JoseGabrielNF
from tkinter import *
from heapq import heappush, heappop,heapify
import time
import numpy as np

#inicializando janela
root = Tk()
root.title("Labirinto")
root.geometry("650x500+320+120")
root.configure(bg='white')
root.resizable(False, False)


# variaveis globais
metodo="busca em largura"      # variavel que salva o metodo sendo utilizado
botaoVerde=None                # variavel que salva botão anterior, para não existir dois inicios 
botaoVermelho=None             # variavel que salva botão anterior, para não existir dois finais 
cor='white'                    # variavel que salva a cor atual a ser pintada na tela.
clicando=False                 # variavel que salva quando o usuario para de pintar
tempo=0                        # variavel que salva a lentidão do algoritimo

# função que verifica em volta da posição atual
def pisosEmVolta(piso,matriz):                          # salvando as posições possiveis em volta do piso atual
   pisos=[]                                             # inicializando lista de pisos
   x,y=piso                                             # extraindo posição do piso atual
   xm=len(matriz)                                       # extraindo dimensão da matriz
   ym=len(matriz[0])                                    # extraindo dimensão da matriz
   if(x+1 <xm and matriz[x+1][y]!='blue'):              # se m[x+1][y] for possivel
        pisos.append((x+1,y))                           # então adicione a posição na lista de piso em volta
   if(y+1 <ym and matriz[x][y+1]!='blue'):              # se m[x][y+1] for possivel
        pisos.append((x,y+1))                           # então adicione a posição na lista de piso em volta
   if(x-1 >=0 and matriz[x-1][y]!='blue'):              # se m[x-1][y] for possivel
        pisos.append((x-1,y))                           # então adicione a posição na lista de piso em volta
   if(y-1 >= 0 and matriz[x][y-1]!='blue'):             # se m[x][y-1] for possivel
        pisos.append((x,y-1))                           # então adicione a posição na lista de piso em volta       
   return pisos                                         # retornar pisos possiveis

#converte posição para string para ser utilizada como indice   
def paraString(proximopiso):                            
   return str(proximopiso[0])+","+str(proximopiso[1])   

def pintarMatriz(piso,corcaminho):
    h=horizontal.get()                           # tamanho horizontal
    v=vertical.get()                             # tamanho vertical
    quadrados=root.winfo_children()              # lendo toda tela
    quadrados=quadrados[-(v*h):]                 # pegando ultimos valores relacionados a matriz
    m = np.reshape(quadrados, (v, h))            # convertendo a lista em uma matriz

    x,y=piso                                 # extraindo a posição do piso
    quadrado=m[x][y]                         # posição do piso na matriz de botões
    if(quadrado['background']!='red' 
    and quadrado['background']!='green'):    # se o quadrado nao for verde ou veremlho entao pinte
        quadrado['background']=corcaminho    # pintando o botao com a cor, desenhando o caminho
        quadrado.update()                    # atualizando a tela

#distancia euclidiana
def h1(inicio,fim):                 
    x1,y1=inicio                            # extraindo posição inicial
    x2,y2=fim                               # extraindo posição final
    soma= (x2-x1)**2 + (y2-y1)**2           # calculando distancia euclidiana
    distancia=soma **(1/2)                  # operação de raiz quadrada
    return distancia  
#distancia manhatam
def h2(inicio,fim):
    x1,y1=inicio                            # extraindo posição inicial
    x2,y2=fim                               # extraindo posição final
    distancia = abs(x1-x2) + abs(y1-y2)     # calculando distancia manhatan
    return distancia  


def busca_heuristica(inicio,fim,matriz,heuristica):
    global tempo                                                # referencia da variavel tempo
    fila     =[]                                                # inicializando uma fila 
    heappush(fila,(heuristica(inicio,fim),inicio))              # transformando a fila em uma heap, e inserindo um valor de heuristica,junto com a posição inicial
    visitados=[inicio]                                          # fila de visitados incluindo a posição inicial
    caminhos =dict()                                            # dicionario para salvar o caminho final
    while(len(fila)>0):                                         # condição de parada
        (_,piso)=heappop(fila)                                  # pegando o piso com o menor valor de heuristica da heap, no caso menor distancia
        root.after(tempo,None)                                  # pausa
        for proximopiso in pisosEmVolta(piso,matriz):           # um laço que percorre por todas as poções em volta [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]  
            if proximopiso not in visitados:                    # se o proximo piso não estiver na lista de visitados,
                visitados.append(proximopiso)                   # então adicione ele na lista de visitados
                caminhos[paraString(proximopiso)]=piso          # adicione no dicionario de caminhos,onde o proximo piso vai ser um indice para o piso anterior
                if proximopiso == fim:                          # se o proximo piso for o final, então encontrou. exemplo (2,2)==(2,2)
                    caminho=[]                                  # inicializa fila caminho
                    passo=proximopiso                           # adiciona o proximopiso em um passo do caminho
                    while(passo!=inicio):                       # percorre passo a passo do final até o inicio
                        caminho.append(passo)                   # adiciona passo na lista de caminho
                        passo=caminhos[paraString(passo)]       # adiciona o proximo passo, baseando se no indice de caminhos definidos   
                        root.after(tempo,None)                  # pausa
                        pintarMatriz(passo,"orange")          # pinta matriz
                    caminho.append(inicio)                      # adicionando a posição inicial no caminho
                    caminho.reverse()                           # revertendo a lista 
                    return caminho                              # retorna lista do caminho encontrado
                else:                                           # se não for o final
                    pintarMatriz(proximopiso,"gray")            # pinta matriz
                    heappush(fila,(heuristica(proximopiso,fim),proximopiso)) # adicione o proximo piso na heap de pisos a serem percorridos, com a heuristica
    return "Caminho não encontrado"

def busca_em_largura(inicio,fim,matriz):
    global tempo                                                # referencia da variavel tempo
    fila     =[inicio]                                          # fila com a posição inicial
    visitados=[inicio]                                          # fila de visitados incluindo a posição inicial
    caminhos =dict()                                            # dicionario para salvar o caminho final
    while(len(fila)>0):                                         # condição de parada
        piso=fila[0]                                            # escolhendo o piso da fila como piso atual
        del fila[0]                                             # deletando o piso da fila para não repetir
        root.after(tempo,None)                                  # pausa                 
        for proximopiso in pisosEmVolta(piso,matriz):           # um laço que percorre por todas as poções em volta [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]  
            if proximopiso not in visitados:                    # se o proximo piso não estiver na lista de visitados,
                visitados.append(proximopiso)                   # então adicione ele na lista de visitados
                caminhos[paraString(proximopiso)]=piso          # adicione no dicionario de caminhos,onde o proximo piso vai ser um indice para o piso anterior
                if proximopiso == fim:                          # se o proximo piso for o final, então encontrou. exemplo (2,2)==(2,2)
                    caminho=[]                                  # inicializa fila caminho
                    passo=proximopiso                           # adiciona o proximopiso em um passo do caminho
                    while(passo!=inicio):                       # percorre passo a passo do final até o inicio
                        caminho.append(passo)                   # adiciona passo na lista de caminho
                        passo=caminhos[paraString(passo)]       # adiciona o proximo passo, baseando se no indice de caminhos definidos   
                        root.after(tempo*2,None)                # pausa
                        pintarMatriz(passo,"orange")          # pinta matriz
                    caminho.append(inicio)                      # adicionando a posição inicial no caminho
                    caminho.reverse()                           # revertendo a lista 
                    return caminho                              # retorna lista do caminho encontrado
                else:                                           # se não for o final
                    pintarMatriz(proximopiso,"gray") 
                    fila.append(proximopiso)                    # adicione o proximo piso na lista de pisos a serem percorridos
    return "Caminho não encontrado"                             # retorne uma string caso não encontre

def a_estrela(inicio,fim,matriz,heuristica):
    global tempo                                                # referencia da variavel tempo
    fila     =[]                                                # inicializando uma fila 
    custo=0                                                     # custo do caminho
    heappush(fila,(heuristica(inicio,fim),inicio,custo))        # transformando a fila em uma heap e inserindo um valor de heuristica, junto com a posição inicial em um custo      
    visitados=[inicio]                                          # fila de visitados incluindo a posição inicial
    caminhos =dict()                                            # dicionario para salvar o caminho final
    while(len(fila)>0):                                         # condição de parada
        (_,piso,custo)=heappop(fila)                            # pegando o piso com o menor valor de heuristica da heap, no caso menor distancia e menor custo
        root.after(tempo,None)                                  # pausa
        for proximopiso in pisosEmVolta(piso,matriz):           # um laço que percorre por todas as poções em volta [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]  
            if proximopiso not in visitados:                    # se o proximo piso não estiver na lista de visitados,
                visitados.append(proximopiso)                   # então adicione ele na lista de visitados
                caminhos[paraString(proximopiso)]=piso          # adicione no dicionario de caminhos,onde o proximo piso vai ser um indice para o piso anterior
                if proximopiso == fim:                          # se o proximo piso for o final, então encontrou. exemplo (2,2)==(2,2)
                    caminho=[]                                  # inicializa fila caminho
                    passo=proximopiso                           # adiciona o proximopiso em um passo do caminho
                    while(passo!=inicio):                       # percorre passo a passo do final até o inicio
                        caminho.append(passo)                   # adiciona passo na lista de caminho
                        passo=caminhos[paraString(passo)]       # adiciona o proximo passo, baseando se no indice de caminhos definidos   
                        root.after(tempo,None)                  # pausa
                        pintarMatriz(passo,"orange")            # pinta matriz
                    caminho.append(inicio)                      # adicionando a posição inicial no caminho
                    caminho.reverse()                           # revertendo a lista   
                    return caminho                              # retorna lista do caminho encontrado
                else:                                           # se não for o final 
                    pintarMatriz(proximopiso,"gray")            # pinta matriz
                    heappush(fila,(heuristica(proximopiso,fim)+custo+1,proximopiso,custo+1))# adicione o proximo piso na heap de pisos a serem percorridos, com a heuristica, e soma o custo                 
    return "Caminho não encontrado" 

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

def alterarMetodo(botao):
    global metodo
    if(botao['text']=="busca em largura"):
        metodo="busca heuristica"
    elif(botao['text']=="busca heuristica"):
        metodo="    a estrela    "
    elif(botao['text']=="    a estrela    "):
        metodo="busca em largura"
    botao['text']=metodo
    root.title(metodo)

def encontrarCaminho():
    global metodo
    (inicio,fim,matriz)=lerMatriz()
    if metodo == "busca em largura":
        caminho=busca_em_largura(inicio,fim,matriz)
    elif metodo == "busca heuristica":
        caminho=busca_heuristica(inicio,fim,matriz,h1)
    elif metodo == "    a estrela    ":
        caminho=a_estrela(inicio,fim,matriz,h1)
    print("Caminho Encontrado:",caminho)

 # funções para alterar cores pintadas
def corVerde():                
    global cor
    cor='green'
def corVermelha():
    global cor
    cor='red'
def corAzul():
    global cor
    global clicando
    clicando=False
    cor='blue'
def corBranca():
    global cor
    global clicando
    clicando=False
    cor='white'

#função para alterar a cor dos pisos
def setCor(botao):             
    global cor
    global botaoVerde
    global botaoVermelho
    if(cor=='green'):                            # se a cor for verde
        if(botaoVerde!=None):                      
            botaoVerde.configure(bg="white")     # o verde anterior vai ser branco
        botaoVerde=botao                         # o botão atual vai ser verde
    if(cor=='red'):                              # se a cor for vermelho
        if(botaoVermelho!=None):
            botaoVermelho.configure(bg="white")  # o vermelho anterior vai ser branco
        botaoVermelho=botao                      # o botão atual vai ser vermelho
    botao.configure(bg=cor)                      # trocar cor do botão atual

#função ativada ao arrastar
def modo_arrastar(e):                               
    global cor
    global clicando 
    if(clicando==True):                            # se clicar
        if(cor!='red' and cor!= 'green' ):
            e.widget['background'] = cor           # muda cor do objeto com o mouse em cima

#função que ativa a função de arrastar após o clique
def ativa_modo_arrastar(e):   
    global cor                      
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
    quadrados=quadrados[(10):]                  # pegando tudo que não faz parte da interface, que são os quadrados

    for quadrado in quadrados:        
            quadrado.destroy()                  # destruindo todos os quadrados 
    GD=Label(root, text="   " ,font=('arial', 28, 'bold')) # label auxiliar(excluir depois...)
    GD.grid(row=0,column=0)

    
    for i in range(0,v):
        for j in range (0,h):
            button1 = Button(root,text="",bg="white")                #criando os botões de pisos
            if(i==0 and j==0):                                          #Iniciando botao vermelho
                button1["background"]='red'
                botaoVermelho=button1
            elif(i==v-1 and j==h-1):                                     #Iniciando botao verde
                button1["background"]='green'
                botaoVerde=button1 
            button1.config(command=lambda button=button1:setCor(button)) #
            button1.bind("<Enter>", modo_arrastar)                       #inicializando eventos
            button1.bind("<Button>", ativa_modo_arrastar)                #inicializando eventos
            GD=button1 
            GD.grid(row=i+1,column=j+1)                                  # adicionando o botão no grid
            GD.columnconfigure(1, weight=500)
def alterartempo(var): #tempo de pausa da função de busca
    global tempo
    tempo=velocidade.get()

#configuração dos botões e sliders da tela 
horizontal = Scale(root,from_=0,to=55,orient= HORIZONTAL,length=600)
horizontal.bind("<ButtonRelease>",slide)
horizontal.place(x=30,y=0)
vertical = Scale(root,from_=0,to=15,orient= VERTICAL,length=400)
vertical.bind("<ButtonRelease>",slide)
vertical.place(x=0,y=40)
velocidade = Scale(root,from_=0,to=500,orient= HORIZONTAL,command=alterartempo,length=250)
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
velocidade.set(10)
slide(None)

root.mainloop()


    
