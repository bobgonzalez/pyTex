from __future__ import print_function
import sys
from datetime import date
from subprocess import call

"""
    *TODO: handle empty lines
    *TODO: support tables
    **TODO: flag for explicit filename extensions
    **TODO: adjust vertical spacing of LINE

    WISH_LIST_FOR_GUI:
        - ability to add packages ", ".join[:-2]
        - optional date override
        - WYSIWYG GUI (left pane = editor, right pane = viewer, bottom slice = stout buffer)
        - add / remove micro-expression definition

    WISH_LIST_OF_MICROEXPRESSIONS:
        - BP + EP -> begin / end proof / theorem / lemma / corollary
        - TLINE -> \\ \hline
        - BT + ET -> begin table center tabular end where BT takes in '|l|l|' parameter to tabular
"""


def help_me():
    print("___________________________________________________" +
          "\n*The micro-expressions that follow must \n be the first word on the line to be expanded" +
          "\n---------------------------------------------------" +
          "\nS  \tSection \nSS \tSubSection \nSSS \tSubSubSection\n" +
          "SN \tSection Numbered\nSSN \tSubSection Numbered\nSSSN \tSubSubSection Numbered\n" +
          "BL \tBegin List\nEL \tEnd List\nBLN \tBegin List Numbered\nELN \tEnd List Numbered\n" +
          "BQ \tBegin Text Isolation\nEQ \tEnd Text Isolation\nBB \tBegin Drawing A Box Around Text\n" +
          "EB \tEnd Drawing A Box Around Text\nIT \tItem\nLINE \tDraw A Line Across Page" +
          "\nFIG \t3 Parameters, space separated\n" +
          "\t\t% of Page-Width < 1, \n\t\tPicture Name (assumes .png), \n\t\tCaption" +
          "\n___________________________________________________" +
          "\n*The micro-expressions that follow may \n be any word on the line and will be expanded" +
          "\n---------------------------------------------------" +
          "\nB{ \tBolds all text till closing },\n\tmust have a space preceding it" +
          "\n___________________________________________________"
          )


def init():
    opcodes = ["S", "SS", "SSS", "SN", "SSN", "SSSN", "BL", "EL", "BQ", "EQ", "BB", "EB", "IT", "FIG", "BLN", "ELN", "LINE"]
    file_name = sys.argv[1]
    out = file_name.replace(".txt", ".tex")
    try:
        text_file = open(file_name, 'r')
    except (IOError, OSError) as e:
        #invalid_file()
        print("file " + file_name + " not found! \nPlease enter file in local directory or absolute path to file.")
        return
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
