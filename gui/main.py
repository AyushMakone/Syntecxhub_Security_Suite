import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import os
import sys
import time
import random

# allow relative imports (project root)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from port_scanner.scanner import scan_range, scan_list
from password_manager.vault import add_entry, get_entry, delete_entry, search_entries
from subdomain_finder.finder import find_subdomains

# -------------------------
# Theme Colors (Hacker Purple + Neon Cyan Glow)
# -------------------------
BG = "#0b0b12"            # almost black
PANEL = "#0f0b16"         # deep purple panel
ACCENT = "#8a2be2"        # neon purple
ACCENT2 = "#00e5ff"       # cyan neon
TEXT = "#E6E6FA"          # light lavender
NEON = "#b88cff"          # neon purple for output text
MONO_FONT = ("Consolas", 10)

# -------------------------
# Hex Color Interpolation
# -------------------------
def hex_interp(a, b, t):
    ai = int(a[1:3],16), int(a[3:5],16), int(a[5:7],16)
    bi = int(b[1:3],16), int(b[3:5],16), int(b[5:7],16)
    ri = tuple(int(ai[i] + (bi[i]-ai[i]) * t) for i in range(3))
    return "#%02x%02x%02x" % ri

# -------------------------
# Custom Neon Button
# -------------------------
class NeonButton(ttk.Frame):
    def __init__(self, parent, text, command=None, accent=ACCENT, accent2=ACCENT2):
        super().__init__(parent)
        self.command = command
        self.accent = accent
        self.accent2 = accent2
        self.btn = tk.Label(
            self,
            text=text,
            bg=PANEL,
            fg=TEXT,
            padx=12,
            pady=6,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=2
        )
        self.btn.pack(fill='both', expand=True)
        self.btn.bind("<Enter>", self.on_enter)
        self.btn.bind("<Leave>", self.on_leave)
        self.btn.bind("<Button-1>", self.on_click)

    def on_enter(self, e):
        grad = hex_interp(self.accent, self.accent2, 0.4)
        self.btn.config(bg=grad, fg="#020202")

    def on_leave(self, e):
        self.btn.config(bg=PANEL, fg=TEXT)

    def on_click(self, e):
        if callable(self.command):
            threading.Thread(target=self.command, daemon=True).start()

# -------------------------
# Main App
# -------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Syntecx Security Suite — Cyber Glow")
        root.geometry("980x640")
        root.configure(bg=BG)

        # Particle background
        self._particles_canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self._particles_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.particles = [{"x": random.randint(0, 980), "y": random.randint(0, 640),
                           "vx": random.uniform(-0.3, 0.3), "vy": random.uniform(0.1, 0.5),
                           "size": random.randint(1,3), "color": random.choice([ACCENT, ACCENT2])}
                          for _ in range(120)]
        self._animate_particles()

        self._build_styles()
        self._build_header()
        self._build_body()
        self._build_footer()

    # -------------------------
    # Particle Animation
    # -------------------------
    def _animate_particles(self):
        self._particles_canvas.delete("all")
        w, h = self.root.winfo_width(), self.root.winfo_height()
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["x"] < 0 or p["x"] > w: p["vx"] *= -1
            if p["y"] < 0 or p["y"] > h: p["y"] = 0
            self._particles_canvas.create_oval(p["x"], p["y"], p["x"]+p["size"], p["y"]+p["size"], fill=p["color"], outline="")
        self.root.after(30, self._animate_particles)

    # -------------------------
    # Styles
    # -------------------------
    def _build_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TNotebook', background=BG, borderwidth=0)
        style.configure('TNotebook.Tab',
                        background=PANEL,
                        foreground=TEXT,
                        padding=[10, 6])

        style.map('TNotebook.Tab',
                  background=[('selected', ACCENT)],
                  foreground=[('selected', '#020202')])

        style.configure('Glow.TFrame', background=PANEL)
        style.configure('Small.TLabel', background=PANEL,
                        foreground=TEXT, font=("Segoe UI", 9))

    # -------------------------
    # Header
    # -------------------------
    def _build_header(self):
        header_h = 80
        self.header = tk.Canvas(self.root, height=header_h,
                                bg=BG, highlightthickness=0)
        self.header.pack(fill='x')

        w = 1000
        for i in range(w):
            t = i / w
            color = hex_interp("#120017", "#08102a", t * 0.7)
            self.header.create_line(i, 0, i, header_h, fill=color)

        self.header.create_text(
            20, 40, anchor='w',
            text="⚡Security Suite",
            font=("Segoe UI", 20, "bold"),
            fill=ACCENT
        )

    # -------------------------
    # Footer with pulsing glow
    # -------------------------
    def _build_footer(self):
        footer = tk.Frame(self.root, bg=PANEL, height=25)
        footer.pack(side='bottom', fill='x')

        self.footer_label = tk.Label(
            footer,
            text="Created by Ayush Makone",
            bg=PANEL,
            fg=ACCENT2,
            font=("Segoe UI", 9, "italic")
        )
        self.footer_label.pack(pady=4)
        self._pulse_footer(0, True)

    def _pulse_footer(self, step, up):
        t = step / 20
        if not up: t = 1 - t
        color = hex_interp(ACCENT2, ACCENT, t)
        self.footer_label.config(fg=color)
        step += 1
        if step > 20:
            step = 0
            up = not up
        self.root.after(100, lambda: self._pulse_footer(step, up))

    # -------------------------
    # Main Layout
    # -------------------------
    def _build_body(self):
        body = ttk.Frame(self.root, style='Glow.TFrame')
        body.pack(fill='both', expand=True, padx=12, pady=(10, 12))

        # Left side (module buttons)
        left = ttk.Frame(body, width=300, style='Glow.TFrame')
        left.pack(side='left', fill='y', padx=(0, 12))
        left.pack_propagate(False)

        ttk.Label(left, text="Modules", style='Small.TLabel').pack(anchor='w', padx=12, pady=(10, 4))

        NeonButton(left, "Port Scanner", command=self._show_port).pack(fill='x', padx=12, pady=6)
        NeonButton(left, "Password Vault", command=self._show_pass).pack(fill='x', padx=12, pady=6)
        NeonButton(left, "Subdomain Finder", command=self._show_sub).pack(fill='x', padx=12, pady=6)

        # Right side — content frame container for neon borders
        self.container_outer = tk.Frame(body, bg=PANEL, highlightthickness=3, highlightbackground=ACCENT2)
        self.container_outer.pack(side='left', fill='both', expand=True)
        self.container = ttk.Frame(self.container_outer, style='Glow.TFrame')
        self.container.pack(fill='both', expand=True, padx=0, pady=0)

        # Create pages
        self.port_frame = self._build_port_frame(self.container)
        self.pass_frame = self._build_pass_frame(self.container)
        self.sub_frame = None

        self._show_port()

        # Start neon border updater
        self._update_neon_border()

    # -------------------------
    # Neon border update
    # -------------------------
    def _update_neon_border(self):
        # Determine active frame
        active = None
        if self.port_frame.winfo_ismapped(): active = self.port_frame
        if self.pass_frame.winfo_ismapped(): active = self.pass_frame
        if self.sub_frame and self.sub_frame.winfo_ismapped(): active = self.sub_frame

        if active:
            self.container_outer.config(highlightbackground=ACCENT2)
        self.root.after(200, self._update_neon_border)

    # -------------------------
    # Port Scanner Page
    # -------------------------
    def _build_port_frame(self, parent):
        f = ttk.Frame(parent, padding=10, style='Glow.TFrame')

        controls = ttk.Frame(f, style='Glow.TFrame')
        controls.pack(fill='x')

        ttk.Label(controls, text="Host:", style='Small.TLabel').grid(row=0, column=0, sticky='w')
        self.host_entry = ttk.Entry(controls, width=25)
        self.host_entry.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(controls, text="Start Port:", style='Small.TLabel').grid(row=1, column=0, sticky='w')
        self.start_entry = ttk.Entry(controls, width=10)
        self.start_entry.insert(0, "1")
        self.start_entry.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(controls, text="End Port:", style='Small.TLabel').grid(row=2, column=0, sticky='w')
        self.end_entry = ttk.Entry(controls, width=10)
        self.end_entry.insert(0, "1024")
        self.end_entry.grid(row=2, column=1, padx=6, pady=4)

        action = ttk.Frame(f, style='Glow.TFrame')
        action.pack(fill='x', pady=10)

        NeonButton(action, "Scan Range", command=self.run_port_scan).pack(side='left', padx=6)
        NeonButton(action, "Scan Common", command=self.run_common_scan).pack(side='left', padx=6)

        out = tk.Frame(f, bg="#060608")
        out.pack(fill='both', expand=True)

        self.port_output = scrolledtext.ScrolledText(
            out,
            bg="#020206",
            fg=NEON,
            insertbackground=NEON,
            font=MONO_FONT,
            wrap='none',
            relief='flat'
        )
        self.port_output.pack(fill='both', expand=True, padx=8, pady=8)

        return f

    def run_port_scan(self):
        host = self.host_entry.get().strip()
        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
        except:
            messagebox.showerror("Error", "Ports must be numbers.")
            return

        self.port_output.insert('end', f"[{time.asctime()}] Scanning {host} {start}-{end}...\n")
        self.port_output.see('end')

        threading.Thread(
            target=self._port_scan_thread,
            args=(host, start, end),
            daemon=True
        ).start()

    def _port_scan_thread(self, host, start, end):
        try:
            result = scan_range(host, start, end, threads=200)
            self.port_output.insert('end', f"Open ports: {result}\n")
            self.port_output.see('end')
        except Exception as e:
            self.port_output.insert('end', f"Error: {e}\n")

    def run_common_scan(self):
        host = self.host_entry.get().strip()
        common_ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,8080]

        self.port_output.insert('end', f"[{time.asctime()}] Scanning common ports on {host}...\n")
        self.port_output.see('end')

        threading.Thread(
            target=self._common_scan_thread,
            args=(host, common_ports),
            daemon=True
        ).start()

    def _common_scan_thread(self, host, ports):
        try:
            result = scan_list(host, ports)
            self.port_output.insert('end', f"Open common ports: {result}\n")
            self.port_output.see('end')
        except Exception as e:
            self.port_output.insert('end', f"Error: {e}\n")

    # -------------------------
    # Password Vault Page
    # -------------------------
    def _build_pass_frame(self, parent):
        f = ttk.Frame(parent, padding=10, style='Glow.TFrame')

        box = ttk.Frame(f, style='Glow.TFrame')
        box.pack(fill='x')

        ttk.Label(box, text="Master Password:", style='Small.TLabel').grid(row=0, column=0, sticky='w')
        self.master_entry = ttk.Entry(box, show="*", width=25)
        self.master_entry.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(box, text="Entry Name:", style='Small.TLabel').grid(row=1, column=0, sticky='w')
        self.entry_name = ttk.Entry(box, width=25)
        self.entry_name.grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(box, text="Username:", style='Small.TLabel').grid(row=2, column=0, sticky='w')
        self.entry_user = ttk.Entry(box, width=25)
        self.entry_user.grid(row=2, column=1, padx=6, pady=4)

        ttk.Label(box, text="Password:", style='Small.TLabel').grid(row=3, column=0, sticky='w')
        self.entry_pass = ttk.Entry(box, width=25)
        self.entry_pass.grid(row=3, column=1, padx=6, pady=4)

        actions = ttk.Frame(f, style='Glow.TFrame')
        actions.pack(fill='x', pady=10)

        NeonButton(actions, "Add / Update", command=self.add_vault_entry).pack(side='left', padx=6)
        NeonButton(actions, "Get Entry", command=self.get_vault_entry).pack(side='left', padx=6)
        NeonButton(actions, "Search", command=self.search_vault).pack(side='left', padx=6)
        NeonButton(actions, "Delete", command=self.delete_vault_entry).pack(side='left', padx=6)

        out = tk.Frame(f, bg="#060608")
        out.pack(fill='both', expand=True)

        self.pass_output = scrolledtext.ScrolledText(
            out,
            bg="#03030a",
            fg=ACCENT2,
            insertbackground=ACCENT2,
            font=MONO_FONT,
            wrap='word',
            relief='flat'
        )
        self.pass_output.pack(fill='both', expand=True, padx=8, pady=8)

        return f

    # Vault Actions
    def add_vault_entry(self):
        mp = self.master_entry.get().strip()
        if not mp:
            messagebox.showerror("Error", "Master password required.")
            return

        name = self.entry_name.get().strip()
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()

        try:
            add_entry(mp, name, user, pwd)
            self.pass_output.insert('end', f"[+] Added/Updated: {name}\n")
        except Exception as e:
            self.pass_output.insert('end', f"[Error] {e}\n")
        self.pass_output.see('end')

    def get_vault_entry(self):
        mp = self.master_entry.get().strip()
        name = self.entry_name.get().strip()
        try:
            data = get_entry(mp, name)
            self.pass_output.insert('end', f"{name}: {data}\n")
        except Exception as e:
            self.pass_output.insert('end', f"[Error] {e}\n")
        self.pass_output.see('end')

    def search_vault(self):
        mp = self.master_entry.get().strip()
        name = self.entry_name.get().strip()
        try:
            results = search_entries(mp, name)
            self.pass_output.insert('end', f"Search Results:\n{results}\n\n")
        except Exception as e:
            self.pass_output.insert('end', f"[Error] {e}\n")
        self.pass_output.see('end')

    def delete_vault_entry(self):
        mp = self.master_entry.get().strip()
        name = self.entry_name.get().strip()
        try:
            delete_entry(mp, name)
            self.pass_output.insert('end', f"[-] Deleted: {name}\n")
        except Exception as e:
            self.pass_output.insert('end', f"[Error] {e}\n")
        self.pass_output.see('end')

    # -------------------------
    # Subdomain Finder Page
    # -------------------------
    def _build_sub_frame(self, parent):
        f = ttk.Frame(parent, padding=10, style='Glow.TFrame')
        f.pack(fill='both', expand=True)

        frame = ttk.Frame(f, style='Glow.TFrame')
        frame.pack(fill='x')

        ttk.Label(frame, text="Base Domain:", style='Small.TLabel')\
            .grid(row=0, column=0, sticky='w')
        self.domain_entry = ttk.Entry(frame, width=30)
        self.domain_entry.grid(row=0, column=1, padx=6, pady=4)

        btn_choose_frame = ttk.Frame(frame, style="Glow.TFrame")
        btn_choose_frame.grid(row=1, column=0, sticky='w')
        NeonButton(btn_choose_frame, "Choose Wordlist", command=self.choose_wordlist)\
            .pack(fill='x')

        self.wordlist_label = ttk.Label(frame, text="Using default wordlist", style='Small.TLabel')
        self.wordlist_label.grid(row=1, column=1, sticky='w', padx=6, pady=4)

        btn_start_frame = ttk.Frame(frame, style="Glow.TFrame")
        btn_start_frame.grid(row=2, column=0, sticky='w', pady=6)
        NeonButton(btn_start_frame, "Start Scan", command=self.run_subdomain_scan)\
            .pack(fill='x')

        out = tk.Frame(f, bg="#060608")
        out.pack(fill='both', expand=True, pady=(8, 0))

        self.sub_output = scrolledtext.ScrolledText(
            out,
            bg="#030010",
            fg="#d6b3ff",
            insertbackground="#d6b3ff",
            font=MONO_FONT,
            wrap='none',
            relief='flat'
        )
        self.sub_output.pack(fill='both', expand=True, padx=8, pady=8)

        self.wordlist_path = None
        return f

    def choose_wordlist(self):
        path = filedialog.askopenfilename(title="Select Wordlist")
        if path:
            self.wordlist_path = path
            self.wordlist_label.config(text=path)

    def run_subdomain_scan(self):
        domain = self.domain_entry.get().strip()
        wl = self.wordlist_path

        self.sub_output.insert('end', f"[{time.asctime()}] Scanning {domain}...\n")
        self.sub_output.see('end')

        threading.Thread(
            target=self._sub_scan_thread,
            args=(domain, wl),
            daemon=True
        ).start()

    def _sub_scan_thread(self, domain, wl):
        try:
            results = find_subdomains(domain, wl)
            for r in results:
                self.sub_output.insert('end', r + "\n")
            self.sub_output.see('end')
        except Exception as e:
            self.sub_output.insert('end', f"[Error] {e}\n")

    # -------------------------
    # Page Switching
    # -------------------------
    def _show_port(self):
        for w in self.container.winfo_children():
            w.pack_forget()
        self.port_frame.pack(fill='both', expand=True)

    def _show_pass(self):
        for w in self.container.winfo_children():
            w.pack_forget()
        self.pass_frame.pack(fill='both', expand=True)

    def _show_sub(self):
        for w in self.container.winfo_children():
            w.pack_forget()

        if not self.sub_frame:
            self.sub_frame = self._build_sub_frame(self.container)

        self.sub_frame.pack(fill='both', expand=True)

    # -------------------------
    # Footer (Cyber Glow)
    # -------------------------
    def _build_footer(self):
        self.footer = tk.Frame(self.root, bg=PANEL, height=25)
        self.footer.pack(side='bottom', fill='x')

        self.footer_label = tk.Label(
            self.footer,
            text="Created by Ayush Makone",
            bg=PANEL,
            fg=ACCENT2,
            font=("Segoe UI", 9, "italic")
        )
        self.footer_label.pack(pady=4)

    # Animation for glowing footer
    def _animate_footer(self):
        t = (time.time() % 2) / 2
        color = hex_interp(ACCENT2, ACCENT, t)
        self.footer_label.config(fg=color)
        self.root.after(70, self._animate_footer)

# -------------------------
# Launcher
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
