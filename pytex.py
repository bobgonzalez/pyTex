from __future__ import print_function
import sys
from datetime import date
from subprocess import call

"""
    TODO: handle extra empty lines
    TODO: flag for explicit filename extensions
    TODO: optional date override
    TODO: ability to add packages ", ".join[:-2]
    TODO: adjust vertical spacing of LINE
    WISH_LIST_OF_MICROEXPRESSIONS:
         'B{' -> \textbf{} (unless '\B{')
         BP + EP -> begin / end proof / theorem / l
"""
if(sys.argv[1]=='-h' or '--help')
    help()
else
    regular()
def help():
    print("S - Subscetion \n
          SS - SubSection \n
          SSS - SubSubSection\n
          SN - Section Numbered\n
          SSN - SubSection Numbered\n
          SSSN - SubSubSection Numbered\n
          BL - Begin List\n
          EL - End List\n
          BLN - Begin List Numbered\n
          ELN - End List Numbered\n
          BQ - Begin Text Isolation\n
          EQ - End Text Isolation\n
          BB - Begin Drawing A Box Around Text\n
          EB - End Drawing A Box Aroung Text\n
          IT - Item\n
          FIG - 3 Parameters\n
          \t percentage of width of page < 1, Title of Picture,Caption\n
          LINE - Draw A Line Across The Page"
          
def regular():    
    OPCODES = ["S", "SS", "SSS", "SN", "SSN", "SSSN", "BL", "EL", "BQ", "EQ", "BB", "EB", "IT", "FIG", "BLN", "ELN", "LINE"]
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
        if row[0] not in OPCODES:
            print(line)
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
                print("\\item " + line[3].upper() + line[4:-1])
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
