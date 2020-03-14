import re
import sys
list0=[]
s=""  
list1=[]
type=0



#DIALOG function

def createDialogFile(filename):
    global type
    global s
    global list
    global list1
    fp=open(filename,"r",encoding="UTF-8")
    s1=s+(fp.read())
    s1=s1.replace("Page", "",1)                                                #replacing the word "Page" to read chapter names
    
    #we try to divide the code to red 2 types of file. if file is like "sh.txt" it is type or else it is like "dracula.txt"
    
    if(len(re.findall(r'([XVI]+\.\s\b[A-Z]+\b\s\b[A-Z]+\b)', s1))):            #(checking if file is type 1 or not)
        type=1
    s1=re.sub(r'([XVI]+\.\s\b[A-Z]+\b\s\b[A-Z]+\b)', r'CHAPTER \1', s1)        #adding keyword "CHAPTER" before roman numerals
    
    
    #Storing the chapter number and names in the list1.
    if(type==1):        
        list1.append(re.findall(r'CHAPTER ([XVI]+\.\s\b[A-Z]+\b\s\b[A-Z\-]+\b\s\b[A-Z]+\b\s((\b[A-Z\-\’]+\b)\s){0,10})', s1))
    else:        
        list1.append(re.findall(r'CHAPTER\s[A-Za-z\s\'\-\"\.,]+[^0-9\-\_]', s1))
        list2=[]
        for i in list1[0]:
            i=i.replace("\n"," ")
            i=i.replace("   ","")
            list2.append(i)
        list1.clear()
        list1=list2.copy()
        
        '''1.Replacing newline with space
           2. Replacing “ with "  
           3. adding space between closing " and any special character like ) or - or ;
        '''
        
    s2=s1.replace("\n"," ")
    s2=s2.replace("“","\"")
    s2=s2.replace("”","\"")
    s2=s2.replace("      "," ")
    s2=s2.replace("\"),","\" ")
    s2=s2.replace("\"-,","\" -")
    s2=s2.replace("\";,","\" ;")
    list0.append(re.findall(r'["](.*?)" |(CHAPTER\s[A-Z]+)',s2))
    fp2=open('testfile.txt', 'w')
    for i in range(len(list0[0])):                                             #storing the dialog in file=testfile.txt present in the same directory
        if(list0[0][i][1]!=""):
            fp2.write("\"%s\"\n" % list0[0][i][1])
        else:
            fp2.write("\"%s\"\n" % list0[0][i][0])
         
    fp2.close()
    fp.close()
count=0
totalchapters=0
a=[]
b=[]
a.append(-1)
#KMP serach algo for searching dialog in testfile.txt
def KMPSearch(pat, txt): 
    global count
    global a
    M = len(pat) 
    N = len(txt)   
    lps = [0]*M 
    j = 0 
    computeLPSArray(pat, M, lps) 
    i = 0 
    while i < N: 
        if pat[j] == txt[i]: 
            i += 1
            j += 1
        if j == M: 
            j = lps[j-1]
            a.append(i-j)
            count=count+1
        elif i < N and pat[j] != txt[i]: 
            if j != 0: 
                j = lps[j-1] 
            else: 
                i += 1
  
def computeLPSArray(pat, M, lps): 
    len = 0
    lps[0] 
    i = 1
    while i < M: 
        if pat[i]== pat[len]: 
            len += 1
            lps[i] = len
            i += 1
        else: 
            if len != 0: 
                len = lps[len-1]  
            else: 
                lps[i] = 0
                i += 1
                
def numberofchapter():  # function to calculate the total no of chapters
    global count
    global totalchapters
    global type
    s2=''
    fp=open("testfile.txt","r")
    txt=s2+(fp.read()) 
    fp.close()
    KMPSearch("CHAPTER",txt)
    a.sort()
    totalchapters=count/2
    if type==1:
        totalchapters=count
    count=0;
    


def findstring(s,casesensitive):#function to add case sensitive and case insensitive search.
    numberofchapter()
    global a 
    global b
    global type
    global list1
    b.clear()
    b=a.copy()
    a.clear()
    global totalchapters 
    s2=''
    fp5=open("testfile.txt","r")
    txt=s2+(fp5.read()) 
    fp5.close()
    if(casesensitive==1):
        KMPSearch(s,txt)
    else:
        s=s.upper()
        txt=txt.upper()
        KMPSearch(s,txt)
    a.sort()
    print("____________________________________________FOUND IN THE FOLLOWING CHAPTERS_________________________________________________________")
    if(len(a)==0):
        print("Not in any chapter")     
    for i in range(len(a)):
        flag=0
        if type!=1:
            for j in range (int(totalchapters)-1,len(b)):
                if(a[i]<b[j]):
                    if(j-1-int(totalchapters)==0):
                        print("Found one occurence before the novel starts(maybe in content, preface, title)")
                        flag=1
                        break;
                    elif(j-2-int(totalchapters)==0): 
                        print(str(list1[0]))
                        flag=1
                        break;
                    else:
                        print(str(list1[j-2]))
                    flag=1
                    break
            if(flag==0):
                print(str(list1[int(totalchapters)-1]))
            print("-------------------------------------------------------------------------------------------------------")
        
            
        else:
            for j in range (0,len(b)):
                if(a[i]<b[j]):
                    if(j-2==0): 
                        print(str(list1[0][0][0]))
                        flag=1
                        break;
                    elif(j-1==0):
                        print("Found one occurence before the novel starts(maybe in content, preface, title)")
                        flag=1
                        break;
                    else:
                        print(str(list1[0][j-2][0]))
                        flag=1
                        break
            if(flag==0):
                print(str(list1[0][int(totalchapters)-1][0]))
            print("-------------------------------------------------------------------------------------------------------")                

def dialogSearch(filename,pattern,casesensitive):##calling the functions here
    createDialogFile(filename)
    findstring(pattern,casesensitive)
    a.clear()
    

def explain():
    print("-----------------ALERT---------------------\nWhen running the code for DIALOGSEARCH with filename in CMD\n1.enter the file in which Dialog has to be searched for\n2.enter the string to be searched for\n3.enter 1 for case sensitive search and 0 for non sensitive search \n(format: python3 temp.py dracula.txt Dracula 1)\n\n\n\n-----------------ALERT---------------------\nWhen running the code for DIALOG with filename in CMD\n1.enter the file in which Dialog has to be searched for\n(format: python3 temp.py sh.txt)\n")       



if __name__ == "__main__":
    if(len(sys.argv)==4):
        filename=str(sys.argv[1])
        pattern=str(sys.argv[2])
        casesensitive=int(sys.argv[3])
        dialogSearch(filename,pattern,casesensitive)
    elif(len(sys.argv)==2):
        createDialogFile(str(sys.argv[1]))
        
    else:
        explain()