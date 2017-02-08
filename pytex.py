from __future__ import print_function
import sys

OPCODES = ["S", "SS", "SSS", "BL", "EL", "BQ", "EQ", "IT", "FIG"]
#file_name = sys.argv
file_name = "input.txt"
out = file_name.replace(".txt", ".tex")
tex_file = open(out, 'w')
text_file = open(file_name, 'r')

print("\\documentclass{article}", file=tex_file)
print("\\pagestyle{plain}", file=tex_file)
print("\\usepackage{graphicx, wrapfig, mathpazo, csquotes, float}\n", file=tex_file)
print("\\begin{document}\n", file=tex_file)
print("\\title{\\textbf{Title}}", file=tex_file)
print("\\author{\\textsc{Author}}", file=tex_file)
print("\\date{Date}", file=tex_file)
print("\\maketitle\n", file=tex_file)

for line in text_file:
    row = line.split()
    if row[0] not in OPCODES:
        print(line, file=tex_file)
    else:
        if row[0] == OPCODES[0]:
            print("\\section*{" + line[2:-1] + "}", file=tex_file)
        elif row[0] == OPCODES[1]:
            print("\\subsection*{" + line[3:-1] + "}", file=tex_file)
        elif row[0] == OPCODES[2]:
            print("\\subsubsection*{" + line[4:-1] + "}", file=tex_file)
        elif row[0] == OPCODES[3]:
            print("\\begin{itemize}", file=tex_file)
        elif row[0] == OPCODES[4]:
            print("\\end{itemize}", file=tex_file)
        elif row[0] == OPCODES[5]:
            print("\\begin{displayquote}", file=tex_file)
        elif row[0] == OPCODES[6]:
            print("\\end{displayquote}", file=tex_file)
        elif row[0] == OPCODES[7]:
            print("\\item " + line[3:-1], file=tex_file)
        elif row[0] == OPCODES[8]:
            print("\\begin{figure}[H]", file=tex_file)
            print("  \\begin{center}", file=tex_file)
            print("    \\includegraphics[width=0."+line[4]+"\\textwidth]{picture.png}", file=tex_file)
            print("    \\caption{"+line[6:]+"}", file=tex_file)
            print("    \\label{label}", file=tex_file)
            print("  \\end{center}", file=tex_file)
            print("\\end{figure}", file=tex_file)

print("\n\\end{document}", file=tex_file)
text_file.close()
tex_file.close()
