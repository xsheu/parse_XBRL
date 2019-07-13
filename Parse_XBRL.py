'''
Created on Jul 9, 2019

@author: xsheu
'''
import math

def xbrl_parse(xbrl_str):
    xbrl_file=open(xbrl_str)
    total=0
    digits=[0.0*i for i in range(99)]
    for lines in xbrl_file:
        try:
            line=lines.splitlines();
            for sentsence in line:
                segment=sentsence.split("<")
                for seperate in segment:
                    data=seperate.split(">")
                    for seperate_string in data:
                        if(seperate_string.isdigit()):
                            leading=seperate_string[0:1]
                            firsttwo=seperate_string[0:2]
                            leading_pos=int(leading)
                            firsttwo_pos=int(firsttwo)
                            digits[leading_pos-1]+=1
                            digits[firsttwo_pos-1]+=1
                            total+=1
        except:
            return -1,0                   
    for j in range(99):
        digits[j]=digits[j]/total
    return total, digits

def theoretical(opinion,digit,c,n):
    value=0.0
    if(opinion==1):
        value=Benford(digit)
    else:
        if(opinion==2):
            value=Zipf(digit,n)
        else:
            value=Pareto(digit,c,n)
    return value
            

def Benford(digit):
    return math.log10(1.0 + 1.0/digit)

def Zipf(digit,n):
    return 1.0/math.pow(digit,n)

def Pareto(digit,c,n):
    return c/math.pow(digit,n)

def cumulative(opinion,digits,c,n):
    actual = [0.0*i for i in range(99)]
    theo = [0.0*i for i in range(99)]
    cumub=0.0
    for j in range(1,9):
        for k in range(1,j):
            actual[j]=actual[j]+digits[k]
            cumub=theoretical(opinion,k,c,n)
            theo[j-1]=theo[j-1]+cumub
    for k in range(10,99):
        for j in range(10,k):
            actual[k]=actual[k]+digits[j]
            cumub=theoretical(opinion,j,c,n)
            theo[k]=theo[k]+cumub
    return actual,theo

def mad(itype,opinion,digits,c,n):
    value=0.0
    if(itype==1):
        start=1
        ends=9
    else:
        if(itype==2):
            start=10
            ends=99 
    for k in range(start,ends):
        if(opinion==1):
            theos=Benford(k)
        else:
            if(opinion==2):
                theos=Zipf(k,n)
            else:
                theos=Pareto(k,c,n)   
        diff=digits[k-1]-theos
        value+=abs(diff)
    return value/(ends-start+1)

def chi(itype,opinion,digits,c,n,total):
    value=0.0
    if(itype==1):
        start=1
        ends=9
    else:
        if(itype==2):
            start=10
            ends=99 
    for k in range(start,ends):
        if(opinion==1):
            theos=Benford(k)
        else:
            if(opinion==2):
                theos=Zipf(k,n)
            else:
                theos=Pareto(k,c,n)   
        diff=digits[k]-theos
        value+=diff*diff*total/theos
    return value

def Kuiper(itype,actual,theoret):
    left=0.0
    right=0.0
    if(itype==1):
        start=1
        ends=9
    else:
        if(itype==2):
            start=10
            ends=99 
    for k in range(start,ends):
        diff=actual[k]-theoret[k]
        left=max(diff,left)
        right=max(-diff,right)
    return (left+right)

def KolmogorovSmirnov(itype,actual,theoret):
    value=0.0
    if(itype==1):
        start=1
        ends=9
    else:
        if(itype==2):
            start=10
            ends=99 
    for k in range(start,ends):
        diff=abs(actual[k]-theoret[k])
        value=max(diff,value)
    return value

def mad_conclude(itype,value):
    if(itype==1):
        if(value<=0.006):
            return 1.0
        else:
            if(value<=0.012):
                return 1.0/3.0
            else:
                if(value<=0.015):
                    return -1.0/3.0
                else:
                    return -1.0
    else:
        if(value<=0.012):
            return 1.0
        else:
            if(value<=0.018):
                return 1.0/3.0
            else:
                if(value<=0.022):
                    return -1.0/3.0
                else:
                    return -1.0   

def chi_conclude(itype,level,value):
    critical_value=0.0
    if(itype==1):
        if(level==0.5):
            critical_value=13.362
        else:
            if(level==0.1):
                critical_value=15.507
            else:
                if(level==0.01):
                    critical_value=20.090
                else:
                    critical_value=26.124
    else:
        if(level==0.5):
            critical_value=106.469
        else:
            if(level==0.1):
                critical_value=112.022
            else:
                if(level==0.01):
                    critical_value=122.942
                else:
                    critical_value=135.948          
    if(value>=critical_value):
        return -1.0
    else:
        return 1.0

def Kuiper_conclude(value,total):
    critical_value=0.0
    if(level==0.5):
        critical_value=1.62
    else:
        if(level==0.1):
            critical_value=1.747
        else:
            if(level==0.01):
                critical_value=2.001
            else:
                critical_value=2.303      
    if(value>=critical_value/math.sqrt(total)):
        return -1.0
    else:
        return 1.0
    
def KolmogorovSmirnov_conclude(value,total):
    critical_value=0.0
    if(level==0.5):
        critical_value=1.22
    else:
        if(level==0.1):
            critical_value=1.36
        else:
            if(level==0.01):
                critical_value=1.63
            else:
                critical_value=1.95      
    if(value>=critical_value/math.sqrt(total)):
        return -1.0
    else:
        return 1.0
def ydetermine(ymin,ymax,value):
    if(value<=ymin):
        ymin=value
    if(ymax>=value):
        ymax=value
    return ymin,ymax    
    
        
file_str = "/Users/xsheu/eclipse-workspace/parse_XBRL/filelist.txt"
output_file="/Users/xsheu/Desktop/xbrl2018.txt"
total=0
f=open(file_str)
fo=open(output_file,"w")
for component in f:
    digital = [0.0 for i in range(99)]
    actual = [0.0 for i in range(99)]
    ymax1d=0.0
    ymin1d=0.0
    ymax2d=0.0
    ymin2d=0.0
    theoretical_digital = [0.0 for i in range(99)]
    theoretical_value = [0.0 for i in range(99)]
    for j in range(1,99):
        value=theoretical(1,j,0.0,0.0)
        theoretical_digital[j]=value
    total,digital = xbrl_parse(component)
    if(total != -1):
        opinion=1
        level=0.1
        c=0.0
        n=0.0
        actual,theoretical_value=cumulative(opinion,digital,c,n)
        KolmogorovSmirnov1d=0
        mad1d=mad(1,1,digital,c,n)
        chi1d=chi(1,1,digital,c,n,total)
        kuiper1d=Kuiper(1,actual,theoretical_value)
        KolmogorovSmirnov1d=KolmogorovSmirnov(1,actual,theoretical_value)
        mad1dconclude=mad_conclude(1,mad1d)
        ymin1d,ymax1d=ydetermine(ymin1d,ymax1d,mad1dconclude)
        chi1dconclude=chi_conclude(1,level,chi1d)
        ymin1d,ymax1d=ydetermine(ymin1d,ymax1d,chi1dconclude)
        kuiper1dconclude=Kuiper_conclude(kuiper1d,total)
        ymin1d,ymax1d=ydetermine(ymin1d,ymax1d,kuiper1dconclude)
        KolmogorovSmirnov1dconclude=KolmogorovSmirnov_conclude(KolmogorovSmirnov1d,total)
        ymin1d,ymax1d=ydetermine(ymin1d,ymax1d,KolmogorovSmirnov1dconclude)
        KolmogorovSmirnov2d=0
        mad2d=mad(2,1,digital,c,n)
        chi2d=chi(2,1,digital,c,n,total)
        kuiper2d=Kuiper(2,actual,theoretical_value)
        KolmogorovSmirnov2d=KolmogorovSmirnov(2,actual,theoretical_value)
        mad2dconclude=mad_conclude(2,mad2d)
        ymin2d,ymax2d=ydetermine(ymin2d,ymax2d,mad2dconclude)
        chi2dconclude=chi_conclude(2,level,chi2d)
        ymin2d,ymax2d=ydetermine(ymin2d,ymax2d,chi2dconclude)
        kuiper2dconclude=Kuiper_conclude(kuiper2d,total)
        ymin2d,ymax2d=ydetermine(ymin2d,ymax2d,kuiper2dconclude)
        KolmogorovSmirnov2dconclude=KolmogorovSmirnov_conclude(KolmogorovSmirnov2d,total)
        KolmogorovSmirnov2dconclude=KolmogorovSmirnov_conclude(KolmogorovSmirnov2d,total)
        print("Audit the file: "+component[32:]+" Completed")
    else:
        print("Audit the file: "+component[32:]+" encountered exceptions")
        ymin1d=-1.0
        ymax1d=-1.0
        ymin2d=-1.0
        ymax2d=-1.0    
    output_string = component[32:]+" "+str(ymin1d)+" "+str(ymax1d)+" "+str(ymin2d)+" "+str(ymax2d)
    fo.write(output_string)
f.close()
fo.close()    