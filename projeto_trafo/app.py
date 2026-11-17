import math
import pandas as pd
import streamlit as st
import schemdraw
import schemdraw.elements as elm
from circuit import gerar_svg_circuito

st.set_page_config(page_title="Modelo em L - Transformador", layout="centered")
st.title("Parâmetros e Circuito Equivalente em L")
st.markdown(
    """
    <style>
    /* Força qualquer SVG dentro do markdown ou container a respeitar 100% da largura */
    div.stMarkdown svg, div.element-container svg {
        max-width: 100% !important;
        height: auto !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# footer style

footer="""<style>
::-webkit-scrollbar {
            display: none !important;
        }
        * {
            -ms-overflow-style: none !important;  /* IE/Edge */
            scrollbar-width: none !important;  /* Firefox */
        }

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #0e1117;
color: #f1f1f1;
text-align: right;
}

p{
    padding-right:10px;
}
</style>
<div class="footer">
<p>Projeto IFMG Itabirito</p>
<p>Leandro H. B. Campos & Andresa A. S. Cotta</p>
</div>
"""



# 1. Entradas dos Ensaios (na barra lateral)
with st.sidebar:
    st.header("Dados dos Ensaios")
    st.subheader("Ensaio a Vazio (VZ)")
    v_vz = st.number_input("Tensão VZ (V)", value=240.0, step=1.0)
    i_vz = st.number_input("Corrente VZ (A)", value=7.133, format="%.3f")
    p_vz = st.number_input("Potência VZ (W)", value=400.0, step=1.0)

    st.subheader("Ensaio de Curto-Circuito")
    v_cc = st.number_input("Tensão CC (V)", value=489.0, step=1.0)
    i_cc = st.number_input("Corrente CC (A)", value=2.5, step=0.1)
    p_cc = st.number_input("Potência CC (W)", value=240.0, step=1.0)

    st.subheader("Referência do Circuito")
    relacao_a = st.number_input("Relação de transformação (a = V_AT / V_BT)", value=1.0, min_value=0.01, step=0.1)
    referir_para = st.radio("Referir parâmetros ao lado:", ["Manter nos lados medidos", "Lado de Alta (AT)", "Lado de Baixa (BT)"])


rc = (v_vz ** 2) / p_vz if p_vz > 0 else 0.0
s_vz = v_vz * i_vz
q_vz = math.sqrt(max(0.0, s_vz**2 - p_vz**2))
xm = (v_vz ** 2) / q_vz if q_vz > 0 else 0.0

req = p_cc / (i_cc ** 2) if i_cc > 0 else 0.0
z_cc = v_cc / i_cc if i_cc > 0 else 0.0
xeq = math.sqrt(max(0.0, z_cc**2 - req**2))


if referir_para == "Lado de Alta (AT)":
    rc *= (relacao_a ** 2)
    xm *= (relacao_a ** 2)
elif referir_para == "Lado de Baixa (BT)":
    req /= (relacao_a ** 2)
    xeq /= (relacao_a ** 2)


st.subheader("Parâmetros Calculados")
df_params = pd.DataFrame({
    "Parâmetro": ["Rc (Perdas no Núcleo)", "Xm (Magnetização)", "Req (Resistência Equiv.)", "Xeq (Reatância Equiv.)"],
    "Símbolo": ["Rc", "jXm", "Req", "jXeq"],
    "Valor (Ω)": [f"{rc:.2f} Ω", f"j{xm:.2f} Ω", f"{req:.2f} Ω", f"j{xeq:.2f} Ω"]
})
st.dataframe(df_params, hide_index=True, use_container_width=True)



svg_bytes = gerar_svg_circuito(rc, xm, req, xeq)

st.subheader("Circuito Equivalente em L")
svg_str = svg_bytes.decode("utf-8")


st.markdown(
    f'<div style="background-color: white; padding: 16px; border-radius: 8px; text-align: center">{svg_str}</div>',
    unsafe_allow_html=True
)

st.markdown(footer,unsafe_allow_html=True)
