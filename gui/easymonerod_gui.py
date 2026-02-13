#!/usr/bin/env python3
"""
EasyMonerod GUI - Flatpak Edition
A GTK4 graphical interface for the EasyNode Monero node installer.
Based on easynode_linux.sh v5 by kerlannXmr
https://github.com/kerlannXmr/EasyMonerod

License: Same as original EasyMonerod project
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

# VTE Terminal - try multiple versions (GTK4 versions)
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
# CONSTANTS
# ─────────────────────────────────────────────
APP_ID = "org.easymonerod.gui"
APP_NAME = "EasyMonerod"
MONERO_VERSION = "0.18.4.5"
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
SCRIPT_PATH = os.path.join(SCRIPT_DIR, "easynode_linux.sh")
CONFIG_FILE = os.path.expanduser("~/.config/easymonerod/settings.json")

# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
TRANSLATIONS = {
    "FR": {
        "app_subtitle": "Installation facile d'un nœud Monero",
        "language_title": "SÉLECTION DE LA LANGUE",
        "menu_title": "MENU PRINCIPAL",
        "guide": "GUIDE",
        "update_system": "Mise à jour système",
        "install_monero": "Installer Monero CLI",
        "install_tor": "Installer service Tor",
        "configure_bitmonero": "Configurer bitmonero",
        "configure_dns": "Configurer DNS anonymes",
        "blockchain_section": "BLOCKCHAIN",
        "start": "DÉMARRER",
        "stop": "ARRÊTER",
        "disk_section": "Options Disque",
        "external_disk": "Blockchain sur DISQUE EXTERNE",
        "internal_disk": "Blockchain sur DISQUE INTERNE",
        "other_section": "AUTRES OPTIONS",
        "change_lang": "Changer langue",
        "features": "INFOS",
        "notes": "NOTES",
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
        "running": "En cours...",
        "completed": "Terminé",
        "error": "Erreur",
        "blockchain_type": "Type de blockchain :",
        "start_mode": "Mode de démarrage :",
        "select_disk": "Sélectionnez le disque :",
        "enter_disk": "Nom du disque (ex: sdb1) :",
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

<b><span foreground='#FF6600'>6)</span> Blockchain sur disque EXTERNE</b>
   - Montage et configuration fstab

<b><span foreground='#FF6600'>7)</span> Revenir sur disque INTERNE</b>
   - Démontage du disque externe

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

🙏 Dons MONERO(Xmr) : kerlann.xmr (cake wallet)
📧 Contact: easynode@kerlann.org
🔗 Code source: https://github.com/kerlannXmr/easymonerod""",
        "privacy_matters": "🔒 LA VIE PRIVÉE COMPTE 🔒",
        "thank_you": "Merci d'avoir utilisé ce programme.",
        "description": "Programme d'aide informatique et de liberté.\nPermet d'installer un nœud MONERO sans aucune connaissance sur Linux.",
    },
    "EN": {
        "app_subtitle": "Easy Monero node installation",
        "language_title": "LANGUAGE SELECTION",
        "menu_title": "MAIN MENU",
        "guide": "HOW TO",
        "update_system": "Update system",
        "install_monero": "Install Monero CLI",
        "install_tor": "Install configure Tor",
        "configure_bitmonero": "Configure bitmonero",
        "configure_dns": "Configure anonymous DNS",
        "blockchain_section": "BLOCKCHAIN",
        "start": "START",
        "stop": "STOP",
        "disk_section": "Disk Options",
        "external_disk": "Blockchain on EXTERNAL DISK",
        "internal_disk": "Blockchain on INTERNAL DISK",
        "other_section": "OTHER OPTIONS",
        "change_lang": "Change language",
        "features": "FEATURES",
        "notes": "READ",
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
        "running": "Running...",
        "completed": "Completed",
        "error": "Error",
        "blockchain_type": "Blockchain type:",
        "start_mode": "Start mode:",
        "select_disk": "Select disk:",
        "enter_disk": "Disk name (e.g., sdb1):",
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
  ➡️ Step 7: Unmount the blockchain from the external disk
  ➡️ Step 4: Also serves as DEBUG of the boot path

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

<b><span foreground='#FF6600'>6)</span> Blockchain on EXTERNAL disk</b>
   - Mounting and fstab configuration

<b><span foreground='#FF6600'>7)</span> Return to INTERNAL disk</b>
   - Unmounting external disk

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

🙏 MONERO(Xmr) donations: kerlann.xmr (cake wallet)
📧 Contact: easynode@kerlann.org
🔗 Source code: https://github.com/kerlannXmr/easymonerod""",
        "privacy_matters": "🔒 PRIVACY MATTERS 🔒",
        "thank_you": "Thank you for using this program.",
        "description": "Computer assistance and freedom program.\nHelps you install a MONERO node without any knowledge on Linux.",
    }
}

# ─────────────────────────────────────────────
# CUSTOM CSS - Monero Theme
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
"""


# ─────────────────────────────────────────────
# MAIN APPLICATION
# ─────────────────────────────────────────────
class EasyMonerodApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.lang = "FR"
        self.username = ""
        self.blockchain_type = "complete"
        self.connect("activate", self.on_activate)

    def t(self, key):
        """Get translated string"""
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["EN"]).get(key, key)

    def on_activate(self, app):
        # Load CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # Detect username
        self.username = os.environ.get("SUDO_USER", os.environ.get("USER", os.getlogin()))

        # Build main window
        self.win = Adw.ApplicationWindow(application=app)
        self.win.set_title("EasyMonerod")
        self.win.set_default_size(1100, 750)
        self.win.add_css_class("main-window")

        # Main layout: show language selector first
        self.main_stack = Gtk.Stack()
        self.main_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.main_stack.set_transition_duration(300)

        # Language page
        self.main_stack.add_named(self._build_language_page(), "language")

        # App page (built after language selection)
        self.app_page = Gtk.Box()
        self.main_stack.add_named(self.app_page, "app")

        self.win.set_content(self.main_stack)
        self.win.present()

    # ═══════════════════════════════════════════
    # LANGUAGE SELECTION PAGE
    # ═══════════════════════════════════════════
    def _build_language_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.set_valign(Gtk.Align.CENTER)
        page.set_halign(Gtk.Align.CENTER)

        # Monero ASCII banner
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
        page.append(Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0))  # spacer

        # Title
        title = Gtk.Label(label="LANGUAGE SELECTION / SÉLECTION DE LA LANGUE")
        title.add_css_class("page-title")
        title.set_margin_top(40)
        title.set_margin_bottom(30)
        page.append(title)

        # Language buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        btn_box.set_halign(Gtk.Align.CENTER)

        btn_fr = Gtk.Button(label="🇫🇷  Français")
        btn_fr.add_css_class("lang-button")
        btn_fr.connect("clicked", lambda b: self._select_language("FR"))
        btn_box.append(btn_fr)

        btn_en = Gtk.Button(label="🇬🇧  English")
        btn_en.add_css_class("lang-button")
        btn_en.connect("clicked", lambda b: self._select_language("EN"))
        btn_box.append(btn_en)

        page.append(btn_box)

        # Privacy matters
        privacy = Gtk.Label(label="🔒 PRIVACY MATTERS 🔒")
        privacy.add_css_class("banner-subtitle")
        privacy.set_margin_top(40)
        page.append(privacy)

        return page

    def _select_language(self, lang):
        self.lang = lang
        self._build_app_ui()
        self.main_stack.set_visible_child_name("app")

    # ═══════════════════════════════════════════
    # MAIN APP UI (after language selection)
    # ═══════════════════════════════════════════
    def _build_app_ui(self):
        # Clear old content
        child = self.app_page.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.app_page.remove(child)
            child = next_child

        # Outer box
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Header bar
        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="⬡ EASYMONEROD"))
        header.get_title_widget().add_css_class("page-title")

        # Language switch button in header
        lang_btn = Gtk.Button(label="🌐 " + self.lang)
        lang_btn.add_css_class("secondary-button")
        lang_btn.connect("clicked", self._on_change_language)
        header.pack_end(lang_btn)

        outer.append(header)

        # Paned: sidebar + content
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_shrink_start_child(False)
        paned.set_shrink_end_child(False)
        paned.set_position(260)

        # ── Sidebar ──
        sidebar_scroll = Gtk.ScrolledWindow()
        sidebar_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scroll.add_css_class("sidebar")
        sidebar_scroll.set_size_request(260, -1)

        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        sidebar.set_margin_top(8)

        # Mini banner in sidebar
        mini_banner = Gtk.Label(label="⬡ EASYNODE")
        mini_banner.add_css_class("banner-subtitle")
        mini_banner.set_margin_bottom(12)
        mini_banner.set_margin_top(8)
        sidebar.append(mini_banner)

        sidebar.append(Gtk.Separator())

        # Store buttons for highlighting
        self.sidebar_buttons = {}
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.content_stack.set_transition_duration(200)

        # Menu structure
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
                sidebar.append(btn)
                self.sidebar_buttons[page_id] = btn

        # Exit button at bottom
        sidebar.append(Gtk.Box(vexpand=True))  # spacer
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

        # ── Content area ──
        content_scroll = Gtk.ScrolledWindow()
        content_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        content_scroll.add_css_class("content-area")

        # Build all pages
        self.content_stack.add_named(self._build_guide_page(), "guide")
        self.content_stack.add_named(self._build_terminal_page("update", self.t("update_system"),
            "Step 1: System update, firewall, SSH, fail2ban..."), "update")
        self.content_stack.add_named(self._build_install_monero_page(), "monero")
        self.content_stack.add_named(self._build_terminal_page("tor", self.t("install_tor"),
            "Step 3: Tor hidden services setup"), "tor")
        self.content_stack.add_named(self._build_configure_bitmonero_page(), "bitmonero")
        self.content_stack.add_named(self._build_terminal_page("dns", self.t("configure_dns"),
            "Step 5: Anonymous DNS (AdGuard)"), "dns")
        self.content_stack.add_named(self._build_start_page(), "start")
        self.content_stack.add_named(self._build_stop_page(), "stop")
        self.content_stack.add_named(self._build_external_disk_page(), "ext_disk")
        self.content_stack.add_named(self._build_terminal_page("int_disk", self.t("internal_disk"),
            "Step 9: Unmount external disk, revert to internal"), "int_disk")
        self.content_stack.add_named(self._build_info_page("features"), "features")
        self.content_stack.add_named(self._build_info_page("notes"), "notes")

        content_scroll.set_child(self.content_stack)
        paned.set_end_child(content_scroll)

        outer.append(paned)
        self.app_page.append(outer)
        outer.set_vexpand(True)

        # Show guide by default
        self._activate_sidebar("guide")

    def _on_sidebar_click(self, button, page_id):
        if button.get_active():
            # Deactivate all others
            for pid, btn in self.sidebar_buttons.items():
                if pid != page_id:
                    btn.set_active(False)
            self.content_stack.set_visible_child_name(page_id)

    def _activate_sidebar(self, page_id):
        for pid, btn in self.sidebar_buttons.items():
            btn.set_active(pid == page_id)
        self.content_stack.set_visible_child_name(page_id)

    # ═══════════════════════════════════════════
    # PAGE BUILDERS
    # ═══════════════════════════════════════════

    def _create_terminal(self, height=400):
        """Create a VTE terminal or fallback TextView"""
        if VTE_AVAILABLE:
            terminal = Vte.Terminal()
            terminal.set_size_request(-1, height)
            terminal.add_css_class("terminal-view")
            terminal.set_color_background(Gdk.RGBA(red=0.05, green=0.05, blue=0.05, alpha=1.0))
            terminal.set_color_foreground(Gdk.RGBA(red=0.88, green=0.88, blue=0.88, alpha=1.0))
            terminal.set_font(Pango.FontDescription("Monospace 11"))
            terminal.set_scroll_on_output(True)
            terminal.set_scrollback_lines(10000)
            terminal.set_vexpand(True)
            return terminal
        else:
            # Fallback: scrollable TextView that looks like a terminal
            textview = Gtk.TextView()
            textview.set_editable(False)
            textview.set_cursor_visible(False)
            textview.set_monospace(True)
            textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            textview.set_size_request(-1, height)
            textview.set_vexpand(True)
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

        # Visual step flow
        flow_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        flow_box.set_halign(Gtk.Align.CENTER)
        flow_box.set_margin_top(20)

        steps = ["1", "➜", "2", "➜", "3", "➜", "4", "➜", "5", "➜", "6", "➜", "8"]
        for s in steps:
            if s == "➜":
                lbl = Gtk.Label(label=s)
                lbl.set_opacity(0.5)
                flow_box.append(lbl)
            else:
                btn = Gtk.Button(label=s)
                btn.add_css_class("step-badge")
                btn.set_size_request(40, 40)
                step_map = {"1": "update", "2": "monero", "3": "tor", "4": "bitmonero",
                            "5": "dns", "6": "ext_disk", "7": "int_disk", "8": "start"}
                if s in step_map:
                    btn.connect("clicked", lambda b, pid=step_map[s]: self._activate_sidebar(pid))
                flow_box.append(btn)

        page.append(flow_box)
        return page

    def _build_terminal_page(self, page_id, title, description):
        """Generic page with a Run button and embedded terminal"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)

        page.append(self._make_page_header(title, description))

        # Username entry
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

        # Terminal
        terminal = self._create_terminal(400)

        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(True)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)

        # Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)

        # Status label
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
        """Step 2: Install Monero CLI with GPG verification"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)

        page.append(self._make_page_header(
            "⬡ " + self.t("install_monero"),
            f"Monero v{MONERO_VERSION} - Download, GPG verify, install"
        ))

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

        # Info card
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info.add_css_class("info-box")
        info_lbl = Gtk.Label()
        info_lbl.set_markup(
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

        # Terminal
        terminal = self._create_terminal(350)

        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(True)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)

        # Buttons
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
        """Step 4: Configure bitmonero.conf with RPC security options"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)

        page.append(self._make_page_header(
            "⚙️ " + self.t("configure_bitmonero"),
            self.t("rpc_security")
        ))

        # Username
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

        # RPC Security choice
        security_group = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        # Option 1: With password
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

        # Password fields
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

        # Option 2: Without password
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

        # Toggle password fields visibility
        self.rpc_radio_pass.connect("toggled", lambda b: self.pass_fields_box.set_visible(b.get_active()))
        self.rpc_radio_nopass.connect("toggled", lambda b: self.pass_fields_box.set_visible(not b.get_active()))

        # Terminal
        terminal = self._create_terminal(200)

        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(True)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)

        # Error label
        self.bitmonero_error_label = Gtk.Label(label="")
        self.bitmonero_error_label.add_css_class("status-warning")
        self.bitmonero_error_label.set_xalign(0)
        page.append(self.bitmonero_error_label)

        # Buttons
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
        """Step 6: Start blockchain with options"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_start(24)
        page.set_margin_end(24)
        page.set_margin_top(20)
        page.set_margin_bottom(20)

        page.append(self._make_page_header("▶️ " + self.t("start")))

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

        # Options row
        options_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)

        # Blockchain type
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

        # Start mode
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

        # Terminal
        terminal = self._create_terminal(350)

        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(True)
        term_scroll.add_css_class("terminal-view")
        page.append(term_scroll)

        # Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)

        status_label = Gtk.Label(label="")
        status_label.set_hexpand(True)
        status_label.set_xalign(0)
        btn_box.append(status_label)

        run_btn = Gtk.Button(label="▶  " + self.t("start"))
        run_btn.add_css_class("action-button")
        run_btn.connect("clicked", lambda b: self._run_start_blockchain(terminal, status_label, run_btn))
        btn_box.append(run_btn)

        page.append(btn_box)
        return page

    def _build_stop_page(self):
        """Step 7: Stop blockchain"""
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

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.CENTER)
        btn_box.set_margin_top(24)

        status_label = Gtk.Label(label="")
        status_label.set_hexpand(True)
        status_label.set_xalign(0)
        btn_box.append(status_label)

        stop_btn = Gtk.Button(label="⏹  " + self.t("stop"))
        stop_btn.add_css_class("danger-button")
        stop_btn.connect("clicked", lambda b: self._run_stop_blockchain(status_label))
        btn_box.append(stop_btn)

        page.append(btn_box)
        return page

    def _build_external_disk_page(self):
        """Step 6: Blockchain on external disk - with auto disk listing"""
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

        # ── Disk list card ──
        disk_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        disk_card.add_css_class("option-card")

        disk_title = Gtk.Label(label=self.t("select_disk"))
        disk_title.set_xalign(0)
        disk_title.add_css_class("page-subtitle")
        disk_card.append(disk_title)

        # Scrollable list of detected disks
        self.disk_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        disk_scroll = Gtk.ScrolledWindow()
        disk_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        disk_scroll.set_child(self.disk_list_box)
        disk_scroll.set_min_content_height(120)
        disk_scroll.set_max_content_height(200)
        disk_card.append(disk_scroll)

        # Refresh button
        refresh_btn = Gtk.Button(label="🔄 " + ("Rafraîchir la liste" if self.lang == "FR" else "Refresh disk list"))
        refresh_btn.add_css_class("secondary-button")
        refresh_btn.set_margin_top(8)
        refresh_btn.connect("clicked", lambda b: self._refresh_disk_list())
        disk_card.append(refresh_btn)

        # Manual entry fallback
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

        # Terminal
        terminal = self._create_terminal(250)

        term_scroll = Gtk.ScrolledWindow()
        term_scroll.set_child(terminal)
        term_scroll.set_vexpand(True)
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

        # Auto-detect disks on page build
        self._disk_radio_group = None
        GLib.idle_add(self._refresh_disk_list)

        return page

    def _refresh_disk_list(self):
        """Detect and list available disks (partitions) using lsblk"""
        # Clear existing list
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

                name = parts[0]          # /dev/sdb1
                size = parts[1]          # 500G
                dtype = parts[2]         # part / disk
                fstype = parts[3] if len(parts) > 3 else ""
                mount = parts[4] if len(parts) > 4 else ""
                model = " ".join(parts[5:]) if len(parts) > 5 else ""

                # Show partitions (not whole disks, not loop, not rom)
                # Also skip small partitions (swap, boot) and currently mounted root
                if dtype == "part" and mount != "/":
                    short_name = name.replace("/dev/", "")
                    # Build display string
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

                    # When a radio is selected, update the entry field
                    radio.connect("toggled", lambda r, sn=short_name:
                                  self.disk_entry.set_text(sn) if r.get_active() else None)
                    self.disk_list_box.append(radio)

        except Exception as e:
            err_lbl = Gtk.Label(label=f"⚠️ Error: {e}")
            err_lbl.set_xalign(0)
            err_lbl.add_css_class("status-warning")
            self.disk_list_box.append(err_lbl)

        return False  # for GLib.idle_add

    def _build_info_page(self, page_type):
        """Features / Notes information page"""
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

        # Dynamic Tor/Network info for features page
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
            refresh_btn.connect("clicked", lambda b: self._load_network_info())
            net_card.append(refresh_btn)

            page.append(net_card)
            GLib.idle_add(self._load_network_info)

        # Links
        if page_type == "notes":
            links_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            links_box.set_margin_top(16)

            privacy_lbl = Gtk.Label(label=self.t("privacy_matters"))
            privacy_lbl.add_css_class("page-title")
            privacy_lbl.set_margin_top(20)
            links_box.append(privacy_lbl)

            page.append(links_box)

        return page

    def _load_network_info(self):
        """Load Tor addresses and network info dynamically"""
        info_parts = []

        # Tor Monero hidden service
        try:
            tor_monero = subprocess.run(
                ["sudo", "cat", f"/var/lib/tor/monero/hostname"],
                capture_output=True, text=True, timeout=5
            )
            if tor_monero.returncode == 0 and tor_monero.stdout.strip():
                addr = tor_monero.stdout.strip()
                info_parts.append(f"<b>Monero RPC .onion:</b>\n  <span foreground='#47a347'>{addr}</span>")
                info_parts.append(f"  Port: <b>18081</b>")
        except Exception:
            pass

        # Tor SSH hidden service
        try:
            tor_ssh = subprocess.run(
                ["sudo", "cat", f"/var/lib/tor/ssh/hostname"],
                capture_output=True, text=True, timeout=5
            )
            if tor_ssh.returncode == 0 and tor_ssh.stdout.strip():
                addr = tor_ssh.stdout.strip()
                info_parts.append(f"\n<b>SSH .onion:</b>\n  <span foreground='#47a347'>{addr}</span>")
                info_parts.append(f"  Port: <b>22</b>")
        except Exception:
            pass

        # Local IP
        try:
            ip_result = subprocess.run(
                ["hostname", "-I"],
                capture_output=True, text=True, timeout=5
            )
            if ip_result.returncode == 0:
                local_ip = ip_result.stdout.strip().split()[0]
                info_parts.append(f"\n<b>IP locale:</b> <span foreground='#e8b849'>{local_ip}</span>")
        except Exception:
            pass

        # Ports
        info_parts.append(f"\n<b>Ports:</b>")
        info_parts.append(f"  P2P: <b>18080</b>  |  RPC: <b>18081</b>  |  ZMQ: <b>18083</b>")
        info_parts.append(f"  SSH: <b>22</b>  |  Tor SOCKS: <b>9050</b>")

        # Tor status
        try:
            tor_status = subprocess.run(
                ["systemctl", "is-active", "tor"],
                capture_output=True, text=True, timeout=5
            )
            status = tor_status.stdout.strip()
            if status == "active":
                info_parts.append(f"\n<b>Tor:</b> <span foreground='#47a347'>✓ Actif</span>")
            else:
                info_parts.append(f"\n<b>Tor:</b> <span foreground='#CC3333'>✖ Inactif ({status})</span>")
        except Exception:
            pass

        if not info_parts:
            if self.lang == "FR":
                markup = "<i>Aucune information réseau disponible.\nInstallez Tor (étape 3) pour voir les adresses .onion.</i>"
            else:
                markup = "<i>No network info available.\nInstall Tor (step 3) to see .onion addresses.</i>"
        else:
            markup = "\n".join(info_parts)

        self.tor_info_label.set_markup(markup)
        return False

    # ═══════════════════════════════════════════
    # COMMAND EXECUTION
    # ═══════════════════════════════════════════

    def _run_in_terminal(self, terminal, cmd):
        """Spawn a command in a VTE terminal or fallback TextView"""
        if VTE_AVAILABLE and isinstance(terminal, Vte.Terminal):
            terminal.reset(True, True)
            try:
                terminal.spawn_async(
                    Vte.PtyFlags.DEFAULT,
                    os.path.expanduser("~"),
                    cmd,
                    None,  # envv
                    GLib.SpawnFlags.DEFAULT,
                    None, None,  # child_setup
                    -1,  # timeout
                    None,  # cancellable
                    None,  # callback
                )
            except Exception as e:
                print(f"Terminal spawn error: {e}")
        else:
            # Fallback: run command and capture output to TextView
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
        """Append text to a TextView buffer (called from GLib.idle_add)"""
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert(end_iter, text)
        return False

    def _source_preamble(self):
        """Build a bash preamble that sources ONLY the functions from the script,
        without executing the main menu (setup_terminal/select_language/show_menu)."""
        script = SCRIPT_PATH
        return (
            # Source everything EXCEPT the last 4 lines that auto-run the menu
            f'eval "$(head -n -4 "{script}")"; '
            # Override functions that would block in GUI context
            f'setup_terminal() {{ true; }}; '
            f'select_language() {{ true; }}; '
            f'show_menu() {{ true; }}; '
            f'draw_banner() {{ true; }}; '
            # Fix wget user-agent: getmonero.org blocks default wget user-agent
            f'real_wget=$(which wget); '
            f'wget() {{ $real_wget --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "$@"; }}; '
            f'export -f wget; '
            # Override ALL "read -p" that are just "press enter to continue" prompts
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
            # Set our variables
            f'LANG_CHOICE="{self.lang}"; '
            f'USERNAME="{self.username}"; '
            f'MONERO_VERSION="0.18.4.5"; '
            # Override ask_username to be non-interactive
            f'ask_username() {{ USERNAME="{self.username}"; return 0; }}; '
        )

    def _build_step_command(self, step_id):
        """Build the bash command for a given step."""
        preamble = self._source_preamble()

        step_functions = {
            "update":   "update_system",
            "monero":   "install_monero_cli",
            "tor":      "install_tor",
            "dns":      "configure_dns",
            "int_disk": "unmount_sdb1",
        }

        func = step_functions.get(step_id)
        if func:
            cmd_str = f'{preamble} {func}'
            return ["pkexec", "bash", "-c", cmd_str]
        return None

    def _run_script_step(self, step_id, terminal, status_label, run_btn):
        """Execute a script step in the terminal"""
        status_label.set_text("⏳ " + self.t("running"))
        status_label.add_css_class("status-running")
        run_btn.set_sensitive(False)
        run_btn.set_label("⏳ " + self.t("running"))

        cmd = self._build_step_command(step_id)
        if cmd:
            self._run_in_terminal(terminal, cmd)
        else:
            # For steps needing special handling
            if step_id == "ext_disk":
                disk_name = self.disk_entry.get_text().strip()
                if not disk_name:
                    status_label.set_text("⚠️ Enter disk name first")
                    status_label.add_css_class("status-warning")
                    run_btn.set_sensitive(True)
                    return

                run_btn.set_sensitive(False)
                run_btn.set_label("⏳ " + self.t("running"))
                status_label.set_text("⏳ " + self.t("running"))

                cmd_str = (
                    self._source_preamble() +
                    f'press_enter() {{ true; }}; '
                    f'echo -e "{disk_name}\\n\\n\\n\\n" | manage_blockchain'
                )
                self._run_in_terminal(terminal, ["pkexec", "bash", "-c", cmd_str])
                return

            run_btn.set_sensitive(True)
            status_label.set_text("")

    def _run_configure_bitmonero(self, terminal, status_label, run_btn):
        """Handle step 4 with RPC security options"""
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
        run_btn.set_label("⏳ " + self.t("running"))

        # Build a script that pre-answers the prompts
        if security_choice == "1":
            cmd_str = (
                self._source_preamble() +
                f'configure_monero <<< $\'{security_choice}\\n{rpc_password}\\n{rpc_password}\''
            )
        else:
            cmd_str = (
                self._source_preamble() +
                f'configure_monero <<< $\'{security_choice}\''
            )

        self._run_in_terminal(terminal, ["pkexec", "bash", "-c", cmd_str])

    def _run_start_blockchain(self, terminal, status_label, run_btn):
        """Handle step 6 with blockchain type and IP ban options"""
        bc_type = "complete" if self.bc_radio_complete.get_active() else "pruned"
        bc_choice = "1" if bc_type == "complete" else "2"
        start_choice = "1" if self.start_radio_ban.get_active() else "2"

        status_label.set_text("⏳ " + self.t("running"))
        status_label.add_css_class("status-running")
        run_btn.set_sensitive(False)
        run_btn.set_label("⏳ " + self.t("running"))

        cmd_str = (
            self._source_preamble() +
            f'BLOCKCHAIN_TYPE={bc_type}; '
            f'start_blockchain <<< $\'{bc_choice}\\n{start_choice}\''
        )

        self._run_in_terminal(terminal, ["pkexec", "bash", "-c", cmd_str])

    def _run_stop_blockchain(self, status_label):
        """Stop all monerod processes (but NOT this GUI)"""
        try:
            # Use pgrep/pkill with exact patterns to avoid killing easymonerod-gui
            subprocess.run(["pkexec", "bash", "-c",
                # Kill only the actual monerod daemon, not this GUI
                "pkill -x monerod 2>/dev/null; "
                "systemctl stop haproxy-monero 2>/dev/null; "
                "systemctl stop monero-decoy 2>/dev/null; "
                "systemctl stop monero 2>/dev/null; "
                "sleep 1; "
                "pkill -9 -x monerod 2>/dev/null; "
                "echo 'Blockchain stopped'"
            ], check=False)
            if self.lang == "FR":
                status_label.set_text("✓ Blockchain arrêtée")
            else:
                status_label.set_text("✓ Blockchain stopped")
            status_label.add_css_class("status-running")
        except Exception as e:
            status_label.set_text(f"Error: {e}")
            status_label.add_css_class("status-warning")

    def _on_change_language(self, button):
        """Switch back to language selection"""
        self.main_stack.set_visible_child_name("language")

    def _on_exit(self, button):
        """Exit application"""
        self.quit()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
def main():
    app = EasyMonerodApp()
    app.run(sys.argv)


if __name__ == "__main__":
    main()
