## This Python file uses the following encoding: utf-8
#===== variáveis globais ==========
atividade = []
escolhas = []
custos = []
custoStr = []
custoCarro = 0
INF = 900
linha = ""
linhaAux = ""

#===========Função para ler o arquivo =============
def leArquivo(arquivo):
	rio = open(arquivo,"r")

    #======= Strings a serem comparadas com as tags no arquivo ========    
	atividades = "<Atividades	Periodo>\n"
	turistas = "<Escolha Turistas>\n"
	custosAtividades = "<Custos das Atividades>\n"
	custoFixo = "<Custo fixo>\n"
	fim = "<Fim>\n"

    ####### Variável de controle ###########
	flag = 0

	######## Lê os dados do arquivo ##############
	while rio.readline():
		linha = rio.readline()
		if linha == atividades:
			flag = 1
		while flag == 1:
			linha = rio.readline()
			linhaAux = linha
			if linha == turistas:
				flag = 2
			else:
				linha = linha.translate(None, '\n\t1234567890')
				atividade.append(linha)
				linhaAux = linhaAux.translate(None,'\n\tMVN')
				escolhas.append(linhaAux)
		while flag == 2:
			linha = rio.readline()
			if linha == custosAtividades:
				flag = 3
			else:
				print "Lendo arquivo.."
		while flag == 3:
			linha = rio.readline()
			if linha == custoFixo:
				flag = 4
			else:
				linha = linha.replace("\n","").split("	")
				custoStr.append(linha)
		while flag == 4:
			linha = rio.readline()
			if linha == fim:
				flag = 0
			else:
				custoCarro = int(linha)
	return atividade,escolhas,custoCarro
	
    ####### fecha  o arquivo ###########
	rio.close()

def transform(escolhas):
	#### variável auxiliar #######
	custoAux = []

	for x in range(0,len(escolhas)):
		escolhas[x] = int(escolhas[x])

	########  Converte a matriz de custos de str para int ############
	for x in range(1,len(custoStr)):
		for y in range(1,len(custoStr)):
			if custoStr[x][y] == "INF":
				custoAux.append(INF)
			else:
				custoAux.append(int(custoStr[x][y]))
		custos.append(custoAux)
		custoAux = []
	return custos,escolhas

