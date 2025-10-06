# sections/conclusions.py
import streamlit as st

def render(df_sel, tables, filters):
    st.header("Conclusions & Implications")

    st.subheader("Insights clés")
    st.markdown(
        "- Les pays **les plus touchés** affichent des taux supérieurs à la moyenne UE la plus récente.\n"
        "- Les **écarts H/F** sont (à confirmer selon sélection) modérés/forts — à surveiller.\n"
        "- Le **gradient de revenu** montre une privation nettement plus forte dans les groupes à faible revenu.\n"
        "- Certains pays montrent des **tendances à la baisse/hausse** sur la décennie."
    )

    st.subheader("Limites & qualité de données")
    st.info(
        "- Indicateur subjectif (déclaration) : attention aux **biais d’auto-rapport**.\n"
        "- Variations méthodologiques possibles entre années/pays.\n"
        "- Agrégations (moyennes) masquent des disparités infra-nationales."
    )

    st.subheader("Pistes d’action / Next steps")
    st.markdown(
        "- Cibler des **mesures d’aide** (chèques habillement, TVA réduite ciblée) pour les groupes à risque.\n"
        "- Croiser avec **inflation textile**, **salaires médians** et **filets sociaux**.\n"
        "- Approfondir au niveau **régional** (NUTS2/3) si données disponibles."
    )

    st.subheader("Réplicabilité")
    st.caption("App prête à packager : requirements.txt, README, et CSV dans /data. Utiliser `st.cache_data` pour la perf.")
