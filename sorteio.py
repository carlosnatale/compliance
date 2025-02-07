import streamlit as st
import pandas as pd
import random

# Carregar o dataset
def load_data():
    file_path = "gamecompliance.xlsx"  # O arquivo deve estar na mesma pasta do app
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="db")
    return df

def main():
    st.title("Sorteio Aleatório de Nomes")
    st.write("Defina a quantidade de sorteados e clique no botão para realizar o sorteio.")
    
    df = load_data()
    nomes = df["Nome"].tolist()
    
    # Selecionar a quantidade de sorteados
    qtd_sorteados = st.number_input("Quantidade de sorteados:", min_value=1, max_value=len(nomes), value=1)
    
    if st.button("Sortear"):
        sorteados = random.sample(nomes, qtd_sorteados)
        st.success("Nomes sorteados:")
        for nome in sorteados:
            st.write(f"- {nome}")

if __name__ == "__main__":
    main()
