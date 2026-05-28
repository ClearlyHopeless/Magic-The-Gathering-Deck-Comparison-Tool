import tkinter
import DeckComparator
import DeckPuller
from tkinter import messagebox as messagebox
from DeckComparator import Comparison_Results
from typing import Any

dark_color = '#2C363F'
accent_color = '#ED6A5A'
light_color = '#F2F5EA'
default_font = "Planewalker"

# Variables to store the last submitted deck data
current_deck1_info: dict[str, Any] = {}
current_deck2_info: dict[str, Any] = {}

# Window Essentials
root = tkinter.Tk()
root.iconbitmap('icon_image.ico')
root.title("Magic: The Gathering Deck Analyzer")
root.geometry('1000x1000')
root['bg'] = dark_color

# The frame currently being displayed to the user
current_raised_frame = tkinter.Frame(root)

input_frame = tkinter.Frame(root)
difference_results_frame = tkinter.Frame(root)
option_menu_frame = tkinter.Frame(root)

def create_input_frame() -> None:
    top = tkinter.Frame(input_frame, bg=dark_color)
    middle = tkinter.Frame(input_frame, bg=dark_color)
    bottom = tkinter.Frame(input_frame, bg=dark_color)
    
    top_title = tkinter.Label(top, text="Magic: The Gathering Deck Analyzer", padx=10, pady=20, font=("MagicMedieval", 20, "bold"), bg=dark_color, fg=light_color)
    top_title.pack()
    
    entry_frame1 = tkinter.Frame(middle, padx=10, pady=20, bg=dark_color)
    entry_frame2 = tkinter.Frame(middle, padx=10, pady=20, bg=dark_color)
    
    entry1_title = tkinter.Label(entry_frame1, text="First Deck Url: ", padx=10, pady=10, font=(default_font, 15), bg=dark_color, fg=light_color)
    entry1 = tkinter.Entry(entry_frame1, width=60, bg=light_color, fg=accent_color, font=(default_font, 15))
    entry1_title.pack()
    entry1.pack()
    
    entry2_title = tkinter.Label(entry_frame2, text="Second Deck Url:", padx=10, pady=10, font=(default_font, 15), bg=dark_color, fg=light_color)
    entry2 = tkinter.Entry(entry_frame2, width=60, bg=light_color, fg=accent_color, font=(default_font, 15))
    entry2_title.pack()
    entry2.pack()
    
    entry_frame1.pack()
    entry_frame2.pack()
    
    button_frame = tkinter.Frame(bottom, padx=10, pady=20, bg=dark_color)
    submit_button = tkinter.Button(button_frame, text="Submit Decks",command=lambda:submit_entries_comparator(entry1, entry2), padx=10, pady=10, width=20, font=(default_font, 15), bg=accent_color, fg=light_color, activebackground=light_color, activeforeground=accent_color)
    exit_button = tkinter.Button(button_frame, text="Exit Program", command=lambda:root.destroy(), padx=10, pady=10, width=20, font=(default_font, 15), bg=accent_color, fg=light_color, activebackground=light_color, activeforeground=accent_color)
    submit_button.pack(padx=10, pady=10)
    exit_button.pack(padx=10, pady=10)
    button_frame.pack(padx=10, pady=20)
    
    top.pack(fill='both', expand=True)
    middle.pack(fill='both', expand=True)
    bottom.pack(fill='both', expand=True)

def create_difference_results_frame(results: Comparison_Results, name1: str, name2: str) -> None:
    
    for widget in difference_results_frame.winfo_children():
        widget.destroy()
    
    canvas = tkinter.Canvas(difference_results_frame, bg=dark_color)
    canvas.pack(side='left', fill='both', expand=True)

    scrollbar = tkinter.Scrollbar(difference_results_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tkinter.Frame(canvas, bg=dark_color)

    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def resize_scrollable_frame(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_scrollable_frame)
    setup_mousewheel(difference_results_frame, canvas)
    top = tkinter.Frame(scrollable_frame, bg=dark_color)
    middle = tkinter.Frame(scrollable_frame, bg=dark_color)
    bottom = tkinter.Frame(scrollable_frame, bg=dark_color)
    
    unique_cards_title = tkinter.Label(middle, text="Cards Unique to Either Deck", padx=10, pady=20, font=("MagicMedieval", 20, "bold"), bg=dark_color, fg=light_color)
    unique_cards_title.pack()
    unique_cards_frame = tkinter.Frame(middle, padx=10, pady=10, bg=dark_color)
    
    deck1_unique_cards_frame = tkinter.LabelFrame(unique_cards_frame, padx=10, pady=10, bg=dark_color, text=name1, labelanchor='n', font=(default_font, 15), fg=accent_color)
    deck2_unique_cards_frame = tkinter.LabelFrame(unique_cards_frame, padx=10, pady=10, bg=dark_color, text=name2, labelanchor='n', font=(default_font, 15), fg=accent_color)
    deck1_unique_cards_frame.pack(side='left', expand=True, fill='both')
    deck2_unique_cards_frame.pack(side='left', expand=True, fill='both')
    
    deck1_unique_cards_text_box = tkinter.Label(deck1_unique_cards_frame, text=format_cards_list(results.deck1_unique_cards) , padx=10, pady=10, font=(default_font, 15), bg=dark_color, fg=light_color, justify='left', anchor='n')
    deck1_unique_cards_text_box.pack(padx=10, pady=10, fill='x')
    
    deck2_unique_cards_text_box = tkinter.Label(deck2_unique_cards_frame, text=format_cards_list(results.deck2_unique_cards), padx=10, pady=10, font=(default_font, 15), bg=dark_color, fg=light_color, justify='left', anchor='n')
    deck2_unique_cards_text_box.pack(padx=10, pady=10, fill='x')
    
    unique_cards_frame.pack(expand=True, fill='x')
    
    same_but_different_cards_title = tkinter.Label(middle, text="Cards With Different Amounts in Either Deck", padx=10, pady=20, font=("MagicMedieval", 20, "bold"), bg=dark_color, fg=light_color)
    same_but_different_cards_title.pack()
    same_but_differing_amounts_frame = tkinter.Frame(middle, padx=10, pady=10, bg=dark_color)
    
    deck1_same_differing_cards_frame = tkinter.LabelFrame(same_but_differing_amounts_frame, padx=10, pady=10, bg=dark_color, text=name1, labelanchor='n', font=(default_font, 15), fg=accent_color)
    deck2_same_differing_cards_frame = tkinter.LabelFrame(same_but_differing_amounts_frame, padx=10, pady=10, bg=dark_color, text=name2, labelanchor='n', font=(default_font, 15), fg=accent_color)
    deck1_same_differing_cards_frame.pack(side='left', expand=True, fill='both')
    deck2_same_differing_cards_frame.pack(side='left', expand=True, fill='both')
    
    deck1_same_differing_cards_text_box = tkinter.Label(deck1_same_differing_cards_frame, text=format_cards_list(results.differing_card_numbers["Deck1"]), padx=10, pady=10,  font=(default_font, 15), bg=dark_color, fg=light_color, justify='left', anchor='n')
    deck1_same_differing_cards_text_box.pack(padx=10, pady=10, fill='x')
    
    deck2_same_differing_cards_text_box = tkinter.Label(deck2_same_differing_cards_frame, text=format_cards_list(results.differing_card_numbers["Deck2"]), padx=10, pady=10, font=(default_font, 15), bg=dark_color, fg=light_color, justify='left', anchor='n')
    deck2_same_differing_cards_text_box.pack(padx=10, pady=10, fill='x')
    
    same_but_differing_amounts_frame.pack(expand=True, fill='x')
    
    shared_cards_title = tkinter.Label(middle, text="Cards Shared Between Decks", font=("MagicMedieval", 20, "bold"), bg=dark_color, fg=light_color)
    shared_cards_title.pack()
    shared_cards_frame = tkinter.Frame(middle, padx=10, pady=10, bg=dark_color)
    
    shared_cards_text_box = tkinter.Label(shared_cards_frame, text=format_cards_list(results.shared_cards), padx=10, pady=10, font=(default_font, 15), bg=dark_color, fg=light_color, justify='left', anchor='n')
    shared_cards_text_box.pack(expand=True, fill='x')
    
    shared_cards_frame.pack(expand=True, fill='x')
    
    button_frame = tkinter.Frame(bottom, padx=10, pady=20, bg=dark_color)
    return_button = tkinter.Button(button_frame, text="Return to Tools",command=lambda:switch_frame(option_menu_frame), padx=10, pady=10, width=20, font=(default_font, 15), bg=accent_color, fg=light_color, activebackground=light_color, activeforeground=accent_color)
    exit_button = tkinter.Button(button_frame, text="Exit Program", command=lambda:root.destroy(), padx=10, pady=10, width=20, font=(default_font, 15), bg=accent_color, fg=light_color, activebackground=light_color, activeforeground=accent_color)
    return_button.pack(padx=10, pady=10)
    exit_button.pack(padx=10, pady=10)
    button_frame.pack(padx=10, pady=20)
    
    top.pack(fill='x')
    middle.pack(fill='x')
    bottom.pack(fill='x')

def create_option_menu_frame() -> None:
    top = tkinter.Frame(option_menu_frame, bg=dark_color)
    middle = tkinter.Frame(option_menu_frame, bg=dark_color)
    bottom = tkinter.Frame(option_menu_frame, bg=dark_color)
    
    top_title = tkinter.Label(top, text="Tools:", padx=10, pady=20, font=("MagicMedieval", 20, "bold"), bg=dark_color, fg=light_color)
    top_title.pack()
    
    button_frame = tkinter.Frame(middle, padx=10, pady=20, bg=dark_color)
    comparator_button = tkinter.Button(button_frame, text="Compare Cards", command=lambda:compare_cards(), padx=10, pady=10, width=20, font=(default_font, 15), bg=accent_color, fg=light_color, activebackground=light_color, activeforeground=accent_color)
    return_button = tkinter.Button(button_frame, text="Return to Title Screen",command=lambda:switch_frame(input_frame), padx=10, pady=10, width=20, font=(default_font, 15), bg=accent_color, fg=light_color, activebackground=light_color, activeforeground=accent_color)
    exit_button = tkinter.Button(button_frame, text="Exit Program", command=lambda:root.destroy(), padx=10, pady=10, width=20, font=(default_font, 15), bg=accent_color, fg=light_color, activebackground=light_color, activeforeground=accent_color)
    comparator_button.pack(padx=10, pady=10)
    return_button.pack(padx=10, pady=10)
    exit_button.pack(padx=10, pady=10)
    button_frame.pack(padx=10, pady=20)
    
    top.pack(fill='both', expand=True)
    middle.pack(fill='both', expand=True)
    bottom.pack(fill='both', expand=True)
    
def submit_entries_comparator(entry1: tkinter.Entry, entry2: tkinter.Entry) -> None:
    global current_deck1_info
    global current_deck2_info
    
    entry1_submission = entry1.get()
    entry2_submission = entry2.get()
    entry1.delete(0, len(entry1_submission))
    entry2.delete(0, len(entry2_submission))
    
    current_deck1_info = DeckPuller.get_deck_info(entry1_submission)
    if current_deck1_info is None:
        tkinter.messagebox.showerror("Invalid Url", f"Sorry {entry1_submission} was not able to be pulled. Please ensure the URL is valid and try again")
        switch_frame(input_frame)
        return
    
    current_deck2_info = DeckPuller.get_deck_info(entry2_submission)
    if current_deck2_info is None:
        tkinter.messagebox.showerror("Invalid Url", f"Sorry {entry2_submission} was not able to be pulled. Please ensure the URL is valid and try again")
        switch_frame(input_frame)
        return
    
    switch_frame(option_menu_frame)

def compare_cards() -> None:
    global current_deck1_info
    global current_deck2_info
    
    deck_comparison_info = DeckComparator.compare_mainboards(current_deck1_info['mainboard'], current_deck2_info['mainboard'])
    
    create_difference_results_frame(deck_comparison_info, current_deck1_info['name'], current_deck2_info['name'])
    
    switch_frame(difference_results_frame)

def switch_frame(new: tkinter.Frame) -> None:
    global current_raised_frame
    current_raised_frame.pack_forget()
    new.pack(fill='both', expand=True)
    current_raised_frame = new
    
def clear_frame(frame: tkinter.Frame) -> None:
    for widget in frame.winfo_children():
        widget.destroy()

def setup_mousewheel(frame: tkinter.Frame, canvas: tkinter.Canvas) -> None:
    def enter(event) -> None:
        bound_to_mousewheel(event, canvas)
    def leave(event) -> None:
        unbound_to_mousewheel(event, canvas)
    frame.bind('<Enter>', enter)
    frame.bind('<Leave>', leave)

def bound_to_mousewheel(event, canvas) -> None:
    def on_mousewheel_caller(event) -> None:
        on_mousewheel(event, canvas)
    canvas.bind_all("<MouseWheel>", on_mousewheel_caller)

def unbound_to_mousewheel(event, canvas) -> None:
    canvas.unbind_all("<MouseWheel>")

def on_mousewheel(event, canvas) -> None:
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def format_cards_list(card_dict: dict) -> str:
    output =  ""
    for card in card_dict:
        card_count = card_dict[card]
        output += format_card(card, card_count) + "\n"
    return output

def format_card(card: str, count:int) -> str:
    return f"{count}x {card}"
    
def run():
    create_input_frame()
    create_option_menu_frame()
    input_frame.pack()
    global current_raised_frame
    current_raised_frame = input_frame
    root.mainloop()