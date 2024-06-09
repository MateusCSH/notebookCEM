import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime as dt
from Notebook_aux import format_timedelta, transformar_horas

#data_pre['DATA INICIAL'] = pd.to_datetime(data_pre['DATA INICIAL'])
#data_pre['DATA FINAL'] = pd.to_datetime(data_pre['DATA FINAL'])

with open("stylenote.css") as f:
    css = f.read()

# Renderize o CSS
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


up = st.sidebar.file_uploader('Arquivo notebook', type='csv')

if up is not None:

    df = pd.read_csv(up, header=None).drop(0).drop(columns=0)
    df.columns = ['Nome', 'Matricula','Periodo', 'Máquina', 'Inicio','Fim']

    df['Inicio'] = pd.to_datetime(df['Inicio'], format='%H:%M:%S')
    df['Fim'] = pd.to_datetime(df['Fim'], format='%H:%M:%S')
    #print(df.info())
    #print(df['Inicio'])


    note = st.sidebar.multiselect('Select seu notebook',
                                  options=sorted(df['Máquina'].unique()),
                                  default=sorted(df['Máquina'].unique()),
                                  placeholder='Escolha a máquina')
    
    note_selec = df.query(
        'Máquina == @note'
    )

    esc = st.selectbox('Escolha a opção', ('Horas', 'Periodo'))

    if esc == 'Horas':
        total = transformar_horas(note_selec)
        total_sum = total.sum()
        formatted_total = format_timedelta(total_sum)   # Retorna conversão h:m         

        
        st.markdown(f'<div class="note"> <span>TOTAL HORAS ACUMULADO</span> <span class = "value">{formatted_total}</span></div>', unsafe_allow_html=True)
        



    p1=0; p2=0; p3=0; p4=0; p5=0 
    p6=0; p7=0; p8=0; p9=0; p10=0
    if esc == 'Periodo':
        for i in note_selec.index:
            if note_selec.loc[i,'Periodo'] == '1º Período':
                p1 = p1+1

            elif note_selec.loc[i,'Periodo'] == '2º Período':
                p2 = p2+1

            elif note_selec.loc[i,'Periodo'] == '3º Período':
                p3 = p3+1

            elif note_selec.loc[i,'Periodo'] == '4º Período':
                p4 = p4+1

            elif note_selec.loc[i,'Periodo'] == '5º Período':
                p5 = p5+1

        st.markdown('Quantidade de pessoa por período')
        col1, col2, col3, col4, col5 = st.columns(5)
      
        
        with col1:
            
            st.markdown(f'<div class="note"><span>1º Periodo</span><span class="value">{p1} </span></div>', unsafe_allow_html=True)
            

        with col2:
            st.markdown(f'<div class="note"><span>2º Periodo</span><span class="value">{p2} </span></div>', unsafe_allow_html=True)

        with col3:
            st.markdown(f'<div class="note"><span>3º Periodo</span><span class="value">{p3} </span></div>', unsafe_allow_html=True)

        with col4:
            st.markdown(f'<div class="note"><span>4º Periodo</span><span class="value">{p4} </span></div>', unsafe_allow_html=True)

        with col5:
            st.markdown(f'<div class="note"><span>5º Periodo</span><span class="value">{p5} </span></div>', unsafe_allow_html=True)

        opn = st.button('Quantidade maxima de ocupação')

        if opn:
            op = [p1,p2,p3,p4,p5]
            maximo = max(op, key=int)
            st.subheader(maximo)
            




    

else:
    st.warning('Faça o upload do arquivo de notebook')
