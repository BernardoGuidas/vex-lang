# =========================
# VEX RUNTIME FINAL
# =========================

import sys
import builtins

VEX_ATIVO = False

# -------------------------
# COMANDOS VEX
# -------------------------

def scan(*args):
    if not VEX_ATIVO:
        print("[ERRO] vexcmd() não ativado")
        return
    print(*args)

def vexcmd():
    global VEX_ATIVO
    user = input("Usuário: ")
    senha = input("Senha: ")

    if user == "anonimo" and senha == "Vexprox":
        VEX_ATIVO = True
        print("[LOGIN] Acesso concedido ✔")
        print("╔══════════════════╗")
        print("║   VEX TERMINAL   ║")
        print("╚══════════════════╝")
    else:
        print("[LOGIN] Acesso negado ✖")

def vexscanpc():
    if not VEX_ATIVO:
        print("[ERRO] vexcmd() não ativado")
        return
    print("[SCAN] CPU: OK")
    print("[SCAN] MEMÓRIA: OK")
    print("[SCAN] DISCO: OK")

def trace_usuario():
    if not VEX_ATIVO:
        print("[ERRO] vexcmd() não ativado")
        return
    print("[TRACE] Usuário: root")
    print("[TRACE] Permissões: admin")

# -------------------------
# TRADUTOR VEX → PYTHON
# -------------------------

def traduzir_vex(codigo):
    linhas_py = []

    for linha in codigo.split("\n"):
        linha = linha.rstrip()

        if not linha or linha.strip().startswith("#"):
            continue

        # log = import
        if linha.startswith("log "):
            mod = linha.replace("log", "").strip()
            linhas_py.append(f"import {mod}")

        # trace usuario
        elif linha.strip() == "trace usuario":
            linhas_py.append("trace_usuario()")

        # scan vira print (mas com segurança VEX)
        elif linha.strip().startswith("scan"):
            linhas_py.append(linha)

        # comandos diretos
        elif linha.strip() in ("vexcmd()", "vexscanpc()"):
            linhas_py.append(linha)

        # TODO: resto é Python puro
        else:
            linhas_py.append(linha)

    return "\n".join(linhas_py)

# -------------------------
# EXECUTOR .VEX
# -------------------------

def executar_vex(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        codigo_vex = f.read()

    codigo_python = traduzir_vex(codigo_vex)

    exec(codigo_python, globals())

# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python vex_runtime.py arquivo.vex")
    else:
        executar_vex(sys.argv[1])