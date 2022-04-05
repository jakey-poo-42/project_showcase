class Inputs:
    """
    Class outlines functions for updating the cnf dictionary -- used to convert rules to cnf form, collecting
    hard constraints, and collecting rules for penalty, possibilistic, and qualitative logics.
    """
    def updateDictionary(self, attributes: list):
        """
        Reads through each item in the list, splitting at the comma and creating a dictionary for the integer value
        of the attribute options before inverting the dictionary and returning a list containing both the default
        and inversed dictionary.

        :param attributes:  List of attributes which contain every option combination determined by the user.
        :return:            List with first value being the cnfDictionary and the second value being the inverse.
        """
        count = 1
        dictionary = {}
        for item in attributes:
            readattr = item.split(',')
            dictionary[readattr[0]] = count
            dictionary[readattr[1]] = -count
            count += 1
        revDictionary = {v: k for k, v in dictionary.items()}
        twoDictionaries = [dictionary, revDictionary]
        return twoDictionaries

    def cnfConstraints(self, constraints: list, cnfDict: dict):
        """
        Reads through each item in the list, creating a string in cnf form (as per the requirements for using clasp)
        and returning it after reading through the list.

        :param constraints: List of contraints which contain every clause for determining feasible objects.
        :param cnfDict:     The cnfDictionary which contains the cnf values of each attribute option.
        :return:            Returns a string which matches the file input for clasp.
        """
        attr = cnfDict
        numattributes = int(len(attr) / 2)
        numclauses = 0
        textformat = ""
        lastnot = False
        for constr in constraints:
            if textformat != "":
                textformat += "\n"
            parseconstr = constr.split()
            for term in parseconstr:
                if term == "NOT":
                    lastnot = True
                elif lastnot:
                    item = int(attr[term]) * -1
                    textformat += str(item)
                    lastnot = False
                elif term == "AND":
                    numclauses += 1
                    textformat += " 0\n"
                elif term == "OR":
                    textformat += " "
                else:
                    textformat += str(attr[term])
            numclauses += 1
            textformat += " 0"
        cnfString = "p cnf " + str(numattributes) + " " + str(numclauses) + "\n" + textformat
        return cnfString

    def cnfLogic(self, logicLines: list, cnfDict: dict):
        """
        Used for penalty and possibilistic logics, reads through each item in the list, splitting at the comma to save
        the value of the condition and creates a string in cnf form. The string and value are paired in a tuple and
        appended to a list, which is returned at the end of the function.

        :param logicLines:  List of rules which contain a clause and value attached to that clause for either
                            penalty or possibilistic logic rules.
        :param cnfDict:     The cnfDictionary which contains the cnf values of each attribute option.
        :return:            Returns list of tuples in format of [(cnfstring, value), ...]
        """
        logic = cnfDict
        numattr = int(len(logic) / 2)
        numclauses = 1
        textformat = ""
        logictuples = []
        lastnot = False
        for lines in logicLines:
            parselogic = lines.split(',')
            numsave = str(parselogic[1])
            parselogic = parselogic[0].split()
            for term in parselogic:
                if term == "NOT":
                    lastnot = True
                elif lastnot:
                    item = int(logic[term]) * -1
                    textformat += str(item)
                    lastnot = False
                elif term == "AND":
                    textformat += " 0\n"
                    numclauses += 1
                elif term == "OR":
                    textformat += " "
                else:
                    textformat += str(logic[term])
            cnfLogic = "p cnf " + str(numattr) + " " + str(numclauses) + "\n" + textformat + " 0"
            t = cnfLogic, numsave
            logictuples.append(t)
            textformat = ""
            numclauses = 1
        return logictuples

    def cnfQualitative(self, qualLines: list, cnfDict: dict):
        """
        Used for qualitative logic, reads through each item in the list, first checking to see if there is a condition
        before saving it -- or 0 to mark no conditon -- and splits at the IF, reading through each item to determine the
        cnf form string for each line and preparing a list of tuples which contain the condition and a nested tuple of
        each rule matching the condition that it will return.

        :param qualLines:   List of rules which contain a clause and (optionally) a value attached to that clause for
                            qualitative logic rules.
        :param cnfDict:     The cnfDictionary which contains the cnf values of each attribute option.
        :return:            Returns list of tuples in format of [(condition, (cnf, ...)), ...]
        """
        numattr = int(len(cnfDict) / 2)
        numclauses = 1
        textformat = ""
        qualtuples = []
        rule = []
        lastnot = False
        for lines in qualLines:
            if lines.endswith("IF"):
                condition = "0"
                qualitems = lines.split("IF")
                quallist = qualitems[0].split()
            else:
                qualitems = lines.split("IF")
                qualitems[1] = qualitems[1].replace(" ", "")
                condition = str(cnfDict[qualitems[1]])
                quallist = qualitems[0].split()
            for term in quallist:
                if term == "NOT":
                    lastnot = True
                elif lastnot:
                    item = int(cnfDict[term]) * -1
                    textformat += str(item)
                    lastnot = False
                elif term == "AND":
                    textformat += " 0\n"
                    numclauses += 1
                elif term == "OR":
                    textformat += " "
                elif term == "BT":
                    cnfQual = "p cnf " + str(numattr) + " " + str(numclauses) + "\n" + textformat + " 0"
                    rule.append(cnfQual)
                    textformat = ""
                    numclauses = 1
                else:
                    textformat += str(cnfDict[term])
            cnfQual = "p cnf " + str(numattr) + " " + str(numclauses) + "\n" + textformat + " 0"
            rule.append(cnfQual)
            t = condition, tuple(rule)
            qualtuples.append(t)
            rule[:] = []
            textformat = ""
            numclauses = 1
        return qualtuples
