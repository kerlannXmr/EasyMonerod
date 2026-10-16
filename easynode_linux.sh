#!/bin/bash

declare -A COLORS=(
    
    ["PRIMARY"]='\033[38;5;255m'    
    ["SUCCESS"]='\033[38;5;71m'     
    ["MONERO"]='\033[38;5;208m'     
    ["WARNING"]='\033[38;5;184m'    
    ["ERROR"]='\033[38;5;167m'      
    ["INFO"]='\033[38;5;74m'        
    ["BG"]='\033[48;5;16m'         
    ["GRIS"]='\033[38;5;245m'        
    
)


draw_banner() {
    tput sc
    tput cup 0 0
    echo -e "\033[38;5;208m"
    echo "  *     *   ***   *   * ***** ****   ***   "
    echo "  **   **  *   *  **  * *     *   * *   *  "
    echo "  * * * * *     * * * * ****  ****  *   *  "
    echo "  *  *  * *     * *  ** *     * *   *   *  "
    echo "  *     *  *   *  *   * *     *  *  *   *  "
    echo "  *     *   ***   *   * ***** *   *  ***   "
    echo "  ═══════════ ▌EASYNODE▐ ═══════════linux"
   
    echo -e "${COLORS[RESET]}"
    tput rc
}

USERNAME=""
LANG_CHOICE=""
BLOCKCHAIN_TYPE=""
MONERO_VERSION="0.18.5.4"

print_styled() {
    local style=$1
    local message=$2
    echo -e "${COLORS[$style]}${message}${COLORS[RESET]}"
}
info() {
    print_styled "INFO" "ℹ $1"
}

error() {
    print_styled "ERROR" "✖ $1"
}

warning() {
    print_styled "WARNING" "⚠ $1"
}

success() {
    print_styled "SUCCESS" "✓ $1"
}


print_header() {
    local message=$1
    local length=${#message}
    local total_width=37    
    local line="═════════════════════════════════════════"
    local padding=$(( (total_width - length) / 2 ))
    local spaces=$(printf '%*s' $padding '')
    echo
    print_styled "MONERO" "$line"
    print_styled "HEADER" "${spaces}${message}"
    print_styled "MONERO" "$line"
    echo
}

setup_terminal() {
    echo -e "${COLORS[BG]}"
    clear
    printf '\033]11;#1a1a1a\007'
    draw_banner
}

select_language() {
    clear
    draw_banner
    echo -e "\n\n\n\n\n\n\n\n"  
    print_header "LANGUAGE SELECTION"
                  
    while true; do
        print_styled "PRIMARY" "1) Français"
        print_styled "PRIMARY" "2) English"
        echo -n "$(print_styled "MONERO" "Choose/Choisissez (1-2): ")"    
            
        read -r lang_choice
        case $lang_choice in
            1) LANG_CHOICE="FR"; break ;;
            2) LANG_CHOICE="EN"; break ;;
            *) error "Invalid choice / Choix invalide" ;;    
        esac
      done
}

get_message() {
    local fr_msg=$1
    local en_msg=$2
    if [ "$LANG_CHOICE" = "FR" ]; then
        echo "$fr_msg"
    else
        echo "$en_msg"
    fi
}
 Manuel() {
    clear
    setup_terminal
    echo -e "\n\n\n\n\n\n\n\n"  
    print_header "$(get_message "GUIDE" "HOW TO")"
   
    print_styled "MONERO" "$(get_message "Pour une installation complète, suivez ces étapes dans l'ordre:" "For a complete installation, follow these steps in order:")"
    echo
         print_styled "SUCCESS" "$(get_message "  1️⃣ ➜ 2️⃣ ➜ 3️⃣ ➜ 4️⃣ ➜ 5️⃣." "  1️⃣ ➜ 2️⃣ ➜ 3️⃣ ➜ 4️⃣ ➜ 5️⃣.")"
   echo
   print_styled "SUCCESS" "$(get_message "  Puis au choix :" "  Then your choice :")"
   echo
   print_styled "SUCCESS" "$(get_message "  ▶️ Disque interne : étape 8️⃣." "  ▶️ Internal disk : step 8️⃣.")"
   echo
   print_styled "SUCCESS" "$(get_message "  ▶️ Disque externe : étape 6️⃣ puis 8️⃣." "  ▶️ External disk : step 6️⃣ then 8️⃣.")"
   echo
   print_header "$(get_message "AUTRES" "OTHER")"
   print_styled "GRIS" "$(get_message "  ➡️ Étape 8 : Démarrer le nœud et configurer l'exclusion des ⛔ 'IP bannis '." "  ➡️ Step 8: Start the Node and introduce the exclusion of the ⛔ 'listed IP bans'.")"
   echo
   print_styled "GRIS" "$(get_message "  ➡️ Étape 7 : Démonter la blockchain du disque externe," "  ➡️ Step 7 : Is used to unmount the blockchain from the external disk,")"
   print_styled "GRIS" "$(get_message "  ↳ Pour revenir au disque interne : passez à l'étape 8." "  ↳ Return on internal disk: then step 8.")"
   echo
   print_styled "GRIS" "$(get_message "  ➡️ Étape 4 : Sert aussi pour le DEBUG du chemin d'amorçage du disque interne." "  ➡️ Step 4 : Also serves as DEBUG of the boot path to internal disk.")"
   echo
   print_styled "PRIMARY" "$(get_message "   CTRL+C 1 seule fois pour arreter la Blockchain et revenir au menu." "  -CTRL+C 1 time only to stop the Blockchain and return to the menu.")"
   echo
   print_styled "WARNING" "$(get_message "⚠️ Important: REDIRIGER le port 22 et 18080 de votre Box internet" "⚠️ Important: REDIRECT port 22 and 18080 from your internet router")"
   print_styled "WARNING" "$(get_message "  vers l'adresse 'ip local' de votre PC" "  to your 'local ip' of your PC")"
   echo
    read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour revenir au menu..." "Press Enter to return to menu...")")"
}
select_blockchain_type() {
    print_header "$(get_message "TYPE DE BLOCKCHAIN" "BLOCKCHAIN TYPE")"
    
        print_styled "PRIMARY" "$(get_message "1) Complète 220 Go" "1) Complete 220 Go")"
        print_styled "PRIMARY" "$(get_message "2) Prune 90 Go" "2) Pruned 90 Go")"
        echo -n "$(print_styled "INFO" "$(get_message "Choix (1-2): " "Choice (1-2): ")")"
        read -r choice
        case $choice in
            1) BLOCKCHAIN_TYPE="complete"; return 0  ;;
            2) BLOCKCHAIN_TYPE="pruned"; return 0 ;;
            *) 
            error "$(get_message "Choix invalide" "Invalid choice")" 
            return 1;;
        esac
    
}

update_system() {
    print_header "$(get_message "MISE À JOUR DU SYSTÈME" "SYSTEM UPDATE")"
    
    info "$(get_message "Mise à jour initiale du système..." "Initial system update...")"
    sudo apt update && sudo apt upgrade -y

    info "$(get_message "Installation des outils système essentiels..." "Installing essential system tools...")"
    sudo apt install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        wget \
        gnupg \
        dirmngr

    info "$(get_message "Installation des outils de compression..." "Installing compression tools...")"
    sudo apt install -y \
        bzip2 \
        tar

    info "$(get_message "Installation des outils réseau..." "Installing network tools...")"
    sudo apt install -y \
        net-tools \
        openssh-server \
        ufw \
        fail2ban


    info "$(get_message "Configuration de SSH..." "Configuring SSH...")"
    sudo systemctl enable ssh
    sudo systemctl start ssh
    
if [ ! -f /etc/ssh/sshd_config.backup ]; then
    sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
fi

sudo sed -i 's/MaxAuthTries 6/MaxAuthTries 3/' /etc/ssh/sshd_config

if ! grep -q "PermitRootLogin no" /etc/ssh/sshd_config; then
    echo "PermitRootLogin no" | sudo tee -a /etc/ssh/sshd_config
fi



    info "$(get_message "Configuration du pare-feu..." "Configuring firewall...")"
    
ufw_status=$(sudo ufw status)

if [[ "$ufw_status" == *"Status: inactive"* ]]; then
    sudo ufw --force enable
fi

sudo ufw allow 22/tcp comment "SSH"           
sudo ufw allow 80/tcp comment "HTTP"
sudo ufw allow 443/tcp comment "HTTPS"
sudo ufw allow 9050/tcp comment "TOR SOCKS"
sudo ufw allow 18080/tcp comment "Monero P2P"
sudo ufw allow 18081/tcp comment "Monero RPC"
sudo ufw allow 18083/tcp comment "Monero ZMQ"


   

    info "$(get_message "Configuration de fail2ban..." "Configuring fail2ban...")"
    sudo systemctl enable fail2ban
    sudo systemctl start fail2ban

    info "$(get_message "Nettoyage du système..." "System cleanup...")"
    sudo apt autoremove -y
    sudo apt clean

    success "$(get_message "Mise à jour terminée" "Update completed")"
    read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..." "Press Enter to continue...")")"
}

HOSTNAME=$(hostname)
IP_ADDRESS=$(hostname -I | cut -d' ' -f1)
SYSTEM_INFO=$(uname -s)" "$(uname -r)

echo -e "\e[0;33;38;5;208m  *     *   ***   *   * ***** ****   ***   
  **   **  *   *  **  * *     *   * *   *  
  * * * * *     * * * * ****  ****  *   *  
  *  *  * *     * *  ** *     * *   *   *  
  *     *  *   *  *   * *     *  *  *   *  
  *     *   ***   *   * ***** *   *  ***   
  ═════════════ ▌EASYNODE▐ ═════════Linux\e[0m

\e[0;33;38;5;208m    ▐ EASYNODE               EASYNODE▐ \e[0m

\e[1;34mNode Status:\e[0m
- Hostname: $HOSTNAME
- IP Address: $IP_ADDRESS
- Monero Version: $MONERO_VERSION
- System: $SYSTEM_INFO

\e[1;33mUseful Commands:\e[0m
- monerod --help : Show Monero daemon help
- monero-wallet-cli --help : Show wallet CLI help

\e[1;31mImportant:\e[0m
- Start monero: monerod
- Stop  monero: CTRL+C
- Check status: monerod status" | sudo tee /etc/motd > /dev/null
ask_username() {
clear
    setup_terminal
    echo -e "\n\n\n\n\n\n\n\n"  

    print_header "$(get_message "CONFIGURATION UTILISATEUR" "USER CONFIGURATION")"
    
    local current_user=""
    if [ -n "$SUDO_USER" ]; then
        current_user="$SUDO_USER"
    elif [ -n "$USER" ]; then
        current_user="$USER"
    else
        current_user=$(whoami)
    fi
    
    echo -e "$(get_message "Utilisateur détecté: " "Detected user: ")${COLORS[SUCCESS]}${current_user}${COLORS[RESET]}"
    echo
    
    print_styled "INFO" "$(get_message "Appuyez sur Entrée pour confirmer ou tapez un autre nom d'utilisateur: " "Press Enter to confirm or type another username: ")"
    read -r input_username
    
    if [ -z "$input_username" ]; then
        input_username="$current_user"
        USERNAME="$input_username"
        return 0
    fi
    
    if ! id "$input_username" &>/dev/null; then
        error "$(get_message "L'utilisateur n'existe pas" "User does not exist")"
        return 1
    fi
    
    USERNAME="$input_username"
    return 0
}

verify_monero_gpg() {
    local MONERO_FILE="$1"
    local MONERO_VERSION="$2"
    
    info "$(get_message "🔍 Vérification complète des binaires Monero..." "🔍 Complete Monero binary verification...")"
    
    info "$(get_message "📋 Vérifications préliminaires..." "📋 Preliminary checks...")"
    
    local FILE_SIZE=$(stat -c%s "$MONERO_FILE" 2>/dev/null || stat -f%z "$MONERO_FILE" 2>/dev/null)
    if [ -z "$FILE_SIZE" ]; then
        error "$(get_message "Impossible de lire la taille du fichier" "Cannot read file size")"
        return 1
    fi
    
    info "$(get_message "   Taille: $(( FILE_SIZE / 1024 / 1024 )) MB" "   Size: $(( FILE_SIZE / 1024 / 1024 )) MB")"
    
    if [ "$FILE_SIZE" -lt 50000000 ]; then
        error "$(get_message "Fichier trop petit (${FILE_SIZE} bytes) - téléchargement incomplet" "File too small (${FILE_SIZE} bytes) - incomplete download")"
        return 1
    fi
    
    if [ "$FILE_SIZE" -gt 200000000 ]; then
        warning "$(get_message "Fichier très volumineux ($(( FILE_SIZE / 1024 / 1024 )) MB)" "Very large file ($(( FILE_SIZE / 1024 / 1024 )) MB)")"
    fi
    
    if command -v file >/dev/null 2>&1; then
        local file_type=$(file "$MONERO_FILE")
        if echo "$file_type" | grep -q "bzip2"; then
            success "$(get_message "   ✅ Format bzip2 correct" "   ✅ Correct bzip2 format")"
        else
            error "$(get_message "Format de fichier inattendu: $file_type" "Unexpected file format: $file_type")"
            return 1
        fi
    fi
    
    if tar -tjf "$MONERO_FILE" >/dev/null 2>&1; then
        success "$(get_message "   ✅ Archive valide et lisible" "   ✅ Valid and readable archive")"
    else
        error "$(get_message "Archive corrompue ou invalide" "Corrupted or invalid archive")"
        return 1
    fi
    
    local monero_files=$(tar -tjf "$MONERO_FILE" 2>/dev/null | grep -E "(monerod|monero-wallet-cli)" | wc -l)
    if [ "$monero_files" -ge 2 ]; then
        success "$(get_message "   ✅ Fichiers Monero détectés ($monero_files fichiers)" "   ✅ Monero files detected ($monero_files files)")"
    else
        warning "$(get_message "   ⚠️ Fichiers Monero non clairement détectés" "   ⚠️ Monero files not clearly detected")"
    fi
    
    # User-agent complet Chrome pour contourner Cloudflare/anti-bot de getmonero.org
    local UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    # Fonction de téléchargement avec fallback curl
    _dl() {
        local url="$1" dest="$2"
        wget -q --user-agent="$UA" "$url" -O "$dest" 2>/dev/null || \
        curl -sL --user-agent "$UA" "$url" -o "$dest" 2>/dev/null
    }

    info "$(get_message "🔐 Vérification cryptographique..." "🔐 Cryptographic verification...")"

    if ! _dl "https://www.getmonero.org/downloads/hashes.txt" hashes.txt; then
        error "$(get_message "Échec téléchargement hashes.txt depuis getmonero.org" "Failed to download hashes.txt from getmonero.org")"
        return 1
    fi
    
    local expected_hash=$(grep "monero-linux-x64-v${MONERO_VERSION}.tar.bz2" hashes.txt | awk '{print $1}')
    if [ -z "$expected_hash" ]; then
        error "$(get_message "Hash SHA256 non trouvé pour la version $MONERO_VERSION" "SHA256 hash not found for version $MONERO_VERSION")"
        rm -f hashes.txt
        return 1
    fi
    
    local actual_hash=$(sha256sum "$MONERO_FILE" | awk '{print $1}')
    if [ "$expected_hash" != "$actual_hash" ]; then
        error "$(get_message "❌ HASH SHA256 INVALIDE - FICHIER SUSPECT" "❌ INVALID SHA256 HASH - SUSPICIOUS FILE")"
        error "$(get_message "   Attendu: $expected_hash" "   Expected: $expected_hash")"
        error "$(get_message "   Obtenu:  $actual_hash" "   Got:      $actual_hash")"
        rm -f hashes.txt
        return 1
    fi
    
    success "$(get_message "✅ Hash SHA256 vérifié contre getmonero.org" "✅ SHA256 hash verified against getmonero.org")"
    
    local signer=""
    local fingerprint=""
    local sig_date=""
    local key_date=""

    # ── Signature GPG obligatoire ──────────────────────────────────────
    # Clés acceptées pour signer les binaires Monero :
    #  1) les empreintes fixes ci-dessous (binaryfate, luigi1111) ;
    #  2) automatiquement, toute clé publiée dans le dépôt officiel Monero sur
    #     GitHub (monero-project/monero/utils/gpg_keys). Un changement de
    #     signataire est ainsi pris en compte sans mise à jour d'EasyMonerod.
    local TRUSTED_FPRS="${MONERO_TRUSTED_FPRS:-81AC591FE9C4B65C5806AFC3F0AF4D462A0BDF92 8777AB8F778EE89487A2F8E7F4ACA0183641E010}"
    local REPO_FPRS=""
    local GPG_KEYS_API="${MONERO_GPG_KEYS_API:-https://api.github.com/repos/monero-project/monero/contents/utils/gpg_keys}"

    info "$(get_message "🗝️ Vérification signature GPG..." "🗝️ Verifying GPG signature...")"

    if ! command -v gpg >/dev/null 2>&1; then
        error "$(get_message "gpg introuvable - installation annulée" "gpg not found - installation aborted")"
        rm -f hashes.txt
        return 1
    fi

    # Méthode officielle Monero : hashes.txt porte sa propre signature
    # (« PGP SIGNED MESSAGE »). hashes.txt.sig n'est qu'un secours : il peut
    # être en retard sur hashes.txt juste après une nouvelle version.
    local CLEARSIGNED=0
    grep -q -- "-----BEGIN PGP SIGNED MESSAGE-----" hashes.txt && CLEARSIGNED=1
    rm -f hashes.txt.sig
    _dl "https://www.getmonero.org/downloads/hashes.txt.sig" hashes.txt.sig
    [ -s hashes.txt.sig ] || rm -f hashes.txt.sig
    if [ "$CLEARSIGNED" -ne 1 ] && [ ! -f hashes.txt.sig ]; then
        error "$(get_message "hashes.txt n'est pas signé et hashes.txt.sig est introuvable - installation annulée" "hashes.txt is not signed and hashes.txt.sig is missing - installation aborted")"
        rm -f hashes.txt
        return 1
    fi

    # Vérifie la signature ; le contenu réellement signé va dans hashes_signed.txt
    _gpg_check() {
        rm -f hashes_signed.txt
        if [ "$CLEARSIGNED" -eq 1 ] && [ "$1" != "sig" ]; then
            GNUPGHOME="$GPG_TMP" LANG=C gpg --batch --status-fd 1 --output hashes_signed.txt --decrypt hashes.txt 2>/dev/null
        elif [ -f hashes.txt.sig ]; then
            GNUPGHOME="$GPG_TMP" LANG=C gpg --batch --status-fd 1 --verify hashes.txt.sig hashes.txt 2>/dev/null \
                && cp hashes.txt hashes_signed.txt
        fi
    }

    # Trousseau temporaire : ne touche pas au trousseau de l'utilisateur
    local GPG_TMP
    GPG_TMP=$(mktemp -d)
    chmod 700 "$GPG_TMP"

    if _dl "https://raw.githubusercontent.com/monero-project/monero/master/utils/gpg_keys/binaryfate.asc" binaryfate.asc; then
        GNUPGHOME="$GPG_TMP" gpg --batch --quiet --import binaryfate.asc >/dev/null 2>&1
    fi

    # Clés publiées dans le dépôt officiel Monero (liste via l'API GitHub)
    local key_url key_tmp
    key_tmp=$(mktemp)
    if _dl "$GPG_KEYS_API" monero_gpg_keys.json; then
        for key_url in $(grep -o '"download_url": *"[^"]*\.asc"' monero_gpg_keys.json | sed 's/.*"\(https[^"]*\)"/\1/'); do
            case "$key_url" in
                https://raw.githubusercontent.com/monero-project/monero/*) ;;
                *) continue ;;
            esac
            if _dl "$key_url" "$key_tmp"; then
                REPO_FPRS="$REPO_FPRS $(LANG=C gpg --batch --with-colons --import-options show-only --import "$key_tmp" 2>/dev/null \
                    | awk -F: '$1=="pub"{p=1; next} p && $1=="fpr"{print $10; p=0}')"
                GNUPGHOME="$GPG_TMP" gpg --batch --quiet --import "$key_tmp" >/dev/null 2>&1
            fi
        done
    fi
    rm -f "$key_tmp" monero_gpg_keys.json
    if [ -n "${REPO_FPRS// /}" ]; then
        info "$(get_message "   Clés du dépôt officiel Monero chargées : $(echo $REPO_FPRS | wc -w)" "   Official Monero repository keys loaded: $(echo $REPO_FPRS | wc -w)")"
    else
        warning "$(get_message "   Dépôt Monero injoignable : seules les clés intégrées sont acceptées" "   Monero repository unreachable: only built-in keys are accepted")"
    fi
    # Clé absente : on la récupère sur un serveur de clés. Sans risque, car
    # seule une empreinte présente dans TRUSTED_FPRS est acceptée plus bas.
    local key_id
    key_id=$(_gpg_check | awk '$2=="NO_PUBKEY"{print $3; exit}')
    if [ -n "$key_id" ]; then
        GNUPGHOME="$GPG_TMP" gpg --batch --quiet --keyserver hkps://keys.openpgp.org --recv-keys "$key_id" >/dev/null 2>&1 || \
        GNUPGHOME="$GPG_TMP" gpg --batch --quiet --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys "$key_id" >/dev/null 2>&1
    fi

    local status_out
    status_out=$(_gpg_check)
    if ! echo "$status_out" | grep -q " VALIDSIG " && [ "$CLEARSIGNED" -eq 1 ] && [ -f hashes.txt.sig ]; then
        status_out=$(_gpg_check sig)
    fi
    signer=$(echo "$status_out" | awk '$2=="GOODSIG"{$1=$2=$3=""; sub(/^ +/,""); print; exit}')
    # VALIDSIG : $3 = empreinte de la (sous-)clé de signature, $NF = empreinte de la clé principale
    local sig_fpr primary_fpr
    sig_fpr=$(echo "$status_out" | awk '$2=="VALIDSIG"{print $3; exit}')
    primary_fpr=$(echo "$status_out" | awk '$2=="VALIDSIG"{print $NF; exit}')
    sig_date=$(echo "$status_out" | awk '$2=="VALIDSIG"{print $4; exit}')
    rm -rf "$GPG_TMP"

    local trusted_ok=0 f
    for f in $TRUSTED_FPRS; do
        if [ -n "$primary_fpr" ] && [ "$primary_fpr" = "$f" ]; then trusted_ok=1; fi
        if [ -n "$sig_fpr" ] && [ "$sig_fpr" = "$f" ]; then trusted_ok=1; fi
    done
    if [ "$trusted_ok" -ne 1 ]; then
        for f in $REPO_FPRS; do
            if [ -n "$primary_fpr" ] && [ "$primary_fpr" = "$f" ]; then trusted_ok=2; fi
        done
    fi

    if [ -z "$sig_fpr" ]; then
        error "$(get_message "❌ SIGNATURE GPG INVALIDE OU NON VÉRIFIABLE - installation annulée" "❌ INVALID OR UNVERIFIABLE GPG SIGNATURE - installation aborted")"
        rm -f hashes.txt hashes.txt.sig hashes_signed.txt binaryfate.asc
        return 1
    fi
    if [ "$trusted_ok" -eq 0 ]; then
        error "$(get_message "❌ hashes.txt est signé par une clé NON RECONNUE - installation annulée" "❌ hashes.txt is signed by an UNRECOGNISED key - installation aborted")"
        error "$(get_message "   Clé : $primary_fpr ${signer:+($signer)}" "   Key: $primary_fpr ${signer:+($signer)}")"
        warning "$(get_message "   Cette clé n'est ni intégrée à EasyMonerod, ni publiée dans le dépôt officiel Monero." "   This key is neither built into EasyMonerod nor published in the official Monero repository.")"
        rm -f hashes.txt hashes.txt.sig hashes_signed.txt binaryfate.asc
        return 1
    fi

    if [ "$trusted_ok" -eq 2 ]; then
        warning "$(get_message "   ℹ️ Nouveau signataire, accepté car sa clé est publiée dans le dépôt officiel Monero" "   ℹ️ New signer, accepted because its key is published in the official Monero repository")"
    fi
    # Le hash doit figurer dans la partie SIGNÉE (pas seulement dans le fichier brut)
    local signed_hash
    signed_hash=$(grep "monero-linux-x64-v${MONERO_VERSION}.tar.bz2" hashes_signed.txt 2>/dev/null | awk '{print $1}' | head -n1)
    if [ -z "$signed_hash" ] || [ "$signed_hash" != "$actual_hash" ]; then
        error "$(get_message "❌ Le hash de l'archive ne figure pas dans la partie signée de hashes.txt - installation annulée" "❌ The archive hash is not in the signed part of hashes.txt - installation aborted")"
        rm -f hashes.txt hashes.txt.sig hashes_signed.txt binaryfate.asc
        return 1
    fi

    fingerprint="$primary_fpr"
    [ -n "$sig_date" ] && sig_date=$(date -d "@$sig_date" 2>/dev/null || echo "$sig_date")
    success "$(get_message "🎉 SIGNATURE GPG VÉRIFIÉE !" "🎉 GPG SIGNATURE VERIFIED !")"
    
    echo
    success "$(get_message "🎉 FICHIER MONERO AUTHENTIFIÉ AVEC SUCCÈS" "🎉 MONERO FILE SUCCESSFULLY AUTHENTICATED")"
    echo
    success "$(get_message "🔐 VÉRIFICATIONS CRYPTOGRAPHIQUES :" "🔐 CRYPTOGRAPHIC VERIFICATIONS:")"
    success "$(get_message "   ✓ Hash SHA256: $expected_hash" "   ✓ SHA256 Hash: $expected_hash")"
    
    if [ -n "$signer" ]; then
        success "$(get_message "   ✓ Signature GPG: $signer" "   ✓ GPG Signature: $signer")"
        if [ -n "$sig_date" ]; then
            success "$(get_message "   ✓ Signé le: $sig_date" "   ✓ Signed on: $sig_date")"
        fi
        if [ -n "$fingerprint" ]; then
            success "$(get_message "   ✓ Empreinte: $fingerprint" "   ✓ Fingerprint: $fingerprint")"
        fi
        if [ -n "$key_date" ]; then
            success "$(get_message "   ✓ Clé créée: $key_date" "   ✓ Key created: $key_date")"
        fi
    fi
    
    echo
    success "$(get_message "🛡️ GARANTIES DE SÉCURITÉ :" "🛡️ SECURITY GUARANTEES:")"
    success "$(get_message "   ✓ Intégrité physique vérifiée" "   ✓ Physical integrity verified")"
    success "$(get_message "   ✓ Authenticité cryptographique vérifiée" "   ✓ Cryptographic authenticity verified")" 
    success "$(get_message "   ✓ Contenu Monero confirmé" "   ✓ Monero content confirmed")"
    
    rm -f hashes.txt hashes.txt.sig hashes_signed.txt binaryfate.asc
    
    return 0
}


install_monero_cli() {
    if [ -z "$USERNAME" ]; then
        error "$(get_message "Nom d'utilisateur non défini" "Username not defined")"
        return 1
    fi

    print_header "$(get_message "INSTALLATION DE MONERO" "MONERO INSTALLATION")"
    
    if ! command -v gpg &> /dev/null; then
        info "$(get_message "Installation de GPG..." "Installing GPG...")"
        sudo apt update && sudo apt install -y gnupg
    fi
    
    mkdir -p ~/monero_install
    cd ~/monero_install || exit
    
    local MONERO_FILE="monero-linux-x64-v${MONERO_VERSION}.tar.bz2"
    
    info "$(get_message "Téléchargement de Monero..." "Downloading Monero...")"
    if wget --tries=3 "https://downloads.getmonero.org/cli/${MONERO_FILE}"; then
        success "$(get_message "Téléchargement terminé" "Download completed")"
        
        local FILE_SIZE=$(stat -f%z "$MONERO_FILE" 2>/dev/null || stat -c%s "$MONERO_FILE")
        if [ "$FILE_SIZE" -lt 1000000 ]; then  
            error "$(get_message "Fichier téléchargé incomplet" "Downloaded file is incomplete")"
            rm -f "$MONERO_FILE"
            return 1
        fi
        
        if ! verify_monero_gpg "$MONERO_FILE" "$MONERO_VERSION"; then
            error "$(get_message "Échec de la vérification GPG" "GPG verification failed")"
            rm -f "$MONERO_FILE" "${MONERO_FILE}.asc"
            return 1
        fi
        
        info "$(get_message "Extraction des fichiers..." "Extracting files...")"
        if tar xvjf "$MONERO_FILE"; then
            success "$(get_message "Extraction terminée" "Extraction completed")"
        else
            error "$(get_message "Échec de l'extraction - Tentative de re-téléchargement" "Extraction failed - Trying to download again")"
            rm -f "$MONERO_FILE" "${MONERO_FILE}.asc"
            if wget --tries=3 "https://downloads.getmonero.org/cli/${MONERO_FILE}" && \
               verify_monero_gpg "$MONERO_FILE" "$MONERO_VERSION" && \
               tar xvjf "$MONERO_FILE"; then
                success "$(get_message "Second essai réussi" "Second attempt successful")"
            else
                error "$(get_message "Installation impossible" "Installation impossible")"
                return 1
            fi
        fi
    else
        error "$(get_message "Échec du téléchargement" "Download failed")"
        return 1
    fi

    sudo mkdir -p "/home/$USERNAME/monero"
    sudo cp -r "monero-x86_64-linux-gnu-v${MONERO_VERSION}"/* "/home/$USERNAME/monero/"
    echo "export PATH=\$PATH:/home/$USERNAME/monero" | sudo tee -a "/home/$USERNAME/.bashrc"

    sudo chown -R "$USERNAME:$USERNAME" "/home/$USERNAME/monero"
    sudo chmod -R 755 "/home/$USERNAME/monero"

    sudo mkdir -p "/home/$USERNAME/.bitmonero"
    sudo chown -R "$USERNAME:$USERNAME" "/home/$USERNAME/.bitmonero"
    sudo chmod -R 755 "/home/$USERNAME/.bitmonero"

    cd ~ || exit
    rm -rf ~/monero_install

    success "$(get_message "✅ Installation terminée avec vérification GPG dans /home/$USERNAME/monero" "✅ Installation completed with GPG verification in /home/$USERNAME/monero")"
    return 0
}


install_tor() {
    print_header "$(get_message "INSTALLATION DE TOR" "TOR INSTALLATION")"
    
    if ! command -v tor &> /dev/null; then
        info "$(get_message "Installation de Tor..." "Installing Tor...")"
        if sudo apt update && sudo apt install -y tor; then
            success "$(get_message "Installation de Tor terminée" "Tor installation completed")"
        else
            error "$(get_message "Échec de l'installation de Tor" "Tor installation failed")"
            return 1
        fi
    else
        info "$(get_message "Tor est déjà installé" "Tor is already installed")"
    fi

    if [ -f /etc/tor/torrc ]; then
        sudo cp /etc/tor/torrc /etc/tor/torrc.backup
    fi

  sudo bash -c 'cat > /etc/tor/torrc << EOL
SOCKSPort 9050
ControlPort 9051
HiddenServiceDir /var/lib/tor/ssh/
HiddenServicePort 22 127.0.0.1:22         
HiddenServiceDir /var/lib/tor/monero-service/
HiddenServicePort 18081 127.0.0.1:18081
EOL'

    if [ ! -d "/var/lib/tor/monero-service/" ]; then
        sudo mkdir -p /var/lib/tor/monero-service/
        sudo chown -R debian-tor:debian-tor /var/lib/tor/monero-service/
        sudo chmod 700 /var/lib/tor/monero-service/
    fi

    if [ ! -d "/var/lib/tor/ssh/" ]; then
        sudo mkdir -p /var/lib/tor/ssh/
        sudo chown -R debian-tor:debian-tor /var/lib/tor/ssh/
        sudo chmod 700 /var/lib/tor/ssh/
    fi

    info "$(get_message "Redémarrage de Tor..." "Restarting Tor...")"
    sudo systemctl restart tor

    info "$(get_message "Génération de l'adresse onion..." "Generating onion address...")"
    sleep 10

    if [ -f /var/lib/tor/monero-service/hostname ]; then
        ONION_ADDRESS=$(sudo cat /var/lib/tor/monero-service/hostname)
        success "$(get_message "Adresse onion: $ONION_ADDRESS" "Onion address: $ONION_ADDRESS")"
        echo "Monero Onion Address ($(date)): $ONION_ADDRESS" | sudo tee -a "/home/$USERNAME/monero_onion_address.txt"
        sudo chown "$USERNAME:$USERNAME" "/home/$USERNAME/monero_onion_address.txt"
        echo "-------------------->$(get_message "L'adresse TOR est sauvegardée dans le dossier /home" "The TOR address is saved in the folder /home")"
    else
        error "$(get_message "Échec de la génération de l'adresse onion" "Failed to generate onion address")"
    fi

    if [ -f /var/lib/tor/ssh/hostname ]; then
        SSH_ONION_ADDRESS=$(sudo cat /var/lib/tor/ssh/hostname)
        success "$(get_message "Adresse onion SSH: " "SSH onion address: ")$SSH_ONION_ADDRESS"
        echo "SSH Onion Address ($(date)): $SSH_ONION_ADDRESS" | sudo tee -a "/home/$USERNAME/ssh_onion_address.txt"
        sudo chown "$USERNAME:$USERNAME" "/home/$USERNAME/ssh_onion_address.txt"
        echo "-------------------->$(get_message "L'adresse SSH est sauvegardée dans le dossier /home" "The SSH address is saved in the folder /home")"
    else
        error "$(get_message "Échec de la génération de l'adresse onion SSH" "Failed to generate SSH onion address")"
    fi

    read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..." "Press Enter to continue...")")"
}



# ── Helper : génère rpc_easynode_pass.txt dans la bonne langue ──────────────
# Usage: write_rpc_pass_file "$USERNAME" "$RPC_USERNAME" "$RPC_PASSWORD" "$BLOCKCHAIN_PATH"
# Si RPC_USERNAME/PASSWORD vides → mode sans authentification
write_rpc_pass_file() {
    local user="$1"
    local rpc_user="$2"
    local rpc_pass="$3"
    local blockchain_path="${4:-/home/$user/.bitmonero}"
    local dest="/home/$user/rpc_easynode_pass.txt"

    if [ -n "$rpc_user" ] && [ -n "$rpc_pass" ]; then
        # Mode sécurisé avec mot de passe
        if [ "$LANG_CHOICE" = "FR" ]; then
            cat > "$dest" << EOL
=== IDENTIFICATION RPC MONERO (SÉCURISÉ) ===
Username: $rpc_user
Password: $rpc_pass
Date: $(date)
Blockchain: $blockchain_path
=====================================

📝 PROCÉDURE DE CONNEXION: (wallet externe)
1️⃣ Ouvrir le wallet
2️⃣ Aller dans Paramètres > Nœud
3️⃣ Sélectionner 'Nœud distant' ou 'Noeud local'
4️⃣ Adresse: [IP_DE_TOR_VOTRE_NOEUD] OU ip local:18081
5️⃣ Nom d'utilisateur: $rpc_user
6️⃣ Mot de passe: $rpc_pass

⚠️ IMPORTANT: Gardez ce fichier en sécurité !
EOL
        else
            cat > "$dest" << EOL
=== MONERO RPC CREDENTIALS (SECURED) ===
Username: $rpc_user
Password: $rpc_pass
Date: $(date)
Blockchain: $blockchain_path
=====================================

📝 LOGIN PROCEDURE: (external wallet)
1️⃣ Open the wallet 
2️⃣ Go to Settings > Node 
3️⃣ Select 'Remote Node' or 'Local Node' 
4️⃣ Address: [IP_DE_TOR_NODE] OR local ip:18081
5️⃣ Username: $rpc_user
6️⃣ Password: $rpc_pass

⚠️ IMPORTANT: Keep this file secure!
EOL
        fi
    else
        # Mode sans authentification
        if [ "$LANG_CHOICE" = "FR" ]; then
            cat > "$dest" << EOL
=== CONFIGURATION RPC MONERO (NON SÉCURISÉ) ===
Mode: Sans authentification
Date: $(date)
Blockchain: $blockchain_path
=====================================

📝 PROCÉDURE DE CONNEXION: (wallet externe)
1️⃣ Ouvrir le wallet
2️⃣ Aller dans Paramètres > Nœud
3️⃣ Sélectionner 'Nœud distant' ou 'Noeud local'
4️⃣ Adresse: [IP_DE_TOR_VOTRE_NOEUD] OU ip local:18081
5️⃣ Aucun mot de passe requis

⚠️ ATTENTION: Cette configuration est moins sécurisée
   mais plus simple pour un usage personnel local.
EOL
        else
            cat > "$dest" << EOL
=== MONERO RPC CONFIGURATION (UNSECURED) ===
Mode: No authentication
Date: $(date)
Blockchain: $blockchain_path
=====================================

📝 LOGIN PROCEDURE: (external wallet)
1️⃣ Open the wallet 
2️⃣ Go to Settings > Node 
3️⃣ Select 'Remote Node' or 'Local Node' 
4️⃣ Address: [IP_DE_TOR_NODE] OR local ip:18081
5️⃣ No password
⚠️ WARNING: This configuration is less secure
   but simpler for personal local use.
EOL
        fi
    fi

    sudo chown "$user:$user" "$dest"
    chmod 600 "$dest"
}
# ────────────────────────────────────────────────────────────────────────────

configure_monero() {
    if [ -z "$USERNAME" ]; then
        error "$(get_message "Nom d'utilisateur non défini" "Username not defined")"
        return 1
    fi

    print_header "$(get_message "CONFIGURATION DE MONERO" "MONERO CONFIGURATION")"
    
    CONFIG_FILE="/home/$USERNAME/.bitmonero/bitmonero.conf"
    mkdir -p "/home/$USERNAME/.bitmonero"

    cat > "$CONFIG_FILE" << EOL
no-igd=1
no-zmq=1
rpc-bind-ip=0.0.0.0
rpc-bind-port=18081
p2p-bind-port=18080
p2p-bind-ip=0.0.0.0
in-peers=32
out-peers=32
disable-dns-checkpoints=1
confirm-external-bind=1
restricted-rpc=0
data-dir=/home/$USERNAME/.bitmonero
EOL

    echo
    print_styled "WARNING" "$(get_message "🔐 CONFIGURATION DE LA SÉCURITÉ RPC" "🔐 RPC SECURITY CONFIGURATION")"
    echo
    print_styled "INFO" "$(get_message "Choisissez le mode de sécurisation de votre nœud :" "Choose your node security mode:")"
    echo
    print_styled "PRIMARY" "$(get_message "1) AVEC mot de passe (Recommandé - Plus sécurisé)" "1) WITH password (Recommended - More secure)")"
    print_styled "GRIS" "$(get_message "   ↳ Nécessite une connexion en mode distant dans Monero GUI d'abord" "   ↳ Requires remote connection in Monero GUI first")"
    print_styled "GRIS" "$(get_message "   ↳ Puis vous pourrez revenir en mode local après connexion" "   ↳ Then you can switch back to local mode after connection")"
    echo
    print_styled "PRIMARY" "$(get_message "2) SANS mot de passe (Connexion directe en local)" "2) WITHOUT password (Direct local connection)")"
    print_styled "GRIS" "$(get_message "   ↳ Connexion directe possible mais moins sécurisé" "   ↳ Direct connection possible but less secure")"
    print_styled "GRIS" "$(get_message "   ↳ Recommandé uniquement pour usage personnel local" "   ↳ Recommended only for personal local use")"
    echo
    
    while true; do
        echo -n "$(print_styled "INFO" "$(get_message "Votre choix (1-2): " "Your choice (1-2): ")")"
        read -r security_choice
        
        case $security_choice in
            1)
                echo
                print_styled "SUCCESS" "$(get_message "✅ Configuration sécurisée choisie" "✅ Secure configuration selected")"
                echo
                print_styled "WARNING" "$(get_message "📝 IMPORTANT - Procédure de connexion du wallet(portefeuille) :" "📝 IMPORTANT - Wallet connection procedure:")"
                print_styled "INFO" "$(get_message "   1️⃣ Ouvrir le wallet" "   1️⃣ Open wallet")"
                print_styled "INFO" "$(get_message "   2️⃣ Aller dans Paramètres > Nœud" "   2️⃣ Go to Settings > Node")"
                print_styled "INFO" "$(get_message "   3️⃣ Sélectionner 'Nœud distant ou noeud local'" "   3️⃣ Select 'Remote node or local node'")"
                print_styled "INFO" "$(get_message "   4️⃣ Entrer : [IP_DE_VOTRE_NOEUD]:18081" "   4️⃣ Enter: [YOUR_NODE_IP]:18081")"
                print_styled "INFO" "$(get_message "   5️⃣ Nom d'utilisateur : easynode" "   5️⃣ Username: easynode")"
                print_styled "INFO" "$(get_message "   6️⃣ Mot de passe : [celui que vous allez créer]" "   6️⃣ Password: [the one you're about to create]")"
                
                echo

                while true; do
                    echo -n "$(print_styled "PRIMARY" "$(get_message "Entrez un mot de passe RPC sécurisé: " "Enter a secure RPC password: ")")"
                    read -r RPC_PASSWORD
                    
                    if [ -z "$RPC_PASSWORD" ]; then
                        error "$(get_message "Le mot de passe ne peut pas être vide" "Password cannot be empty")"
                        continue
                    fi
                    
                    if [ ${#RPC_PASSWORD} -lt 6 ]; then
                        error "$(get_message "Le mot de passe doit contenir au moins 6 caractères" "Password must be at least 6 characters")"
                        continue
                    fi
                    
                    echo -n "$(print_styled "PRIMARY" "$(get_message "Confirmez le mot de passe: " "Confirm password: ")")"
                    read -r RPC_PASSWORD_CONFIRM
                    
                    if [ "$RPC_PASSWORD" = "$RPC_PASSWORD_CONFIRM" ]; then
                        break
                    else
                        error "$(get_message "Les mots de passe ne correspondent pas" "Passwords do not match")"
                        echo
                    fi
                done

                RPC_USERNAME="easynode"

                echo "rpc-login=$RPC_USERNAME:$RPC_PASSWORD" >> "$CONFIG_FILE"

                write_rpc_pass_file "$USERNAME" "$RPC_USERNAME" "$RPC_PASSWORD" "/home/$USERNAME/.bitmonero"

                print_styled "SUCCESS" "$(get_message "🔐 Authentification RPC sécurisée configurée" "🔐 Secure RPC authentication configured")"
                break
                ;;
                
            2)
                echo
                print_styled "WARNING" "$(get_message "⚠️ Configuration non sécurisée choisie" "⚠️ Unsecured configuration selected")"
                print_styled "INFO" "$(get_message "✅ Connexion directe possible en mode local dans Monero GUI" "✅ Direct connection possible in local mode in Monero GUI")"
                echo
                print_styled "INFO" "$(get_message "📝 PROCÉDURE DE CONNEXION du WALLET (portefeuille) :" "📝 WALLET CONNECTION PROCEDURE:")"
                print_styled "INFO" "$(get_message "   1️⃣ Ouvrir le wallet" "   1️⃣ Open Wallet")"
                print_styled "INFO" "$(get_message "   2️⃣ Sélectionner 'Nœud local ou noeud distant'" "   2️⃣ Select 'Local node or remote node'")"
                print_styled "INFO" "$(get_message "   4️⃣ Entrer : [IP_DE_VOTRE_NOEUD]:18081" "   4️⃣ Enter: [YOUR_NODE_IP]:18081")"
                print_styled "INFO" "$(get_message "   6️⃣ Aucun mot de passe requis" "   6️⃣ No password required")"
                echo

                RPC_USERNAME=""
                RPC_PASSWORD=""

                write_rpc_pass_file "$USERNAME" "" "" "/home/$USERNAME/.bitmonero"

                print_styled "SUCCESS" "$(get_message "✅ Configuration sans authentification activée" "✅ Configuration without authentication enabled")"
                break
                ;;
                
            *)
                error "$(get_message "Choix invalide. Choisissez 1 ou 2." "Invalid choice. Choose 1 or 2.")"
                ;;
        esac
    done

    sudo chown "$USERNAME:$USERNAME" "$CONFIG_FILE"
    sudo chmod 644 "$CONFIG_FILE"

    sudo chown -R "$USERNAME:$USERNAME" "/home/$USERNAME/.bitmonero"
    sudo chmod -R u+rw "/home/$USERNAME/.bitmonero"

    if grep -q "data-dir=" "$CONFIG_FILE" | grep -q "/media"; then
        BLOCKCHAIN_PATH=$(grep "data-dir=" "$CONFIG_FILE" | cut -d'=' -f2)
        
        if [ ! -d "$BLOCKCHAIN_PATH" ]; then
            mkdir -p "$(dirname "$BLOCKCHAIN_PATH")"
            ln -sf "/home/$USERNAME/.bitmonero" "$BLOCKCHAIN_PATH"
        fi
    fi

    success "$(get_message "Configuration créée dans $CONFIG_FILE" "Configuration created in $CONFIG_FILE")"
    
    if [ -n "$RPC_PASSWORD" ]; then
        print_styled "SUCCESS" "$(get_message "🔐 Mode sécurisé activé" "🔐 Secure mode enabled")"
        print_styled "PRIMARY" "$(get_message "Username: $RPC_USERNAME" "Username: $RPC_USERNAME")"
        print_styled "WARNING" "$(get_message "⚠️ Identifiants sauvés dans: /home/$USERNAME/rpc_easynode_pass.txt" "⚠️ Credentials saved in: /home/$USERNAME/rpc_easynode_pass.txt")"
        echo
        print_styled "INFO" "$(get_message "🔗 Pour Monero GUI : Mode distant puis local après sync" "🔗 For Monero GUI: Remote mode then local after sync")"
    else
        print_styled "SUCCESS" "$(get_message "✅ Mode direct activé" "✅ Direct mode enabled")"
        print_styled "INFO" "$(get_message "🔗 Pour Monero GUI : Mode local directement" "🔗 For Monero GUI: Local mode directly")"
    fi
    
    read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..." "Press Enter to continue...")")"
}

configure_dns() {
    print_header "$(get_message "CONFIGURATION DNS" "DNS CONFIGURATION")"

    info "$(get_message "Cette option permet de configurer la résolution DNS de votre système." "This option configures your system's DNS resolution.")"
    echo
    print_styled "PRIMARY" "$(get_message "1) Ne rien changer (vous utilisez déjà un routeur après votre box)" "1) Do nothing (you already use a router behind your internet box)")"
    print_styled "GRIS"    "$(get_message "   → Conserve la configuration actuelle. Recommandé si vous avez un routeur" "   → Keeps current configuration. Recommended if you have a router")"
    print_styled "GRIS"    "$(get_message "     dédié (GL.iNet, pfSense, etc.) qui gère déjà les DNS." "     (GL.iNet, pfSense, etc.) that already handles DNS.")"
    echo
    print_styled "PRIMARY" "$(get_message "2) Activer les DNS chiffrés AdGuard (confidentialité accrue)" "2) Enable encrypted AdGuard DNS (enhanced privacy)")"
    print_styled "GRIS"    "$(get_message "   → Utilise DNS-over-TLS pour que votre FAI ne puisse plus voir les sites" "   → Uses DNS-over-TLS so your ISP can no longer see the websites")"
    print_styled "GRIS"    "$(get_message "     que vous visitez. Bloque aussi trackers et publicités." "     you visit. Also blocks trackers and ads.")"
    echo
    print_styled "PRIMARY" "$(get_message "3) Réparer / réinitialiser le DNS par défaut" "3) Repair / reset DNS to default")"
    print_styled "GRIS"    "$(get_message "   → Restaure systemd-resolved en mode automatique (DHCP)." "   → Restores systemd-resolved in automatic mode (DHCP).")"
    print_styled "GRIS"    "$(get_message "     À utiliser si vous avez perdu internet suite à une manipulation." "     Use this if you lost internet after a previous change.")"
    echo
    print_styled "PRIMARY" "$(get_message "0) Retour au menu" "0) Return to menu")"
    echo
    echo -n "$(print_styled "INFO" "$(get_message "Choix (0-3): " "Choice (0-3): ")")"
    read -r dns_choice

    case $dns_choice in
        0)
            info "$(get_message "Aucun changement effectué." "No changes made.")"
            ;;

        1)
            success "$(get_message "Aucun changement effectué — votre configuration actuelle est conservée." "No changes made — your current configuration is kept.")"
            ;;

        2)
            info "$(get_message "Activation des DNS chiffrés AdGuard via systemd-resolved..." "Enabling encrypted AdGuard DNS via systemd-resolved...")"

            # Sauvegarde de l'état actuel
            if [ ! -f /etc/resolv.conf.backup ]; then
                sudo cp -a /etc/resolv.conf /etc/resolv.conf.backup 2>/dev/null
            fi
            if [ -f /etc/systemd/resolved.conf ] && [ ! -f /etc/systemd/resolved.conf.backup ]; then
                sudo cp /etc/systemd/resolved.conf /etc/systemd/resolved.conf.backup
            fi

            # S'assurer que systemd-resolved est installé et activé
            sudo systemctl enable systemd-resolved
            sudo systemctl start systemd-resolved

            # Configurer DNS-over-TLS avec AdGuard (DNS chiffrés + fallback Quad9)
            sudo tee /etc/systemd/resolved.conf > /dev/null << 'EOL'
[Resolve]
DNS=94.140.14.14#dns.adguard-dns.com 94.140.15.15#dns.adguard-dns.com
FallbackDNS=9.9.9.9 1.1.1.1
DNSOverTLS=yes
DNSSEC=allow-downgrade
Cache=yes
EOL

            # Recréer le symlink propre
            sudo rm -f /etc/resolv.conf
            sudo ln -s /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

            # Redémarrer pour appliquer
            sudo systemctl restart systemd-resolved

            sleep 2
            success "$(get_message "DNS chiffrés AdGuard activés (DNS-over-TLS)" "Encrypted AdGuard DNS enabled (DNS-over-TLS)")"
            info "$(get_message "Votre FAI ne peut plus voir vos requêtes DNS." "Your ISP can no longer see your DNS queries.")"
            info "$(get_message "Test : resolvectl status  (cherchez la ligne DNS-over-TLS)" "Test: resolvectl status  (look for DNS-over-TLS line)")"
            ;;

        3)
            info "$(get_message "Réinitialisation du DNS en mode automatique..." "Resetting DNS to automatic mode...")"

            # Restaurer resolved.conf par défaut si une sauvegarde existe
            if [ -f /etc/systemd/resolved.conf.backup ]; then
                sudo cp /etc/systemd/resolved.conf.backup /etc/systemd/resolved.conf
            else
                # Sinon, config par défaut minimale (tout en auto)
                sudo tee /etc/systemd/resolved.conf > /dev/null << 'EOL'
[Resolve]
#DNS=
#FallbackDNS=
#DNSOverTLS=no
Cache=yes
EOL
            fi

            # Retirer l'attribut immutable s'il a été posé
            sudo chattr -i /etc/resolv.conf 2>/dev/null

            # Activer et démarrer systemd-resolved
            sudo systemctl enable systemd-resolved
            sudo systemctl start systemd-resolved

            # Recréer le symlink vers le stub
            sudo rm -f /etc/resolv.conf
            sudo ln -s /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

            # Relancer le service
            sudo systemctl restart systemd-resolved

            sleep 2
            success "$(get_message "DNS réinitialisés en mode automatique (DHCP)" "DNS reset to automatic mode (DHCP)")"
            info "$(get_message "Le système utilise maintenant le DNS fourni par votre routeur/box." "The system now uses the DNS provided by your router/box.")"
            ;;

        *)
            error "$(get_message "Choix invalide" "Invalid choice")"
            ;;
    esac

    echo
    read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..." "Press Enter to continue...")")"
}

unmount_sdb1() {
    print_header "$(get_message "DÉMONTAGE DU DISQUE" "DISK UNMOUNTING")"
    
    MOUNT_POINT="/media/$USERNAME"
    
    if mount | grep -q "$MOUNT_POINT"; then
        if lsof "$MOUNT_POINT" > /dev/null 2>&1; then
            warning "$(get_message "Fermeture des processus en cours..." "Closing active processes...")"
            lsof "$MOUNT_POINT" | awk 'NR!=1 {print $2}' | xargs -r sudo kill
            sleep 2
        fi
        
        if sudo umount -f "$MOUNT_POINT"; then
            success "$(get_message "Disque démonté avec succès" "Disk unmounted successfully")"
            
            if [ -n "$USERNAME" ]; then
                CONFIG_FILE="/home/$USERNAME/.bitmonero/bitmonero.conf"
                if [ -f "$CONFIG_FILE" ]; then
                    EXISTING_RPC_LOGIN=""
                    if grep -q "^rpc-login=" "$CONFIG_FILE"; then
                        EXISTING_RPC_LOGIN=$(grep "^rpc-login=" "$CONFIG_FILE")
                        info "$(get_message "Configuration RPC avec mot de passe préservée" "RPC configuration with password preserved")"
                    else
                        info "$(get_message "Configuration RPC sans mot de passe préservée" "RPC configuration without password preserved")"
                    fi
                    
                    grep -v "^data-dir=" "$CONFIG_FILE" | sudo tee "$CONFIG_FILE.tmp" > /dev/null
                    
                    echo "data-dir=/home/$USERNAME/.bitmonero" | sudo tee -a "$CONFIG_FILE.tmp"
                    
                    if [ -n "$EXISTING_RPC_LOGIN" ]; then
                        echo "$EXISTING_RPC_LOGIN" | sudo tee -a "$CONFIG_FILE.tmp"
                    fi
                    
                    sudo mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
                    sudo chown "$USERNAME:$USERNAME" "$CONFIG_FILE"
                    sudo chmod 644 "$CONFIG_FILE"
                    
                    sudo chown -R "$USERNAME:$USERNAME" "/home/$USERNAME/.bitmonero"
                    sudo chmod -R u+rw "/home/$USERNAME/.bitmonero"
                    
                    if [ -n "$EXISTING_RPC_LOGIN" ]; then
                        RPC_USERNAME=$(echo "$EXISTING_RPC_LOGIN" | cut -d'=' -f2 | cut -d':' -f1)
                        RPC_PASSWORD=$(echo "$EXISTING_RPC_LOGIN" | cut -d':' -f2)
                        write_rpc_pass_file "$USERNAME" "$RPC_USERNAME" "$RPC_PASSWORD" "/home/$USERNAME/.bitmonero"
                    else
                        write_rpc_pass_file "$USERNAME" "" "" "/home/$USERNAME/.bitmonero"
                    fi
                    
                    success "$(get_message "Configuration Monero mise à jour" "Monero configuration updated")"
                fi
            else
                warning "$(get_message "Impossible de mettre à jour la configuration: utilisateur non défini" "Cannot update configuration: username not defined")"
            fi
        else
            error "$(get_message "Échec du démontage" "Unmounting failed")"
            return 1
        fi
    else
        warning "$(get_message "Le disque n'est pas monté sur $MOUNT_POINT" "Disk is not mounted on $MOUNT_POINT")"
    fi

    # ── Nettoyage fstab ──────────────────────────────────────────────
    FSTAB_CHANGED=0
    if grep -q "# Entr.*EasyNode" /etc/fstab 2>/dev/null; then
        sudo cp /etc/fstab /etc/fstab.bak_easymonerod
        sudo sed -i '/# Entr.*EasyNode/d' /etc/fstab
        FSTAB_CHANGED=1
    fi
    if grep -q "/media/$USERNAME.*x-gvfs-show" /etc/fstab 2>/dev/null; then
        sudo sed -i "/\/media\/$USERNAME.*x-gvfs-show/d" /etc/fstab
        FSTAB_CHANGED=1
    fi
    if [ "$FSTAB_CHANGED" -eq 1 ]; then
        sudo systemctl daemon-reload 2>/dev/null || true
        sudo udevadm trigger 2>/dev/null || true
        success "$(get_message "fstab nettoyé — disque externe libéré (backup: /etc/fstab.bak_easymonerod)" "fstab cleaned — external disk released (backup: /etc/fstab.bak_easymonerod)")"
    else
        info "$(get_message "Aucune entrée EasyNode dans fstab à supprimer" "No EasyNode fstab entry to remove")"
    fi
    # ─────────────────────────────────────────────────────────────────

    read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..." "Press Enter to continue...")")"
}


manage_blockchain() {
    print_header "$(get_message "GESTION DE LA BLOCKCHAIN" "BLOCKCHAIN MANAGEMENT")"
    
    if [ -z "$USERNAME" ]; then
        error "$(get_message "Nom d'utilisateur non défini" "Username not defined")"
        return 1
    fi

    EXTERNAL_DRIVE="/media/$USERNAME"
    
    BLOCKCHAIN_FOLDER="MoneroBlockchain"
    BLOCKCHAIN_PATH="$EXTERNAL_DRIVE/$BLOCKCHAIN_FOLDER"

    info "$(get_message "Liste des disques disponibles:" "Available disks:")"
    lsblk -nrpo "NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE" | awk '$3=="disk" || $3=="part"'
    
    echo -n "$(print_styled "INFO" "$(get_message "Entrez le nom du disque (ex: sdb1): " "Enter disk name (e.g., sdb1): ")")"
    read -r DEVICE
    
    if [ -z "$DEVICE" ]; then
        error "$(get_message "Aucun disque sélectionné" "No disk selected")"
        return 1
    fi
    
    DEVICE="/dev/$DEVICE"
    
    if [ ! -b "$DEVICE" ]; then
        error "$(get_message "Le périphérique $DEVICE n'existe pas" "Device $DEVICE does not exist")"
        return 1
    fi

    if mount | grep -q "$DEVICE"; then
        sudo umount "$DEVICE" 2>/dev/null
    fi

    sudo mkdir -p "$EXTERNAL_DRIVE"
    if ! sudo mount -o uid=$(id -u $USERNAME),gid=$(id -g $USERNAME) "$DEVICE" "$EXTERNAL_DRIVE"; then
        error "$(get_message "Échec du montage" "Mount failed")"
        return 1
    fi
    
    sudo mkdir -p "$BLOCKCHAIN_PATH"
    
    CONFIG_FILE="/home/$USERNAME/.bitmonero/bitmonero.conf"
    if [ -f "$CONFIG_FILE" ]; then
        sudo cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"
        
        EXISTING_RPC_LOGIN=""
        if grep -q "^rpc-login=" "$CONFIG_FILE"; then
            EXISTING_RPC_LOGIN=$(grep "^rpc-login=" "$CONFIG_FILE")
            info "$(get_message "Configuration RPC existante préservée" "Existing RPC configuration preserved")"
        else
            info "$(get_message "Aucune configuration RPC trouvée - mode sans mot de passe conservé" "No RPC configuration found - passwordless mode preserved")"
        fi
    fi

    sudo mkdir -p "$(dirname "$CONFIG_FILE")"

    TMP_CONFIG=$(mktemp)
    
    {
        echo "# Configuration Monero"
        echo "no-igd=1"
        echo "no-zmq=1"
        echo "rpc-bind-ip=0.0.0.0"
        echo "rpc-bind-port=18081"
        echo "p2p-bind-port=18080"
        echo "p2p-bind-ip=0.0.0.0"
        echo "in-peers=32"
        echo "out-peers=32"
        echo "disable-dns-checkpoints=1"
        echo "confirm-external-bind=1"
        echo "restricted-rpc=0"
        echo "data-dir=$BLOCKCHAIN_PATH"
        
        if [ -n "$EXISTING_RPC_LOGIN" ]; then
            echo "$EXISTING_RPC_LOGIN"
        fi
        
        if [ "$BLOCKCHAIN_TYPE" = "pruned" ]; then
            echo "prune-blockchain=1"
        fi
    } > "$TMP_CONFIG"

    if [ -n "$EXISTING_RPC_LOGIN" ]; then
        success "$(get_message "Configuration RPC avec mot de passe conservée" "RPC configuration with password preserved")"
    else
        success "$(get_message "Configuration RPC sans mot de passe conservée" "RPC configuration without password preserved")"
    fi

    if [ -s "$TMP_CONFIG" ]; then
        sudo cp "$TMP_CONFIG" "$CONFIG_FILE"
        rm "$TMP_CONFIG"
        
        if ! grep -q "^data-dir=" "$CONFIG_FILE"; then
            echo "data-dir=$BLOCKCHAIN_PATH" | sudo tee -a "$CONFIG_FILE"
        fi
    else
        error "$(get_message "Erreur lors de la création de la configuration" "Error creating configuration")"
        rm -f "$TMP_CONFIG"
        return 1
    fi

    sudo chown "$USERNAME:$USERNAME" "$CONFIG_FILE"
    sudo chmod 644 "$CONFIG_FILE"
    sudo chown -R "$USERNAME:$USERNAME" "/home/$USERNAME/.bitmonero"
    sudo chmod -R u+rw "/home/$USERNAME/.bitmonero"

    DEVICE_UUID=$(sudo blkid -s UUID -o value "$DEVICE")
    if [ -z "$DEVICE_UUID" ]; then
        error "$(get_message "Impossible d'obtenir l'UUID du disque" "Unable to get disk UUID")"
        return 1
    fi

    MOUNTPOINT_BEFORE=$(findmnt -n -o TARGET -S UUID="$DEVICE_UUID" 2>/dev/null || echo "")
    if [ -n "$MOUNTPOINT_BEFORE" ] && [ "$MOUNTPOINT_BEFORE" != "$EXTERNAL_DRIVE" ]; then
        info "$(get_message "Le disque est actuellement monté sur $MOUNTPOINT_BEFORE" "Disk is currently mounted on $MOUNTPOINT_BEFORE")"
    fi

    if grep -q "UUID=$DEVICE_UUID" /etc/fstab; then
        info "$(get_message "Suppression des entrées existantes pour UUID=$DEVICE_UUID" "Removing existing entries for UUID=$DEVICE_UUID")"
        sudo sed -i "/UUID=$DEVICE_UUID/d" /etc/fstab
    fi
    # Supprimer aussi les commentaires EasyNode orphelins accumulés
    sudo sed -i '/# Entr.*EasyNode/d' /etc/fstab

    USER_ID=$(id -u "$USERNAME")
    GROUP_ID=$(id -g "$USERNAME")
    echo "# Entrée pour EasyNode - Ne pas modifier manuellement" | sudo tee -a /etc/fstab > /dev/null
    echo "UUID=$DEVICE_UUID $EXTERNAL_DRIVE auto defaults,users,uid=$USER_ID,gid=$GROUP_ID,umask=022,nofail,x-gvfs-show 0 0" | sudo tee -a /etc/fstab > /dev/null
    success "$(get_message "Configuration du montage automatique ajoutée/mise à jour" "Automatic mount configuration added/updated")"

    info "$(get_message "Rechargement de systemd..." "Reloading systemd...")"
    sudo systemctl daemon-reload

    if ! mountpoint -q "$EXTERNAL_DRIVE"; then
        info "$(get_message "Montage du disque..." "Mounting disk...")"
        sudo mount -a
        
        if ! mountpoint -q "$EXTERNAL_DRIVE"; then
            warning "$(get_message "Le montage automatique a échoué, tentative de montage direct..." "Automatic mount failed, trying direct mount...")"
            sudo mount -U "$DEVICE_UUID" "$EXTERNAL_DRIVE"
        fi
    fi

    if [ -n "$EXISTING_RPC_LOGIN" ]; then
        RPC_USERNAME=$(echo "$EXISTING_RPC_LOGIN" | cut -d'=' -f2 | cut -d':' -f1)
        RPC_PASSWORD=$(echo "$EXISTING_RPC_LOGIN" | cut -d':' -f2)
        write_rpc_pass_file "$USERNAME" "$RPC_USERNAME" "$RPC_PASSWORD" "$BLOCKCHAIN_PATH"
    else
        write_rpc_pass_file "$USERNAME" "" "" "$BLOCKCHAIN_PATH"
    fi

    success "$(get_message "Blockchain configurée dans: $BLOCKCHAIN_PATH" "Blockchain configured in: $BLOCKCHAIN_PATH")"
    info "$(get_message "Le disque sera monté automatiquement au démarrage" "The disk will be automatically mounted at boot")"
    read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..." "Press Enter to continue...")")"
}


ban_ip_via_monerod() {
    local ip="$1"
    local duration="$2"
    
    
    if [ -f "/home/$USERNAME/.bitmonero/bitmonero.conf" ] && grep -q "^rpc-login=" "/home/$USERNAME/.bitmonero/bitmonero.conf"; then
        local RPC_CREDENTIALS=$(grep "^rpc-login=" "/home/$USERNAME/.bitmonero/bitmonero.conf" | cut -d'=' -f2)
        "$MONEROD_PATH" ban "$ip" "$duration" --rpc-bind-port 18081 --rpc-login "$RPC_CREDENTIALS" >/dev/null 2>&1
    else
        "$MONEROD_PATH" ban "$ip" "$duration" --rpc-bind-port 18081 >/dev/null 2>&1
    fi
    
    return $?
}

start_blockchain() {
    if [ -z "$USERNAME" ]; then
        error "$(get_message "Nom d'utilisateur non défini" "Username not defined")"
        return 1
    fi

    print_header "$(get_message "DÉMARRAGE DE LA BLOCKCHAIN" "STARTING BLOCKCHAIN")"
    
    print_styled "PRIMARY" "$(get_message "Sélectionnez le type de blockchain:" "Select blockchain type:")"
    print_styled "PRIMARY" "1) $(get_message "Complète 220 Go" "Complete 220 Go")"
    print_styled "PRIMARY" "2) $(get_message "Prune 90 Go" "Pruned 90 Go")"
    echo -n "$(print_styled "INFO" "$(get_message "Choix (1-2): " "Choice (1-2): ")")"
    read -r bc_choice
    
    case $bc_choice in
        1) BLOCKCHAIN_TYPE="complete" ;;
        2) BLOCKCHAIN_TYPE="pruned" ;;
        *) 
            error "$(get_message "Choix invalide" "Invalid choice")"
            return 1 ;;
    esac
    
    CONFIG_FILE="/home/$USERNAME/.bitmonero/bitmonero.conf"
    DEFAULT_DATA_DIR="/home/$USERNAME/.bitmonero"
    
    if [ -f "$CONFIG_FILE" ]; then
        sudo sed -i '/^prune-blockchain=/d' "$CONFIG_FILE"
        
        if [ "$BLOCKCHAIN_TYPE" = "pruned" ]; then
            echo "prune-blockchain=1" | sudo tee -a "$CONFIG_FILE" > /dev/null
        fi
        
        BLOCKCHAIN_LOCATION=$(grep "^data-dir=" "$CONFIG_FILE" 2>/dev/null | cut -d'=' -f2)
    fi

    if [ -z "$BLOCKCHAIN_LOCATION" ]; then
        BLOCKCHAIN_LOCATION="$DEFAULT_DATA_DIR"
    fi

    info "$(get_message "Emplacement de la blockchain: $BLOCKCHAIN_LOCATION" "Blockchain location: $BLOCKCHAIN_LOCATION")"
    
    download_ban_list
    
    if [ -n "$BLOCKCHAIN_LOCATION" ] && [[ "$BLOCKCHAIN_LOCATION" == "/media/$USERNAME"* ]]; then
        DEVICE=$(mount | grep "/media/$USERNAME" | awk '{print $1}')
        if [ -z "$DEVICE" ]; then
            error "$(get_message "Le disque externe n'est pas monté" "External disk is not mounted")"
            return 1
        fi
        info "$(get_message "Disque externe monté: $DEVICE" "External disk mounted: $DEVICE")"
    fi

    print_styled "PRIMARY" "$(get_message "Démarrer la blockchain MONERO ?" "Start MONERO blockchain?")"
    print_styled "PRIMARY" "1) $(get_message "Avec blocage IP" "With IP blocking")"
    print_styled "PRIMARY" "2) $(get_message "Sans blocage IP" "Without IP blocking")"
    print_styled "PRIMARY" "3) $(get_message "Annuler" "Cancel")"
    echo -n "$(print_styled "INFO" "$(get_message "Choix (1-3): " "Choice (1-3): ")")"
    read -r START_CHOICE

    if [ -n "$BLOCKCHAIN_LOCATION" ] && [ ! -w "$BLOCKCHAIN_LOCATION" ]; then
        error "$(get_message "Permissions insuffisantes sur $BLOCKCHAIN_LOCATION" "Insufficient permissions on $BLOCKCHAIN_LOCATION")"
        return 1
    fi

    MONEROD_PATH="/home/$USERNAME/monero/monerod"
    if [ ! -x "$MONEROD_PATH" ]; then
        error "$(get_message "monerod n'est pas trouvé ou n'est pas exécutable" "monerod not found or not executable")"
        return 1
    fi
monitor_peers() {
    sleep 15  
    
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    RESET='\033[0m'
    
    RPC_AUTH=""
    CONFIG_FILE="/home/$USERNAME/.bitmonero/bitmonero.conf"
    
    if [ -f "$CONFIG_FILE" ] && grep -q "^rpc-login=" "$CONFIG_FILE"; then
        RPC_LOGIN_LINE=$(grep "^rpc-login=" "$CONFIG_FILE")
        RPC_CREDENTIALS=$(echo "$RPC_LOGIN_LINE" | cut -d'=' -f2)
        RPC_AUTH="--digest -u $RPC_CREDENTIALS"
    elif [ -f "/home/$USERNAME/rpc_easynode_pass.txt" ]; then
        RPC_USERNAME=$(grep "Username:" "/home/$USERNAME/rpc_easynode_pass.txt" 2>/dev/null | cut -d' ' -f2)
        RPC_PASSWORD=$(grep "Password:" "/home/$USERNAME/rpc_easynode_pass.txt" 2>/dev/null | cut -d' ' -f2)
        if [ -n "$RPC_USERNAME" ] && [ -n "$RPC_PASSWORD" ]; then
            RPC_AUTH="--digest -u $RPC_USERNAME:$RPC_PASSWORD"
        fi
    fi
    
    while pgrep -f "monerod" > /dev/null; do
        if [ $STOP_MONEROD -eq 1 ]; then
            break
        fi
        
        if [ -n "$RPC_AUTH" ]; then
            PEER_INFO=$(curl -s -X POST http://localhost:18081/json_rpc \
                $RPC_AUTH \
                -H "Content-Type: application/json" \
                -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' 2>/dev/null)
        else
            PEER_INFO=$(curl -s -X POST http://localhost:18081/json_rpc \
                -H "Content-Type: application/json" \
                -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' 2>/dev/null)
        fi
        
        if [ $? -eq 0 ] && echo "$PEER_INFO" | grep -q '"result"' && ! echo "$PEER_INFO" | grep -q '"error"'; then
            IN_PEERS=$(echo "$PEER_INFO" | sed -n 's/.*"incoming_connections_count":\s*\([0-9]*\).*/\1/p')
            OUT_PEERS=$(echo "$PEER_INFO" | sed -n 's/.*"outgoing_connections_count":\s*\([0-9]*\).*/\1/p')
            
            if [ -n "$IN_PEERS" ] && [ -n "$OUT_PEERS" ]; then
                echo -ne "\r${GREEN}IN-PEERS: ${IN_PEERS:-0}${RESET} | ${GREEN}OUT-PEERS: ${OUT_PEERS:-0}${RESET}                    "
            else
                echo -ne "\r${GREEN}RPC OK, attente des données...${RESET}                    "
            fi
        else
            if echo "$PEER_INFO" | grep -q "401\|unauthorized\|Unauthorized"; then
                echo -ne "\r${GREEN}❌ Erreur d'authentification RPC${RESET}                    "
            elif [ -z "$PEER_INFO" ]; then
                echo -ne "\r${GREEN}⏳ Attente connexion RPC...${RESET}                    "
            else
                echo -ne "\r${GREEN}⏳ Synchronisation en cours...${RESET}                    "
            fi
        fi
        
        sleep 15  
    done
    
    echo -ne "\r                                                    \r"
}

cleanup() {
                if [ -n "$trap_original" ]; then
                    eval "$trap_original"
                else
                    trap - SIGINT
                fi
                
                if [ -n "$MONEROD_PID" ] && kill -0 $MONEROD_PID 2>/dev/null; then
                    info "$(get_message "Arrêt de monerod..." "Stopping monerod...")"
                    kill $MONEROD_PID 2>/dev/null
                    wait $MONEROD_PID 2>/dev/null
                fi
                
                success "$(get_message "Blockchain arrêtée" "Blockchain stopped")"
            }
            
            handle_sigint() {
                echo
                info "$(get_message "CTRL+C détecté, arrêt de la blockchain..." "CTRL+C detected, stopping blockchain...")"
                STOP_MONEROD=1
                
                if [ -n "$MONEROD_PID" ] && kill -0 $MONEROD_PID 2>/dev/null; then
                    kill -SIGINT $MONEROD_PID 2>/dev/null
                fi
                
                return 0
            }
            
    case $START_CHOICE in
        1)
            STOP_MONEROD=0
            
            trap_original=$(trap -p SIGINT)
            
            
            
            trap handle_sigint SIGINT
            
if [ -n "$BLOCKCHAIN_LOCATION" ]; then
    if [ -d "$BLOCKCHAIN_LOCATION" ]; then
        sudo chown -R "$USERNAME:$USERNAME" "$BLOCKCHAIN_LOCATION" 2>/dev/null || true
        sudo chmod -R u+rw "$BLOCKCHAIN_LOCATION" 2>/dev/null || true
    fi
    
    sudo chown -R "$USERNAME:$USERNAME" "/home/$USERNAME/.bitmonero" 2>/dev/null || true
    sudo chmod -R u+rw "/home/$USERNAME/.bitmonero" 2>/dev/null || true
fi
            

# ── Bans IP chargés PAR MONEROD LUI-MÊME au démarrage (--ban-list) ──
# Une seule lecture interne du fichier, avant toute connexion aux pairs :
# plus de boucle "monerod ban" IP par IP (15 min) ni de fenêtre où les
# nœuds espions peuvent se connecter avant d'être bannis.
BAN_ARGS=()
BANLIST_COUNT=0
BAN_LIST_FILE="/home/$USERNAME/.bitmonero/ban_list.txt"
if [ -s "$BAN_LIST_FILE" ]; then
    BANLIST_COUNT=$(grep -cE '^[0-9]' "$BAN_LIST_FILE")
fi
if [ "$BANLIST_COUNT" -gt 0 ]; then
    BAN_ARGS=(--ban-list "$BAN_LIST_FILE")
    info "$(get_message "Liste des IP bannis : $BANLIST_COUNT entrées, chargées par monerod au démarrage" "IP ban list: $BANLIST_COUNT entries, loaded by monerod at startup")"
else
    warning "$(get_message "Liste des IP bannis vide ou absente : démarrage sans blocage IP" "IP ban list empty or missing: starting without IP blocking")"
fi

monitor_peers &
MONITOR_PID=$!
            
            if [ -n "$BLOCKCHAIN_LOCATION" ]; then
                info "$(get_message "Démarrage de la blockchain avec le fichier de configuration" "Starting blockchain with config file")"
                "$MONEROD_PATH" --config-file="$CONFIG_FILE" "${BAN_ARGS[@]}" --non-interactive &
                MONEROD_PID=$!
            else
                info "$(get_message "Démarrage de la blockchain avec le dossier par défaut" "Starting blockchain with default folder")"
                "$MONEROD_PATH" --data-dir="$DEFAULT_DATA_DIR" "${BAN_ARGS[@]}" --non-interactive &
                MONEROD_PID=$!
            fi
            
            info "$(get_message "Attente du démarrage du service RPC..." "Waiting for RPC service to start...")"
            for i in {1..60}; do
                if [ $STOP_MONEROD -eq 1 ]; then
                    break
                fi
                
                if nc -z localhost 18081; then
                    success "$(get_message "Service RPC disponible" "RPC service available")"
                    break
                fi
                
                echo -n "."
                sleep 2
                
                if [ $i -eq 60 ]; then
                    error "$(get_message "Timeout en attendant le service RPC" "Timeout waiting for RPC service")"
                fi
            done
            
            if [ $STOP_MONEROD -eq 0 ]; then
                # ── Vérification : UN SEUL appel RPC (get_bans) au lieu de N appels ──
                if [ "$BANLIST_COUNT" -gt 0 ]; then
                    info "$(get_message "Vérification de l'état des bans..." "Checking ban status...")"
                    local active_bans
                    active_bans=$(count_active_bans)
                    if [ -n "$active_bans" ] && [ "$active_bans" -gt 0 ]; then
                        success "$(get_message "Bans actifs dans monerod : $active_bans (liste : $BANLIST_COUNT entrées)" "Active bans in monerod: $active_bans (list: $BANLIST_COUNT entries)")"
                    else
                        warning "$(get_message "Impossible de confirmer les bans via RPC (ils sont chargés au démarrage, voir bitmonero.log)" "Could not confirm bans via RPC (they are loaded at startup, see bitmonero.log)")"
                    fi
                fi
            fi
            
            print_styled "PRIMARY" "$(get_message "Patientez..." "Wait..")"
            
            while [ $STOP_MONEROD -eq 0 ]; do
                if ! kill -0 $MONEROD_PID 2>/dev/null; then
                    info "$(get_message "Le processus monerod s'est terminé" "Monerod process has terminated")"
                    STOP_MONEROD=1
                    break
                fi
                sleep 1
            done
             if [ -n "$MONITOR_PID" ]; then
                kill $MONITOR_PID 2>/dev/null
            fi
            cleanup
            ;;
        2)
            STOP_MONEROD=0
            
            trap_original=$(trap -p SIGINT)
            
            
            
            trap handle_sigint SIGINT
            
if [ -n "$BLOCKCHAIN_LOCATION" ]; then
    if [ -d "$BLOCKCHAIN_LOCATION" ]; then
        sudo chown -R "$USERNAME:$USERNAME" "$BLOCKCHAIN_LOCATION" 2>/dev/null || true
        sudo chmod -R u+rw "$BLOCKCHAIN_LOCATION" 2>/dev/null || true
    fi
    
    sudo chown -R "$USERNAME:$USERNAME" "/home/$USERNAME/.bitmonero" 2>/dev/null || true
    sudo chmod -R u+rw "/home/$USERNAME/.bitmonero" 2>/dev/null || true
fi

monitor_peers &
MONITOR_PID=$!
            
            
            if [ -n "$BLOCKCHAIN_LOCATION" ]; then
                info "$(get_message "Démarrage de la blockchain avec le fichier de configuration" "Starting blockchain with config file")"
                "$MONEROD_PATH" --config-file="$CONFIG_FILE" --non-interactive &
                MONEROD_PID=$!
            else
                info "$(get_message "Démarrage de la blockchain avec le dossier par défaut" "Starting blockchain with default folder")"
                "$MONEROD_PATH" --data-dir="$DEFAULT_DATA_DIR" --non-interactive &
                MONEROD_PID=$!
            fi
            
            print_styled "PRIMARY" "$(get_message "Appuyez sur CTRL+C pour arrêter la blockchain et revenir au menu" "Press CTRL+C to stop the blockchain and return to the menu")"
            
            while [ $STOP_MONEROD -eq 0 ]; do
                if ! kill -0 $MONEROD_PID 2>/dev/null; then
                    info "$(get_message "Le processus monerod s'est terminé" "Monerod process has terminated")"
                    STOP_MONEROD=1
                    break
                fi
                sleep 1
            done
             if [ -n "$MONITOR_PID" ]; then
                kill $MONITOR_PID 2>/dev/null
            fi
            cleanup
            ;;
        3|*)
            info "$(get_message "Démarrage annulé" "Startup cancelled")"
            return 1
            ;;
    esac
    
    return 0
}

download_ban_list() {
    local BAN_LIST_FILE="/home/$USERNAME/.bitmonero/ban_list.txt"
    local BAN_LIST_URL="https://raw.githubusercontent.com/Boog900/monero-ban-list/main/ban_list.txt"
    local tmp_raw tmp_clean count

    info "$(get_message "Téléchargement de la liste des IP bannis..." "Downloading IP ban list...")"

    mkdir -p "/home/$USERNAME/.bitmonero"
    tmp_raw=$(mktemp)
    tmp_clean=$(mktemp)

    # Téléchargement dans un fichier temporaire : un échec ne vide plus
    # l'ancienne liste (wget -O tronquait le fichier même en cas d'erreur).
    if wget -q -O "$tmp_raw" "$BAN_LIST_URL" && [ -s "$tmp_raw" ]; then
        # Ne garder que les lignes IPv4 ou IPv4/CIDR valides (retire \r, espaces,
        # commentaires) : monerod --ban-list lit alors un fichier propre.
        tr -d '\r' < "$tmp_raw" | sed 's/#.*//; s/^[[:space:]]*//; s/[[:space:]].*$//' \
            | grep -E '^([0-9]{1,3}\.){3}[0-9]{1,3}(/[0-9]{1,2})?$' | sort -u > "$tmp_clean"
        count=$(wc -l < "$tmp_clean")
        if [ "$count" -gt 0 ]; then
            mv -f "$tmp_clean" "$BAN_LIST_FILE"
            sudo chown "$USERNAME:$USERNAME" "$BAN_LIST_FILE"
            sudo chmod 644 "$BAN_LIST_FILE"
            success "$(get_message "Liste des IP bannis téléchargée : $count entrées" "IP ban list downloaded: $count entries")"
        else
            error "$(get_message "Liste téléchargée invalide : ancienne liste conservée" "Downloaded list is invalid: previous list kept")"
        fi
    else
        error "$(get_message "Échec du téléchargement : ancienne liste conservée (si présente)" "Download failed: previous list kept (if any)")"
    fi
    rm -f "$tmp_raw" "$tmp_clean"

    if [ ! -f "$BAN_LIST_FILE" ]; then
        touch "$BAN_LIST_FILE"
        sudo chown "$USERNAME:$USERNAME" "$BAN_LIST_FILE"
        sudo chmod 644 "$BAN_LIST_FILE"
    fi
}

# Compte les bans actifs avec UN SEUL appel JSON-RPC get_bans
count_active_bans() {
    local conf="/home/$USERNAME/.bitmonero/bitmonero.conf"
    local auth=()
    if [ -f "$conf" ] && grep -q "^rpc-login=" "$conf"; then
        auth=(--digest -u "$(grep "^rpc-login=" "$conf" | head -n1 | cut -d'=' -f2-)")
    fi
    curl -s --max-time 30 "${auth[@]}" -X POST http://127.0.0.1:18081/json_rpc \
        -H 'Content-Type: application/json' \
        -d '{"jsonrpc":"2.0","id":"0","method":"get_bans"}' 2>/dev/null \
        | grep -o '"host"' | wc -l
}
show_notes() {
          clear
                setup_terminal
                echo -e "\n\n\n\n\n\n\n\n"   
                

                print_header "$(get_message "NOTES" "READ")"
                
                print_styled "MONERO" "$(get_message "- Pour arrêter la blockchain : CTRL + C" "- To stop the blockchain: CTRL + C")"
                echo
                print_styled "MONERO" "$(get_message "- Votre nom d'utilisateur est: ${COLORS[SUCCESS]}$SUDO_USER${COLORS[INFO]}" "- Your username is: ${COLORS[SUCCESS]}$SUDO_USER${COLORS[INFO]}")"
                echo
                print_styled "MONERO" "$(get_message "- Vérification de l'adresse IP Tor..." "- Checking Tor IP address...")"
    TOR_IP=$(torsocks curl -s https://check.torproject.org/api/ip 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$TOR_IP" ]; then
        print_styled "SUCCESS" "$(get_message "- Adresse IP TOR: ${COLORS[SUCCESS]}$TOR_IP${COLORS[SUCCESS]}" "- TOR IP address: ${COLORS[SUCCESS]}$TOR_IP${COLORS[SUCCESS]}")"
    else
        print_styled "ERROR" "$(get_message "- Impossible de récupérer l'adresse IP Tor" "- Unable to retrieve Tor IP address")"
    fi
    echo
                print_styled "PRIMARY" "$(get_message "- Configuration réseau requise :" "- Required network configuration:")"
    print_styled "PRIMARY" "$(get_message "⚠️ REDIRIGER le port 22 et 18080 de votre Box internet" "⚠️ Open port 22 and 18080 of your internet router")"
    print_styled "PRIMARY" "$(get_message "  vers l'IP de votre PC." "  to your PC's IP address.")"
    print_styled "MONERO" "$(get_message "  https://github.com/kerlannXmr/EasyMonerod/issues/10" "  https://github.com/kerlannXmr/EasyMonerod/issues/10")"
                echo
    print_styled "MONERO" "$(get_message "- Installer MONERO GUI pour la gestion du wallet" "- Install MONERO GUI for wallet management")"
                print_styled "MONERO" "$(get_message "  MONERO GUI se synchronisera sur ce noeud" "  MONERO GUI will synch on this node")"
                
                print_styled "MONERO" "$(get_message "  https://www.getmonero.org/downloads/" "  https://www.getmonero.org/downloads/")"
                echo
                print_styled "MONERO" "\e]8;;https://mega.nz/file/gjNWgL5B#itd6yCJJk_-1QbP2NbGWIm5DI1CC_MbTr8L6TeDqESI\e\\  PDF Documentations point 5 (CTRL+click)\e]8;;\e\\"
                echo
    
    echo
    print_styled "PRIMARY" "$(get_message "-🙏 Gacieux Dons MONERO(Xmr) pour le dur labeur: " "-🙏 Send MONERO(Xmr) donation for hard work")" 
    print_styled "PRIMARY" "$(get_message "    avec 'cake wallet' à:    kerlann.xmr" "    with 'cake wallet' to:   kerlann.xmr")"
    echo
    print_styled "MONERO" "$(get_message "- Contact:  easynode@kerlann.org" "- Contact:  easynode@kerlann.org")"
    echo
    print_styled "MONERO" "$(get_message "- Code source:" "- Source Code:")"
    print_styled "MONERO" "$(get_message "  https://github.com/kerlannXmr/easymonerod" "  https://github.com/kerlannXmr/easymonerod")"
                
                read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..❤️." "Press Enter to continue..❤️.")")"
}
show_scripts() {
       clear
       setup_terminal
       echo -e "\n\n\n\n\n\n"
       print_header "$(get_message "INFOS" "FEATURES")"
  
  print_styled "MONERO" "1) $(get_message "Mise à jour système et installation des paquets" "System update and package installation")"
    print_styled "PRIMARY" "   $(get_message "- Configuration du firewall activé avec ouverture des ports :" "- Firewall configuration Actived with ports opening:")"
    echo -e "${COLORS[GRIS]}    $(get_message "-Ports system: 22(SSH), 80(HTTP), 443(HTTPS), 9050(Tor), 4200(SHELL IN BOX), 4444(i2p-http), 4447(i2p-socks), 53317(localsend)" "-System ports: 22(SSH), 80(HTTP), 443(HTTPS), 9050(Tor), 4200(SHELL IN BOX), 4444(i2p-http), 4447(i2p-socks), 53317(localsend)")${COLORS[RESET]}"
    echo -e "${COLORS[GRIS]}    $(get_message "-Ports Monero: 18080(P2P), 18081(Public), 18083(ZMQ), 18084(Tor), 18085(I2P), 18086(LWS), 18081(RPC)" "-Monero ports: 18080(P2P), 18081(Public), 18083(ZMQ), 18084(Tor), 18085(I2P), 18086(LWS), 18081(RPC)")${COLORS[RESET]}"
    echo
    print_styled "MONERO" "2) $(get_message "Installation de Monero CLI" "Monero CLI Installation")"
    print_styled "PRIMARY" "   $(get_message "- Installation des fichiers Monero" "- Installing Monero files")"
    print_styled "PRIMARY" "   $(get_message "- Configuration des permissions" "- Setting up permissions")"
    echo
    print_styled "MONERO" "3) $(get_message "Installation et configuration de TOR" "TOR Installation and configuration")"
           
    if [ -f /var/lib/tor/monero-service/hostname ]; then
    ONION_ADDRESS=$(sudo cat /var/lib/tor/monero-service/hostname)
    echo -e "${COLORS[SUCCESS]}    -TOR Onion: $ONION_ADDRESS${COLORS[RESET]}"
fi
   print_styled "SUCCESS" "     PORT RPC: 18081"
   if [ -f /var/lib/tor/ssh/hostname ]; then
    SSH_ONION_ADDRESS=$(sudo cat /var/lib/tor/ssh/hostname)
    echo -e "${COLORS[SUCCESS]}    -SSH Onion: $SSH_ONION_ADDRESS${COLORS[RESET]}"
fi
   print_styled "SUCCESS" "     PORT SSH: 22"
   print_styled "WARNING" "   $(get_message " Les adresses Tor sont créées uniquement lors de votre installation" "  Tor addresses are only created during installation")"
    echo
    print_styled "MONERO" "4) $(get_message "Configuration de bitmonero.conf" "bitmonero.conf configuration")"
    print_styled "PRIMARY" "   $(get_message "- Configuration du fichier de démarrage" "- Configuring startup file")"
    print_styled "PRIMARY" "   $(get_message "- Configuration des ports" "- Setting up ports")"
    print_styled "SUCCESS" "$(get_message "    -rpc-bind-port=18081" "     rpc-bind-port=18081")"
    print_styled "PRIMARY" "   $(get_message "- Configuration des chemins" "- Setting up paths")"
    echo
    print_styled "MONERO" "5) $(get_message "Configuration DNS Anonyme" "Anonymous DNS Configuration")"
    print_styled "PRIMARY" "   $(get_message "- Installation des DNS sécurisés" "- Installing secure DNS")"
    print_styled "PRIMARY" "   $(get_message "- Configuration des serveurs DNS" "- Configuring DNS servers")"
    echo
    print_styled "MONERO" "6) $(get_message "Blockchain sur DISQUE EXTERNE" "Blockchain on EXTERNAL DISK")"
    print_styled "PRIMARY" "   $(get_message "- Montage et configuration fstab" "- Mounting and fstab configuration")"
    echo
    print_styled "MONERO" "7) $(get_message "Démontage du disque externe" "Unmount external disk")"
    print_styled "PRIMARY" "   $(get_message "- Démontage et nettoyage fstab" "- Unmounting and fstab cleanup")"
    echo
    print_styled "MONERO" "8)$(get_message " Démarrage Blockchain et Bloquage 'IP Bans list':" "Start & Block 'IP bans list':")"
    print_styled "PRIMARY" "   $(get_message "- https://github.com/monero-project/meta/issues/1124" "- https://github.com/monero-project/meta/issues/1124")"
    print_styled "PRIMARY" "   $(get_message "- https://github.com/Boog900/monero-ban-list/blob/main/ban_list.txt" "- https://github.com/Boog900/monero-ban-list/blob/main/ban_list.txt")"
    echo
    print_styled "WARNING" "$(get_message " ⚠️  Configurer votre router/Box internet pour REDIRIGER le port 22 et 18080" " ⚠️   Configure your router/internet box to REDIRECT port 22 and 18080")"
   print_styled "WARNING" "$(get_message "    vers l'ADRESSE IP de votre PC" "    to your PC's IP ADDRESS")"
   print_styled "PRIMARY" "$(get_message "- https://github.com/kerlannXmr/EasyMonerod/issues/10" "- https://github.com/kerlannXmr/EasyMonerod/issues/10")"
                echo

                read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..." "Press Enter to continue...")")"
}


monero_animation() {
    clear

    local logo_frame1="
      ████████████      
    ██            ██    
   ██   ██    ██   ██   
  ██    ███  ███    ██  
  ██    ██ ██ ██    ██  
  ██    ██    ██    ██  
  ██    ██    ██    ██  
   ██   ██    ██   ██   
    ██            ██    
      ████████████      
"

    local logo_frame2="
      ************      
    **            **    
   **   **    **   **   
  **    ***  ***    **  
  **    ** ** **    **  
  **    **    **    **  
  **    **    **    **  
   **   **    **   **   
    **            **    
      ************      
"

    local terminal_width=$(tput cols)
    local logo_width=24
    local center_x=$(( (terminal_width - logo_width) / 2 ))
    local top_y=3
    
    if [ $center_x -lt 0 ]; then
        center_x=0
    fi
    
    for ((i=0; i<8; i++)); do
        clear
        
        if ((i % 2 == 0)); then
            logo="${logo_frame1}"
            color="${COLORS[MONERO]}"  
        else
            logo="${logo_frame2}"
            color="${COLORS[PRIMARY]}"  
        fi
        
        tput cup $top_y $center_x
        echo -e "$color$logo${COLORS[RESET]}"
        
        sleep 0.3
    done
}

show_menu() {
    while true; do
        setup_terminal
        echo -e "\n\n\n\n\n\n\n\n"  
        
         
        print_styled "PRIMARY" "0) $(get_message "GUIDE" "HOW TO")"
        
        echo -e "\033[38;5;208m$(get_message "Menu Principal:" "Main Menu:")${COLORS[RESET]}"
        print_styled "PRIMARY" "1) $(get_message "Mise à jour système" "Update system")"
        print_styled "PRIMARY" "2) $(get_message "Installer Monero CLI" "Install Monero CLI")"
        print_styled "PRIMARY" "3) $(get_message "Installer service Tor" "Install configure Tor")"
        print_styled "PRIMARY" "4) $(get_message "Configurer bitmonero" "Configure bitmonero")"
        print_styled "PRIMARY" "5) $(get_message "Configurer DNS anonymes" "Configure anonymous DNS")"
        
        echo -e "\033[38;5;208m$(get_message "Option du Noeud sur Disque:" "Node Option on DISK:")${COLORS[RESET]}"

        print_styled "PRIMARY" "6) $(get_message "Blockchain sur DISQUE EXTERNE" "Blockchain on EXTERNAL DISK")"
        print_styled "PRIMARY" "7) $(get_message "Démontage du disque externe" "Unmount external disk")"

        echo -e "\033[38;5;208m$(get_message "BLOCKCHAIN" "BLOCKCHAIN")${COLORS[RESET]}"
        print_styled "PRIMARY" "8) $(get_message "MARCHE" "START")"
        print_styled "PRIMARY" "9) $(get_message "ARRET= ctrl+c" "STOP= ctrl+c")"
        
        echo -e "\033[38;5;208m$(get_message "AUTRES OPTIONS" "OTHER OPTIONS")${COLORS[RESET]}"
        print_styled "PRIMARY" "10) $(get_message "Changer language" "Change language")"
        print_styled "PRIMARY" "11) $(get_message "INFOS" "FEATURES")"
        print_styled "PRIMARY" "12) $(get_message "NOTES" "READ")"
        
        echo -e "\033[38;5;208m$(get_message "FIN" "END")${COLORS[RESET]}"
        print_styled "PRIMARY" "13) $(get_message "QUITTER" "EXIT")"
                
        echo -n "$(print_styled "INFO" "$(get_message "Choix (1-13): " "Choice (1-13): ")")"
        read -r choice

        case $choice in
              
            0) 
                Manuel
                ;;
            1) 
                update_system 
                ;;
            2)  
                if ! ask_username; then
                    continue
                fi
               
                install_monero_cli
                read -p "$(print_styled "PRIMARY" "$(get_message "Appuyez sur Entrée pour continuer..." "Press Enter to continue...")")"
                ;;
            3)  
                if ! ask_username; then
                    continue
                fi
                install_tor
                ;;
            4)  
                if ! ask_username; then
                    continue
                fi
                configure_monero
                ;;
            5) 
                configure_dns 
                ;;
            6)
                if ! ask_username; then
                    continue
                fi
                manage_blockchain
                ;;
            7) 
                unmount_sdb1 
                ;;
            8) 
                if ! ask_username; then
                    continue
                fi
                start_blockchain
                ;;
            9) 
        echo -n "$(print_styled "INFO" "$(get_message "Voulez-vous vraiment arrêter la blockchain? (o/n): " "Do you really want to stop the blockchain? (y/n): ")")"
read -r confirm
case $confirm in
    [OoYy]*)
        pkill -f monerod
        sudo systemctl stop haproxy-monero
        sudo systemctl stop monero-decoy
        sudo systemctl stop monero
        
        if pgrep -f monerod > /dev/null; then
            warning "$(get_message "Certains processus persistent, forçage de l'arrêt..." "Some processes still running, forcing shutdown...")"
            pkill -9 -f monerod
        fi
        
        success "$(get_message "Blockchain arrêtée" "Blockchain stopped")"
        ;;

        *)
                        continue
                        ;;
                esac
                ;;
            10) 
                select_language
                continue
                ;;
            11) 
                show_scripts 
                ;;
            12) 
                 
                show_notes 
                ;;
            13) 
                    clear
                     if ! monero_animation; then
                    continue
                fi
    setup_terminal
    echo -e "\n\n\n\n\n\n\n\n"  
    print_header "$(get_message "MERCI" "THANK YOU")"
    
    echo
    print_styled "SUCCESS" "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
    if [ "$LANG_CHOICE" = "FR" ]; then
        print_styled "SUCCESS" "┃                                                                             ┃"
        print_styled "SUCCESS" "┃  Programme d'aide informatique et de liberté.                               ┃"
        print_styled "SUCCESS" "┃  Permet d'installer un nœud MONERO sans aucune connaissance sur Linux.      ┃"
        print_styled "SUCCESS" "┃                                                                             ┃"
        print_styled "SUCCESS" "┃  Merci d'avoir utilisé ce programme.                                        ┃"
        print_styled "SUCCESS" "┃                                                                             ┃"
        print_styled "MONERO"  "┃                           🔒 PRIVACY MATTERS 🔒                             ┃"
    else
        print_styled "SUCCESS" "┃                                                                             ┃"
        print_styled "SUCCESS" "┃  Computer assistance and freedom program.                                   ┃"
        print_styled "SUCCESS" "┃  Helps you install a MONERO node without any knowledge on Linux.            ┃"
        print_styled "SUCCESS" "┃                                                                             ┃"
        print_styled "SUCCESS" "┃  Thank you for using this program.                                          ┃"
        print_styled "SUCCESS" "┃                                                                             ┃"
        print_styled "MONERO"  "┃                           🔒 PRIVACY MATTERS 🔒                             ┃"
    fi
    print_styled "SUCCESS" "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    echo
      
    sleep 3
    exit 0
    ;;
        esac
    done
}

setup_terminal
select_language
show_menu
exit 0
