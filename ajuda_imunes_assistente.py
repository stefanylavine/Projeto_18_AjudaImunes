
import os
import streamlit as st
from groq import Groq

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Ajuda Imunes AI Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PROMPT DO ASSISTENTE
# ==========================================

CUSTOM_PROMPT = """
Você é o Ajuda Imunes AI Coder, um assistente especializado
em programação, principalmente em Python.

Sua missão é ajudar iniciantes com explicações claras,
precisas e didáticas.

REGRAS:

1. Responda apenas sobre programação, algoritmos,
estruturas de dados, bibliotecas e frameworks.

2. Organize as respostas com:
- Explicação clara do conceito.
- Exemplo de código Python comentado.
- Explicação das principais partes do código.
- Documentação oficial relevante.

3. Utilize linguagem simples e objetiva.

4. Se a pergunta não for sobre programação,
explique educadamente qual é o foco do assistente.

5. Inclua links para documentações oficiais
sempre que forem relevantes.
"""

# ==========================================
# BARRA LATERAL
# ==========================================

with st.sidebar:
    st.title("🤖 Ajuda Imunes AI Coder")

    st.markdown(
        "Seu assistente de inteligência artificial "
        "para aprender programação Python."
    )

    st.markdown("---")

    groq_api_key = st.text_input(
        "🔑 Chave da API Groq",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    st.markdown("---")

    st.info(
        "💡 Utilize o assistente para aprender, "
        "resolver dúvidas e compreender códigos."
    )

    st.caption(
        "A IA pode cometer erros. "
        "Verifique as respostas e a documentação."
    )

# ==========================================
# TÍTULO PRINCIPAL
# ==========================================

st.title("🐍 Ajuda Imunes AI Coder")

st.subheader("Seu assistente pessoal de programação")

st.caption(
    "Faça perguntas sobre Python e receba exemplos, "
    "explicações e referências."
)

st.markdown("---")

# ==========================================
# HISTÓRICO DE CONVERSAS
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# CONEXÃO COM A API GROQ
# ==========================================

client = None

if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        st.sidebar.error(
            f"Erro ao inicializar o cliente Groq: {e}"
        )

# ==========================================
# CHAT COM INTELIGÊNCIA ARTIFICIAL
# ==========================================

prompt = st.chat_input("💬 Qual é sua dúvida sobre Python?")

if prompt:
    if not client:
        st.warning(
            "Insira uma chave válida da API Groq "
            "na barra lateral para começar."
        )
    else:
        # Salva e exibe a pergunta do usuário
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepara o histórico enviado à API
        messages_for_api = [
            {"role": "system", "content": CUSTOM_PROMPT}
        ]

        messages_for_api.extend(
            st.session_state.messages
        )

        # Gera a resposta da inteligência artificial
        with st.chat_message("assistant"):
            with st.spinner("Analisando sua pergunta..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=messages_for_api,
                        model="openai/gpt-oss-20b",
                        temperature=0.7,
                        max_tokens=2048
                    )

                    resposta = (
                        chat_completion.choices[0].message.content
                    )

                    if not resposta:
                        resposta = "Não foi possível gerar uma resposta."

                    st.markdown(resposta)

                    # Salva a resposta no histórico
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": resposta
                        }
                    )

                except Exception as e:
                    st.error(
                        "Ocorreu um erro ao se comunicar "
                        f"com a API da Groq: {e}"
                    )

# ==========================================
# RODAPÉ
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <p>
            🤖 Ajuda Imunes AI Coder
        </p>
        <p>
            Desenvolvido para incentivar o aprendizado
            de programação e inteligência artificial.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
