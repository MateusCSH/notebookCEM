import pandas as pd
import streamlit as st
import plotly.express as px

import plotly.graph_objects as go

from datetime import datetime as dt
from Notebook_aux import format_timedelta, transformar_horas

#python -m venv venv
#.\venv\Scripts\activate
#pip freeze > .\requirements.txt
# pip install -r .\requirements.txt

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
        qtd_pessoas = len(note_selec)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="note"> <span>TOTAL HORAS ACUMULADA</span> <span class = "value">{formatted_total}</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="note"> <span>QUANTIDADE DE PESSOAS</span> <span class = "value">{qtd_pessoas}</span></div>', unsafe_allow_html=True)



        maq = st.selectbox('Escolha a máquina desejada', (sorted(df['Máquina'].unique())))

        maq_select = df.query('@maq == Máquina')    
        hrs_selec_maq = transformar_horas(maq_select)   # Pega as horas da pessoa
        tot_hrs_selec_maq = hrs_selec_maq.sum()         # Soma as horas da pessoa
        percent = (tot_hrs_selec_maq / total_sum) * 100 

        fig = go.Figure(go.Indicator(
                mode="gauge+number",    #gráfico de gauge (ou medidor) + número
                value=percent,
                title={'text': "Percentual de Horas utilização"},
                gauge={'axis': {'range': [None, 100]}}, #Define as configurações do gauge. Nesse caso, estamos definindo a escala do gauge para ir de 0 a 100.
                domain={'x': [0, 1], 'y': [0, 1]}   #Define a área do gráfico que será ocupada pelo gauge. Nesse caso, estamos definindo que o gauge ocupará toda a área do gráfico (x e y vão de 0 a 1).
            ))

        st.plotly_chart(fig)
       



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

        st.markdown('<div class = "my_title">QUANTIDADE DE USUÁRIOS POR PERÍODO</div>', unsafe_allow_html=True)
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

        sele_per = st.selectbox('Escolha o período', (sorted(df['Periodo'].unique())))
        peri_select = df.query('@sele_per == Periodo')

        soma_peri = len(peri_select)


        
        hrs_por_periodo = transformar_horas(peri_select)   # Pega as horas da pessoa
        tot_hrs_periodo = hrs_por_periodo.sum()         # Soma as horas da pessoa
        tot_hrs_periodo_formatado = format_timedelta(tot_hrs_periodo)   # Retorna conversão h:m 

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="note"><span>Quantidade de pessoas</span><span class="value">{soma_peri}</span> </div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="note"><span>Quantidade de horas</span><span class="value">{tot_hrs_periodo_formatado}</span></div>', unsafe_allow_html=True)


        percent_peri = (soma_peri/len(df['Periodo'])) * 100

        
            

        fig = go.Figure(go.Indicator(
                mode="gauge+number",    #gráfico de gauge (ou medidor) + número
                value=percent_peri,
                title={'text': "Percentual de utilização por período"},
                gauge={'axis': {'range': [None, 100]}}, #Define as configurações do gauge. Nesse caso, estamos definindo a escala do gauge para ir de 0 a 100.
                domain={'x': [0, 1], 'y': [0, 1]}   #Define a área do gráfico que será ocupada pelo gauge. Nesse caso, estamos definindo que o gauge ocupará toda a área do gráfico (x e y vão de 0 a 1).
            ))

        st.plotly_chart(fig)


    

else:
    st.warning('Faça o upload do arquivo de notebook')

    st.markdown(f'<div class = "meu_meu"> <span>OBS: Arquivo deve ser em formato</span> <span class = "com_valor"> .CSV </span></div>', unsafe_allow_html=True)
