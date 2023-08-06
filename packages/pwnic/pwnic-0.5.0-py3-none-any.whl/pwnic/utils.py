import re
import subprocess
from pathlib import Path


def install_package(package_name: str) -> bool:
    if re.search(r"[|&;\\]", package_name):
        return False
    package_name = re.sub(r"\s+", "", package_name)

    command = f"pip install {package_name}"
    print(f"running `{command}`")
    if subprocess.run(
        ["pip", "install", package_name], shell=False
    ).returncode:
        return False
    return True


def ensure_certs() -> tuple[str, str]:
    certdir = Path("cert")

    try:
        keyfile = next(certdir.glob("*key*"))
    except StopIteration:  # if no key, generate it
        print("Generating a key for self-signing")
        subprocess.run(
            args=[
                "openssl",
                "genpkey",
                "-algorithm",
                "RSA",
                "-out",
                "cert/key.pem",
                "-pkeyopt",
                "rsa_keygen_bits:4096",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        keyfile = next(certdir.glob("*key*"))

    try:  # check if there's a cert already
        certfile = next(certdir.glob("*cert*"))
    except StopIteration:  # if not, check for a key
        print("Generating a self-signed certificate")
        subprocess.run(
            args=[
                "openssl",
                "req",
                "-new",
                "-x509",
                "-sha256",
                "-key",
                "cert/key.pem",
                "-out",
                "cert/cert.pem",
                "-days",
                "30",
                "-subj",
                "/CN=pwnic",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        certfile = next(certdir.glob("*cert*"))

    return str(keyfile.resolve()), str(certfile.resolve())


def get_ip_addresses() -> list[str]:
    sub = subprocess.run(
        ["hostname", "--all-ip-addresses"], stdout=subprocess.PIPE
    )

    return sub.stdout.strip().decode().split("\n")
