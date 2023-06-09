from data import get_data
import matplotlib.pyplot as ml
import seaborn as sb
import streamlit as st
import pandas as pd

def format_heure(dataframe):    
    dataframe['heure'] = pd.to_timedelta(dataframe['heure']).apply(lambda x: f"{x.components.hours}:{x.components.minutes:02d}:{x.components.seconds:02d}")
    return dataframe

def fonction_de_construction_projet():
    st.title(":construction::rotating_light: :red[project in progresse] :rotating_light::construction:")

def afichage_de_la_page_aceille():
    #appèle des image sur internet
    image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Gwenn_ha_Du_%2811_mouchetures%29.svg/langfr-1024px-Gwenn_ha_Du_%2811_mouchetures%29.svg.png'
    image2 = 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Plan_bibus_2016-2017.png'
    #création d'un tableau pour metre le titre et l'image du drapeau breton a la suite
    col1, col2 = st.columns([1.5, 2])
    #afichage du titre et des deux image
    col1.title(":red[Br]:orange[ei]:green[zh]:blue[ib]:violet[us] :bus:")
    col2.image(image, caption=None, width=100, use_column_width=False, channels='RGB', output_format='auto')
    st.image (image2, caption="reseau de busse de Brest")

def aficher_histogramme_des_frequantation_par_lignes():
 
    query = """SELECT lignes.nom AS ligne, SUM(frequentation.nombre_passagers) 
    AS total_passagers FROM frequentation
    INNER JOIN horaires ON frequentation.horaire = horaires.id
    INNER JOIN lignes ON horaires.ligne = lignes.id
    GROUP BY lignes.nom;
    """
    dataframe=get_data(query)
    
    sb.set(rc={'axes.facecolor':'#FEEAA1', 'figure.facecolor':'#D6955B'})

    st.title("Fréquentations par ligne :bus: :")

    fig = ml.figure(figsize=[14,9],dpi=100)

    ax = sb.barplot(x="ligne", y="total_passagers", data=dataframe, palette = ["red", "green", "blue", "black"], saturation = .55)
    ml.ylim((220, 290))
    ml.ylabel('Nombre de passagers')
    ml.xlabel('Lignes')
    ml.title('Histogramme des fréquentations par lignes')

    for i in ax.containers:
        ax.bar_label(i)

    st.pyplot(fig)

def aficher_frequentation_par_heures():
    query = """
            SELECT horaires.heure AS horaire, SUM(frequentation.nombre_passagers) AS total_passagers
            FROM frequentation
            INNER JOIN horaires ON frequentation.horaire = horaires.id
            GROUP BY horaires.heure;
            """
    dataframe=get_data(query)

    sb.set(rc={'axes.facecolor':'#FEEAA1', 'figure.facecolor':'#D6955B'})

    st.title("Fréquentations par heure :bus::")

    fig=ml.figure(figsize=[14,9], dpi=100)
    ax = sb.lineplot(x="horaire", y="total_passagers", data=dataframe, linewidth=8, color=(0.0, 0.0, 1.0, .55))
    ml.ylim((0, 150))
    ml.ylabel('Nombre de passagers')
    ml.xlabel('Heures')
    ml.title('Fréquentations par heure')

    st.pyplot(fig)

def aficher_camembert_des_frequantation_par_jours():
    query = """
            SELECT frequentation.jour AS Jour, SUM(frequentation.nombre_passagers) AS Total_Passagers
            FROM frequentation
            GROUP BY frequentation.jour;
            """
    dataframe=get_data(query)

    sb.set(rc={'axes.facecolor':'#FEEAA1', 'figure.facecolor':'#D6955B'})

    st.title("Fréquentations par jour :bus::")

    fig=ml.figure(figsize=[11,8],dpi=100)
    ml.pie(dataframe['Total_Passagers'], labels=dataframe['Jour'], autopct='%1.1f%%', startangle=90)
    ml.title('Répartition des fréquentations par jour')

    st.pyplot(fig)

def aficher_des_horaire_par_ligne():
    query = "Select l.nom as ligne,h.heure,a.libelle as arret,a.adresse from horaires h left join arrets a on a.id=h.arret left join lignes l on l.id=h.ligne"
    dataframe=format_heure(get_data(query))

    option = dataframe['ligne'].drop_duplicates()
    option = st.selectbox('Choisissez votre ligne', dataframe['ligne'].unique())
    st.write(f"Les horaires pour la ligne {option}: ")

    st.dataframe(dataframe[dataframe['ligne'] == option].reset_index(drop=True).drop('ligne', axis=1))

 