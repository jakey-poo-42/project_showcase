import tkinter as tk
from tkinter import *
from tkinter import messagebox
from inputs import Inputs as middleMan
from preferenceLogic import Logic as brain

BA_Options = [] #for error checking if the option name already exists
attrOptions = [] #list of options for each attribute seperated by a comma
hardConstraints = [] #list of hard constraints (string)
pref_penalty = [] #list of penalty logic
pref_possible = [] #list of possiblistic logic
pref_qualitative = [] #list of qualitative logic
feasibleObjects = [] #feasible objects (clasp)

root = tk.Tk() #establishing root window
root.title("CAP4630 Project 3")

"""TASK METHOD DEFINITIONS"""
#pop up window for exemplify
def exemplify():
    """
    Chooses two random feasible objects and, using the different preference logics,
    returns the object that is more preferred.
    param: N/A (info either generated in-function or recieved from outer scope)
    :return: N/A (window opens)
    """
    if len(pref_penalty) != 0 and len(pref_possible) != 0 and len(pref_qualitative) != 0 and len(feasibleObjects) != 0:
        exemp_win = Toplevel(taskFrame)
        exemp_win.title("Exemplify")

        cnf = middleMan()
        cnfDictionaries = cnf.updateDictionary(attrOptions)
        cnfPen = cnf.cnfLogic(pref_penalty, cnfDictionaries[0])
        cnfPoss = cnf.cnfLogic(pref_possible, cnfDictionaries[0])
        cnfQual = cnf.cnfQualitative(pref_qualitative, cnfDictionaries[0])
        rules = (cnfPen, cnfPoss, cnfQual)
        logic = brain()
        output = logic.exemplify(feasibleObjects[0], rules)
        claspObj = output[0]
        objects = revertClasp(cnfDictionaries[1], claspObj)

        ob1 = StringVar()
        ob2 = StringVar()
        obPen = StringVar()
        obPoss = StringVar()
        obQual = StringVar()
        ob1.set(objects[0])
        ob2.set(objects[1])
        if int(output[1]) == 1:
            obPen.set("Object 1")
        elif int(output[1]) == 2:
            obPen.set("Object 2")
        else:
            obPen.set("Congruent")
        if int(output[2]) == 1:
            obPoss.set("Object 1")
        elif int(output[2]) == 2:
            obPoss.set("Object 2")
        else:
            obPoss.set("Congruent")
        if int(output[3]) == 1:
            obQual.set("Object 1")
        elif int(output[3]) == 2:
            obQual.set("Object 2")
        elif int(output[3] == -1):
            obQual.set("Incomparable")
        else:
            obQual.set("Congruent")
        

        ob1Label = Label(exemp_win, text="Object 1")
        ob2Label = Label(exemp_win, text= "Object 2")
        prefLabelFrame = LabelFrame(exemp_win, text= "Objects with Higher Preference", padx=10,pady=10)
        penLabel = Label(prefLabelFrame, text="Penalty Logic")
        possLabel = Label(prefLabelFrame, text="Possiblistic Logic")
        qualLabel = Label(prefLabelFrame, text="Qualitative Choice Logic")

        ob1Entry = Entry(exemp_win, textvariable=ob1, state=DISABLED, width=50)
        ob2Entry = Entry(exemp_win, textvariable=ob2, state=DISABLED, width=50)
        ob1_scrollH = Scrollbar(exemp_win, orient='horizontal', command=ob1Entry.xview)
        ob1_scrollH.grid(row=2, column=0, sticky='ew')
        ob1Entry['xscrollcommand'] = ob1_scrollH.set
        ob2_scrollH = Scrollbar(exemp_win, orient='horizontal', command=ob2Entry.xview)
        ob2_scrollH.grid(row=2, column=1, sticky='ew')
        ob2Entry['xscrollcommand'] = ob2_scrollH.set

        penEntry = Entry(prefLabelFrame, textvariable=obPen, state=DISABLED)
        possEntry = Entry(prefLabelFrame, textvariable=obPoss, state=DISABLED)
        qualEntry = Entry(prefLabelFrame, textvariable=obQual, state=DISABLED)

        ob1Label.grid(row=0,column=0)
        ob2Label.grid(row=0,column=1)
        ob1Entry.grid(row=1,column=0)
        ob2Entry.grid(row=1,column=1)

        prefLabelFrame.grid(row=3)
        penLabel.grid(row=0,column=0)
        possLabel.grid(row=1,column=0)
        qualLabel.grid(row=2,column=0)
        penEntry.grid(row=0,column=1)
        possEntry.grid(row=1,column=1)
        qualEntry.grid(row=2,column=1)
    else:
        messagebox.showinfo("ERROR: Preferences/Feasible Objects Empty", "Please make sure you've generated all preferences and feasible objects.")
    
#pop up window for optimize
def optimize():
    """
    From the feasible objects that are currently generated, will display an optimal object for each of the
    three preference logics.
    :param: N/A (info either generated in-function or recieved from outer scope)
    :return: N/A (window opens)
    """
    if len(pref_penalty) != 0 and len(pref_possible) != 0 and len(pref_qualitative) != 0 and len(feasibleObjects) != 0:
        messagebox.showinfo("Load Warning", "This process may take a while. A window will pop up with the results when ready. \n(To start the computation, please press \"OK\")")
        op_win = Toplevel(taskFrame)
        op_win.title("Optimal Objects for Each Preference")

        cnf = middleMan()
        cnfDictionaries = cnf.updateDictionary(attrOptions)
        cnfPen = cnf.cnfLogic(pref_penalty, cnfDictionaries[0])
        cnfPoss = cnf.cnfLogic(pref_possible, cnfDictionaries[0])
        cnfQual = cnf.cnfQualitative(pref_qualitative, cnfDictionaries[0])
        rules = (cnfPen, cnfPoss, cnfQual)
        logic = brain()
        output = logic.optimize(feasibleObjects[0], rules)
        objects = revertClasp(cnfDictionaries[1], output)

        #print(output)
        #print(objects)

        obPen = StringVar()
        obPoss = StringVar()
        obQual = StringVar()
        obPen.set(objects[0])
        obPoss.set(objects[1])
        obQual.set(objects[2])

        opPenLabel = Label(op_win, text="Penalty Logic").grid(row=0,column=0)
        opPossPLabel = Label(op_win, text="Possibilistic Logic").grid(row=1,column=0)
        opQualLabel = Label(op_win, text="Qualitative Choice Logic").grid(row=2,column=0)

        opPenEntry = Entry(op_win, textvariable=obPen, state=DISABLED,width=100).grid(row=0,column=1)
        opPossEntry = Entry(op_win, textvariable=obPoss, state=DISABLED,width=100).grid(row=1,column=1)
        opQualEntry = Entry(op_win, textvariable=obQual, state=DISABLED,width=100).grid(row=2,column=1)
        
    else:
        messagebox.showinfo("ERROR: Preferences/Feasible Objects Empty", "Please make sure you've generated all preferences and feasible objects.")

#pop up window for omni-optimize
def omni():
    """
    From the feasible objects that are currently generated, will display all feasible objects w.r.t
    each of the three preference logics.
    :param: N/A (info either generated in-function or recieved from outer scope)
    :return: N/A (window opens)
    """
    if len(pref_penalty) != 0 and len(pref_possible) != 0 and len(pref_qualitative) != 0 and len(feasibleObjects) != 0:
        messagebox.showinfo("Load Warning", "This process may take a while. A window will pop up with the results when ready. \n(To start the computation, please press \"OK\")")
        omni_win = Toplevel(taskFrame)
        omni_win.title("Omni-Optimize")

        cnf = middleMan()
        cnfDictionaries = cnf.updateDictionary(attrOptions)
        cnfPen = cnf.cnfLogic(pref_penalty, cnfDictionaries[0])
        cnfPoss = cnf.cnfLogic(pref_possible, cnfDictionaries[0])
        cnfQual = cnf.cnfQualitative(pref_qualitative, cnfDictionaries[0])
        rules = (cnfPen, cnfPoss, cnfQual)
        logic = brain()
        output = logic.omniOptimize(feasibleObjects[0], rules)
        
        objs_pen = revertClasp(cnfDictionaries[1], output[0])
        objs_poss = revertClasp(cnfDictionaries[1], output[1])
        objs_qual = revertClasp(cnfDictionaries[1], output[2])

        omniPenLabel = Label(omni_win, text="Penalty Logic").grid(row=0,column=0)
        omniPossPLabel = Label(omni_win, text="Possibilistic Logic").grid(row=0,column=2)
        omniQualLabel = Label(omni_win, text="Qualitative Choice Logic").grid(row=0,column=4)

        omniPen_lbox = Listbox(omni_win, width=60)
        omniPoss_lbox = Listbox(omni_win, width=60)
        omniQual_lbox = Listbox(omni_win, width=60)

        omniPen_scrollV = Scrollbar(omni_win, orient='vertical', command=omniPen_lbox.yview)
        omniPen_lbox['yscrollcommand'] = omniPen_scrollV.set
        omniPen_lbox.grid(row=1,column=0)
        omniPen_scrollV.grid(row=1, column=1, sticky='ns')
        omniPen_scrollH = Scrollbar(omni_win, orient='horizontal', command=omniPen_lbox.xview)
        omniPen_lbox['xscrollcommand'] = omniPen_scrollH.set
        omniPen_scrollH.grid(row=2, column=0, sticky='ew')

        omniPoss_scroll = Scrollbar(omni_win, orient='vertical', command=omniPoss_lbox.yview)
        omniPoss_lbox['yscrollcommand'] = omniPoss_scroll.set
        omniPoss_lbox.grid(row=1,column=2)
        omniPoss_scroll.grid(row=1, column=3, sticky='ns')
        omniPoss_scrollH = Scrollbar(omni_win, orient='horizontal', command=omniPoss_lbox.xview)
        omniPoss_lbox['xscrollcommand'] = omniPoss_scrollH.set
        omniPoss_scrollH.grid(row=2, column=2, sticky='ew')

        omniQual_scroll = Scrollbar(omni_win, orient='vertical', command=omniQual_lbox.yview)
        omniQual_lbox['yscrollcommand'] = omniQual_scroll.set
        omniQual_lbox.grid(row=1,column=4)
        omniQual_scroll.grid(row=1, column=5, sticky='ns')
        omniQual_scrollH = Scrollbar(omni_win, orient='horizontal', command=omniQual_lbox.xview)
        omniQual_lbox['xscrollcommand'] = omniQual_scrollH.set
        omniQual_scrollH.grid(row=2, column=4, sticky='ew')

        for obj in objs_pen:
            omniPen_lbox.insert(END, obj)
        for obj in objs_poss:
            omniPoss_lbox.insert(END, obj)
        for obj in objs_qual:
            omniQual_lbox.insert(END, obj)
    else:
        messagebox.showinfo("ERROR: Preferences/Feasible Objects Empty", "Please make sure you've generated all preferences and feasible objects.")

"""END TASK METHOD DEFINITIONS"""

"""ERROR CHECKING"""
def check_valid(test, qual):
    """
    Will check to see if the given input is a valid conditional is valid given
    current binary attributes.
    :param test: conditional statement in the form of a string
    :param qual: boolean value to determine if the conditional is qualitative logic or not
    :return: integer value that is associated with error message for error_checking function
    """
    not_item = False
    need_item = True
    need_comparison = False
    if qual:
        if_comparison = False
        for item in test.split():
            if item == "AND" or item == "BT":
                if need_item or not need_comparison:
                    error_checking(3)
                    return 1
                else:
                    need_item = True
                    need_comparison = False
            elif item == "IF":
                if if_comparison or need_item or not need_comparison:
                    error_checking(3)
                    return 1
                else:
                    if_comparison = True
                    need_comparison = False
                    need_item = True
            elif item in BA_Options:
                if need_comparison or not need_item:
                    error_checking(4)
                    return 1
                elif if_comparison:
                    need_comparison = False
                    need_item = False
                else:
                    need_comparison = True
                    need_item = False
            else:
                error_checking(6)
                return 1
        if not if_comparison:
            error_checking(9)
            return 1
        else:
            return 0
    else:
        for item in test.split():
            if item == "NOT":
                if not_item:
                    error_checking(1)
                    return 1
                elif need_comparison:
                    error_checking(2)
                    return 1
                else: # success
                    not_item = True
            elif item == "AND" or item == "OR":
                if need_item:
                    error_checking(3)
                    return 1
                else: # success
                    need_item = True
                    need_comparison = False
            elif item in BA_Options:
                if need_comparison:
                    error_checking(4)
                    return 1
                elif not_item:
                    not_item = False
                need_item = False
                need_comparison = True
            else:
                error_checking(5)
                return 1
        if need_item:
            error_checking(6)
            return 1
        else:
            return 0

def error_checking(num):
    """
    Makes a pop-up window with corresponding error message for the conditionals from check_valid function.
    :param num: integer value from check_valid corresponding to each error message (1-9)
    :return: N/A (pop-up window)
    """
    if num == 1:
        messagebox.showinfo("ERROR: Syntax", "There cannot be more than two NOT statements used in a row.")
        return
    elif num == 2:
        messagebox.showinfo("ERROR: Syntax", "There cannot be a NOT statement before a comparison.")
        return
    elif num == 3:
        messagebox.showinfo("ERROR: Syntax", "There cannot be two comparisons in a row.")
        return
    elif num == 4:
        messagebox.showinfo("ERROR: Syntax", "There cannot be two items in a row.")
        return
    elif num == 5:
        messagebox.showinfo("ERROR: Syntax", "The item name does not correlate to any attributes.")
        return
    elif num == 6:
        messagebox.showinfo("ERROR: Syntax", "There cannot be unresolved comparisons.")
        return
    elif num == 7:
        messagebox.showinfo("ERROR: Syntax", "BT and IF statements can only be used in qualitative logic rules.")
        return
    elif num == 8:
        messagebox.showinfo("ERROR: Syntax", "Comparisons cannot be made for conditions.")
        return
    elif num == 9:
        messagebox.showinfo("ERROR: Syntax", "Qualitative logic needs an IF statement -- even if there's no condition")

"""END ERROR CHECKING"""

"""ADD BUTTON DEFINITIONS"""
def binAtr_add():
    """
    Adds an attribute from the user input from the GUI, making it into objects to use later.
    :param: N/A (variables either in outer scope or in GUI entry field)
    :return: N/A (will add object if no errors, will make error message if not all entry boxes are filled)
    """
    userAtr = binAtr_entr_attr.get()
    userAtr = userAtr.replace(" ","-")
    userOp1 = binAtr_entr_op1.get()
    userOp1 = userOp1.replace(" ","-")
    userOp2 = binAtr_entr_op2.get()
    userOp2 = userOp2.replace(" ","-")
    if userAtr != "" and userOp1 != "" and userOp2 != "":
        statement = userAtr + ": " + userOp1 + ", " + userOp2
        binAtr_lbox.insert(END, statement)
        attrOptions.append(str(userOp1 + "," + userOp2))
        BA_Options.append(userOp1)
        BA_Options.append(userOp2)
        binAtr_entr_attr.delete(0, END)
        binAtr_entr_op1.delete(0,END)
        binAtr_entr_op2.delete(0,END)
        #print(attrOptions)
    else:
        messagebox.showinfo("ERROR: Binary Attributes","Please fill in all entries before entering a binary attribute.")
    
def hardConstr_add():
    """
    Adds a hard constraint from the user input from the GUI, making it into objects to use later.
    :param: N/A (variables either in outer scope or in GUI entry field)
    :return: N/A (will add object if no errors, will make error message pop-up if error encountered)
    """
    userHardConstr = hardConstr_entr_constr.get()
    result = check_valid(userHardConstr, False)
    if result == 0:
        hardConstr_lbox.insert(END, userHardConstr)
        hardConstr_entr_constr.delete(0,END)
        hardConstraints.append(userHardConstr)
        #print(hardConstraints)

def pen_add():
    """
    Adds a penalty preference from the user input from the GUI, making it into objects to use later.
    :param: N/A (variables either in outer scope or in GUI entry field)
    :return: N/A (will add object if no errors, will make error message pop-up if error encountered)
    """
    userPenalty = pen_entr_pref.get()
    userValue = pen_entr_val.get()
    if userValue.isnumeric() == False:
        messagebox.showinfo("ERROR: Non-numeric Value", "Please enter an integer value for the \"Value\" field.")
    else:
        result = check_valid(userPenalty, False)
        if result == 0:
            statement = userPenalty + "," + str(userValue)
            pen_lbox.insert(END, statement)
            pref_penalty.append(statement)
            pen_entr_pref.delete(0, END)
            pen_entr_val.delete(0, END)

def poss_add():
    """
    Adds a possibilistic preference from the user input from the GUI, making it into objects to use later.
    :param: N/A (variables either in outer scope or in GUI entry field)
    :return: N/A (will add object if no errors, will make error message pop-up if error encountered)
    """
    userPoss = poss_entr_pref.get()
    userValue = poss_entr_val.get()
    val = False
    try:
        userValue = float(userValue)
        if(userValue > 1 or userValue < 0):
            messagebox.showinfo("ERROR: Non-numeric Value", "Please enter an decimal value between 0 and 1 for the \"Value\" field.")
            val = False
        else: 
            val = True
    except:
         messagebox.showinfo("ERROR: Non-numeric Value", "Please enter a valid decimal for the \"Value\" field.")
         val = False

    if val == True:
        result = check_valid(userPoss, False)
        if result == 0:
            statement = userPoss + "," + str(userValue)
            poss_lbox.insert(END, statement)
            pref_possible.append(statement)
            poss_entr_pref.delete(0, END)
            poss_entr_val.delete(0, END)

def qual_add():
    """
    Adds a wualitative choice logic preference from the user input from the GUI, making it into objects to use later.
    :param: N/A (variables either in outer scope or in GUI entry field)
    :return: N/A (will add object if no errors, will make error message pop-up if error encountered)
    """
    userQual = qual_entr_pref.get()
    result = check_valid(userQual, True)
    if result == 0:
        pref_qualitative.append(userQual)
        qual_lbox.insert(END, userQual)
        qual_entr_pref.delete(0,END)

"""END ADD BUTTON DEFINITIONS"""

"""UPDATE WITH FILE INFO"""
def updateAttr():
    """
    Opens attributes.txt and makes them into attribute/options objects that are used later.
    :param: N/A (file opened in function, GUI objects within outer scope)
    :return: N/A (objects added to respective lists in outer scope)
    """
    with open ('attributes.txt') as attrfile:
        readattr = attrfile.readline()
        attrnames = []

        while readattr != '':
            parseattr = readattr.split(':')
            head = parseattr[0]
            if head in attrnames:
                readattr = attrfile.readline()
                parseattr[:] = []
                continue
            attrnames.append(head)
            parseattr = parseattr[1].split(',')
            parseattr[0]=parseattr[0].replace(" ","")
            parseattr[1]=parseattr[1].replace(" ","")
            parseattr[0]=parseattr[0].replace("\n","")
            parseattr[1]=parseattr[1].replace("\n","")
            BA_Options.append(parseattr[0])
            BA_Options.append(parseattr[1])
            options = parseattr[0] + "," + parseattr[1]
            statement = head + ": " + parseattr[0] + ", " + parseattr[1]
            binAtr_lbox.insert(END, statement)
            attrOptions.append(options)
            " incrementing & reseting "
            readattr = attrfile.readline()
            parseattr[:] = []
    #print(attrOptions)
        
def updateHardConstr():
    """
    Opens constraints.txt and makes them into hard constraints objects that are used later.
    :param: N/A (file opened in function, GUI objects within outer scope)
    :return: N/A (objects added to respective lists in outer scope)
    """
    with open ('constraints.txt') as constrfile:
        readconstr = constrfile.readline()
        while readconstr != '':
            readconstr = readconstr.replace("\n","")
            hardConstraints.append(readconstr)
            hardConstr_lbox.insert(END, readconstr)
            readconstr = constrfile.readline()
    #print(hardConstraints)

def updatePenalty():
    """
    Opens penalty.txt and makes them into penalty preference objects that are used later.
    :param: N/A (file opened in function, GUI objects within outer scope)
    :return: N/A (objects added to respective lists in outer scope)
    """
    with open("penalty.txt") as penFile:
        readPen = penFile.readline()
        while readPen != '':
            readPen = readPen.replace("\n","")
            pen_lbox.insert(END, readPen)
            penParse = readPen.split(",")
            penParse[1] = penParse[1].replace(" ","")
            readPen = penParse[0] + "," + penParse[1]
            #print(readPen)
            pref_penalty.append(readPen)
            readPen = penFile.readline()
    #print(pref_penalty)

def updatePossible():
    """
    Opens possible.txt and makes them into possibilistic preference objects that are used later.
    :param: N/A (file opened in function, GUI objects within outer scope)
    :return: N/A (objects added to respective lists in outer scope)
    """
    with open("possible.txt") as possFile:
        readPoss = possFile.readline()
        while readPoss != '':
            readPoss = readPoss.replace("\n","")
            poss_lbox.insert(END, readPoss)
            possParse = readPoss.split(",")
            possParse[1] = possParse[1].replace(" ","")
            readPoss = possParse[0] + "," + possParse[1]
            #print(readPoss)
            pref_possible.append(readPoss)
            readPoss = possFile.readline()
    #print(pref_possible)

def updateQuality():
    """
    Opens qualitative.txt and makes them into qualitative choice preference objects that are used later.
    :param: N/A (file opened in function, GUI objects within outer scope)
    :return: N/A (objects added to respective lists in outer scope)
    """
    with open("qualitative.txt") as qualFile:
        readQual = qualFile.readline()
        while readQual != '':
            readQual = readQual.replace("\n","")
            qual_lbox.insert(END, readQual)
            pref_qualitative.append(readQual)
            readQual = qualFile.readline()
    #print(pref_qualitative)

def updateFeasObj():
    """
    Makes a list of feasible objects from all of the current attributes and hard constraints given, adding
    them to the GUI.
    :param: N/A (GUI within outer scope, constraints and attributes within outer scrope)
    :return: N/A (objects added to respective list in outer scope)
    """
    if len(attrOptions) != 0:
        feasibleObjects.clear()
        feasObj_lbox.delete(0, END)
        cnf = middleMan()
        cnfDictionaries = cnf.updateDictionary(attrOptions) #[0] is passed to objects, [1] is reversed for outputs
        cnfReverse = cnfDictionaries[1]
        cnfConstraints = cnf.cnfConstraints(hardConstraints, cnfDictionaries[0])
        logic = brain()
        feasObj = logic.createFeasibleObjects(cnfConstraints)
        feasibleObjects.append(feasObj)
        objects = revertClasp(cnfReverse, feasibleObjects[0])
        for obj in objects:
            feasObj_lbox.insert(END, obj)
    else:
        messagebox.showinfo("Error: No Binary Attributes", "Please make sure you've added binary attributes.")
    
def revertClasp(cnfReverse, feasibleObjectList):
    """
    Takes an object generated in clasp and returns it back in the form of words.
    :param cnfReverse: a reversed dictionary of the current attribute options in clasp form (key="number", value="option")
    :param feasibleObjectList: a list of objects in clasp form
    :return: list of the objects in word form
    """
    revertedObj = []
    for obj in feasibleObjectList:
        output = ""
        items = obj.split()
        for item in items:
            output = output + " " + str(cnfReverse[int(item)])
        output = output[1:]
        revertedObj.append(output)
    return revertedObj
"""END UPDATE WITH FILE INFO"""

"""RESET METHOD"""
def reset():
    """
    Resets all of the relevant lists in the outer scope as well as clears the
    respective listboxes.
    :param: N/A (lists and GUI in outer scope)
    :return: N/A
    """
    BA_Options.clear() #for error checking if the option name already exists
    attrOptions.clear() #list of options for each attribute seperated by a comma
    hardConstraints.clear() #list of hard constraints (string)
    pref_penalty.clear() #list of penalty logic
    pref_possible.clear() #list of possiblistic logic
    pref_qualitative.clear() #list of qualitative logic
    feasibleObjects.clear() #list of feasible objects
    binAtr_lbox.delete(0,END)
    hardConstr_lbox.delete(0,END)
    pen_lbox.delete(0,END)
    poss_lbox.delete(0,END)
    qual_lbox.delete(0,END)
    feasObj_lbox.delete(0,END)

"""END RESET METHOD"""

"""END METHOD DEFINITIONS"""

#top frame to help align with preferences row
top = Frame(root)
top.grid(row=0, column=0) 

"""START BINARY ATTRIBUTES"""
#binary attribute frames
binAtr_frame = tk.LabelFrame(top, text="Binary Attributes", padx=10, pady=10)
binAtr_frame2 = tk.Frame(binAtr_frame)
binAtr_frame.grid(row=0, column=0, padx=10)
binAtr_frame2.grid(row=0, column=2, sticky='ns')

#binary attribute frame 1
binAtr_lbox = tk.Listbox(binAtr_frame, width=40)
binAtr_lbox.grid(row=0,column=0)
binAtr_scroll = Scrollbar(binAtr_frame, orient='vertical', command=binAtr_lbox.yview)
binAtr_scroll.grid(row=0, column=1, sticky='ns')
binAtr_lbox['yscrollcommand'] = binAtr_scroll.set

#binary attribute frame 2
binAtr_lb_attr = tk.Label(binAtr_frame2, text = "Attribute")
binAtr_lb_op1 = tk.Label(binAtr_frame2, text = "Option 1")
binAtr_lb_op2 = tk.Label(binAtr_frame2, text = "Option 2")
binAtr_entr_attr = tk.Entry(binAtr_frame2)
binAtr_entr_op1 = tk.Entry(binAtr_frame2)
binAtr_entr_op2 = tk.Entry(binAtr_frame2)

binAtr_addButton = tk.Button(binAtr_frame2, text="Add Attribute", command=binAtr_add)
binAtr_updateFileButton = tk.Button(binAtr_frame2, text="Update with File Info", command=updateAttr)

#binary attribute frame 2 (placements)
binAtr_lb_attr.grid(row=0,column=0)
binAtr_entr_attr.grid(row=1, column=0)
binAtr_lb_op1.grid(row=2, column=0)
binAtr_entr_op1.grid(row=3,column=0)
binAtr_lb_op2.grid(row=2, column=2)
binAtr_entr_op2.grid(row=3,column=2)
binAtr_addButton.grid(row=4, column=0)
binAtr_updateFileButton.grid(row=5, column=0)
"""END binary Attributes"""

"""HARD CONSTRAITS"""
#hard constraints frames
hardConstr_frame = tk.LabelFrame(top, text="Hard Constraints", padx=10, pady=10)
hardConstr_frame2 = tk.Frame(hardConstr_frame)
hardConstr_frame.grid(row=0, column=1, padx=10)
hardConstr_frame2.grid(row=0, column=2, sticky='ns')

#frame1
hardConstr_lbox = tk.Listbox(hardConstr_frame, width=40)
hardConstr_lbox.grid(row=0, column=0)
hardConstr_scroll = Scrollbar(hardConstr_frame, orient='vertical', command=hardConstr_lbox.yview)
hardConstr_scroll.grid(row=0, column=1, sticky='ns')
hardConstr_lbox['yscrollcommand'] = hardConstr_scroll.set

#frame2
hardConstr_lb_constr = tk.Label(hardConstr_frame2, text="Constraint")
hardConstr_entr_constr = tk.Entry(hardConstr_frame2)

#buttons
hardConstr_addButton = tk.Button(hardConstr_frame2, text="Add Constraint", command=hardConstr_add)
hardConstr_fileButton = tk.Button(hardConstr_frame2, text="Update with File Info", command=updateHardConstr)

#frame2 fill
hardConstr_lb_constr.grid(row=0, column=0)
hardConstr_entr_constr.grid(row=1, column=0)
hardConstr_addButton.grid(row=2, column=0)
hardConstr_fileButton.grid(row=3, column=0)
"""END HARD CONSTRAINTS"""

"""FEASIBLE OBJECTS"""
feasObj_frame = LabelFrame(top, text="Feasible Objects", padx=10, pady=10)
feasObj_frame.grid(row=0, column=3)

feasObj_lbox = Listbox(feasObj_frame, width=40)
feasObj_lbox.grid(row=0, column=0)
feasObj_scrollV = Scrollbar(feasObj_frame, orient='vertical', command=feasObj_lbox.yview)
feasObj_scrollV.grid(row=0, column=1, sticky='ns')
feasObj_lbox['yscrollcommand'] = feasObj_scrollV.set
feasObj_scrollH = Scrollbar(feasObj_frame, orient='horizontal', command=feasObj_lbox.xview)
feasObj_scrollH.grid(row=1, column=0, sticky='ew')
feasObj_lbox['xscrollcommand'] = feasObj_scrollH.set


feasObj_updateButton = Button(feasObj_frame, text="Update", command=updateFeasObj)
feasObj_updateButton.grid(row=0,column=2)
"""END FEASIBLE OBJECTS"""

"""PREFERENCES"""
pref_frame = LabelFrame(root, text="Preferences", bd='5', pady=5)
pref_frame.grid(row=1, column=0)

"""PENALTY (PREFERENCE 1)"""
#penalty frames
pen_frame = LabelFrame(pref_frame, text="Penalty Logic", padx=10, pady=10)
pen_frame2 = Frame(pen_frame)
pen_frame.grid(row=0, column=0, padx=10)
pen_frame2.grid(row=0, column=2,sticky='ns')

#penalty frame1
pen_lbox = Listbox(pen_frame, width=40)
pen_lbox.grid(row=0, column=0)
pen_scroll = Scrollbar(pen_frame, orient='vertical', command=pen_lbox.yview)
pen_scroll.grid(row=0, column=1, sticky='ns')
pen_lbox['yscrollcommand'] = pen_scroll.set

#penalty frame2
pen_lb_pref = Label(pen_frame2, text="Preference")
pen_lb_val = Label(pen_frame2, text="Value")
pen_entr_pref = Entry(pen_frame2)
pen_entr_val = Entry(pen_frame2)
pen_addButton = Button(pen_frame2, text="Add Preference", command=pen_add)
pen_fileButton = Button(pen_frame2, text="Update with File Info", command=updatePenalty)

#penalty frame2 placements
pen_lb_pref.grid(row=0, column=0)
pen_entr_pref.grid(row=1, column=0)
pen_lb_val.grid(row=0, column=1)
pen_entr_val.grid(row=1, column=1)
pen_addButton.grid(row=2, column=0)
pen_fileButton.grid(row=3, column=0)
"""END PENALTY (PREFERENCE 1)"""

"""POSSIBILISTIC (PREFERENCE 2)"""
#possibilistic frames
poss_frame = LabelFrame(pref_frame, text="Possibilistic Logic", padx=10, pady=10)
poss_frame2 = Frame(poss_frame)
poss_frame.grid(row=0, column=1, padx=10)
poss_frame2.grid(row=0, column=2,sticky='ns')

#possibilistic frame1
poss_lbox = Listbox(poss_frame, width=40)
poss_lbox.grid(row=0, column=0)
poss_scroll = Scrollbar(poss_frame, orient='vertical', command=poss_lbox.yview)
poss_scroll.grid(row=0, column=1, sticky='ns')
poss_lbox['yscrollcommand'] = poss_scroll.set

#possibilistic frame2
poss_lb_pref = Label(poss_frame2, text="Preference")
poss_lb_val = Label(poss_frame2, text="Value")
poss_entr_pref = Entry(poss_frame2)
poss_entr_val = Entry(poss_frame2)
poss_addButton = Button(poss_frame2, text="Add Preference", command=poss_add)
poss_fileButton = Button(poss_frame2, text="Update with File Info", command=updatePossible)

#possibilistic placements
poss_lb_pref.grid(row=0, column=0)
poss_entr_pref.grid(row=1, column=0)
poss_lb_val.grid(row=0, column=1)
poss_entr_val.grid(row=1, column=1)
poss_addButton.grid(row=2, column=0)
poss_fileButton.grid(row=3, column=0)
"""END POSSIBILISTIC (PREFERENCE 2)"""

"""QUALITATIVE (PREFERENCE 3)"""
#qualitative frames
qual_frame = LabelFrame(pref_frame, text="Qualitative Choice Logic", padx=10, pady=10)
qual_frame2 = Frame(qual_frame)
qual_frame.grid(row=0, column=2, padx=10)
qual_frame2.grid(row=0, column=2,sticky='ns')

#qualitiative frame1
qual_lbox = Listbox(qual_frame, width=40)
qual_lbox.grid(row=0, column=0)
qual_scroll = Scrollbar(qual_frame, orient='vertical', command=qual_lbox.yview)
qual_scroll.grid(row=0, column=1, sticky='ns')
qual_lbox['yscrollcommand'] = qual_scroll.set

#qualitiative frame2
qual_lb_pref = Label(qual_frame2, text="Preference")
qual_entr_pref = Entry(qual_frame2)
qual_addButton = Button(qual_frame2, text="Add Preference", command=qual_add)
qual_fileButton = Button(qual_frame2, text="Update with File Info", command=updateQuality)

#qualitative frame2 placements
qual_lb_pref.grid(row=0, column=0)
qual_entr_pref.grid(row=1, column=0)
qual_addButton.grid(row=2, column=0)
qual_fileButton.grid(row=3, column=0)
"""END QUALITATIVE (PREFERENCE 3)"""

"""END PREFERENCE"""

"""TASK BUTTONS"""
#buttons for the other tasks
taskFrame = Frame(root)
taskFrame.grid(row=2, column=0)

b_exemplify = Button(taskFrame, text="Exemplify",command=exemplify)
b_optimize = Button(taskFrame, text="Optimize", command=optimize)
b_omni = Button(taskFrame, text="Omni-Optimize", command=omni)

b_exemplify.grid(row=0, column=0)
b_optimize.grid(row=0, column=1)
b_omni.grid(row=0, column=2)

#exit and reset
exitFrame = Frame(root)
exitFrame.grid(row=3, column=0)

b_quit = Button(exitFrame, text="Quit", command=root.destroy)
b_reset = Button(exitFrame, text="Reset", command=reset)
b_reset.grid(row=0,column=0)
b_quit.grid(row=0,column=1)

"""END TASK BUTTONS"""

root.mainloop()
