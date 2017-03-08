from token_check import token_check
"""
WISH_LIST_OF_MICROEXPRESSIONS:
        - BP + EP -> begin / end proof / theorem / lemma / corollary
        - TLINE -> \\ \hline
        - BT + ET -> begin table center tabular end where BT takes in '|l|l|' parameter to tabular
"""


class MicroExpressions():
    def __init__(self):
        self.exps = [Exp0(), Exp1(), Exp2(), Exp3(), Exp4(), Exp5(), Exp6(),
                     Exp7(), Exp8(), Exp9(), Exp10(), Exp11(), Exp12(), Exp13(),
                     Exp14(), Exp15(), Exp16()]


class Exp():
    def __init__(self, macro):
        self.macro = macro

    def handler(self, line):
        return token_check(line)


class Exp0(Exp):
    def __init__(self):
        Exp.__init__(self, "S")

    def handler(self, line):
        return str("\\section*{" + line[2:-1] + "}")


class Exp1(Exp):
    def __init__(self):
        Exp.__init__(self, "SS")

    def handler(self, line):
        return str("\\subsection*{" + line[3:-1] + "}")
    
    
class Exp2(Exp):
    def __init__(self):
        Exp.__init__(self, "SSS")

    def handler(self, line):
        return str("\\subsubsection*{" + line[4:-1] + "}")
    
    
class Exp3(Exp):
    def __init__(self):
        Exp.__init__(self, "SN")

    def handler(self, line):
        return str("\\section{" + line[2:-1] + "}")
    
    
class Exp4(Exp):
    def __init__(self):
        Exp.__init__(self, "SSN")

    def handler(self, line):
        return str("\\subsection{" + line[3:-1] + "}")
    
    
class Exp5(Exp):
    def __init__(self):
        Exp.__init__(self, "SSSN")

    def handler(self, line):
        return str("\\subsubsection{" + line[4:-1] + "}")


class Exp6(Exp):
    def __init__(self):
        Exp.__init__(self, "BL")

    def handler(self, line):
        return str("\\begin{itemize}")


class Exp7(Exp):
    def __init__(self):
        Exp.__init__(self, "EL")

    def handler(self, line):
        return str("\\end{itemize}")


class Exp8(Exp):
    def __init__(self):
        Exp.__init__(self, "BLN")

    def handler(self, line):
        return str("\\begin{enumerate}")


class Exp9(Exp):
    def __init__(self):
        Exp.__init__(self, "ELN")

    def handler(self, line):
        return str("\\end{enumerate}")


class Exp10(Exp):
    def __init__(self):
        Exp.__init__(self, "BQ")

    def handler(self, line):
        return str("\\begin{displayquote}")


class Exp11(Exp):
    def __init__(self):
        Exp.__init__(self, "EQ")

    def handler(self, line):
        return str("\\end{displayquote}")


class Exp12(Exp):
    def __init__(self):
        Exp.__init__(self, "BB")

    def handler(self, line):
        return str("\\begin{tcolorbox}")


class Exp13(Exp):
    def __init__(self):
        Exp.__init__(self, "EB")

    def handler(self, line):
        return str("\\end{tcolorbox}")


class Exp14(Exp):
    def __init__(self):
        Exp.__init__(self, "IT")

    def handler(self, line):
        l = token_check(line)
        if l[3] == '\\':
            return str("\\item " + l[3:])
        # return str("\\item " + l[3:11] + l[11].upper() + l[12:])
        else:
            return str("\\item " + l[3:])
        # return str("\\item " + l[3].upper() + l[4:])


class Exp15(Exp):
    def __init__(self):
        Exp.__init__(self, "FIG")

    def handler(self, line):
        row = line.split()
        ret = ["\\begin{figure}[H]",
               "  \\begin{center}",
               "    \\includegraphics[width=0." + row[1] + "\\textwidth]{" + row[2] + ".png}",
               "    \\caption{" + ' '.join(row[3:]) + "}",
               "    \\label{label}",
               "  \\end{center}",
               "\\end{figure}"]
        return '\n'.join(ret)


class Exp16(Exp):
    def __init__(self):
        Exp.__init__(self, "LINE")

    def handler(self, line):
        return str("\\rule{\\linewidth}{0.2mm}")
