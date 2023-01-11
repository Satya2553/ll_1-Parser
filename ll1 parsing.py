from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as ntx

name=input("ENTER THE FILE NAME CONSISTING OF GRAMMAR :  ")
f=open(name,"r")
s=f.read()
print("\n")
print(s)
print("\n")
s1=s.split("\n")
s2=[]
dict=defaultdict(list)
for i in range(len(s1)):
    s3=s1[i].split("->")
    for j in range(0,len(s3)-1,2):
        dict[s3[j]].append(s3[j+1])
st=s1[0].split("->")
start=st[0]
nt=list(dict.keys())
n=[]
for i in nt:
    if i not in n:
        n.append(i)
nonterminal=set(nt)
print("NONTERMINALS:")
print("-------------")
print(nonterminal)
print("\n")
t=list(dict.values())
t1=[]
for i in t:
    for j in i:
        for k in j:
            if k in nt:
                continue
            if k in t1:
                continue
            else:
                t1.append(k)
terminal=set(t1)
print("TERMINALS:")
print("---------")
print(terminal)
print("\n")
t2=terminal.copy()
if '^' in t2:
    t2.remove('^')

### CALCULATING FIRST
FIRST=defaultdict(list)
def first(char):
    for j in dict[char]:
        for k in j:
            if k in terminal:
                if k not in FIRST[char]:
                    FIRST[char].append(k)
                break
            if k in nonterminal:  
                ind=j.index(k)
                if '^' in first(k) and ind<len(k):
                    for i in first(j[ind+1]):
                        if i not in FIRST[char]:
                            FIRST[char]=first(k)+[i]
                    break
                else:
                    xt=first(k)
                    for r in xt:
                        if r not in FIRST[char]:
                            FIRST[char].append(r)
                    break 
    return FIRST[char]
for i in nonterminal:
    first(i)
print("FIRST:")
print("-----")
print(FIRST)
print("\n")

### CALCULATING FOLLOW
FOLLOW=defaultdict(list)
def follow(char):
    if char==start:
        FOLLOW[char]=['$']
    else:
        for i in t:
            for j in i:
                for k in range(len(j)):
                    if j[k]==char:
                        l=k+1
                        if l<len(j):
                            m=j[l]
                            if m in t2 and m not in FOLLOW[char]:
                                FOLLOW[char].append(m)
                                #break
                            if m in nonterminal:
                                if '^' in FIRST[m]:
                                    l2=FIRST[m].remove('^')
                                    FOLLOW[char]=FIRST[m]
                                    #break
                        elif l==len(j):
                            for n1 in nonterminal:
                                if dict[n1]==i and char!=n1:
                                    for w in follow(n1):
                                        if w not in FOLLOW[char]:
                                            FOLLOW[char]=FOLLOW[char]+follow(n1)
                                    #break
                            #break
    return FOLLOW[char]
for i in nonterminal:
    follow(i)
print("FOLLOW:")
print("------")
print(FOLLOW)
print("\n")
di=defaultdict(list)
for i in range(len(s1)):
    s4=s1[i].split("->")
    for i in range(0,len(s4)-1,2):
        di[s4[i+1]].append(s4[i])

### Table filling
table=[[ "  " for i in range(len(t2)+2)] for j in range(len(nonterminal)+1)]
for i in range(len(t2)+2):
    k=i-2
    n2=len(t2)+1
    table[0][n2]='$'
    for x in t1[k]:
        if x=='^':
            break
    if i==0:
        table[0][i]="  "
    elif i==len(t2)+1:
        table[0][i]="$"
    else :
        if t1[i-2]!='^':
            table[0][i]=t1[i-2]
table[0][-1]=='$'
for j in range(len(nonterminal)+1):
    if j==0:
        table[j][0]="  "
    else:
        table[j][0]=n[j-1]
for i in range(1,len(nonterminal)+1):
    for j in range(1,len(t2)+2):
        for k in range(len(FIRST[n[i-1]])):
                       if FIRST[n[i-1]][k]==table[0][j]:
                           b=n[i-1]
                           for l in dict[b]:
                               table[i][j]=b+'->'+l
                           for l in dict[b]:
                               if l[0]==table[0][j]:
                                   table[i][j]=b+'->'+l
if '^' in terminal:
    for i in range(1,len(nonterminal)+1):
        for j in range(1,len(t2)+2):
            for k in range(len(FOLLOW[n[i-1]])):
                           if FOLLOW[n[i-1]][k]==table[0][j]:
                               f=n[i-1]
                               for g in  dict[f]:
                                   table[i][j]=f+'->'+'^'
                               for g in  dict[f]:
                                   if g[0]==table[0][j]:
                                       table[i][j]=f+'->'+'^'

print("PARSE TABLE FOR GIVEN GRAMMAR WILL BE: ")
print("---------------------------------------")
for i in range(len(nonterminal)+1):
    for j in range(len(t2)+2):
        print(format(table[i][j],"<8"),end="  ")
    print()

##VALIDATING INPUT
print("\n")
str=input("Enter the string you want to validate:  ")
print(str)
y=[]
for i in str:
    y.append(i)
stack=[]
stack.append(start)
G=ntx.DiGraph()
o=0
while(len(stack)!=0 and len(y)>0):
    for i in range(len(nonterminal)+1):
        for j in range(len(t2)+2):
            if table[0][j-2]==y[0]:
                e=stack[-1]
                if stack[-1]==table[i-1][0]:
                    t=table[i-1][j-2]
                    l=t.split('->')
                    z=l[-1]
                    t1=z[::-1]
                    stack.pop()
                    for x in t1:
                        stack.append(x)
                    for k in z:
                        G.add_edges_from([(e,k)])      
        if stack[-1]=='^':
            stack.pop()
    if stack[-1]==y[0]:
        stack.pop()
        y.remove(y[0])
    else:
        break
    """"""
    o+=1
if len(stack)==0:
    print("ACCEPTED")
    pos=ntx.spring_layout(G)
    ntx.draw_networkx_nodes(G,pos,node_size=500)
    ntx.draw_networkx_edges(G,pos,edgelist=G.edges())
    ntx.draw_networkx_labels(G,pos)
    plt.show()
else:
    print("REJECTED")
