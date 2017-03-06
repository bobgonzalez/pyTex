from __future__ import print_function
import sys
from datetime import date

"""
    TODO: handle extra empty lines
    TODO: flag for explicit filename extensions
    TODO: optional date override
    TODO: ability to add packages ", ".join[:-2]
"""

OPCODES = ["S", "SS", "SSS", "BL", "EL", "BQ", "EQ", "IT", "FIG"]
file_name = sys.argv[1]
#file_name = "input.txt"
out = file_name.replace(".txt", ".tex")
text_file = open(file_name, 'r')
sys.stdout = open(out, 'w')
cur_date = date.today()
file_name = file_name.replace("_", "\\_")

print("\\documentclass{article}")
print("\\pagestyle{plain}")
print("\\usepackage{graphicx, wrapfig, mathpazo, csquotes, float}\n")
print("\\begin{document}\n")
print("\\title{\\textbf{" + file_name[:-4] + "}}")
print("\\author{\\textsc{}}")
print("\\date{" + str(cur_date.month) + "/" + str(cur_date.day) + "/" + str(cur_date.year) + "}")
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
            print("\\item " + line[3].upper() + line[4:-1])
            #print("\\item " + line[3:-1])
        elif row[0] == OPCODES[8]:
            print("\\begin{figure}[H]")
            print("  \\begin{center}")
            print("    \\includegraphics[width=0." + row[1] +"\\textwidth]{" + row[2] + ".png}")
            print("    \\caption{" + ' '.join(row[3:]) + "}")
            print("    \\label{label}")
            print("  \\end{center}")
            print("\\end{figure}")
print("\n\\end{document}")
text_file.close()
