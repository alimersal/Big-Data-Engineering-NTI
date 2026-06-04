#!/usr/bin/env python3
# =========================================================
# Hadoop HDFS & YARN Control Center - ULTIMATE UI
# Removed Advanced Tab - Clean Version - No Tooltips
# =========================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import queue
import os
import time
import webbrowser
from datetime import datetime

# =========================================================
# CONFIGURATION
# =========================================================
class Config:
    HADOOP_HOME = "/home/bigdata/hadoop-2.7.3"
    ANACONDA_HOME = "/home/bigdata/anaconda3"
    JAVA_HOME = "/usr/java/default"
    
    # PREMIUM FONTS
    FONT_MAIN = ("DejaVu Sans", 11, "bold")
    FONT_BUTTON = ("DejaVu Sans", 11, "bold")
    FONT_LARGE = ("DejaVu Sans", 12, "bold")
    FONT_XLARGE = ("DejaVu Sans", 15, "bold")
    FONT_XXLARGE = ("DejaVu Sans", 18, "bold")
    FONT_CONSOLE = ("DejaVu Sans Mono", 10, "bold")
    FONT_TAB = ("DejaVu Sans", 11, "bold")
    FONT_STATUS = ("DejaVu Sans", 9, "bold")
    FONT_LABEL = ("DejaVu Sans", 10, "bold")
    FONT_SMALL = ("DejaVu Sans", 9, "bold")
    
    # MODERN COLOR PALETTE
    BG_DARK = "#0a0e1a"
    BG_PANEL = "#0f141f"
    BG_INPUT = "#1a1f2e"
    BG_LABEL = "#151b28"
    BG_HOVER = "#1e2538"
    TEXT_PRIMARY = "#f0f3f8"
    TEXT_SECONDARY = "#8a9bb5"
    TEXT_PATH_GRAY = "#6c7a96"
    TEXT_SUCCESS = "#2ecc71"
    TEXT_ERROR = "#e74c3c"
    TEXT_WARNING = "#f39c12"
    TEXT_INFO = "#3498db"
    
    # BUTTON COLORS
    BTN_SUCCESS = "#27ae60"
    BTN_DANGER = "#e74c3c"
    BTN_PRIMARY = "#2980b9"
    BTN_WARNING = "#e67e22"
    BTN_INFO = "#8e44ad"
    BTN_NEUTRAL = "#5a6c7e"
    BTN_ACCENT = "#1abc9c"
    
    BTN_SUCCESS_HOVER = "#2ecc71"
    BTN_DANGER_HOVER = "#c0392b"
    BTN_PRIMARY_HOVER = "#3498db"
    BTN_WARNING_HOVER = "#f39c12"
    BTN_INFO_HOVER = "#9b59b6"

# =========================================================
# CUSTOM BUTTON WITH HOVER EFFECT (No Tooltip)
# =========================================================
class ModernButton(tk.Frame):
    def __init__(self, parent, text, command, color, hover_color=None, font=None, **kwargs):
        super().__init__(parent, bg=Config.BG_PANEL)
        
        self.command = command
        self.default_color = color
        self.hover_color = hover_color or self.get_hover_color(color)
        
        self.btn = tk.Button(
            self,
            text=text,
            command=self.on_click,
            bg=self.default_color,
            fg=Config.TEXT_PRIMARY,
            font=font or Config.FONT_BUTTON,
            relief="flat",
            cursor="hand2",
            activebackground=self.hover_color,
            activeforeground=Config.TEXT_PRIMARY,
            borderwidth=0,
            padx=10,
            pady=6,
            **kwargs
        )
        self.btn.pack(fill="both", expand=True)
        
        self.btn.bind("<Enter>", self.on_enter)
        self.btn.bind("<Leave>", self.on_leave)
    
    def get_hover_color(self, color):
        hover_map = {
            Config.BTN_SUCCESS: Config.BTN_SUCCESS_HOVER,
            Config.BTN_DANGER: Config.BTN_DANGER_HOVER,
            Config.BTN_PRIMARY: Config.BTN_PRIMARY_HOVER,
            Config.BTN_WARNING: Config.BTN_WARNING_HOVER,
            Config.BTN_INFO: Config.BTN_INFO_HOVER,
        }
        return hover_map.get(color, color)
    
    def on_enter(self, event):
        self.btn.config(bg=self.hover_color)
    
    def on_leave(self, event):
        self.btn.config(bg=self.default_color)
    
    def on_click(self):
        if self.command:
            self.command()
    
    def config(self, **kwargs):
        self.btn.config(**kwargs)
    
    def pack(self, **kwargs):
        super().pack(**kwargs)
    
    def grid(self, **kwargs):
        super().grid(**kwargs)

# =========================================================
# SCROLLABLE FRAME
# =========================================================
class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg=Config.BG_PANEL, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=750)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
    
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
    
    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

# =========================================================
# MAIN APPLICATION
# =========================================================
class HadoopControlCenter:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hadoop Control Center")
        
        self.window_width = 1200
        self.window_height = 800
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.minsize(900, 600)
        self.root.configure(bg=Config.BG_DARK)
        
        self.center_window()
        self.root.resizable(True, True)
        
        self.output_queue = queue.Queue()
        self.auto_clear = tk.BooleanVar(value=True)
        
        self.command_lock = threading.Lock()
        self.is_running = False
        self.buttons = []
        self.services = {"hdfs": False, "yarn": False}
        
        self.setup_environment()
        self.build_ui()
        self.update_output_loop()
        self.update_service_state()
        
        self.log("+" + "=" * 70 + "+", Config.TEXT_INFO)
        self.log("||     HADOOP CONTROL CENTER - SUCCESSFULLY STARTED      ||", Config.TEXT_SUCCESS)
        self.log("+" + "=" * 70 + "+", Config.TEXT_INFO)
        self.log("Ready for commands\n", Config.TEXT_SUCCESS)
    
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
    
    def setup_environment(self):
        self.env = os.environ.copy()
        hadoop_sbin = f"{Config.HADOOP_HOME}/sbin"
        hadoop_bin = f"{Config.HADOOP_HOME}/bin"
        java_bin = f"{Config.JAVA_HOME}/bin"
        anaconda_bin = f"{Config.ANACONDA_HOME}/bin"
        current_path = self.env.get('PATH', '')
        self.env['PATH'] = f"{java_bin}:{hadoop_sbin}:{hadoop_bin}:{anaconda_bin}:{current_path}"
        self.env['HADOOP_CONF_DIR'] = f"{Config.HADOOP_HOME}/etc/hadoop"
        self.env['HADOOP_HOME'] = Config.HADOOP_HOME
        self.env['JAVA_HOME'] = Config.JAVA_HOME

    def create_tracked_button(self, parent, text, command, bg, font=None, **kwargs):
        font = font or Config.FONT_BUTTON
        btn = ModernButton(parent, text, command, bg, font=font, **kwargs)
        self.buttons.append(btn.btn)
        return btn

    def set_buttons_state(self, state):
        for b in self.buttons:
            try:
                b.config(state=state)
            except tk.TclError:
                pass
    
    def can_run(self):
        if self.is_running:
            self.log("[!] Another operation is currently running. Please wait for it to complete before starting a new operation.", Config.TEXT_WARNING)
            return False
        return True

    def execute_command(self, command, title, auto_clear=None):
        if not self.can_run():
            return

        self.command_lock.acquire()
        self.is_running = True
        self.set_buttons_state("disabled")
        
        should_clear = self.auto_clear.get() if auto_clear is None else auto_clear
        if should_clear: self.clear_output()
        
        self.log("+" + "-" * 70 + "+", Config.TEXT_INFO)
        self.log("| EXECUTING: " + title, "command")
        self.log("| COMMAND: " + command, "info")
        self.log("+" + "-" * 70 + "+\n", Config.TEXT_INFO)
        self.status_bar.config(text="[EXECUTING] " + title, fg=Config.TEXT_INFO)
        self.progress.start(10)
        
        def worker():
            try:
                if not os.path.exists(Config.HADOOP_HOME):
                    self.log("\n[ERROR] FATAL: Hadoop not found at expected location", "error")
                    return
                
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, 
                                         stderr=subprocess.STDOUT, env=self.env, text=True, bufsize=1)
                
                for line in process.stdout:
                    if line.strip():
                        lower = line.lower()
                        if "error" in lower or "exception" in lower or "failed" in lower:
                            self.log(f"[ERROR] {line.rstrip()}", "error")
                        elif "warn" in lower:
                            self.log(f"[WARN] {line.rstrip()}", "warning")
                        elif "success" in lower:
                            self.log(f"[OK] {line.rstrip()}", "success")
                        else:
                            self.log(f"  {line.rstrip()}")
                
                process.wait()
                if process.returncode == 0:
                    self.log(f"\n[OK] Success (exit code: 0)", "success")
                else:
                    self.log(f"\n[ERROR] Command failed (exit code: {process.returncode})", "error")
                    
            except Exception as e:
                self.log(f"\n[ERROR] Execution Error: {str(e)}", "error")
            finally:
                self.is_running = False
                self.set_buttons_state("normal")
                self.command_lock.release()
                self.progress.stop()
                self.status_bar.config(text="[READY]", fg=Config.TEXT_SECONDARY)
                self.log("")
                self.update_service_state()
        
        threading.Thread(target=worker, daemon=True).start()
    
    def update_service_state(self):
        try:
            result = subprocess.getoutput("jps")
            self.services["hdfs"] = ("NameNode" in result and "DataNode" in result)
            self.services["yarn"] = ("ResourceManager" in result and "NodeManager" in result)
            self.update_service_indicators()
        except:
            pass
    
    def update_service_indicators(self):
        hdfs_status = "[ACTIVE] HDFS" if self.services["hdfs"] else "[INACTIVE] HDFS"
        yarn_status = "[ACTIVE] YARN" if self.services["yarn"] else "[INACTIVE] YARN"
        hdfs_color = Config.TEXT_SUCCESS if self.services["hdfs"] else Config.TEXT_ERROR
        yarn_color = Config.TEXT_SUCCESS if self.services["yarn"] else Config.TEXT_ERROR
        
        try:
            self.hdfs_indicator.config(text=hdfs_status, fg=hdfs_color)
            self.yarn_indicator.config(text=yarn_status, fg=yarn_color)
        except:
            pass

    def start_hdfs(self):
        self.update_service_state()
        if self.services["hdfs"]:
            self.log("[OK] HDFS already running", Config.TEXT_WARNING)
            return
        self.execute_command(Config.HADOOP_HOME + "/sbin/start-dfs.sh", "Starting HDFS Services")
    
    def stop_hdfs(self):
        self.update_service_state()
        if not self.services["hdfs"]:
            self.log("[WARN] HDFS already stopped", Config.TEXT_WARNING)
            return
        self.execute_command(Config.HADOOP_HOME + "/sbin/stop-dfs.sh", "Stopping HDFS Services")
    
    def start_yarn(self):
        self.update_service_state()
        if self.services["yarn"]:
            self.log("[OK] YARN already running", Config.TEXT_WARNING)
            return
        self.execute_command(Config.HADOOP_HOME + "/sbin/start-yarn.sh", "Starting YARN Services")
    
    def stop_yarn(self):
        self.update_service_state()
        if not self.services["yarn"]:
            self.log("[WARN] YARN already stopped", Config.TEXT_WARNING)
            return
        self.execute_command(Config.HADOOP_HOME + "/sbin/stop-yarn.sh", "Stopping YARN Services")
    
    def restart_all(self):
        if not messagebox.askyesno("Confirm Restart", "Are you sure you want to restart ALL Hadoop services?"):
            return
        def chain():
            self.execute_command(Config.HADOOP_HOME + "/sbin/stop-all.sh", "Stopping All Services")
            self.log("[...] Waiting for services to stop...", Config.TEXT_INFO)
            while True:
                self.update_service_state()
                if not self.services["hdfs"] and not self.services["yarn"]:
                    break
                time.sleep(1)
            self.log("[OK] All stopped. Starting services...", Config.TEXT_SUCCESS)
            self.execute_command(Config.HADOOP_HOME + "/sbin/start-all.sh", "Starting All Services")
        threading.Thread(target=chain, daemon=True).start()
    
    def check_jps(self): 
        self.execute_command("jps", "Java Process Status", auto_clear=True)
    
    def build_ui(self):
        self.create_header()
        self.create_main_layout()
        self.create_status_bar()
    
    def create_header(self):
        header = tk.Frame(self.root, bg=Config.BG_DARK, height=70)
        header.pack(fill="x", padx=15, pady=(8, 5))
        
        title_frame = tk.Frame(header, bg=Config.BG_DARK)
        title_frame.pack(side="left", fill="y")
        
        tk.Label(title_frame, text=">_", bg=Config.BG_DARK, 
                fg=Config.TEXT_PRIMARY, font=("DejaVu Sans", 22, "bold")).pack(side="left", padx=(0, 8))
        
        text_frame = tk.Frame(title_frame, bg=Config.BG_DARK)
        text_frame.pack(side="left")
        
        tk.Label(text_frame, text="HADOOP CONTROL CENTER", bg=Config.BG_DARK, 
                fg=Config.TEXT_PRIMARY, font=Config.FONT_XXLARGE).pack(anchor="w")
        tk.Label(text_frame, text="Enterprise HDFS & YARN Management Platform", bg=Config.BG_DARK, 
                fg=Config.TEXT_SECONDARY, font=Config.FONT_SMALL).pack(anchor="w", pady=(2, 0))
        
        indicator_frame = tk.Frame(header, bg=Config.BG_PANEL, relief="flat", bd=1)
        indicator_frame.pack(side="right", padx=8, pady=4)
        
        self.hdfs_indicator = tk.Label(indicator_frame, text="[INACTIVE] HDFS", 
                                       bg=Config.BG_PANEL, fg=Config.TEXT_ERROR,
                                       font=Config.FONT_LABEL, padx=10, pady=5)
        self.hdfs_indicator.pack(side="left")
        
        tk.Label(indicator_frame, text=" | ", bg=Config.BG_PANEL, 
                fg=Config.TEXT_SECONDARY, font=Config.FONT_LABEL).pack(side="left")
        
        self.yarn_indicator = tk.Label(indicator_frame, text="[INACTIVE] YARN",
                                       bg=Config.BG_PANEL, fg=Config.TEXT_ERROR,
                                       font=Config.FONT_LABEL, padx=10, pady=5)
        self.yarn_indicator.pack(side="left")
        
        ctrl_frame = tk.Frame(header, bg=Config.BG_DARK)
        ctrl_frame.pack(side="right", padx=15)
        
        self.chk_auto = tk.Checkbutton(
            ctrl_frame, 
            text="[X] AUTO CLEAR", 
            variable=self.auto_clear,
            bg=Config.BG_DARK,
            fg=Config.TEXT_PRIMARY,
            font=Config.FONT_LABEL,
            selectcolor=Config.BG_PANEL,
            activebackground=Config.BG_DARK,
            activeforeground=Config.TEXT_PRIMARY,
            relief="flat",
            padx=6,
            pady=3
        )
        self.chk_auto.pack(side="left", padx=(0, 10))
        
        self.btn_clear = tk.Button(
            ctrl_frame, 
            text="[CLEAR] OUTPUT", 
            command=self.clear_output, 
            bg=Config.BTN_NEUTRAL,
            fg=Config.TEXT_PRIMARY, 
            font=Config.FONT_LABEL, 
            relief="flat", 
            cursor="hand2",
            padx=12, 
            pady=5,
            borderwidth=0
        )
        self.btn_clear.pack(side="left")
        self.buttons.append(self.btn_clear)
        
        self.btn_clear.bind("<Enter>", lambda e: self.btn_clear.config(bg=Config.BTN_INFO))
        self.btn_clear.bind("<Leave>", lambda e: self.btn_clear.config(bg=Config.BTN_NEUTRAL))
    
    def create_main_layout(self):
        self.main_pane = tk.PanedWindow(self.root, orient="vertical", bg=Config.BG_DARK, 
                                        sashwidth=4, sashrelief="raised")
        self.main_pane.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        
        self.top_frame = tk.Frame(self.main_pane, bg=Config.BG_DARK)
        self.main_pane.add(self.top_frame, minsize=300, height=400)
        
        self.bottom_frame = tk.Frame(self.main_pane, bg=Config.BG_DARK)
        self.main_pane.add(self.bottom_frame, minsize=180, height=220)
        
        self.create_tabs()
        self.create_output_section()
    
    def create_tabs(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=Config.BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", font=Config.FONT_TAB, padding=[30, 15],
                       background=Config.BG_PANEL, foreground=Config.TEXT_SECONDARY)
        style.map("TNotebook.Tab", background=[("selected", Config.BG_INPUT)],
                 foreground=[("selected", Config.TEXT_PRIMARY)])
        
        self.notebook = ttk.Notebook(self.top_frame)
        self.notebook.pack(fill="both", expand=True, padx=2, pady=(0, 2))
        
        self.tab_services = tk.Frame(self.notebook, bg=Config.BG_PANEL)
        self.tab_basic = tk.Frame(self.notebook, bg=Config.BG_PANEL)
        self.tab_files = tk.Frame(self.notebook, bg=Config.BG_PANEL)
        self.tab_custom = tk.Frame(self.notebook, bg=Config.BG_PANEL)
        
        self.notebook.add(self.tab_services, text="[ SERVICES ]", padding=8)
        self.notebook.add(self.tab_basic, text="[ BASIC HDFS ]", padding=8)
        self.notebook.add(self.tab_files, text="[ FILE OPS ]", padding=8)
        self.notebook.add(self.tab_custom, text="[ CUSTOM CMD ]", padding=8)
        
        self.build_services_tab()
        self.build_basic_tab()
        self.build_files_tab()
        self.build_custom_tab()
    
    def build_services_tab(self):
        frame = self.tab_services
        for i in range(4): frame.grid_rowconfigure(i, weight=1)
        for i in range(2): frame.grid_columnconfigure(i, weight=1)
        
        buttons = [
            ("> START HDFS", Config.BTN_SUCCESS, self.start_hdfs, 0, 0),
            ("[STOP] HDFS", Config.BTN_DANGER, self.stop_hdfs, 0, 1),
            ("> START YARN", Config.BTN_PRIMARY, self.start_yarn, 1, 0),
            ("[STOP] YARN", Config.BTN_WARNING, self.stop_yarn, 1, 1),
            ("[RESTART] ALL", Config.BTN_INFO, self.restart_all, 2, 0),
            ("[CHECK] JPS", Config.BTN_NEUTRAL, self.check_jps, 2, 1),
            ("[WEB] HDFS UI", Config.BTN_ACCENT, self.open_hdfs_ui, 3, 0),
            ("[WEB] YARN UI", Config.BTN_ACCENT, self.open_yarn_ui, 3, 1),
        ]
        
        for text, color, cmd, row, col in buttons:
            btn = self.create_tracked_button(frame, text, cmd, color, Config.FONT_LARGE)
            btn.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
    
    def build_basic_tab(self):
        frame = self.tab_basic
        for i in range(4): frame.grid_rowconfigure(i, weight=1)
        for i in range(2): frame.grid_columnconfigure(i, weight=1)
        
        commands = [
            ("[LIST] ROOT /", "hdfs dfs -ls /", Config.BTN_PRIMARY),
            ("[LIST] /USER", "hdfs dfs -ls /user", Config.BTN_INFO),
            ("[DISK] USAGE", "hdfs dfs -du -h /", Config.BTN_WARNING),
            ("[COUNT] FILES", "hdfs dfs -count /", Config.BTN_NEUTRAL),
            ("[CREATE] DIR", "hdfs dfs -mkdir /test", Config.BTN_SUCCESS),
            ("[REMOVE] DIR", "hdfs dfs -rm -r /test", Config.BTN_DANGER),
            ("[REPORT] CLUSTER", "hdfs dfsadmin -report", Config.BTN_INFO),
            ("[CHECK] PERMS", "hdfs dfs -ls /", Config.BTN_NEUTRAL),
        ]
        
        row, col = 0, 0
        for name, cmd, color in commands:
            btn = self.create_tracked_button(frame, name, lambda c=cmd, n=name: self.execute_command(c, n), color, Config.FONT_MAIN)
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            col += 1
            if col > 1: 
                col, row = 0, row + 1
    
    def build_files_tab(self):
        frame = self.tab_files
        
        path_frame = tk.LabelFrame(frame, text="[PATH CONFIGURATION]", 
                                   bg=Config.BG_PANEL, fg=Config.TEXT_PRIMARY, 
                                   font=Config.FONT_LABEL, padx=10, pady=10)
        path_frame.pack(fill="x", padx=10, pady=6)
        
        local_container = tk.Frame(path_frame, bg=Config.BG_PANEL)
        local_container.pack(fill="x", pady=4)
        tk.Label(local_container, text="LOCAL:", bg=Config.BG_PANEL, 
                fg=Config.TEXT_INFO, font=Config.FONT_LABEL, width=8, anchor="w").pack(side="left")
        self.local_path = ttk.Entry(local_container, font=Config.FONT_MAIN, 
                                   background=Config.BG_INPUT, foreground=Config.TEXT_PATH_GRAY)
        self.local_path.pack(side="left", fill="x", expand=True, padx=(6, 4))
        self.local_path.insert(0, "/home/bigdata/Desktop/")
        btn_browse = tk.Button(local_container, text="[BROWSE]", command=self.browse_local, 
                              bg=Config.BTN_NEUTRAL, fg=Config.TEXT_PRIMARY, 
                              font=Config.FONT_SMALL, relief="flat", cursor="hand2", padx=8, pady=3)
        btn_browse.pack(side="left")
        self.buttons.append(btn_browse)
        
        hdfs_container = tk.Frame(path_frame, bg=Config.BG_PANEL)
        hdfs_container.pack(fill="x", pady=4)
        tk.Label(hdfs_container, text="HDFS:", bg=Config.BG_PANEL, 
                fg=Config.TEXT_INFO, font=Config.FONT_LABEL, width=8, anchor="w").pack(side="left")
        self.hdfs_path = ttk.Entry(hdfs_container, font=Config.FONT_MAIN, 
                                   background=Config.BG_INPUT, foreground=Config.TEXT_PATH_GRAY)
        self.hdfs_path.pack(side="left", fill="x", expand=True, padx=(6, 4))
        self.hdfs_path.insert(0, "/user/bigdata/")
        btn_verify = tk.Button(hdfs_container, text="[VERIFY]", command=self.verify_hdfs_path, 
                              bg=Config.BTN_INFO, fg=Config.TEXT_PRIMARY, 
                              font=Config.FONT_SMALL, relief="flat", cursor="hand2", padx=8, pady=3)
        btn_verify.pack(side="left")
        self.buttons.append(btn_verify)
        
        ops_frame = tk.LabelFrame(frame, text="[FILE OPERATIONS]", 
                                  bg=Config.BG_PANEL, fg=Config.TEXT_PRIMARY, 
                                  font=Config.FONT_LABEL, padx=10, pady=10)
        ops_frame.pack(fill="x", padx=10, pady=6)
        
        for i in range(5): ops_frame.grid_columnconfigure(i, weight=1)
        file_ops = [
            ("[UPLOAD]", "upload", Config.BTN_SUCCESS),
            ("[DOWNLOAD]", "download", Config.BTN_PRIMARY),
            ("[VIEW]", "view", Config.BTN_INFO),
            ("[CHMOD]", "chmod", Config.BTN_WARNING),
            ("[DELETE]", "delete", Config.BTN_DANGER),
        ]
        
        for i, (text, op_type, color) in enumerate(file_ops):
            btn = self.create_tracked_button(ops_frame, text, lambda ot=op_type: self.handle_file_operation(ot), color, Config.FONT_LARGE)
            btn.grid(row=0, column=i, sticky="nsew", padx=3, pady=5)
    
    def build_custom_tab(self):
        frame = self.tab_custom
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        main_container = tk.Frame(frame, bg=Config.BG_PANEL)
        main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_container.grid_rowconfigure(2, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        cmd_frame = tk.LabelFrame(main_container, text="[CUSTOM HADOOP COMMAND]", 
                                  bg=Config.BG_PANEL, fg=Config.TEXT_PRIMARY, 
                                  font=Config.FONT_LABEL, padx=10, pady=8)
        cmd_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        
        self.custom_cmd = tk.Text(cmd_frame, height=3, font=Config.FONT_CONSOLE, 
                                  bg=Config.BG_INPUT, fg=Config.TEXT_PRIMARY, 
                                  insertbackground=Config.TEXT_PRIMARY, 
                                  wrap="word", relief="flat", padx=8, pady=8)
        self.custom_cmd.pack(fill="both", expand=True, pady=4)
        self.custom_cmd.bind("<Control-Return>", lambda e: self.run_custom_command())
        
        exec_frame = tk.Frame(cmd_frame, bg=Config.BG_PANEL)
        exec_frame.pack(fill="x", pady=(4, 0))
        btn_exec = tk.Button(exec_frame, text="[EXECUTE] (Ctrl+Enter)", command=self.run_custom_command, 
                            bg=Config.BTN_SUCCESS, fg=Config.TEXT_PRIMARY, 
                            font=Config.FONT_LARGE, relief="flat", cursor="hand2", 
                            padx=20, pady=8)
        btn_exec.pack(side="right")
        self.buttons.append(btn_exec)
        btn_exec.bind("<Enter>", lambda e: btn_exec.config(bg=Config.BTN_SUCCESS_HOVER))
        btn_exec.bind("<Leave>", lambda e: btn_exec.config(bg=Config.BTN_SUCCESS))
        
        sug_frame = tk.LabelFrame(main_container, text="[COMMAND EXAMPLES]", 
                                  bg=Config.BG_PANEL, fg=Config.TEXT_PRIMARY, 
                                  font=Config.FONT_LABEL, padx=10, pady=8)
        sug_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        
        scroll_examples = ScrollableFrame(sug_frame)
        scroll_examples.pack(fill="both", expand=True)
        
        suggestions = [
            ("hdfs dfs -mkdir -p /user/bigdata/input", "Create directory"),
            ("hdfs dfs -text /user/bigdata/mapreduce/word.txt | head -50", "View first 50 lines"),
            ("hdfs dfs -count -q -h /user", "Show quota"),
            ("hdfs dfsadmin -report", "Cluster report"),
        ]
        
        for cmd_tpl, desc in suggestions:
            row_frame = tk.Frame(scroll_examples.scrollable_frame, bg=Config.BG_PANEL)
            row_frame.pack(fill="x", pady=2)
            btn = tk.Button(row_frame, text=cmd_tpl, 
                          command=lambda c=cmd_tpl: self.insert_smart_command(c), 
                          bg=Config.BG_INPUT, fg=Config.TEXT_INFO, 
                          font=("DejaVu Sans Mono", 9, "bold"),
                          relief="flat", cursor="hand2", anchor="w", 
                          padx=8, pady=4)
            btn.pack(side="left", fill="x", expand=True)
            self.buttons.append(btn)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Config.BG_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Config.BG_INPUT))
            tk.Label(row_frame, text=f"-> {desc}", bg=Config.BG_PANEL, 
                    fg=Config.TEXT_SECONDARY, font=Config.FONT_SMALL).pack(side="left", padx=(6, 0))
    
    def create_output_section(self):
        header = tk.Frame(self.bottom_frame, bg=Config.BG_DARK)
        header.pack(fill="x", padx=6, pady=(4, 2))
        
        tk.Label(header, text="[MAIN CONSOLE]", bg=Config.BG_DARK, 
                fg=Config.TEXT_PRIMARY, font=Config.FONT_LARGE).pack(side="left")
        tk.Label(header, text="Real-time command output", bg=Config.BG_DARK, 
                fg=Config.TEXT_SECONDARY, font=Config.FONT_SMALL).pack(side="left", padx=(6, 0))
        
        self.output = ScrolledText(self.bottom_frame, bg="#0a0e1a", fg=Config.TEXT_SUCCESS, 
                                  font=Config.FONT_CONSOLE, wrap="word", 
                                  relief="flat", padx=10, pady=10)
        self.output.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.output.config(state="disabled")
        
        self.output.tag_configure("info", foreground=Config.TEXT_INFO)
        self.output.tag_configure("success", foreground=Config.TEXT_SUCCESS)
        self.output.tag_configure("error", foreground=Config.TEXT_ERROR)
        self.output.tag_configure("warning", foreground=Config.TEXT_WARNING)
        self.output.tag_configure("command", foreground="#60a5fa")
    
    def create_status_bar(self):
        status_container = tk.Frame(self.root, bg=Config.BG_PANEL)
        status_container.pack(fill="x", side="bottom")
        
        self.status_bar = tk.Label(status_container, text="[READY]", 
                                  bg=Config.BG_PANEL, fg=Config.TEXT_SECONDARY, 
                                  font=Config.FONT_STATUS, anchor="w", padx=10, pady=5)
        self.status_bar.pack(side="left", fill="x", expand=True)
        
        self.progress = ttk.Progressbar(status_container, mode="indeterminate", length=100)
        self.progress.pack(side="right", padx=10, pady=3)
    
    def log(self, message, tag=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_queue.put((f"[{timestamp}] {message}\n", tag))
    
    def update_output_loop(self):
        try:
            while True:
                msg, tag = self.output_queue.get_nowait()
                self.output.config(state="normal")
                self.output.insert("end", msg, tag)
                self.output.see("end")
                self.output.config(state="disabled")
        except queue.Empty:
            pass
        self.root.after(50, self.update_output_loop)
    
    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")
        self.log("[OK] Console cleared", Config.TEXT_INFO)
    
    def open_hdfs_ui(self):
        url = "http://localhost:50070"
        self.log(f"[WEB] Opening HDFS UI: {url}", "info")
        try: 
            webbrowser.open(url, new=2)
            self.log("[OK] Browser opened", "success")
        except: 
            messagebox.showinfo("HDFS UI", f"Open: {url}")
    
    def open_yarn_ui(self):
        url = "http://localhost:8088"
        self.log(f"[WEB] Opening YARN UI: {url}", "info")
        try: 
            webbrowser.open(url, new=2)
            self.log("[OK] Browser opened", "success")
        except: 
            messagebox.showinfo("YARN UI", f"Open: {url}")
    
    def run_custom_command(self):
        cmd = self.custom_cmd.get("1.0", "end").strip()
        if cmd: 
            self.execute_command(cmd, "Custom Command")
        else:
            self.log("[WARN] Enter a command first", Config.TEXT_WARNING)
    
    def insert_smart_command(self, template):
        local = self.local_path.get().strip() if hasattr(self, 'local_path') else ""
        hdfs = self.hdfs_path.get().strip() if hasattr(self, 'hdfs_path') else ""
        filled = template.replace("{local}", local).replace("{hdfs}", hdfs)
        self.custom_cmd.delete("1.0", "end")
        self.custom_cmd.insert("1.0", filled)
        self.custom_cmd.focus()
    
    def handle_file_operation(self, op_type):
        local = self.local_path.get().strip()
        hdfs = self.hdfs_path.get().strip()
        
        if not hdfs: 
            self.show_error("HDFS path required")
            return
        
        if op_type == "upload":
            if not local or not os.path.exists(local) or not os.path.isfile(local):
                self.show_error("Valid local file required")
                return
            dest = hdfs.rstrip("/") + "/" + os.path.basename(local)
            self.execute_command(f'hdfs dfs -put "{local}" "{dest}"', f"Upload: {os.path.basename(local)}")
        
        elif op_type == "download":
            if not local: 
                self.show_error("Local path required")
                return
            self.execute_command(f'hdfs dfs -get "{hdfs}" "{local}"', "Download")
        
        elif op_type == "view":
            self.execute_command(f'hdfs dfs -cat "{hdfs}"', f"View: {hdfs}", auto_clear=True)
        
        elif op_type == "chmod":
            self.show_chmod_dialog(hdfs)
        
        elif op_type == "delete":
            if messagebox.askyesno("Confirm Delete", f"Delete:\n{hdfs}"):
                self.execute_command(f'hdfs dfs -rm -r "{hdfs}"', f"Delete: {hdfs}")
    
    def show_chmod_dialog(self, hdfs):
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Permissions")
        dialog.configure(bg=Config.BG_PANEL)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="CHANGE PERMISSIONS", bg=Config.BG_PANEL, 
                fg=Config.TEXT_PRIMARY, font=Config.FONT_LARGE).pack(pady=(15, 10))
        tk.Label(dialog, text=f"Path: {hdfs}", bg=Config.BG_PANEL, 
                fg=Config.TEXT_SECONDARY, font=("DejaVu Sans Mono", 9)).pack(pady=(0, 8))
        tk.Label(dialog, text="Mode (e.g., 755):", bg=Config.BG_PANEL, 
                fg=Config.TEXT_PRIMARY, font=Config.FONT_LABEL).pack(pady=(5, 5))
        
        entry = ttk.Entry(dialog, font=Config.FONT_MAIN, width=15)
        entry.pack(pady=5)
        entry.insert(0, "755")
        entry.focus()
        
        def apply():
            mode = entry.get().strip()
            if not mode.isdigit() or len(mode) != 3:
                self.show_error("Use 3 digits (e.g., 755)")
                return
            self.execute_command(f'hdfs dfs -chmod {mode} "{hdfs}"', f"CHMOD: {mode}")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=Config.BG_PANEL)
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="APPLY", command=apply, 
                 bg=Config.BTN_SUCCESS, fg=Config.TEXT_PRIMARY, 
                 font=Config.FONT_LABEL, relief="flat", padx=15, pady=6).pack(side="left", padx=4)
        tk.Button(btn_frame, text="CANCEL", command=dialog.destroy, 
                 bg=Config.BTN_DANGER, fg=Config.TEXT_PRIMARY, 
                 font=Config.FONT_LABEL, relief="flat", padx=15, pady=6).pack(side="left", padx=4)
        
        dialog.update_idletasks()
        w, h = 380, dialog.winfo_reqheight() + 40
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")
    
    def browse_local(self):
        path = filedialog.askopenfilename(title="Select File")
        if path: 
            self.local_path.delete(0, "end")
            self.local_path.insert(0, path)
            self.log(f"[OK] Selected: {path}", "info")
    
    def verify_hdfs_path(self):
        hdfs = self.hdfs_path.get().strip()
        if not hdfs: 
            self.show_error("Enter HDFS path first")
            return
        self.execute_command(f'hdfs dfs -test -e "{hdfs}" && echo "[OK] Path exists" || echo "[ERROR] Path does not exist"', 
                            "Verify Path", auto_clear=True)
    
    def show_error(self, msg):
        messagebox.showerror("Error", msg)
        self.log(f"[ERROR] {msg}", "error")

# =========================================================
# MAIN
# =========================================================
def main():
    root = tk.Tk()
    app = HadoopControlCenter(root)
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
    root.mainloop()

if __name__ == "__main__":
    main()
