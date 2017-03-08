from __future__ import print_function
import sys
from datetime import date
from subprocess import call

"""
    *TODO: handle empty lines
    **TODO: flag for explicit filename extensions
    ***TODO: WYSIWYG GUI
    ***TODO: optional date override (post-GUI)
    ***TODO: ability to add packages ", ".join[:-2] (post-GUI)
    **TODO: adjust vertical spacing of LINE
    *TODO: support tables
    WISH_LIST_OF_MICROEXPRESSIONS:
         'B{' -> \textbf{} (unless '\B{')
         BP + EP -> begin / end proof / theorem / lemma / corollary
         TLINE -> \\ \hline
         BT + ET -> begin table center tabular end where BT takes in '|l|l|' paramenter to tabular
"""


def help_me():
    print("S - Subscetion \nSS - SubSection \nSSS - SubSubSection\n" +
          "SN - Section Numbered\nSSN - SubSection Numbered\nSSSN - SubSubSection Numbered\n" +
          "BL - Begin List\nEL - End List\nBLN - Begin List Numbered\nELN - End List Numbered\n" +
          "BQ - Begin Text Isolation\nEQ - End Text Isolation\nBB - Begin Drawing A Box Around Text\n" +
          "EB - End Drawing A Box Aroung Text\nIT - Item\nFIG - 3 Parameters, space separated\n" +
          "\t percentage of page width < 1, Picture Name (assumes .png), Caption\nLINE - Draw A Line Across Page")


def init():
    opcodes = ["S", "SS", "SSS", "SN", "SSN", "SSSN", "BL", "EL", "BQ", "EQ", "BB", "EB", "IT", "FIG", "BLN", "ELN", "LINE"]
    file_name = sys.argv[1]
    out = file_name.replace(".txt", ".tex")
    text_file = open(file_name, 'r')
    sys.stdout = open(out, 'w')
    cur_date = date.today()
    file_name = file_name.replace("_", "\\_")

    print("\\documentclass{article}")
    print("\\pagestyle{plain}")
    print("\\usepackage{graphicx, wrapfig, mathpazo, csquotes, float, tcolorbox}\n")
    print("\\begin{document}\n")
    print("\\title{\\textbf{" + file_name[:-4] + "}}")
    print("\\author{\\textsc{}}")
    print("\\date{" + str(cur_date.month) + "/" + str(cur_date.day) + "/" + str(cur_date.year) + "}")
    print("\\maketitle\n")

    for line in text_file:
        row = line.split()
        if row[0] not in opcodes:
            print(token_check(line))
        else:
            if row[0] == "S":
                print("\\section*{" + line[2:-1] + "}")
            elif row[0] == "SS":
                print("\\subsection*{" + line[3:-1] + "}")
            elif row[0] == "SSS":
                print("\\subsubsection*{" + line[4:-1] + "}")
            elif row[0] == "SN":
                print("\\section{" + line[2:-1] + "}")
            elif row[0] == "SSN":
                print("\\subsection{" + line[3:-1] + "}")
            elif row[0] == "SSSN":
                print("\\subsubsection{" + line[4:-1] + "}")
            elif row[0] == "BL":
                print("\\begin{itemize}")
            elif row[0] == "EL":
                print("\\end{itemize}")
            elif row[0] == "BLN":
                print("\\begin{enumerate}")
            elif row[0] == "ELN":
                print("\\end{enumerate}")
            elif row[0] == "BQ":
                print("\\begin{displayquote}")
            elif row[0] == "EQ":
                print("\\end{displayquote}")
            elif row[0] == "BB":
                print("\\begin{tcolorbox}")
            elif row[0] == "EB":
                print("\\end{tcolorbox}")
            elif row[0] == "IT":
                l = token_check(line)
                if l[3] == '\\':
                    print("\\item " + l[3:11] + l[11].upper() + l[12:])
                else:
                    print("\\item " + l[3].upper() + l[4:])
                #print("\\item " + line[3:-1])
            elif row[0] == "FIG":
                print("\\begin{figure}[H]")
                print("  \\begin{center}")
                print("    \\includegraphics[width=0." + row[1] +"\\textwidth]{" + row[2] + ".png}")
                print("    \\caption{" + ' '.join(row[3:]) + "}")
                print("    \\label{label}")
                print("  \\end{center}")
                print("\\end{figure}")
            elif row[0] == "LINE":
                print("\\rule{\\linewidth}{0.2mm}")
    print("\n\\end{document}")
    text_file.close()
    sys.stdout = sys.__stdout__
    call(["pdflatex", str(out)])


def token_check(line1):
    sp_line = line1.split()
    for i, token in enumerate(sp_line):
        if token[0:2] == "B{":
            sp_line[i] = "\\textbf" + str(token[1:])
    new_line = ' '.join(sp_line)
    return new_line


if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    help_me()
else:
    init()
