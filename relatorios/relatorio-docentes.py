import pandas as pd
import numpy as np
import streamlit as st
import PIL
# import matplotlib.pyplot as plt

st.title('Relatório Docentes')

st.write('Olá Docente! Este é o seu **relatório do SIMUFSC 2021**.')
st.write("Ele é dividido em **duas seções principais**. A primeira delas, apresenta dados gerais sobre toda a prova, estas informações são padronizadas para todas as disciplinas. A seção 2 apresenta dados **específicos para cada matéria**. Para selecionar qual matéria você deseja analisar os dados, basta selecioná-la na barra lateral esquerda.")
st.write("Façam bom uso!")

# ! dados gerais !

st.header("**1. Dados sobre a Prova Geral**")

st.subheader("**1.1 Dados sobre as Questões Objetivas**")

# media e % das objetivas 
media_acerto_materia = pd.read_pickle('relatorios/dados/docentes/media_acerto_materia.pkl')
#media_acertos_obj = media_acerto_materia['Correção'].mean()

#st.write("A média geral de acertos da prova objetiva foi ", str(round(media_acertos_obj, 3)*100)+'%')
 

st.markdown("**Média de acertos por matéria (em %)**")

media_acerto_materia = media_acerto_materia.reset_index()

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
media_acerto_materia.set_index('Disciplina',inplace=True)

st.write(pd.DataFrame({
   'Média de acertos': round(media_acerto_materia['Média']*100, 2)
}))


def get_media_a_m():
    path = 'relatorios/dados/docentes/media_acerto_materia.pkl'
    return pd.read_pickle(path)
 
# gráfico com a média de acerto de cada matéria

# o grafico fica com os rotulos na horizontal com as duas linhas a seguir, mas, quando o codigo é upado no servidor do streamlit ele sai todo desconfigurado. 
# caso queira testar para ver se não dá mais o bug, é so "descomentar" as duas linhas a seguir

# media_acerto_materia = media_acerto_materia.reset_index()
# media_acerto_materia = media_acerto_materia.set_index('Correção')
media_acerto_materia = pd.read_pickle('relatorios/dados/docentes/media_acerto_materia.pkl')
st.markdown("**Gráfico da porcentagem média de acerto em cada matéria**")
st.bar_chart(data=media_acerto_materia["Média"])

st.write("Passando o mouse por cima do gráfico você pode identificar qual é a matéria e nota referentes a cada barra.")


# media e % da redação

media_redacao =  pd.read_pickle('relatorios/dados/docentes/media_redacao.pkl')
print(media_redacao)
# tabela com os dados coletados acima
st.subheader("**1.2 Dados sobre a Redação**")
st.write(pd.DataFrame({
    'Nota Média': media_redacao['Nota']
}))

# questões discursivas


st.subheader("**1.3 Dados sobre as Questões discursivas**")

st.write("Os dados dizem respeito à pontuação média obtida em cada alternativa e na nota final.")
media_discursivas = pd.read_pickle('relatorios/dados/docentes/media_discursivas.pkl')
st.write(pd.DataFrame({
    'A': media_discursivas['a)'],
    'B': media_discursivas['b)'],
    "C": media_discursivas['c)'].astype(str),
    'Nota final': media_discursivas['Nota final'].astype(str)
}))


# tabela com a colocação dos alunos

colocacao = pd.read_pickle('relatorios/dados/docentes/colocacao.pkl')
st.subheader("**1.4   Colocação dos alunos do Einstein**")
colocacao.set_index('Colocação',inplace=True)
st.write(pd.DataFrame({
    'Nome': colocacao['aluno_login'],
    'Pontos': colocacao['Pontuação'],
    "Porcentagem de Acerto": colocacao['% de acerto']
}))


#  ! dados específicos por matéria  ! 

# questões separadas por materia e por assunto
# # tem o total de acertos, total de alunos que responderam e média de acerto

media_acerto_materia = get_media_a_m()
media_acerto_materia = media_acerto_materia.reset_index()

materia_escolhida = st.sidebar.selectbox("Escolha a matéria", media_acerto_materia['Disciplina'])

dados_materia_escolhida = media_acerto_materia[(media_acerto_materia['Disciplina'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
dados_materia_escolhida.set_index('Disciplina',inplace=True)

st.header("**2. Dados sobre a Matéria Selecionada**")

st.write("Aqui você encontra dados sobre a matéria que foi selecionada na caixa localizada na aba lateral.")
st.write(pd.DataFrame({
    "Média Acertos(em %)": dados_materia_escolhida['Média']*100
}))


# todas as questões separadas por matéria
# #  tem o total de acertos, total de alunos que responderam e média de acerto
media_acerto_questao = pd.read_pickle('relatorios/dados/docentes/media_acerto_questao.pkl')

st.subheader("**2.1   Média de acertos por questao**")
st.write("Nesta seção são discretizados os acertos por questão.")
media_acerto_questao = media_acerto_questao.reset_index()
questao_materia_escolhida = media_acerto_questao[(media_acerto_questao['Disciplina'] == materia_escolhida)]


# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
questao_materia_escolhida.set_index('Questão',inplace=True)



st.write(pd.DataFrame({
    "Assunto": questao_materia_escolhida['TEMA'],
    "Dificuldade": questao_materia_escolhida['NÍVEL'],
    "Média Acertos(em %)": questao_materia_escolhida['Média']*100,
    "Tempo Médio(minutos)": questao_materia_escolhida["tempo_no_exercicio(s)"]/60
}))

grafico_questoes = questao_materia_escolhida['Média']
grafico_questoes = grafico_questoes.reset_index()
grafico_questoes['questao'] = grafico_questoes['Questão'].astype(str)
grafico_questoes["media"] = grafico_questoes['Média']
grafico_questoes.set_index('questao',inplace=True)

st.bar_chart(data=grafico_questoes['media'])
st.write("Dependendo das pontuações das questões, pode ser que o gráfico apresente **escalas diferentes para cada matéria**. Lembre de sempre olhar os valores do eixo vertical.")

# questões separadas por materia e por assunto
# #  tem o total de acertos, total de alunos que responderam e média de acerto

def get_media_p_a():
    path = 'relatorios/dados/docentes/media_por_assunto.pkl'
    return pd.read_pickle(path)
media_por_assunto = get_media_p_a()
# print(media_por_assunto)

media_por_assunto = media_por_assunto.reset_index()
assuntos_materia_escolhida = media_por_assunto[(media_por_assunto['Disciplina'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
assuntos_materia_escolhida.set_index('TEMA',inplace=True)

st.subheader("**2.2   Média de acertos por assunto**")

st.write(pd.DataFrame({
    "Total Acertos": assuntos_materia_escolhida['Total Acertos'],
    'Total Respostas': assuntos_materia_escolhida['Total Respostas'],
    'Média (em %)': round(assuntos_materia_escolhida['Média']*100,3)
}))



# analise dos acertos por dificuldade
media_por_dificuldade = pd.read_pickle('relatorios/dados/docentes/media_por_dificuldade.pkl')

st.subheader("**2.3   Média de acertos por dificuldade**")

media_por_dificuldade = media_por_dificuldade.reset_index()
dificuldade_materia_escolhida = media_por_dificuldade[(media_por_dificuldade['Disciplina'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
dificuldade_materia_escolhida.set_index('NÍVEL',inplace=True)


st.write(pd.DataFrame({
    "Total Acertos": dificuldade_materia_escolhida['Total Acertos'],
    'Total Respostas': dificuldade_materia_escolhida['Total Respostas'],
    'Média (em %)': round(dificuldade_materia_escolhida['Média']*100,3)		
}))


# destrinchando as alternativas que os alunos assinalaram 

st.subheader("**2.4   Distribuição das respostas dos alunos**")

st.write("Aqui você encontra a distibuição de vezes que os alunos assinalaram as alternativas. Por exemplo, 14/60 significa que dos 60 alunos que responderam a questão, 14 assinalaram a alternativa como correta.")

qntd_assinaladas = pd.read_pickle("relatorios/dados/docentes/qntd_assinaladas.pkl")
qntd_assinaladas.reset_index(inplace=True)
qntd_assinalas_materia = qntd_assinaladas[qntd_assinaladas['Disciplina'] == materia_escolhida]
qntd_assinalas_materia.drop_duplicates(subset=['Questão'], inplace=True)
qntd_assinalas_materia.set_index("Questão",inplace=True)
st.write(pd.DataFrame({
    "Gabarito": qntd_assinalas_materia['alternativas_certas'].str.strip('[]'),
    "1": qntd_assinalas_materia['1'],
    '2': qntd_assinalas_materia['2'],
    '4': qntd_assinalas_materia['4'],
    "8": qntd_assinalas_materia['8'],
    '16': qntd_assinalas_materia['16'],
    '32': qntd_assinalas_materia['32'],
    '64': qntd_assinalas_materia['64']
}))

# destrinchando as zonas de pontuação

