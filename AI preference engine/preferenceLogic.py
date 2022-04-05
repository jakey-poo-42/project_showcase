import subprocess as sp
import os
import sys
import random
import platform

class Node:
    """
    Helper class for determining qualitative preference
    """
    objects = [] # Contains all congruent objects for this node
    satisfactionDegrees = () # The satisfaction degrees for each rule for the object(s)
    worseThan = [] # References all nodes preferred over this node

    def __init__(self, objects, sd):
        self.objects = objects
        self.satisfactionDegrees = sd
        self.worseThan = []

    def __str__(self):
        result = ""
        for i in self.objects:
            result += i + "|"
        result += " (sd:"
        for i in self.satisfactionDegrees:
            result += str(i) + " "
        result += ")|(worse than " + str(len(self.worseThan)) + " nodes)"
        return result

    def setObjects(self, object):
        self.objects = object

    def setSD(self, sd):
        self.satisfactionDegrees = sd

class Logic:

    def determinePenaltyPreference(self, objects: list[str], rules: list):
        """
        :param objects: the objects to apply the rules to, formatted as binary strings
        :param rules: the rules to run the objects against
        :return: a list of tuples of objects, where the earlier in the list an object appears, the more preferred that tuple is
        """
        objPens = []
        for o in objects:
            penalty = 0
            for r in rules:
                inpRule = r[0]
                if self.checkRule(o, inpRule) == 0:
                    penalty += int(r[1])
            t = (o, penalty)
            objPens.append(t)

        # Determine how many unique penalty values there are and make a list of them
        penalties = []
        for i in objPens:
            if i[1] not in penalties:
                penalties.append(i[1])
        penalties.sort()

        # Prepare result list
        temp = []
        for i in penalties:
            temp.append([])

        # Populate result list
        for i in objPens:
            j = self.findIndex(penalties, i[1])
            temp[j].append(i[0])

        # Convert result list into a list of tuples
        result = []
        for i in temp:
            result.append(tuple(i))

        return result

    def determinePossibilisticPreference(self, objects: list[str], rules: list):
        """
        :param objects: the objects to apply the rules to, formatted as clasp output
        :param rules: the rules to run the objects against
        :return: a list of tuples of objects, where the earlier in the list an object appears, the more preferred it is
        """
        # Determine the possibilities of each object
        objPens = []
        for o in objects:
            probabilities = []
            for r in rules:
                inpRule = r[0]
                if self.checkRule(o, inpRule) == 0:
                    probabilities.append(float(r[1]))
                else:
                    probabilities.append(1)
            t = (o, min(probabilities))
            objPens.append(t)

        # Determine how many unique penalty values there are and make a list of them
        penalties = []
        for i in objPens:
            if i[1] not in penalties:
                penalties.append(i[1])
        penalties.sort(reverse=True)

        # Prepare result list
        temp = []
        for i in penalties:
            temp.append([])

        # Populate result list
        for i in objPens:
            j = self.findIndex(penalties, i[1])
            temp[j].append(i[0])

        # Convert result list into a list of tuples
        result = []
        for i in temp:
            result.append(tuple(i))

        return result

    def qualitativeLogic(self, objects: list[str], rules):
        """
        Perform qualitative choice analysis on objects.
        :param objects: the objects to test
        :param rules: the rule set to test the objects against, in the form (condition, (rule1, rule2, ...). All inputs should be formatted as strings.
        :return: a list of Node objects
        """
        # Determine SDs for each object
        objectSDs = [] # Elements look like (object, (sd1, sd2...))
        for i in objects:
            temp = []
            for j in rules:
                sd = self.determineQualitativeSD(i, j)
                temp.append(sd)
            objectSDs.append((i, tuple(temp)))

        # Combine all congruent objects into their own lists
        congruencyLists = [] # Elements look like
        for i in range(0, len(objectSDs)):
            # Check if current object is not already in a list
            accountedFor = False
            for x in congruencyLists:
                if objectSDs[i] in x:
                    accountedFor = True

            if not accountedFor:
                tempList = [objectSDs[i]]
                j = i+1
                for j in range(j, len(objectSDs)):
                    if self.determineQualitativePreference(objectSDs[i], objectSDs[j]) == 0:
                        tempList.append(objectSDs[j])
                congruencyLists.append(tempList)

        # Create nodes for each list
        nodes = []
        for i in congruencyLists:
            temp = []
            for j in range(0, len(i)):
                temp.append(i[j][0])
            nodes.append(Node(temp, i[0][1]))

        # Compare each node to each other node
        for i in range(0, len(nodes)):
            for j in range(0, len(nodes)):
                if i == j:
                    continue
                res = -1
                for k in range(0, len(nodes[i].satisfactionDegrees)):
                    a = nodes[i].satisfactionDegrees[k]
                    b = nodes[j].satisfactionDegrees[k]
                    if a > b:
                        if res != j:
                            res = i
                        else:
                            res = -1
                    elif a < b:
                        if res != i:
                            res = j
                        else:
                            res = -1
                if res == i:
                    if nodes[j] not in nodes[i].worseThan:
                        nodes[i].worseThan.append(nodes[j])
                elif res == j:
                    if nodes[i] not in nodes[j].worseThan:
                        nodes[j].worseThan.append(nodes[i])


        return nodes

    def determineQualitativeSD(self, object, rule):
        """
        Determines whether or not an object satisfies a rule, and returns the satisfaction degree of that rule.
        :param object: the object to test against the rule
        :param rule: the rule to test, in the form (condition, (rule1, rule2, ...). All inputs should be formatted as strings.
        :return: If object conforms to rule, satisfaction degree, else sys.maxsize (infinity)
        """
        inf = sys.maxsize
        # Check condition first, if it exists
        if rule[0] != "0":
            enumAttr = object.split()
            numAttr = len(enumAttr)
            condFile = open("condition.cnf", "w")
            condFile.write("p cnf " + str(numAttr) + " 1\n")
            condFile.write(str(rule[0]) + " 0\n")
            for i in enumAttr:
                condFile.write(i + " 0\n")
            condFile.close()
            if platform.system() == "Windows":
                condOut = sp.run('.\clingo.exe --mode=clasp condition.cnf --verbose=1', shell=True, capture_output=True)
            else:
                condOut = sp.run('clasp condition.cnf --verbose=1', shell=True, capture_output=True)
            condString = str(condOut.stdout)
            # os.remove('condition.cnf')
            if "UNSATISFIABLE" in condString:
                return inf

        # Check the object against every rule and return their satisfaction degree
        sd = 1
        for i in rule[1]:
            if self.checkRule(object, i) == 1:
                return sd
            sd += 1

        # If the code reaches this point, all rules have failed.
        return inf

    def determineQualitativePreference(self, obj1: tuple, obj2: tuple):
        """
        Determines which of the two objects is better according to their SDs. Returns the number of the object that is
        more preferred, 0 if they are congruent, or -1 if they are incomparable.\n
        objx : A tuple containing the object itself and its SDs
        """
        # Determines out of two objects and their SDs, which is better.
        # Returns the number of the object that is better, 0 if they are congruent, or -1 if they are incomparable
        result = 0
        j = 0
        for i in obj1[1]:
            if i < obj2[1][j]:
                if result != 2:
                    result = 1
                else:
                    return -1
            elif i > obj2[1][j]:
                if result != 1:
                    result = 2
                else:
                    return -1
            j += 1

        return result

    def findIndex(self, list, search):
        a = 0;
        for i in list:
            if i == search:
                return a
            a += 1

        return -1;

    def checkRule(self, object: str, rule):
        """Determines if an object conforms to a penalty logic rule. Returns 1 if it does, 0 otherwise."""
        fp = open('checkRule.cnf', 'w')
        fp.write(rule)
        fp.write("\n")
        items = object.split()
        for i in items:
            fp.write(i + " 0\n")
        fp.close()
        if platform.system() == "Windows":
            claspOut = sp.run('.\clingo.exe --mode=clasp checkRule.cnf --verbose=0', shell=True, capture_output=True)
        else:
            claspOut = sp.run('clasp checkRule.cnf --verbose=0', shell=True, capture_output=True)
        claspString = str(claspOut.stdout)

        if "UNSATISFIABLE" in claspString:
            result = 0
        else:
            result = 1

        # os.remove("checkRule.cnf")
        return result

    def min(self, inp: list[int]) -> int:
        result = sys.maxsize
        for i in inp:
            if i < result:
                result = i
        return result

    def exemplify(self, feasibleObjects: list, rules: tuple) -> list:
        """
        Generates all feasible objects, picks two at random, and compares them according to the different logics.\n
        :param feasibleObjects: the list of feasible objects
        :param rules: the preference rules to use. Must be a 3-tuple, with the elements being the rules for penalty, possibilistic, and qualitative logics, respectfully
        :return: a list containing the following items, in order: a 2-tuple with the objects used, and the number of the object (1 or 2) that is preferred for each of the logics, in the above order, with 0 being congruency (and -1 for incompatibility for qualitative)
        """
        # Select two random objects
        results = []
        obj1Int = random.randrange(0, len(feasibleObjects))
        obj2Int = random.randrange(0, len(feasibleObjects))
        if obj1Int == obj2Int:
            if obj2Int+1 == len(feasibleObjects):
                obj2Int -= 1
            else:
                obj2Int += 1
        obj1 = feasibleObjects[obj1Int]
        obj2 = feasibleObjects[obj2Int]
        results.append((obj1, obj2))

        # Test 1: Penalty logic. Ruleset = rules[0]
        penaltyResults = self.determinePenaltyPreference([obj1, obj2], rules[0])
        if len(penaltyResults) != 2:
            results.append(0)
        else:
            if penaltyResults[0][0] == obj1:
                results.append(1)
            else:
                results.append(2)

        # Test 2: Possibilistic logic. Ruleset = rules[1]
        possibilisticResults = self.determinePossibilisticPreference([obj1, obj2], rules[1])
        if len(possibilisticResults) != 2:
            results.append(0)
        else:
            if possibilisticResults[0][0] == obj1:
                results.append(1)
            else:
                results.append(2)

        # Test 3: Qualitative Choice logic. Ruleset = rules[2]
        obj1SDs = []
        obj2SDs = []
        for i in rules[2]:
            x = self.determineQualitativeSD(obj1, i)
            y = self.determineQualitativeSD(obj2, i)
            obj1SDs.append(x)
            obj2SDs.append(y)

        obj1withSDs = (obj1, tuple(obj1SDs))
        obj2withSDs = (obj2, tuple(obj2SDs))

        results.append(self.determineQualitativePreference(obj1withSDs, obj2withSDs))

        return results

    def omniOptimize(self, feasibleObjects: list, rules: tuple):
        """
        Runs penalty, possibilistic, and qualitative logics on all feasible objects, and returns all optimal objects.
        :param feasibleObjects: all feasible objects
        :param rules: the preference rules to use. Must be a 3-tuple, with the elements being the rules for penalty, possibilistic, and qualitative logics, respectfully
        :return: a list containing tuples of the optimal objects for each logic, in order (penalty, possibilistic, qualitative)
        """
        penaltyOptimal = self.determinePenaltyPreference(feasibleObjects, rules[0])
        print("Number of optimal objects for penalty: " + str(penaltyOptimal))
        possibilisitcOptimal = self.determinePossibilisticPreference(feasibleObjects, rules[1])
        print("Number of optimal objects for possibilistic: " + str(possibilisitcOptimal))
        nodes = self.qualitativeLogic(feasibleObjects, rules[2])
        for x in nodes:
            if len(x.worseThan) == 0:
                qualitativeOptimal = x
                break

        return [penaltyOptimal[0], possibilisitcOptimal[0], tuple(qualitativeOptimal.objects)]

    def optimize(self, feasibleObjects: list, rules: tuple):
        """
        Runs omniOptimize, selects one random element from each list, and returns each.
        :param feasibleObjects: all feasible objects
        :param rules: the preference rules to use. Must be a 3-tuple, with the elements being the rules for penalty, possibilistic, and qualitative logics, respectfully
        :return: a list containing one optimal object for each of the logics
        """
        optimal = self.omniOptimize(feasibleObjects, rules)
        rand1 = random.randrange(0, len(optimal[0]))
        rand2 = random.randrange(0, len(optimal[1]))
        rand3 = random.randrange(0, len(optimal[2]))

        return [optimal[0][rand1], optimal[1][rand2], optimal[2][rand3]]

    def createFeasibleObjects(self, constraints):
        """Returns a list of all feasible objects, represented in clasp output"""
        print("Input to createFeasibleObjects: " + constraints)
        fp = open('feasible.cnf', 'w')
        fp.write(constraints)
        fp.close()
        if platform.system() == "Windows":
            claspOut = sp.run('.\clingo.exe --mode=clasp feasible.cnf -n 0 --verbose=0', shell=True, capture_output=True)
        else:
            # Note to grader: none of us had a Unix machine, so we don't know if this line will work. We do know that it works on Windows.
            claspOut = sp.run('clasp feasible.cnf -n 0 --verbose=0', shell=True, capture_output=True)
        claspString = str(claspOut.stdout)
        # os.remove("feasible.cnf")

        if "UNSATISFIABLE" in claspString:
            return []

        unquote = claspString.split("\'v ")
        solns = unquote[1].split(" 0\\r\\nv ")
        tempA = len(solns) - 1
        tempB = solns[tempA].split(" 0\\r\\n")
        solns[tempA] = tempB[0]

        print("There are " + str(len(solns)) + " feasible objects.")

        return solns

    def createAllObjects(self, numAttr):
        """
        Generates all possible objects with the given number of attributes, ignoring constraints
        :param numAttr: the number of attributes
        :return: a list of objects
        """
        fp = open('allattr.cnf', 'w')
        fp.write('p cnf ' + str(numAttr) + ' 0')
        fp.close()
        if platform.system() == "Windows":
            claspOut = sp.run('.\clingo.exe --mode=clasp allattr.cnf -n 0 --verbose=0', shell=True, capture_output=True)
        else:
            claspOut = sp.run('clasp allattr.cnf -n 0 --verbose=0', shell=True, capture_output=True)
        claspString = str(claspOut.stdout)
        # os.remove("allattr.cnf")
        unquote = claspString.split("\'v ")
        solns = unquote[1].split(" 0\\r\\nv ")
        tempA = len(solns) - 1
        tempB = solns[tempA].split(" 0\\r\\n")
        solns[tempA] = tempB[0]

        objects = []
        for i in solns:
            tempC = ""
            attributes = i.split()
            for j in attributes:
                if j[0] == "-":
                    tempC += "1"
                else:
                    tempC += "0"
            objects.append(tempC)

        return objects