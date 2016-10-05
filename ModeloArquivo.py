## This Python file uses the following encoding: utf-8
#Importa biblioteca pulp
from pulp import *
import leArquivo
import sys

#========== Chama a função arquivo, e retorna os dados necessários para o problema =================
atividade,escolhas,custoCarro = leArquivo.leArquivo(sys.argv[1])
custos,escolhas = leArquivo.transform(escolhas)

#Lista com o numero de carros
numeroCarros = list(range(1, (len(atividade) + 1)))


atividade.insert(0,"0")
escolhas.insert(0,0)

#=======================================
v = makeDict([escolhas], atividade, 0)

# Cria a variavel model
model = pulp.LpProblem("PTTOR-16", LpMinimize)

#Define a variavel C que contem o custo de cada camimho
#Cria um dictionary
custos = pulp.makeDict([escolhas, escolhas], custos,0)

# Declaracao das variaveis x: quantidade produzida do item i no periodo t #######################       
x = LpVariable.dicts("x",(escolhas,escolhas,numeroCarros),0,1,LpBinary)
y = LpVariable.dicts("y",(numeroCarros),0,1,LpBinary)


#Somatorio dos custos
#========================= FUNCAO OBJETIVO (RV1) ================================= 
#Nova funcao objetivo: model += lpSum(lpSum(custos[i][j]*x[i][j][k] for i in escolhas for j in escolhas) for k in numeroCarros)

model += lpSum(lpSum(custos[i][j]*x[i][j][k] for i in escolhas for j in escolhas) 
        for k in numeroCarros) + lpSum( y[k]*custoCarro for k in numeroCarros) 


#Restricoes

#restringindo arestas com atividades diferentes a Noatividade e Matutino 
for k in numeroCarros:
        for i in escolhas:
                for j in escolhas:
                        if(v[i] == 'N' and v[j] == 'M'):
                                model +=( x[i][j][k]) == 0
                        if(v[j] == 'M' and v[i] == 'N'):
                                model += (x[j][i][k]) == 0

#restringindo arestas com atividades diferentes [i][n] + [n][i] <= 1
for k in numeroCarros:
        for i in escolhas:
                for j in escolhas:
                        for n in escolhas:
                                if(v[i] == 'N' and v[n] == 'V' and v[j] == 'M'):
                                        model += (x[i][n][k] + x[n][j][k]) <= 1
                                if(v[i] == 'M' and v[n] == 'V' and v[j] == 'N'):
                                        model += (x[i][n][k] + x[n][j][k]) <= 1
                        

 # restringindo subciclos
for i in escolhas:
        for j in escolhas:
                model +=  lpSum( x[j][i][k] + x[i][j][k]    for k in numeroCarros)  <= 1                       


# restringe que apenas uma aresta saia do vertice
for j in escolhas:
        if(j != 0):
                model += lpSum( x[j][i][k]  for i in escolhas for k in numeroCarros) == 1
        else:
                #restringe um numero minimo de carros saindo do ponto 0
                model += lpSum( x[j][i][k]  for i in escolhas for k in numeroCarros) >= 3


 
# restringe que apenas uma aresta chegue do vertice
for i in escolhas:
        if(i != 0):
                model += lpSum( x[j][i][k]  for j in escolhas for k in numeroCarros) == 1
        else:
                #restringe um numero minimo de carros chegando no ponto 0
                model += lpSum( x[j][i][k]  for j in escolhas for k in numeroCarros) >= 3



# restringindo o mesmo carro chegando e saindo de cada ponto
for k in numeroCarros:
        for i in escolhas:
                model +=  lpSum( x[j][i][k] - x[i][j][k]    for j in escolhas  )  == 0



# restringindo numero maximo de passageiros ( numero maximo mais e igual ao numero de arestas do subciclo)
for k in numeroCarros:
        model += lpSum( x[j][i][k]  for j in escolhas for i in escolhas) <= 5                



#caso o carro seja usado o custo dele e adicionado a funcao objetivo
for k in numeroCarros:
        for j in escolhas:
                for i in escolhas:
                        model += y[k] >= x[j][i][k]




model.solve(PULP_CBC_CMD(msg=1,maxSeconds=3600.0))

#model.solve()

#for i in escolhas:
#        for j in escolhas:
#                for k in numeroCarros:
#                        if(x[i][j][k].value() == 1):
#                                print "%s : %.2f" % (x[i][j][k] , x[i][j][k].value())

#for k in numeroCarros:
#        print "%s : %.2f" % (y[k], y[k].value())
                
#print(model)

print ("Status:" , pulp.LpStatus[model.status])
print 'Custo Total: %.2f:' % model.objective.value()

contCarros = 0
for k in numeroCarros:
        if(y[k].value() > 0):
                contCarros += 1
print("Numero de carros utilizados: %d\n" % contCarros)
#impressao de trajetorias                
for k in numeroCarros:
        if(y[k].value() > 0):  
                print("Trajeto do carro %d: " % k)
                for i in escolhas:
                        for j in escolhas:
                                if(x[i][j][k].value() == 1):
                                        if(j == 0):
                                                print "%d -> Chegada , atividade: %s , Valor: %d" % (i, v[i], custos[i][j])
                                        elif(i == 0):
                                                print "Saida -> %d , atividade: %s, Valor: %d" % (j, v[j], custos[i][j])
                                        else:
                                                print "%d -> %d, atividade: %s, Valor: %d" % (i,j, v[j], custos[i][j])
                print ""
print sys.argv[1]