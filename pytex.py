from __future__ import print_function
import sys

OPCODES = ["S", "SS", "SSS", "BL", "EL", "BQ", "EQ", "IT", "FIG"]
file_name = sys.argv[1]
#file_name = "input.txt"
out = file_name.replace(".txt", ".tex")
text_file = open(file_name, 'r')
sys.stdout = open(out, 'w')

print("\\documentclass{article}")
print("\\pagestyle{plain}")
print("\\usepackage{graphicx, wrapfig, mathpazo, csquotes, float}\n")
print("\\begin{document}\n")
print("\\title{\\textbf{Title}}")
print("\\author{\\textsc{Author}}")
print("\\date{Date}")
print("\\maketitle\n")

for line in text_file:
    row = line.split()
    if row[0] not in OPCODES:
        print(line)
    else:
        if row[0] == OPCODES[0]:
            print("\\section*{" + line[2:-1] + "}")
        elif row[0] == OPCODES[1]:
            print("\\subsection*{" + line[3:-1] + "}")
        elif row[0] == OPCODES[2]:
            print("\\subsubsection*{" + line[4:-1] + "}")
        elif row[0] == OPCODES[3]:
            print("\\begin{itemize}")
        elif row[0] == OPCODES[4]:
            print("\\end{itemize}")
        elif row[0] == OPCODES[5]:
            print("\\begin{displayquote}")
        elif row[0] == OPCODES[6]:
            print("\\end{displayquote}")
        elif row[0] == OPCODES[7]:
            print("\\item " + line[3:-1])
        elif row[0] == OPCODES[8]:
            print("\\begin{figure}[H]")
            print("  \\begin{center}")
            print("    \\includegraphics[width=0."+line[4]+"\\textwidth]{picture.png}")
            print("    \\caption{"+line[6:-1]+"}")
            print("    \\label{label}")
            print("  \\end{center}")
            print("\\end{figure}")

print("\n\\end{document}")
text_file.close()
