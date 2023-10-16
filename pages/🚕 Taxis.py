import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import pyarrow.parquet as pq
import os



####################función leer datos y guardarlos en caché###########
@st.cache_data
def get_data():
    directories = ['data/Taxis/taxis/','data/Taxis/taxis-2011/' ]
    # Create an empty list to store individual DataFrames
    dataframes = []
    # Loop through each directory
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith(".parquet"):
                # Construct the full file path
                file_path = os.path.join(directory, filename)
            
                # Read the Parquet file into a DataFrame and append it to the list
                df = pq.read_table(file_path).to_pandas()
                dataframes.append(df)

    # Concatenate all the DataFrames into one
    dff = pd.concat(dataframes, ignore_index=True)
    return dff


#status_text.text('Bienvenido!')

Tipo = st.radio('Que quieres ver?', ('Heatmap', 'Top destinos', 'Destino más popular por mes y año', 'Km/año', 'Viajes más costosos'))


#######################carga la info######################
df = get_data()

l_year = df.pickup_year.unique().tolist()#.sort()
l_year.sort()
puzone = df.PU_Zone.unique().tolist()#.sort()
dozone = df.DO_Zone.unique().tolist()
zones = puzone+dozone

zones = list(dict.fromkeys(zones))


l_year =  [x for x in l_year if x <= 2023]
l_year =  [x for x in l_year if x >= 2009]


########### leer el año que se quiera ver ####################
years = st.multiselect("Elige al menos un año", l_year, [2020])


######## Manejo si no selecciona año #####################
if not years:
    st.error("elige al menos un año.")


else:
    ##################heatmap#################################
    if Tipo == 'Heatmap':
        
        l_month = df[df['pickup_year'].isin(years)].pickup_month.unique().tolist()#.sort()
        l_month.sort()
        
        if years == [2023]:
            months = st.multiselect("Elige un mes", l_month, [1,2,3,4,5,6])
        else:
            months = st.multiselect("Elige un mes", l_month, [1,2,3,4,5,6,7,8,9,10,11,12])
        
        zones = st.multiselect("Elige una o más zonas: ", zones, [ "Central Park", "Lenox Hill East", "Midtown North", "Midtown South", "East Elmhurst", "West Chelsea/Hudson Yards", "TriBeCa/Civic Center", "West Village", "Sutton Place/Turtle Bay North", "JFK Airport", "Two Bridges/Seward Park", "Meatpacking/West Village West", "Lower East Side", "Little Italy/NoLiTa", "Union Sq", "Manhattan Valley" ])
        
        sns.set(font_scale=1)
        sns.set(rc={'figure.figsize':(15,20)})
        
        try:        
            with st.spinner('Calculando...'):
                heat_m = pd.crosstab(df[(df['pickup_year'].isin(years))& (df['pickup_month'].isin(months)) &(df['PU_Zone'].isin(zones))&(df['DO_Zone'].isin(zones))].PU_Zone, df[(df['pickup_year'].isin(years))& (df['pickup_month'].isin(months)) &(df['PU_Zone'].isin(zones))&(df['DO_Zone'].isin(zones))].DO_Zone, aggfunc = 'sum', values = df.conteo)
                fig, ax = plt.subplots()
                if len(months) <= 10:
                    sns.set(font_scale=0.7)
                    sns.set(rc={'figure.figsize':(15,15)})
                elif len(months) <= 20:
                    sns.set(rc={'figure.figsize':(15,20)})
                    sns.set(font_scale=0.9)
                    
                else:
                    sns.set(font_scale=0.9)
                    sns.set(rc={'figure.figsize':(50,50)})
                    
                    
                sns.heatmap(heat_m, annot=True, cmap = 'YlOrBr', fmt='g').set(title='Cantidad de viajes en el periodo seleccionado:')
                st.pyplot(fig)
            st.success('Done!')
        except: 
            st.error("Elige al menos uno de cada parámetro.")
        #st.write('Cantidad de viajes en el periodo seleccionado:')
        
        
    ################## compara km recorridos por año #################################
    elif Tipo == 'Km/año':

        
        with st.spinner('Calculando...'):
            sns.set(rc={'figure.figsize':(15,15)})
            kmy = df[(df['pickup_year'].isin(years))]
            # create color mapping based on all unique values of year
            sumkmy = kmy.groupby('pickup_year', as_index =False)['distancia'].sum()
            sumkmy['distancia'] = sumkmy['distancia']/1000000
            pal = sns.color_palette("ch:s=.25,rot=-.25", len(sumkmy))
            #rank = sumkmy.argsort().argsort() 
            
            fig, ax = plt.subplots()
            sns.barplot(sumkmy, x="pickup_year", y="distancia").set(title='Cantidad de kilometros recorridos por año (Millones de km)')
            ax.bar_label(ax.containers[0])
            st.pyplot(fig)
        st.success('Done!')
    
    ################## cálculo destinos #################################
    elif Tipo == 'Top destinos':
        matplotlib.rc_file_defaults()
        with st.spinner('Calculando...'):
            l_month = df[df['pickup_year'].isin(years)].pickup_month.unique().tolist()#.sort()
            l_month.sort()
            #zones = st.multiselect("elige una o más zonas: ", zones)
            
            months = st.multiselect("elige un mes", l_month, [1])
            
            num_dest = st.slider("Top de destinos: ", 2, 20, 5)
            
            dest = df[(df['pickup_year'].isin(years))& (df['pickup_month'].isin(months))]
            # create color mapping based on all unique values of year
            dest = dest.groupby('DO_Zone', as_index =False)['conteo'].sum()
            dest['conteo'] = dest['conteo']/1000000
            dest = dest.sort_values('conteo', ascending =False).head(num_dest)
            
            #st.show(dest.plot.barh().figure)
            
            fig3, ax3 = plt.subplots()
            sns.barplot(dest, y="DO_Zone", x="conteo").set(title='Destinos más populares (Millones de viajes)')
            ax3.bar_label(ax3.containers[0])
            st.pyplot(fig3)
        st.success('Done!')
    
    ################## viajes más rentables desde-hacia #################################      
    elif Tipo == 'Viajes más costosos':
        matplotlib.rc_file_defaults()
        l_month = df[df['pickup_year'].isin(years)].pickup_month.unique().tolist()#.sort()
        l_month.sort()
        months = st.multiselect("elige un mes", l_month, [1])
        num_dest = st.slider("Top de destinos: ", 2, 20, 5)
        
        with st.spinner('Calculando...'):
            rent = df[(df['pickup_year'].isin(years))& (df['pickup_month'].isin(months))]
            rent = rent.groupby(['PU_Zone', 'DO_Zone'], as_index =False)[['conteo', 'tot_amt']].sum()
            rent['avg_val'] = rent['tot_amt']/rent['conteo']
            rent = rent.sort_values('avg_val', ascending =False).head(num_dest)
            #heat_d = pd.crosstab(rent.PU_Zone, rent.DO_Zone, aggfunc = 'sum', values = rent.avg_val)
            fig, ax = plt.subplots()
            sns.barplot(rent, y= rent['PU_Zone'] + " to " + rent['DO_Zone'], x="avg_val").set(title='Viajes más costosos ($)')
            ax.bar_label(ax.containers[0])
            st.pyplot(fig)
        st.success('Done!')
        
        
    elif Tipo =='Destino más popular por mes y año':
    
        with st.spinner('Calculando...'):
            st.write('Destinos más populares (conteo de viajes por año)')
            dest_pop = df[(df['pickup_year'].isin(years))]
            dest_pop = dest_pop.groupby(['pickup_year','pickup_month', 'DO_Zone'], as_index =False)[['conteo']].sum()
            dest_pop = dest_pop.loc[dest_pop.groupby(['pickup_year', 'pickup_month'])['conteo'].idxmax()]
            
            st.dataframe(dest_pop)
            
        st.success('Done!')
        
    
