"""
NdimbalIA — Interface chatbot de l'assistant RAG (démarches administratives du Sénégal).
« ndimbal » = aide / assistance (wolof).

Lancer depuis la racine du projet :
    streamlit run app_ui.py

L'index se construit automatiquement au premier lancement (il faut data/corpus + GROQ_API_KEY).
"""
import os

import streamlit as st

st.set_page_config(page_title="NdimbalIA — Démarches administratives",
                   page_icon="🇸🇳", layout="centered")

# --------------------------------------------------------------------------- #
# Style
# --------------------------------------------------------------------------- #
st.markdown(
    """
    <style>
      .block-container { padding-top: 1.6rem; padding-bottom: 6rem; max-width: 820px; }
      header[data-testid="stHeader"] { background: transparent; }

      .nd-header {
        background: linear-gradient(120deg, #15294a 0%, #1C345C 55%, #35527e 100%);
        border-radius: 18px; padding: 26px 30px; color: #fff; margin-bottom: 18px;
        box-shadow: 0 6px 20px rgba(21,41,74,.25);
      }
      .nd-header .nd-logo { font-size: 30px; }
      .nd-header h1 { margin: 2px 0 0; font-size: 30px; letter-spacing:.3px; }
      .nd-header p { margin: 6px 0 0; color:#C9D8F5; font-size: 15px; max-width: 640px; }

      .nd-welcome { background:#F6F9FD; border:1px solid #E1E9F4; border-radius:14px;
                    padding:18px 20px; margin: 4px 0 10px; }
      .nd-welcome h4 { margin:0 0 6px; color:#1C345C; }
      .nd-welcome p { margin:0; color:#5A6472; font-size:14.5px; }

      .nd-badge { display:inline-block; background:#EEF3FA; color:#1C345C; border:1px solid #CFE0F6;
                  border-radius:999px; padding:2px 11px; font-size:12px; margin:2px 6px 2px 0; }
      .nd-src b { color:#1C345C; }
      .nd-src { font-size:13px; color:#3a4452; line-height:1.4; margin-bottom:10px; }
      [data-testid="stChatMessageContent"] p { font-size:15.5px; }
      .stButton button { border-radius:10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="nd-header">
      <div class="nd-logo">🇸🇳</div>
      <h1>NdimbalIA</h1>
      <p>Votre assistant des démarches administratives du Sénégal.
      Posez votre question : la réponse s'appuie sur des documents publics, avec ses sources.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

EXEMPLES = [
    "Quels documents pour un passeport ?",
    "Comment obtenir un extrait de naissance ?",
    "Combien coûte une CNI biométrique ?",
    "Où demander un casier judiciaire ?",
]
USER_AVATAR = "🧑"
BOT_AVATAR = "🇸🇳"


# --------------------------------------------------------------------------- #
# Préparation du moteur (construit l'index si nécessaire — une seule fois)
# --------------------------------------------------------------------------- #
@st.cache_resource(show_spinner=False)
def prepare():
    from src.rag.pipeline import _store
    store = _store()
    try:
        vide = store._collection.count() == 0
    except Exception:
        vide = True
    if vide:
        from src.rag.build_index import main as build_index
        build_index()
        _store.cache_clear()
    from src.advanced.pipeline_advanced import answer_advanced
    return answer_advanced


with st.spinner("Préparation du moteur (au premier lancement : indexation du corpus)…"):
    try:
        answer_fn = prepare()
        moteur_ok = True
    except Exception as e:
        answer_fn, moteur_ok = None, False
        st.error(
            "Le moteur n'a pas pu démarrer. Vérifie que `data/corpus/` existe et que "
            f"`GROQ_API_KEY` est renseignée dans `.env`.\n\nDétail : {e}"
        )


# --------------------------------------------------------------------------- #
# Barre latérale
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.markdown("### 🇸🇳 NdimbalIA")
    st.caption(
        "Assistant des démarches administratives du Sénégal (CNI, passeport, état civil, "
        "casier judiciaire, résidence, permis). Réponses sourcées à partir de documents publics.\n\n"
        "Projet P1IA — Groupe 1, Orange Digital Center."
    )
    st.markdown("**Exemples de questions**")
    for ex in EXEMPLES:
        if st.button(ex, use_container_width=True, key="ex_" + ex):
            st.session_state["pending"] = ex
            st.rerun()
    st.divider()
    if st.button("🗑️ Nouvelle conversation", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
    st.caption("Moteur : LangChain · Chroma · Groq")


# --------------------------------------------------------------------------- #
# État & affichage
# --------------------------------------------------------------------------- #
if "messages" not in st.session_state:
    st.session_state["messages"] = []


def render(msg):
    avatar = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] != "assistant":
            return
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
                    st.markdown(
                        f'<div class="nd-src"><b>{nom}</b><br>{p.get("texte","")[:260]}…</div>',
                        unsafe_allow_html=True,
                    )
        obs = msg.get("obs")
        if obs:
            st.caption(f"⏱️ {obs['lat']:.2f}s · {obs['tok']} tokens · ~{obs['cout']:.6f} $")


# Accueil (conversation vide)
if not st.session_state["messages"]:
    st.markdown(
        """
        <div class="nd-welcome">
          <h4>👋 Bonjour ! Comment puis-je vous aider ?</h4>
          <p>Demandez-moi les pièces à fournir, les lieux, les délais ou les coûts d'une démarche.
          Choisissez un exemple dans le menu de gauche ou écrivez votre question ci-dessous.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

for m in st.session_state["messages"]:
    render(m)


# --------------------------------------------------------------------------- #
# Entrée utilisateur
# --------------------------------------------------------------------------- #
prompt = st.chat_input("Posez votre question sur une démarche…", disabled=not moteur_ok)
if not prompt and st.session_state.get("pending"):
    prompt = st.session_state.pop("pending")

if prompt and moteur_ok:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.spinner("NdimbalIA cherche dans le corpus…"):
        try:
            res = answer_fn(prompt)
        except Exception as e:
            res = {"reponse": f"⚠️ Erreur : {e}", "passages": [], "securite": {},
                   "observabilite": {}, "outils": []}

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
