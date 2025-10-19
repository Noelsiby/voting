import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from PIL import Image, ImageTk
import os
import json
from datetime import datetime
from collections import OrderedDict

class SchoolVotingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced School Voting System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Variables
        self.elections = OrderedDict()  # Stores all elections
        self.current_election = None
        self.election_name = tk.StringVar()
        self.num_candidates = tk.IntVar(value=2)
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for multiple elections
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Welcome tab
        self.welcome_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.welcome_tab, text="Welcome")
        
        self.show_welcome_screen()
        
        # Bind notebook change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('.', background='#f5f5f5')
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('Primary.TButton', background='#3498db', foreground='white')
        self.style.configure('Success.TButton', background='#2ecc71', foreground='white')
        self.style.configure('TEntry', font=('Segoe UI', 10), padding=5)
        self.style.configure('TNotebook', background='#f5f5f5')
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10), padding=6)
        self.style.map('Primary.TButton', background=[('active', '#2980b9')])
        self.style.map('Success.TButton', background=[('active', '#27ae60')])
    
    def show_welcome_screen(self):
        for widget in self.welcome_tab.winfo_children():
            widget.destroy()
        
        welcome_frame = ttk.Frame(self.welcome_tab)
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        ttk.Label(welcome_frame, text="Advanced School Voting System", 
                 style='Title.TLabel').pack(pady=30)
        
        ttk.Label(welcome_frame, text="Manage multiple elections simultaneously", 
                 font=('Segoe UI', 12)).pack(pady=10)
        
        features = [
            "• Create and run multiple elections at the same time",
            "• Each election has its own tab for easy access",
            "• Modern, user-friendly interface with scrollable content",
            "• View results while other elections are still running"
        ]
        
        for feature in features:
            ttk.Label(welcome_frame, text=feature).pack(anchor='w', pady=2)
        
        start_btn = ttk.Button(welcome_frame, text="Create New Election", 
                             style='Primary.TButton',
                             command=self.show_election_setup)
        start_btn.pack(pady=30, ipadx=20, ipady=5)
        
        if self.elections:
            load_btn = ttk.Button(welcome_frame, text="Continue Existing Elections", 
                                style='Success.TButton',
                                command=self.focus_on_first_election)
            load_btn.pack(pady=10, ipadx=20, ipady=5)
    
    def focus_on_first_election(self):
        if self.elections:
            first_tab = list(self.elections.keys())[0]
            self.notebook.select(self.elections[first_tab]['tab'])
    
    def show_election_setup(self):
        # Create a new tab for the election setup
        setup_tab = ttk.Frame(self.notebook)
        tab_id = len(self.elections) + 1
        temp_name = f"New Election {tab_id}"
        self.notebook.add(setup_tab, text=temp_name)
        self.notebook.select(setup_tab)
        
        # Create scrollable frame
        canvas = tk.Canvas(setup_tab, highlightthickness=0)
        scrollbar = ttk.Scrollbar(setup_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Setup content
        ttk.Label(scrollable_frame, text="Create New Election", 
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=20)
        
        # Election Name
        ttk.Label(scrollable_frame, text="Election Name:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        name_entry = ttk.Entry(scrollable_frame, textvariable=self.election_name, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        name_entry.focus()
        
        # Number of Candidates
        ttk.Label(scrollable_frame, text="Number of Candidates:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        num_spin = ttk.Spinbox(scrollable_frame, textvariable=self.num_candidates, from_=2, to=10)
        num_spin.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # Buttons
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        create_btn = ttk.Button(btn_frame, text="Create Election", 
                              style='Primary.TButton',
                              command=lambda: self.create_election(setup_tab))
        create_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", 
                              command=lambda: self.close_tab(setup_tab))
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Configure grid weights
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=1)
    
    def close_tab(self, tab):
        self.notebook.forget(tab)
        if not self.elections:
            self.show_welcome_screen()
    
    def create_election(self, setup_tab):
        name = self.election_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter an election name")
            return
        
        if name in self.elections:
            messagebox.showerror("Error", "An election with this name already exists")
            return
        
        num_candidates = self.num_candidates.get()
        if num_candidates < 2:
            messagebox.showerror("Error", "Please select at least 2 candidates")
            return
        
        # Create new election structure
        election = {
            'name': name,
            'status': 'setup',
            'candidates': [],
            'votes': {},
            'tab': setup_tab,
            'photo_refs': [],  # To keep references to images
            'symbol_refs': []
        }
        
        self.elections[name] = election
        self.current_election = election
        
        # Rename the tab
        self.notebook.tab(setup_tab, text=name)
        
        # Show candidate registration
        self.show_candidate_registration()
    
    def show_candidate_registration(self):
        if not self.current_election:
            return
        
        tab = self.current_election['tab']
        for widget in tab.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        canvas = tk.Canvas(tab, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Title
        ttk.Label(scrollable_frame, text=f"Register Candidates for {self.current_election['name']}", 
                 style='Title.TLabel').grid(row=0, column=0, columnspan=3, pady=20)
        
        # Create frames for each candidate
        self.candidate_entries = []
        
        for i in range(self.num_candidates.get()):
            candidate_frame = ttk.LabelFrame(scrollable_frame, text=f"Candidate {i+1}")
            candidate_frame.grid(row=i+1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')
            
            # Name
            ttk.Label(candidate_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
            name_entry = ttk.Entry(candidate_frame)
            name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
            
            # Photo
            ttk.Label(candidate_frame, text="Photo:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
            photo_frame = ttk.Frame(candidate_frame)
            photo_frame.grid(row=1, column=1, padx=5, pady=5, sticky='w')
            
            photo_btn = ttk.Button(photo_frame, text="Upload Photo", 
                                 command=lambda idx=i: self.upload_photo(idx))
            photo_btn.pack(side=tk.LEFT)
            
            # Symbol
            ttk.Label(candidate_frame, text="Symbol:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
            symbol_frame = ttk.Frame(candidate_frame)
            symbol_frame.grid(row=2, column=1, padx=5, pady=5, sticky='w')
            
            symbol_btn = ttk.Button(symbol_frame, text="Upload Symbol", 
                                  command=lambda idx=i: self.upload_symbol(idx))
            symbol_btn.pack(side=tk.LEFT)
            
            self.candidate_entries.append({
                'name': name_entry,
                'photo_btn': photo_btn,
                'symbol_btn': symbol_btn,
                'photo_path': None,
                'symbol_path': None
            })
            
            candidate_frame.columnconfigure(1, weight=1)
        
        # Button frame
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=self.num_candidates.get()+2, column=0, columnspan=3, pady=20)
        
        start_btn = ttk.Button(btn_frame, text="Start Voting", 
                             style='Primary.TButton',
                             command=self.start_voting_process)
        start_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", 
                              command=lambda: self.close_tab(tab))
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Configure grid weights
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=3)
        scrollable_frame.columnconfigure(2, weight=1)
    
    def upload_photo(self, candidate_idx):
        file_path = filedialog.askopenfilename(
            title="Select Candidate Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            self.candidate_entries[candidate_idx]['photo_path'] = file_path
            self.candidate_entries[candidate_idx]['photo_btn'].config(text="✓ Photo Uploaded")
    
    def upload_symbol(self, candidate_idx):
        file_path = filedialog.askopenfilename(
            title="Select Candidate Symbol",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            self.candidate_entries[candidate_idx]['symbol_path'] = file_path
            self.candidate_entries[candidate_idx]['symbol_btn'].config(text="✓ Symbol Uploaded")
    
    def start_voting_process(self):
        # Validate all candidates
        for idx, candidate in enumerate(self.candidate_entries):
            if not candidate['name'].get().strip():
                messagebox.showerror("Error", f"Please enter a name for Candidate {idx+1}")
                return
            if not candidate['photo_path']:
                messagebox.showerror("Error", f"Please upload a photo for Candidate {idx+1}")
                return
            if not candidate['symbol_path']:
                messagebox.showerror("Error", f"Please upload a symbol for Candidate {idx+1}")
                return
        
        # Store candidates and initialize votes
        self.current_election['candidates'] = []
        self.current_election['votes'] = {}
        
        for candidate in self.candidate_entries:
            name = candidate['name'].get().strip()
            self.current_election['candidates'].append({
                'name': name,
                'photo_path': candidate['photo_path'],
                'symbol_path': candidate['symbol_path']
            })
            self.current_election['votes'][name] = 0
        
        self.current_election['status'] = 'voting'
        
        # Load images
        self.load_candidate_images()
        
        # Show voting interface
        self.show_voting_interface()
    
    def load_candidate_images(self):
        self.current_election['photo_refs'] = []
        self.current_election['symbol_refs'] = []
        
        for candidate in self.current_election['candidates']:
            # Load and resize candidate photo
            try:
                photo_img = Image.open(candidate['photo_path'])
                photo_img = photo_img.resize((180, 180), Image.LANCZOS)
                photo_tk = ImageTk.PhotoImage(photo_img)
                self.current_election['photo_refs'].append(photo_tk)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load photo: {str(e)}")
                return
            
            # Load and resize symbol
            try:
                symbol_img = Image.open(candidate['symbol_path'])
                symbol_img = symbol_img.resize((60, 60), Image.LANCZOS)
                symbol_tk = ImageTk.PhotoImage(symbol_img)
                self.current_election['symbol_refs'].append(symbol_tk)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load symbol: {str(e)}")
                return
    
    def show_voting_interface(self):
        tab = self.current_election['tab']
        for widget in tab.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(main_frame, text=f"Voting: {self.current_election['name']}", 
                 style='Title.TLabel').pack(pady=10)
        
        # Instructions
        ttk.Label(main_frame, text="Click on a candidate to cast your vote", 
                 font=('Segoe UI', 11)).pack(pady=5)
        
        # Create canvas and scrollbar for candidates
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        candidates_frame = ttk.Frame(canvas)
        
        candidates_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=candidates_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Display candidates in a grid
        for idx, candidate in enumerate(self.current_election['candidates']):
            candidate_card = ttk.Frame(candidates_frame, borderwidth=1, relief='solid')
            candidate_card.grid(row=idx//2, column=idx%2, padx=10, pady=10, sticky='nsew')
            
            # Photo
            photo_label = ttk.Label(candidate_card, 
                                 image=self.current_election['photo_refs'][idx])
            photo_label.pack(pady=10)
            
            # Name
            ttk.Label(candidate_card, text=candidate['name'], 
                    font=('Segoe UI', 12, 'bold')).pack()
            
            # Symbol
            symbol_label = ttk.Label(candidate_card, 
                                   image=self.current_election['symbol_refs'][idx])
            symbol_label.pack(pady=5)
            
            # Vote button
            vote_btn = ttk.Button(candidate_card, text="Vote for this Candidate", 
                                style='Primary.TButton',
                                command=lambda name=candidate['name']: self.cast_vote(name))
            vote_btn.pack(pady=10, padx=20, fill=tk.X)
            
            # Configure grid weights
            candidates_frame.columnconfigure(0, weight=1)
            candidates_frame.columnconfigure(1, weight=1)
        
        # End voting button
        end_btn = ttk.Button(main_frame, text="End Voting & Show Results", 
                           style='Success.TButton',
                           command=self.end_voting)
        end_btn.pack(pady=20, ipadx=20, ipady=5)
    
    def cast_vote(self, candidate_name):
        self.current_election['votes'][candidate_name] += 1
        messagebox.showinfo("Vote Recorded", f"Your vote for {candidate_name} has been counted!")
    
    def end_voting(self):
        self.current_election['status'] = 'completed'
        self.show_results()
    
    def show_results(self):
        tab = self.current_election['tab']
        for widget in tab.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(main_frame, text=f"Results: {self.current_election['name']}", 
                 style='Title.TLabel').pack(pady=10)
        
        # Sort candidates by votes
        sorted_candidates = sorted(
            self.current_election['candidates'],
            key=lambda x: self.current_election['votes'][x['name']],
            reverse=True
        )
        
        # Create canvas and scrollbar for results
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        results_frame = ttk.Frame(canvas)
        
        results_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Display results
        for idx, candidate in enumerate(sorted_candidates):
            result_card = ttk.Frame(results_frame, borderwidth=1, relief='solid')
            result_card.pack(fill=tk.X, padx=10, pady=10)
            
            # Position label
            position = ttk.Label(result_card, 
                               text=f"{idx+1}. {candidate['name']}",
                               font=('Segoe UI', 14, 'bold'))
            position.pack(anchor='w', padx=10, pady=5)
            
            # Details frame
            details_frame = ttk.Frame(result_card)
            details_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Get the original index for images
            orig_idx = next(
                i for i, c in enumerate(self.current_election['candidates']) 
                if c['name'] == candidate['name']
            )
            
            # Photo
            photo_frame = ttk.Frame(details_frame)
            photo_frame.pack(side=tk.LEFT, padx=10)
            ttk.Label(photo_frame, 
                     image=self.current_election['photo_refs'][orig_idx]).pack()
            
            # Votes
            votes_frame = ttk.Frame(details_frame)
            votes_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
            
            ttk.Label(votes_frame, 
                     text=f"Total Votes: {self.current_election['votes'][candidate['name']]}",
                     font=('Segoe UI', 12)).pack(anchor='w', pady=5)
            
            # Symbol
            symbol_frame = ttk.Frame(details_frame)
            symbol_frame.pack(side=tk.RIGHT, padx=10)
            ttk.Label(symbol_frame, 
                     image=self.current_election['symbol_refs'][orig_idx]).pack()
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        save_btn = ttk.Button(btn_frame, text="Save Results to File", 
                            style='Primary.TButton',
                            command=self.save_results_to_file)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        new_btn = ttk.Button(btn_frame, text="Create New Election", 
                           command=self.show_election_setup)
        new_btn.pack(side=tk.LEFT, padx=10)
    
    def save_results_to_file(self):
        if not self.current_election:
            return
        
        election_data = {
            'election_name': self.current_election['name'],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'candidates': self.current_election['candidates'],
            'votes': self.current_election['votes']
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"{self.current_election['name']}_results.json"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(election_data, f, indent=4)
                messagebox.showinfo("Success", "Results saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def on_tab_change(self, event):
        selected_tab = self.notebook.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        
        if tab_text == "Welcome":
            self.show_welcome_screen()
        elif tab_text in self.elections:
            self.current_election = self.elections[tab_text]
            if self.current_election['status'] == 'setup':
                self.show_candidate_registration()
            elif self.current_election['status'] == 'voting':
                self.show_voting_interface()
            else:
                self.show_results()

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolVotingSystem(root)
    root.mainloop()