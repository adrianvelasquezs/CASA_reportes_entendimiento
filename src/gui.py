# Nombre de archivo: gui.py
# Guardar en la carpeta: src/
#
# @author: Adrian Esteban Velasquez Solano (Modificado por Gemini)
# @date: 10-2025
#
# Descripción: Esta es una interfaz gráfica (GUI) para gestionar el
# generador de reportes de CASA. Permite ejecutar la consolidación
# y la generación de reportes de forma secuencial.

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import os

# --- IMPORTANTE ---
# Importa la configuración de rutas PRIMERO
try:
    import path_config as paths
except ImportError:
    print("ERROR CRÍTICO: No se pudo encontrar path_config.py")
    # Este error debe mostrarse en la GUI si es posible
# Estos son los scripts de tu proyecto.
# Asumimos que 'gui.py' está en la misma carpeta 'src/'
try:
    import file_merger
    import program_report_generator
    import logger
except ImportError as e:
    messagebox.showerror("Error de Importación",
                         f"No se pudieron encontrar los scripts del proyecto.\n"
                         f"Asegúrate de que 'gui.py' esté en la carpeta 'src/' "
                         f"junto a 'file_merger.py' y 'program_report_generator.py'.\n"
                         f"Detalle: {e}")
    sys.exit(1)


class TextRedirector:
    """Redirige la salida de stdout/stderr a un widget de texto de Tkinter."""

    def __init__(self, widget, root):
        self.widget = widget
        self.root = root

    def write(self, s):
        # Usamos root.after() para asegurar que la actualización de la GUI
        # ocurra en el hilo principal de Tkinter, haciéndolo thread-safe.
        self.root.after(0, self.thread_safe_write, s)

    def thread_safe_write(self, s):
        """Método para escribir de forma segura en el widget de texto."""
        try:
            self.widget.configure(state='normal')
            self.widget.insert(tk.END, s)
            self.widget.see(tk.END)
            self.widget.configure(state='disabled')
        except tk.TclError:
            # Pasa si la ventana se cierra mientras se escribe
            pass

    def flush(self):
        # Requerido por la interfaz de stdout
        pass


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Reportes CASA")
        self.root.geometry("750x600")  # Tamaño (ancho x alto)

        # Configurar un estilo
        style = ttk.Style()
        style.theme_use('clam')  # 'clam', 'default', 'alt', 'classic'

        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 1. Frame de Instrucciones ---
        instrucciones_frame = ttk.LabelFrame(main_frame, text="Instrucciones", padding="10")
        instrucciones_frame.pack(fill=tk.X, expand=False, pady=5)

        instrucciones_texto = (
            "1. Asegúrese de que los archivos `base.xlsx` y `admitidos.xlsx` se encuentren en la carpeta `data/raw/`.\n"
            "2. Haga clic en '1. Consolidar Archivos' para unificar los datos. Espere a que termine.\n"
            "3. Una vez completada la consolidación, haga clic en '2. Generar Reportes'.\n"
            "4. Los archivos finales se guardarán en `data/procesada/` y `data/reportes/`.\n"
            "5. La consola de abajo mostrará el progreso y los posibles errores."
        )
        ttk.Label(instrucciones_frame, text=instrucciones_texto, justify=tk.LEFT).pack(fill=tk.X)

        # --- 2. Frame de Acciones ---
        acciones_frame = ttk.LabelFrame(main_frame, text="Acciones", padding="10")
        acciones_frame.pack(fill=tk.X, expand=False, pady=10)

        # Botones
        self.consolidar_btn = ttk.Button(acciones_frame,
                                         text="1. Consolidar Archivos",
                                         command=self.run_consolidar_task)
        self.consolidar_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.reportes_btn = ttk.Button(acciones_frame,
                                       text="2. Generar Reportes",
                                       command=self.run_reportes_task)
        self.reportes_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.limpiar_btn = ttk.Button(acciones_frame,
                                      text="Limpiar Consola",
                                      command=self.clear_log)
        self.limpiar_btn.pack(side=tk.RIGHT, fill=tk.X, expand=False, padx=5)

        # --- 3. Frame de Consola ---
        log_frame = ttk.LabelFrame(main_frame, text="Consola de Progreso", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, state='disabled', height=20, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # --- Redirigir stdout y stderr ---
        redirector = TextRedirector(self.log_area, self.root)
        sys.stdout = redirector
        sys.stderr = redirector

        print("Interfaz iniciada. Listo para comenzar.")
        print(f"Directorio de trabajo actual: {os.getcwd()}")
        print(f"Raíz del proyecto (PROJECT_ROOT): {paths.PROJECT_ROOT}")
        print(f"Buscando datos en: {paths.DATA_FOLDER}\n")

    def clear_log(self):
        """Limpia el área de la consola."""
        self.log_area.configure(state='normal')
        self.log_area.delete('1.0', tk.END)
        self.log_area.configure(state='disabled')
        print("Consola limpiada.\n")

    def start_task(self, task_function, button):
        """
        Inicia una función (task_function) en un hilo separado
        y deshabilita el botón (button) mientras corre.
        """
        button.config(state='disabled')
        self.clear_log()

        # Iniciar la tarea en un hilo para no congelar la GUI
        threading.Thread(target=self.task_wrapper,
                         args=(task_function, button),
                         daemon=True).start()

    def task_wrapper(self, task_function, button):
        """
        Envoltorio para las tareas que se ejecutan en hilos.
        Maneja el éxito/error y reactiva el botón.
        """
        try:
            print(f"--- Iniciando tarea: {task_function.__name__} ---\n")
            # Llama a la función principal (ej. file_merger.generate_consolidated_file)
            success = task_function()

            if success:
                print(f"\n--- TAREA COMPLETADA CON ÉXITO ---")
            else:
                print(f"\n--- TAREA FALLIDA (ver errores arriba) ---")

        except Exception as e:
            print(f"\n--- ERROR INESPERADO EN LA TAREA ---")
            print(f"Excepción: {e}")
            import traceback
            traceback.print_exc()  # Imprime el stack trace completo
        finally:
            # Reactiva el botón (de forma thread-safe)
            self.root.after(0, lambda: button.config(state='normal'))
            print(f"--- Proceso finalizado. ---")

    def run_consolidar_task(self):
        """Llama a la tarea de consolidación."""
        self.start_task(file_merger.generate_consolidated_file, self.consolidar_btn)

    def run_reportes_task(self):
        """Llama a la tarea de generación de reportes."""
        self.start_task(program_report_generator.generate_tables_graphs, self.reportes_btn)


# --- Punto de entrada principal ---
if __name__ == "__main__":
    # Validar que los scripts existan antes de lanzar la GUI
    if 'file_merger' in locals() and 'program_report_generator' in locals():
        # Inicializar la app
        root = tk.Tk()
        app = App(root)

        # Iniciar el bucle principal de la GUI
        root.mainloop()