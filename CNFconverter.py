import sys
import copy
import os.path

""" CONVERT TO CNF """
def convert_CNF(sentence):
    components=eval(sentence)    #convert string to list
    bidirectional_elimination(components)
    implication_elimination(components)
    demorgans(components)
    distributivity(components)  
    flag=1
    while(components[0]=="or" and flag==1):
        if (len(components[2])>1  and components[2][0]=="and"):
            distributivity_recursion(components)
            flag=1
        elif (len(components[1])>1  and components[1][0]=="and"):
            distributivity_recursion(components)
            flag=1
        else:
            flag=0

    associvity(components)
    remove_parens(components)
    remove_duplicates(components)
    remove_single_literals(components)
    quality_check(components)
    remove_parens(components)

    check=1
    if(components[0]=="and"):
       temp_literal=components[1]
       for x in range(1,len(components)):
           if temp_literal != components[x]:
               check=0

    if check==1:
        remove_duplicates(components)
        remove_single_literals(components)
        quality_check(components)
        remove_parens(components)
    return components

""" BIDIRECTIONAL ELIMINATION"""
def bidirectional_elimination(components): 
    if(components[0]=="iff"):
        literal_1=components[1]
        literal_2=components[2]
        components[0]="and"
        components[1]=["implies",literal_1,literal_2]
        components[2]=["implies",literal_2,literal_1]

    for literal in components:
        if(len(literal)>1):
            bidirectional_elimination(literal)

""" IMPLICATION ELIMINATION"""
def implication_elimination(components):  
    if(components[0]=="implies"):
        literal_1=components[1]
        components[0]="or"
        components[1]=["not",literal_1]

    for literal in components:
        if(len(literal)>1):
            implication_elimination(literal)
 
""" DE-MORGAN'S LAW """
def demorgans(components): 
    if(components[0]=="not"):
        literal=components[1]

        if(literal[0]=="not"):
            del components[:]
            if(len(literal[1])==1):
                components.append(literal[1])
            else:
                for literal_1 in literal[1]:
                    components.append(literal_1)

                if(len(components)>1):
                    demorgans(components)

        elif(literal[0]=="or"):
            del components[:]
            components.append("and")
            for literal_1 in literal:
                if literal_1== "or":
                    continue
                else:
                    components.append(["not",literal_1])

        elif(literal[0]=="and"):
            del components[:]
            components.append("or")
            for literal_1 in literal:
                if literal_1== "and":
                    continue
                else:
                    components.append(["not",literal_1])
        
       

    for literal in components:
        if(len(literal)>1 ):
            demorgans(literal)

""" DISTRIBUTIVE LAW """
def distributivity(components):
    if(components[0]=="or"):
        if(len(components[2])>1  and components[2][0]=="and"):
            literal_1=components[1]
            literal_2=components[2]
            del components[:]
            components.append("and")
            for literal_x in literal_2:
                if literal_x=="and":
                    continue
                components.append(["or",literal_1,literal_x])
        elif(len(components[1])>1  and components[1][0]=="and"):
            literal_1=components[1]
            literal_2=components[2]
            del components[:]
            components.append("and")
            for literal_x in literal_1:
                if literal_x=="and":
                    continue
                components.append(["or",literal_x,literal_2])

    for literal in components:
        if(len(literal)>1 ):
            distributivity(literal)

""" OUTER RECURSIVE DISTRIBUTIVE LAW"""
def distributivity_recursion(components):
    if(components[0]=="or"):
        if(len(components[2])>1  and components[2][0]=="and"):
            literal_1=components[1]
            literal_2=components[2]
            del components[:]
            components.append("and")
            for literal_x in literal_2:
                if literal_x=="and":
                    continue
                components.append(["or",literal_1,literal_x])
        elif(len(components[1])>1  and components[1][0]=="and"):
            literal_1=components[1]
            literal_2=components[2]
            del components[:]
            components.append("and")
            for literal_x in literal_1:
                if literal_x=="and":
                    continue
                components.append(["or",literal_x,literal_2])

""" ASSOCIATIVE LAW """
def associvity(components):
    if(components[0]=="and"):
        temp_components=copy.deepcopy(components)
        del components[:]
        for literal in temp_components:
            if literal=="and":
                components.append("and")
            else:
                if literal[0]!="and":
                    components.append(literal)
                else:
                    for literal_x in literal:
                        if literal_x=="and":
                            continue
                        else:
                            components.append(literal_x)

    if(components[0]=="or"):
        temp_components=copy.deepcopy(components)
        del components[:]
        for literal in temp_components:
            if literal=="or":
                components.append("or")
            else:
                if literal[0]!="or":
                    components.append(literal)
                else:
                    for literal_x in literal:
                        if literal_x=="or":
                            continue
                        else:
                            components.append(literal_x)

    for literal in components:
        if(len(literal)>1):
            associvity(literal) 
                   
""" REMOVE PARENS """   
def remove_parens(components):
     i=0
     for literal in components:
        if(len(literal)==1):
            temp=str(literal)  
            if(len(temp)>1):
              components[i]=temp[2]
        elif(len(literal)>1):
            remove_parens(literal)
        i=i+1

""" REMOVE DUPLICATES """
def remove_duplicates(components):
    delete_literals=[]
    if(components[0]=="and" or components[0]=="or"):
        for x in range(0,len(components)):
            for y in range(x+1,len(components)):
                literal_1=sorted(components[x])
                literal_2=sorted(components[y])
                if literal_1==literal_2:
                   delete_literals.append(components[y])
 
    if(len(delete_literals)>=1):
        temp_components=[]
        for literal in delete_literals:
            flag=1
            for literal_x in components:
                if (literal==literal_x and flag==1):
                    flag=0
                    continue
                else:
                    temp_components.append(literal_x)
        
        del components[:]
        for literal in temp_components:
            components.append(literal)
        

    for literal in components:
        if(len(literal)>1):
            remove_duplicates(literal) 

""" REMOVE SINGLE LITERALS WITH AND-OR """
def remove_single_literals(components):
    if(len(components)==2 and components[0]!="not"):
        del components[0]

    for literal in components:
        if(len(literal)>1 and isinstance(literal, list)):
            remove_single_literals(literal)

""" QUALITY CHECK """
def quality_check(components):
    if(len(components)==1 and len(components[0])>1):
        literal=components[0]
        del components[:]
        for literal_x in literal:
            components.append(literal_x)

    for literal in components:
        if(len(literal)>1):
            quality_check(literal)

   
""" WRITE TO OUTPUT FILE """
def writeOutput(final_list):
    filename='sentences_CNF.txt'
    outputFile = open(filename,'a')

    for sentence in final_list:
        sentence=str(sentence)
        sentence=sentence.replace("\'","\"")
        outputFile.write(sentence)
        outputFile.write("\n")
    
    outputFile.close()

""" CLEAR THE OUTPUT FILE """
def clear():
    filename='sentences_CNF.txt'
    outputFile = open(filename,'w')
    outputFile.truncate()
    outputFile.close()

""" READ THE INPUT FILE """
clear()
inputFile = open(sys.argv[2])
conf=0
line_number=0
final_list=[]
for line in inputFile:
    if conf==0:
        spl = line.strip().split(' ')
        line_number=int(spl[0])
        conf=1
    else:
        sentence=convert_CNF(line)
        if(len(sentence)==1):
            temp="\""+sentence[0]+"\""
            final_list.append(temp)
        else:
            final_list.append(sentence)
                    
inputFile.close()
writeOutput(final_list)