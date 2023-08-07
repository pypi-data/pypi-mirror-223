import tkinter as tk
class LanguageType():
    def __init__(self, language_type : str, row_size : int, column_size : int):
        self.language_type = language_type
        self.row_size = row_size
        self.column_size = column_size
        self.braille_dict = self.get_braille_dict()

    def get_braille_dict(self):
        if self.language_type == 'en':
            braille_dict = {'':'000000','a':"100000", 'b': "110000", 'c': '100100', 'd': '100110', 'e': '100010', 'f': '110100', 'g': '110110', 'h': '110010', 'i': '010100', 'j': '010110', 'k': '101000', 'l': '111000', 'm': '101100', 'n': '101110', 'o': '101010', 'p': '111100', 'q': '111110', 'r': '111010', 's': '011100', 't': '011110', 'u': '101001', 'v': '111001', 'w': '010111', 'x': '101101', 'y': '101111', 'z': '101011'}
        return braille_dict
    
    def display_matrix(self):
        braille_dict = self.get_braille_dict()
        
        def cell_clicked(event):
            cell = event.widget
            cell.config(text=entry.get())

        def convert_to_matrix():
            matrix = []
            bin_matrix = []
            for i in range(rows):
                row = []
                for j in range(columns):
                    cell_index = i * columns + j
                    cell_text = cells[cell_index].cget("text")
                    row.append(cell_text)
                matrix.append(row)
            for row in matrix:
                print(row)
            for row in matrix:
                first_row = ''
                second_row = ''
                third_row = ''
                for j in row:
                    first_row += braille_dict[j][:2]
                    second_row += braille_dict[j][2:4:]
                    third_row += braille_dict[j][4:6:]
                bin_matrix.append(first_row)
                bin_matrix.append(second_row)
                bin_matrix.append(third_row)
            print(bin_matrix)
            with open('bin_matrix.txt', 'a') as f:
                f.write(str(bin_matrix))

        def create_cells():
            global cells
            cells = []
            for i in range(rows):
                for j in range(columns):
                    cell = tk.Label(cell_frame, width=5, height=2, relief=tk.RAISED)
                    cell.grid(row=i, column=j)
                    cell.bind("<Button-1>", cell_clicked)
                    cells.append(cell)

        root = tk.Tk()
        root.title("Cell Window")

        # Entry widget to type letters
        entry = tk.Entry(root)
        entry.pack()

        # Button to convert letters to string matrix
        convert_button = tk.Button(root, text="Convert to Matrix", command=convert_to_matrix)
        convert_button.pack()

        # Frame to hold cells
        cell_frame = tk.Frame(root)
        cell_frame.pack()

        rows = self.row_size
        columns = self.column_size

        create_cells()

        root.mainloop()
