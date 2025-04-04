# Ophiophagus hannah - scientific name for the King Kobra.
# Inspiration for the name of this Python Tool.
# Enumeration Tool created by - gOvX - github.com/GreatOverlordX

import os
import socket
import platform
import argparse
import subprocess
import psutil

# no function docstrings since functions are pretty obvious :)
def get_system_info():
    print("=== ◉ ◉ ◉ System Information ◉ ◉ ◉ ===\n")
    print(f"System -> {platform.system()}")
    print(f"Node Name -> {platform.node()}")
    print(f"Release -> {platform.release()}")
    print(f"Version -> {platform.version()}")
    print(f"Machine -> {platform.machine()}")
    print(f"Processor -> {platform.processor()}")

def get_network_info():
    print("\n === ◉ ◉ ◉ Network Info ◉ ◉ ◉ ===\n")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Hostname -> {hostname}")
    print(f"IP address -> {ip_address}")   
    # Network interfaces listing:
    addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in addrs.items():
        print(f"\nInterface -> {interface_name}")
        for address in interface_addresses:
            print(f"    Address -> {address.address}")
            print(f"    Netmask -> {address.netmask}")
            print(f"    Broadcast -> {address.broadcast}")

def get_installed_packages(verbose=False, count_only=False, outdated_only=False):
    print("\n=== Installed Packages ===\n")
    system = platform.system()
    packages = []
    outdated_packages = []

    try:
        # Linux System - enumeration
        if system == "Linux":
            if os.path.exists("/etc/debian_version"):
                # Debian-based distros
                result = subprocess.run(['dpkg-query', '-f', '${binary:Package}\n', '-W'], capture_output=True, text=True, check=False)
                if result.returncode != 0:
                    print(f"⚠ Warning ⚠ dpkg-query failed with return code {result.returncode} ⚠\nPackage list might be incomplete.\n")
                packages = result.stdout.strip().split('\n')
                if verbose or outdated_only:
                    try:
                        outdated_result = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True, check=True)
                        outdated_packages = [line.split()[0] for line in
                                            outdated_result.stdout.strip().split('\n')[1:]]  # Skips header
                    except subprocess.CalledProcessError as e:
                        print(f"⚠ Error retrieving outdated packages with {e} ⚠\n(There might not be any outdated packages)")
            elif os.path.exists("/etc/arch-release"):
                # Arch-based distros
                result = subprocess.run(['pacman', '-Q'], capture_output=True, text=True, check=False)
                if result.returncode !=0:
                    print(f"⚠ Warning - pacman -Q failed with return code{result.returncode} ⚠ package list might be incomplete\n")
                packages = result.stdout.strip().split('\n')
                if verbose or outdated_only:
                    try:
                        outdated_result = subprocess.run(['pacman', '-Qu'], capture_output=True, text=True, check=True)
                        outdated_packages = [line.split()[0] for line in outdated_result.stdout.strip().
                                            split('\n') if line.strip()]
                    except subprocess.CalledProcessError as e:
                        print(f"⚠ Error retrieving outdated packages with {e} ⚠\n\n(there might not be any outdated packages)\n")
            else:
                print("!!Unsupported Linux Distribution!!")
        elif system == "Windows":
            # Windows OS - using winget for package enumeration
            try:
                result = subprocess.run(['winget', 'list', '--accept-source-agreements'], capture_output=True, text=True, check=True)
                packages = [line.split()[0] for line in result.stdout.strip().split('\n')[2:]]  # Skips header lines
            except subprocess.CalledProcessError as e:
                print(f"⚠ Error retrieving installed packages with winget: {e} ⚠\n")

            # Windows does not have a direct equivalent for checking outdated packages AFAIK
            outdated_packages = []
        else:
            print(f"Oops! Unsupported Operating System -> {system}\n")
    # Error handling
    except FileNotFoundError as e:
        print(f"Error ⚠ A required file was not found: {e}\n")
    except OSError as e:
        print(f"OS Error ⚠ {e}\n")
    except Exception as e:
        print(f"Unexpected error retrieving installed packages ==> {e}\n")
        return
    # outputs packages with/without -c, -v or -o mode - for user friendly purposes
    if count_only:
        print(f"Number of installed packages ==> {len(packages)}")
    elif outdated_only:
        if outdated_packages:
            print("  ↓ OUTDATED PACKAGES  ↓\n")
            for package in outdated_packages:
                print(f"\n❯❯ ⚠ {package} ⚠\n")
        else:
            print("☰☰NO OUTDATED package was found ☰☰\n")
    elif verbose:
        if outdated_packages:
            print(" ↓ INSTALLED PACKAGES ↓ [ outdated packages are marked with ⚠ and ✖  ]\n")
        else:
            print(" ↓ INSTALLED PACKAGES ↓\n")
        for package in packages:
            if package in outdated_packages:
                print(f"⚠  -  {package}   ✖ ")  # ✖ is for outdated packages
            else:
                print(f"ℹ  - {package}")  # ℹ is for mere "info" symbolisation.
    else:
        for package in packages:
            print(package.split()[0])  # Print ONLY the package name

def main():
    parser = argparse.ArgumentParser(description="ophio.py --->> System Enumeration Tool")
    parser.add_argument('-s', '--system', action='store_true', help='Get system information')
    parser.add_argument('-n', '--network', action='store_true', help='Get network information')
    parser.add_argument('-p', '--packages', action='store_true', help='Get installed packages information')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output for installed packages')
    parser.add_argument('-c', '--count', action='store_true', help='Count of installed packages')
    parser.add_argument('-o', '--outdated', action='store_true', help='List only outdated packages')

    args = parser.parse_args()

    if not (args.system or args.network or args.packages):
        print("\nHold on, mate! No enumeration options specified!\nUse: [ -s / --system], [-n / --network], and/or [-p / --packages] with Its [-v / --verbose] [-c / --count] flags.\n")
        parser.print_help()
        return

    if args.system:
        get_system_info()
    if args.network:
        get_network_info()
    if args.packages:
        get_installed_packages(verbose=args.verbose, count_only=args.count, outdated_only=args.outdated)

if __name__ == "__main__":
    main()
