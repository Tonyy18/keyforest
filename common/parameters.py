
org_name_length = 50

class User:
    org_count = 5 #max organizations to create

class Organization:
    max_name_length = 50
    min_name_length = 4
    max_bio_length = 200

class API:
    max_org_search = 10 #maxmium results in one search

class Application:
    max_name_length = 50
    min_name_length = 4
    max_bio_length = 200 #Description length
    count_per_org = 50 #Applications in organization

class Role:
    class Admin:
        role = 1
    
    class Developer:
        role = 2
    
    class Moderator:
        role = 3
    
    testbench_access = [Admin.role, Developer.role]