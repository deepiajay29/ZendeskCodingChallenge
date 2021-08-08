import os
import json

#Zendesk Code Challenge: Command line application to search data in JSON files and return the results 

### FUNCTIONS ###

#Function to display help field details
def displayFields(userchoice) :
    tmp_field_map = fieldsmegamap[userchoice]
    print(tmp_field_map)

#The basic search function using hashmap
def search(userchoice, user_search_key, user_search_value):
    result = {}
    #print("userchoice is ", userchoice, user_search_key, user_search_value)
    if(userchoice not in megamap):
        return {}
    tmp_mega_map = megamap[userchoice]
    #print(tmp_mega_map)
       
    if user_search_key in tmp_mega_map.keys(): #Proceed only if the key exists
        tmp_map = tmp_mega_map[user_search_key] #Hash into the required map
        if user_search_value in tmp_map.keys():
            result = tmp_map[user_search_value]
            #print(json.dumps(result, indent=4, sort_keys=True))
            return result
        else:
            #print("Error: Search Item does not exist")
            return {}
    else:
        #print("Error1: Search Item does not exist")
        return {}
        
        
#This function is tightly coupled with user input mapped as 1) User 2) Ticket 3) Organisation and also their file names
def initialiseDependencies():
    megamap[user] = user_mega_map
    megamap[ticket] = tickets_mega_map
    megamap[organisation] = organisations_mega_map
    
    fieldsmegamap[user] = userfields_mega_map
    fieldsmegamap[ticket] = ticketfields_mega_map
    fieldsmegamap[organisation] = organisationfields_mega_map
    
    filename_inputindex_map["users.json"] = user
    filename_inputindex_map["tickets.json"] = ticket
    filename_inputindex_map["organizations.json"] = organisation


#This function creates a Hash map parsing all the required files for faster search.
def createHashMap():
    initialiseDependencies()
    fileNames = file_names;
    
    # In addition to creating a hash map, also create a list of all id's to be displayed as help to user
    for fileName in fileNames:
        userfile = open(fileName)
        userData = json.load(userfile)
        userfile.close()
        tmp_fields_map = []
        
        tmp_mega_map = megamap[filename_inputindex_map[fileName]]
        tmp_fields_map = fieldsmegamap[filename_inputindex_map[fileName]]
        
        for user in userData: #For each user
            #print(user)
            for key in user.keys(): #For each key in every user
                if(key not in tmp_fields_map):
                    tmp_fields_map.append(key)
                    
                if str(key) in tmp_mega_map:
                    user_key_map = tmp_mega_map[str(key)]
                else:
                    user_key_map = {}
                    
                #print(user[key])
                if(isinstance(user[key], list)): #if any key has a list as value
                    #print("list key", user[key], key)
                    for item in user[key]: #Eg for item in user["tags"] is a list
                        if item in user_key_map:
                            user_key_map[str(item)].append(user)
                        else:
                            user_key_map[str(item)] = [user]
                else:
                    if str(user[key]) in user_key_map:
                        user_key_map[str(user[key])].append(user)
                    else:
                        user_key_map[str(user[key])] = [user]
                            
                tmp_mega_map[str(key)] = user_key_map
            #print(tmp_mega_map)

# The main search function 
# First performs a basic search from one JSON file
# Then pulls in related information from other JSON files
# Eg for searching on users, perform relative searches on Tickets and Organisations to get Organisation name and
# Ticket details for a particular user.
def advanceSearch(userchoice, user_search_key, user_search_value):
    results = search(userchoice, user_search_key, user_search_value) #basic search function
    tmp_result_1 = {}
    tmp_result_2 = {}
    if(results != {}):
        #print("Search Successful")
        for result in results: #if successful, then parse other JSON files
            if(userchoice == user): #for user, get ticket and organisation details
                result["Ticket"] = []
                result["Organisation_Name"] = []
                tmp_result_1 = search(ticket, "submitter_id", str(result.get("_id")))
                #print(tmp_result_1)
                if(tmp_result_1 != {}):
                    for ticket_result in tmp_result_1: #iterate through all tickets submitted by this user
                        if "Ticket" in result:
                            result["Ticket"].append(ticket_result.get("subject"))
                        else:
                            result["Ticket"] = [ticket_result.get("subject")]
                        
                tmp_result_2 = search(organisation, "_id", str(result.get("organization_id")))
                if(tmp_result_2 != {}):
                    for org_result in tmp_result_2: #iterate through all organisations for this user
                        if "Organisation_Name" in result:
                            result["Organisation_Name"].append(org_result.get("name"))
                        else:
                            result["Organisation_Name"] = [org_result.get("name")]
                    
            if(userchoice == ticket): #for a ticket, get user and organisation details
                result["Submitter"] = []
                result["Organisation_Name"] = []
                tmp_result_1 = search(user, "_id", str(result.get("submitter_id")))
                #print(tmp_result_1)
                if(tmp_result_1 != {}):
                    for ticket_result in tmp_result_1: 
                        #print(ticket_result["name"])
                        if "Submitter" in result:
                            result["Submitter"].append(ticket_result.get("name"))
                        else:
                            result["Submitter"] = [ticket_result.get("name")]
                        
                tmp_result_2 = search(organisation, "_id", str(result.get("organization_id")))
                if(tmp_result_2 != {}):
                    for org_result in tmp_result_2: #iterate through all organisations for this user
                        #print(org_result["name"])
                        if "Organisation_Name" in result:
                            result["Organisation_Name"].append(org_result.get("name"))
                        else:
                            result["Organisation_Name"] = [org_result["name"]]
            if(userchoice == organisation): #for Organisation, get all users from a particular organisation
                result["Users"] = []
                tmp_result_1 = search(user, "organization_id", str(result.get("_id")))
                #print(tmp_result_1)
                if(tmp_result_1 != {}):
                    for ticket_result in tmp_result_1: 
                        #print(ticket_result["name"])
                        if "Users" in result:
                            result["Users"].append(ticket_result.get("name"))
                        else:
                            result["Users"] = [ticket_result.get("name")]
    return results

#This function is used to display results of the search in a readable format       
def displayResult(result):
    print(json.dumps(result, indent=4))
    
def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    #os.system('cls')              
    print("**********************************************")
    print("*********  Welcome to Zendesk Search  ********")
    print("**********************************************")
    print("Type 'quit' to exit at any time, Press 'Enter' to continue \n")
    userchoice = input()
    if userchoice == 'quit':
        print("\nThank you for using Zendesk CLI: Please email feedback to: support@zendesk.com")
        quit()
     
def get_user_choice():
    # Let users know what they can do.
    print("\n[1] Search Zendesk")
    print("[2] View List of Searchable fields")
    print("[quit] Quit.\n")
    return input("What would you like to do? ")

#This function is used to take user inputs and decide the next state of the application   
def processUserInput():
    display_title_bar()
    choice = ''
    while choice != 'quit':    
        print("\nPlease Select one of the following choices:")
        choice = get_user_choice()
        #Respond to the user's choice.
        if choice == '1':
            userchoice = input("Select 1)Users or 2)Tickets or 3)Organisations \n")
            if(userchoice == '1' or userchoice == '2' or userchoice == '3' ):
                user_search_key = input("Enter Search Term ")
                user_search_value = input("Enter Search Value ")
                result = advanceSearch(userchoice, user_search_key, user_search_value)
                if(result == {}):
                    print("*** Searching ",user_option[userchoice], " for " , user_search_key , " with a value of ", user_search_value, " ***")
                    print("*** No Results Found ***")
                else:
                    displayResult(result)
            elif userchoice == 'quit':
                print(thankyou_msg)
            else:
                print(incorrect_input_msg)
        elif choice == '2':
            userchoice = input("Select 1)Users or 2)Tickets or 3)Organisations \n")
            if(userchoice == '1' or userchoice == '2' or userchoice == '3' ):
                displayFields(userchoice)
        elif choice == 'quit':
            print(thankyou_msg)
            quit()
        else:
            print(incorrect_input_msg)

user = "1"
ticket = "2"
organisation = "3"
user_option = {}
user_option[user] = "Users"
user_option[ticket] = "Tickets"
user_option[organisation] = "Organisations"

file_names = {"users.json", "tickets.json", "organizations.json"}
filename_inputindex_map = {}

thankyou_msg = "\nThank you for using Zendesk CLI: Please email feedback to: customersupport@zendesk.com"
incorrect_input_msg = "\nIncorrect Input: Please enter one of the following choices \n"

#Parent hashmap used to index into user_mega_map,  tickets_mega_map or organisations_mega_map
megamap = {}
#Parent hashmap to store all keys for every JSON file.
fieldsmegamap = {}
#hashmap to store keys and values for each user.
user_mega_map = {}
#hashmap to store keys and values for every ticket.
tickets_mega_map = {}
#hashmap to store keys and values for each organisation.
organisations_mega_map = {}

#hashmap to store user, ticket and organisation fields.
userfields_mega_map = []
ticketfields_mega_map = []
organisationfields_mega_map = []

choice = ''
### MAIN PROGRAM ###
if __name__ == '__main__':
    os.system('cls')
    #Create a Hashmap by parsing all the JSON files for faster search
    createHashMap()
    # Set up a loop where users can choose what they'd like to do.
    processUserInput()
 
