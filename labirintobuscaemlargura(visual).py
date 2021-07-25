from tkinter import *
import time
import numpy as np

root = Tk()
root.title("Labirinto")
root.geometry("650x500+120+120")
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
        quadrado['background']=corcaminho # pintando o botao com a cor, desenhando o caminho


def bfs(inicio,fim,matriz):
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
                  root.after(tempo*2,None)             #pausa
                  pintarMatriz(caminho,"orange",0)     #printa matriz
                  root.update()                        #atualiza tela usuario
               caminho.append(inicio)
               caminho.reverse()
               pintarMatriz(caminho,"orange",0)
               print(caminho)
               return 
            else:
               fila.append(proximopiso)
           

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
            quadrado=matriz[i][j]
            quadrado=quadrado['background']     # convertendo a matriz em cores
            matriz[i][j]= quadrado
            if(quadrado=='red'):
                ini=(i,j)                       # pegando a posição inicial
            if(quadrado=='green'):              
                fim=(i,j)                       # pegando a posição final
    
    return ini,fim,matriz

def encontrarCaminho():
    (inicio,fim,matriz)=lerMatriz()
    bfs(inicio,fim,matriz)


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
        clicando=True

def slide(var):
    global botaoVerde
    global botaoVermelho
    
    h=horizontal.get()                          # tamanho horizontal
    v=vertical.get()                            # tamanho vertical
    quadrados=root.winfo_children()
    quadrados=quadrados[(9):]                 

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
horizontal = Scale(root,from_=0,to=30,orient= HORIZONTAL,command=slide,length=600)
horizontal.place(x=30,y=0)
vertical = Scale(root,from_=0,to=15,orient= VERTICAL,command=slide,length=400)
vertical.place(x=0,y=40)
velocidade = Scale(root,from_=0,to=300,orient= HORIZONTAL,command=alterartempo,length=300)
velocidade.place(x=360,y=450)
Inicio=Button(root,text="Inicio",bg='red',command=corVermelha)
Inicio.place(x=0,y=450,height=50)
Fim=Button(root,text="Fim",bg='green',command=corVerde)
Fim.place(x=40,y=450,height=50)
Obstaculo=Button(root,text="Obstaculo",bg='blue',command=corAzul)
Obstaculo.place(x=70,y=450,height=50)
Branco=Button(root,text="Branco",bg='white',command=corBranca)
Branco.place(x=130,y=450,height=50)
encontrarCaminho=Button(root,text="Encontrar Caminho",bg='orange',command=encontrarCaminho)
encontrarCaminho.place(x=250,y=450,height=50)
labelVelocidade=Label(root,text="Pausa")
labelVelocidade.place(x=500,y=430)
horizontal.set(3)
vertical.set(3)
velocidade.set(1)

root.mainloop()


    
