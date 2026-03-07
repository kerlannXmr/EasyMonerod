# ⬡ EasyMonerod GUI

**Simple GUI interface to install and manage a Monero node on Linux in 5 stape in less than 10 minutes**  
*Gui mode of [EasyMonerod v5](https://github.com/kerlannXmr/EasyMonerod) by kerlannXmr*

[![contact_Mail](https://img.shields.io/badge/✉️_Email-FF6600?style=flat&logoColor=white)](mailto:easynode@kerlann.org)
[![GitHub-page](https://img.shields.io/badge/Page--WEB-FF6600?style=flat&logo=github&logoColor=white)](https://easynode.kerlann.org)
[![Monero-ecosystem](https://img.shields.io/badge/🧭_Ecosystem-FF6600?style=flat&logoColor=white)](https://easynode.kerlann.org/ecosystem.html)
[![Bank-Exit](https://img.shields.io/badge/🇫🇷_Bank_Exit-FF6600?style=flat&logoColor=white)](https://bank-exit.org/tutoriels/monero-node-easymonerod)
[![Monerica](https://img.shields.io/badge/≣_Monerica-FF6600?style=flat&logoColor=white)](https://monerica.com/nodes)

# 📸 Screenshot

![EasyMonerod GUI](https://github.com/kerlannXmr/EasyMonerod/blob/main/gui/picture/1.3.png)

<p align="center">
  <a href="https://video.liberta.vip/w/xajxJSb2WE5aVqnxUnzPBW?start=3s">
    ⬇️ Right-click → Open in new tab to SEE the demo video
  </a>
  </p>

---

## 🇬🇧 English

### What is this?

EasyMonerod GUI is a **graphical interface** to install a full Monero node on Linux **without any technical knowledge**. It's the visual version of the EasyMonerod bash script.

### Installation (simple method)

 1. Open a terminal 

 2. 🟢 Download install.sh in personnal folder

```bash
wget https://raw.githubusercontent.com/kerlannXmr/EasyMonerod/main/gui/install.sh -O  install.sh && sudo bash install.sh
```
 3. Run installation

 4. Search " Easymonerod " in your application


**That's it!** The app appears in your Applications menu as **EasyMonerod**.

### Launch

- **Applications Menu** → search "EasyMonerod"
- or
- **Terminal** → type `easymonerod-gui`

### Usage

1. Choose your language (Français / English)
2. Follow the steps in order: **1 ➜ 2 ➜ 3 ➜ 4 ➜ 5**
3. Each step has a **▶ Confirm** button to execute
4. The integrated terminal shows real-time progress

   ### Steps available 

| # | Function | Description | 
|---|---------|--------| 
| 0 | Guide | How to use the program | 
| 1 | System update | Install packages, configure firewall, SSH, fail2ban | 
| 2 | Install Monero CLI | Download and verify (GPG) Monero v0.18.4.5 | 
| 3 | Install Tor | Configure Tor hidden services | 
| 4 | Configure bitmonero | Creates bitmonero.conf with RPC security options | 
| 5 | Configure DNS | Configure anonymous DNS (AdGuard) | 
| 6 | START | Launches the blockchain (complete/pruned, with/without IP ban) | 
| 7 | STOP | Stop the blockchain | 
| 8 | External disk | Configure blockchain on external drive | 
| 9 | Internal disk | Returns to internal disk | 
| 11 | Info | Ports and Configuration Information | 
| 12 | Notes | Useful links, donations, contact |


### 🆕 ✅ check for updates

```bash
sudo bash install.sh
```

## 🔴 Do you want to uninstall?

### Uninstall SSH

```bash

sudo apt remove openssh-server
sudo apt purge openssh-server    
sudo apt autoremove              

```
### Uninstall Easymonerod

```bash

sudo rm -rf /opt/easymonerod-gui /usr/local/bin/easymonerod-gui /usr/share/applications/easymonerod-gui.desktop ~/install.sh

```
### Requirements

![GTK4](https://img.shields.io/badge/GTK-4.0-blue?logo=gnome&logoColor=white)
![Libadwaita](https://img.shields.io/badge/Libadwaita-1.x-4A86CF?logo=gnome&logoColor=white)
![VTE](https://img.shields.io/badge/VTE-3.91_(GTK4)-green?logo=gnome&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)

### Compatible OS

![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04+-E95420?logo=ubuntu&logoColor=white)
![Linux Mint](https://img.shields.io/badge/Linux_Mint-22+-87CF3E?logo=linuxmint&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-13+-A81D33?logo=debian&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-39+-51A2DA?logo=fedora&logoColor=white)
![Arch](https://img.shields.io/badge/Arch_Linux-supported-1793D1?logo=archlinux&logoColor=white)

### ❕ DISCLAIMER ❕

This script is designed **for dedicated Monero node PCs** with Monero_Gui and could makes system modifications.

- Don't use on primary computers first.


---


## 🇫🇷 Français

### Qu'est-ce que c'est ?

EasyMonerod GUI est une **interface graphique** qui permet d'installer un nœud complet Monero sur Linux **sans aucune connaissance technique**. C'est la version visuelle du script bash EasyMonerod.

### Installation (méthode simple)

 1. Ouvrir un terminal 

 2. 🟢 Télécharge et "install.sh" dans ton dossier personnel

```bash
wget https://raw.githubusercontent.com/kerlannXmr/EasyMonerod/main/gui/install.sh -O  install.sh && chmod +x install.sh && sudo ./install.sh
```
 3. Démarrage de l'installation et fin

 4. Cherche " Easymonerod " dans ton tirroir d'applications

**C'est tout !** L'application apparaît dans votre menu Applications sous le nom **EasyMonerod**.

### Lancement

- **Menu Applications** → cherchez "EasyMonerod"
- ou
- **Terminal** → tapez `easymonerod-gui`

### Utilisation

1. Choisissez votre langue (Français / English)
2. Suivez les étapes dans l'ordre : **1 ➜ 2 ➜ 3 ➜ 4 ➜ 5**
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

### 🆕 ✅ Mise à jour

```bash
sudo bash install.sh
```
## 🔴 Pour Désinstaller?

### Désinstalle SSH

```bash

sudo apt remove openssh-server
sudo apt purge openssh-server    
sudo apt autoremove              

```

### Désinstalle EasyMonerod

```bash

sudo rm -rf /opt/easymonerod-gui /usr/local/bin/easymonerod-gui /usr/share/applications/easymonerod-gui.desktop ~/install.sh

```

---

### Requiert

![GTK4](https://img.shields.io/badge/GTK-4.0-blue?logo=gnome&logoColor=white)
![Libadwaita](https://img.shields.io/badge/Libadwaita-1.x-4A86CF?logo=gnome&logoColor=white)
![VTE](https://img.shields.io/badge/VTE-3.91_(GTK4)-green?logo=gnome&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)

### Compatible OS

![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04+-E95420?logo=ubuntu&logoColor=white)
![Linux Mint](https://img.shields.io/badge/Linux_Mint-22+-87CF3E?logo=linuxmint&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-13+-A81D33?logo=debian&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-39+-51A2DA?logo=fedora&logoColor=white)
![Arch](https://img.shields.io/badge/Arch_Linux-supported-1793D1?logo=archlinux&logoColor=white)


## ⚠️ Important

**Redirect port 22 and 18080** from your internet router to your PC's local IP address.  
→ [Guide](https://github.com/kerlannXmr/EasyMonerod/issues/10)

## 🙏 Donations

MONERO (XMR) : `kerlann.xmr` (via Cake Wallet or Unstoppable wallet in the address Bar)

```
85oN3YjxpsbER5fEnDusRr4Gj6jxBaTSSSRZeMDP6Mb1D5qB8m5oR9y5VhAcxE5RXKADMKk7ttQ4yScXwbaSMeqH7vp5AVZ
```



## 🔒 PRIVACY MATTERS 🔒

