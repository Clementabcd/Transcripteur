# 🎙 EchoScript

EchoScript est une application de bureau multiplateforme (macOS et Windows) permettant de transcrire automatiquement des fichiers audio et vidéo en texte grâce au modèle **Whisper** de Faster-Whisper.

L'application est développée en **Python** avec **PySide6** et fonctionne entièrement en local une fois le modèle téléchargé.

---

# Fonctionnalités

* 🎙 Transcription automatique de fichiers audio et vidéo
* ⚡ Utilisation de Faster-Whisper (CTranslate2)
* 🌍 Fonctionnement entièrement local
* 📥 Téléchargement automatique du modèle Whisper lors du premier lancement
* 🎵 Téléchargement automatique de FFmpeg grâce à imageio-ffmpeg
* 📄 Export au format TXT
* 📑 Export au format SRT
* 🌐 Export au format VTT
* 📦 Export au format JSON
* 🖥 Interface graphique moderne avec PySide6
* 🍎 Compatible macOS
* 🪟 Compatible Windows

---

# Technologies utilisées

* Python
* PySide6
* Faster-Whisper
* CTranslate2
* HuggingFace Hub
* imageio-ffmpeg

---

# Fonctionnement

## Premier lancement

Lors du premier démarrage :

1. EchoScript vérifie si le modèle Whisper est disponible.
2. Si nécessaire, il télécharge automatiquement le modèle.
3. FFmpeg est téléchargé automatiquement par imageio-ffmpeg.
4. Une fois l'installation terminée, l'utilisateur est invité à fermer puis relancer l'application.

Cette opération n'est effectuée qu'une seule fois.

---

## Transcription

Lorsque l'utilisateur sélectionne un fichier :

1. Vérification du format.
2. Normalisation audio avec FFmpeg.
3. Conversion en WAV mono 16 kHz.
4. Découpage automatique des longs fichiers (20 minutes maximum par segment).
5. Transcription de chaque segment avec Faster-Whisper.
6. Fusion des résultats.
7. Export dans le format choisi.

---

# Formats pris en charge

Audio :

* MP3
* WAV
* FLAC
* AAC
* OGG
* M4A

Vidéo :

* MP4
* MOV
* MKV

---

# Arborescence

```text
EchoScript/
│
├── app.py
├── gui.py
├── engine.py
├── worker.py
├── model_manager.py
├── first_launch.py
├── logger.py
├── utils.py
│
├── assets/
│   ├── icon.icns
│   ├── icon.ico
│   └── logo.png
│
├── .github/
│   └── workflows/
│       └── build.yml
│
├── requirements.txt
└── README.md
```

---

# Architecture

```
Utilisateur
      │
      ▼
Interface graphique (PySide6)
      │
      ▼
Worker (Thread)
      │
      ▼
TranscriptionEngine
      │
      ├── FFmpeg
      ├── Faster-Whisper
      └── Exports
```

---

# Gestion des modèles

Le modèle Whisper est téléchargé automatiquement par Faster-Whisper.

Le dossier de stockage dépend du système d'exploitation.

Aucun téléchargement manuel n'est nécessaire.

---

# FFmpeg

EchoScript n'exige pas que FFmpeg soit installé sur l'ordinateur.

Le projet utilise :

imageio-ffmpeg

Le binaire est téléchargé automatiquement lors de la première utilisation.

---

# Compilation

Le projet est compilé automatiquement grâce à GitHub Actions.

Les builds sont générés pour :

* macOS (.app)
* Windows (.exe)

---

# Dépendances

```text
PySide6
faster-whisper
ctranslate2
huggingface-hub
imageio-ffmpeg
```

Installation :

```bash
pip install -r requirements.txt
```

---

# Lancer en développement

```bash
python app.py
```

---

# Journalisation

Les journaux sont enregistrés dans le dossier utilisateur de l'application.

Ils permettent de diagnostiquer les erreurs éventuelles.

---

# Feuille de route

Améliorations envisagées :

* Détection automatique de la langue
* Traduction automatique
* Export DOCX
* Export PDF
* Sous-titres personnalisables
* Historique des transcriptions
* Paramètres avancés
* Accélération GPU améliorée

---

# Licence

Projet personnel développé à des fins éducatives et de productivité.

---

Développé avec ❤️ en Python.
