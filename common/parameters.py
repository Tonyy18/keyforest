
org_name_length = 50

class User:
    org_count = 5

class Organization:
    max_name_length = 50
    min_name_length = 4
    max_bio_length = 200

class API:
    max_org_search = 10

class Application:
    max_name_length = 50
    min_name_length = 4
    max_bio_length = 200
    count_per_org = 50

class Role:
    class Admin:
        role = 1
    
    class Developer:
        role = 2
    
    class Moderator:
        role = 3
    
    testbench_access = [Admin.role, Developer.role];