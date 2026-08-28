import subprocess
import os

def publish_to_web(commit_message="Publicación automática desde Community Manager"):
    """
    Ejecuta git add, commit y push a origin main.
    Esto dispara el despliegue automático en Netlify para que la página se actualice en vivo en < 1 min.
    """
    repo_dir = r"C:\Users\julio\dev\sitio-web-csd"
    try:
        # Git add
        res_add = subprocess.run(["git", "add", "."], cwd=repo_dir, capture_output=True, text=True)
        if res_add.returncode != 0:
            return False, f"Error en git add: {res_add.stderr}"

        # Git commit
        res_commit = subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_dir, capture_output=True, text=True)
        # Si no hay cambios que commitear no es error grave
        if "nothing to commit" in res_commit.stdout or "nada para hacer commit" in res_commit.stdout:
            print("No hay cambios pendientes para commit.")

        # Git push
        res_push = subprocess.run(["git", "push", "origin", "main"], cwd=repo_dir, capture_output=True, text=True)
        if res_push.returncode != 0:
            return False, f"Error al subir a GitHub (push): {res_push.stderr}"

        return True, "¡Publicado en vivo exitosamente! La página web csd.edu.co se actualizará en unos segundos."

    except Exception as e:
        return False, f"Excepción durante la publicación: {str(e)}"

if __name__ == "__main__":
    success, msg = publish_to_web("Prueba de módulo publicador")
    print(f"Resultado: {success} - {msg}")
