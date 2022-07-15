#importind module for sql
import pypyodbc as db
import pandas as pd
connection = db.connect('Driver={SQL Server};'
                        'Server=MANI\SQLEXPRESS;'
                        'Database=BankManagement;'
                        'Trusted_Connection=yes')
cursor = connection.cursor()


bankID = "49005"
bankCityNumber = "HAM"
clientNumber = 0

#Function to create new Client
def new_user(): 
    clientFirstName = input("Enter the First name of Client: ")
    clientLastName = input("Enter the Last name of Client: ")
    balance = 0
    if type (clientFirstName) == str and type (clientLastName) == str:
        try:
            clientFullName = clientFirstName + " " + clientLastName
            cursor.execute("SELECT clientID from ClientInfo")
            clientIDData = cursor.fetchall()

            for i in clientIDData:
                global x
                lastID = i[len(i) - 1]
                x = (lastID.split("M"))

            ClientNumID = int(x[1]) + 1
            newClientID = x[0] + "M" + str(ClientNumID)
            newClientCommand = ("INSERT INTO clientInfo (clientID, clientFirstName, clientLastName, balance ) VALUES (? , ? , ? , ?)")
            values = [newClientID, clientFirstName, clientLastName, balance]
    
            #Processing Query  
            cursor.execute(newClientCommand,values)   
            #Commiting any pending transaction to the database.  
            connection.commit()  
            #closing connection  
            connection.close()  
            print("New Client " + clientFullName + " has been created.\n"
                   "Client ID:  " + newClientID)
        except:
              print("Invalid Input, Please enter valid Name")
              new_user()

#Function used to get client information i.e name, id and balance
def clientInfo(clientID):
        cursor.execute("SELECT * from clientInfo WHERE clientID = '%s'" %clientID)
        client = cursor.fetchall()
        connection.commit()
        for i in client:
            number = i[0]
            balance = int(i[3])
            clientFullName = i[1] + " " + i[2]
            return (number, clientFullName, balance)



#if client want to deposit
def deposit(number, clientFullName, balance, clientID):
    try: 
        depositAmount =int(input("Enter amount that you want to deposit: "))
        if type (depositAmount) == int:
            balance = balance + abs(depositAmount)
            cursor.execute("UPDATE clientInfo SET balance = '%s' WHERE clientID = '%s' " %(balance, number))
            connection.commit()
            connection.close()
            print(clientFullName + " has $" + str(balance) +" in account.")
    except:
        print("Invalid Amount, Please enter a valid number")
        transaction(clientID)

#if client want to withdraw
def withdraw(number, clientFullName, balance, clientID):
    try:
        withdrawAmount = int(input("Enter amount that you want to withdraw: "))
        if type (withdrawAmount) == int:
            balance = balance - abs(withdrawAmount)
            cursor.execute("UPDATE clientInfo SET balance = '%s' WHERE clientID = '%s' " %(balance, number))
            print(clientFullName + " has $" + str(balance) +" in account.")
            connection.commit()
            connection.close()
    except:
        print("Invalid Amount, Please enter a valid number")
        transaction(clientID)
# Any transaction has been made on client account i.e withdraw/deposit
def transaction(clientID):
    try:
        clienttuple = clientInfo(clientID)
        number = str(clienttuple[0])
        clientFullName = clienttuple[1]
        balance = int(clienttuple[2])
        info = ("Client ID: " + number + "\n"
                "Client Name: " + clientFullName + "\n"
                "Balance: {}")
        print(info.format(balance))

        choice = int(input("Press 1 if you want to deposit OR Press 2 if you want to Withdraw."))
        if choice == 1:
            deposit(number, clientFullName, balance, clientID)
        elif choice == 2:
            withdraw(number, clientFullName, balance, clientID)
        else:
            print("Enter only 1 or 2.")
            transaction(number)
    except:
        print("Invalid Client ID. Please Enter ID again")
        correct_Input()


#making sure that user input correct key
def correct_Input():
    try:
        key = int(input("Press 1 if you want to create new account.\nPress 2 to access existing client.\n"
                        "Press 3 to print all client Information."))
        if key == 1:
            new_user()
            correct_Input()
        elif key == 2:
            clientNumber = input("Enter Client ID please: ")
            transaction(clientNumber)
            correct_Input()
        elif key == 3:
            print("Information of all Clients")
            fetchData()
            correct_Input()
        else:
             print("Wrong input. Try Again")
             key = int(input("Press 1 if you want to create new account or press 2 to access existing client: "))
             correct_Input()
    except: 
        print("Enter valid input 1,2 or 3.")
        correct_Input()
# fetching all the data from database
def fetchData():
    cursor.execute("SELECT * from ClientInfo")
    result = cursor.fetchall()
    allClients = []
    for data in result:
        data = list(data)
        allClients.append(data)

    columns = ["clientID", "clientFirstName", "clientLastName", "balance"]
    clientTable = pd.DataFrame(allClients, columns = columns)
    print(clientTable)


#main Program
print("Welcome to National Bank")
correct_Input()












