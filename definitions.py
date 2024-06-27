
class Skill:
    """
    This class stores the information about skills and its level.
    """

    def __init__(self,name,level,presence=0.5,probability=0.5,cluster=None,family=None):
        self.name = name
        self.level = level
        self.presence = presence
        self.probability = probability
        self.cluster = cluster
        self.family = family


    def __str__(self):
        string_ = f"{self.name}"
        return string_
    
    def __repr__(self):
        return self.name
    
    def check_skill(self,skill_list):
        """
            This function checks if a given skill is in a list and returns the skill
            and its level or the self skill and level 0 if it is not found
        """
        for s in skill_list:
            if s.name == self.name: #skill found in list returning level
                return s,s.level
        
        return self,0 # skill not found, returning level 0
    
    def add_skill(self,skill_list):
        """
            This function adds a given skill in a list and updates it's level if it is higher
        """
        s,lev_ = self.check_skill(skill_list)
        if lev_ == 0: #skill not found
            skill_list.append(self)
        else: #skill found, check level and update
            if self.level > s.level: #update
                skill_list.remove(s)
                skill_list.append(self)
    
class Activity:
    """
    This class stores the information about activities and its methods.
    """

    def __init__(self,id,name,time=1,cost=1,course=True,provider=None,url=None):
        self.id = id
        self.name = name
        self.skills = [] #skills obtained after completing activity
        self.prerequisites = [] #skills required to do the activity
        self.time = time #time slots to complete the activity
        self.cost = cost #monetary cost to complete the activity
        self.course = course #boolean to indicate whether is it a course
        self.topics = [] #topics of the course
        self.provider = provider
        self.url = url
    
    def __str__(self):
        return f"{self.name}"


class Job:
    """
    This class stores the information about Jobs and its methods.
    """

    def __init__(self,id,name,descriptor=None):
        self.id = id
        self.name = name
        self.descriptor = descriptor
        self.skills = [] #skills needed for obtaining the job

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.id

