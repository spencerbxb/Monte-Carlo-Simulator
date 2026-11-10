import ctypes
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from montecarlo import simulate
import textcontent as tx


class MonteCarloApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Give the application its own Windows identity
        app_id = "spencer.portfolio.montecarlo.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self.title("Portfolio Monte Carlo")

        self.app_icon = tk.PhotoImage(file="icon/icon.png")
        self.iconphoto(True, self.app_icon)

        self.geometry('1120x760')
        self.minsize(850, 620)
        self.language = tk.IntVar(value=0)
        self.rows = []
        self.result = None
        self.busy = False
        self.capital = tk.StringVar(value='10000')
        self.simulations = tk.StringVar(value='1000')
        self.days = tk.StringVar(value='252')
        self.history = tk.StringVar(value='300')
        self.status = tk.StringVar()
        self.summary_text = tk.StringVar()
        self._build()

    def tr(self, phrase):
        return phrase[self.language.get()]

    def _build(self):
        # Rebuilding the widgets preserves input variables and the latest result.
        saved_rows = [(ticker.get(), weight.get()) for _, ticker, weight in self.rows]
        if not saved_rows:
            saved_rows = [('AAPL', '25'), ('NVDA', '20'), ('TSLA', '15'),
                          ('BNS', '10'), ('TD', '15'), ('RY', '15')]
        for widget in self.winfo_children():
            widget.destroy()
        self.rows = []

        root = ttk.Frame(self, padding=16)
        root.pack(fill='both', expand=True)
        left = ttk.LabelFrame(root, text=self.tr(tx.PORTFOLIOPARAMETER), padding=12)
        left.pack(side='left', fill='y', padx=(0, 12))
        right = ttk.Frame(root)
        right.pack(side='left', fill='both', expand=True)

        language_bar = ttk.Frame(left)
        language_bar.pack(fill='x', pady=(0, 12))
        ttk.Label(language_bar, text=self.tr(tx.LANGUAGE)).pack(side='left')
        chooser = ttk.Combobox(language_bar, state='readonly', width=12,
                               values=('English', 'Français'))
        chooser.current(self.language.get())
        chooser.pack(side='right')
        chooser.bind('<<ComboboxSelected>>', lambda event: self.change_language(chooser.current()))

        self.asset_frame = ttk.Frame(left)
        self.asset_frame.pack(fill='x')
        ttk.Label(self.asset_frame, text=self.tr(tx.SYMBOL), width=15).grid(row=0, column=0)
        ttk.Label(self.asset_frame, text=self.tr(tx.WEIGHT), width=16).grid(row=0, column=1)
        for symbol, pct in saved_rows:
            self.add_asset(symbol, pct)
        ttk.Button(left, text=self.tr(tx.ADD_ASSET), command=self.add_asset).pack(fill='x', pady=8)

        form = ttk.LabelFrame(left, text=self.tr(tx.SIMULATION), padding=10)
        form.pack(fill='x', pady=12)
        for idx, (label, var) in enumerate([
            (tx.INITIAL_CAPITAL, self.capital),
            (tx.SIMULATION_COUNT, self.simulations),
            (tx.TIME_HORIZON, self.days),
            (tx.HISTORY, self.history),
        ]):
            ttk.Label(form, text=self.tr(label)).grid(row=idx, column=0, sticky='w', pady=4)
            ttk.Entry(form, textvariable=var, width=13).grid(row=idx, column=1, padx=6, pady=4)

        self.apply = ttk.Button(left, text=self.tr(tx.APPLY), command=self.run_simulation)
        self.apply.pack(fill='x', pady=8)
        if self.busy:
            self.apply.config(state='disabled')
        ttk.Label(left, textvariable=self.status, wraplength=270).pack(anchor='w')

        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=right)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        summary_frame = ttk.LabelFrame(right, text=self.tr(tx.RESULTS), padding=10)
        summary_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(summary_frame, textvariable=self.summary_text, justify='left').pack(anchor='w')
        if self.result is None:
            self._empty_chart()
            self.summary_text.set(self.tr(tx.NO_RESULTS))
            self.status.set(self.tr(tx.RUNNING if self.busy else tx.READY))
        else:
            self._render_result(self.result)

    def change_language(self, language):
        if language == self.language.get():
            return
        self.language.set(language)
        self._build()

    def _empty_chart(self):
        self.ax.clear()
        self.ax.set(title=self.tr(tx.CHART_TITLE), xlabel=self.tr(tx.CHART_X),
                    ylabel=self.tr(tx.CHART_Y))
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def add_asset(self, symbol='', pct='0'):
        row = ttk.Frame(self.asset_frame)
        row.grid(row=len(self.rows) + 1, column=0, columnspan=3, sticky='ew', pady=3)
        ticker_var, weight_var = tk.StringVar(value=symbol), tk.StringVar(value=pct)
        ttk.Entry(row, textvariable=ticker_var, width=15).pack(side='left', padx=(0, 6))
        ttk.Entry(row, textvariable=weight_var, width=14).pack(side='left', padx=(0, 6))
        ttk.Button(row, text='×', width=3, command=lambda: self.remove_asset(row)).pack(side='left')
        self.rows.append((row, ticker_var, weight_var))

    def remove_asset(self, frame):
        if len(self.rows) == 1:
            messagebox.showwarning(self.tr(tx.PORTFOLIO), self.tr(tx.KEEP_ASSET))
            return
        self.rows = [item for item in self.rows if item[0] is not frame]
        frame.destroy()


    def run_simulation(self):
        if self.busy:
            return

        try:
            tickers = [
                ticker.get().strip().upper()
                for _, ticker, _ in self.rows
            ]

            percentages = [
                float(weight.get())
                for _, _, weight in self.rows
            ]

            capital = float(self.capital.get())
            simulations = int(self.simulations.get())
            days = int(self.days.get())
            history = int(self.history.get())

        except ValueError:
            messagebox.showerror(
                self.tr(tx.INVALID_INPUT),
                self.tr(tx.CHECK_NUMBERS)
            )
            return

        # Capture language before starting the worker thread
        selected_language = self.language.get()

        self.busy = True
        self.apply.config(state='disabled')
        self.status.set(self.tr(tx.RUNNING))

        def worker():
            try:
                result = simulate(
                    tickers,
                    percentages,
                    capital,
                    simulations,
                    days,
                    history,
                    language=selected_language
                )

            except Exception as exc:
                error = str(exc)
                self.after(
                    0,
                    lambda: self.show_error(error)
                )

            else:
                self.after(
                    0,
                    lambda: self.show_result(result)
                )

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

    def show_error(self, error):
        self.busy = False
        self.apply.config(state='normal')
        self.status.set(self.tr(tx.SIMULATION_FAILED))
        messagebox.showerror(self.tr(tx.ERROR), error)

    def _render_result(self, result):
        self.ax.clear()

        self.ax.plot(
            result.paths,
            linewidth=0.7,
            alpha=0.25
        )

        self.ax.plot(
            np.median(result.paths, axis=1),
            color='black',
            linewidth=2,
            label=self.tr(tx.MEDIAN)
        )

        self.ax.axhline(
            result.initial_capital,
            color='gray',
            linestyle='--',
            linewidth=1
        )

        self.ax.set(
            title=self.tr(tx.CHART_TITLE),
            xlabel=self.tr(tx.CHART_X),
            ylabel=self.tr(tx.CHART_Y)
        )

        self.ax.legend(loc='best')
        self.figure.tight_layout()
        self.canvas.draw_idle()

        stats = result.summary(
            language=self.language.get()
        )

        labels = (
            tx.MEAN_FINAL,
            tx.MEDIAN_FINAL,
            tx.PERCENTILE_5,
            tx.PERCENTILE_95,
            tx.LOSS_PROBABILITY
        )

        lines = []

        for label, value in zip(labels, stats.values()):
            if label is tx.LOSS_PROBABILITY:
                formatted = f'{value:.1%}'
            else:
                formatted = f'${value:,.2f}'

            lines.append(
                f'{self.tr(label)} : {formatted}'
            )

        self.summary_text.set('\n'.join(lines))

        self.status.set(
            self.tr(tx.SIMULATIONS_COMPLETED).format(
                f'{result.paths.shape[1]:,}'
            )
        )

    def show_result(self, result):
        self.result = result
        self.busy = False
        self.apply.config(state='normal')
        self._render_result(result)