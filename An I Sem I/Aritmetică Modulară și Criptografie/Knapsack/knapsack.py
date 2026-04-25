import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from math import gcd


# ---------- CRYPTOGRAPHY FUNCTIONS ----------

def generate_super_increasing_sequence(n):
    """Generate a super-increasing sequence"""
    sequence = [random.randint(2, 10)]  # Start smaller
    while len(sequence) < n:
        next_element = sum(sequence) + random.randint(1, 5)  # Smaller increments
        sequence.append(next_element)
    return sequence


def generate_private_key(public_key, q, r):
    """Generate the private key from the public key"""
    private_key = [(r * element) % q for element in public_key]
    return private_key


def knapsack_encrypt(plaintext, public_key):
    """Encrypt the plaintext using the public key"""
    encrypted_message = sum(public_key[i] for i in range(len(plaintext)) if plaintext[i] == '1')
    return encrypted_message


def knapsack_decrypt(ciphertext, private_key, q, r):
    """Decrypt the ciphertext using the private key"""
    r_inverse = pow(r, -1, q)  # Modular multiplicative inverse of r
    c_prime = (ciphertext * r_inverse) % q

    decrypted_message = ''
    for element in reversed(private_key):
        if c_prime >= element:
            decrypted_message = '1' + decrypted_message
            c_prime -= element
        else:
            decrypted_message = '0' + decrypted_message
    return decrypted_message


def generate_keys(n=40):
    """Generate public and private keys for knapsack cryptosystem"""
    # Generate super-increasing sequence (this is the private key W)
    W = generate_super_increasing_sequence(n)

    # Choose q > sum(W)
    q = sum(W) + random.randint(50, 200)  # Smaller range

    # Choose r coprime to q
    r = random.randint(2, q - 1)
    while gcd(r, q) != 1:
        r = random.randint(2, q - 1)

    # Generate public key B
    B = generate_private_key(W, q, r)

    return W, B, q, r


# ---------- GUI APPLICATION ----------

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Cryptosystem")
        self.root.geometry("1000x600")
        self.root.minsize(900, 550)

        # Generate initial keys (use 40 bits for reasonable key sizes)
        self.W, self.B, self.q, self.r = generate_keys(n=40)
        self.cipher = 0
        self.bit_len = 0

        # Animation variables
        self.shake_count = 0
        self.original_x = 0
        self.original_y = 0

        self.setup_gui()
        self.populate_initial_keys()

    def setup_gui(self):
        """Setup the GUI layout"""
        # Create main container frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left side - controls (fixed width)
        left_frame = tk.Frame(main_frame, width=650)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        left_frame.pack_propagate(False)  # Prevent frame from shrinking

        # Right side - backpack image
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load and display backpack image
        try:
            img = Image.open("backpack.png")
            img = img.resize((220, 220), Image.Resampling.LANCZOS)
            self.bag = ImageTk.PhotoImage(img)
            self.bag_label = tk.Label(right_frame, image=self.bag)
            self.bag_label.pack(pady=20)
        except FileNotFoundError:
            # Fallback if image not found
            self.bag_label = tk.Label(right_frame, text="🎒\nKNAPSACK",
                                      font=("Arial", 36), fg="#2c5aa0")
            self.bag_label.pack(pady=20)

        # Generate Keys Button
        tk.Button(left_frame, text="Generate Keys", command=self.generate,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                  padx=10, pady=5).pack(fill=tk.X, pady=(0, 10))

        # Private Key W with scrollbar
        key_frame1 = tk.Frame(left_frame)
        key_frame1.pack(fill=tk.X, pady=5)
        tk.Label(key_frame1, text="Private Key (W):",
                 font=("Arial", 9, "bold"), width=15, anchor='w').pack(side=tk.LEFT)

        w_container = tk.Frame(key_frame1)
        w_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_w = tk.Entry(w_container, font=("Arial", 9))
        self.entry_w.pack(fill=tk.X)
        w_scroll = tk.Scrollbar(w_container, orient=tk.HORIZONTAL, command=self.entry_w.xview)
        w_scroll.pack(fill=tk.X)
        self.entry_w.config(xscrollcommand=w_scroll.set)

        # Public Key B with scrollbar
        key_frame2 = tk.Frame(left_frame)
        key_frame2.pack(fill=tk.X, pady=5)
        tk.Label(key_frame2, text="Public Key (B):",
                 font=("Arial", 9, "bold"), width=15, anchor='w').pack(side=tk.LEFT)

        b_container = tk.Frame(key_frame2)
        b_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_b = tk.Entry(b_container, font=("Arial", 9))
        self.entry_b.pack(fill=tk.X)
        b_scroll = tk.Scrollbar(b_container, orient=tk.HORIZONTAL, command=self.entry_b.xview)
        b_scroll.pack(fill=tk.X)
        self.entry_b.config(xscrollcommand=b_scroll.set)

        # Parameters
        param_frame = tk.Frame(left_frame)
        param_frame.pack(fill=tk.X, pady=5)
        tk.Label(param_frame, text="q, r:",
                 font=("Arial", 9, "bold"), width=15, anchor='w').pack(side=tk.LEFT)
        self.entry_params = tk.Entry(param_frame, font=("Arial", 9))
        self.entry_params.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Message Input
        msg_frame = tk.Frame(left_frame)
        msg_frame.pack(fill=tk.X, pady=5)
        tk.Label(msg_frame, text="Message:",
                 font=("Arial", 9, "bold"), width=15, anchor='w').pack(side=tk.LEFT)
        self.entry_msg = tk.Entry(msg_frame, font=("Arial", 10))
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Encrypt Button
        tk.Button(left_frame, text="Encrypt", command=self.do_encrypt,
                  bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                  padx=10, pady=5).pack(fill=tk.X, pady=10)

        # Binary Representation
        bin_frame = tk.Frame(left_frame)
        bin_frame.pack(fill=tk.X, pady=5)
        tk.Label(bin_frame, text="Binary:",
                 font=("Arial", 9, "bold"), width=15, anchor='w').pack(side=tk.LEFT)
        self.entry_bits = tk.Entry(bin_frame, font=("Courier", 8))
        self.entry_bits.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Ciphertext
        cipher_frame = tk.Frame(left_frame)
        cipher_frame.pack(fill=tk.X, pady=5)
        tk.Label(cipher_frame, text="Ciphertext:",
                 font=("Arial", 9, "bold"), width=15, anchor='w').pack(side=tk.LEFT)
        self.entry_cipher = tk.Entry(cipher_frame, font=("Arial", 10), fg="#d32f2f")
        self.entry_cipher.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Decrypt Button
        tk.Button(left_frame, text="Decrypt", command=self.do_decrypt,
                  bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                  padx=10, pady=5).pack(fill=tk.X, pady=10)

        # Decrypted Message
        result_frame = tk.Frame(left_frame)
        result_frame.pack(fill=tk.X, pady=5)
        tk.Label(result_frame, text="Decrypted:",
                 font=("Arial", 9, "bold"), width=15, anchor='w').pack(side=tk.LEFT)
        self.entry_result = tk.Entry(result_frame, font=("Arial", 10), fg="#388E3C")
        self.entry_result.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Items in Knapsack
        items_label = tk.Label(left_frame, text="Items in Knapsack:",
                               font=("Arial", 9, "bold"), anchor='w')
        items_label.pack(fill=tk.X, pady=(10, 5))

        listbox_frame = tk.Frame(left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.bag_items = tk.Listbox(listbox_frame, font=("Courier", 9),
                                    yscrollcommand=scrollbar.set, height=8)
        self.bag_items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.bag_items.yview)

    def populate_initial_keys(self):
        """Populate the key fields with initial values"""
        self.entry_w.delete(0, tk.END)
        self.entry_w.insert(0, str(self.W))

        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, str(self.B))

        self.entry_params.delete(0, tk.END)
        self.entry_params.insert(0, f"q={self.q}, r={self.r}")

    def generate(self):
        """Generate new keys"""
        self.W, self.B, self.q, self.r = generate_keys()

        self.populate_initial_keys()

        self.bag_items.delete(0, tk.END)
        self.entry_cipher.delete(0, tk.END)
        self.entry_bits.delete(0, tk.END)
        self.entry_result.delete(0, tk.END)
        self.entry_msg.delete(0, tk.END)
        self.cipher = 0
        self.bit_len = 0

    def shake_backpack(self):
        """Animate the backpack with a shake effect"""
        if self.shake_count == 0:
            # Store original position
            self.original_x = self.bag_label.winfo_x()
            self.original_y = self.bag_label.winfo_y()

        if self.shake_count < 10:
            # Alternate offset direction
            offset_x = 8 if self.shake_count % 2 == 0 else -8
            self.bag_label.place(x=self.original_x + offset_x, y=self.original_y)
            self.shake_count += 1
            self.root.after(50, self.shake_backpack)
        else:
            # Reset to pack layout
            self.bag_label.pack(pady=20)
            self.shake_count = 0

    def do_encrypt(self):
        """Encrypt the message"""
        try:
            msg = self.entry_msg.get()
            if not msg:
                messagebox.showwarning("Warning", "Please enter a message to encrypt")
                return

            # Convert message to binary
            bits = "".join(format(ord(c), "08b") for c in msg)

            if len(bits) > len(self.B):
                messagebox.showerror("Error", f"Message too long! Max {len(self.B) // 8} characters")
                return

            self.bit_len = len(bits)

            # Encrypt using the public key
            self.cipher = knapsack_encrypt(bits, self.B)

            # Find which items were selected
            chosen = [self.B[i] for i in range(len(bits)) if bits[i] == '1']

            self.entry_bits.delete(0, tk.END)
            self.entry_bits.insert(0, bits)

            self.entry_cipher.delete(0, tk.END)
            self.entry_cipher.insert(0, str(self.cipher))

            self.bag_items.delete(0, tk.END)
            for x in chosen:
                self.bag_items.insert(tk.END, x)

            # Shake the backpack
            self.shake_backpack()

        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def do_decrypt(self):
        """Decrypt the ciphertext"""
        try:
            if self.cipher == 0 or self.bit_len == 0:
                messagebox.showwarning("Warning", "Please encrypt a message first")
                return

            # Decrypt using the private key
            bits = knapsack_decrypt(self.cipher, self.W, self.q, self.r)

            # Convert binary back to text
            chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
            message = "".join(chr(int(b, 2)) for b in chars if b)

            self.entry_result.delete(0, tk.END)
            self.entry_result.insert(0, message)

            # Shake the backpack
            self.shake_backpack()

        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")


# ---------- MAIN ----------

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()