# 🎓 Rivezli Chatbot  
### L’assistant intelligent pour réviser vos cours et documents PDF
Pour voir le démo complet aller à mon Profil Linkedin: <iframe src="https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7406102547473702912?compact=1" height="399" width="504" frameborder="0" allowfullscreen="" title="Post intégré"></iframe>

Rivezli Chatbot est une application IA interactive permettant aux étudiants de **poser des questions directement sur leurs documents PDF** (cours, supports pédagogiques, notes, etc.) et d’obtenir des **réponses fiables, contextualisées et strictement basées sur le contenu fourni**.
<img width="1918" height="739" alt="image" src="https://github.com/user-attachments/assets/0a76baf3-bdb5-41b9-86da-11d210d8be3d" />
<img width="1919" height="732" alt="image" src="https://github.com/user-attachments/assets/87a65b35-e014-43e4-a22b-b98f5d608ff6" />



---

## 🚀 Objectif du projet

Pendant les périodes de révision, parcourir de longs documents PDF peut être chronophage.  
**Rivezli Chatbot** simplifie ce processus en combinant :
- la **recherche sémantique**,
- l’**IA conversationnelle**,
- et une **interface moderne et intuitive**,

afin d’améliorer l’apprentissage et le gain de temps pour les étudiants.

---

## ✨ Fonctionnalités principales

- 📄 Téléversement de plusieurs fichiers PDF
- 🔍 Recherche sémantique intelligente dans les documents
- 💬 Chat conversationnel interactif
- 🧠 Mémoire du contexte de la conversation
- ✅ Réponses strictement limitées au contenu des documents
- ❌ Refus automatique si l’information n’existe pas dans les PDFs
- 🎨 Interface UI moderne avec bulles de chat et avatars

---

## 🧠 Architecture & Fonctionnement
<img width="1461" height="756" alt="Capture d&#39;écran 2025-12-13 131517" src="https://github.com/user-attachments/assets/25b1d493-ce3a-455a-a8bc-2721b6fd6e29" />

1. **Extraction du texte PDF**  
   → PyPDF2 lit et extrait le contenu des fichiers

2. **Découpage intelligent du texte**  
   → Segmentation en chunks avec LangChain Text Splitter

3. **Vectorisation & indexation**  
   → HuggingFace Instruct Embeddings + FAISS

4. **Recherche contextuelle**  
   → Récupération des passages les plus pertinents

5. **Génération de réponse**  
   → DeepSeek LLM via HuggingFace (ConversationalRetrievalChain)

6. **Interface utilisateur**  
   → Streamlit + HTML/CSS personnalisé

---

## 🛠️ Technologies utilisées

- **Python**
- **Streamlit**
- **LangChain**
- **DeepSeek LLM (HuggingFace)**
- **HuggingFace Instruct Embeddings**
- **FAISS**
- **PyPDF2**
- **HTML / CSS**
- **dotenv**

---

## 📦 Installation & Exécution

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/hattay112amine/-Rivezli_Chatbot-.git
cd Rivezli_Chatbot
