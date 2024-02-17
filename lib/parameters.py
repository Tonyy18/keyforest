
class User:
    org_count = 5 #max organizations to create
    max_firstname_length = 30
    min_firstname_length = 2
    max_lastname_length = 30
    min_lastname_length = 2
    max_password_length = 50
    min_password_length = 3
    max_email_length = 100

class Organization:
    max_name_length = 50
    min_name_length = 4
    max_bio_length = 200
    app_count = 50 #Applications in organization

class API:
    max_org_search = 10 #maxmium results in one search
    max_user_search = 10 #maxmium results in one search
    max_app_search = 20 #maxmium results in one search

class Application:
    max_name_length = 50
    min_name_length = 3
    max_bio_length = 600 #Description length
    license_count = 50
    thumbnail_name_length = 45 #For displaying in UI

class License:
    max_name_length = 30
    min_name_length = 6
    max_bio_length = 300
    max_parameter_count = 15
    max_parameter_name_length = 15
    max_parameter_value_length = 15
    max_amount = 100000000
    max_price = 1000000.00
    min_price = 1.00
    max_subscription_period = 50000
    class Subscription_period_type:
        never = 0
        days = 1
        weeks = 2
        months = 3
        text = ["never ending", "days", "weeks", "months"]
        singular_text = ["never ending", "daily", "weekly", "monthly"]

class Transaction:
    class Type:
        purchase = 0
        platform_fee = 1
        text = ["Purchase transaction", "Platform fee"]

class Stripe:
    
    application_fee = 20 #percent

    class Checkout:
        class Status:
            open = 0
            completed = 1
            expired = 2
    class Subscription:
        class Status:
            incomplete = 0
            expired = 1
            active = 2
            past_due = 3
            canceled = 4
            unpaid = 5
            text = ["incomplete", "expired", "active", "past due", "canceled", "unpaid"]
    class Purchase:
        class Status:
            not_activated = 0
            activated = 1
            not_usable = 2
            canceled = 3
            text = ["not activated", "active", "not usable", "canceled"]
    class Invoice:
        class Status:
            draft = 0
            open = 1
            void = 2
            paid = 3
            uncollectible = 4
            text = ["draft", "open", "void", "paid", "uncollectible"]

class Server:
    url = "http://localhost:3000"

class Pages:
    class Checkout:
        desc_hide_length = 150

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

    class Stripe_connect:
        name = "stripe_connect"
        

class Permission_groups:

    class All_permissions:
        name = "*"
        by_name = {}
        permissions = [
            Permissions.Create_apps,
            Permissions.Edit_org,
            Permissions.Access_all_apps,
            Permissions.Add_users,
            Permissions.Remove_users,
            Permissions.All,
            Permissions.Stripe_connect,
        ]
        for perm in permissions:
            by_name[perm.name] = perm
#permissions
#create applications => create_apps => apps page
#edit_org => edit ogranization info => summary page

#all_apps => view all apps in organization
#app_app name => view specific app