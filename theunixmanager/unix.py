#!/usr/bin/env python3
#
# Copyright (C) 2025 Archetypum
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>

try:
    import re
    import os
    import sys
    import typing
    import subprocess
except ModuleNotFoundError as import_error:
    print(f"[!] Error while loading python modules:\n{import_error}.")
    sys.exit(1)


class Globals:
    #
    # `tum` version:
    #
    VERSION: str = "0.0.1-stable"
    
    #
    # ANSI Color codes and text formatting:
    #
    BLACK: str = "\033[90m"
    WHITE: str = "\033[97m"
    YELLOW: str = "\033[93m"
    ORANGE: str = "\033[38;5;214m"
    BLUE: str = "\033[94m"
    CYAN: str = "\033[0;36m"
    PURPLE: str = "\033[95m"
    GREEN: str = "\033[92m"
    RED: str = "\033[91m"

    BG_BLACK: str = "\033[40m"
    BG_RED: str = "\033[41m"
    BG_GREEN: str = "\033[42m"
    BG_ORANGE: str = "\033[43m"
    BG_BLUE: str = "\033[44m"
    BG_MAGENTA: str = "\033[105m"
    BG_CYAN: str = "\033[46m"
    BG_WHITE: str = "\033[47m"

    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"
    REVERSED: str = "\033[7m"
    ITALIC: str = "\033[3m"
    CROSSED_OUT: str = "\033[9m"
    RESET: str = "\033[0m"
    
    #
    # Supported Package Managers:
    #
    SUPPORTED_PMS: typing.List[str] = [
        "apt",                          
        "apt-get",                      
        "apt-cache",                    
        "apt-cdrom",                    
        "apt-config",                   
        "apt-extracttemplates",         
        "apt-listchanges",              
        "apt-mark",                     
        "apt-sortpkgs",                 
        "aptitude",                     
        "aptitude-create-state-bundle", 
        "aptitude-run-state-bundle",    
        "apk",                          
        "dnf",                          
        "dpkg",                         
        "guix",                         
        "homebrew",                     
        "pkg",                          
        "pkgin",                        
        "pkg_add",                      
        "pkg_delete",                   
        "pkg_create",                   
        "pkg_info",                     
        "pacman",                       
        "yay",                          
        "pamac",                        
        "trizen",                       
        "portage",                      
        "qi",                           
        "slackpkg",                     
        "xbps",                         
        "yum",                          
        "zypper",                       
        "zypper-log",                   
    ]

    #
    # Supported Initialization Systems:
    #
    SUPPORTED_INITS: typing.List[str] = [
        "sysvinit",   
        "openrc",     
        "s6",         
        "runit",      
        "systemd",    
        "dinit",      
        "launchd",    
    ]
    
    #
    # Supported UNIX distributions:
    #
    DEBIAN_BASED: typing.List[str] = [
        # The universal operating system.
        # <https://www.debian.org/>

        "debian", "ubuntu", "xubuntu", "linuxmint", "lmde", "trisquel", "devuan", "kali", "parrotos", "popos", "elementaryos",
        "mx", "antix", "crunchbag", "crunchbag++", "pureos", "deepin", "zorinos", "peppermintos", "lubuntu", "kubuntu", "wubuntu",
        "astra", "tails", "ututos", "ulteo", "aptosid", "canaima", "corel", "dreamlinux", "elive", "finnix", "gibraltar",
        "linex", "kanotix", "kurumin", "linspire", "maemo", "mepis", "vyatta", "solusos", "openzaurus", "cutefishos", "knoppix",
        "siduction", "psychos", "neptune", "doglinux", "armbian", "droidian", "mobian", "grml", "backbox", "blacklablinux", "mmabuntus",
        "galliumos", "linuxschools", "linuxliteos", "mythbuntu", "solydxk", "uberstudent", "q4os", "demolinux", "libranet", "omoikane",
        "eagle", "college", "blackrhino", "luinux", "bonzai", "oralux", "demudi", "brlspeak", "censornet", "bluewall", "antemium",
        "knoppel", "skolelinux", "natures", "debxpde", "catix", "brlix", "parsix", "b2d", "troppix", "ging", "zonecd", "archeos",
        "insigne", "dzongkha", "boss", "resulinux", "epidemic", "clonezilla", "inquisitor", "musix", "satux", "pelicanhpc", "minino",
        "avlinux", "tangostudio", "doudou", "saline", "rebellin", "rescatux", "forlex", "proxmox", "wmlive", "point", "tanglu",
        "openmediavault", "vyos", "steamos", "metamorphose", "robolinux", "whonix", "storm", "linuxin", "kinneret", "wienux", "olive",
        "hymera", "spezzos", "primtux", "rebeccablackos", "uninvention", "handy", "selks", "linuxbbq", "kwheezy", "volumio", "raspbian",
        "osmc", "pibang", "sparky", "exe", "semplice", "venenux", "descentos", "martiux", "turnkey", "privatix", "estrellaroja", "untangle",
        "blankon", "webconverger", "swecha", "myrinix", "thisk", "64studio", "gnewsense", "gparted", "pardus", "genieos", "2x", "taprobane",
        "paipix", "amber", "beatrix", "santafe", "userlinux", "sunwah", "erposs", "munjoy", "smartpeer", "euronode", "kalango", "overclockix",
        "danix", "aslinux", "sphinxos", "condorux", "indilinux", "morphix", "clusterix", "mockup", "nepalinux", "slotech", "gnustep", "freeducsup",
        "adamantix", "trx", "freeduc", "slix", "pequelin", "quantian", "shabdix", "defender", "phlak", "std", "zopix", "clusterknoppix", "beernix",
        "eduknoppix", "roslims", "knoppix64", "slynux", "kaella", "knosciences", "beafanatix", "snappix", "ogoknoppix", "penguinsleuth", "augustux",
        "julex", "vmknoppix", "insert", "evinux", "xarnoppix", "llgp", "pilot", "slavix", "linespa", "klustrix", "knoppixmame", "bioknoppix", "knopils",
        "las", "feather", "livux", "featherweight", "lamppix", "damnsmall", "biadix", "hikarunix", "luit", "arabbix", "youresale", "xandros", "bayanihan",
        "caixamagica", "squiggleos", "miko", "guadalinex", "max", "xfld", "helix", "gnix", "esun", "xevian", "voyager", "ozos", "lliurex", "edubuntu",
        "impi", "nubuntu", "fluxbuntu", "ufficiozero", "swift", "vast", "commodore", "ubuntuce", "tuquito", "kiwi", "gos", "ultimate", "symphony",
        "earos", "runtu", "abuledu", "baltix", "debris", "moonos", "caine", "superos", "mangaka", "cae", "monomaxos", "zentyal", "masonux", "asturix",
        "element", "gnacktrack", "xpud", "vinux", "okatux", "dreamstudio", "pear", "luniux", "bodhi", "hybryde", "iqunix", "ubuntudp", "ubuntukylin",
        "makulu", "lite", "linuxfx", "peachosi", "emmabuntus", "cub", "auroraos", "suriyan", "bella", "chaletos", "ubuntumate", "kxstudio", "salentos",
        "centrych", "chitwanix", "ubuntugnome", "ozunity", "redo", "biolinux", "leeenux", "superx", "snowlinux", "arios", "pinguy", "madbox", "ubuntupr",
        "jolios", "wattos", "nexentastor", "deft", "kuki", "remnux", "lxle", "karoshi", "ubunturescue", "easypeasy", "nova", "qimo", "zevenos", "progex",
        "bardlinux", "extix", "ulite", "maryan", "greenie", "opengeu", "sabily", "protech", "comfusion", "ubuntustudio", "artistx", "shift", "freespire",
        "arabian", "poseidon", "alinex", "gnoppix", "openlx", "dynebolic", "molinux", "apodio", "biglinux", "tilix", "imagicos", "pioneer", "ichthux",
        "klikit", "tupiserver", "geolivre", "dizinha", "ankur", "linuxlte", "esware", "progeny", "liis", "muriqui", "loco",
    ]

    ARCH_BASED: typing.List[str] = [
        # A simple, lightweight distribution.
        # <https://www.archlinux.org/>
        
        "arch", "artix", "manjaro", "endeavouros", "garuda", "parabola", "hyperbola", "archbang", "blackarch", "librewolf", "archlabs",
        "chakra", "archex", "archman", "arco", "bluestar", "chimeraos", "instantos", "kaos", "rebornos", "archhurd", "cyberos", "archcraft",
        "cachyos", "ctlos", "crystallinux", "msys2", "obarun", "parchlinux", "snal", "steamos3", "tearchlinux", "uboslinux", "linhes", "underground",
        "kdemar", "archie", "faunos", "firefly", "linuxgamers", "kahelos", "netrunner", "ctkarch", "bridge", "sonar", "poliarch", "antergos",
    ]

    ALPINE_BASED: typing.List[str] = [
        # Small. Simple. Secure.
        # <https://www.alpinelinux.org/>
        
        "alpine", "postmarket",
    ]

    GENTOO_BASED: typing.List[str] = [
        # Welcome to Gentoo, a highly flexible, source-based Linux distribution.
        # <https://www.gentoo.org/>
        
        "gentoo", "argent", "pentoo", "funtoo", "calculate", "chromeosflex", "vidalinux", "knopperdisk", "gentoox", "sabayon", "chromiumos",
        "tinhatlinux", "ututo", "exgent", "flatcarlinux", "gentooplayer", "decibel", "liguros", "macaronilinux", "moccacinoos", "xenialinux",
        "redcorelinux", "porteuskiosk", "navynos", "ututo", "redwall", "papug", "toorox", "librete", "coreos", "shark", "zerahstar", "ibox",
        "gentooth", "mayix", "bicom", "bintoo", "phaeronix", "flash", "vlos", "systemrescue", "litrix", "iollix",
    ]

    VOID_BASED: typing.List[str] = [
        # Void is a general purpose operating system, based on the monolithic Linux kernel.
        # <https://www.voidlinux.org/>
    
        "void", "argon", "shikake", "pristine", "projecttrident",
    ]

    DRAGORA_BASED: typing.List[str] = [
        # Stable. Secure. Reliable.
        # <https://www.dragora.org/>

        "dragora",
    ]

    SLACKWARE_BASED: typing.List[str] = [
        # The Slackware Linux Project.
        # <http://www.slackware.com/>
        
        "slackware", "root", "evilentity", "blin", "stux", "jolinux", "netwosix", "connochaet", "salix", "ultima", "slackintosh", "slamd64", "easys",
        "topologilinux", "truva", "draco", "slackel", "cdlinux", "kongoni", "sms", "linvo", "rubix", "drinou", "bearops", "rip", "livecdrouter",
        "porteus", "austrumi", "wifislax", "absolute", "bluewhite64", "howtux", "pqui", "voltalinux", "slampp", "zenwalk", "zencafe", "imagineos",
        "darkstar", "openlab", "runt", "buffalo", "mutagenix", "klax", "lg3d", "nimblex", "dvl", "arudius", "alixe", "parslinux", "wolvix", "tumix",
        "saxenos", "nonux", "whoppix", "freepia", "slax", "supergamer", "vector", "plamo", "sentryfirewall",
    ]

    REDHAT_BASED: typing.List[str] = [
        # Red Hat is the leading provider of enterprise open source software solutions.
        # <https://www.redhat.com/>
    
        "rhel", "fedora", "mos", "rocky", "centos", "almalinux", "oraclelinux", "circlelinux", "clearos", "euleros", "nobara", "yellowdog", "bulinux",
        "elastix", "digantel", "nethserver", "baruwa", "stella", "asterisknow", "trixbox", "honeywall", "rockscluster", "smeserver", "tao", "niigata",
        "kondara", "laster5", "wow", "immunix", "startcom", "whitebox", "endian", "userful", "springdale", "holon", "superrescue", "lineox", "fermi",
        "scientific", "piebox", "wazobia", "tinysofa", "xos", "oeone", "planb", "voodoo", "medialab", "msc", "miracle", "hispafuentes", "mizi", "bluepoint",
        "redflag", "asianux", "cle", "linpus", "sot", "gelecek", "engarde", "thiz", "nuxone", "idms", "cool", "magic", "aurora", "lorma", "sulix", "ftosx",
        "hakin9", "opendesktop", "pingo", "freedows", "resala", "linare", "ingalum", "berry", "linuxxp", "atmission", "atomix", "nst", "ekaaty", "elpicx",
        "ezey", "korora", "olpc", "qubes", "bee", "fox", "dynasoft", "cpubuilders", "chapeau", "pidora", "hanthana", "fusion", "vortexbox", "ojuba", "mythdora",
        "asianlinux", "edulinux", "sci", "krud", "kore", "cobind", "happymac", "mylinux", "onet", "haansoft", "ezplanet", "rpmlive", "ares", "biobrew", "blag",
        "openna", "adios", "annyung", "linuxinstall", "phpsol", "aurox", "linuxplus", "jamd", "elx", "openwall", "k12linux", "asp", "tfm", "merdeka",
        "trustix", "wibni", "hancom", "xteam",
    ]

    OPENSUSE_BASED: typing.List[str] = [
        # The makers' choice for sysadmins, developers and desktop users.
        # <https://www.opensuse.org/>
        
        "opensuse", "suse", "geckolinux", "linuxkamarada", "united", "kmlinux", "sunjds", "urix", "sle", "karamad", "jacklab", "stresslinux",
    ]

    GUIX_BASED: typing.List[str] = [
        # A complete GNU operating system harnessing all the capabilities of the Guix software. Spawned by Guix itself.
        # <https://guix.gnu.org/>
        
        "guix",
    ]

    FREEBSD_BASED: typing.List[str] = [
        # FreeBSD is an operating system used to power modern servers, desktops, and embedded platforms.
        # <https://www.freebsd.org/>
        
        "freebsd", "midnightbsd", "ghostbsd", "bastillebsd", "cheribsd", "dragonflybsd", "trueos", "hardenedbsd", "hellosystem", "picobsd", "nanobsd",
        "truenas", "nomadbsd", "clonos", "junosos", "xigmanas", "opnsense", "pfsense", "cellos", "orbisos", "zrouter", "ulbsd", "ravynos", "freenas",
        "fireflybsd", "freesbie", "desktopbsd", "frenzy", "rofreesbie", "ging", "triance", "gulicbsd", "monowall", "pcbsd", "nas4free", "bsdrp",
    ]

    OPENBSD_BASED: typing.List[str] = [
        # Only two remote holes in the default install, in a heck of a long time!
        # <https://www.openbsd.org/>
        
        "openbsd", "adj", "libertybsd", "bitrig", "bowlfish", "ekkobsd", "embsd", "fabbsd", "fuguita", "marbsd", "microbsd", "commixwall", "bsdanywhere",
        "miros", "olivebsd", "psygnat", "quetzal", "sonafr", "hyperbolabsd", "aeriebsd", "anonymos", "utmfw", "gnobsd",
    ]

    NETBSD_BASED: typing.List[str] = [
        # NetBSD is a free, fast, secure, and highly portable Unix-like Open Source operating system.
        # <https://www.netbsd.org/>
        
        "netbsd", "blackbsd", "edgebsd", "seos", "os108", "jibbed", "fdgw", "g4u", "irbsd", "smolbsd",
    ]

    SOLARIS_ILLUMOS_BASED: typing.List[str] = [
        # Oracle Solaris is the trusted business platform that you depend on. Oracle Solaris gives you consistent compatibility, is simple to use, and is designed to always be secure.
        # <https://www.oracle.com/solaris/solaris11/>
        #
        # Unix OS which provides next-generation features for downstream distros, including advanced system debugging, next generation filesystem, networking, and virtualization options
        # <https://www.illumos.org/>
    
        "solaris", "illumos", "opensolaris", "openindiana", "omnios", "tribblix", "smartos", "nexenta", "belenix", "milax", "nexentasor", "schillix",
        "xstreamos",
    ]

    MACOS_BASED: typing.List[str] = [
        # If you can dream it, Mac can do it.
        # <https://www.apple.com/macos>
        
        "macos", "darwin", "xnu", "osx",
    ]


def is_debian_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Debian-based.

    Args:
        distro (str): The name of the GNU/Linux distribution to check (e.g., "ubuntu", "debian").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["debian", "ubuntu", "linuxmint"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["debian", "ubuntu", "linuxmint"]
        >>> is_debian_based("Ubuntu", base_list)
        True

        >>> is_debian_based("fedora", base_list)
        False
    """

    return distro.lower() in base_distros


def is_arch_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Arch-based.

    Args:
        distro (str): The name of the GNU/Linux distribution to check (e.g., "arch", "artix").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["arch", "artix", "archcraft"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["arch", "artix", "archcraft"]
        >>> is_arch_based("Arch", base_list)
        True

        >>> is_debian_based("fedora", base_list)
        False
    """

    return distro.lower() in base_distros


def is_alpine_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Alpine-based.

    Args:
        distro (str): The name of the Linux distribution to check (e.g., "alpine", "postmarketos").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["alpine", "postmartketos"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["alpine", "postmarketos"]
        >>> is_alpine_based("Alpine", base_list)
        True

        >>> is_alpine_based("fedora", base_list)
        False
    """

    return distro.lower() in base_distros


def is_gentoo_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Gentoo-based.

    Args:
        distro (str): The name of the GNU/Linux distribution to check (e.g., "gentoo", "pentoo", "funtoo").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["gentoo", "funtoo"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["gentoo", "funtoo"]
        >>> is_alpine_based("Gentoo", base_list)
        True

        >>> is_alpine_based("fedora", base_list)
        False
    """

    return distro.lower() in base_distros


def is_void_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Void-based.

    Args:
        distro (str): The name of the GNU/Linux distribution to check (e.g., "void").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["void", "projecttrident"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["void", "projecttrident"]
        >>> is_void_based("Void", base_list)
        True

        >>> is_void_based("ubuntu", base_list)
        False
    """

    return distro.lower() in base_distros


def is_dragora_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Dragora-based.

    Args:
        distro (str): The name of the GNU/Linux distribution to check (e.g., "dragora").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["dragora"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["dragora"]
        >>> is_dragora_based("Dragora", base_list)
        True

        >>> is_dragora_based("slackware", base_list)
        False
    """

    return distro.lower() in base_distros


def is_slackware_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Slackware-based.

    Args:
        distro (str): The name of the GNU/Linux distribution to check (e.g., "slackware").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["slackware", "slax", "zenwalk"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["slackware", "slax", "zenwalk"]
        >>> is_slackware_based("Slackware", base_list)
        True

        >>> is_slackware_based("debian", base_list)
        False
    """

    return distro.lower() in base_distros


def is_redhat_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Red Hat-based.

    Args:
        distro (str): The name of the GNU/Linux distribution to check (e.g., "fedora", "centos").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["redhat", "fedora", "centos", "rhel"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["redhat", "fedora", "centos", "rhel"]
        >>> is_redhat_based("Fedora", base_list)
        True

        >>> is_redhat_based("arch", base_list)
        False
    """

    return distro.lower() in base_distros


def is_guix_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Guix-based.

    Args:
        distro (str): The name of the GNU/Linux distribution to check (e.g., "guix").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["guix"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["guix"]
        >>> is_guix_based("Guix", base_list)
        True

        >>> is_guix_based("ubuntu", base_list)
        False
    """

    return distro.lower() in base_distros


def is_freebsd_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is FreeBSD-based.

    Args:
        distro (str): The name of the distribution to check (e.g., "freebsd", "ghostbsd").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["freebsd", "ghostbsd", "midnightbsd"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["freebsd", "ghostbsd", "midnightbsd"]
        >>> is_freebsd_based("FreeBSD", base_list)
        True

        >>> is_freebsd_based("netbsd", base_list)
        False
    """

    return distro.lower() in base_distros


def is_openbsd_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is OpenBSD-based.

    Args:
        distro (str): The name of the distribution to check (e.g., "openbsd").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["openbsd", "hyperbolabsd"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["openbsd", "hyperbolabsd"]
        >>> is_openbsd_based("OpenBSD", base_list)
        True

        >>> is_openbsd_based("netbsd", base_list)
        False
    """

    return distro.lower() in base_distros


def is_netbsd_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is NetBSD-based.

    Args:
        distro (str): The name of the distribution to check (e.g., "netbsd").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["netbsd", "smolbsd"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["netbsd", "smolbsd"]
        >>> is_netbsd_based("NetBSD", base_list)
        True

        >>> is_netbsd_based("freebsd", base_list)
        False
    """

    return distro.lower() in base_distros


def is_solaris_illumos_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given distribution is Solaris/Illumos-based.

    Args:
        distro (str): The name of the distribution to check (e.g., "illumos", "openindiana").
        base_distros (List[str]): A list of base distributions to compare against (typically lowercase names like ["solaris", "illumos", "openindiana"]).

    Returns:
        bool: True if the distro is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["solaris", "illumos", "openindiana"]
        >>> is_solaris_illumos_based("illumos", base_list)
        True

        >>> is_solaris_illumos_based("debian", base_list)
        False
    """

    return distro.lower() in base_distros


def is_macos_based(distro: str, base_distros: typing.List[str]) -> bool:
    """
    Check if a given system is macOS-based.

    Args:
        distro (str): The name of the operating system to check (e.g., "macos", "darwin").
        base_distros (List[str]): A list of base systems to compare against (typically lowercase names like ["macos", "darwin", "osx"]).

    Returns:
        bool: True if the system is in the base_distros list, False otherwise.

    Example:
        >>> base_list = ["macos", "darwin", "osx"]
        >>> is_macos_based("macOS", base_list)
        True

        >>> is_macos_based("linux", base_list)
        False
    """

    return distro.lower() in base_distros


def get_user_distro() -> typing.Optional[str]:
    """
    Attempt to detect the user's operating system distribution.

    This function tries to determine the distribution name by reading
    from the `/etc/os-release` file. It first checks for the `ID_LIKE`
    field (which provides a family-like identifier, e.g., "debian"),
    and falls back to `ID` if `ID_LIKE` is not present.

    If the file is missing or unreadable (e.g., on non-GNU/Linux systems),
    the user is prompted to manually input the distribution name.
    The input is validated to only contain safe characters.

    Returns:
        Optional[str]: The detected or user-provided distribution name in lowercase, or `None` if detection fails and user input is empty or invalid.

    Example:
        >>> get_user_distro()
        'debian'

        # If /etc/os-release is not available:
        [==>] Write your OS yourself: Void
        'void'
    """

    try:

        with open("/etc/os-release") as release_file:
            for line in release_file:
                if line.startswith("ID_LIKE="):
                    return line.split("=", 1)[1].strip().lower()
                if line.startswith("ID="):
                    return line.split("=", 1)[1].strip().lower()

    except FileNotFoundError:
        print(f"{Globals.RED}[!] Error: Cannot detect distribution from '/etc/os-release'.{Globals.RESET}")
        while True:
            name: str = input("[==>] Write your OS yourself: ").strip().lower()
            if name and re.match(r"^[\w@.+:/=-]+$", name):
                return name

            print(f"{Globals.RED}[!] Invalid input. Please enter a valid distro name.{Globals.RESET}")

    return None


def get_pid1_comm() -> typing.Optional[str]:
    """
    Get the name of the command running as PID 1 (the init system).

    This function uses the `ps` command to retrieve the `comm` (command name)
    of the process with PID 1. This is commonly used to detect the init system
    in use (e.g., "systemd", "init", "runit", "s6-svscan", etc.).

    Returns:
        Optional[str]: The command name of PID 1 if detected successfully, or None if the command fails.

    Example:
        >>> get_pid1_comm()
        'systemd'
    """

    result: bytes

    try:
        result = subprocess.check_output(["ps", "-p", "1", "-o", "comm="], stderr=subprocess.DEVNULL)
        return result.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return None


def get_init_system() -> str:
    """
    Detect the init system used by the current operating system.

    This function attempts to determine the init system by:
    - Checking the presence of well-known init-related directories.
    - Using the command name of PID 1 (via `get_pid1_comm()`).

    Returns:
        str: The name of the detected init system. One of:
            - "systemd"
            - "openrc"
            - "sysvinit"
            - "s6"
            - "runit"
            - "dinit"
            - "launchd"
            - "unknown" (if none matched)

    Example:
        >>> get_init_system()
        'systemd'
    """

    pid1_comm: typing.Optional[str]
    
    pid1_comm = get_pid1_comm()
    if os.path.isdir("/run/systemd/system") or pid1_comm == "systemd":
        return "systemd"

    if os.path.isdir("/etc/init.d") and os.path.exists("/etc/init.d/openrc"):
        return "openrc"

    if os.path.isdir("/etc/init.d"):
        return "sysvinit"

    if os.path.isdir("/etc/s6"):
        return "s6"

    if os.path.isdir("/etc/runit"):
        return "runit"

    if pid1_comm == "dinit":
        return "dinit"

    if pid1_comm == "launchd":
        return "launchd"

    return "unknown"


def clear_screen() -> None:
    """
    Clear the terminal screen using the `clear` command.

    This function attempts to run the `clear` command via subprocess.
    If the command fails (e.g., command not found or subprocess error), it prints a warning message to the user.

    Returns:
        None

    Example:
        >>> clear_screen()
        # Clears the terminal, or prints a warning if it fails.
    """

    try:
        subprocess.run(["clear"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Globals.YELLOW}[!] Warning: Failed to clear the screen.{Globals.RESET}")


def prompt_user(prompt: str, default: str = "N") -> bool:
    """
    Prompt the user with a yes/no question and return their response as a boolean.

    If the user enters nothing, the `default` value is used instead.
    Accepts flexible variations of "yes" (e.g., "y", "ye", "yes").

    Args:
        prompt (str): The prompt message to display to the user.
        default (str): The default answer if the user provides no input. 
                       Should be "y" or "n" (case-insensitive). Defaults to "N".

    Returns:
        bool: True if the user answered yes, False otherwise.

    Example:
        >>> prompt_user("Do you want to continue?", default="Y")
        Do you want to continue? (y/n): y
        True
    """

    user_input: str
    
    user_input = input(f"{prompt} (y/n): ").strip().lower()
    if not user_input:
        user_input = default.lower()

    return user_input in ["y", "ye", "es", "yes"]


def check_privileges() -> None:
    """
    Check if the script is running with root privileges.

    This function verifies that the effective user ID is 0 (root).
    If not, it prints an error message and exits the program with status code 1.

    Returns:
        None

    Example:
        >>> check_privileges()
        [!] Error: This script requires root privileges to work.
        # Script exits with code 1 if not run as root.
    """

    if os.geteuid() != 0:
        print(f"{Globals.RED}[!] Error: This script requires root privileges to work.{Globals.RESET}")
        sys.exit(1)
