<img src="picture/titre6.png" alt="Monero EasyNode top">
<div align="center">

## Make easy a MONERO Node 

<img src="picture/logo2.png" width="300" height="300" alt="Monero EasyNode Logo">
</div>

<hr style="border-top: 3px solid orange;">
<b>'EasyNode'</b> turns installing a <b>'MONERO node'</b> into a quick and easy blockchain process, perform all staps in less than 10 minutes!

Then download its blockchain...

Finally, start your adventure, you are sovereign...

You can use it in 🐧Linux versions or 🪟 windows  10/11 in wsl version. 

No knowledge required. Select step 1,2,3,4,5 and you're done. 
After Boot to your internal drive, 6, or move the blockchain to your external disk, 8.

The node is protected by Tor and an onion address allows you to connect to a mobile wallet.
An SSH onion address is available to access the node remotely.
Added the 'MRL' IP bann list of 'boog900'.

🇬🇧 English- 🇫🇷French language.

Enjoy.


## 📥 Download:

<div align="center">

| Version | Links |
|---------|------|
| 🐧 Linux | [![Linux](https://img.shields.io/badge/Download-EasyNode_Linux-orange?style=for-the-badge)](https://github.com/kerlannXmr/Monero_EasyNode/releases/download/v1.0/easynode_linux.sh) |
| 🪟 WSL | [![WSL](https://img.shields.io/badge/Download-EasyNode_WSL-orange?style=for-the-badge)](https://github.com/kerlannXmr/Monero_EasyNode/releases/download/v1.0/easynode_wsl.sh) |

</div>

## 🖥️ Interface:
<div align="center">
<img src="picture/linux-interface.png" width="310" alt="Linux Interface">
<img src="picture/wsl_interface.png" width="316" alt="wsl Interface">
</div>

## 📝 HOW TO

### Internal disk :
- Follow the stap 1➡️2➡️3➡️4➡️5
- Then do : Stap 6

### External Disk :
- Follow the stap 1➡️2➡️3➡️4➡️5
- Then do : Stap 8 and 6

## 🚀 Installation

### 🐧 Linux :
⮕ Download this script, then open a terminal and make it executable:
```bash
wget https://github.com/kerlannXmr/Monero_EasyNode/releases/latest/download/easynode_linux

chmod +x easynode_linux.sh
sudo ./easynode_linux.sh
```

### 🪟 Windows (WSL) :
WSL Ubuntu in widows 10/11:

-🔹 Go to Microsoft Store, then in search type Ubuntu, click on Ubuntu 24LTS.

Other:

-🔸 In powershell administrator:
```bash
wsl --install
```
learn.microsoft.com/fr-fr/windows/wsl/install

learn.microsoft.com/en-us/windows/wsl/install

⮕ Download this script, then open a terminal and make it executable:
```bash
wget https://github.com/kerlannXmr/Monero_EasyNode/releases/latest/download/easynode_wsl

chmod +x easynode_wsl.sh
sudo ./easynode_wsl.sh
```

## ⚡ Features

- ✅ Automated installation
- ✅ allow firewall port
- ✅ Monero configuration
- ✅ Disk management (internal/external)
- ✅ Built-in Tor (Tor/SSH onion address)
- ✅ Anonymous DNS
- ✅ Block IP 'ban listed' (MRL)
- ✅ SSH remote access
- ✅ Intuitive user interface
- ✅ no knowledge required

## ⚠️ Important

-➡🟧 REDIRECT port 22 and 18080 from your internet router to your ' local ip ' of your PC.

-➡📗  Remote access wallet:
  
  Take 'cake wallet', settings, connect and sync, manage nodes, add +, node address= onion Tor, node port= 18089, save. Close and open. Wait the sync.
  
-➡📗  Remote access ssh:
  
  Open terminal pc or take 'Termux' on android: ' ssh username@local_ip_pc ' . Or ' ssh username@onion_ssh_address '.
  
-➡🟧 Stop the Blockchain : CTRL+C (1 times)

## 🔄 Compatibility
| Distribution | Compatibilité | Notes |
|--------------|---------------|--------|
| Debian | ✅ | Distribution de base |
| Ubuntu et dérivés |✅||
| Lubuntu | ✅ | LXDE/LXQt |
| Kubuntu | ✅ | KDE |
| Xubuntu | ✅ | XFCE |
| Ubuntu Budgie | ✅ | Budgie |
| Ubuntu MATE | ✅ | MATE |
| Ubuntu Studio | ✅ | Multimédia |
| Mint et dérivés |✅||
| Linux Mint | ✅ | Basé sur Ubuntu |
| LMDE | ✅ | Basé sur Debian |
| Tails |✅ | Nécessite configuration supplémentaire |
| Parrot OS | ✅ | OS Sécurisé |
| PureOS | ✅ | OS Sécurisé |
| Kali Linux | ✅ | OS Sécurisé |
| BackBox | ✅ | OS Sécurisé |
| Fedora |❌||
| SUSE |❌ ||
| Gnome | ✅ | Environment de bureau |
| KDE Plasma | ✅ | Environment de bureau |
| Linux Lite | ✅ | Léger |
| Gentoo |❌ ||
| Elementary OS | ✅ | Basé sur Ubuntu |
| MX Linux | ✅ | Basé sur Debian |
| Zorin OS | ✅ | Basé sur Ubuntu |
| AntiX | ✅ | Léger |
| Bodhi Linux | ✅ | Léger |
| Deepin | ✅ | Basé sur Debian |
| KDE neon | ✅ | Basé sur Ubuntu |
| Voyager | ✅ | Basé sur Debian |
| Watttos | ✅ | Basé sur Debian |
|Arch Linux |❌ ||

These distributions must be 64-bit, as the script is designed for x86_64 architecture.



# Paquets installés par EASYNODE

| Catégorie | Paquets | Description |
|-----------|---------|-------------|
| **Outils Système** | build-essential | Outils de compilation et build |
| | software-properties-common | Gestion des dépôts APT |
| | apt-transport-https | Support HTTPS pour APT |
| | curl | Transfert de données |
| | wget | Téléchargement de fichiers |
| | git | Système de contrôle de version |
| | gnupg | Chiffrement et signatures |
| | lsb-release | Informations sur la distribution |
| **Compression** | bzip2 | Compression bzip2 |
| | libbz2-dev | Bibliothèques bzip2 |
| | zip | Compression zip |
| | unzip | Décompression zip |
| | tar | Archivage tar |
| | gzip | Compression gzip |
| **Réseau** | net-tools | Outils réseau basiques |
| | openssh-server | Serveur SSH |
| | ufw | Pare-feu simple |
| | fail2ban | Protection contre les attaques |
| | nmap | Scanner de ports |
| | tcpdump | Analyseur de paquets |
| | htop | Moniteur de processus |
| | iftop | Moniteur de bande passante |
| | iotop | Moniteur d'I/O |
| **Python** | python3 | Interpréteur Python 3 |
| | python3-pip | Gestionnaire de paquets Python |
| | python3-dev | Headers et libs Python |
| **Éditeurs** | vim | Éditeur de texte avancé |
| | nano | Éditeur de texte simple |

## 📞 Support

- Consult the [Documentation](https://tinyurl.com/kerlann)

<div align="center">

---
🙏 <b>Make donnation with 'cake wallet' to : ' kerlann.xmr '</b>🙏
---
Made with ❤️ by [KerlannXmr](https://github.com/kerlannXmr)

</div>
