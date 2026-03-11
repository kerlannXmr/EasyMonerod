#!/usr/bin/env python3
"""
EasyMonerod GUI
Interfacium graphicum GTK4 pro installatione nodi Monero.
Scriptum ab easynode_linux.sh v5 auctore kerlannXmr
© 2024-2026 Kerlann — Omnia iura reservata
https://github.com/kerlannXmr/EasyMonerod/blob/main/gui/README.md
Licentia: GPL V3.0
"""
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
# Terminalis VTE - tentatio plurium versionum (versiones GTK4)
VTE_AVAILABLE = False
for vte_ver in ['3.91', '2.91']:
    try:
        gi.require_version('Vte', vte_ver)
        from gi.repository import Vte
        VTE_AVAILABLE = True
        break
    except (ValueError, ImportError):
        continue
from gi.repository import Gtk, Adw, Gdk, GLib, Gio, Pango
import subprocess
import threading
import os
import sys
import shutil
import json
import time
import signal
# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
APP_ID = "org.easymonerod.gui"
APP_NAME = "EasyMonerod"
APP_VERSION = "1.8.4.1"
MONERO_VERSION = "0.18.4.5"
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
SCRIPT_PATH = os.path.join(SCRIPT_DIR, "easynode_linux.sh")
CONFIG_FILE = os.path.expanduser("~/.config/easymonerod/settings.json")
INSTALLED_GUI_PATH = "/opt/easymonerod-gui/easymonerod_gui.py"
GITHUB_MONERO_API = "https://api.github.com/repos/monero-project/monero/releases/latest"
# ─────────────────────────────────────────────
# TRANSLATIONES
# ─────────────────────────────────────────────
TRANSLATIONS = {
    "FR": {
        "app_subtitle": "Installation facile d'un nœud Monero",
        "language_title": "SÉLECTION DE LA LANGUE",
        "menu_title": "MENU PRINCIPAL",
        "guide": "GUIDE",
        "update_system": "Installer dépendences",
        "install_monero": "Installer Monero CLI",
        "install_tor": "Installer service Tor",
        "configure_bitmonero": "Configurer bitmonero",
        "configure_dns": "Configurer DNS anonymes",
        "blockchain_section": "BLOCKCHAIN",
        "start": "DÉMARRER",
        "stop": "ARRÊTER",
        "disk_section": "Options Disque",
        "external_disk": "Blockchain sur DISQUE EXTERNE",
        "internal_disk": "Démontage du DISQUE EXTERNE",
        "other_section": "AUTRES OPTIONS",
        "change_lang": "Changer langue",
        "features": "INFOS",
        "notes": "NOTES",
        "update_gui": "Update GUI",
        "exit": "QUITTER",
        "complete": "Complète 220 Go",
        "pruned": "Prune 90 Go",
        "with_ip_ban": "Avec blocage IP",
        "without_ip_ban": "Sans blocage IP",
        "cancel": "Annuler",
        "confirm": "Confirmer",
        "username_title": "CONFIGURATION UTILISATEUR",
        "detected_user": "Utilisateur détecté :",
        "confirm_or_change": "Appuyez sur Confirmer ou tapez un autre nom :",
        "with_password": "AVEC mot de passe (Recommandé)",
        "without_password": "SANS mot de passe (Local uniquement)",
        "rpc_security": "SÉCURITÉ RPC",
        "enter_password": "Mot de passe RPC :",
        "confirm_password": "Confirmer le mot de passe :",
        "password_mismatch": "Les mots de passe ne correspondent pas",
        "password_too_short": "Le mot de passe doit avoir au moins 6 caractères",
        "running": "Fait !",
        "completed": "Terminé",
        "error": "Erreur",
        "blockchain_type": "Type de blockchain :",
        "start_mode": "Mode de démarrage :",
        "select_disk": "Dossier sélectionné :",
        "enter_disk": "Chemin du dossier :",
        "browse_folder": "📂 Parcourir...",
        "select_folder_title": "Choisir le dossier pour la blockchain",
        "no_folder_selected": "Aucun dossier sélectionné",
        "folder_configured": "✅ Dossier configuré avec succès !",
        "folder_error_empty": "⚠️ Sélectionnez un dossier d'abord",
        "folder_error_write": "⚠️ Permissions insuffisantes sur ce dossier",
        "current_datadir": "Emplacement actuel de la blockchain :",
        "stop_confirm": "Voulez-vous vraiment arrêter la blockchain ?",
        "yes": "Oui",
        "no": "Non",
        "back": "Retour",
        "guide_text": """<b>Pour une installation complète, suivez ces étapes dans l'ordre :</b>
<span foreground='#47a347'>  1️⃣ ➜ 2️⃣ ➜ 3️⃣ ➜ 4️⃣ ➜ 5️⃣</span>
<b>Puis au choix :</b>
  ▶️ Disque interne : passez directement à l'étape 8️⃣
  ▶️ Disque externe : étape 6️⃣ puis 8️⃣
<b>AUTRES :</b>
  ➡️ Étape 8 : Démarrer le nœud et configurer l'exclusion des ⛔ IP bannis
  ➡️ Étape 7 : Démonter la blockchain du disque externe
  ➡️ Étape 4 : Sert aussi pour le DEBUG du chemin d'amorçage
<span foreground='#47a347'><b>  Compatible avec :</b>
  🟢 <b>Monero GUI</b> — Portefeuille officiel (wallet)
  🟢 <b>Gupax</b> — Minage sur le pool P2Pool
  🟢 <b>RetoSwap</b> — Achat et échanges décentralisés
  🟢 <b>Autres</b> — Logiciels qui nécessitent un noeud avec le port 18081</span>
<span foreground='#e8b849'>⚠️ Important: REDIRIGER le port 22 et 18080 de votre Box internet
  vers l'adresse IP locale de votre PC</span>""",
        "features_text": """<b><span foreground='#FF6600'>1)</span> Mise à jour système et installation des paquets</b>
   - Configuration du firewall avec ouverture des ports
   - Ports system: 22(SSH), 80(HTTP), 443(HTTPS), 9050(Tor)
   - Ports Monero: 18080(P2P), 18081(Public), 18083(ZMQ)
<b><span foreground='#FF6600'>2)</span> Installation de Monero CLI</b>
   - Téléchargement et vérification GPG
   - Configuration des permissions
<b><span foreground='#FF6600'>3)</span> Installation et configuration de TOR</b>
   - Création des services cachés
   - Adresse .onion pour Monero RPC et SSH
<b><span foreground='#FF6600'>4)</span> Configuration de bitmonero.conf</b>
   - Configuration du fichier de démarrage
   - Configuration des ports et chemins
<b><span foreground='#FF6600'>5)</span> Configuration DNS Anonyme</b>
   - Installation des DNS sécurisés (AdGuard)
<b><span foreground='#FF6600'>6)</span> Blockchain sur un DISQUE EXTERNE</b>
   - Sélection du dossier via explorateur de fichiers
   - Configuration de data-dir dans bitmonero.conf
<b><span foreground='#FF6600'>7)</span> Revenir sur disque INTERNE</b>
   - Démontage du DISQUE EXTERNE
<b><span foreground='#FF6600'>8)</span> Démarrage Blockchain et Blocage IP Bans</b>
<b><span foreground='#FF6600'>9)</span> Arrêt de la Blockchain</b>
<span foreground='#e8b849'>⚠️ Configurer votre router pour REDIRIGER le port 22 et 18080
  vers l'ADRESSE IP de votre PC</span>""",
        "notes_text": """- Pour arrêter la blockchain : utilisez le bouton ARRÊTER
- Vérification de l'adresse IP Tor disponible après installation
<b>Configuration réseau requise :</b>
<span foreground='#e8b849'>⚠️ REDIRIGER le port 22 et 18080 de votre Box internet
  vers l'IP de votre PC.</span>
- Installer MONERO GUI pour la gestion du wallet
  MONERO GUI se synchronisera sur ce noeud
  https://www.getmonero.org/downloads/
🙏 Dons MONERO(Xmr) : kerlann.xmr (cake wallet - Unstoppable wallet)
📧 Contact: easynode@kerlann.org
🔗 Code source: <a href="https://github.com/kerlannXmr/EasyMonerod/blob/main/gui/README.md">https://github.com/kerlannXmr/easymonerod/blob/main/gui/README.md</a>""",
        "privacy_matters": "🔒 LA VIE PRIVÉE COMPTE 🔒",
        "thank_you": "Merci d'avoir utilisé ce programme.",
        "description": "Programme d'aide informatique et de liberté.\nPermet d'installer un nœud MONERO sans aucune connaissance sur Linux.",
    },
    "EN": {
        "app_subtitle": "Easy Monero node installation",
        "language_title": "LANGUAGE SELECTION",
        "menu_title": "MAIN MENU",
        "guide": "HOW TO",
        "update_system": "Install dependencies",
        "install_monero": "Install Monero CLI",
        "install_tor": "Install configure Tor",
        "configure_bitmonero": "Configure bitmonero",
        "configure_dns": "Configure anonymous DNS",
        "blockchain_section": "BLOCKCHAIN",
        "start": "START",
        "stop": "STOP",
        "disk_section": "Disk Options",
        "external_disk": "Blockchain on EXTERNAL DISK",
        "internal_disk": "Unmount EXTERNAL DISK",
        "other_section": "OTHER OPTIONS",
        "change_lang": "Change language",
        "features": "FEATURES",
        "notes": "READ",
        "update_gui": "Update GUI",
        "exit": "EXIT",
        "complete": "Complete 220 Go",
        "pruned": "Pruned 90 Go",
        "with_ip_ban": "With IP blocking",
        "without_ip_ban": "Without IP blocking",
        "cancel": "Cancel",
        "confirm": "Confirm",
        "username_title": "USER CONFIGURATION",
        "detected_user": "Detected user:",
        "confirm_or_change": "Press Confirm or type another username:",
        "with_password": "WITH password (Recommended)",
        "without_password": "WITHOUT password (Local only)",
        "rpc_security": "RPC SECURITY",
        "enter_password": "RPC Password:",
        "confirm_password": "Confirm password:",
        "password_mismatch": "Passwords do not match",
        "password_too_short": "Password must be at least 6 characters",
        "running": "Done !",
        "completed": "Completed",
        "error": "Error",
        "blockchain_type": "Blockchain type:",
        "start_mode": "Start mode:",
        "select_disk": "Selected folder:",
        "enter_disk": "Folder path:",
        "browse_folder": "📂 Browse...",
        "select_folder_title": "Choose folder for the blockchain",
        "no_folder_selected": "No folder selected",
        "folder_configured": "✅ Folder configured successfully!",
        "folder_error_empty": "⚠️ Select a folder first",
        "folder_error_write": "⚠️ Insufficient permissions on this folder",
        "current_datadir": "Current blockchain location:",
        "stop_confirm": "Do you really want to stop the blockchain?",
        "yes": "Yes",
        "no": "No",
        "back": "Back",
        "guide_text": """<b>For a complete installation, follow these steps in order:</b>
<span foreground='#47a347'>  1️⃣ ➜ 2️⃣ ➜ 3️⃣ ➜ 4️⃣ ➜ 5️⃣</span>
<b>Then your choice:</b>
  ▶️ Internal disk: go directly to step 8️⃣
  ▶️ External disk: step 6️⃣ then 8️⃣
<b>OTHER:</b>
  ➡️ Step 8: Start the Node and introduce the exclusion of ⛔ listed IP bans
  ➡️ Step 7: Unmount the EXTERNAL DISK
  ➡️ Step 4: Also serves as DEBUG of the boot path
<span foreground='#47a347'><b>  Compatible with:</b>
  🟢 <b>Monero GUI</b> — Official wallet
  🟢 <b>Gupax</b> — Mining on P2Pool
  🟢 <b>RetoSwap</b> — Decentralized buying and trading
  🟢 <b>Other</b> — Software that requires a node with port 18081</span>
<span foreground='#e8b849'>⚠️ Important: REDIRECT port 22 and 18080 from your internet router
  to your local IP address of your PC</span>""",
        "features_text": """<b><span foreground='#FF6600'>1)</span> System update and package installation</b>
   - Firewall configuration with port opening
   - System ports: 22(SSH), 80(HTTP), 443(HTTPS), 9050(Tor)
   - Monero ports: 18080(P2P), 18081(Public), 18083(ZMQ)
<b><span foreground='#FF6600'>2)</span> Monero CLI Installation</b>
   - Download and GPG verification
   - Setting up permissions
<b><span foreground='#FF6600'>3)</span> TOR Installation and configuration</b>
   - Hidden services creation
   - .onion address for Monero RPC and SSH
<b><span foreground='#FF6600'>4)</span> bitmonero.conf configuration</b>
   - Configuring startup file
   - Setting up ports and paths
<b><span foreground='#FF6600'>5)</span> Anonymous DNS Configuration</b>
   - Installing secure DNS (AdGuard)
<b><span foreground='#FF6600'>6)</span> Blockchain on EXTERNAL DISK</b>
   - Folder selection via file browser
   - data-dir configuration in bitmonero.conf
<b><span foreground='#FF6600'>7)</span> Return to INTERNAL disk</b>
   - Unmounting EXTERNAL DISK
<b><span foreground='#FF6600'>8)</span> Start Blockchain and Block IP Bans</b>
<b><span foreground='#FF6600'>9)</span> Stop Blockchain</b>
<span foreground='#e8b849'>⚠️ Configure your router to REDIRECT port 22 and 18080
  to your PC's IP ADDRESS</span>""",
        "notes_text": """- To stop the blockchain: use the STOP button
- Tor IP address check available after installation
<b>Required network configuration:</b>
<span foreground='#e8b849'>⚠️ REDIRECT port 22 and 18080 from your internet router
  to your PC's IP address.</span>
- Install MONERO GUI for wallet management
  MONERO GUI will sync on this node
  https://www.getmonero.org/downloads/
🙏 MONERO(Xmr) donations: kerlann.xmr (cake wallet - Unstoppable Wallet)
📧 Contact: easynode@kerlann.org
🔗 Source code: <a href="https://github.com/kerlannXmr/EasyMonerod/blob/main/gui/README.md">https://github.com/kerlannXmr/easymonerod/blob/main/gui/README.md</a>""",
        "privacy_matters": "🔒 PRIVACY MATTERS 🔒",
        "thank_you": "Thank you for using this program.",
        "description": "Computer assistance and freedom program.\nHelps you install a MONERO node without any knowledge on Linux.",
    }
}
# ─────────────────────────────────────────────
# CSS PROPRIUM - Thema Monerokerlannxmr
# ─────────────────────────────────────────────
CSS = """
/* ═══════════════════════════════════════════
   EasyMonerod - Monero Dark Orange Theme
   ═══════════════════════════════════════════ */
/* Global window */
window, .main-window {
    background-color: #1a1a1a;
    color: #e0e0e0;
}
/* Header bar */
headerbar {
    background: linear-gradient(180deg, #2a2a2a 0%, #1e1e1e 100%);
    border-bottom: 2px solid #FF6600;
    box-shadow: 0 2px 8px rgba(255, 102, 0, 0.15);
}
headerbar title {
    color: #FF6600;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 2px;
}
/* Monero banner area */
.monero-banner {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d1800 50%, #1a1a1a 100%);
    border: 1px solid #FF660040;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
}
.monero-banner label {
    color: #FF6600;
    font-family: 'JetBrains Mono', 'Fira Code', 'Source Code Pro', monospace;
}
.banner-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #FF6600;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}
.banner-subtitle {
    font-size: 12px;
    color: #FF660099;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    letter-spacing: 3px;
    margin-top: 4px;
}
.xmr-price-label {
    color: #FF6600;
    font-size: 13px;
    font-weight: bold;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    background-color: #FF660020;
    border-radius: 6px;
    padding: 4px 10px;
    margin: 0 4px;
}
.cpu-temp-label {
    color: #e8b849;
    font-size: 13px;
    font-weight: bold;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    background-color: #e8b84920;
    border-radius: 6px;
    padding: 4px 10px;
    margin: 0 4px;
}
.cpu-temp-hot {
    color: #e85050;
    background-color: #e8505020;
}
.tor-indicator-label {
    font-size: 13px;
    font-weight: bold;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    border-radius: 6px;
    padding: 4px 10px;
    margin: 0 4px;
}
.tor-active {
    color: #47a347;
    background-color: #47a34720;
}
.tor-inactive {
    color: #e85050;
    background-color: #e8505020;
}
.tor-starting {
    color: #e8b849;
    background-color: #e8b84920;
}
.node-info-label {
    font-size: 13px;
    font-weight: bold;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    border-radius: 6px;
    padding: 4px 10px;
    margin: 0 4px;
}
.node-info-synced {
    color: #47a347;
    background-color: #47a34720;
}
.node-info-syncing {
    color: #e8b849;
    background-color: #e8b84920;
}
.node-info-offline {
    color: #666666;
    background-color: #66666615;
}
.news-label {
    color: #aaaaaa;
    font-size: 12px;
    font-style: italic;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    padding: 4px 10px;
    margin: 0 4px;
}
/* Sidebar / Navigation */
.sidebar {
    background-color: #141414;
    border-right: 1px solid #FF660030;
}
.sidebar-section-label {
    color: #FF6600;
    font-weight: 800;
    font-size: 11px;
    letter-spacing: 2px;
    padding: 12px 16px 4px 16px;
}
.sidebar-button {
    background: transparent;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 2px 8px;
    color: #d0d0d0;
    font-size: 13px;
    font-weight: 500;
    transition: all 200ms ease;
}
.sidebar-button:hover {
    background: #FF660018;
    color: #FF6600;
}
.sidebar-button:checked,
.sidebar-button.active {
    background: linear-gradient(90deg, #FF660025 0%, #FF660010 100%);
    color: #FF6600;
    border-left: 3px solid #FF6600;
    font-weight: 700;
}
/* Step number badges */
.step-badge {
    background: #FF6600;
    color: #1a1a1a;
    border-radius: 50%;
    min-width: 24px;
    min-height: 24px;
    font-size: 12px;
    font-weight: 800;
}
/* Main content area */
.content-area {
    background-color: #1a1a1a;
    padding: 24px;
}
.page-title {
    color: #FF6600;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
button.flat.page-title:hover {
    text-decoration: underline;
    color: #FFA500;
    background-color: rgba(255, 165, 0, 0.15);
    border-radius: 4px;
}
.page-subtitle {
    color: #999999;
    font-size: 13px;
    margin-bottom: 20px;
}
/* Cards */
.option-card {
    background: linear-gradient(135deg, #222222 0%, #1e1e1e 100%);
    border: 1px solid #333333;
    border-radius: 12px;
    padding: 20px;
    margin: 6px 0;
    transition: all 200ms ease;
}
.option-card:hover {
    border-color: #FF660060;
    background: linear-gradient(135deg, #282828 0%, #222222 100%);
    box-shadow: 0 4px 12px rgba(255, 102, 0, 0.1);
}
/* Action buttons */
.action-button {
    background: linear-gradient(135deg, #FF6600 0%, #CC5200 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(255, 102, 0, 0.3);
    transition: all 200ms ease;
}
.action-button:hover {
    background: linear-gradient(135deg, #FF7720 0%, #FF6600 100%);
    box-shadow: 0 6px 20px rgba(255, 102, 0, 0.4);
}
.action-button:active {
    background: linear-gradient(135deg, #CC5200 0%, #993D00 100%);
}
.danger-button {
    background: linear-gradient(135deg, #CC3333 0%, #AA2222 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
    font-weight: 700;
    font-size: 14px;
    box-shadow: 0 4px 12px rgba(204, 51, 51, 0.3);
}
.danger-button:hover {
    background: linear-gradient(135deg, #DD4444 0%, #CC3333 100%);
}
.secondary-button {
    background: #2a2a2a;
    color: #d0d0d0;
    border: 1px solid #444444;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
}
.secondary-button:hover {
    background: #333333;
    border-color: #FF660060;
    color: #FF6600;
}
/* Terminal output */
.terminal-view {
    background-color: #0d0d0d;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 8px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Source Code Pro', monospace;
    font-size: 12px;
}
/* VTE Terminal */
vte-terminal {
    padding: 8px;
}
/* Status indicators */
.status-running {
    color: #47a347;
    font-weight: 700;
}
.status-stopped {
    color: #CC3333;
    font-weight: 700;
}
.status-warning {
    color: #e8b849;
    font-weight: 700;
}
/* Radio buttons and checkboxes */
checkbutton, radiobutton {
    color: #d0d0d0;
}
checkbutton:checked, radiobutton:checked {
    color: #FF6600;
}
check, radio {
    background: #2a2a2a;
    border: 2px solid #555555;
    border-radius: 4px;
}
check:checked, radio:checked {
    background: #FF6600;
    border-color: #FF6600;
}
/* Entry fields */
entry {
    background: #222222;
    border: 1px solid #444444;
    border-radius: 6px;
    color: #e0e0e0;
    padding: 8px 12px;
    font-size: 14px;
    caret-color: #FF6600;
}
entry:focus {
    border-color: #FF6600;
    box-shadow: 0 0 0 2px rgba(255, 102, 0, 0.2);
}
/* Scrolled window */
scrolledwindow {
    background: transparent;
}
/* Info boxes */
.info-box {
    background: #FF660012;
    border: 1px solid #FF660030;
    border-radius: 8px;
    padding: 16px;
}
.warning-box {
    background: #e8b84912;
    border: 1px solid #e8b84930;
    border-radius: 8px;
    padding: 16px;
}
.success-box {
    background: #47a34712;
    border: 1px solid #47a34730;
    border-radius: 8px;
    padding: 16px;
}
/* Separator */
separator {
    background-color: #FF660020;
    min-height: 1px;
}
/* Language selector */
.lang-button {
    background: #222222;
    border: 2px solid #444444;
    border-radius: 12px;
    padding: 24px 48px;
    color: #d0d0d0;
    font-size: 18px;
    font-weight: 700;
    min-width: 200px;
    transition: all 200ms ease;
}
.lang-button:hover {
    border-color: #FF6600;
    background: #FF660015;
    color: #FF6600;
    box-shadow: 0 4px 16px rgba(255, 102, 0, 0.2);
}
/* Progress bar */
progressbar trough {
    background: #222222;
    border-radius: 4px;
    min-height: 8px;
}
progressbar progress {
    background: linear-gradient(90deg, #FF6600, #FF8833);
    border-radius: 4px;
}
/* Monero logo area */
.monero-logo-text {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 14px;
    font-weight: 700;
    color: #FF6600;
}
/* Dropdown */
dropdown {
    background: #222222;
    border: 1px solid #444444;
    border-radius: 6px;
    color: #e0e0e0;
    padding: 6px 12px;
}
dropdown:focus {
    border-color: #FF6600;
}
/* Tooltips */
tooltip {
    background: #2a2a2a;
    border: 1px solid #FF660040;
    border-radius: 6px;
    color: #e0e0e0;
}
/* Popover infobulle option 7 */
.info-popover > contents {
    background-color: #1a3a1a;
    border: 1px solid #4CAF50;
    border-radius: 8px;
    padding: 2px;
}
.info-popover-label {
    color: #a8e6a8;
    font-size: 12px;
}
/* Link buttons */
.link-label {
    color: #FF6600;
}
.link-label:hover {
    color: #FF8833;
}
/* Scrollbar */
scrollbar slider {
    background-color: #FF660050;
    border-radius: 4px;
    min-width: 8px;
}
scrollbar slider:hover {
    background-color: #FF660080;
}
/* Tab-like page indicators */
.step-indicator {
    color: #666666;
    font-size: 12px;
}
.step-indicator.completed {
    color: #47a347;
}
.step-indicator.current {
    color: #FF6600;
    font-weight: 700;
}
/* Flat pane styling */
.flat-pane {
    background-color: #1a1a1a;
}
/* ── Welcome / Splash page ── */
.welcome-page {
    background: linear-gradient(160deg, #1a1a1a 0%, #2d1800 50%, #1a1a1a 100%);
}
.welcome-col {
    background-color: #222020dd;
    border-radius: 14px;
    border: 1px solid #FF660035;
    padding: 28px 32px;
    margin: 8px;
}
.welcome-lang-tag {
    color: #FF6600;
    font-size: 11px;
    font-weight: 800;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    letter-spacing: 3px;
    margin-bottom: 10px;
}
.welcome-title {
    color: #FF6600;
    font-size: 19px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 4px;
}
.welcome-subtitle {
    color: #bbbbbb;
    font-size: 13px;
    font-style: italic;
    margin-bottom: 16px;
}
.welcome-section-title {
    color: #FF8833;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    margin-top: 14px;
    margin-bottom: 5px;
}
.welcome-body {
    color: #cccccc;
    font-size: 13px;
}
.welcome-point {
    color: #dddddd;
    font-size: 13px;
    margin: 2px 0;
}
.welcome-warning {
    color: #e8b849;
    font-size: 12px;
    font-style: italic;
    margin-top: 12px;
}
.welcome-continue-btn {
    background: linear-gradient(135deg, #FF6600 0%, #cc4400 100%);
    color: #ffffff;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 1px;
    border-radius: 10px;
    padding: 10px 48px;
    border: none;
    box-shadow: 0 3px 12px rgba(255,102,0,0.35);
}
.welcome-continue-btn:hover {
    background: linear-gradient(135deg, #ff8833 0%, #e05500 100%);
}
.welcome-col-sep {
    min-width: 1px;
    background-color: #FF660025;
    margin: 16px 4px;
}
.welcome-skip-check {
    color: #888888;
    font-size: 12px;
    margin-bottom: 6px;
}
.welcome-skip-check:checked {
    color: #FF6600;
}
"""
# ─────────────────────────────────────────────
# APPLICATIO PRINCIPALIS kerlannxmr
# ─────────────────────────────────────────────
class EasyMonerodApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.lang = "FR"
        self._pending_lang = None
        self.username = ""
        self.blockchain_type = "complete"
        self.blockchain_running = False
        self.connect("activate", self.on_activate)

    def t(self, key):
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["EN"]).get(key, key)

    def on_activate(self, app):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        try:
            self.username = os.environ.get("SUDO_USER", os.environ.get("USER", "")) or os.getlogin()
        except OSError:
            import pwd
            self.username = pwd.getpwuid(os.getuid()).pw_name
        self.win = Adw.ApplicationWindow(application=app)
        self.win.set_title("EasyMonerod")
        _w, _h = 1100, 750
        try:
            _display = Gdk.Display.get_default()
            if _display:
                _mons = _display.get_monitors()
                if _mons.get_n_items() > 0:
                    _geom = _mons.get_item(0).get_geometry()
                    _w = min(_w, _geom.width - 40)
                    _h = min(_h, _geom.height - 100)
        except Exception:
            pass
        self.win.set_default_size(_w, _h)
        self.win.add_css_class("main-window")
        self.app_page = Gtk.Box()
        self._build_app_ui()
        self.main_stack = Gtk.Stack()
        self.main_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.main_stack.set_transition_duration(80)
        self.main_stack.add_named(self.app_page, "app")
        self.main_stack.add_named(self._build_language_page(), "language")
        self.main_stack.add_named(self._build_welcome_page(), "welcome")
        prefs = self._load_prefs()
        saved_lang = prefs.get("lang")
        skip_welcome = prefs.get("skip_welcome", False)
        if skip_welcome and saved_lang:
            self.lang = saved_lang
            self._rebuild_lang_strings()
            self.main_stack.set_visible_child_name("app")
            GLib.timeout_add_seconds(2, self._start_header_timers)
            threading.Thread(target=self._check_monero_update, daemon=True).start()
        elif skip_welcome:
            self.main_stack.set_visible_child_name("language")
        elif saved_lang:
            self._pending_lang = saved_lang
            self.main_stack.set_visible_child_name("welcome")
        else:
            self._pending_lang = None
            self.main_stack.set_visible_child_name("welcome")
        self.win.set_content(self.main_stack)
        self.win.connect("close-request", self._on_window_close_request)
        self.win.present()

    # ═══════════════════════════════════════════
    # PREFERENCES (settings.json)
    # ═══════════════════════════════════════════
    def _load_prefs(self):
        try:
            if os.path.isfile(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_prefs(self, prefs):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, "w") as f:
                json.dump(prefs, f, indent=2)
        except Exception:
            pass

    # ═══════════════════════════════════════════
    # PAGINA SALUTATIONIS kerlannxmr
    # ═══════════════════════════════════════════
    def _build_welcome_page(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.add_css_class("welcome-page")
        page.set_vexpand(True)
        page.set_hexpand(True)
        page.append(self._spacer(20))
        banner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        banner_box.add_css_class("monero-banner")
        banner_box.set_halign(Gtk.Align.CENTER)
        for line in ["  *     *   ***   *   * ***** ****   ***  ",
                     "  **   **  *   *  **  * *     *   * *   * ",
                     "  * * * * *     * * * * ****  ****  *   * ",
                     "  *  *  * *     * *  ** *     * *   *   * ",
                     "  *     *  *   *  *   * *     *  *  *   * ",
                     "  *     *   ***   *   * ***** *   *  ***  "]:
            lbl = Gtk.Label(label=line)
            lbl.add_css_class("banner-title")
            banner_box.append(lbl)
        sep = Gtk.Label(label="═══════════ ▌EASYNODE▐ ═══════════")
        sep.add_css_class("banner-subtitle")
        banner_box.append(sep)
        page.append(banner_box)
        page.append(self._spacer(16))
        cols_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        cols_box.set_hexpand(True)
        cols_box.set_margin_start(24)
        cols_box.set_margin_end(24)
        cols_box.append(self._welcome_col_fr())
        sep_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sep_box.add_css_class("welcome-col-sep")
        sep_box.set_vexpand(True)
        cols_box.append(sep_box)
        cols_box.append(self._welcome_col_en())
        page.append(cols_box)
        page.append(self._spacer(20))
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        bottom_box.set_halign(Gtk.Align.CENTER)
        skip_check = Gtk.CheckButton(
            label="Ne plus afficher ce message  /  Don't show this again")
        skip_check.add_css_class("welcome-skip-check")
        bottom_box.append(skip_check)
        btn = Gtk.Button(label="▶  Continuer  /  Continue  ▶")
        btn.add_css_class("welcome-continue-btn")
        def on_continue(b):
            if skip_check.get_active():
                prefs = self._load_prefs()
                prefs["skip_welcome"] = True
                self._save_prefs(prefs)
            if self._pending_lang:
                self._select_language(self._pending_lang, remember=True)
            else:
                self.main_stack.set_visible_child_name("language")
        btn.connect("clicked", on_continue)
        bottom_box.append(btn)
        page.append(bottom_box)
        page.append(self._spacer(24))
        scroll.set_child(page)
        return scroll

    def _spacer(self, height):
        s = Gtk.Box()
        s.set_size_request(-1, height)
        return s

    def _welcome_col_fr(self):
        col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        col.add_css_class("welcome-col")
        col.set_hexpand(True)
        tag = Gtk.Label(label="🇫🇷  FRANÇAIS")
        tag.add_css_class("welcome-lang-tag")
        tag.set_xalign(0)
        col.append(tag)
        title = Gtk.Label(label="Qu'est-ce que Monero ?")
        title.add_css_class("welcome-title")
        title.set_xalign(0)
        col.append(title)
        subtitle = Gtk.Label(label="La cryptomonnaie privée par défaut")
        subtitle.add_css_class("welcome-subtitle")
        subtitle.set_xalign(0)
        col.append(subtitle)
        def section(text):
            l = Gtk.Label(label=text)
            l.add_css_class("welcome-section-title")
            l.set_xalign(0)
            col.append(l)
        def body(text):
            l = Gtk.Label(label=text)
            l.add_css_class("welcome-body")
            l.set_xalign(0)
            l.set_wrap(True)
            l.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
            col.append(l)
        def point(icon, text):
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            row.set_margin_top(2)
            ico = Gtk.Label(label=icon)
            txt = Gtk.Label(label=text)
            txt.add_css_class("welcome-point")
            txt.set_xalign(0)
            txt.set_wrap(True)
            row.append(ico)
            row.append(txt)
            col.append(row)
        section("◆ LA MONNAIE")
        body("Monero (XMR) est une cryptomonnaie open-source dont toutes "
             "les transactions sont privées et non traçables par défaut.")
        section("◆ POURQUOI UN NŒUD ?")
        point("🟢", "Vérifier vous-même la blockchain sans dépendre d'un tiers")
        point("🟢", "Contribuer à la décentralisation du réseau")
        point("🟢", "Accéder à Monero sans serveur externe ni intermédiaire")
        point("🟢", "Tor par défaut — routage anonyme intégré")
        point("🟢", "Certains nœuds publics sont compromis et collectent vos données — votre propre nœud élimine ce risque")
        point("🟢", "Protection active contre les spywares : EasyNode bloque par option les IP malveillantes connues")
        section("◆ CE QUE FAIT CE LOGICIEL")
        body("EasyMonerod installe et configure automatiquement monerod "
             "(le nœud officiel Monero) sur votre machine Linux.")
        warn1 = Gtk.Label(label="⚠️  Votre autorisation sudo sera nécessaire pour l'installation.")
        warn1.add_css_class("welcome-warning")
        warn1.set_xalign(0)
        col.append(warn1)
        warn2 = Gtk.Label(label="💡 Privilégiez un PC dédié — même ancien — pour faire tourner votre nœud en continu 24h/24.")
        warn2.add_css_class("welcome-warning")
        warn2.set_xalign(0)
        col.append(warn2)
        return col

    def _welcome_col_en(self):
        col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        col.add_css_class("welcome-col")
        col.set_hexpand(True)
        tag = Gtk.Label(label="🇬🇧  ENGLISH")
        tag.add_css_class("welcome-lang-tag")
        tag.set_xalign(0)
        col.append(tag)
        title = Gtk.Label(label="What is Monero?")
        title.add_css_class("welcome-title")
        title.set_xalign(0)
        col.append(title)
        subtitle = Gtk.Label(label="The privacy-first cryptocurrency")
        subtitle.add_css_class("welcome-subtitle")
        subtitle.set_xalign(0)
        col.append(subtitle)
        def section(text):
            l = Gtk.Label(label=text)
            l.add_css_class("welcome-section-title")
            l.set_xalign(0)
            col.append(l)
        def body(text):
            l = Gtk.Label(label=text)
            l.add_css_class("welcome-body")
            l.set_xalign(0)
            l.set_wrap(True)
            l.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
            col.append(l)
        def point(icon, text):
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            row.set_margin_top(2)
            ico = Gtk.Label(label=icon)
            txt = Gtk.Label(label=text)
            txt.add_css_class("welcome-point")
            txt.set_xalign(0)
            txt.set_wrap(True)
            row.append(ico)
            row.append(txt)
            col.append(row)
        section("◆ THE CURRENCY")
        body("Monero (XMR) is an open-source cryptocurrency where all "
             "transactions are private and untraceable by default.")
        section("◆ WHY RUN A NODE?")
        point("🟢", "Verify the blockchain yourself — no trusted third party")
        point("🟢", "Contribute to the decentralisation of the network")
        point("🟢", "Access Monero without relying on any external server")
        point("🟢", "Tor by defaut— built-in anonymous routing")
        point("🟢", "Some public nodes are compromised and log your activity — your own node eliminates that risk")
        point("🟢", "Active spyware protection: EasyNode automatically bans known malicious IPs by choice")
        section("◆ WHAT THIS SOFTWARE DOES")
        body("EasyMonerod automatically installs and configures monerod "
             "(the official Monero node) on your Linux machine.")
        warn1 = Gtk.Label(label="⚠️  Your sudo permission will be required for installation.")
        warn1.add_css_class("welcome-warning")
        warn1.set_xalign(0)
        col.append(warn1)
        warn2 = Gtk.Label(label="💡 Consider using a dedicated machine — even an old one — to keep your node running 24/7.")
        warn2.add_css_class("welcome-warning")
        warn2.set_xalign(0)
        col.append(warn2)
        return col

    # ═══════════════════════════════════════════
    # PAGINA SELECTIONIS LINGUAE kerlannxmr
    # ═══════════════════════════════════════════
    def _build_language_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.set_valign(Gtk.Align.CENTER)
        page.set_halign(Gtk.Align.CENTER)
        page.set_hexpand(True)
        page.set_vexpand(True)
        banner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        banner_box.add_css_class("monero-banner")
        banner_box.set_halign(Gtk.Align.CENTER)
        ascii_art = [
            "  *     *   ***   *   * ***** ****   ***  ",
            "  **   **  *   *  **  * *     *   * *   * ",
            "  * * * * *     * * * * ****  ****  *   * ",
            "  *  *  * *     * *  ** *     * *   *   * ",
            "  *     *  *   *  *   * *     *  *  *   * ",
            "  *     *   ***   *   * ***** *   *  ***  ",
        ]
        for line in ascii_art:
            lbl = Gtk.Label(label=line)
            lbl.add_css_class("banner-title")
            banner_box.append(lbl)
        sep_lbl = Gtk.Label(label="═══════════ ▌EASYNODE▐ ═══════════")
        sep_lbl.add_css_class("banner-subtitle")
        banner_box.append(sep_lbl)
        page.append(banner_box)
        page.append(Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0))
        title = Gtk.Label(label="LANGUAGE SELECTION / SÉLECTION DE LA LANGUE")
        title.add_css_class("page-title")
        title.set_margin_top(40)
        title.set_margin_bottom(30)
        page.append(title)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        btn_box.set_halign(Gtk.Align.CENTER)
        btn_fr = Gtk.Button(label="🇫🇷  Français")
        btn_fr.add_css_class("lang-button")
        btn_fr.connect("clicked", lambda b: self._select_language("FR", remember_check.get_active()))
        btn_box.append(btn_fr)
        btn_en = Gtk.Button(label="🇬🇧  English")
        btn_en.add_css_class("lang-button")
        btn_en.connect("clicked", lambda b: self._select_language("EN", remember_check.get_active()))
        btn_box.append(btn_en)
        page.append(btn_box)
        remember_check = Gtk.CheckButton(
            label="Mémoriser mon choix  /  Remember my choice")
        remember_check.add_css_class("welcome-skip-check")
        remember_check.set_halign(Gtk.Align.CENTER)
        remember_check.set_margin_top(16)
        prefs = self._load_prefs()
        if prefs.get("lang"):
            remember_check.set_active(True)
        page.append(remember_check)
        privacy = Gtk.Label(label="🔒 PRIVACY MATTERS 🔒")
        privacy.add_css_class("banner-subtitle")
        privacy.set_margin_top(24)
        page.append(privacy)
        return page

    def _select_language(self, lang, remember=False):
        self.lang = lang
        self._build_app_ui()
        self.main_stack.set_visible_child_name("app")
        prefs = self._load_prefs()
        if remember:
            prefs["lang"] = lang
        else:
            prefs.pop("lang", None)
        self._save_prefs(prefs)
        GLib.timeout_add_seconds(2, self._start_header_timers)
        threading.Thread(target=self._check_monero_update, daemon=True).start()

    # ═══════════════════════════════════════════
    # UI PRINCIPALIS APP (post selectionem linguae)
    # ═══════════════════════════════════════════
    def _rebuild_lang_strings(self):
        try:
            self.lang_btn.set_label(self.lang)
        except Exception:
            pass

    def _build_app_ui(self):
        child = self.app_page.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.app_page.remove(child)
            child = next_child
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        header = Adw.HeaderBar()
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title_box.set_halign(Gtk.Align.CENTER)
        gif_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "xxmr.gif"),
            "/opt/easymonerod-gui/icons/xxmr.gif",
        ]
        gif_loaded = False
        for gif_path in gif_paths:
            if os.path.isfile(gif_path):
                try:
                    from gi.repository import GdkPixbuf
                    anim = GdkPixbuf.PixbufAnimation.new_from_file(gif_path)
                    if not anim.is_static_image():
                        gif_image = Gtk.Image()
                        gif_image.set_from_file(gif_path)
                        gif_image.set_pixel_size(48)
                        title_box.append(gif_image)
                        gif_loaded = True
                    else:
                        gif_image = Gtk.Image()
                        gif_image.set_from_file(gif_path)
                        gif_image.set_pixel_size(32)
                        title_box.append(gif_image)
                        gif_loaded = True
                except Exception:
                    pass
                break
        if not gif_loaded:
            for logo_path in [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "logo2.png"),
                "/opt/easymonerod-gui/icons/logo2.png",
            ]:
                if os.path.isfile(logo_path):
                    try:
                        logo_img = Gtk.Image()
                        logo_img.set_from_file(logo_path)
                        logo_img.set_pixel_size(32)
                        title_box.append(logo_img)
                    except Exception:
                        pass
                    break
        title_btn = Gtk.Button(label="EASYMONEROD")
        title_btn.add_css_class("flat")
        title_btn.add_css_class("page-title")
        title_btn.set_cursor_from_name("pointer")
        title_btn.connect("clicked", lambda *_: subprocess.Popen(
            ["xdg-open", "https://github.com/kerlannXmr/EasyMonerod/blob/main/gui/README.md"]))
        title_box.append(title_btn)
        title_btn.set_has_tooltip(True)
        header.set_title_widget(title_box)
        self.lang_btn = Gtk.Button(label=self.lang)
        self.lang_btn.add_css_class("secondary-button")
        self.lang_btn.connect("clicked", self._on_change_language)
        header.pack_end(self.lang_btn)
        self.xmr_header_label = Gtk.Label(label="⬡ XMR ...")
        self.xmr_header_label.add_css_class("xmr-price-label")
        header.pack_end(self.xmr_header_label)
        self.cpu_temp_label = Gtk.Label(label="🌡️ --°C")
        self.cpu_temp_label.add_css_class("cpu-temp-label")
        header.pack_end(self.cpu_temp_label)
        self.tor_status_label = Gtk.Label(label="🧅 Tor ○")
        self.tor_status_label.add_css_class("tor-indicator-label")
        self.tor_status_label.add_css_class("tor-inactive")
        header.pack_end(self.tor_status_label)
        self.sync_label = Gtk.Label(label="⟳ --%")
        self.sync_label.add_css_class("node-info-label")
        self.sync_label.add_css_class("node-info-offline")
        self.sync_label.set_tooltip_text(
            "Synchronisation blockchain" if self.lang == "FR" else "Blockchain sync")
        header.pack_end(self.sync_label)
        self.peers_label = Gtk.Label(label="👥 --")
        self.peers_label.add_css_class("node-info-label")
        self.peers_label.add_css_class("node-info-offline")
        header.pack_end(self.peers_label)
        self.height_label = Gtk.Label(label="📦 --")
        self.height_label.add_css_class("node-info-label")
        self.height_label.add_css_class("node-info-offline")
        header.pack_end(self.height_label)
        self.update_btn = Gtk.Button()
        self.update_btn.set_label("⏳ " + ("Vérification..." if self.lang == "FR" else "Checking..."))
        self.update_btn.connect("clicked", self._on_update_clicked)
        header.pack_start(self.update_btn)
        self._latest_monero_version = None
        self.news_label = Gtk.Label(label="📰 Loading Monero news...")
        self.news_label.add_css_class("news-label")
        self.news_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.news_label.set_max_width_chars(90)
        self.news_label.set_hexpand(True)
        self.news_label.set_xalign(0)
        header.pack_start(self.news_label)
        self._news_index = 0
        self._news_items = []
        outer.append(header)
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_shrink_start_child(False)
        paned.set_shrink_end_child(False)
        paned.set_position(260)
        sidebar_scroll = Gtk.ScrolledWindow()
        sidebar_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scroll.add_css_class("sidebar")
        sidebar_scroll.set_size_request(260, -1)
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        sidebar.set_margin_top(8)
        mini_banner = Gtk.Label(label="⬡ EASYNODE")
        mini_banner.add_css_class("banner-subtitle")
        mini_banner.set_margin_bottom(12)
        mini_banner.set_margin_top(8)
        sidebar.append(mini_banner)
        sidebar.append(Gtk.Separator())
        self.sidebar_buttons = {}
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.content_stack.set_transition_duration(200)
        menu_sections = [
            (None, [
                ("guide", "📖", self.t("guide"), "0"),
            ]),
            (self.t("menu_title"), [
                ("update", "🔄", self.t("update_system"), "1"),
                ("monero", "⬡", self.t("install_monero"), "2"),
                ("tor", "🧅", self.t("install_tor"), "3"),
                ("bitmonero", "⚙️", self.t("configure_bitmonero"), "4"),
                ("dns", "🌐", self.t("configure_dns"), "5"),
            ]),
            (self.t("disk_section"), [
                ("ext_disk", "💾", self.t("external_disk"), "6"),
                ("int_disk", "🖥️", self.t("internal_disk"), "7"),
            ]),
            (self.t("blockchain_section"), [
                ("start", "▶️", self.t("start"), "8"),
                ("stop", "⏹️", self.t("stop"), "9"),
            ]),
            (self.t("other_section"), [
                ("features", "ℹ️", self.t("features"), "10"),
                ("notes", "📝", self.t("notes"), "11"),
                ("update_gui", "⬆️", self.t("update_gui"), "12"),
            ]),
        ]
        for section_label, items in menu_sections:
            if section_label:
                sec = Gtk.Label(label=section_label)
                sec.add_css_class("sidebar-section-label")
                sec.set_xalign(0)
                sidebar.append(sec)
            for page_id, icon, label, step_num in items:
                btn = Gtk.ToggleButton()
                btn_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                btn_content.set_margin_start(4)
                step_label = Gtk.Label(label=step_num)
                step_label.add_css_class("step-badge")
                step_label.set_size_request(24, 24)
                step_label.set_halign(Gtk.Align.CENTER)
                step_label.set_valign(Gtk.Align.CENTER)
                btn_content.append(step_label)
                icon_lbl = Gtk.Label(label=icon)
                btn_content.append(icon_lbl)
                text_lbl = Gtk.Label(label=label)
                text_lbl.set_xalign(0)
                text_lbl.set_hexpand(True)
                text_lbl.set_ellipsize(Pango.EllipsizeMode.END)
                btn_content.append(text_lbl)
                btn.set_child(btn_content)
                btn.add_css_class("sidebar-button")
                btn.connect("toggled", self._on_sidebar_click, page_id)
                tooltips = {
                    "update": (
                        "ℹ️ À faire uniquement à la 1ère utilisation",
                        "ℹ️ Do this only on first use"
                    ),
                    "int_disk": (
                        "✅ À faire après avoir arrêté la blockchain (option 9)\n\n"
                        "Démonte le disque externe et nettoie le fstab\n"
                        "pour que le disque puisse se remonter normalement\n"
                        "sur n'importe quel PC sans redémarrage.",
                        "✅ Do this after stopping the blockchain (option 9)\n\n"
                        "Unmounts the EXTERNAL DISK and cleans fstab\n"
                        "so the disk can be auto-mounted normally\n"
                        "on any PC without rebooting."
                    ),
                }
                if page_id in tooltips:
                    tip_fr, tip_en = tooltips[page_id]
                    tip_text = tip_fr if self.lang == "FR" else tip_en
                    popover = Gtk.Popover()
                    popover.set_autohide(False)
                    popover.set_position(Gtk.PositionType.RIGHT)
                    popover.add_css_class("info-popover")
                    tip_label = Gtk.Label(label=tip_text)
                    tip_label.add_css_class("info-popover-label")
                    tip_label.set_margin_top(8)
                    tip_label.set_margin_bottom(8)
                    tip_label.set_margin_start(10)
                    tip_label.set_margin_end(10)
                    tip_label.set_xalign(0)
                    popover.set_child(tip_label)
                    popover.set_parent(btn)
                    motion = Gtk.EventControllerMotion()
                    motion.connect("enter", lambda *_, p=popover: p.popup())
                    motion.connect("leave", lambda *_, p=popover: p.popdown())
                    btn.add_controller(motion)
                sidebar.append(btn)
                self.sidebar_buttons[page_id] = btn
        eco_btn = Gtk.Button(label="Xmr.Ecosystem")
        eco_btn.add_css_class("sidebar-button")
        eco_btn.set_margin_start(8)
        eco_btn.set_margin_end(8)
        eco_btn.set_margin_top(6)
        eco_btn.connect("clicked", lambda *_: subprocess.Popen(
            ["xdg-open", "https://easynode.kerlann.org/ecosystem.html"]))
        sidebar.append(eco_btn)
        gui_btn = Gtk.Button(label="EasyMonerod_Gui")
        gui_btn.add_css_class("sidebar-button")
        gui_btn.set_margin_start(8)
        gui_btn.set_margin_end(8)
        gui_btn.set_margin_top(2)
        gui_btn.connect("clicked", lambda *_: subprocess.Popen(
            ["xdg-open", "https://github.com/kerlannXmr/EasyMonerod/blob/main/gui/README.md"]))
        sidebar.append(gui_btn)
        sidebar.append(Gtk.Box(vexpand=True))
        sep = Gtk.Separator()
        sidebar.append(sep)
        exit_btn = Gtk.Button(label="⏻  " + self.t("exit"))
        exit_btn.add_css_class("sidebar-button")
        exit_btn.set_margin_bottom(12)
        exit_btn.set_margin_start(8)
        exit_btn.set_margin_end(8)
        exit_btn.connect("clicked", self._on_exit)
        sidebar.append(exit_btn)
        sidebar_scroll.set_child(sidebar)
        paned.set_start_child(sidebar_scroll)
        content_scroll = Gtk.ScrolledWindow()
        content_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        content_scroll.add_css_class("content-area")
        self.content_stack.add_named(self._build_guide_page(), "guide")
        self.content_stack.add_named(self._build_terminal_page("update", self.t("update_system"),
            "Step 1: System update, firewall, SSH, fail2ban...",
            info_markup=(
                "<b>Cette étape va :</b>\n"
                "  • Mettre à jour le système (apt update &amp;&amp; upgrade)\n"
                "  • Installer les outils essentiels (curl, wget, git...)\n"
                "  • Configurer le firewall (UFW) avec les ports Monero\n"
                "  • Installer et configurer fail2ban et SSH"
            ) if self.lang == "FR" else (
                "<b>This step will:</b>\n"
                "  • Update the system (apt update &amp;&amp; upgrade)\n"
                "  • Install essential tools (curl, wget, git...)\n"
                "  • Configure firewall (UFW) with Monero ports\n"
                "  • Install and configure fail2ban and SSH"
            )), "update")
        self.content_stack.add_named(self._build_install_monero_page(), "monero")
        self.content_stack.add_named(self._build_terminal_page("tor", self.t("install_tor"),
            "Step 3: Tor hidden services setup",
            info_markup=(
                "<b>Cette étape va :</b>\n"
                "  • Installer et configurer le service Tor\n"
                "  • Créer un service caché (.onion) pour le nœud Monero\n"
                "  • Créer un service caché (.onion) pour SSH\n"
                "  • Anonymiser les connexions du nœud"
            ) if self.lang == "FR" else (
                "<b>This step will:</b>\n"
                "  • Install and configure the Tor service\n"
                "  • Create a hidden service (.onion) for the Monero node\n"
                "  • Create a hidden service (.onion) for SSH\n"
                "  • Anonymize node connections"
            )), "tor")
        self.content_stack.add_named(self._build_configure_bitmonero_page(), "bitmonero")
        self.content_stack.add_named(self._build_terminal_page("dns", self.t("configure_dns"),
            "Step 5: Anonymous DNS (AdGuard)",
            info_markup=(
                "<b>Cette étape va :</b>\n"
                "  • Remplacer les DNS par défaut par AdGuard DNS\n"
                "  • Protéger votre vie privée (pas de logs, filtrage publicités)\n"
                "  • Un backup de resolv.conf est créé automatiquement"
            ) if self.lang == "FR" else (
                "<b>This step will:</b>\n"
                "  • Replace default DNS with AdGuard DNS\n"
                "  • Protect your privacy (no logs, ad filtering)\n"
                "  • A backup of resolv.conf is created automatically"
            )), "dns")
        self.content_stack.add_named(self._build_start_page(), "start")
        self.content_stack.add_named(self._build_stop_page(), "stop")
        self.content_stack.add_named(self._build_external_disk_page(), "ext_disk")
        self.content_stack.add_named(self._build_terminal_page("int_disk", self.t("internal_disk"),
            "Step 7: Unmount EXTERNAL DISK, clean fstab, revert to internal",
            info_markup=(
                "<b>Cette étape va :</b>\n"
                "  • Démonter le disque externe proprement\n"
                "  • Nettoyer les entrées fstab ajoutées par EasyMonerod\n"
                "  • Remettre la blockchain sur le disque interne\n"
                "  • Libérer le disque externe (montage auto rétabli)"
            ) if self.lang == "FR" else (
                "<b>This step will:</b>\n"
                "  • Cleanly unmount the external disk\n"
                "  • Clean fstab entries added by EasyMonerod\n"
                "  • Switch blockchain back to internal disk\n"
                "  • Release the external disk (auto-mount restored)"
            )), "int_disk")
        self.content_stack.add_named(self._build_info_page("features"), "features")
        self.content_stack.add_named(self._build_info_page("notes"), "notes")
        self.content_stack.add_named(self._build_update_gui_page(), "update_gui")
        content_scroll.set_child(self.content_stack)
        paned.set_end_child(content_scroll)
        outer.append(paned)
        self.app_page.append(outer)
        outer.set_vexpand(True)
        self._activate_sidebar("guide")

    def _on_sidebar_click(self, button, page_id):
        if button.get_active():
            for pid, btn in self.sidebar_buttons.items():
                if pid != page_id:
                    btn.set_active(False)
            self.content_stack.set_visible_child_name(page_id)
            if page_id == "features":
                threading.Thread(target=self._load_network_info, daemon=True).start()
            # ── AJOUT kerlann: rafraîchir le chemin quand on ouvre la page ext_disk ──
            if page_id == "ext_disk":
                self._refresh_datadir_label()

    def _activate_sidebar(self, page_id):
        for pid, btn in self.sidebar_buttons.items():
            btn.set_active(pid == page_id)
        self.content_stack.set_visible_child_name(page_id)

    # ═══════════════════════════════════════════
    # CONSTRUCTORES PAGINARUM
    # ═══════════════════════════════════════════
    def _create_terminal(self, height=300):
        if VTE_AVAILABLE:
            terminal = Vte.Terminal()
            terminal.set_size_request(-1, height)
            terminal.add_css_class("terminal-view")
            bg_color = Gdk.RGBA()
            bg_color.parse("rgba(13,13,13,1.0)")
            terminal.set_color_background(bg_color)
            fg_color = Gdk.RGBA()
            fg_color.parse("rgba(242,242,242,1.0)")
            terminal.set_color_foreground(fg_color)
            terminal.set_font(Pango.FontDescription("Monospace 11"))
            terminal.set_scroll_on_output(True)
            terminal.set_scrollback_lines(10000)
            terminal.set_vexpand(False)
            return terminal
        else:
            textview = Gtk.TextView()
            textview.set_editable(False)
            textview.set_cursor_visible(False)
            textview.set_monospace(True)
            textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            textview.set_size_request(-1, height)
            textview.set_vexpand(False)
            textview.add_css_class("terminal-view")
            return textview

    def _make_page_header(self, title, subtitle=""):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.set_margin_bottom(20)
        title_lbl = Gtk.Label(label=title)
        title_lbl.add_css_class("page-title")
        title_lbl.set_xalign(0)
        box.append(title_lbl)
        if subtitle:
            sub_lbl = Gtk.Label(label=subtitle)
            sub_lbl.add_css_class("page-subtitle")
            sub_lbl.set_xalign(0)
            box.append(sub_lbl)
        box.append(Gtk.Separator())
        return box

    def _build_guide_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.append(self._make_page_header("📖 " + self.t("guide")))
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        info_box.add_css_class("info-box")
        guide_label = Gtk.Label()
        guide_label.set_markup(self.t("guide_text"))
        guide_label.set_xalign(0)
        guide_label.set_wrap(True)
        guide_label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        info_box.append(guide_label)
        page.append(info_box)
        step_map = {"1": "update", "2": "monero", "3": "tor", "4": "bitmonero",
                    "5": "dns", "6": "ext_disk", "7": "int_disk",
                    "8": "start",  "9": "stop"}
        def make_step_row(label_fr, label_en, steps_list, suffix_fr="", suffix_en=""):
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            row.set_margin_top(16)
            title_lbl = Gtk.Label()
            title_lbl.set_markup(f"<b><span foreground='#FF8833'>"
                                 f"{' ' + label_fr if self.lang == 'FR' else ' ' + label_en}"
                                 f"</span></b>")
            title_lbl.set_xalign(0)
            row.append(title_lbl)
            flow = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            flow.set_halign(Gtk.Align.START)
            for s in steps_list:
                if s == "➜":
                    arr = Gtk.Label(label="➜")
                    arr.set_opacity(0.5)
                    flow.append(arr)
                elif s == "puis" or s == "then":
                    sep = Gtk.Label(label=("puis" if self.lang == "FR" else "then"))
                    sep.set_markup("<i><span foreground='#aaaaaa'>"
                                  + ("puis" if self.lang == "FR" else "then")
                                  + "</span></i>")
                    sep.set_margin_start(6)
                    sep.set_margin_end(6)
                    flow.append(sep)
                else:
                    btn = Gtk.Button(label=s)
                    btn.add_css_class("step-badge")
                    btn.set_size_request(40, 40)
                    if s in step_map:
                        btn.connect("clicked", lambda b, pid=step_map[s]:
                                    self._activate_sidebar(pid))
                    flow.append(btn)
            if suffix_fr:
                suf = Gtk.Label()
                suf.set_markup("<span foreground='#aaaaaa'><i>"
                               + (suffix_fr if self.lang == "FR" else suffix_en)
                               + "</i></span>")
                suf.set_margin_start(8)
                flow.append(suf)
            row.append(flow)
            return row
        def section_title(txt_fr, txt_en, color="#FF6600"):
            lbl = Gtk.Label()
            lbl.set_markup(f"<b><span foreground='{color}' size='large'>"
                           + (txt_fr if self.lang == "FR" else txt_en)
                           + "</span></b>")
            lbl.set_xalign(0)
            lbl.set_margin_top(20)
            lbl.set_margin_bottom(4)
            return lbl
        flows_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        flows_box.set_margin_top(8)
        flows_box.append(section_title(
            "⚡ 1er démarrage :",
            "⚡ First start :",
            color="#A0522D"
        ))
        flows_box.append(make_step_row(
            "Disque INTERNE", "INTERNAL disk",
            ["1", "➜", "2", "➜", "3", "➜", "4", "➜", "5", "➜", "8"],
            suffix_fr="→ puis 9 pour arrêter",
            suffix_en="→ then 9 to stop"
        ))
        flows_box.append(make_step_row(
            "Disque EXTERNE", "EXTERNAL disk",
            ["1", "➜", "2", "➜", "3", "➜", "4", "➜", "5", "➜", "6", "➜", "8"],
            suffix_fr="→ puis 9 pour arrêter, 7 pour démonter",
            suffix_en="→ then 9 to stop, 7 to unmount"
        ))
        flows_box.append(section_title(
            "🔄 Démarrage journalier :",
            "🔄 Daily start :",
            color="#47a347"
        ))
        flows_box.append(make_step_row(
            "Disque INTERNE", "INTERNAL disk",
            ["4", "➜", "8"],
            suffix_fr="→ puis 9 pour arrêter",
            suffix_en="→ then 9 to stop"
        ))
        flows_box.append(make_step_row(
            "Disque EXTERNE", "EXTERNAL disk",
            ["6", "➜", "8"],
            suffix_fr="→ puis 9 pour arrêter, 7 pour démonter",
            suffix_en="→ then 9 to stop, 7 to unmount"
        ))
        page.append(flows_box)
        return page

    def _build_terminal_page(self, page_id, title, description, info_markup=None):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.append(self._make_page_header(title, description))
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        user_box.set_margin_bottom(8)
        user_lbl = Gtk.Label(label=self.t("detected_user"))
        user_lbl.set_xalign(0)
        user_box.append(user_lbl)
        user_entry = Gtk.Entry()
        user_entry.set_text(self.username)
        user_entry.set_hexpand(True)
        user_entry.connect("changed", lambda e: setattr(self, 'username', e.get_text()))
        user_box.append(user_entry)
        page.append(user_box)
        if info_markup:
            info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            info.add_css_class("info-box")
            info_lbl = Gtk.Label()
            info_lbl.set_markup(info_markup)
            info_lbl.set_xalign(0)
            info_lbl.set_wrap(True)
            info.append(info_lbl)
            page.append(info)
        terminal = self._create_terminal(250)
        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(False)
        term_scroll.set_size_request(-1, 350)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)
        status_label = Gtk.Label(label="")
        status_label.set_hexpand(True)
        status_label.set_xalign(0)
        btn_box.append(status_label)
        run_btn = Gtk.Button(label="▶  " + self.t("confirm"))
        run_btn.add_css_class("action-button")
        run_btn.connect("clicked", lambda b: self._run_script_step(page_id, terminal, status_label, run_btn))
        btn_box.append(run_btn)
        page.append(btn_box)
        return page

    def _build_install_monero_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.append(self._make_page_header(
            "⬡ " + self.t("install_monero"),
            f"Monero v{MONERO_VERSION} - " + (
                "Téléchargement, vérification GPG, installation"
                if self.lang == "FR" else
                "Download, GPG verify, install"
            )
        ))
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        user_box.set_margin_bottom(8)
        user_lbl = Gtk.Label(label=self.t("detected_user"))
        user_box.append(user_lbl)
        user_entry = Gtk.Entry()
        user_entry.set_text(self.username)
        user_entry.set_hexpand(True)
        user_entry.connect("changed", lambda e: setattr(self, 'username', e.get_text()))
        user_box.append(user_entry)
        page.append(user_box)
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.add_css_class("info-box")
        info_lbl = Gtk.Label()
        info_lbl.set_markup(
            "<b>Cette étape va :</b>\n"
            "  • Télécharger Monero CLI depuis getmonero.org\n"
            "  • Vérifier le hash SHA256 + signature GPG\n"
            "  • Installer dans ~/monero/\n"
            "  • Configurer le PATH et les permissions"
            if self.lang == "FR" else
            "<b>This step will:</b>\n"
            "  • Download Monero CLI from getmonero.org\n"
            "  • Verify SHA256 hash + GPG signature\n"
            "  • Install to ~/monero/\n"
            "  • Configure PATH and permissions"
        )
        info_lbl.set_xalign(0)
        info_lbl.set_wrap(True)
        info.append(info_lbl)
        page.append(info)
        terminal = self._create_terminal(250)
        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(False)
        term_scroll.set_size_request(-1, 350)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)
        status_label = Gtk.Label(label="")
        status_label.set_hexpand(True)
        status_label.set_xalign(0)
        btn_box.append(status_label)
        run_btn = Gtk.Button(label="▶  " + self.t("confirm"))
        run_btn.add_css_class("action-button")
        run_btn.connect("clicked", lambda b: self._run_script_step("monero", terminal, status_label, run_btn))
        btn_box.append(run_btn)
        page.append(btn_box)
        return page

    def _build_configure_bitmonero_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.append(self._make_page_header(
            "⚙️ " + self.t("configure_bitmonero"),
            self.t("rpc_security")
        ))
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        user_box.set_margin_bottom(12)
        user_lbl = Gtk.Label(label=self.t("detected_user"))
        user_box.append(user_lbl)
        user_entry = Gtk.Entry()
        user_entry.set_text(self.username)
        user_entry.set_hexpand(True)
        user_entry.connect("changed", lambda e: setattr(self, 'username', e.get_text()))
        user_box.append(user_entry)
        page.append(user_box)
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.add_css_class("info-box")
        info_lbl = Gtk.Label()
        info_lbl.set_markup(
            "<b>Cette étape va :</b>\n"
            "  • Configurer bitmonero.conf (ports, chemins)\n"
            "  • Définir les options RPC et sécurité\n"
            "  • Configurer les ports P2P, RPC et ZMQ\n"
            "  • Sauvegarder les identifiants RPC"
            if self.lang == "FR" else
            "<b>This step will:</b>\n"
            "  • Configure bitmonero.conf (ports, paths)\n"
            "  • Set RPC options and security\n"
            "  • Configure P2P, RPC and ZMQ ports\n"
            "  • Save RPC credentials"
        )
        info_lbl.set_xalign(0)
        info_lbl.set_wrap(True)
        info.append(info_lbl)
        page.append(info)
        security_group = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        opt1_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        opt1_card.add_css_class("option-card")
        self.rpc_radio_pass = Gtk.CheckButton(label="🔐 " + self.t("with_password"))
        self.rpc_radio_pass.set_active(True)
        opt1_card.append(self.rpc_radio_pass)
        pass_desc = Gtk.Label()
        if self.lang == "FR":
            pass_desc.set_markup("<small>Nécessite une connexion en mode distant dans Monero GUI d'abord\nPuis vous pourrez revenir en mode local après connexion</small>")
        else:
            pass_desc.set_markup("<small>Requires remote connection in Monero GUI first\nThen you can switch back to local mode after connection</small>")
        pass_desc.set_xalign(0)
        pass_desc.set_margin_start(28)
        pass_desc.set_opacity(0.6)
        opt1_card.append(pass_desc)
        self.pass_fields_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.pass_fields_box.set_margin_start(28)
        self.pass_fields_box.set_margin_top(8)
        pass_entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        pass_lbl = Gtk.Label(label=self.t("enter_password"))
        pass_lbl.set_size_request(180, -1)
        pass_lbl.set_xalign(0)
        pass_entry_box.append(pass_lbl)
        self.rpc_password_entry = Gtk.Entry()
        self.rpc_password_entry.set_visibility(False)
        self.rpc_password_entry.set_hexpand(True)
        self.rpc_password_entry.set_placeholder_text("Min. 6 characters")
        pass_entry_box.append(self.rpc_password_entry)
        self.pass_fields_box.append(pass_entry_box)
        conf_entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        conf_lbl = Gtk.Label(label=self.t("confirm_password"))
        conf_lbl.set_size_request(180, -1)
        conf_lbl.set_xalign(0)
        conf_entry_box.append(conf_lbl)
        self.rpc_password_confirm = Gtk.Entry()
        self.rpc_password_confirm.set_visibility(False)
        self.rpc_password_confirm.set_hexpand(True)
        conf_entry_box.append(self.rpc_password_confirm)
        self.pass_fields_box.append(conf_entry_box)
        opt1_card.append(self.pass_fields_box)
        security_group.append(opt1_card)
        opt2_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        opt2_card.add_css_class("option-card")
        self.rpc_radio_nopass = Gtk.CheckButton(label="🔓 " + self.t("without_password"))
        self.rpc_radio_nopass.set_group(self.rpc_radio_pass)
        opt2_card.append(self.rpc_radio_nopass)
        nopass_desc = Gtk.Label()
        if self.lang == "FR":
            nopass_desc.set_markup("<small>Connexion directe possible mais moins sécurisé\nRecommandé uniquement pour usage personnel local</small>")
        else:
            nopass_desc.set_markup("<small>Direct connection possible but less secure\nRecommended only for personal local use</small>")
        nopass_desc.set_xalign(0)
        nopass_desc.set_margin_start(28)
        nopass_desc.set_opacity(0.6)
        opt2_card.append(nopass_desc)
        security_group.append(opt2_card)
        page.append(security_group)
        self.rpc_radio_pass.connect("toggled", lambda b: self.pass_fields_box.set_visible(b.get_active()))
        self.rpc_radio_nopass.connect("toggled", lambda b: self.pass_fields_box.set_visible(not b.get_active()))
        terminal = self._create_terminal(250)
        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(False)
        term_scroll.set_size_request(-1, 220)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)
        self.bitmonero_error_label = Gtk.Label(label="")
        self.bitmonero_error_label.add_css_class("status-warning")
        self.bitmonero_error_label.set_xalign(0)
        page.append(self.bitmonero_error_label)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(8)
        status_label = Gtk.Label(label="")
        status_label.set_hexpand(True)
        status_label.set_xalign(0)
        btn_box.append(status_label)
        run_btn = Gtk.Button(label="▶  " + self.t("confirm"))
        run_btn.add_css_class("action-button")
        run_btn.connect("clicked", lambda b: self._run_configure_bitmonero(terminal, status_label, run_btn))
        btn_box.append(run_btn)
        page.append(btn_box)
        return page

    def _build_start_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.append(self._make_page_header("▶️ " + self.t("start")))
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        user_box.set_margin_bottom(8)
        user_lbl = Gtk.Label(label=self.t("detected_user"))
        user_box.append(user_lbl)
        user_entry = Gtk.Entry()
        user_entry.set_text(self.username)
        user_entry.set_hexpand(True)
        user_entry.connect("changed", lambda e: setattr(self, 'username', e.get_text()))
        user_box.append(user_entry)
        page.append(user_box)
        options_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        bc_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        bc_card.add_css_class("option-card")
        bc_card.set_hexpand(True)
        bc_title = Gtk.Label(label=self.t("blockchain_type"))
        bc_title.set_xalign(0)
        bc_title.add_css_class("page-subtitle")
        bc_card.append(bc_title)
        self.bc_radio_complete = Gtk.CheckButton(label="📦 " + self.t("complete"))
        self.bc_radio_complete.set_active(True)
        bc_card.append(self.bc_radio_complete)
        self.bc_radio_pruned = Gtk.CheckButton(label="✂️ " + self.t("pruned"))
        self.bc_radio_pruned.set_group(self.bc_radio_complete)
        bc_card.append(self.bc_radio_pruned)
        options_box.append(bc_card)
        mode_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        mode_card.add_css_class("option-card")
        mode_card.set_hexpand(True)
        mode_title = Gtk.Label(label=self.t("start_mode"))
        mode_title.set_xalign(0)
        mode_title.add_css_class("page-subtitle")
        mode_card.append(mode_title)
        self.start_radio_ban = Gtk.CheckButton(label="🛡️ " + self.t("with_ip_ban"))
        self.start_radio_ban.set_active(True)
        mode_card.append(self.start_radio_ban)
        self.start_radio_noban = Gtk.CheckButton(label="⚡ " + self.t("without_ip_ban"))
        self.start_radio_noban.set_group(self.start_radio_ban)
        mode_card.append(self.start_radio_noban)
        options_box.append(mode_card)
        page.append(options_box)
        self.start_terminal = self._create_terminal(250)
        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(self.start_terminal)
        term_scroll.set_vexpand(False)
        term_scroll.set_size_request(-1, 350)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)
        sync_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        sync_box.set_margin_top(8)
        self._sync_progress_label = Gtk.Label(label="")
        self._sync_progress_label.set_xalign(0)
        sync_box.append(self._sync_progress_label)
        self._sync_progress_bar = Gtk.ProgressBar()
        self._sync_progress_bar.set_show_text(True)
        self._sync_progress_bar.set_fraction(0.0)
        self._sync_progress_bar.set_text("—")
        sync_box.append(self._sync_progress_bar)
        page.append(sync_box)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)
        status_label = Gtk.Label(label="")
        status_label.set_hexpand(True)
        status_label.set_xalign(0)
        btn_box.append(status_label)
        run_btn = Gtk.Button(label="▶  " + self.t("start"))
        run_btn.add_css_class("action-button")
        run_btn.connect("clicked", lambda b: self._run_start_blockchain(self.start_terminal, status_label, run_btn))
        btn_box.append(run_btn)
        page.append(btn_box)
        return page

    def _build_stop_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.append(self._make_page_header("⏹️ " + self.t("stop")))
        warning_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        warning_box.add_css_class("warning-box")
        warn_lbl = Gtk.Label(label=self.t("stop_confirm"))
        warn_lbl.set_xalign(0)
        warning_box.append(warn_lbl)
        page.append(warning_box)
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.add_css_class("info-box")
        info_lbl = Gtk.Label()
        info_lbl.set_markup(
            "💾 <b>Si la blockchain est sur un disque externe :</b>\n"
            "  • Arrêtez d'abord la blockchain ici\n"
            "  • Puis allez à l'<b>option 7</b> pour démonter le disque\n"
            "  • Cela évite la corruption des données et libère le disque"
            if self.lang == "FR" else
            "💾 <b>If the blockchain is on an external disk:</b>\n"
            "  • Stop the blockchain here first\n"
            "  • Then go to <b>option 7</b> to unmount the disk\n"
            "  • This prevents data corruption and releases the disk"
        )
        info_lbl.set_xalign(0)
        info_lbl.set_wrap(True)
        info.append(info_lbl)
        page.append(info)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.CENTER)
        btn_box.set_margin_top(24)
        status_label = Gtk.Label(label="")
        status_label.set_hexpand(True)
        status_label.set_xalign(0)
        btn_box.append(status_label)
        stop_btn = Gtk.Button(label="⏹  " + self.t("stop"))
        stop_btn.add_css_class("danger-button")
        stop_btn.connect("clicked", lambda b: self._run_stop_blockchain(status_label, b))
        btn_box.append(stop_btn)
        page.append(btn_box)
        return page

    # ── AJOUT kerlann: méthode pour lire le data-dir actuel depuis bitmonero.conf ──
    def _get_current_datadir(self):
        """Lit le data-dir actuel depuis bitmonero.conf"""
        config_path = f"/home/{self.username}/.bitmonero/bitmonero.conf"
        default_path = f"/home/{self.username}/.bitmonero"
        try:
            if os.path.isfile(config_path):
                with open(config_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("data-dir="):
                            return line.split("=", 1)[1]
            return default_path
        except Exception:
            return default_path

    # ── AJOUT kerlann: méthode pour rafraîchir le label du chemin blockchain ──
    def _refresh_datadir_label(self):
        """Rafraîchit le label du chemin blockchain depuis bitmonero.conf"""
        if hasattr(self, 'datadir_display_label'):
            self.datadir_display_label.set_markup(
                f"<span foreground='#00FF00'><b>{self._get_current_datadir()}</b></span>"
            )
        return False  # Ne pas répéter le timer

    def _build_external_disk_page(self):
        """Gradus 6: Blockchain in disco externo - cum auto indicatione discorum"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.append(self._make_page_header("💾 " + self.t("external_disk")))
        # Username
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        user_box.set_margin_bottom(8)
        user_lbl = Gtk.Label(label=self.t("detected_user"))
        user_box.append(user_lbl)
        user_entry = Gtk.Entry()
        user_entry.set_text(self.username)
        user_entry.set_hexpand(True)
        user_entry.connect("changed", lambda e: setattr(self, 'username', e.get_text()))
        user_box.append(user_entry)
        page.append(user_box)
        # Carta informationis
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.add_css_class("info-box")
        info_lbl = Gtk.Label()
        info_lbl.set_markup(
            "<b>Cette étape va :</b>\n"
            "  • Détecter et monter le disque externe choisi\n"
            "  • Configurer la blockchain sur ce disque\n"
            "  • Ajouter le montage automatique dans fstab\n"
            "  • ⚠️ Après utilisation, démontez via l'option 7"
            if self.lang == "FR" else
            "<b>This step will:</b>\n"
            "  • Detect and mount the selected external disk\n"
            "  • Configure the blockchain on this disk\n"
            "  • Add automatic mount to fstab\n"
            "  • ⚠️ After use, unmount via option 7"
        )
        info_lbl.set_xalign(0)
        info_lbl.set_wrap(True)
        info.append(info_lbl)
        page.append(info)

        # ── AJOUT kerlann: Affichage dynamique du chemin actuel de la blockchain ──
        datadir_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        datadir_card.add_css_class("option-card")

        datadir_title = Gtk.Label()
        datadir_title.set_markup(
            "<b><span foreground='#FF8833'>📂 "
            + self.t("current_datadir")
            + "</span></b>"
        )
        datadir_title.set_xalign(0)
        datadir_card.append(datadir_title)

        self.datadir_display_label = Gtk.Label()
        self.datadir_display_label.set_markup(
            f"<span foreground='#00FF00'><b>{self._get_current_datadir()}</b></span>"
        )
        self.datadir_display_label.set_xalign(0)
        self.datadir_display_label.set_margin_start(16)
        self.datadir_display_label.set_margin_top(4)
        self.datadir_display_label.set_selectable(True)
        datadir_card.append(self.datadir_display_label)

        page.append(datadir_card)
        # ── FIN AJOUT kerlann ──

        # ── Disk list card ──
        disk_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        disk_card.add_css_class("option-card")
        disk_title = Gtk.Label(label=self.t("select_disk"))
        disk_title.set_xalign(0)
        disk_title.add_css_class("page-subtitle")
        disk_card.append(disk_title)
        self.disk_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        disk_scroll = Gtk.ScrolledWindow()
        disk_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        disk_scroll.set_child(self.disk_list_box)
        disk_scroll.set_min_content_height(120)
        disk_scroll.set_max_content_height(200)
        disk_card.append(disk_scroll)
        refresh_btn = Gtk.Button(label="🔄 " + ("Rafraîchir la liste" if self.lang == "FR" else "Refresh disk list"))
        refresh_btn.add_css_class("secondary-button")
        refresh_btn.set_margin_top(8)
        refresh_btn.connect("clicked", lambda b: self._refresh_disk_list())
        disk_card.append(refresh_btn)
        manual_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        manual_box.set_margin_top(8)
        manual_lbl = Gtk.Label(label=self.t("enter_disk"))
        manual_lbl.set_xalign(0)
        manual_box.append(manual_lbl)
        self.disk_entry = Gtk.Entry()
        self.disk_entry.set_placeholder_text("sdb1")
        self.disk_entry.set_hexpand(True)
        manual_box.append(self.disk_entry)
        disk_card.append(manual_box)
        page.append(disk_card)
        # ═══ OU : Parcourir un dossier ═══
        browse_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        browse_card.add_css_class("option-card")
        browse_title = Gtk.Label()
        browse_title.set_markup(
            "<b>📂 " + ("Ou parcourir un dossier..." if self.lang == "FR"
                         else "Or browse a folder...") + "</b>")
        browse_title.set_xalign(0)
        browse_card.append(browse_title)
        browse_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self._browse_path_entry = Gtk.Entry()
        self._browse_path_entry.set_placeholder_text(
            "/media/user/disque" if self.lang == "FR" else "/media/user/disk")
        self._browse_path_entry.set_hexpand(True)
        browse_row.append(self._browse_path_entry)
        browse_btn = Gtk.Button(label=self.t("browse_folder"))
        browse_btn.add_css_class("secondary-button")
        browse_btn.connect("clicked", self._on_browse_folder)
        browse_row.append(browse_btn)
        browse_card.append(browse_row)
        self._browse_info_label = Gtk.Label(label="")
        self._browse_info_label.set_xalign(0)
        self._browse_info_label.set_wrap(True)
        self._browse_info_label.set_margin_top(4)
        browse_card.append(self._browse_info_label)
        page.append(browse_card)
        # Terminalis
        terminal = self._create_terminal(250)
        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(False)
        term_scroll.set_size_request(-1, 320)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)
        status_label = Gtk.Label(label="")
        status_label.set_hexpand(True)
        status_label.set_xalign(0)
        btn_box.append(status_label)
        run_btn = Gtk.Button(label="▶  " + self.t("confirm"))
        run_btn.add_css_class("action-button")
        run_btn.connect("clicked", lambda b: self._run_script_step("ext_disk", terminal, status_label, run_btn))
        btn_box.append(run_btn)
        page.append(btn_box)
        self._disk_radio_group = None
        GLib.idle_add(self._refresh_disk_list)
        return page

    def _refresh_disk_list(self):
        child = self.disk_list_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.disk_list_box.remove(child)
            child = next_child
        self._disk_radio_group = None
        try:
            result = subprocess.run(
                ["lsblk", "-nrpo", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,MODEL"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")
            found_disks = []
            for line in lines:
                parts = line.split()
                if len(parts) < 3:
                    continue
                name = parts[0]
                size = parts[1]
                dtype = parts[2]
                fstype = parts[3] if len(parts) > 3 else ""
                mount = parts[4] if len(parts) > 4 else ""
                model = " ".join(parts[5:]) if len(parts) > 5 else ""
                if dtype != "part":
                    continue
                if mount in ["/", "/boot", "/boot/efi", "/home", "[SWAP]"]:
                    continue
                if fstype in ["", "swap"]:
                    continue
                short_name = name.replace("/dev/", "")
                info = f"{short_name}  —  {size}"
                if fstype:
                    info += f"  [{fstype}]"
                if mount:
                    info += f"  (monté: {mount})" if self.lang == "FR" else f"  (mounted: {mount})"
                elif self.lang == "FR":
                    info += "  (non monté)"
                else:
                    info += "  (not mounted)"
                if model:
                    info += f"  ({model})"
                found_disks.append((short_name, info))
            if not found_disks:
                no_disk_lbl = Gtk.Label(
                    label="⚠️ " + ("Aucun disque externe détecté" if self.lang == "FR"
                                    else "No external disk detected"))
                no_disk_lbl.set_xalign(0)
                no_disk_lbl.add_css_class("status-warning")
                self.disk_list_box.append(no_disk_lbl)
            else:
                for short_name, info in found_disks:
                    radio = Gtk.CheckButton(label=f"  💾 {info}")
                    if self._disk_radio_group is None:
                        self._disk_radio_group = radio
                    else:
                        radio.set_group(self._disk_radio_group)
                    radio.connect("toggled", lambda r, sn=short_name:
                                  self.disk_entry.set_text(sn) if r.get_active() else None)
                    self.disk_list_box.append(radio)
        except Exception as e:
            err_lbl = Gtk.Label(label=f"⚠️ Error: {e}")
            err_lbl.set_xalign(0)
            err_lbl.add_css_class("status-warning")
            self.disk_list_box.append(err_lbl)
        return False

    def _on_browse_folder(self, button):
        try:
            dialog = Gtk.FileDialog()
            dialog.set_title(self.t("select_folder_title"))
            initial_path = f"/media/{self.username}"
            if not os.path.isdir(initial_path):
                initial_path = os.path.expanduser("~")
            dialog.set_initial_folder(Gio.File.new_for_path(initial_path))
            dialog.select_folder(self.win, None, self._on_folder_selected)
        except AttributeError:
            self._open_folder_chooser_legacy()

    def _open_folder_chooser_legacy(self):
        dialog = Gtk.FileChooserNative(
            title=self.t("select_folder_title"),
            transient_for=self.win,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            accept_label=self.t("confirm"),
            cancel_label=self.t("cancel"),
        )
        initial_path = f"/media/{self.username}"
        if not os.path.isdir(initial_path):
            initial_path = os.path.expanduser("~")
        dialog.set_current_folder(Gio.File.new_for_path(initial_path))
        dialog.connect("response", self._on_folder_chooser_legacy_response)
        dialog.show()

    def _on_folder_chooser_legacy_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            folder = dialog.get_file()
            if folder:
                self._process_browse_path(folder.get_path())
        dialog.destroy()

    def _on_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                self._process_browse_path(folder.get_path())
        except GLib.Error:
            pass

    def _process_browse_path(self, path):
        """Detectio partitionis e via selecta et renovatio disk_entry"""
        self._browse_path_entry.set_text(path)
        try:
            result = subprocess.run(
                ["df", path], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                device = lines[1].split()[0]
                short = device.replace("/dev/", "")
                self.disk_entry.set_text(short)
                stat = os.statvfs(path)
                free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
                total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
                writable = os.access(path, os.W_OK)
                info = f"💾 {free_gb:.1f} Go / {total_gb:.1f} Go"
                info += "  ✅" if writable else "  ❌"
                info += f"  →  {short}"
                self._browse_info_label.set_text(info)
        except Exception:
            self._browse_info_label.set_text("")

        # ── AJOUT kerlann: actualiser immédiatement le chemin affiché ──
        if hasattr(self, 'datadir_display_label'):
            self.datadir_display_label.set_markup(
                f"<span foreground='#00FF00'><b>{path}</b></span>"
            )

    def _build_info_page(self, page_type):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        if page_type == "features":
            page.append(self._make_page_header("ℹ️ " + self.t("features")))
            text_key = "features_text"
        else:
            page.append(self._make_page_header("📝 " + self.t("notes")))
            text_key = "notes_text"
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        info_box.add_css_class("info-box")
        info_label = Gtk.Label()
        info_label.set_markup(self.t(text_key))
        info_label.set_xalign(0)
        info_label.set_wrap(True)
        info_label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        info_label.set_selectable(True)
        info_box.append(info_label)
        page.append(info_box)
        if page_type == "features":
            net_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            net_card.add_css_class("option-card")
            net_card.set_margin_top(12)
            net_title = Gtk.Label()
            net_title.set_markup("<b><span foreground='#FF6600'>🧅 " +
                ("Informations réseau / Tor" if self.lang == "FR" else "Network / Tor info") +
                "</span></b>")
            net_title.set_xalign(0)
            net_card.append(net_title)
            self.tor_info_label = Gtk.Label()
            self.tor_info_label.set_xalign(0)
            self.tor_info_label.set_wrap(True)
            self.tor_info_label.set_selectable(True)
            self.tor_info_label.set_markup("<i>" +
                ("Chargement des informations..." if self.lang == "FR" else "Loading info...") +
                "</i>")
            net_card.append(self.tor_info_label)
            refresh_btn = Gtk.Button(label="🔄 " +
                ("Rafraîchir" if self.lang == "FR" else "Refresh"))
            refresh_btn.add_css_class("secondary-button")
            refresh_btn.set_margin_top(8)
            refresh_btn.connect("clicked", lambda b: threading.Thread(target=self._load_network_info, daemon=True).start())
            net_card.append(refresh_btn)
            page.append(net_card)
        if page_type == "notes":
            qr_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            qr_box.add_css_class("option-card")
            qr_box.set_margin_top(12)
            qr_box.set_halign(Gtk.Align.CENTER)
            qr_title = Gtk.Label()
            if self.lang == "FR":
                qr_title.set_markup("<b><span foreground='#FF6600'>🙏 Dons Monero (XMR)</span></b>")
            else:
                qr_title.set_markup("<b><span foreground='#FF6600'>🙏 Monero (XMR) Donations</span></b>")
            qr_box.append(qr_title)
            qr_paths = [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "qrcode1.png"),
                "/opt/easymonerod-gui/icons/qrcode1.png",
            ]
            for qr_path in qr_paths:
                if os.path.isfile(qr_path):
                    try:
                        qr_image = Gtk.Image()
                        qr_image.set_from_file(qr_path)
                        qr_image.set_pixel_size(150)
                        qr_image.set_margin_top(8)
                        qr_image.set_margin_bottom(8)
                        qr_box.append(qr_image)
                    except Exception:
                        pass
                    break
            qr_addr = Gtk.Label()
            qr_addr.set_markup("<span foreground='#47a347'><b>kerlann.xmr</b></span>  (Cake Wallet - Unstoppable Wallet)")
            qr_addr.set_selectable(True)
            qr_box.append(qr_addr)
            xmr_addr = Gtk.Label()
            xmr_addr.set_markup(
                "<span foreground='#e8b849'>"
                "85oN3YjxpsbER5fEnDusRr4Gj6jxBaTSSSRZeMDP6Mb1D5qB8m5oR9y5VhAcxE5RXKADMKk7ttQ4yScXwbaSMeqH7vp5AVZ"
                "</span>")
            xmr_addr.set_selectable(True)
            xmr_addr.set_wrap(True)
            xmr_addr.set_margin_top(4)
            qr_box.append(xmr_addr)
            page.append(qr_box)
            links_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            links_box.set_margin_top(16)
            privacy_lbl = Gtk.Label(label=self.t("privacy_matters"))
            privacy_lbl.add_css_class("page-title")
            privacy_lbl.set_margin_top(20)
            links_box.append(privacy_lbl)
            page.append(links_box)
        return page

    def _build_update_gui_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)
        page.append(self._make_page_header(
            "⬆️ " + self.t("update_gui"),
            f"EasyMonerod GUI v{APP_VERSION}" if self.lang == "EN" else f"EasyMonerod GUI v{APP_VERSION}"
        ))
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.add_css_class("info-box")
        info_lbl = Gtk.Label()
        info_lbl.set_markup(
            "<b>Cette mise à jour va :</b>\n"
            "  • Télécharger la dernière version de <b>easymonerod_gui.py</b>\n"
            "  • Télécharger la dernière version de <b>easynode_linux.sh</b>\n"
            "  • Redémarrer le GUI automatiquement"
            if self.lang == "FR" else
            "<b>This update will:</b>\n"
            "  • Download the latest version of <b>easymonerod_gui.py</b>\n"
            "  • Download the latest version of <b>easynode_linux.sh</b>\n"
            "  • Restart the GUI automatically"
        )
        info_lbl.set_xalign(0)
        info_lbl.set_wrap(True)
        info.append(info_lbl)
        page.append(info)
        version_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        version_card.add_css_class("option-card")
        version_card.set_margin_top(8)
        self._update_local_lbl = Gtk.Label()
        self._update_local_lbl.set_markup(
            f"<b>{'Version installée' if self.lang == 'FR' else 'Installed version'} :</b>  v{APP_VERSION}"
        )
        self._update_local_lbl.set_xalign(0)
        version_card.append(self._update_local_lbl)
        self._update_remote_lbl = Gtk.Label()
        self._update_remote_lbl.set_markup(
            "<b>" + ("Dernière version" if self.lang == "FR" else "Latest version") + " :</b>  " +
            ("<i>cliquez sur Vérifier</i>" if self.lang == "FR" else "<i>click Check</i>")
        )
        self._update_remote_lbl.set_xalign(0)
        version_card.append(self._update_remote_lbl)
        self._update_status_lbl = Gtk.Label(label="")
        self._update_status_lbl.set_xalign(0)
        self._update_status_lbl.set_margin_top(4)
        version_card.append(self._update_status_lbl)
        page.append(version_card)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_margin_top(16)
        btn_box.set_halign(Gtk.Align.CENTER)
        self._check_btn = Gtk.Button(label="🔍  " + ("Vérifier" if self.lang == "FR" else "Check"))
        self._check_btn.add_css_class("secondary-button")
        self._check_btn.connect("clicked", self._on_check_update)
        btn_box.append(self._check_btn)
        self._update_btn = Gtk.Button(label="⬆️  " + ("Mettre à jour" if self.lang == "FR" else "Update"))
        self._update_btn.add_css_class("action-button")
        self._update_btn.set_sensitive(False)
        self._update_btn.connect("clicked", self._on_run_update)
        btn_box.append(self._update_btn)
        page.append(btn_box)
        self._restart_btn = Gtk.Button(label="🔄  " + ("Redémarrer le GUI" if self.lang == "FR" else "Restart GUI"))
        self._restart_btn.add_css_class("action-button")
        self._restart_btn.set_halign(Gtk.Align.CENTER)
        self._restart_btn.set_margin_top(8)
        self._restart_btn.set_visible(False)
        self._restart_btn.connect("clicked", lambda b: self._restart_gui())
        page.append(self._restart_btn)
        self._update_terminal = self._create_terminal(250)
        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(self._update_terminal)
        term_scroll.set_vexpand(True)
        term_scroll.set_size_request(-1, 350)
        term_scroll.add_css_class("terminal-view")
        term_scroll.set_margin_top(16)
        page.append(term_scroll)
        return page

    def _on_check_update(self, btn):
        btn.set_sensitive(False)
        self._update_status_lbl.set_markup(
            "<i>" + ("Vérification en cours..." if self.lang == "FR" else "Checking...") + "</i>"
        )
        self._update_remote_lbl.set_markup(
            "<b>" + ("Dernière version" if self.lang == "FR" else "Latest version") + " :</b>  <i>...</i>"
        )
        def check():
            try:
                result = subprocess.run(
                    ["wget", "-q", "--user-agent=Mozilla/5.0", "-O", "-",
                     "https://raw.githubusercontent.com/kerlannXmr/EasyMonerod/main/gui/VERSION"],
                    capture_output=True, text=True, timeout=10
                )
                remote_version = result.stdout.strip()
                if not remote_version:
                    result = subprocess.run(
                        ["curl", "-sL",
                         "https://raw.githubusercontent.com/kerlannXmr/EasyMonerod/main/gui/VERSION"],
                        capture_output=True, text=True, timeout=10
                    )
                    remote_version = result.stdout.strip()
            except Exception:
                remote_version = ""
            GLib.idle_add(self._update_check_result, remote_version)
        threading.Thread(target=check, daemon=True).start()

    def _update_check_result(self, remote_version):
        self._check_btn.set_sensitive(True)
        if not remote_version:
            self._update_remote_lbl.set_markup(
                "<b>" + ("Dernière version" if self.lang == "FR" else "Latest version") + " :</b>  " +
                "<span foreground='#e8b849'>⚠️ " +
                ("GitHub inaccessible" if self.lang == "FR" else "GitHub unreachable") + "</span>"
            )
            self._update_status_lbl.set_markup(
                "<span foreground='#e8b849'>" +
                ("Impossible de vérifier. Vérifiez votre connexion." if self.lang == "FR"
                 else "Cannot check. Verify your connection.") + "</span>"
            )
            self._update_btn.set_sensitive(False)
            return
        self._update_remote_lbl.set_markup(
            f"<b>{'Dernière version' if self.lang == 'FR' else 'Latest version'} :</b>  v{remote_version}"
        )
        if remote_version == APP_VERSION:
            self._update_status_lbl.set_markup(
                "<span foreground='#47a347'>✅ " +
                ("Vous avez la dernière version !" if self.lang == "FR"
                 else "You have the latest version!") + "</span>"
            )
            self._update_btn.set_sensitive(False)
        else:
            self._update_status_lbl.set_markup(
                "<span foreground='#FF6600'>🆕 " +
                (f"Nouvelle version disponible : v{remote_version}" if self.lang == "FR"
                 else f"New version available: v{remote_version}") + "</span>"
            )
            self._update_btn.set_sensitive(True)

    def _on_run_update(self, btn):
        btn.set_sensitive(False)
        self._check_btn.set_sensitive(False)
        self._update_status_lbl.set_markup(
            "<i>" + ("Mise à jour en cours..." if self.lang == "FR"
                     else "Update in progress...") + "</i>"
        )
        def run():
            try:
                import tempfile
                tmp = tempfile.mktemp(suffix=".sh")
                result = subprocess.run(
                    ["wget", "-q", "--user-agent=Mozilla/5.0", "-O", tmp,
                     "https://raw.githubusercontent.com/kerlannXmr/EasyMonerod/main/gui/install.sh"],
                    timeout=30
                )
                if result.returncode != 0 or not os.path.getsize(tmp):
                    raise Exception("Download failed")
                os.chmod(tmp, 0o755)
                GLib.idle_add(self._run_update_in_terminal, tmp)
            except Exception as e:
                GLib.idle_add(self._update_status_lbl.set_markup,
                    f"<span foreground='#e8b849'>⚠️ Erreur : {e}</span>")
                GLib.idle_add(btn.set_sensitive, True)
                GLib.idle_add(self._check_btn.set_sensitive, True)
        threading.Thread(target=run, daemon=True).start()

    def _run_update_in_terminal(self, tmp_script):
        if not VTE_AVAILABLE or self._update_terminal is None:
            subprocess.run(["pkexec", "bash", tmp_script])
            self._update_status_lbl.set_markup(
                "<span foreground='#47a347'>✅ " +
                ("Renovatio completa!" if self.lang == "FR" else "Update complete!") +
                "</span>")
            self._restart_btn.set_visible(True)
            return
        cmd = ["pkexec", "bash", tmp_script]
        self._update_terminal.spawn_async(
            Vte.PtyFlags.DEFAULT, None, cmd, None,
            GLib.SpawnFlags.DO_NOT_REAP_CHILD, None, None, -1, None,
            self._on_update_terminal_ready, tmp_script
        )

    def _on_update_terminal_ready(self, terminal, pid, error, *args):
        tmp_script = args[0] if args else None
        if error:
            GLib.idle_add(self._update_status_lbl.set_markup,
                "<span foreground='#e8b849'>⚠️ Erreur terminal</span>")
            return
        def wait_and_show_btn():
            import time
            try:
                os.waitpid(pid, 0)
            except Exception:
                time.sleep(5)
            try:
                os.unlink(tmp_script)
            except Exception:
                pass
            GLib.idle_add(self._update_status_lbl.set_markup,
                "<span foreground='#47a347'>✅ " +
                ("Renovatio completa!" if self.lang == "FR" else "Update complete!") +
                "</span>")
            GLib.idle_add(self._restart_btn.set_visible, True)
        threading.Thread(target=wait_and_show_btn, daemon=True).start()

    def _restart_gui(self):
        python = sys.executable
        os.execv(python, [python] + sys.argv)

    def _load_network_info(self):
        info_parts = []
        def read_onion(service_paths, saved_file):
            checks = " || ".join([f'cat "{p}" 2>/dev/null' for p in service_paths])
            try:
                result = subprocess.run(
                    ["pkexec", "bash", "-c", checks],
                    capture_output=True, text=True, timeout=10
                )
                addr = result.stdout.strip().split("\n")[0].strip()
                if addr and ".onion" in addr:
                    return addr
            except Exception:
                pass
            for user_dir in [f"/home/{self.username}", os.path.expanduser("~")]:
                fpath = os.path.join(user_dir, saved_file)
                try:
                    if os.path.isfile(fpath):
                        with open(fpath, "r") as f:
                            for line in f:
                                line = line.strip()
                                if ".onion" in line:
                                    parts = line.split(":")
                                    for part in parts:
                                        part = part.strip()
                                        if ".onion" in part:
                                            return part
                except Exception:
                    continue
            return None
        monero_onion = read_onion(
            ["/var/lib/tor/monero-service/hostname",
             "/var/lib/tor/monero/hostname",
             "/var/lib/tor/hidden_service/hostname"],
            "monero_onion_address.txt"
        )
        if monero_onion:
            info_parts.append(f"<b>🧅 Monero RPC .onion:</b>")
            info_parts.append(f"  <span foreground='#47a347'>{monero_onion}</span>")
            info_parts.append(f"  Port: <b>18081</b>")
        ssh_onion = read_onion(
            ["/var/lib/tor/ssh/hostname",
             "/var/lib/tor/sshd/hostname"],
            "ssh_onion_address.txt"
        )
        if ssh_onion:
            info_parts.append(f"\n<b>🧅 SSH .onion:</b>")
            info_parts.append(f"  <span foreground='#47a347'>{ssh_onion}</span>")
            info_parts.append(f"  Port: <b>22</b>")
        if not monero_onion and not ssh_onion:
            if self.lang == "FR":
                info_parts.append("<i>⚠️ Adresses .onion non trouvées.\nInstallez Tor (étape 3) d'abord.</i>")
            else:
                info_parts.append("<i>⚠️ .onion addresses not found.\nInstall Tor (step 3) first.</i>")
        try:
            ip_result = subprocess.run(
                ["hostname", "-I"],
                capture_output=True, text=True, timeout=5
            )
            if ip_result.returncode == 0 and ip_result.stdout.strip():
                local_ip = ip_result.stdout.strip().split()[0]
                info_parts.append(f"\n<b>🖥️ IP locale:</b> <span foreground='#e8b849'>{local_ip}</span>")
        except Exception:
            pass
        info_parts.append(f"\n<b>📡 Ports:</b>")
        info_parts.append(f"  P2P: <b>18080</b>  |  RPC: <b>18081</b>  |  ZMQ: <b>18083</b>")
        info_parts.append(f"  SSH: <b>22</b>  |  Tor SOCKS: <b>9050</b>")
        try:
            tor_status = subprocess.run(
                ["systemctl", "is-active", "tor"],
                capture_output=True, text=True, timeout=5
            )
            status = tor_status.stdout.strip()
            if status == "active":
                info_parts.append(f"\n<b>Tor:</b> <span foreground='#47a347'>✓ Actif</span>")
                try:
                    tor_ip_result = subprocess.run(
                        ["torsocks", "curl", "-s", "https://check.torproject.org/api/ip"],
                        capture_output=True, text=True, timeout=15
                    )
                    if tor_ip_result.returncode == 0 and tor_ip_result.stdout.strip():
                        tor_ip_raw = tor_ip_result.stdout.strip()
                        try:
                            tor_ip_data = json.loads(tor_ip_raw)
                            tor_ip = tor_ip_data.get("IP", tor_ip_raw)
                        except (json.JSONDecodeError, ValueError):
                            tor_ip = tor_ip_raw
                        info_parts.append(f"<b>🌐 Tor IP:</b> <span foreground='#47a347'>{tor_ip}</span>")
                    else:
                        if self.lang == "FR":
                            info_parts.append("<i>  ⚠️ Impossible de récupérer l'adresse IP Tor</i>")
                        else:
                            info_parts.append("<i>  ⚠️ Unable to retrieve Tor IP address</i>")
                except FileNotFoundError:
                    if self.lang == "FR":
                        info_parts.append("<i>  ⚠️ torsocks non installé</i>")
                    else:
                        info_parts.append("<i>  ⚠️ torsocks not installed</i>")
                except subprocess.TimeoutExpired:
                    if self.lang == "FR":
                        info_parts.append("<i>  ⚠️ Délai dépassé pour la récupération de l'IP Tor</i>")
                    else:
                        info_parts.append("<i>  ⚠️ Timeout retrieving Tor IP</i>")
            else:
                info_parts.append(f"\n<b>Tor:</b> <span foreground='#CC3333'>✖ Inactif ({status})</span>")
        except Exception:
            pass
        markup = "\n".join(info_parts)
        GLib.idle_add(self.tor_info_label.set_markup, markup)
        return False

    # ═══════════════════════════════════════════
    # EXECUTIO MANDATORUM
    # ═══════════════════════════════════════════
    def _run_in_terminal(self, terminal, cmd):
        if VTE_AVAILABLE and isinstance(terminal, Vte.Terminal):
            old_pid = getattr(terminal, '_child_pid', None)
            if old_pid:
                try:
                    os.kill(old_pid, 9)
                except (ProcessLookupError, PermissionError):
                    pass
                terminal._child_pid = None
            terminal.reset(True, True)
            def on_spawn_complete(terminal_ref, pid, error, *args):
                if pid and pid > 0:
                    terminal_ref._child_pid = pid
            try:
                env = os.environ.copy()
                env["TERM"] = "xterm-256color"
                env["COLORTERM"] = "truecolor"
                envv = [f"{k}={v}" for k, v in env.items()]
                terminal.spawn_async(
                    Vte.PtyFlags.DEFAULT,
                    os.path.expanduser("~"),
                    cmd,
                    envv,
                    GLib.SpawnFlags.DEFAULT,
                    None, None,
                    -1,
                    None,
                    on_spawn_complete,
                )
            except Exception as e:
                print(f"Error generationis terminalis: {e}")
        else:
            text_buffer = terminal.get_buffer()
            text_buffer.set_text("$ " + " ".join(cmd) + "\n\n")
            def run_and_capture():
                try:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1
                    )
                    for line in iter(process.stdout.readline, ''):
                        GLib.idle_add(self._append_to_textview, text_buffer, line)
                    process.wait()
                    GLib.idle_add(self._append_to_textview, text_buffer,
                                  f"\n--- Finished (exit code: {process.returncode}) ---\n")
                except Exception as e:
                    GLib.idle_add(self._append_to_textview, text_buffer, f"\nError: {e}\n")
            thread = threading.Thread(target=run_and_capture, daemon=True)
            thread.start()

    def _append_to_textview(self, text_buffer, text):
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert(end_iter, text)
        return False

    def _source_preamble(self):
        script = SCRIPT_PATH
        return (
            f'eval "$(head -n -4 "{script}")"; '
            f'setup_terminal() {{ true; }}; '
            f'select_language() {{ true; }}; '
            f'show_menu() {{ true; }}; '
            f'draw_banner() {{ true; }}; '
            f'real_wget=$(which wget); '
            f'wget() {{ $real_wget --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "$@"; }}; '
            f'export -f wget; '
            f'read() {{ '
            f'  local args=("$@"); '
            f'  local prompt=""; '
            f'  for ((i=0; i<${{#args[@]}}; i++)); do '
            f'    if [[ "${{args[$i]}}" == "-p" ]]; then prompt="${{args[$((i+1))]}}"; fi; '
            f'  done; '
            f'  if [[ "$prompt" == *"Entrée"* ]] || [[ "$prompt" == *"Enter"* ]] || [[ "$prompt" == *"continuer"* ]] || [[ "$prompt" == *"continue"* ]] || [[ "$prompt" == *"menu"* ]]; then '
            f'    echo ""; return 0; '
            f'  fi; '
            f'  builtin read "$@"; '
            f'}}; '
            f'LANG_CHOICE="{self.lang}"; '
            f'USERNAME="{self.username}"; '
            f'MONERO_VERSION="0.18.4.6"; '
            f'ask_username() {{ USERNAME="{self.username}"; return 0; }}; '
        )

    def _build_step_command(self, step_id):
        preamble = self._source_preamble()
        step_functions = {
            "update":   "update_system",
            "monero":   "install_monero_cli",
            "tor":      "install_tor",
            "dns":      "configure_dns",
        }
        func = step_functions.get(step_id)
        if func:
            cmd_str = f'{preamble} {func}'
            return ["pkexec", "bash", "-c", cmd_str]
        if step_id == "int_disk":
            media_cleanup = f'MEDIA_DIR="/media/{self.username}"; if [ -d "$MEDIA_DIR" ]; then echo -e "\\033[33m🧹 Cleaning $MEDIA_DIR...\\033[0m"; find "$MEDIA_DIR" -mindepth 1 -maxdepth 1 -type d | while read dir; do if ! mountpoint -q "$dir" 2>/dev/null; then if [ -z "$(find "$dir" -type f 2>/dev/null | head -1)" ]; then rm -rf "$dir" 2>/dev/null && echo -e "\\033[32m  ✓ Removed: $dir\\033[0m" || echo -e "\\033[33m  ⚠ Cannot remove: $dir\\033[0m"; else echo -e "\\033[33m  ⏭ Skipped (has files): $dir\\033[0m"; fi; else echo -e "\\033[33m  ⏭ Skipped (still mounted): $dir\\033[0m"; fi; done; echo -e "\\033[32m✓ /media cleaned\\033[0m"; fi'
            fstab_cleanup = "cp /etc/fstab /etc/fstab.bak_easymonerod; " + "sed -i '/# Entr.*EasyNode/d' /etc/fstab; " + "sed -i '/\\/media\\/.*auto.*x-gvfs-show/d' /etc/fstab; " + "systemctl daemon-reload 2>/dev/null || true; " + "udevadm trigger 2>/dev/null || true; " + "echo -e '\\033[32m✓ fstab cleaned\\033[0m'; " + media_cleanup + "; echo -e '\\033[32m✓ ✅external disk ready\\033[0m'"
            cmd_str = f'{preamble} unmount_sdb1 2>/dev/null; {fstab_cleanup}'
            return ["pkexec", "bash", "-c", cmd_str]
        return None     
    def _run_script_step(self, step_id, terminal, status_label, run_btn):
        status_label.set_text("\u23f3 " + self.t("running"))
        status_label.add_css_class("status-running")
        run_btn.set_sensitive(False)
        cmd = self._build_step_command(step_id)
        if cmd:
            self._run_in_terminal(terminal, cmd)
        else:
            if step_id == "ext_disk":
                disk_name = self.disk_entry.get_text().strip()
                if not disk_name:
                    status_label.set_text("\u26a0\ufe0f Enter disk name first")
                    status_label.add_css_class("status-warning")
                    run_btn.set_sensitive(True)
                    return
                run_btn.set_sensitive(False)
                status_label.set_text("\u23f3 " + self.t("running"))
                browse_path = ""
                if hasattr(self, '_browse_path_entry'):
                    browse_path = self._browse_path_entry.get_text().strip()
                if browse_path:
                    escaped_path = browse_path.replace("'", "'\\''")
                    config_path = f"/home/{self.username}/.bitmonero/bitmonero.conf"
                    escaped_config = config_path.replace("'", "'\\''")
                    cmd_str = (
                        self._source_preamble() +
                        f'press_enter() {{ true; }}; '
                        f'DEVICE=$(df "{escaped_path}" 2>/dev/null | tail -1 | awk \'{{print $1}}\'); '
                        f'if [ -z "$DEVICE" ] || [ "$DEVICE" = "-" ]; then '
                        f'  PARENT=$(dirname "{escaped_path}"); '
                        f'  DEVICE=$(df "$PARENT" 2>/dev/null | tail -1 | awk \'{{print $1}}\'); '
                        f'fi; '
                        f'echo "i Detected partition: $DEVICE"; '
                        f'EXISTING_RPC_LOGIN=""; '
                        f'if [ -f "{escaped_config}" ] && grep -q "^rpc-login=" "{escaped_config}"; then '
                        f'  EXISTING_RPC_LOGIN=$(grep "^rpc-login=" "{escaped_config}"); '
                        f'fi; '
                        f"mkdir -p '{escaped_path}'; "
                        f"chown -R {self.username}:{self.username} '{escaped_path}' 2>/dev/null; "
                        f"mkdir -p /home/{self.username}/.bitmonero; "
                        f"if [ -f '{escaped_config}' ]; then "
                        f"  sed -i '/^data-dir=/d' '{escaped_config}'; "
                        f"  echo 'data-dir={escaped_path}' >> '{escaped_config}'; "
                        f"else "
                        f"  echo 'data-dir={escaped_path}' > '{escaped_config}'; "
                        f"fi; "
                        f'if [ -n "$EXISTING_RPC_LOGIN" ]; then '
                        f'  grep -q "^rpc-login=" "{escaped_config}" || echo "$EXISTING_RPC_LOGIN" >> "{escaped_config}"; '
                        f'fi; '
                        f"chown {self.username}:{self.username} '{escaped_config}'; "
                        f"chmod 644 '{escaped_config}'; "
                        f"chown -R {self.username}:{self.username} /home/{self.username}/.bitmonero; "
                        f'echo -e "\\033[32m\u2713 data-dir={escaped_path}\\033[0m"; '
                        f'DEVICE_UUID=$(blkid -s UUID -o value "$DEVICE" 2>/dev/null); '
                        f'echo "i Detected UUID: $DEVICE_UUID"; '
                        f'if [ -n "$DEVICE_UUID" ]; then '
                        f'  cp /etc/fstab /etc/fstab.bak_easymonerod; '
                        f'  sed -i "/UUID=$DEVICE_UUID/d" /etc/fstab; '
                        f"  sed -i '/# Entr.*EasyNode/d' /etc/fstab; "
                        f'  USER_ID=$(id -u {self.username}); '
                        f'  GROUP_ID=$(id -g {self.username}); '
                        f'  MOUNT_POINT=$(findmnt -n -o TARGET "$DEVICE" 2>/dev/null); '
                        f'  if [ -z "$MOUNT_POINT" ]; then MOUNT_POINT="/media/{self.username}"; fi; '
                        f'  echo "# Entree pour EasyNode - Ne pas modifier manuellement" >> /etc/fstab; '
                        f'  echo "UUID=$DEVICE_UUID $MOUNT_POINT auto defaults,users,uid=$USER_ID,gid=$GROUP_ID,umask=022,nofail,x-gvfs-show 0 0" >> /etc/fstab; '
                        f'  systemctl daemon-reload; '
                        f'  echo -e "\\033[32m\u2713 Auto-mount configured (UUID=$DEVICE_UUID)\\033[0m"; '
                        f'  echo -e "\\033[32m\u2713 Mount point: $MOUNT_POINT\\033[0m"; '
                        f'  echo -e "\\033[32m\u2713 Blockchain configured in: {escaped_path}\\033[0m"; '
                        f'  echo -e "\\033[32m\u2713 Disk ready\\033[0m"; '
                        f'else '
                        f'  echo -e "\\033[33m\u26a0 UUID not found for $DEVICE -- fstab not configured\\033[0m"; '
                        f'  echo -e "\\033[33m\u26a0 Disk must be mounted manually before each start\\033[0m"; '
                        f'fi'
                    )
                    self._run_in_terminal(terminal, ["pkexec", "bash", "-c", cmd_str])
                    if hasattr(self, 'datadir_display_label'):
                        GLib.timeout_add_seconds(3, self._refresh_datadir_label)
                    return
                else:
                    cmd_str = (
                        self._source_preamble() +
                        f'press_enter() {{ true; }}; '
                        f'echo -e "{disk_name}\\\\n\\\\n\\\\n\\\\n" | manage_blockchain'
                    )
                self._run_in_terminal(terminal, ["pkexec", "bash", "-c", cmd_str])
                if hasattr(self, 'datadir_display_label'):
                    GLib.timeout_add_seconds(3, self._refresh_datadir_label)
                return
            run_btn.set_sensitive(True)
            status_label.set_text("")

    def _run_configure_bitmonero(self, terminal, status_label, run_btn):
        self.bitmonero_error_label.set_text("")
        if self.rpc_radio_pass.get_active():
            pwd = self.rpc_password_entry.get_text()
            pwd_confirm = self.rpc_password_confirm.get_text()
            if len(pwd) < 6:
                self.bitmonero_error_label.set_text("⚠️ " + self.t("password_too_short"))
                return
            if pwd != pwd_confirm:
                self.bitmonero_error_label.set_text("⚠️ " + self.t("password_mismatch"))
                return
            security_choice = "1"
            rpc_password = pwd
        else:
            security_choice = "2"
            rpc_password = ""
        status_label.set_text("⏳ " + self.t("running"))
        run_btn.set_sensitive(False)
        if security_choice == "1":
            cmd_str = (
                self._source_preamble() +
                f'_gui_read_count=0; '
                f'read() {{ '
                f'  _gui_read_count=$((_gui_read_count+1)); '
                f'  local args=("$@"); '
                f'  local prompt=""; '
                f'  for ((i=0; i<${{#args[@]}}; i++)); do '
                f'    if [[ "${{args[$i]}}" == "-p" ]]; then prompt="${{args[$((i+1))]}}"; fi; '
                f'  done; '
                f'  if [[ "$prompt" == *"Entrée"* ]] || [[ "$prompt" == *"Enter"* ]] || [[ "$prompt" == *"continuer"* ]] || [[ "$prompt" == *"continue"* ]] || [[ "$prompt" == *"menu"* ]]; then '
                f'    echo ""; return 0; '
                f'  fi; '
                f'  if [ $_gui_read_count -eq 1 ]; then eval "${{!#}}={security_choice}"; return 0; fi; '
                f'  if [ $_gui_read_count -eq 2 ]; then eval "${{!#}}={rpc_password}"; return 0; fi; '
                f'  if [ $_gui_read_count -eq 3 ]; then eval "${{!#}}={rpc_password}"; return 0; fi; '
                f'  builtin read "$@"; '
                f'}}; '
                f'configure_monero'
            )
        else:
            cmd_str = (
                self._source_preamble() +
                f'_gui_read_count=0; '
                f'read() {{ '
                f'  _gui_read_count=$((_gui_read_count+1)); '
                f'  local args=("$@"); '
                f'  local prompt=""; '
                f'  for ((i=0; i<${{#args[@]}}; i++)); do '
                f'    if [[ "${{args[$i]}}" == "-p" ]]; then prompt="${{args[$((i+1))]}}"; fi; '
                f'  done; '
                f'  if [[ "$prompt" == *"Entrée"* ]] || [[ "$prompt" == *"Enter"* ]] || [[ "$prompt" == *"continuer"* ]] || [[ "$prompt" == *"continue"* ]] || [[ "$prompt" == *"menu"* ]]; then '
                f'    echo ""; return 0; '
                f'  fi; '
                f'  if [ $_gui_read_count -eq 1 ]; then eval "${{!#}}={security_choice}"; return 0; fi; '
                f'  builtin read "$@"; '
                f'}}; '
                f'configure_monero'
            )
        self._run_in_terminal(terminal, ["pkexec", "bash", "-c", cmd_str])

    def _run_start_blockchain(self, terminal, status_label, run_btn):
        bc_type = "complete" if self.bc_radio_complete.get_active() else "pruned"
        bc_choice = "1" if bc_type == "complete" else "2"
        start_choice = "1" if self.start_radio_ban.get_active() else "2"
        status_label.set_text("⏳ " + self.t("running"))
        status_label.add_css_class("status-running")
        run_btn.set_sensitive(False)
        cmd_str = (
            self._source_preamble() +
            f'BLOCKCHAIN_TYPE={bc_type}; '
            f'bc_choice={bc_choice}; '
            f'START_CHOICE={start_choice}; '
            f'select_blockchain_type() {{ true; }}; '
            f'_gui_read_count=0; '
            f'read() {{ '
            f'  local args=("$@"); '
            f'  local prompt=""; '
            f'  for ((i=0; i<${{#args[@]}}; i++)); do '
            f'    if [[ "${{args[$i]}}" == "-p" ]]; then prompt="${{args[$((i+1))]}}"; fi; '
            f'  done; '
            f'  if [[ "$prompt" == *"Entrée"* ]] || [[ "$prompt" == *"Enter"* ]] || [[ "$prompt" == *"continuer"* ]] || [[ "$prompt" == *"continue"* ]] || [[ "$prompt" == *"menu"* ]]; then '
            f'    echo ""; return 0; '
            f'  fi; '
            f'  _gui_read_count=$((_gui_read_count+1)); '
            f'  if [ $_gui_read_count -eq 1 ]; then '
            f'    eval "${{!#}}={bc_choice}"; return 0; '
            f'  elif [ $_gui_read_count -eq 2 ]; then '
            f'    eval "${{!#}}={start_choice}"; return 0; '
            f'  fi; '
            f'  builtin read "$@"; '
            f'}}; '
            f'start_blockchain'
        )
        self.blockchain_running = True
        if VTE_AVAILABLE and isinstance(terminal, Vte.Terminal):
            self._sync_terminal = terminal
            if not hasattr(self, '_vte_sync_timer') or self._vte_sync_timer is None:
                self._vte_sync_timer = GLib.timeout_add_seconds(3, self._poll_terminal_sync)
        self._run_in_terminal(terminal, ["pkexec", "bash", "-c", cmd_str])

    def _run_stop_blockchain(self, status_label, stop_btn=None):
        if stop_btn:
            stop_btn.set_sensitive(False)
        stopped = False
        if hasattr(self, 'start_terminal') and self.start_terminal:
            if VTE_AVAILABLE and isinstance(self.start_terminal, Vte.Terminal):
                try:
                    pty = self.start_terminal.get_pty()
                    if pty:
                        fd = pty.get_fd()
                        os.write(fd, b'\x03')
                        stopped = True
                except Exception:
                    pass
                if not stopped:
                    try:
                        self.start_terminal.feed_child(b'\x03')
                        stopped = True
                    except Exception:
                        pass
                if not stopped:
                    try:
                        self.start_terminal.feed_child_binary(b'\x03')
                        stopped = True
                    except Exception:
                        pass
            if not stopped:
                child_pid = getattr(self.start_terminal, '_child_pid', None)
                if child_pid:
                    try:
                        os.kill(child_pid, signal.SIGINT)
                        stopped = True
                    except Exception:
                        pass
        if stopped:
            if self.lang == "FR":
                status_label.set_text("✓ Arrêt en cours... (CTRL+C)")
            else:
                status_label.set_text("✓ Stopping... (CTRL+C)")
            status_label.add_css_class("status-running")
            self.blockchain_running = False
        else:
            try:
                subprocess.run(["pkexec", "bash", "-c",
                    "pkill -SIGINT -x monerod 2>/dev/null; "
                    "sleep 2; "
                    "pkill -x monerod 2>/dev/null; "
                    "echo 'Done'"
                ], check=False, timeout=20)
                if self.lang == "FR":
                    status_label.set_text("✓ Blockchain arrêtée")
                else:
                    status_label.set_text("✓ Blockchain stopped")
                self.blockchain_running = False
                status_label.add_css_class("status-running")
            except Exception as e:
                status_label.set_text(f"Error: {e}")
                status_label.add_css_class("status-warning")
        if stop_btn:
            stop_btn.set_sensitive(True)

    def _poll_terminal_sync(self):
        if not self.blockchain_running:
            self._vte_sync_timer = None
            return False
        if hasattr(self, '_sync_terminal') and self._sync_terminal:
            self._on_terminal_sync_output(self._sync_terminal)
        return True

    def _update_sync_progress_bar(self, height, target, synced):
        if not hasattr(self, '_sync_progress_bar') or self._sync_progress_bar is None:
            return
        if synced:
            self._sync_start_height = None
            self._sync_progress_bar.set_fraction(1.0)
            self._sync_progress_bar.set_text("100%")
            self._sync_progress_label.set_text(
                "✅ " + ("Blockchain synchronisée" if self.lang == "FR"
                          else "Blockchain synchronized"))
        elif target > 0 and height > 0:
            if not hasattr(self, '_sync_start_height') or self._sync_start_height is None:
                self._sync_start_height = height
            total_to_sync = target - self._sync_start_height
            done = height - self._sync_start_height
            if total_to_sync > 0:
                pct = done / total_to_sync
                if pct > 1.0:
                    pct = 1.0
                if pct < 0.0:
                    pct = 0.0
            else:
                pct = 1.0
            self._sync_progress_bar.set_fraction(pct)
            self._sync_progress_bar.set_text(f"{pct * 100:.1f}%")
            remaining = target - height
            self._sync_progress_label.set_text(
                f"⟳ {height:,} / {target:,}  —  {remaining:,} ".replace(",", " ") +
                ("blocs restants" if self.lang == "FR" else "blocks remaining"))
        elif height > 0:
            self._sync_progress_bar.pulse()
            self._sync_progress_label.set_text(
                f"⟳ {height:,} ".replace(",", " ") +
                ("blocs" if self.lang == "FR" else "blocks"))
        else:
            self._sync_start_height = None
            self._sync_progress_bar.set_fraction(0.0)
            self._sync_progress_bar.set_text("—")
            self._sync_progress_label.set_text(
                "⏳ " + ("En attente de connexion..." if self.lang == "FR"
                          else "Waiting for connection..."))

    def _on_terminal_sync_output(self, terminal):
        import re
        text = ""
        try:
            cursor_col, cursor_row = terminal.get_cursor_position()
            scrollback = terminal.get_scrollback_lines() if hasattr(terminal, 'get_scrollback_lines') else 10000
            start_row = max(0, cursor_row - scrollback)
            result = terminal.get_text_range_format(Vte.Format.TEXT, start_row, 0, cursor_row, -1)
            if isinstance(result, tuple):
                text = result[0] if result[0] else ""
            else:
                text = str(result) if result else ""
            text = text[-5000:]
            text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
        except Exception:
            return
        if not text or len(text) < 5:
            return
        sync_match = re.findall(r'Synced\s+(\d+)/(\d+)', text)
        peers_match = re.findall(r'IN-PEERS:\s*(\d+)\s*\|\s*OUT-PEERS:\s*(\d+)', text)
        is_synced = "SYNCHRONIZED OK" in text.upper()
        height = 0
        target = 0
        if sync_match:
            height = int(sync_match[-1][0])
            target = int(sync_match[-1][1])
        in_p = 0
        out_p = 0
        if peers_match:
            in_p = int(peers_match[-1][0])
            out_p = int(peers_match[-1][1])
        if height == 0 and not is_synced and in_p == 0 and out_p == 0:
            return
        def update_labels():
            if self.sync_label.has_css_class("node-info-synced") and not is_synced:
                return False
            self.sync_label.remove_css_class("node-info-offline")
            if is_synced:
                self.sync_label.set_label("⟳ 100%")
                self.sync_label.remove_css_class("node-info-syncing")
                self.sync_label.add_css_class("node-info-synced")
            elif target > 0:
                pct = (height / target * 100)
                self.sync_label.set_label(f"⟳ {pct:.1f}%")
                self.sync_label.remove_css_class("node-info-synced")
                self.sync_label.add_css_class("node-info-syncing")
            self.height_label.remove_css_class("node-info-offline")
            if is_synced:
                self.height_label.set_label(f"📦 {height:,} ✅".replace(",", " "))
                self.height_label.remove_css_class("node-info-syncing")
                self.height_label.add_css_class("node-info-synced")
            elif height > 0:
                self.height_label.set_label(f"📦 {height:,}".replace(",", " "))
                self.height_label.remove_css_class("node-info-synced")
                self.height_label.add_css_class("node-info-syncing")
            total = in_p + out_p
            if total > 0 or peers_match:
                self.peers_label.set_label(f"👥 {total} ({in_p}↓{out_p}↑)")
                self.peers_label.remove_css_class("node-info-offline")
                self.peers_label.remove_css_class("node-info-syncing")
                self.peers_label.add_css_class("node-info-synced")
            self._update_sync_progress_bar(height, target, is_synced)
            return False
        GLib.idle_add(update_labels)

    def _refresh_xmr_price(self):
        threading.Thread(target=self._fetch_xmr_price_header, daemon=True).start()
        return True

    def _fetch_xmr_price_header(self):
        try:
            import urllib.request
            req = urllib.request.Request(
                "https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=usd,eur",
                headers={"User-Agent": "EasyMonerod-GUI/1.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                usd = data.get("monero", {}).get("usd", 0)
                eur = data.get("monero", {}).get("eur", 0)
                GLib.idle_add(lambda: self.xmr_header_label.set_label(f"⬡ ${usd:.0f} | {eur:.0f}€") or False)
        except Exception:
            GLib.idle_add(lambda: self.xmr_header_label.set_label("⬡ XMR --") or False)

    def _start_header_timers(self):
        GLib.timeout_add_seconds(0, lambda: threading.Thread(target=self._fetch_cpu_temp,         daemon=True).start() or False)
        GLib.timeout_add_seconds(2, lambda: threading.Thread(target=self._fetch_tor_status,       daemon=True).start() or False)
        GLib.timeout_add_seconds(1, lambda: threading.Thread(target=self._fetch_node_info,        daemon=True).start() or False)
        GLib.timeout_add_seconds(3, lambda: threading.Thread(target=self._fetch_xmr_price_header, daemon=True).start() or False)
        GLib.timeout_add_seconds(4, lambda: threading.Thread(target=self._fetch_monero_news,      daemon=True).start() or False)
        GLib.timeout_add_seconds(10,   self._refresh_cpu_temp)
        GLib.timeout_add_seconds(15,   self._refresh_tor_status)
        GLib.timeout_add_seconds(8,    self._refresh_node_info)
        GLib.timeout_add_seconds(120,  self._refresh_xmr_price)
        GLib.timeout_add_seconds(5,    self._rotate_news)
        GLib.timeout_add_seconds(1800, self._refetch_news)
        return False

    # ── Température CPU ──────────────────────────────────────
    def _refresh_cpu_temp(self):
        threading.Thread(target=self._fetch_cpu_temp, daemon=True).start()
        return True

    def _fetch_cpu_temp(self):
        temp = None
        try:
            import glob
            zones = sorted(glob.glob("/sys/class/thermal/thermal_zone*/temp"))
            for zone in zones:
                type_file = zone.replace("temp", "type")
                zone_type = ""
                try:
                    with open(type_file) as f:
                        zone_type = f.read().strip().lower()
                except Exception:
                    pass
                try:
                    with open(zone) as f:
                        val = int(f.read().strip()) / 1000.0
                    if 0 < val < 150:
                        if any(k in zone_type for k in ["x86_pkg", "cpu", "acpitz", "coretemp"]):
                            temp = val
                            break
                        elif temp is None:
                            temp = val
                except Exception:
                    pass
        except Exception:
            pass
        def update():
            if temp is None:
                self.cpu_temp_label.set_label("🌡️ --°C")
                self.cpu_temp_label.remove_css_class("cpu-temp-hot")
            else:
                self.cpu_temp_label.set_label(f"🌡️ {temp:.0f}°C")
                if temp >= 80:
                    self.cpu_temp_label.add_css_class("cpu-temp-hot")
                else:
                    self.cpu_temp_label.remove_css_class("cpu-temp-hot")
            return False
        GLib.idle_add(update)

    # ── Statut Tor ───────────────────────────────────────────
    def _refresh_tor_status(self):
        threading.Thread(target=self._fetch_tor_status, daemon=True).start()
        return True

    def _fetch_tor_status(self):
        status = "inactive"
        try:
            r = subprocess.run(["systemctl", "is-active", "tor"],
                               capture_output=True, text=True, timeout=5)
            service_active = r.stdout.strip() == "active"
        except Exception:
            service_active = False
        if not service_active:
            status = "inactive"
        else:
            bootstrapped = False
            try:
                r = subprocess.run(
                    ["tor-resolve", "check.torproject.org"],
                    capture_output=True, text=True, timeout=8
                )
                if r.returncode == 0 and r.stdout.strip():
                    bootstrapped = True
            except Exception:
                pass
            if not bootstrapped:
                for unit in ["tor@default", "tor"]:
                    try:
                        r = subprocess.run(
                            ["journalctl", "-u", unit, "--since", "1 min ago",
                             "--no-pager", "--output=cat"],
                            capture_output=True, text=True, timeout=5
                        )
                        log = r.stdout
                        if "Bootstrapped 100%" in log:
                            bootstrapped = True
                            break
                    except Exception:
                        continue
            status = "connected" if bootstrapped else "starting"
        def update():
            if status == "connected":
                self.tor_status_label.set_label("🧅 Tor ●")
                self.tor_status_label.remove_css_class("tor-inactive")
                self.tor_status_label.remove_css_class("tor-starting")
                self.tor_status_label.add_css_class("tor-active")
            elif status == "starting":
                self.tor_status_label.set_label("🧅 Tor ◑")
                self.tor_status_label.remove_css_class("tor-active")
                self.tor_status_label.remove_css_class("tor-inactive")
                self.tor_status_label.add_css_class("tor-starting")
            else:
                self.tor_status_label.set_label("🧅 Tor ○")
                self.tor_status_label.remove_css_class("tor-active")
                self.tor_status_label.remove_css_class("tor-starting")
                self.tor_status_label.add_css_class("tor-inactive")
            return False
        GLib.idle_add(update)

    # ── Infos nœud (hauteur, sync, pairs) ───────────────────
    def _refresh_node_info(self):
        threading.Thread(target=self._fetch_node_info, daemon=True).start()
        return True

    def _fetch_node_info(self):
        result = None
        rpc_login = None
        try:
            conf_path = f"/home/{self.username}/.bitmonero/bitmonero.conf"
            with open(conf_path, "r") as cf:
                for line in cf:
                    line = line.strip()
                    if line.startswith("rpc-login="):
                        rpc_login = line.split("=", 1)[1].strip()
                        break
        except Exception:
            pass
        for port in [18081, 18089]:
            try:
                rpc_url = f"http://127.0.0.1:{port}/json_rpc"
                cmd = ["curl", "-s", "--max-time", "2",
                       "-X", "POST", rpc_url,
                       "-H", "Content-Type: application/json",
                       "-d", '{"jsonrpc":"2.0","id":"0","method":"get_info"}']
                if rpc_login:
                    cmd.insert(2, "--digest")
                    cmd.insert(3, "-u")
                    cmd.insert(4, rpc_login)
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=4)
                if r.stdout.strip():
                    result = json.loads(r.stdout).get("result")
                if result:
                    break
            except Exception:
                continue
        def update():
            if result is None:
                if getattr(self, 'blockchain_running', False):
                    return False
                for lbl in [self.height_label, self.peers_label, self.sync_label]:
                    lbl.remove_css_class("node-info-synced")
                    lbl.remove_css_class("node-info-syncing")
                    lbl.add_css_class("node-info-offline")
                self.height_label.set_label("📦 --")
                self.peers_label.set_label("👥 --")
                self.sync_label.set_label("⟳ --%")
                self._update_sync_progress_bar(0, 0, False)
                return False
            height = result.get("height", 0)
            target = result.get("target_height", 0)
            if target == 0:
                synced = result.get("synchronized", False)
            else:
                synced = result.get("synchronized", False) or height >= target
            self.sync_label.remove_css_class("node-info-offline")
            if synced:
                self.sync_label.set_label("⟳ 100%")
                self.sync_label.remove_css_class("node-info-syncing")
                self.sync_label.add_css_class("node-info-synced")
                if hasattr(self, '_vte_sync_timer') and self._vte_sync_timer:
                    GLib.source_remove(self._vte_sync_timer)
                    self._vte_sync_timer = None
            else:
                if target > 0:
                    pct = (height / target * 100)
                    self.sync_label.set_label(f"⟳ {pct:.1f}%")
                else:
                    self.sync_label.set_label("⟳ 0%")
                self.sync_label.remove_css_class("node-info-synced")
                self.sync_label.add_css_class("node-info-syncing")
            if synced:
                self.height_label.set_label(f"📦 {height:,} ✅".replace(",", " "))
                self.height_label.remove_css_class("node-info-offline")
                self.height_label.remove_css_class("node-info-syncing")
                self.height_label.add_css_class("node-info-synced")
            else:
                self.height_label.set_label(f"📦 {height:,}".replace(",", " "))
                self.height_label.remove_css_class("node-info-offline")
                self.height_label.remove_css_class("node-info-synced")
                self.height_label.add_css_class("node-info-syncing")
            in_p  = result.get("incoming_connections_count", 0)
            out_p = result.get("outgoing_connections_count", 0)
            total = in_p + out_p
            self.peers_label.set_label(f"👥 {total} ({in_p}↓{out_p}↑)")
            self.peers_label.remove_css_class("node-info-offline")
            if total > 0:
                self.peers_label.remove_css_class("node-info-syncing")
                self.peers_label.add_css_class("node-info-synced")
            else:
                self.peers_label.remove_css_class("node-info-synced")
                self.peers_label.add_css_class("node-info-syncing")
            self._update_sync_progress_bar(height, target, synced)
            return False
        GLib.idle_add(update)

    # ── Monero News (RSS monero.forum + revuo-xmr.com) ─────────────────────
    def _refetch_news(self):
        threading.Thread(target=self._fetch_monero_news, daemon=True).start()
        return True

    def _fetch_monero_news(self):
        import urllib.request
        import json
        from datetime import datetime, timezone, timedelta
        import re
        import random
        import xml.etree.ElementTree as ET
        fallback = [
            "📰 Monero — Privacy. Security. Untraceable.",
            "🔒 Ring Signatures + RingCT + Stealth Addresses = full privacy",
            "⛓️ Monero is open-source and community-driven",
            "🌐 Run your own node — contribute to the network",
            "🧅 Tor support built-in — route traffic anonymously",
            f"⬡ Monero CLI v{MONERO_VERSION} — getmonero.org",
            "📡 Port 18080 = P2P  |  18081 = RPC  |  18083 = ZMQ",
            "🔑 Your keys, your coins — non-custodial by design",
            "🛡️ Monero is fungible — every coin is equal",
            "🔍 Transactions are private by default, not opt-in",
        ]
        def parse_rss_date(date_str):
            if not date_str:
                return None
            date_str = date_str.strip()
            for fmt in ("%a, %d %b %Y %H:%M:%S %z",
                        "%a, %d %b %Y %H:%M:%S %Z",
                        "%d %b %Y %H:%M:%S %z",
                        "%Y-%m-%dT%H:%M:%S%z",
                        "%Y-%m-%dT%H:%M:%SZ"):
                try:
                    dt = datetime.strptime(date_str, fmt)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt
                except ValueError:
                    continue
            return None
        one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
        def fetch_revuo_news(source_icon="📰", max_items=25):
            items = []
            try:
                req = urllib.request.Request(
                    "https://www.revuo-xmr.com/index.xml",
                    headers={"User-Agent": "EasyMonerod/1.7.3"})
                with urllib.request.urlopen(req, timeout=12) as r:
                    raw = r.read().decode("utf-8", errors="replace")
                root = ET.fromstring(raw)
                page_url = None
                for rss_item in root.findall(".//item"):
                    date_el = rss_item.find("pubDate")
                    if date_el is not None and date_el.text:
                        pub_date = parse_rss_date(date_el.text)
                        if pub_date and pub_date < one_month_ago:
                            continue
                    link_el = rss_item.find("link")
                    if link_el is not None and link_el.text:
                        page_url = link_el.text.strip()
                        break
                if not page_url:
                    return items
                req2 = urllib.request.Request(
                    page_url,
                    headers={"User-Agent": "EasyMonerod/1.7.3"})
                with urllib.request.urlopen(req2, timeout=15) as r2:
                    html = r2.read().decode("utf-8", errors="replace")
                headlines = re.findall(r'<h4[^>]*>(.*?)</h4>', html, re.DOTALL)
                for h in headlines:
                    clean = re.sub(r'<[^>]+>', '', h).strip()
                    if len(clean) > 120:
                        clean = clean[:117] + "..."
                    if clean and len(clean) > 10:
                        items.append(f"{source_icon} {clean}")
                        if len(items) >= max_items:
                            break
            except Exception:
                pass
            return items
        rss_items = fetch_revuo_news("📰", max_items=25)
        seen_titles = set(rss_items)
        random.shuffle(rss_items)
        random.shuffle(fallback)
        items = []
        max_len = max(len(rss_items), len(fallback))
        for i in range(max_len):
            if i < len(rss_items):
                items.append(rss_items[i])
            if i < len(fallback):
                items.append(fallback[i])
        if not items:
            items = fallback[:]
        def store():
            self._news_items = items
            self._news_index = 0
            if items:
                self.news_label.set_label(items[0])
            return False
        GLib.idle_add(store)

    def _rotate_news(self):
        if self._news_items:
            self._news_index = (self._news_index + 1) % len(self._news_items)
            text = self._news_items[self._news_index]
            GLib.idle_add(lambda: self.news_label.set_label(text) or False)
        return True

    def _on_change_language(self, button):
        is_running = self.blockchain_running
        if not is_running:
            try:
                result = subprocess.run(
                    ["pgrep", "-x", "monerod"],
                    capture_output=True, timeout=3
                )
                is_running = result.returncode == 0
            except Exception:
                pass
        if not is_running:
            self.main_stack.set_visible_child_name("language")
            return
        if self.lang == "FR":
            heading = "⚠️ Blockchain en cours d'exécution !"
            body = ("Le nœud Monero est actif.\n\n"
                    "Changer de langue va reconstruire l'interface et vous ferez perdre "
                    "la vue sur le terminal.\n\n"
                    "Monerod continuera de tourner en arrière-plan mais vous ne pourrez "
                    "plus l'arrêter proprement depuis l'interface.\n\n"
                    "Arrêtez la blockchain d'abord (bouton ARRÊTER), puis changez de langue.")
            btn_ok = "OK, je reste"
        else:
            heading = "⚠️ Blockchain is running!"
            body = ("The Monero node is active.\n\n"
                    "Changing language will rebuild the interface and you will lose "
                    "the view of the terminal.\n\n"
                    "Monerod will keep running in the background but you won't be able "
                    "to stop it properly from the interface.\n\n"
                    "Stop the blockchain first (STOP button), then change language.")
            btn_ok = "OK, stay"
        dialog = Adw.MessageDialog(
            transient_for=self.win,
            heading=heading,
            body=body,
        )
        dialog.add_response("ok", btn_ok)
        dialog.set_default_response("ok")
        dialog.present()

    def _check_monero_update(self):
        logfile = "/tmp/easymonerod_update.log"
        def log(msg):
            with open(logfile, "a") as f:
                f.write(msg + "\n")
        log(f"Thread started, current version: {MONERO_VERSION}")
        log(f"API URL: {GITHUB_MONERO_API}")
        try:
            import urllib.request
            log("Fetching API...")
            req = urllib.request.Request(
                GITHUB_MONERO_API,
                headers={"User-Agent": "EasyMonerod-GUI/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode()
                data = json.loads(raw)
                tag = data.get("tag_name", "")
                latest = tag.lstrip("v")
                log(f"Current: {MONERO_VERSION}, GitHub latest: {latest}")
                if latest and latest != MONERO_VERSION:
                    self._latest_monero_version = latest
                    log(f"Update available! {MONERO_VERSION} -> {latest}")
                    GLib.idle_add(self._show_update_available, latest)
                else:
                    log("Already up to date")
                    GLib.idle_add(self._show_up_to_date)
        except Exception as e:
            log(f"Error: {e}")
            GLib.idle_add(self._show_check_failed)

    def _show_update_available(self, version):
        if self.lang == "FR":
            self.update_btn.set_label(f"⬆ MAJ dispo : v{version}")
        else:
            self.update_btn.set_label(f"⬆ Update: v{version}")
        self.update_btn.set_sensitive(True)
        self.update_btn.remove_css_class("secondary-button")
        self.update_btn.add_css_class("action-button")
        return False

    def _show_up_to_date(self):
        self.update_btn.set_label("✓ Monero v" + MONERO_VERSION + " ✓")
        self.update_btn.set_sensitive(False)
        return False

    def _show_check_failed(self):
        self.update_btn.set_label("⚠ Monero v" + MONERO_VERSION)
        self.update_btn.set_sensitive(False)
        return False

    def _on_update_clicked(self, button):
        new_version = self._latest_monero_version
        if not new_version:
            return
        dialog = Adw.MessageDialog(
            transient_for=self.get_active_window(),
            heading="Monero Update" if self.lang == "EN" else "Mise à jour Monero",
            body=(f"Mettre à jour Monero de v{MONERO_VERSION} vers v{new_version} ?\n\n"
                  f"Cela modifie la version dans le GUI.\n"
                  f"Relancez ensuite l'étape 2 (Installer Monero CLI) pour télécharger la nouvelle version."
                  if self.lang == "FR" else
                  f"Update Monero from v{MONERO_VERSION} to v{new_version}?\n\n"
                  f"This updates the version in the GUI.\n"
                  f"Then re-run step 2 (Install Monero CLI) to download the new version."),
        )
        dialog.add_response("cancel", "Annuler" if self.lang == "FR" else "Cancel")
        dialog.add_response("update", "⬆ " + ("Mettre à jour" if self.lang == "FR" else "Update"))
        dialog.set_response_appearance("update", Adw.ResponseAppearance.SUGGESTED)
        dialog.connect("response", self._on_update_response, new_version)
        dialog.present()

    def _on_update_response(self, dialog, response, new_version):
        global MONERO_VERSION
        if response != "update":
            return
        old_version = MONERO_VERSION
        gui_path = os.path.abspath(__file__)
        sed_cmd = (
            f"sed -i 's/MONERO_VERSION = \"{old_version}\"/MONERO_VERSION = \"{new_version}\"/g' \"{gui_path}\"; "
            f"sed -i \"s/MONERO_VERSION=\\\"{old_version}\\\"/MONERO_VERSION=\\\"{new_version}\\\"/g\" \"{gui_path}\"; "
        )
        if gui_path != INSTALLED_GUI_PATH and os.path.isfile(INSTALLED_GUI_PATH):
            sed_cmd += (
                f"sed -i 's/MONERO_VERSION = \"{old_version}\"/MONERO_VERSION = \"{new_version}\"/g' \"{INSTALLED_GUI_PATH}\"; "
                f"sed -i \"s/MONERO_VERSION=\\\"{old_version}\\\"/MONERO_VERSION=\\\"{new_version}\\\"/g\" \"{INSTALLED_GUI_PATH}\"; "
            )
        try:
            subprocess.run(
                ["pkexec", "bash", "-c", sed_cmd],
                check=True, timeout=15
            )
            MONERO_VERSION = new_version
            if self.lang == "FR":
                self.update_btn.set_label(f"✓ Mis à jour → v{new_version}")
            else:
                self.update_btn.set_label(f"✓ Updated → v{new_version}")
            self.update_btn.set_sensitive(False)
            self.update_btn.remove_css_class("action-button")
            self.update_btn.add_css_class("secondary-button")
            success_dialog = Adw.MessageDialog(
                transient_for=self.get_active_window(),
                heading="✓ " + ("Succès" if self.lang == "FR" else "Success"),
                body=(f"Version mise à jour vers v{new_version} !\n\n"
                      f"▶ Redémarrez le GUI\n"
                      f"▶ Puis lancez l'étape 2 pour installer Monero v{new_version}"
                      if self.lang == "FR" else
                      f"Version updated to v{new_version}!\n\n"
                      f"▶ Restart the GUI\n"
                      f"▶ Then run step 2 to install Monero v{new_version}"),
            )
            success_dialog.add_response("ok", "OK")
            success_dialog.present()
        except Exception as e:
            error_dialog = Adw.MessageDialog(
                transient_for=self.get_active_window(),
                heading="⚠️ " + ("Erreur" if self.lang == "FR" else "Error"),
                body=str(e),
            )
            error_dialog.add_response("ok", "OK")
            error_dialog.present()

    def _on_exit(self, button):
        if not self._on_window_close_request(self.win):
            self.quit()

    def _on_window_close_request(self, window):
        is_running = self.blockchain_running
        if not is_running:
            try:
                result = subprocess.run(
                    ["pgrep", "-x", "monerod"],
                    capture_output=True, timeout=3
                )
                is_running = result.returncode == 0
            except Exception:
                pass
        if not is_running:
            return False
        if self.lang == "FR":
            heading = "⚠️ Blockchain en cours d'exécution !"
            body = ("Le nœud Monero (monerod) est actuellement actif.\n\n"
                    "Fermer l'application sans l'arrêter proprement peut corrompre la blockchain.\n\n"
                    "Que voulez-vous faire ?")
            btn_stop_quit = "⏹ Arrêter puis fermer"
            btn_cancel    = "Annuler"
        else:
            heading = "⚠️ Blockchain is running!"
            body = ("The Monero node (monerod) is currently active.\n\n"
                    "Closing the app without stopping it properly may corrupt the blockchain.\n\n"
                    "What do you want to do?")
            btn_stop_quit = "⏹ Stop then close"
            btn_cancel    = "Cancel"
        dialog = Adw.MessageDialog(
            transient_for=window,
            heading=heading,
            body=body,
        )
        dialog.add_response("cancel",    btn_cancel)
        dialog.add_response("stop_quit", btn_stop_quit)
        dialog.set_response_appearance("stop_quit", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.connect("response", self._on_close_dialog_response)
        dialog.present()
        return True

    def _on_close_dialog_response(self, dialog, response):
        if response != "stop_quit":
            return
        dummy_label = Gtk.Label()
        self._run_stop_blockchain(dummy_label, None)
        self._show_stopping_overlay()
        self._quit_poll_count = 0
        GLib.timeout_add(1000, self._poll_monerod_then_quit)

    def _show_stopping_overlay(self):
        if self.lang == "FR":
            heading = "⏳ Arrêt en cours..."
            body = ("Le nœud Monero s'arrête proprement.\n"
                    "Veuillez patienter (peut prendre jusqu'à 30 secondes).\n\n"
                    "L'application se fermera automatiquement.")
        else:
            heading = "⏳ Stopping..."
            body = ("The Monero node is shutting down properly.\n"
                    "Please wait (may take up to 30 seconds).\n\n"
                    "The application will close automatically.")
        self._stopping_dialog = Adw.MessageDialog(
            transient_for=self.win,
            heading=heading,
            body=body,
        )
        self._stopping_dialog.present()

    def _poll_monerod_then_quit(self):
        self._quit_poll_count += 1
        still_running = False
        try:
            result = subprocess.run(
                ["pgrep", "-x", "monerod"],
                capture_output=True, timeout=2
            )
            still_running = (result.returncode == 0)
        except Exception:
            still_running = False
        if not still_running or self._quit_poll_count >= 60:
            try:
                self._stopping_dialog.close()
            except Exception:
                pass
            self.quit()
            return False
        return True

# ─────────────────────────────────────────────
# ENTRY POINT kerlann
# ─────────────────────────────────────────────
def main():
    app = EasyMonerodApp()
    app.run(sys.argv)

if __name__ == "__main__":
    main()
