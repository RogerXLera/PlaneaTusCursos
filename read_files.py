"""
Roger Lera
19/10/2023
"""
import csv
import json
import pandas as pd
import os
import numpy as np
from definitions import *

def skill_extraction(line_,a,object_="Activity"):
    """
        This function extracts the skills aquired and the prerequisites of a given activity
            INPUT: line_ (of the dataframe)
                    a (activity object)
    """
    # we start with the skills
    if object_ == "Activity":
        try:
            skills = line_['skills'].split(';;')
            #skills_level = line_['probabilities'].split(';;')
            skills_level = []
        except:
            skills = []
            skills_level = []
        try:
            prereq = line_['skills required'].split(';;')
            prereq_level = line_['probabilities required'].split(';;')
        except:
            prereq = []
            prereq_level = []
    else:
        try:
            skills = line_['Skills Required'].split(';;')
            skills_level = line_['Prob Skills Required'].split(';;')
        except:
            skills = []
            skills_level = []
        prereq = []
        prereq_level = []
    
    #if len(skills) != len(skills_level):
        #raise ValueError(f"Different number of skills ({len(skills)}) and levels {len(skills_level)} for activity {a.name}.")
    for i in range(len(skills)):
        #s = Skill(name=skills[i],level=1,probability=float(skills_level[i])) #creating a skill object
        s = Skill(name=skills[i],level=1,probability=0.5) #creating a skill object
        s.add_skill(a.skills)

    if len(prereq) != len(prereq_level):
        raise ValueError(f"Different number of skills ({len(prereq)}) and levels {len(prereq_level)} for activity {a.name}.")
    for i in range(len(prereq)):
        s = Skill(name=prereq[i],level=1,probability=float(prereq_level[i])) #creating a skill object
        s.add_skill(a.prerequisites)

    return None

def read_activities(file_path):
    """
        This function reads the file containing the activities and 
    """
    df = pd.read_csv(file_path,sep=',') #store file in pandas.DataFrame
    
    activities = []
    for i in range(len(df)):

        line_ = df.iloc[i] #df line
        id_ = line_['id']
        name_ = line_['title']
        provider = line_['provider']
        try:
            time_ = float(line_['time'])
        except:
            time_ = 10.0
        if np.isnan(time_):
            time_ = 10.0
        """
        if type(line_['Money']) == str and len(line_['Money']) == 0:
            cost_= 0.0
        else:
            cost_= float(line_['Money'])
        """
        cost_ = 0
        url_ = line_['url']
        if cost_ <= 0:
            course_ = True
        else:
            course_ = False

        a = Activity(id=id_,name=name_,time=time_,cost=cost_,course=course_,url=url_,provider=provider) #create activity object
        skill_extraction(line_,a)
        activities.append(a)
    
    return activities

def skills_enumeration(list_):
    """
        This function gets all the skills listed in all the activities.
    """
    skills = []
    skills_level = []
    for a in list_:
        for s in a.skills:
            skills += [s.name]
            skills_level += [s.level]
    
    skills = np.array(skills)
    
    return np.unique(skills),np.max(np.array(skills_level))

def topics_enumeration(list_):
    """
        This function gets all the topics listed in all the activities.
    """
    topics = []
    
    for a in list_:
        for t in a.topics:
            topics += [t.name]

    
    topics = np.array(topics)
    
    return np.unique(topics)

def read_providers(folder_path):
    """
        This function saves all the activities from all providers
    """
    files = os.listdir(folder_path)
    A = [Activity(id=0,name='Initial Activity',cost=0)]
    for file in files:
        file_path = os.path.join(folder_path,file)
        activities = read_activities(file_path)
        A += activities

    return A


def read_fields(field_path):
    """
    This function reads the field names and returns a dict
    """

    with open(field_path,'r') as f:

        f_read = csv.reader(f)
        dict_ = {}
        for row in f_read:
            dict_.update({row[0]:row[1]})

    return dict_

def process_line(line):
    """
    This function process the lines of the .stdout file
    """
    detect_act = "Activity:"
    detect_st = "Start Period:"
    detect_ft = "End Period:"
    
    name = line.split(detect_act)[1].split('(')[0]
    st = int(line.split(detect_st)[1].split(' ')[1])
    fi = int(line.split(detect_ft)[1].split(' ')[1])
    h = float(line.split(')')[-2].split('(')[-1])

    return name[1:-1],st,fi,int(h)

def select_activity(name,A):

    len_ = len(name)
    for a in A:
        if name == a.name[:len_]:
            return a

    raise ValueError(f"{name} does not correspond to any activity.")

def create_link(name,url):
    return f'<a target="_blank" href="{url}">{name}</a>'

def read_path(file_path,A,a_trans):
    """
    This function reads the learning paths and returns a pd.Dataframe and the field affinity
    """

    with open(file_path,'r') as f:

        f_lines = f.readlines()
        name = []
        st = []
        fi = []
        h = []
        url = []
        fa = 0
        detect_act = "Activity:"
        detect_fa = "Job affinity:"
        for row in f_lines:
            if row[:len(detect_act)] == detect_act:
                nam,s,fi_,h_ = process_line(row)
                if nam == 'Initial Activity':
                    continue
                a = select_activity(nam,A)
                #name += [a.name]
                link = create_link(a_trans[str(a.id)],a.url)
                name += [link]
                st += [s]
                fi += [fi_]
                h += [h_]
                url += [a.url]
            elif row[:len(detect_fa)] == detect_fa:
                fa = float(row.split(detect_fa)[1].split(' ')[1])
                
    
    #return pd.DataFrame({'Course':name[1:],'Start Week':st[1:],"End Week":fi[1:],"Study Time (h)":h[1:],"URL":url[1:]}),fa
    return pd.DataFrame({'Curso':name,'Semana de Inicio':st,"Semana de Fín":fi,"Tiempo de Estudio (h)":h}),fa
    
    #return {'Course':name[1:],'Start Week':st[1:],"End Week":fi[1:],"Study Time (h)":h[1:]},fa

def print_dataframe(df):
    """
    This function prints the DataFrame
    """
    #col1,col2,col3,col4 = st.columns(4)
    return None

def read_job(file_name):
    
    with open(file_name,'r') as file_:
        reader = csv.reader(file_)
        row_ = []
        for row in reader:
            row_.extend(row)

        j = Job(row_[0],row_[1],row_[2])
        skills_ = row_[3].split(";;")
        #presence_ = row_[4].split(";;")
        for i in range(len(skills_)):
            s_ = Skill(skills_[i],1,presence=0.5)
            j.skills.append(s_)
       
    return j

def read_jobs(job_path,N:int=229):

    J = {}
    j_dict = {}
    for i in range(N):
        jobfile = os.path.join(job_path,f"{i}.csv")
        j = read_job(jobfile)
        J.update({j.id:j})
        j_dict.update({j.id:i})
    return J,j_dict

def read_field(field_id):
    """
        Read the jobs within the field and save the skills
    """

    path_ = os.getcwd()
    dir = os.path.join(os.path.join(path_,'jobs'),'jobs')
    files = os.listdir(dir)
    field_id = str(field_id)
    len_field = len(field_id)
    J = []
    for file in files:
        j_ = read_job(os.path.join(dir,file))
        if str(j_.id)[:len_field] == field_id:
            J += [j_]

    return J

def read_skill(line):
    """
    This function reads the line and returns the skills
    """
    line_split = line.split('\t')
    if len(line_split) == 3:
        return True,line_split[-1][1:-1]
    elif len(line_split) == 2:
        return False,line_split[-1][1:-1]
    else:
        return None,None

def read_skills(file_path,dicts,A):
    """
    This function reads the learning paths and returns the skills gained with the learning path
    """
    a_dict = {a.name:int(a.id) for a in A}
    j_trans,s_trans,a_trans = dicts
    trigger_s = "Skills per Unit"
    trigger_e = "Skills for Job"
    skill_extraction_c = False
    skill_extraction_j = False
    skills_courses = {}
    skills_job = []
    course = 'Initial Activity'
    with open(file_path,'r') as f:

        f_lines = f.readlines()
        for row in f_lines:
            if row[:len(trigger_s)] == trigger_s:
                skill_extraction_c = True
                continue
            elif row[:len(trigger_e)] == trigger_e:
                skill_extraction_c = False
                skill_extraction_j = True
                continue
            elif skill_extraction_c:
                is_skill,label = read_skill(row)
                if is_skill == True:
                    skills_courses.update({label:course[0:-1]})
                elif is_skill == False:
                    course = label
                else:
                    continue
            elif skill_extraction_j:
                skills_job.append(row[0:-1])

    
    name_c = []
    name_nc = []
    completed = []
    not_completed = []
    act_c = []
    act_nc = []
    for skill in skills_job:

        if skill in skills_courses.keys():
            name_c += [s_trans[skill]]
            completed += ['Sí ✅']
            course = skills_courses[skill]
            course_id = a_dict[course]
            act_c += [a_trans[str(course_id)]]
        else:
            name_nc += [s_trans[skill]]
            not_completed += ['No ❌']
            act_nc += ['']

    name = name_c + name_nc
    trab = completed + not_completed
    act = act_c + act_nc

    return pd.DataFrame(data={'Skill':name,'¿Trabajada?':trab,"Curso":act}) 

def read_all_skills():
    
    df = pd.read_excel(os.path.join(os.getcwd(),'jobs','asf.xlsx'),sheet_name='Skills hierarchy')
    list_ = list(df['Specialist Task'])

    return list_

def job_field_affinity(J,skills,n_jobs):
    """
    This function returns a df with the job affinity of the jobs belonging to a given field, 
    given the skills provided by the plan
    """
    jobs = []
    for j in J:
        ja_counter = 0
        l_skills = len(j.skills)
        for s in j.skills:
            if s.name in skills:
                ja_counter += 1
        jobs += [{'Jobs':j.name,'ja':ja_counter/l_skills*100}]

    def order_dict(e):
        return e['ja']
    
    jobs.sort(reverse=False,key=order_dict)

    return pd.DataFrame(jobs[:n_jobs])


def read_translations():

    path = os.getcwd()
    jobs = os.path.join(path,'jobs','job_dict.json')
    skills = os.path.join(path,'jobs','skills_dict.json')
    units = os.path.join(path,'courses','courses_dict.json')

    with open(jobs,'r') as inputfile:
        j_trans = json.loads(inputfile.read())
    with open(units,'r') as inputfile:
        u_trans = json.loads(inputfile.read())
    with open(skills,'r') as inputfile:
        s_trans = json.loads(inputfile.read())
    return j_trans,s_trans,u_trans
    