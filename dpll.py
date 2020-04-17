# BACKTRACKING DPLL Algorithm

'''
DPLL ALGORITHM OVERVIEW
Input: As set of clauses A
Output: A truth value 

If A is a consistent set of literals then return true

if A contains an empty clause then return false

for every unit clause L in A: 
    A <- unit-propagate(L, A)

for every literal L that is pure in A:
    A <- pure-literal-assign(L, A)

L <- Choose-literal(A)

return DPLL(A and L  ) or DPLL (A and not L )

'''
def DPLL(VARS, instance, assignment):

    if len(VARS) == 0: 
        return instance

    instance = propagate_units(instance)
    instance = pure_elim(instance)

    # CASE: instance contains empty clause which results in "UNSAT"
    if [] in instance: 
        return []

    # Check if assigning everything to true works 
    if checkAllTrue(instance) == True:
        return instance

    # Deepcopy is used so we can backtrack and preserve our previous assignments and not overwrite them
    assignment = copy.deepcopy(assignment)

   # Choose next lteral to assign value in model
    nxtLit = choose_next_lit(instance)
    assignment.append(nxtLit)

    #Check is we reached valid assignment
    if checkValidAssignment(VARS, assignment) == True:
        return instance

    # Deepcopy to prevent state overwrite while backtracking
    # CC is copy of instance -> (set of all our clauses)
    cc1 = copy.deepcopy(instance)
    cc1.append([nxtLit])
    cc2 = copy.deepcopy(instance)

    # Recursively do backtrack and add new literal to assignment
    try:
        # Try finding sol using '+' X where x is next lit assigned 
        sol = DPLL(VARS, cc1, assignment)
        if sol != []:
            return sol
        else:
            # If sol wasn't found try finding sol using '-' X 
            cc2.append([-nxtLit])
            return DPLL(VARS, cc2, assignment)
    except:
        print("If you reached here you fucked up ")

def checkAllTrue(instance):
    # Check if all vars can be assigned true
    v = set()
    for clause in instance:
        for literal in clause:
            v.add(literal)
            if -literal in v:
                return False
    return True
 
def checkValidAssignment(VARS, assignment):
    # check if # Vars = # Assignment -> we found valid sol and ret assignment
    if assignment == VARS:
        # print("SUCCESS: Valid Assignment Found!")
        return True
    else:
        # temp = VARS
        # for x in VARS:
        #     if x in assignment:
        #         temp.remove(x)
        # print("VARS: ", VARS)
        # print("Assignment: ",assignment)
        # print("Assignment Err: ",temp )
        return False


def solve_dpll(instance, verbosity):
    # print(instance)
    # instance.VARS goes 1 to N in a dict
    # print(instance.VARS)
    # print(verbosity)
    
    clauses = instance.clauses
    variables = instance.VARS

    sol = DPLL(variables, clauses, [])
    # Pos/ Neg Literals stored in sets to preserve uniqueness
    posVar, negVar = set(), set()
   
    # If our sol contains empty clause -> UNSAT 
    if sol == []:
        print("UNSAT")
        return False
    else:  
        print("SAT")
        # Check if user wants Pos and Neg Vars
        if verbosity == True:
            for clause in sol:
                for literal in clause:
                    # Add Pos and Neg Literals to set
                    if literal > 0:
                        posVar.add(literal)
                    if literal < 0:
                        negVar.add(literal)
       
            # Format set(posVar) into list(posVar) for correctness & sort by ascending literals
            posVar = list(posVar)
            posVar.sort()
            print(posVar)

            # ~~~~~ DEBUG ~~~~~
            # negVar = list(negVar)
            # negVar.sort(reverse=True)  
            # print(negVar)

    return True

# Get next literal to assign based on the # of occurances in list of clauses 
def choose_next_lit(instance):
    # Store Key: Val pairs of {Literal: Weight}
    weight = dict()
    maxWeight = 0
   
    nxtLitDebug = False
    maxRecurDepth = 1000
    if nxtLitDebug == True:
        if nxtLitTest(instance, maxRecurDepth) == False:
            print("ERROR: EXCEEDED EXPECTED RECURSIVE DEPTH! EXITING PROGRAM...") 
            sys.exit()
        
    
    for clauses in instance:
        #  print("Itr Clauses in Instances: ", len(instance))
        for literal in clauses:
            # print("Itr Literals in Clauses: ", len(clauses))
            # Assign Weight Value corresponding to literal appearance in instance
            if literal not in weight:
                weight[literal] = 1
                # print("Adding Lit: ", literal)
            
            if literal in weight: 
                weight[literal] += 1
                # print("Inc W: ", literal,' ', weight[literal])

                # Check for new max  
                if weight[literal] > maxWeight:
                    maxWeight = weight[literal]
                    next_lit = literal
    return next_lit

# Just for testing test_sat.cnf 
def nxtLitTest(instance, maxRecurDepth):
    if len(instance) > maxRecurDepth:
        return False 
    else:
        return True

#Handles Unit Clauses 
def propagate_units(instance):
    # Search through instance and look for unit clause candidates
    # 1) Add all unit clauses to a list 
    # 2) Itr over list and remove non UC 
    #       -> If UC appears in non UC
    #       -> If '+' UC and '-' UC both are UC's 
    # Cuses cascade effect similar to forward chaining 
    
    unitClauses = []
    # Add all unit clause candidates to list 'unitClauses'
    for clause in instance:
        if len(clause) == 1:
            # Check not in UC already and clause is not empty
            if clause[0] not in unitClauses and clause[0] != 0:
                unitClauses.append(clause[0])

    # Iterate through list of candidates and filter any that appear in other clauses
    while unitClauses != []:
        # Gets first candidate UC 
        unit = unitClauses.pop()
        for clause in instance:
            # CASE: +UC in clause, clause is satisfiable -> remove clause
            if unit in clause and len(clause) > 1:
                instance.remove(clause)

            # CASE: -UC in clause , remove negation of unit from clause 
            if -unit in clause:
                clause.remove(-unit)
                # If clause - unit = length 1, and clause is not in UC -> add lit to UC 
                if len(clause) ==1 and clause[0] not in unitClauses:
                    unitClauses.append(clause[0])
    return instance

# Handles Pures
def pure_elim(instance):
# Search through instance and get all Pures (literals appearing with same sign in all clauses )

    pures = []
    # Get list of Pures
    pures = getPure(instance)
    # Iterate over pures and remove all clauses containing pures
    while len(pures) != 0:
        p = pures.pop()
        temp = []
        # Put all clauses containing a pure literal into temp
        for clause in instance:
            if p in clause:
                temp.append(clause)

        # Iterate over temp and remove clauses from instance
        for clause in temp:
            for lit in clause:
                if lit in pures:
                    pures.remove(lit)
            # Remove Clauses w/ Pures 
            instance.remove(clause)
        # AddPure P to list of clauses -> new unit clause [P]
        instance.append([p])
    return instance

# Gets all Pure Literals
def getPure(instance):
    pcand, pures= set(), set()

    # Add pure candidates to pcand
    for clause in instance:
        for literal in clause:
            if literal not in pcand:
                pcand.add(literal)

    # Check lits in pcadn and ensure they are pure (if 'x' then '-x' not in list, vise versa)
    for lit in pcand:
        if lit not in pures and -lit not in pcand:
            pures.add(lit)
    
    return pures
