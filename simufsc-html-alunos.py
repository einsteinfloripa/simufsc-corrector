import pandas as pd
from jinja2 import Environment, FileSystemLoader
from flask import url_for
import numpy as np
from os import getcwd


# funções pra colorir as tabelas

def _color_correction(data):
    df = data.copy()
    n = len(df)
    
    df.loc[df['Pontuação'] == "1.0", :] = 'background-color: #0fa92c'
    df.loc[df['Pontuação'] == "0.0", :] = 'background-color: #d48585'

    return df

def _color_table_every_other(data):
    df = data.copy()
    n = len(df)
    df.iloc[range(0,n,1), :] = 'background-color: #353F70'
    df.iloc[range(0,n,1), :] = 'color: white'

    #df.iloc[range(0,n,1), :] = 'opacity: 1'
    return df

def _color_table_redacao(data):
    df = data.copy()
    n = len(df)
    # print(df.iloc[0:5,0:3])
    df.iloc[0:6,0:3] = 'background-color: #353F70'
    df.iloc[-1] += '; font-weight: bold'
    #df.iloc[range(0,n,1), :] = 'opacity: 1'
    df.iloc[range(0,n,1), :] = 'color: white'

    return df

# carrega os DataFrames com os dados de questoes
df_q = pd.read_pickle('relatorios/dados/aluno/pontuacao_por_questao.pkl')
df_q = df_q.rename(columns={'assinaladas':'Sua resposta', 'alternativas_certas':'Gabarito','pontuacao':'Pontuação'})
#df_q['Sua resposta'] = df_q['Sua resposta'].str.upper()
#df_q['Gabarito'] = df_q['Gabarito'].str.upper()

# notas dos alunos por materia
df_n = pd.read_pickle('relatorios/dados/aluno/pontuacao_por_materia.pkl')
df_n['Média Individual'] = df_n['Média Individual'].apply(lambda x: str(int(x*100))+'%')
df_n['Média Geral'] = df_n['Média Geral'].apply(lambda x: str(int(x*100))+'%')


# dados da redacao
df_r = pd.read_pickle('relatorios/dados/aluno/redacao.pkl')


# dados das discursivas

df_d = pd.read_pickle('relatorios/dados/aluno/discursivas_alunos.pkl')
df_d.fillna("",inplace=True)

# todas as notas
df_total = pd.read_pickle('relatorios/dados/aluno/pontuacao_total.pkl')


# colocação dos alunos
colocacao = pd.read_pickle("relatorios\dados\docentes\colocacao.pkl")

# dados pessoasi

df_p = pd.read_excel("dados_2021.1\dados_pessoais.xlsx")
df_p.set_index("Login Eduqo", inplace=True)

relatorio_alunos = {}


# /!\ IMPORTANTE /!\
# aqui carrega o template HTML que vai ser usado pelo Jinja
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("relatorios/simufsc.html")

# cria um dicionário com as variáveis pro template
doc = {
    'document_title': 'Correção SIMUFSC 2021'
}

# pra cada aluno
for aluno in df_q.index.get_level_values(0).unique():
    # print(aluno)

    print(aluno)
    # a cada iteração, ele pega os dados correspondente ao 'aluno'
     # nome do aluno
    doc['materias'] = []


    # nome de cada aluno
    if aluno in df_p.index:
        nome = df_p.loc[aluno, :]
        nome = nome.Aluno
        doc['nome'] = nome
    else: 
        nome = aluno
    # colocacao de cada aluno
    coloc_aluno = colocacao[colocacao["aluno_login"] == aluno]

    coloc_aluno.loc[:, 'Colocação'] = coloc_aluno['Colocação']
        
    doc['colocacao'] = coloc_aluno.Colocação.iat[-1]


    # pontuacao geral de cada aluno
    pont_aluno = df_total.loc[df_total['aluno_login'] == aluno]

    pont_aluno =   round(pont_aluno[['Prova objetiva','Questões discursivas',  'Redação']], 2).astype(str)
    #print(pont_aluno)
    doc['pontuacao'] = pont_aluno.style.apply(
                _color_table_every_other,
                axis=None
            ).hide_index().render()


    # questoes de cada aluno
    df_q_aluno = df_q.loc[aluno, :]
    
    #df_q_aluno['Questão'] = df_q_aluno.index.get_level_values(1)
    #print(df_q_aluno['Pontuação'])
    df_q_aluno = df_q_aluno[['Sua resposta','Gabarito','TEMA', 'NÍVEL',"Pontuação"]]

    # pra cada matéria:
    for materia in df_q_aluno.index.get_level_values(0).unique():
        
        doc['materias'].append({
            'materia':materia,
            'df':df_q_aluno.loc[materia, :].style.apply(
                _color_correction,
                axis=None
            ).hide_index().render()
        })

    # mostrar a pontuação em cada materia

    df_n_aluno = df_n.loc[aluno, :]
    df_n_aluno['Matéria'] = df_n_aluno.index.get_level_values(0)
    df_n_aluno.loc[:, 'Pontuação'] = df_n_aluno['Pontuação']
    df_n_aluno.loc[:, 'Média Individual'] = df_n_aluno['Média Individual']
    df_n_aluno.loc[:, 'Média Geral'] = df_n_aluno['Média Geral']
    
    df_n_aluno = df_n_aluno[['Matéria','Pontuação', 'Média Individual',  'Média Geral']]

    doc['notas'] = df_n_aluno.style.apply(
                _color_table_every_other,
                axis=None
            ).hide_index().render()

    
    # pode ser que alguns alunos façam a redação e não façam a prova objetiva, e vice-versa
    if aluno in df_r.index:
        
        red_aluno = df_r.loc[aluno, :]
        # print(len(red_aluno))
        #print(red_aluno)
        
        red_aluno["Criterio"] = red_aluno.index.get_level_values(0)
        red_aluno.loc[:, 'Nota'] = (red_aluno['Nota']).astype(str)
        red_aluno.loc[:, 'Comentario'] = red_aluno['Comentário']
        
        red_aluno = red_aluno[['Criterio', 'Nota','Comentário']]
        
        
        #print(red_aluno)
        doc['redacao'] = red_aluno.style.apply(
                    _color_table_redacao,
                    axis=None
                ).hide_index().render()

    else:
        doc['redacao'] = 'Não fez a redação'
        doc['comentario'] = []

  
    # discursivas

    if aluno in df_d.index:
        
        disc_aluno = df_d.loc[aluno, :]
        # print(len(red_aluno))
        #print(red_aluno)
        disc_aluno["Matéria"] = disc_aluno.index.get_level_values(0)
        disc_aluno.loc[:, 'a)'] = (disc_aluno['a)']).astype(str)
        disc_aluno.loc[:, 'b)'] = (disc_aluno['b)']).astype(str)
        disc_aluno.loc[:, 'c)'] = (disc_aluno['c)']).astype(str)
        disc_aluno.loc[:, 'Nota final'] = (disc_aluno['Nota final']).astype(str)
        disc_aluno.loc[:, 'Comentários'] = disc_aluno['Comentários']
        
        disc_aluno= disc_aluno[["Matéria", 'a)',	'b)','c)','Nota final','Comentários']]
        
        
        # print(red_aluno)
        doc['discursivas'] = disc_aluno.style.apply(
                    _color_table_every_other,
                    axis=None
                ).hide_index().render()

    else:
        doc['discursivas'] = 'Não fez as discursivas'
        doc['comentario'] = []

    doc['grafico_path'] = f'{getcwd()}/relatorios/graficos/{aluno}.jpg'

    # renderiza o html a partir do template e com as informações do dicionário
    html_out = template.render(doc)
    with open(f"html-alunos/{nome.replace(' ', '_')}.html",'w',  encoding='utf-8') as file:
        file.write(html_out)