import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from tkinter import messagebox
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x550")
        self.root.config(bg='#1E1E2F')
        self.root.resizable(True, True)
        
        # API Key(I have taken my API key from fixer.io website)
        self.api_key = '7498f7fe950a5bf02bb02bc7151966ba'  
        
        # Applying a theme
        self.root.set_theme("equilux")
        
        # Style configurations for Label and ComboBox
        style = ttk.Style()
        style.configure("TLabel", foreground="white", background="#1E1E2F", font=("Poppins", 12, "bold"))
        style.configure("TCombobox", fieldbackground="white", background="white", font=("Poppins", 12))

        # Title
        self.label_title = Label(self.root, text="Currency Converter", font=("Poppins", 24, "bold"), fg='#F7D44C', bg='#1E1E2F')
        self.label_title.pack(pady=10)

        # Adding an image
        img = Image.open("currency_converter_transparent.png")
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(img)
        self.label_image = Label(self.root, image=self.img, bg="#1E1E2F")
        self.label_image.pack(pady=10)

        # Amount Input
        self.label_amount = Label(self.root, text="Amount", font=("Poppins", 12, "bold"), fg='#F7D44C', bg='#1E1E2F')
        self.label_amount.pack(pady=5)
        self.entry_amount = Entry(self.root, font=("Poppins", 14), bg="#F5F5F5", fg="#34495E", bd=2, relief=FLAT, highlightthickness=1, highlightcolor="#F7D44C")
        self.entry_amount.pack(pady=5)

        # From Currency
        self.label_from = Label(self.root, text="From Currency", font=("Poppins", 12, "bold"), fg='#F7D44C', bg='#1E1E2F')
        self.label_from.pack(pady=5)
        self.combo_from = ttk.Combobox(self.root, values=[
            "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "NZD", "SGD", "ZAR", "BRL", "MXN",
            "AED", "HKD", "KRW", "RUB", "SEK", "NOK", "DKK", "MYR", "THB", "PHP"
        ], font=("Poppins", 12))
        self.combo_from.pack(pady=5)

        # To Currency
        self.label_to = Label(self.root, text="To Currency", font=("Poppins", 12, "bold"), fg='#F7D44C', bg='#1E1E2F')
        self.label_to.pack(pady=5)
        self.combo_to = ttk.Combobox(self.root, values=[
            "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "NZD", "SGD", "ZAR", "BRL", "MXN",
            "AED", "HKD", "KRW", "RUB", "SEK", "NOK", "DKK", "MYR", "THB", "PHP"
        ], font=("Poppins", 12))
        self.combo_to.pack(pady=5)

        # Button Frame (for Convert and Clear buttons)
        button_frame = Frame(self.root, bg="#1E1E2F")
        button_frame.pack(pady=20)

        # Convert Button
        self.button_convert = Button(button_frame, text="Convert", command=self.convert_currency, font=("Poppins", 10, "bold"),
                                     bg="#2980B9", fg="#ECF0F1", relief=FLAT, padx=15, pady=8, borderwidth=2)
        self.button_convert.grid(row=0, column=0, padx=10)

        # Clear Button
        self.button_clear = Button(button_frame, text="Clear", command=self.clear_fields, font=("Poppins", 10, "bold"),
                                   bg="#E74C3C", fg="#ECF0F1", relief=FLAT, padx=15, pady=8, borderwidth=2)
        self.button_clear.grid(row=0, column=1, padx=10)

        # Result Label
        self.label_result = Label(self.root, text="", font=("Poppins", 13, "bold"), fg='#F7D44C', bg='#1E1E2F')
        self.label_result.pack(pady=11)

    def fetch_rates(self, base_currency):
        """Fetch exchange rates from the API."""
        url = f"http://data.fixer.io/api/latest?access_key={self.api_key}&symbols=USD,EUR,GBP,JPY,CAD,AUD,CHF,CNY,INR,NZD,SGD,ZAR,BRL,MXN,AED,HKD,KRW,RUB,SEK,NOK,DKK,MYR,THB,PHP"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('success'):
                return data['rates']
            else:
                messagebox.showerror("Error", f"Error fetching rates: {data['error']['type']}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error connecting to the API: {e}")
            return None

    def convert_currency(self):
        amount = self.entry_amount.get()
        from_currency = self.combo_from.get()
        to_currency = self.combo_to.get()

        if not amount or not from_currency or not to_currency:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
            return

        # Fetch rates and perform conversion
        rates = self.fetch_rates(from_currency)
        if rates:
            if to_currency in rates:
                converted_amount = amount * rates[to_currency]
                self.label_result.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            else:
                messagebox.showerror("Error", f"Currency {to_currency} is not supported.")

    def clear_fields(self):
        """Clear all input fields and the result label."""
        self.entry_amount.delete(0, END)
        self.combo_from.set('')
        self.combo_to.set('')
        self.label_result.config(text="")

# Run the application
if __name__ == "__main__":
    root = ThemedTk()
    app = CurrencyConverterApp(root)
    root.mainloop()



