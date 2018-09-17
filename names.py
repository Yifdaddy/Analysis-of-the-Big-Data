import csv

##readNames###
def readNames(infile):
    names_list=[]
    with open(infile, 'r') as f:
        reader=csv.reader(f)
        for row in reader:
            names_list.append(row)
    return(names_list)
####test function####
#print(readNames('names_tiny.csv')) 
#####################
#for this function all the value will be convert to character and store in a list of list

##nameIndex###
def nameIndex(names):
    data_list=readNames(names)
    year_list=[]
    name_list=[]
    gender_list=[]
    for i in range(len(data_list)):
        year_list.append(data_list[i][0])
        name_list.append(data_list[i][1])
        gender_list.append(data_list[i][2])
    uni_year_list=list(set(year_list))
    uni_name_list=list(set(name_list))
    
    dic={}
    for i in range(len(uni_name_list)):
        temp_tup=[]
        for j in range(len(uni_year_list)):
            temp_male_num=0
            temp_female_num=0
            for l in range(len(data_list)):
                if data_list[l][1]==uni_name_list[i] and data_list[l][0]==uni_year_list[j]:
                    if data_list[l][2]=="M":
                        temp_male_num=data_list[l][3]
                    if data_list[l][2]=="F":
                        temp_female_num=data_list[l][3]
            if int(temp_male_num)+int(temp_female_num) !=0:   
                temp_tup.append((int(uni_year_list[j]),int(temp_male_num),int(temp_female_num)))
        temp_tup=(sorted(temp_tup, key=lambda x:x[0]))
        dic[uni_name_list[i]]=temp_tup 
    return(dic)
####test function####
#nameIndex("names_tiny.csv")
#####################
#for this function it will record the list as a dictionary and the year, counter num will convert back to int from str

##yearIndex###
def yearIndex(names):
    data_list=readNames(names)
    year_list=[]
    name_list=[]
    gender_list=[]
    for i in range(len(data_list)):
        year_list.append(data_list[i][0])
        name_list.append(data_list[i][1])
        gender_list.append(data_list[i][2])
    uni_year_list=list(set(year_list))
    uni_name_list=list(set(name_list))  
    uni_year_list.sort()
    dic_year={}
    for i in range(len(uni_year_list)):
        temp_name_dic={}
        for j in range(len(uni_name_list)):
            temp_male_num=0
            temp_female_num=0
            
            for l in range(len(data_list)):
                if data_list[l][0]==uni_year_list[i] and data_list[l][1]==uni_name_list[j]:
                    if data_list[l][2]=="M":
                        temp_male_num=data_list[l][3]
                    if data_list[l][2]=="F":
                        temp_female_num=data_list[l][3]
            if int(temp_male_num)+int(temp_female_num) !=0:
                temp_name_dic[uni_name_list[j]]=(int(temp_male_num),int(temp_female_num))
        dic_year[int(uni_year_list[i])]=temp_name_dic    
    return(dic_year)
####test function####
#yearIndex('names_tiny.csv')
#####################
#for this function create a nested dictionary store the year and name info
        
##getBirthsByName###
def getBirthsByName(filename,name,gender=None,start=None,end=None,interval=None):
    
    #get range for the years
    data_list=readNames(filename)
    year_list=[]
    name_list=[]
    gender_list=[]
    for i in range(len(data_list)):
        year_list.append(data_list[i][0])
        name_list.append(data_list[i][1])
        gender_list.append(data_list[i][2])
    uni_year_list=list(map(int,list(set(year_list))))
    uni_name_list=list(set(name_list))  
    uni_gender_list=list(set(gender_list))  
    
    name_index=nameIndex(filename)
    
    #test if the input name is in the datafile
    if name not in uni_name_list:
        print("The name: %s, is not in the name list. End of function..." %name)
        return(0)
    #set flag for gender to test if we have the value or not
    if gender==None:
        flag_gender=0
    else:
        if gender.upper() not in uni_gender_list:
            flag_gender=0
            print("Gender selection will not be functioned. The gender input can only be 'f' or 'm'")
        else:
            flag_gender=1
    #set flag for start to test if we have the value or not        
    if start==None:
        flag_start=0
    else:
        if start not in uni_year_list:
            print("The time selection will not be functioned. The start time input is out of year boundary.")
            flag_start=0
        else:
            flag_start=1
    #set flag for end to test if we have the value or not
    if end==None:
        flag_end=0
    else:
        if end not in uni_year_list:
            print("The time selection will not be functioned. The end time input is out of year boundary.")
            flag_end=0
        else:
            flag_end=1
    #set flag for interval to test if we have the value or not
    if interval==None:
        flag_interval=0
    else:
        flag_interval=1
    
    flag_score=flag_gender*1000+flag_start*100+flag_end*10+flag_interval
    #test about time logic, the only two situation make sense are:
    #start<=end and interval>=0  or start>=end and interval<=0
    #combine with the flag only ?111(have start, end interval), ?110(have start, end, interval default to be 1) and ?100(have start, end default to be the last year) make sense
    test_time=flag_score%1000
    
    if test_time!=111 and test_time!=110 and test_time!=100 and test_time>0: 
        print("The time selection will not be functioned. Lack of start, end ,interval dependency.")
        flag_score=flag_score-test_time
    if test_time==111 and ((start<=end and interval<0) or (start>=end and interval>0)):
        print("The time selection will not be funcitoned. Conflict logic for start, end interval.")
        flag_score=flag_score-test_time
    target_birth=[]
    #only name provided
    if flag_score==0:
        for i in range(len(name_index[name])):
            target_birth.append((name_index[name][i][0],name_index[name][i][1]+name_index[name][i][2]))
    #only name and gender provided
    if flag_score/1000>=1 and flag_score%1000==0:
        if gender=='m':
            for i in range(len(name_index[name])):
                        target_birth.append((name_index[name][i][0],name_index[name][i][1]))
        if gender=='f':
            for i in range(len(name_index[name])):
                        target_birth.append((name_index[name][i][0],name_index[name][i][2]))
    #only name and time range provided
    if flag_score/1000<1 and flag_score%1000!=0:
        if flag_score%1000==100:
            start_t=start
            end_t=start+1
            interval_t=None
        if flag_score%1000==110:
            start_t=start
            end_t=end+1
            if start_t>=end_t:
                interval_t=-1
            if start_t<end_t:
                interval_t=1
        if flag_score%1000==111:
            start_t=start
            end_t=end+1
            interval_t=interval
        
        if interval_t==None:
            time_range=range(start_t,end_t)
        else:
            time_range=range(start_t,end_t,interval_t)
            
        for i in time_range:
            for j in range(len(name_index[name])):
                if name_index[name][j][0]==i:
                    target_birth.append((i,name_index[name][j][1]+name_index[name][j][2]))
    #all the name, gender and time range provided
    if flag_score/1000>=1 and flag_score%1000!=0:
        if flag_score%1000==100:
            start_t=start
            end_t=start+1
            interval_t=None
        if flag_score%1000==110:
            start_t=start
            end_t=end+1
            if start_t>=end_t:
                interval_t=-1
            if start_t<end_t:
                interval_t=1
        if flag_score%1000==111:
            start_t=start
            end_t=end+1
            interval_t=interval
        
        if interval_t==None:
            time_range=range(start_t,end_t)
        else:
            time_range=range(start_t,end_t,interval_t)
        
        for i in time_range:
            for j in range(len(name_index[name])):
                if name_index[name][j][0]==i and gender=='m':
                    target_birth.append((i,name_index[name][j][1])) 
                if name_index[name][j][0]==i and gender=='f':
                    target_birth.append((i,name_index[name][j][2]))
    return(target_birth)
        
####test function####
#getBirthsByName('names_tiny.csv','Mary')
#getBirthsByName('names_tiny.csv','Mary','m')
#getBirthsByName('names_tiny.csv','Mary',start=2005,end=2010,interval=2)
#getBirthsByName('names_tiny.csv','Mary',end=2010,interval=2)
#getBirthsByName('names_tiny.csv','Mary',start=2005,interval=2)
#getBirthsByName('names_tiny.csv','Mary','m',start=2005)
#getBirthsByName('names_tiny.csv','Mary','m',start=2005,end=2010,interval=2)
#####################
#for this function 200% satisfy the function definition, complete all the logic blind angle
        
##getNamesByYear###
#for this function just follow the description, no need to make so perfect
def getNamesByYear(filename,N=None, pattern=None, gender=None, start=None, end=None, interval=None):
    #get range for the years
    data_list=readNames(filename)
    year_list=[]
    name_list=[]
    gender_list=[]
    for i in range(len(data_list)):
        year_list.append(data_list[i][0])
        name_list.append(data_list[i][1])
        gender_list.append(data_list[i][2])
    uni_year_list=list(map(int,list(set(year_list))))
    uni_name_list=list(set(name_list))  
    uni_gender_list=list(set(gender_list))
    min_year=min(uni_year_list)
    max_year=max(uni_year_list)
    
    year_index=yearIndex(filename)    
    
    if N==None:
        N=len(uni_name_list)
    else:
        N=N
        
    if pattern==None:
        pattern=uni_name_list
    else:
        pattern=pattern.split(',')
        pattern=[str(x).strip() for x in pattern]
    
    #set the time range first
    if start==None:
        start_t=min_year
        if end==None:
            end_t=max_year+1
            if interval==None:
                interval_t=1
            else:
                interval_t=1
                print("The time selection will not be functioned. Interval needs both start and end year.")
        else:
            end_t=max_year+1
            interval_t=1
            print("The time selection will not be functioned. End year needs start year.")
    else:
        start_t=start
        if end==None:
            if interval==None:
                end_t=start+1
                interval_t=None
            else:
                start_t=min_year
                end_t=max_year
                interval_t=1
                print("The time selection will not be functioned. Interval needs end year.")
        else:
            end_t=end+1
            if interval==None:
                if start_t>=end_t:
                    interval_t=-1
                else:
                    interval_t=1
            else:
                if start_t>=end_t:
                    if interval>0:
                        start_t=min_year
                        end_t=max_year+1
                        interval_t=1
                        print("The time selection will not be functioned. Start year is bigger than end year, interval should be negative.")
                    if interval<0:
                        interval_t=interval
                else:
                    if interval>0:
                        interval_t=interval
                    else:
                        start_t=min_year
                        end_t=max_year+1
                        interval_t=1
                        print("The time selection will not be functioned. Start year is smaller than end year, interval should be positive.")                        
    tup=[]
    if interval_t==None:
        time_range=range(start_t,end_t)
    else:
        time_range=range(start_t,end_t,interval_t)  
        
    for i in time_range:
        for j in pattern:
            if j in year_index[i].keys():
                if gender=='m':
                    tup.append((j,year_index[i][j][0]))
                if gender=='f':
                    tup.append((j,year_index[i][j][1]))
                if gender==None:
                    tup.append((j,year_index[i][j][0]+year_index[i][j][1]))
    tup_sort=(sorted(tup, key=lambda x:x[1],reverse=True))
    tup_select=tup_sort[0:N]
    return(tup_select)
####test function####
#getNamesByYear('names_tiny.csv',pattern="Mary, Alice", gender="f", start=2000, end=2012, interval=2,N=10)
#getNamesByYear('names_tiny.csv',pattern="Mary, Alice", gender="f", start=2000, end=2012, interval=-2,N=10)
#getNamesByYear('names_tiny.csv',pattern="Mary, Alice", gender="f", start=2012, end=2000, interval=2,N=10)
#getNamesByYear('names_tiny.csv',pattern="Mary, Alice",  start=2000, end=2012, interval=2,N=10)
#####################
###################This part is just try the function and show the graph, no new code is needed######
#import matplotlib.pyplot as plt

#alberto=getBirthsByName('names_tiny.csv','Alberto')
#patrick=getBirthsByName('names_tiny.csv','Patrick')
####
#plt.title('Births by Year')
#plt.xlabel('Year')
#plt.ylabel('Birth')
#plt.plot([y for (y,v) in alberto],[v for (y,v) in alberto])
#plt.show()
####

#plt.title("Briths by Year")
#plt.xlabel('Year')
#plt.ylabel('Birth')
#plt.plot([y for (y,v) in alberto],[v for (y,v) in alberto], 'r--', label='Alberto(m)')
#plt.plot([y for (y,v) in patrick],[v for (y,v) in patrick], 'g--', label='Patrick(m)')
#plt.legend(loc=2)
#plt.show()
            
####        
#girls=getNamesByYear('names_tiny.csv',gender="f", start=1987, end=2006, interval=3,N=10) 
#plt.title('Births by Name')
#plt.xlabel('Births')
#plt.yticks(range(len(girls),0,-1),[n for (n,t) in girls])
#plt.barh(range(len(girls),0,-1),[t for (n,t) in girls])
#plt.show()
######################################        

##names###
def names(infile="names_tiny.csv"):
    import matplotlib.pyplot as plt
    #big loop all the small function below
    command="Action"
    while(command!='x'):
        in_comm=input('names>')
        command=in_comm[0]
        #convert str to int only for number values
        def convert_int(s):
            try:
                return int(s)
            except:
                return(s)
        #function for q
        if command=='q':
            input_row=[]
            for i in in_comm.split()[1:]:
                input_row.append(convert_int(i))
            #check how many input parameters
            length=len(input_row)
            if length==1:
                recall=getBirthsByName(infile,input_row[0])
                print(recall)
            if length==2:
                if 'm' in input_row or 'f' in input_row:
                    recall=getBirthsByName(infile,input_row[0],gender=input_row[1])
                    print(recall)
                else:
                    recall=getBirthsByName(infile,input_row[0],start=input_row[1])
                    print(recall)
            if length==3:
                if "m" in input_row or "f" in input_row:
                    recall=getBirthsByName(infile,input_row[0],gender=input_row[1],start=input_row[2])
                    print(recall)
                else:
                    recall=getBirthsByName(infile,input_row[0],start=input_row[1],end=input_row[2])
            if length==4:
                if "m" in input_row or "f" in input_row:
                    recall=getBirthsByName(infile,input_row[0],gender=input_row[1],start=input_row[2],end=input_row[3])
                    print(recall)
                else:
                    recall=getBirthsByName(infile,input_row[0],start=input_row[1],end=input_row[2], interval=input_row[3])
                    print(recall)  
            if length==5:
                recall=getBirthsByName(infile,input_row[0],gender=input_row[1],start=input_row[2],end=input_row[3], interval=input_row[4])
                print(recall)                
        
        if command=="p":
            input_row=[]
            for i in in_comm.split()[1:]:
                input_row.append(convert_int(i))
                #check how many input parameters
            length=len(input_row)
            if length==1:
                recall=getBirthsByName(infile,input_row[0])
                
            if length==2:
                if 'm' in input_row or 'f' in input_row:
                    recall=getBirthsByName(infile,input_row[0],gender=input_row[1])
                    
                else:
                    recall=getBirthsByName(infile,input_row[0],start=input_row[1])
                    
            if length==3:
                if "m" in input_row or "f" in input_row:
                    recall=getBirthsByName(infile,input_row[0],gender=input_row[1],start=input_row[2])
                    
                else:
                    recall=getBirthsByName(infile,input_row[0],start=input_row[1],end=input_row[2])
            if length==4:
                if "m" in input_row or "f" in input_row:
                    recall=getBirthsByName(infile,input_row[0],gender=input_row[1],start=input_row[2],end=input_row[3])
                    
                else:
                    recall=getBirthsByName(infile,input_row[0],start=input_row[1],end=input_row[2], interval=input_row[3])
                     
            if length==5:
                    recall=getBirthsByName(infile,input_row[0],gender=input_row[1],start=input_row[2],end=input_row[3], interval=input_row[4])
            
            #do the plot                            
            plt.title('Births by Year')
            plt.xlabel('Year')
            plt.ylabel('Birth')
            plt.plot([y for (y,v) in recall],[v for (y,v) in recall],'r--', label=input_row[0])
            
            
        if command=='s':
            #this function means nothing?
            plt.show()
        
        
            
                
                    
                    
                
            



            
                        
            
        
            
   

        
    
    
    

    
    

    

            







