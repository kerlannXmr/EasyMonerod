#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  EasyMonerod GUI - Installation AUTONOME
#  
#  UN SEUL FICHIER SUFFIT !
#  Usage:
#    chmod +x install.sh
#    sudo bash install.sh
#
#  Ce script télécharge automatiquement tout le nécessaire
#  depuis GitHub et installe le GUI EasyMonerod.
# ═══════════════════════════════════════════════════════════════

set -e

# ─── URLs GitHub ───
GITHUB_BASE="https://raw.githubusercontent.com/kerlannXmr/EasyMonerod/main"
GUI_URL="$GITHUB_BASE/gui/easymonerod_gui.py"
SCRIPT_URL="https://github.com/kerlannXmr/EasyMonerod/releases/download/v5/easynode_linux.sh"
LOGO_URL="$GITHUB_BASE/picture/logo2.png"
GIF_URL="$GITHUB_BASE/picture/xxmr.gif"
QRCODE_URL="$GITHUB_BASE/picture/qrcode1.png"

# ─── Paths ───
INSTALL_DIR="/opt/easymonerod-gui"
BIN_LINK="/usr/local/bin/easymonerod-gui"

# ─── Colors ───
ORANGE='\033[38;5;208m'
GREEN='\033[38;5;71m'
WHITE='\033[38;5;255m'
RED='\033[38;5;167m'
RESET='\033[0m'

# ─── Banner ───
echo -e "${ORANGE}"
echo "  *     *   ***   *   * ***** ****   ***  "
echo "  **   **  *   *  **  * *     *   * *   * "
echo "  * * * * *     * * * * ****  ****  *   * "
echo "  *  *  * *     * *  ** *     * *   *   * "
echo "  *     *  *   *  *   * *     *  *  *   * "
echo "  *     *   ***   *   * ***** *   *  ***  "
echo "  ═══════════ ▌EASYNODE GUI▐ ═══════════  "
echo -e "${RESET}"
echo -e "${WHITE}Installation autonome de EasyMonerod GUI${RESET}"
echo ""

# ─── Check root ───
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}⚠️  Ce script doit être lancé avec sudo${RESET}"
    echo "   Usage: sudo bash install.sh"
    exit 1
fi

# ─── Détection : installation ou mise à jour ? ───
IS_UPDATE=false
if [ -f "$INSTALL_DIR/easymonerod_gui.py" ] && [ -f "$INSTALL_DIR/scripts/easynode_linux.sh" ]; then
    IS_UPDATE=true
    echo -e "${ORANGE}🔄 Installation existante détectée — mode MISE À JOUR${RESET}"
    echo -e "${WHITE}   Les fichiers seront mis à jour depuis GitHub.${RESET}"
else
    echo -e "${WHITE}🆕 Nouvelle installation...${RESET}"
fi
echo ""

# ─── Detect downloader ───
download() {
    local url="$1"
    local dest="$2"
    local tmp="$dest.tmp"
    local success=false

    if command -v wget &>/dev/null; then
        wget -q --show-progress -O "$tmp" "$url" 2>/dev/null && success=true
    elif command -v curl &>/dev/null; then
        curl -L --progress-bar -o "$tmp" "$url" 2>/dev/null && success=true
    else
        echo -e "${RED}⚠️  Ni wget ni curl ne sont installés !${RESET}"
        echo "   Installez l'un des deux : sudo apt install wget"
        exit 1
    fi

    # Vérifier que le fichier est non vide avant de l'accepter
    if [ "$success" = true ] && [ -s "$tmp" ]; then
        mv "$tmp" "$dest"
        return 0
    else
        rm -f "$tmp"
        return 1
    fi
}

# ─── Detect distro ───
detect_package_manager() {
    if command -v apt &>/dev/null; then
        echo "apt"
    elif command -v dnf &>/dev/null; then
        echo "dnf"
    elif command -v pacman &>/dev/null; then
        echo "pacman"
    else
        echo "unknown"
    fi
}

PKG_MANAGER=$(detect_package_manager)

# ═══════════════════════════════════════════
# STEP 1: Install system dependencies
# ═══════════════════════════════════════════
if [ "$IS_UPDATE" = true ]; then
    echo -e "${ORANGE}[1/4]${WHITE} Dépendances système — ${GREEN}déjà installées, étape ignorée${RESET}"
else
    echo -e "${ORANGE}[1/4]${WHITE} Installation des dépendances système...${RESET}"
    case $PKG_MANAGER in
        apt)
            apt update
            apt install -y \
                python3 \
                python3-gi \
                python3-gi-cairo \
                gir1.2-gtk-4.0 \
                gir1.2-adw-1 \
                gir1.2-vte-3.91 \
                libvte-2.91-gtk4-dev \
                policykit-1 \
                gnome-icon-theme \
                wget
            ;;
        dnf)
            dnf install -y \
                python3 \
                python3-gobject \
                gtk4 \
                libadwaita \
                vte291-gtk4 \
                polkit \
                gnome-icon-theme \
                wget
            ;;
        pacman)
            pacman -Syu --noconfirm \
                python \
                python-gobject \
                gtk4 \
                libadwaita \
                vte4 \
                polkit \
                gnome-icon-theme-extras \
                wget
            ;;
        *)
            echo -e "${RED}⚠️  Package manager not detected.${RESET}"
            echo "Please install manually: python3, PyGObject, GTK4, libadwaita, VTE (gtk4), polkit"
            ;;
    esac
    echo -e "${GREEN}✓ Dépendances installées${RESET}"
fi
echo ""

# ═══════════════════════════════════════════
# STEP 2: Download & install files
# ═══════════════════════════════════════════
echo -e "${ORANGE}[2/4]${WHITE} Téléchargement des fichiers depuis GitHub...${RESET}"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/scripts"
mkdir -p "$INSTALL_DIR/icons"

# ─── Check if files exist locally (for developers / offline install) ───
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Download or copy GUI
# Priorité : GitHub (toujours à jour) → local (fallback hors-ligne)
echo -e "   ${WHITE}↓${RESET} Téléchargement de easymonerod_gui.py..."
if download "$GUI_URL" "$INSTALL_DIR/easymonerod_gui.py" 2>/dev/null; then
    echo -e "   ${GREEN}✓${RESET} easymonerod_gui.py (GitHub)"
elif [ -f "$SCRIPT_DIR/easymonerod_gui.py" ]; then
    echo -e "   ${ORANGE}~${RESET} GitHub inaccessible, utilisation de la version locale"
    cp "$SCRIPT_DIR/easymonerod_gui.py" "$INSTALL_DIR/easymonerod_gui.py"
else
    echo -e "   ${RED}⚠️  Impossible de récupérer easymonerod_gui.py${RESET}"
    exit 1
fi

# Download or copy easynode_linux.sh
# Priorité : GitHub (toujours à jour) → local (fallback hors-ligne)
echo -e "   ${WHITE}↓${RESET} Téléchargement de easynode_linux.sh..."
if download "$SCRIPT_URL" "$INSTALL_DIR/scripts/easynode_linux.sh" 2>/dev/null; then
    echo -e "   ${GREEN}✓${RESET} easynode_linux.sh (GitHub)"
elif [ -f "$SCRIPT_DIR/easynode_linux.sh" ]; then
    echo -e "   ${ORANGE}~${RESET} GitHub inaccessible, utilisation de la version locale"
    cp "$SCRIPT_DIR/easynode_linux.sh" "$INSTALL_DIR/scripts/easynode_linux.sh"
else
    echo -e "   ${RED}⚠️  Impossible de récupérer easynode_linux.sh${RESET}"
    exit 1
fi

# Fonction de téléchargement image avec fallbacks
download_asset() {
    local url="$1"
    local dest="$2"
    local filename="$(basename $dest)"
    local local_copy="$SCRIPT_DIR/$(basename $dest)"

    echo -e "   ${WHITE}↓${RESET} Téléchargement de $filename..."
    if download "$url" "$dest" 2>/dev/null; then
        echo -e "   ${GREEN}✓${RESET} $filename (GitHub)"
    elif [ -f "$local_copy" ]; then
        cp "$local_copy" "$dest"
        echo -e "   ${GREEN}✓${RESET} $filename (local)"
    elif [ -f "$dest" ]; then
        echo -e "   ${GREEN}✓${RESET} $filename (déjà installé)"
    else
        echo -e "   ${ORANGE}~${RESET} $filename non disponible (optionnel)"
    fi
}

download_asset "$LOGO_URL"   "$INSTALL_DIR/icons/logo2.png"
download_asset "$GIF_URL"    "$INSTALL_DIR/icons/xxmr.gif"
download_asset "$QRCODE_URL" "$INSTALL_DIR/icons/qrcode1.png"

# Install icon to system locations
if [ -f "$INSTALL_DIR/icons/logo2.png" ]; then
    mkdir -p /usr/share/icons/hicolor/128x128/apps
    mkdir -p /usr/share/icons/hicolor/256x256/apps
    cp "$INSTALL_DIR/icons/logo2.png" /usr/share/icons/hicolor/128x128/apps/easymonerod.png
    cp "$INSTALL_DIR/icons/logo2.png" /usr/share/icons/hicolor/256x256/apps/easymonerod.png
    gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true
fi

# Fix permissions
chmod -R 755 "$INSTALL_DIR"
chmod 644 "$INSTALL_DIR/icons/"* 2>/dev/null || true
chmod 755 "$INSTALL_DIR/easymonerod_gui.py"
chmod 755 "$INSTALL_DIR/scripts/easynode_linux.sh"

echo -e "${GREEN}✓ Fichiers installés dans $INSTALL_DIR${RESET}"
echo ""

# ═══════════════════════════════════════════
# STEP 3: Create launcher & desktop entry
# ═══════════════════════════════════════════
echo -e "${ORANGE}[3/4]${WHITE} Création du lanceur...${RESET}"

tee "$BIN_LINK" > /dev/null << 'LAUNCHER'
#!/bin/bash
cd /opt/easymonerod-gui
exec python3 /opt/easymonerod-gui/easymonerod_gui.py "$@"
LAUNCHER
chmod +x "$BIN_LINK"

# Desktop file
if [ -f "/usr/share/icons/hicolor/128x128/apps/easymonerod.png" ]; then
    ICON_PATH="easymonerod"
else
    ICON_PATH="network-server"
fi

tee /usr/share/applications/easymonerod-gui.desktop > /dev/null << DESKTOP
[Desktop Entry]
Name=EasyMonerod
Comment=Easy Monero Node Installer - GUI
Comment[fr]=Installation facile d'un nœud Monero - Interface graphique
Exec=easymonerod-gui
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Network;P2P;System;
Keywords=monero;node;blockchain;crypto;privacy;
StartupNotify=true
DESKTOP

echo -e "${GREEN}✓ Lanceur créé${RESET}"
echo ""

# ═══════════════════════════════════════════
# STEP 4: Polkit policy
# ═══════════════════════════════════════════
echo -e "${ORANGE}[4/4]${WHITE} Configuration des permissions (polkit)...${RESET}"

tee /usr/share/polkit-1/actions/org.easymonerod.gui.policy > /dev/null << 'POLKIT'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
 "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">
<policyconfig>
  <action id="org.easymonerod.gui.run">
    <description>Run EasyMonerod system commands</description>
    <description xml:lang="fr">Exécuter les commandes système EasyMonerod</description>
    <message>Authentication is required to configure your Monero node</message>
    <message xml:lang="fr">L'authentification est requise pour configurer votre nœud Monero</message>
    <icon_name>network-server</icon_name>
    <defaults>
      <allow_any>auth_admin_keep</allow_any>
      <allow_inactive>auth_admin_keep</allow_inactive>
      <allow_active>auth_admin_keep</allow_active>
    </defaults>
  </action>
</policyconfig>
POLKIT

# Polkit rule: remember authorization for 15 minutes for pkexec bash
mkdir -p /etc/polkit-1/localauthority/50-local.d
tee /etc/polkit-1/localauthority/50-local.d/easymonerod.pkla > /dev/null << 'PKLA'
[EasyMonerod GUI - keep auth]
Identity=unix-user:*
Action=org.freedesktop.policykit.exec
ResultAny=auth_admin_keep
ResultInactive=auth_admin_keep
ResultActive=auth_admin_keep
PKLA

# Also try the newer rules.d format for modern polkit
mkdir -p /etc/polkit-1/rules.d
tee /etc/polkit-1/rules.d/49-easymonerod.rules > /dev/null << 'RULES'
// EasyMonerod GUI: retain admin authorization for the session
polkit.addRule(function(action, subject) {
    if (action.id == "org.freedesktop.policykit.exec" &&
        subject.isInGroup("sudo")) {
        return polkit.Result.AUTH_ADMIN_KEEP;
    }
});
RULES

echo -e "${GREEN}✓ Permissions configurées${RESET}"
echo ""

# ═══════════════════════════════════════════
# DONE
# ═══════════════════════════════════════════
echo -e "${ORANGE}═══════════════════════════════════════════${RESET}"
if [ "$IS_UPDATE" = true ]; then
    echo -e "${GREEN}✅ Mise à jour terminée !${RESET}"
else
    echo -e "${GREEN}✅ Installation terminée !${RESET}"
fi
echo -e "${ORANGE}═══════════════════════════════════════════${RESET}"
echo ""
echo -e "${WHITE}Pour lancer EasyMonerod GUI :${RESET}"
echo -e "  ${ORANGE}•${WHITE} Depuis le terminal : ${GREEN}easymonerod-gui${RESET}"
echo -e "  ${ORANGE}•${WHITE} Depuis le menu Applications : cherchez ${GREEN}EasyMonerod${RESET}"
echo ""
if [ "$IS_UPDATE" = false ]; then
    echo -e "${WHITE}Pour désinstaller :${RESET}"
    echo -e "  ${ORANGE}•${WHITE} sudo rm -rf /opt/easymonerod-gui${RESET}"
    echo -e "  ${ORANGE}•${WHITE} sudo rm /usr/local/bin/easymonerod-gui${RESET}"
    echo -e "  ${ORANGE}•${WHITE} sudo rm /usr/share/applications/easymonerod-gui.desktop${RESET}"
    echo ""
fi
echo -e "${ORANGE}🔒 PRIVACY MATTERS 🔒${RESET}"
echo ""
