import pandas as pd
from jinja2 import Environment, FileSystemLoader
from flask import url_for
import numpy as np


# funções pra colorir as tabelas
def _color_correction(data):
    df = data.copy()
    df.loc[df['Sua resposta'] == df['Gabarito'], :] = 'background-color: lightgreen'
    df.loc[df['Sua resposta'] != df['Gabarito'], :] = 'background-color: #d48585'
    return df

def _color_table_every_other(data):
    df = data.copy()
    n = len(df)
    df.iloc[range(0,n,2), :] = 'background-color: #f5f5dc'
    df.iloc[range(1,n,2), :] = 'background-color: #f0f0ce'
    df.iloc[-1,:] += '; font-weight: bold'
    return df

def _color_table_redacao(data):
    df = data.copy()
    n = len(df)
    # print(df.iloc[0:5,0:3])
    df.iloc[0:6,0:3] = 'background-color: #f0f0ce'
    df.iloc[-1] += '; font-weight: bold'
    return df



# dados da redacao
df_r = pd.read_pickle('redacao.pkl')


relatorio_alunos = {}


# /!\ IMPORTANTE /!\
# aqui carrega o template HTML que vai ser usado pelo Jinja
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("relatorios/simulinho_aluno_template.html")

# cria um dicionário com as variáveis pro template
doc = {
    'document_title': 'Correção SIMULINHO 2021'
}

# pra cada aluno
for aluno in df_r.index.get_level_values(0).unique():
    # print(aluno)

    # a cada iteração, ele pega os dados correspondente ao 'aluno'
    doc['nome'] = aluno # nome do aluno
    doc['materias'] = []
    print(aluno)

    # dados pessoais de cada aluno

    # redacao

    red_aluno = df_r.loc[aluno, :]
    # print(len(red_aluno))
    print(red_aluno)
    
    red_aluno["Criterio"] = red_aluno.index.get_level_values(0)
    red_aluno.loc[:, 'Nota'] = (red_aluno['Nota']).astype(str)
    red_aluno.loc[:, 'Comentario'] = red_aluno['Comentário']
    
    red_aluno= red_aluno[['Criterio', 'Nota','Comentário']]
    
    
    # print(red_aluno)
    doc['redacao'] = red_aluno.style.apply(
                _color_table_redacao,
                axis=None
            ).set_properties(
                **{'text-align':'center',
                   'font-family':'Roboto',
                   'border-color':'black',
                   'border-style' :'solid',
                   'border-width': '1px',
                   'border-collapse':'collapse'}
            ).set_table_styles(
                [{'props':[('color','#533884'), ('font-family','Roboto')]}]
            ).hide_index().render()

    # renderiza o html a partir do template e com as informações do dicionário
    html_out = template.render(doc)
    with open(f"html-alunos/{aluno.replace(' ', '_')}.html",'w') as file:
        file.write(html_out)