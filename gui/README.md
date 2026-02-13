# ⬡ EasyMonerod GUI

**Interface graphique pour installer et gérer un nœud Monero sur Linux**  
*Basé sur [EasyMonerod v5](https://github.com/kerlannXmr/EasyMonerod) par kerlannXmr*

![Monero](https://img.shields.io/badge/Monero-FF6600?style=for-the-badge&logo=monero&logoColor=white)
![GTK4](https://img.shields.io/badge/GTK4-4A86CF?style=for-the-badge&logo=gnome&logoColor=white)
![Python](https://img.shields.io/badge/Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

---

## 🇬🇧 English

### What is this?

EasyMonerod GUI is a **graphical interface** to install a full Monero node on Linux **without any technical knowledge**. It's the visual version of the EasyMonerod bash script.

### Installation (simple method)

```bash
# 1. Download install.sh in personnal folder

# 2. Open a terminal 

# 3. Make the script executable
chmod +x install.sh

# 4. Run installation
sudo bash install.sh
```

**That's it!** The app appears in your Applications menu as **EasyMonerod**.

### Launch

- **Applications Menu** → search "EasyMonerod"
- **Terminal** → type `easymonerod-gui`

### Usage

1. Choose your language (Français / English)
2. Follow the steps in order: **1 ➜ 2 ➜ 3 ➜ 4 ➜ 5 ➜ 6**
3. Each step has a **▶ Confirm** button to execute
4. The integrated terminal shows real-time progress

### Uninstall

```bash
sudo bash uninstall.sh
```
---

## 🇫🇷 Français

### Qu'est-ce que c'est ?

EasyMonerod GUI est une **interface graphique** qui permet d'installer un nœud complet Monero sur Linux **sans aucune connaissance technique**. C'est la version visuelle du script bash EasyMonerod.

### Installation (méthode simple)

```bash
# 1. Télécharger install.sh dans ton dossier personnel

# 2. Ouvrir un terminal

# 3. Rendre le script exécutable
chmod +x install.sh

# 4. Lancer l'installation
sudo bash install.sh
```

**C'est tout !** L'application apparaît dans votre menu Applications sous le nom **EasyMonerod**.

### Lancement

- **Menu Applications** → cherchez "EasyMonerod"
- **Terminal** → tapez `easymonerod-gui`

### Utilisation

1. Choisissez votre langue (Français / English)
2. Suivez les étapes dans l'ordre : **1 ➜ 2 ➜ 3 ➜ 4 ➜ 5 ➜ 6**
3. Chaque étape a un bouton **▶ Confirmer** pour l'exécuter
4. Le terminal intégré affiche la progression en temps réel

### Étapes disponibles

| # | Fonction | Description |
|---|----------|-------------|
| 0 | Guide | Comment utiliser le programme |
| 1 | Mise à jour système | Installe les paquets, configure le firewall, SSH, fail2ban |
| 2 | Installer Monero CLI | Télécharge et vérifie (GPG) Monero v0.18.4.5 |
| 3 | Installer Tor | Configure les services cachés Tor |
| 4 | Configurer bitmonero | Crée bitmonero.conf avec options de sécurité RPC |
| 5 | Configurer DNS | Configure les DNS anonymes (AdGuard) |
| 6 | DÉMARRER | Lance la blockchain (complète/pruned, avec/sans ban IP) |
| 7 | ARRÊTER | Stoppe la blockchain |
| 8 | Disque externe | Configure la blockchain sur un disque externe |
| 9 | Disque interne | Revient au disque interne |
| 11 | Infos | Informations sur les ports et la configuration |
| 12 | Notes | Liens utiles, dons, contact |

### Désinstallation

```bash
sudo bash uninstall.sh
```
---

## ⚠️ Important

**Redirect port 22 and 18080** from your internet router to your PC's local IP address.  
→ [Guide](https://github.com/kerlannXmr/EasyMonerod/issues/10)

## 🙏 Donations

MONERO (XMR) : `kerlann.xmr` (via Cake Wallet)

## 📧 Contact

- Email: easynode@kerlann.org
- Source: https://github.com/kerlannXmr/easymonerod

## 🔒 PRIVACY MATTERS 🔒
---
