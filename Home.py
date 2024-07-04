"""
Roger Lera
26/06/2024
"""
import os
import numpy as np
import time
import csv
from read_files import *
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
    
def pie_chart(fa):
    st.write(f"##### Porcentage de Skills Trabajadas (%): {fa:.0f} %")
    df_fa = pd.DataFrame({'name':['Skills Trabajadas','Skills No Trabajadas'],'percentage':[fa,100-fa]})
    pie = px.pie(df_fa, values='percentage', names='name',color='name',
                color_discrete_map={'Skills Trabajadas':'green',
                                'Skills No Trabajadas':'red'},
                category_orders={'name':['Skills Trabajadas','Skills No Trabajadas']})
    pie = px.pie(df_fa, values='percentage', names='name',color='name',
                category_orders={'name':['Skills Trabajadas','Skills No Trabajadas']})
    pie.update_layout(legend=dict(font=dict(size=16)),
                    font_size=16)
    
    st.plotly_chart(pie)
    return None

def bar_chart(J,skills,n_jobs=5):
    st.write(f"##### Jobs for which you would be more employable within this job field")
    ja_df = job_field_affinity(J,skills,n_jobs)
    bar = px.bar(ja_df, x='ja', y='Jobs', orientation='h')
    bar.update_xaxes(title_text = "Porcentage de Skills Aprendidas (%)",
                    range=[0, 100],
                    tickfont=dict(size=14))
    bar.update_yaxes(tickfont=dict(size=14))
    bar.update_layout(yaxis=dict(title=dict(font=dict(size=16))),
                    xaxis=dict(title=dict(font=dict(size=16))))
    st.plotly_chart(bar)
    return None


path_ = os.getcwd()
N_jobs = 229
N_jobs = 80 #professionals and management jobs
results_path = os.path.join(path_,'results')
courses_path = os.path.join(path_,'courses','courses.csv')
jobs_path = os.path.join(path_,'jobs','jobs')


ded_dict = {"Low (10 h)":5,
            "Medium (20 h)":10,
            "Trumpet master (40 h)":20,
            "Aristotelian expert (80 h)":40}

ded_dict = {"Low (10 h)":5,
            "Medium (20 h)":10,
            "High (40 h)":20,
            "Very High (80 h)":40}

ded_dict = {"10 h":5,
            "20 h":10,
            "40 h":20,
            "80 h":40}

ded_dict = {"10 h":5,
            "20 h":10,
            "40 h":20}

ded_emoji = {5:':snail:',
             10:':doughnut:',
             20:':trumpet:',
             40:':books:'}

ded_emoji = {5:':smiley:',
             10:':sunglasses:',
             20:':nerd_face:',
             40:':brain:'}

ded_emoji = {5:':smiley:',
             10:':sunglasses:',
             20:':nerd_face:'}


try:
    A = st.session_state['A']
    S = st.session_state['S']
    J = st.session_state['J']
    j_dict = st.session_state['j_dict']
    j_trans = st.session_state['j_trans']
    s_trans = st.session_state['s_trans']
    a_trans = st.session_state['a_trans']
except:
    A = read_activities(courses_path)
    J,j_dict = read_jobs(jobs_path,N_jobs)
    S = read_all_skills()
    j_trans,s_trans,a_trans = read_translations()
    st.session_state['A'] = A
    st.session_state['J'] = J
    st.session_state['j_dict'] = j_dict
    st.session_state['S'] = S
    st.session_state['j_trans'] = j_trans
    st.session_state['s_trans'] = s_trans
    st.session_state['a_trans'] = a_trans


st.write("# Planea tus cursos :books:")
st.write(f"""
        Para recibir un planning de cursos de dos semanas, 
        escoge tu trabajo deseado y la dedicación que le quieres dedicar.
""")


st.selectbox(
    "Escoge tu trabajo deseado.",
    J.keys(),
    format_func=lambda x : j_trans[x],
    index=47,
    #placeholder = "Unknown Field",
    key = "field"
)


st.selectbox(
    "Escoge el tiempo de estudio deseado.",
    ded_dict.keys(),
    index=1,
    #placeholder = "Unknown Dedication",
    key = 'dedication',
)


if 'dedication' in st.session_state.keys() and 'field' in st.session_state.keys():
    
    ded = st.session_state['dedication']
    fie = st.session_state['field']

    file_path = os.path.join(results_path,f"{j_dict[fie]}-{ded_dict[ded]}.stdout")

    df,fa = read_path(file_path,A,a_trans)
    #J = read_field(f'{J[fie]}')
    dicts = j_trans,s_trans,a_trans
    df_s = read_skills(file_path,dicts,A)



    st.write(f"## Sector Laboral: {j_trans[fie]}")
    st.write(f"### Tiempo de Estudio: {ded} {ded_emoji[ded_dict[ded]]}")

    styler = df.style.hide_index()
    
    st.write(styler.to_html(escape=False, index=False), unsafe_allow_html=True)

    """
    
    """

    pie_chart(fa)

    """
    
    """

    styler_s = df_s.style.hide_index()
    
    st.write(styler_s.to_html(escape=False, index=False), unsafe_allow_html=True)


    #bar_chart(J,skills,n_jobs=5)