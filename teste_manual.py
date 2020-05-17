import tkinter as tk
from sudoku import solve_sudoku
import pdb


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.fontePadrao = ("Arial", "20")
        self.create_header(master)
        self.create_entrys(master)
        self.create_footer(master)
        self.soluction_cel = list()

    def create_header(self, master):
        self.header_container = tk.Frame(master)
        self.header_container["pady"] = 10
        self.header_container.pack()
        self.titulo = tk.Label(self.header_container, text="Sudoku Goku")
        self.titulo["font"] = ("Arial", "20", "bold")
        self.titulo.pack()

        self.subheader_container = tk.Frame(master)
        self.subheader_container["pady"] = 10
        self.subheader_container.pack()
        self.warning = tk.Label(self.subheader_container, text="")
        self.warning["font"] = ("Arial", "15", "bold")
        self.warning.pack()

    def create_entrys(self, master):
        vc = (self.register(self.onValidate), '%P', '%S')
        self.containers = list()
        for n in range(12):
            cont = tk.Frame(master)
            cont["padx"] = 20
            cont.pack()
            self.containers.append(cont)

        self.data = list()
        for y in range(12):
            if not y % 4:
                space = tk.Label(self.containers[y], text=" ")
                space.pack(side=tk.LEFT)
            else:
                for x in range(9):
                    if not x % 3:
                        space = tk.Label(self.containers[y], text=" ")
                        space.pack(side=tk.LEFT)

                    nome = tk.Entry(
                        self.containers[y],  validate="key",
                        validatecommand=vc, justify='center')
                    nome["width"] = 2
                    nome["font"] = self.fontePadrao
                    nome.pack(side=tk.LEFT)
                    self.data.append(nome)

    def create_footer(self, master):
        self.footer_container = tk.Frame(master)
        self.footer_container["pady"] = 20
        self.footer_container.pack()

        self.down_footer_container = tk.Frame(master)
        self.down_footer_container["pady"] = 20
        self.down_footer_container.pack()

        self.autenticar = tk.Button(self.footer_container)
        self.autenticar["text"] = "Resolver Sudoku"
        self.autenticar["font"] = ("Calibri", "16")
        self.autenticar["width"] = 15
        self.autenticar["command"] = self.get_sudoku
        self.autenticar.pack(side=tk.LEFT)

        self.limpar = tk.Button(self.footer_container)
        self.limpar["text"] = "Clear"
        self.limpar["font"] = ("Calibri", "16")
        self.limpar["width"] = 15
        self.limpar["command"] = self.clear
        self.limpar.pack(side=tk.LEFT)

        self.limpar_soluction = tk.Button(self.down_footer_container)
        self.limpar_soluction["text"] = "Soluction's Clearing"
        self.limpar_soluction["font"] = ("Calibri", "16")
        self.limpar_soluction["width"] = 20
        self.limpar_soluction["command"] = self.clear_solution
        self.limpar_soluction.pack()

    def onValidate(self, P, S):
        if S and P in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] or P == '':
            return True
        else:
            self.bell()
            return False

    def clear(self):
        for item in self.data:
            item.delete(0, 'end')
            item.config({"background": "White"})
            item.config(fg='black')
        self.soluction_cel = []

    def clear_solution(self):
        for idx, item in enumerate(self.data):
            item.config({"background": "White"})
            item.config(fg='black')
            if idx in self.soluction_cel:
                item.delete(0, 'end')
        self.soluction_cel = []

    def get_sudoku(self):
        sudoku = []
        linha = []

        num = 0
        while num < 81:

            self.data[num].config({"background": "White"})
            linha.append(self.data[num].get())
            if self.data[num].get() == '':
                self.soluction_cel.append(num)
            num += 1

            if not num % 9 and num:
                sudoku.append(linha)
                linha = []

        result, solucao = solve_sudoku(sudoku)

        if result == 0:
            self.warning['text'] = "Solution:"

            idx = 0
            for lin in solucao:
                for col in lin:
                    if self.data[idx].get() == '':
                        self.data[idx].insert(0, str(col))
                    else:
                        self.data[idx].config(fg='green')
                    idx += 1
        if result == 1:
            self.warning['text'] = "Mutiple solutions, exemple:"
            idx = 0
            for lin in solucao:
                for col in lin:
                    if self.data[idx].get() == '':
                        self.data[idx].insert(0, str(col))
                    else:
                        self.data[idx].config(fg='green')
                    idx += 1
        elif result == 2:
            self.warning['text'] = "Sudoku not resovable"

        elif result == 3:
            self.warning['text'] = "Too litle data in the Sudoku"

        elif result == 4:
            self.warning['text'] = 'Conflicts in the Sudoku'
            for cel in solucao:
                loc = (cel[0]*9) + cel[1]
                self.data[loc].config({"background": "Red"})


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sudoku Solver")
    Application(root)
    root.mainloop()
