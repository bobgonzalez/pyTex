def help_me():
    return("___________________________________________________\n" +
          "*The micro-expressions that follow must \n" +
          " be the first word on the line to be expanded\n" +
          "---------------------------------------------------\n" +
          "S  \tSection \n" +
          "SS \tSubSection \n" +
          "SSS \tSubSubSection\n" +
          "SN \tSection Numbered\n" +
          "SSN \tSubSection Numbered\n" +
          "SSSN \tSubSubSection Numbered\n" +
          "BL \tBegin List\n" +
          "EL \tEnd List\n" +
          "BLN \tBegin List Numbered\n" +
          "ELN \tEnd List Numbered\n" +
          "BQ \tBegin Text Isolation\n" +
          "EQ \tEnd Text Isolation\n" +
          "BB \tBegin Drawing A Box Around Text\n" +
          "EB \tEnd Drawing A Box Around Text\n" +
          "IT \tItem\n" +
          "LINE \tDraw A Line Across Page\n" +
          "FIG \t3 Parameters, space separated\n" +
          "\t\t% of Page-Width < 1, \n" +
          "\t\tPicture Name (assumes .png), \n" +
          "\t\tCaption\n" +
          "___________________________________________________\n" +
          "*The micro-expressions that follow may \n" +
          " be any word on the line and will be expanded\n" +
          "---------------------------------------------------\n" +
          "B{ \tBolds all text till closing },\n" +
          "\tmust have a space preceding it\n" +
          "___________________________________________________"
          )
