from alive_progress import alive_bar
from osint_functions import find_accounts, find_emails, get_amount_of_stargazers

try: 
    github_repo = input("Github Repo URL: ")

    result_filename = input("How should the file with emails be called (extension .txt automatically added): ")

    amount_of_followers = get_amount_of_stargazers(github_repo)

    accounts = []
    emails = []

    print("********************* \n")
    print("Parsing the accounts...")
    with alive_bar(int(amount_of_followers)) as bar:
        for account in find_accounts(github_repo, amount_of_followers):
            if account != None:
                accounts.append(account)
            bar()
    print("Successfully parsed the accounts! \n")
    print("********************* \n")
    print("Parsing the emails...")
    with alive_bar(len(accounts)) as bar:
        for email in find_emails(accounts):
            if email != None:
                emails.append(email)

            bar()
    print("Successfully parsed the emails! \n")

    filename = result_filename + ".txt"
    
    # save to file...
    with open(filename, 'a+') as file:
        for email in emails:
            file.write(email + "\n")


except KeyboardInterrupt:
    print("Successfully exited the program")