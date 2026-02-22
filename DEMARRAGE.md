# 🚀 DÉMARRAGE RAPIDE

## Pour lancer VoiceSnap

**Double-cliquez sur :** `LAUNCH.bat`

C'est tout ! 🎉

---

## ❌ Si ça ne marche pas

### 1. Première fois seulement - Installer les dépendances

Ouvre un terminal dans le dossier `voicesnap` et lance :

```cmd
npm install
cd python
pip install -r requirements.txt
cd ..
```

### 2. Ensuite relance

```cmd
LAUNCH.bat
```

---

## 🎙️ Utilisation

1. **Lancer l'app** : Double-clic sur `LAUNCH.bat`
2. **Enregistrer** : Appuie sur **Ctrl+Space** (n'importe où)
3. **Arrêter** : Appuie encore sur **Ctrl+Space**
4. **Voir la transcription** : Elle apparaît automatiquement et est copiée !

---

## 🐛 Problèmes ?

### Le backend ne démarre pas

**Regarde la fenêtre "VoiceSnap Backend"** qui s'ouvre - elle montre les erreurs.

**Erreurs communes :**
- `ModuleNotFoundError` → Lance `pip install -r python/requirements.txt`
- `Port already in use` → Un autre programme utilise le port 8765

### L'interface ne s'affiche pas

**Vérifie :**
- Node.js est installé : `node --version`
- Les dépendances sont installées : `npm install`

---

## 📝 Raccourcis

- **Ctrl+Space** : Enregistrer / Arrêter
- **F12** : Console développeur (pour debug)

---

Créé le 2026-02-22 🤖
