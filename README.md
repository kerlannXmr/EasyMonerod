[![contact_Mail](https://img.shields.io/badge/✉️_Email-FF6600?style=flat&logoColor=white)](mailto:easynode@kerlann.org)
[![GitHub-page](https://img.shields.io/badge/Page--EN-FF6600?style=flat&logo=github&logoColor=white)](https://easynode.kerlann.org)
[![GitHub-page](https://img.shields.io/badge/Page--FR-FF6600?style=flat&logo=github&logoColor=white)](https://easynode.kerlann.org/fr.html)
[![Monero-ecosystem](https://img.shields.io/badge/🧭_Monero.eco-FF6600?style=flat&logoColor=white)](https://monero.eco)


<div align="center"><img src="picture/banniere5.svg" width="900" height="100" alt="Monero EasyNode top"></div>

<div align="center">

## Make easy a MONERO Node 

<img src="picture/xxmr.gif" width="300" height="300" alt="Monero EasyNode Logo">

<br>
<br>

[▶️ Demo video](https://mega.nz/file/5uFzVRKR#w2RehS8LNruoM7A1vxnJPIm3ipjif1EYL_hg4MMoYW0) *("Open in new tab")*

</div>

<hr style="border-top: 3px solid orange;">
<b>'EasyNode'</b> simplifies the installation of a <b> 'MONERO node' </b> , allowing you to configure your blockchain in just a few clicks. A complete setup in less than 10 minutes!

Then download its blockchain ⬇️ ...

Finally, start your adventure, you are sovereign...

You can use it in 🐧Linux versions or 🪟 windows  10/11 in wsl version. 

No knowledge required. Select step 1➡️2➡️3➡️4➡️5 and you're done. 
After Boot to your internal drive, 6️⃣, or move the blockchain to your external disk, 8️⃣.

The node is protected by Tor and an onion address allows you to connect to a mobile wallet.
An SSH onion address is available to access the node remotely.
Added the 'MRL' IP bann list of 'boog900'.

🇬🇧 English- 🇫🇷French

Enjoy.

## <div align="center">🖥️ Interface:</div>
<div align="center">
<!--<img src="picture/linux-interface.png" width="310" alt="Linux Interface">-->
<img src="picture/wsl_interface.png" width="285" height="430" alt="wsl Interface">
<img src="picture/wsl.gif" width="500" height="430" alt="wsl Interface">

  <b> SSH REMOTE:</b>
<br>

<img src="picture/ssh.jpg" width="285" alt="Démo">
<img src="picture/SSH.gif" width="430" height="470" alt="Démo">

<br>
<br>

[![EasyNode Monero](picture/play-button.svg)](https://mega.nz/file/5uFzVRKR#w2RehS8LNruoM7A1vxnJPIm3ipjif1EYL_hg4MMoYW0) 

<a>right click + "Open in new tab"</a>

 <br>

</div>

## <div align="center">📝 HOW TO</div>

### Internal disk :
- Follow the step 1➡️2➡️3➡️4➡️5
- Then do : Step 6️⃣

### External Disk :
- Follow the step 1➡️2➡️3➡️4➡️5
- Then do : Step 8️⃣ and 6️⃣

## <div align="center">📥 Download:</div>
<div align="center">
  
⇨ 📂 Into path: `/home/$user`
</div>

<div align="center">

| Version | Links |
|---------|------|
| 🐧 Linux | [![Linux](https://img.shields.io/badge/Download-EasyNode_Linux-orange?style=for-the-badge)](https://github.com/kerlannXmr/EasyMonerod/releases/download/v3/easynode_linux.sh) |
| 🪟 WSL | [![WSL](https://img.shields.io/badge/Download-EasyNode_WSL-orange?style=for-the-badge)](https://github.com/kerlannXmr/EasyMonerod/releases/download/v3/easynode_wsl.sh) |
</div>

## <div align="center">🚀 Installation</div>
### 🔒 IP ban_list: (spy, malicius)

◇  Automatic updated 'IP ban-list' in this folder :
-  `/home/$user/.bitmonero`

( Updated: github.com/Boog900/monero-ban-list/blob/main/ban_list.txt )

## 🐧 Linux : Debian, Ubuntu derivatives, Others...

[View issue: Linux installation FR](https://github.com/kerlannXmr/EasyMonerod/issues/7) *(right click + "Open in new tab")*
### ↪️ Download & Install & run script:

- ⚡Beginner users: copy&paste in new terminal

```bash
wget https://github.com/kerlannXmr/EasyMonerod/releases/download/v3/easynode_linux.sh -O easynode_linux.sh && chmod +x easynode_linux.sh && sudo ./easynode_linux.sh
```

- Normal users: copy&paste in new terminal

```bash
sudo wget -P ~ https://github.com/kerlannXmr/EasyMonerod/releases/download/v3/easynode_linux.sh
```
(script goes in folder) " /home/$user "

### ➡️Make it executable

```bash
sudo chmod +x easynode_linux.sh
sudo ./easynode_linux.sh
```

## 🪟 Windows 10/11 (WSL2) :
### ⚫ 1) Verify WSL2 :

-🔺 Make sure virtualization is enabled in bios: Tape in powershell Administrator :

↳ ` Get-ComputerInfo -Property "HyperV*" ` = True ✅

-🔺 Make sure you already have <b>WSL2</b>:

↳ `wsl --list --verbose` [👉 View issue](https://github.com/kerlannXmr/EasyMonerod/issues/4#issue-2873484919) *(right click + "Open in new tab")*

### ⚫ 2) Install Ubuntu:
-🔷 Go to <b>Microsoft Store</b>, then in search type Ubuntu, click on Ubuntu 24LTS.

Other:

-🔶  <b>In powershell administrator:</b>
```bash
wsl --install
```
learn.microsoft.com/fr-fr/windows/wsl/install

learn.microsoft.com/en-us/windows/wsl/install

### ⚫ 3) Download & Install <b>script</b> : 
/home/$user

```bash
sudo wget -P ~ https://github.com/kerlannXmr/EasyMonerod/releases/download/v3/easynode_wsl.sh
```
Make it executable
```bash
sudo chmod +x easynode_wsl.sh
sudo ./easynode_wsl.sh
```

## <div align="center">⚡ Features</div>

- ✅ Automated installation
- ✅ allow firewall port
- ✅ Monero configuration
- ✅ Disk management (internal/external)
- ✅ Built-in Tor (Tor/SSH onion address)
- ✅ Anonymous DNS
- 🔒 Block IP 'ban listed' (MRL) [👉Issue](https://github.com/kerlannXmr/EasyMonerod/issues/3#issue-2871012436)*(right click + "Open in new tab")*          
- 🔒 TOR SSH remote access :  [👉Issue](https://github.com/kerlannXmr/EasyMonerod/issues/2#issue-2870954425)*(right click + "Open in new tab")*                              
- ✅ Intuitive user interface
- ✅ no knowledge required

## <div align="center">⚠️ Important</div>

-➡🟧 REDIRECT port 22 and 18080 from your internet router to your ' local ip ' of your PC.

-18080 allows other Monero nodes to connect to your node, increasing the decentralization and resilience of the network. [👉Issue](https://github.com/kerlannXmr/EasyMonerod/issues/10)

-➡🟧 The external hard drive must be formatted in NTFS (classic) or exFat or ext4.

Because FAT doesn't handle files larger than 4 GB!  [👉Issue](https://github.com/kerlannXmr/EasyMonerod/issues/9)    

-➡📗  Remote access wallet:
  
  Take 'cake wallet', settings, connect and sync, manage nodes, add +, node address= onion Tor, node port= 18089, save. Close and open. Wait the sync.

  or

  Take "Monero Gui", choose "Distant Mode" then " + add new node " and write 'IP local' or 'IP WEB' and port " 18089 "
  
-➡📗  Remote access ssh, port 22:
   
  Open terminal pc or take 'Termux' on android: ' ssh username@local_ip_pc ' . Or ' ssh username@onion_ssh_address '.[👉Issue](https://github.com/kerlannXmr/EasyMonerod/issues11) 
    
-➡🟧 Stop the Blockchain : CTRL+C 

## <div align="center">🔄 Compatibility</div>

<div align="center">
<br>
  
| Distribution | Compatibilité | Notes |
|--------------|---------------|-------|
|      ✅      |       ✅      |     ✅ |

</div>

 **Shell scripts ' EasyNode 'use standard commands that are more portable across different Linux distributions.**
<br>
-➡📗[👉View Issue Distribution compatibility](https://github.com/kerlannXmr/EasyMonerod/issues/8)*(right click + "Open in new tab")*  
<br>
<br>

## <div align="center">🔰 Packages installed by EASYNODE</div>

<br>

- 📝   See the list of packages at this issue [👉PACKAGES list pre-installed ](https://github.com/kerlannXmr/EasyMonerod/issues/6)*(right click + "Open in new tab")*

<br>

## <div align="center">☣️ EasyNode Scripts TEST report</div>

<div align="center">

### Security Scan Results

Audits are performed using VirusTotal and MetaDefender.

| Category | Description | Tools | Status |
|----------|-------------|-------|--------|
| 🔒 Security | Vulnerabilities, malware detection, backdoors | VirusTotal, MetaDefender | ✅ |
| 🐛 Code Issues | Logic flaws, syntax errors, risky patterns | Static Analysis | ✅ |
| 🔍 Behavior | Runtime actions, system modifications, network activity | Dynamic Analysis | ✅ |
| 🔧 Resource Usage | File system access, memory/CPU utilization | MetaDefender | ✅ |
| 📡 Network | Suspicious connections, data exfiltration attempts | VirusTotal | ✅ |
| 💾 File Operations | Dangerous file manipulations, unexpected changes | Both Tools | ✅ |

<br>
  
 <b>Right click + "Open in new tab" to view scann results </b>

| Script | VirusTotal | MetaDefender |
|--------|------------|--------------|
| EasyNode_linux | [![Scan EasyNode_linux with VirusTotal](https://img.shields.io/badge/scan%20Easynode_linux%20with-VirusTotal-brightgreen)](https://www.virustotal.com/gui/url/f647e9bd7a152cab3537fe5130d7b57c6112cec021c73c35403fb6936d0b625c?nocache=1) | [![Scan EasyNode_linux with MetaDefender](https://img.shields.io/badge/scan%20Easynode_linux%20with-MetaDefender-brightgreen)](https://metadefender.com/results/url/aHR0cHM6Ly9naXRodWIuY29tL2tlcmxhbm5YbXIvRWFzeU1vbmVyb2QvcmVsZWFzZXMvZG93bmxvYWQvdjMvZWFzeW5vZGVfbGludXguc2g=) |
| EasyNode_wsl | [![Scan easyNode_wsl with VirusTotal](https://img.shields.io/badge/scan%20Easynode_wsl%20with-VirusTotal-brightgreen)](https://www.virustotal.com/gui/url/e1621216f4ef4f9a5a1aa0651d1717b9c4047473d9b040cc047341369df3cb46?nocache=1) | [![Scan EasyNode_wsl with Metadefender](https://img.shields.io/badge/scan%20Easynode_wsl%20with-metaDefender-brightgreen)](https://metadefender.com/results/url/aHR0cHM6Ly9naXRodWIuY29tL2tlcmxhbm5YbXIvRWFzeU1vbmVyb2QvcmVsZWFzZXMvZG93bmxvYWQvdjMvZWFzeW5vZGVfd3NsLnNo) |

</div>

<br>

## 💬  Contact

[![contact_session](https://img.shields.io/badge/💲_SESSION-FF6600?style=flat&logoColor=white)](mailto:0595c16adb0e1f467740b5bb4d7e51c8b25042695bc4bd9ebd2e66902720dcbb02)
[![contact_Matrix](https://img.shields.io/badge/✳️_Matrix-FF6600?style=flat&logoColor=white)](https://matrix.to/#/!diwbZJBzNngFIyfVVh:matrix.org?via=matrix.org)
[![contact_Simplex](https://img.shields.io/badge/👥_Simplex-FF6600?style=flat&logoColor=white)](https://simplex.chat/contact#/?v=2-7&smp=smp%3A%2F%2F0YuTwO05YJWS8rkjn9eLJDjQhFKvIYd8d4xG8X1blIU%3D%40smp8.simplex.im%2FhVfnrjb6LGrdWF8dcfEO_3funYfYrCsm%23%2F%3Fv%3D1-3%26dh%3DMCowBQYDK2VuAyEA6eMOBbH4MauXsCWIaZO8r1P7QPCorbwiOSHz0rofgUI%253D%26srv%3Dbeccx4yfxxbvyhqypaavemqurytl6hozr47wfc7uuecacjqdvwpw2xid.onion&data=%7B%22type%22%3A%22group%22%2C%22groupLinkId%22%3A%22IB1UQAdA78A2sbjixkya_g%3D%3D%22%7D)
[![contact_Mail](https://img.shields.io/badge/✉️_Email-FF6600?style=flat&logoColor=white)](mailto:easynode@kerlann.org)

## ♠️ Support

- 📝 Consult F.A.Q. [👉Questions](https://github.com/kerlannXmr/EasyMonerod/issues/5)*(right click + "Open in new tab")*
- 📝 Consult the [👉Documentation](https://tinyurl.com/kerlann)*(right click + "Open in new tab")*

## 🫶 Thankful

- 🧭 Thanks [👉Monero eco-system](https://monero.eco)*(right click + "Open in new tab")*
- 🇫🇷 Thanks [👉unbanked0](https://github.com/Unbanked0)*(right click + "Open in new tab")*


<div align="center">

---
### 🙏 <b>Make donnation with 'cake wallet' to : ' kerlann.xmr '</b>🙏
<div align="center"><img src="picture/qrcode1.gif"  alt="wsl Interface"></div>
or fundraiser

[![contact_xmrchat](https://img.shields.io/badge/✨_XmrChat-FF6600?style=flat&logoColor=white)](https://xmrchat.com/easymonerod)
[![contact_kuno](https://img.shields.io/badge/🔥_Kuno-FF6600?style=flat&logoColor=white)](https://kuno.anne.media/fundraiser/dkbu)

---


Made with ❤️ by [KerlannXmr](https://github.com/kerlannXmr)

</div>
<div align="center"><img src="picture/monero.gif" width="190" height="60" alt="wsl Interface"></div>
