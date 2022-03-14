
org_name_length = 50

class User:
    org_count = 5 #max organizations to create

class Organization:
    max_name_length = 50
    min_name_length = 4
    max_bio_length = 200
    app_count = 50 #Applications in organization

class API:
    max_org_search = 10 #maxmium results in one search
    max_user_search = 10 #maxmium results in one search

class Application:
    max_name_length = 50
    min_name_length = 3
    max_bio_length = 200 #Description length

class Role:
    class Admin:
        role = 1
    
    class Developer:
        role = 2
    
    class Moderator:
        role = 3
    
    testbench_access = [Admin.role, Developer.role]

class Permissions:
    class All:
        name = "*"
    class Create_apps:
        name = "create_apps"

    class Edit_org:
        name = "edit_org"

    class Access_all_apps:
        name = "access_all_apps"

    class Add_users:
        name = "add_users"

    class Remove_users:
        name = "remove_users"

class Permission_groups:
    class Manage_users:
        name = "manage_users"
        permissions = [Permissions.Add_users, Permissions.Remove_users]

    class All_permissions:
        name = "*"
        by_name = {}
        permissions = [
            Permissions.Create_apps,
            Permissions.Edit_org,
            Permissions.Access_all_apps,
            Permissions.Add_users,
            Permissions.Remove_users,
            Permissions.All
        ]
        for perm in permissions:
            by_name[perm.name] = perm
#permissions
#create applications => create_apps => apps page
#edit_org => edit ogranization info => summary page

#all_apps => view all apps in organization
#app_app name => view specific app

#invite => send user invitations to the organization