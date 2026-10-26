"""
NdimbalIA — Interface chatbot de l'assistant RAG (démarches administratives du Sénégal).
« ndimbal » = aide / assistance (wolof).

Lancer depuis la racine du projet :
    streamlit run app_ui.py

Prérequis : index construit (python -m src.rag.build_index) et GROQ_API_KEY dans .env.
"""
import os

import streamlit as st

st.set_page_config(page_title="NdimbalIA — Démarches administratives", page_icon="🇸🇳", layout="centered")

# --------------------------------------------------------------------------- #
# Style
# --------------------------------------------------------------------------- #
st.markdown(
    """
    <style>
      .block-container { padding-top: 2rem; max-width: 800px; }
      .nd-header { background: #1C345C; border-radius: 14px; padding: 22px 26px; color: #fff; margin-bottom: 8px; }
      .nd-header h1 { margin: 0; font-size: 30px; }
      .nd-header p { margin: 4px 0 0; color: #CADCFC; font-size: 15px; }
      .nd-badge { display:inline-block; background:#ECF1F6; color:#1C345C; border:1px solid #CADCFC;
                  border-radius:999px; padding:1px 10px; font-size:12px; margin-right:6px; }
      .nd-src { font-size: 13px; color:#1C345C; }
      .stChatMessage { font-size: 15.5px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="nd-header">
      <h1>🇸🇳 NdimbalIA</h1>
      <p>Votre assistant des démarches administratives du Sénégal — réponses sourcées à partir de documents publics.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

INDEX_DIR = "data/index/chroma"
EXEMPLES = [
    "Quels documents pour un passeport ?",
    "Comment obtenir un extrait de naissance ?",
    "Combien coûte une CNI biométrique ?",
    "Où demander un casier judiciaire ?",
]

# --------------------------------------------------------------------------- #
# Chargement du moteur (une seule fois)
# --------------------------------------------------------------------------- #
@st.cache_resource(show_spinner=False)
def get_answer_fn():
    from src.advanced.pipeline_advanced import answer_advanced
    return answer_advanced


# --------------------------------------------------------------------------- #
# Barre latérale
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.subheader("À propos")
    st.caption(
        "NdimbalIA répond à vos questions sur les démarches administratives "
        "(CNI, passeport, état civil, casier judiciaire, résidence, permis) "
        "en citant ses sources. Projet P1IA — Groupe 1, Orange Digital Center."
    )
    st.markdown("**Exemples de questions**")
    for ex in EXEMPLES:
        if st.button(ex, use_container_width=True, key="ex_" + ex):
            st.session_state["pending"] = ex
            st.rerun()
    st.divider()
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
    st.caption("Moteur : LangChain · Chroma · Groq")


# --------------------------------------------------------------------------- #
# État & garde-fou « index »
# --------------------------------------------------------------------------- #
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if not os.path.isdir(INDEX_DIR):
    st.warning(
        "⚠️ L'index n'est pas encore construit. Dans un terminal, lance :\n\n"
        "`python -m src.rag.build_index`\n\npuis recharge la page."
    )


def afficher_message(msg):
    avatar = "🧑" if msg["role"] == "user" else "🇸🇳"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            meta = msg.get("meta", {})
            badges = ""
            if meta.get("outil"):
                badges += f'<span class="nd-badge">🛠️ outil : {meta["outil"]}</span>'
            if meta.get("pii"):
                badges += f'<span class="nd-badge">🔒 {meta["pii"]} donnée(s) masquée(s)</span>'
            if meta.get("bloque"):
                badges += '<span class="nd-badge">🛡️ requête bloquée</span>'
            if badges:
                st.markdown(badges, unsafe_allow_html=True)
            passages = msg.get("passages", [])
            if passages:
                with st.expander(f"📎 Sources citées ({len(passages)})"):
                    for p in passages:
                        nom = os.path.basename(p.get("source", "?"))
                        st.markdown(f'<div class="nd-src"><b>{nom}</b><br>{p.get("texte","")[:260]}…</div>',
                                    unsafe_allow_html=True)
            obs = msg.get("obs")
            if obs:
                st.caption(
                    f"⏱️ {obs['lat']:.2f}s · {obs['tok']} tokens · ~{obs['cout']:.6f} $"
                )


# Historique
for m in st.session_state["messages"]:
    afficher_message(m)


# --------------------------------------------------------------------------- #
# Entrée utilisateur
# --------------------------------------------------------------------------- #
prompt = st.chat_input("Posez votre question sur une démarche…")
if not prompt and st.session_state.get("pending"):
    prompt = st.session_state.pop("pending")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.spinner("NdimbalIA cherche dans le corpus…"):
        try:
            res = get_answer_fn()(prompt)
        except Exception as e:  # clé API manquante, index absent, etc.
            res = {"reponse": f"⚠️ Erreur : {e}", "passages": [], "securite": {}, "observabilite": {}, "outils": []}

    sec = res.get("securite", {}) or {}
    outils = res.get("outils", []) or []
    obsraw = res.get("observabilite", {}) or {}
    obs = None
    if obsraw:
        obs = {
            "lat": obsraw.get("latences_secondes", {}).get("totale", 0.0),
            "tok": obsraw.get("tokens", {}).get("total", 0),
            "cout": obsraw.get("cout_estime_usd", 0.0),
        }
    st.session_state["messages"].append({
        "role": "assistant",
        "content": res.get("reponse", ""),
        "passages": res.get("passages", []),
        "meta": {
            "outil": outils[0]["outil"] if outils else None,
            "pii": len(sec.get("entites_masquees", [])) or None,
            "bloque": sec.get("raison") == "PROMPT_INJECTION",
        },
        "obs": obs,
    })
    st.rerun()
