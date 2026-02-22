# 🚀 VoiceSnap - Lanceurs Windows

**3 façons de lancer VoiceSnap sur Windows**

---

## 🎯 TL;DR - Utilise ceci

```cmd
cd voicesnap
start.bat
```

C'est tout ! 🎉

---

## 📋 Les 3 Options

### 1️⃣ **start.bat** - Le plus simple (RECOMMANDÉ pour débuter)

**Utilisation :**
```cmd
start.bat
```

**Ce qu'il fait :**
- Lance le backend Python
- Lance l'interface Tauri dev
- Tout est prêt en ~10 secondes

**Avantages :**
- ✅ Pas de compilation
- ✅ Rapide
- ✅ Facile à modifier

**Inconvénients :**
- ⚠️ Besoin de Python + Node installés
- ⚠️ Ouvre une fenêtre console

---

### 2️⃣ **launcher.py → .exe** - Le launcher compilé

**Utilisation :**
```cmd
build_exe.bat          REM Compile le launcher
dist\VoiceSnap.exe     REM Lance l'app
```

**Ce qu'il fait :**
- Compile `launcher.py` en .exe standalone
- Double-clic → tout démarre automatiquement

**Avantages :**
- ✅ Un seul fichier .exe
- ✅ Plus "pro" qu'un .bat
- ✅ Peut avoir une icône

**Inconvénients :**
- ⚠️ Besoin de compiler (5-10 min)
- ⚠️ Toujours besoin de Python + Node installés

---

### 3️⃣ **Tauri Build** - L'app complète standalone

**Utilisation :**
```cmd
npm run tauri:build
src-tauri\target\release\bundle\msi\VoiceSnap_3.0.0_x64.msi
```

**Ce qu'il fait :**
- Compile TOUTE l'app en binaire natif
- Crée un installateur .msi Windows

**Avantages :**
- ✅ Vrai .exe standalone professionnel
- ✅ Installateur Windows
- ✅ Hotkey global (Ctrl+Space)
- ✅ Optimisé et rapide

**Inconvénients :**
- ⚠️ Nécessite Rust installé
- ⚠️ Compilation longue (30-60 min)
- ⚠️ Backend Python toujours nécessaire

---

## 🎯 Quel launcher choisir ?

| Besoin | Solution |
|--------|----------|
| **Tester rapidement** | `start.bat` |
| **Utilisation quotidienne** | `launcher.py` → .exe |
| **Distribuer à d'autres** | Tauri Build |
| **Production finale** | Tauri Build |

---

## 🛠️ Installation (première fois)

### Sur ton PC Windows PA (192.168.1.193)

1. **Cloner/Copier le projet**
   ```cmd
   cd C:\Users\PA\Projects
   git clone <repo-url> voicesnap
   cd voicesnap
   ```

2. **Installer Node dependencies**
   ```cmd
   npm install
   ```

3. **Installer Python dependencies**
   ```cmd
   cd python
   pip install -r requirements.txt
   cd ..
   ```

4. **Lancer**
   ```cmd
   start.bat
   ```

C'est prêt ! 🎉

---

## 📝 Notes importantes

### Backend Python obligatoire

**Pourquoi ?**  
Whisper AI (transcription) nécessite Python. Impossible de tout compiler en Rust pur.

**Solutions :**
- **Locale** : Bundler Python avec l'app (complexe)
- **Cloud** : Utiliser une API Whisper externe (payant)
- **Hybride** : Demander Python comme prérequis

Pour l'instant, VoiceSnap nécessite Python installé.

### Structure des lanceurs

```
start.bat          → Lance directement (dev mode)
launcher.py        → Script Python avec gestion propre
build_exe.bat      → Compile launcher.py en .exe
BUILD_WINDOWS.md   → Guide complet
```

---

## 🐛 Si ça marche pas

### "Python n'est pas reconnu"
```cmd
REM Vérifie que Python est dans le PATH
python --version

REM Si ça marche pas, réinstalle Python avec "Add to PATH" coché
```

### "npm n'est pas reconnu"
```cmd
REM Pareil pour Node
node --version
npm --version

REM Réinstalle Node.js si besoin
```

### Le backend ne démarre pas
```cmd
REM Lance manuellement pour voir l'erreur
cd python
python server.py
```

### Port 8765 déjà utilisé
```cmd
REM Trouve le processus
netstat -ano | findstr :8765

REM Tue-le (remplace <PID> par le numéro)
taskkill /PID <PID> /F
```

---

## ✨ Améliorations futures

- [ ] Auto-install Python si absent
- [ ] Bundler Python dans l'exe
- [ ] Menus contextuels Windows
- [ ] Démarrage avec Windows
- [ ] Icône système tray
- [ ] Updates automatiques

---

**Besoin d'aide ?** Ping @ClawdBot sur Discord ! 🤖

---

**Créé le 2026-02-22**
