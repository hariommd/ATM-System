"""
Hello Folks !!!
This is simple python based ATM System

***********************************
>>Fetures are as follows:
    1.User Registration (Username / Pin / Initial Balance)
    2.Local Database based User Validation for every trasnsaction
    3.Withdraws Cash and updates balnace in database.
    4.Add Cash to User Balance
    5.Shows withdrawn amont notes count in 1000 & 100's.

**********************************
Technologies Used : Python & PostgreSQL (for Local Database)

First Install psycopg2 ( for postrgresql connection with python )
Changes required to make it working :
    1.Create DB Named >> abc in PostgreSQL
    2.Make Databse Conn changes accordingly 

For any Queries Regarding Project Contact : hariomd44@gmail.com
"""

import getpass
import psycopg2

def newuser():
    try:
        conn = psycopg2.connect("dbname=abc user=postgres password=postgre")
        cursor = conn.cursor()
        
        username = input("Enter Your Name : ")
        pin = getpass.getpass("Enter 4 Digit Pin for ATM : ")
        if len(pin) < 4 or len(pin) > 4:    
            print("Pleasse Proivde Correct Pin")    
        else:   
            cnfpin = getpass.getpass("Enter Pin Again : ")
            if pin == cnfpin :
                balance = int(input("Enter Balance : "))
            else:
                print("Pin doest not match....Register Again !!")    
        cursor.execute("INSERT INTO test (username,pin,balance) VALUES (%s,%s,%s)",(username,pin,balance))
        conn.commit()
        print("Welcome to ABC ATM System",username,"Your Account balance is :",balance)
        print("Select Service : ")
        b = int(input("To Withdraw Money Select 1 or To Get Balance Select 2 : "))
        if b == 1:
            money = int(input("Enter Amount to Withdraw in multiple of 100 or 1000 only : "))
            userpin = getpass.getpass("Enter Pin : ")
            if userpin == pin:
                if money <= balance :
                    if money%100==0 and money < 1000 :
                        notes = int(money/100)
                        balance = balance - money 
                        print("Amount of Rs",money,"Withdrawn Successfully...! ")
                        print("You Got Cash as : ")
                        print("Notes of Rs 100 : ",notes)
                        print("Remaining balance is : ",balance )
                        try:
                            cursor.execute("UPDATE test SET balance=%s WHERE username=%s",(balance,username))
                            conn.commit()
                        except Exception as err:
                            print("Error is :",err)
                    elif money%100==0 and money > 1000 :
                        notes = money/1000
                        balance = balance - money 
                        print("Amount of Rs",money,"Withdrawn Successfully...! ")
                        knotes = int(notes)
                        print("Yot Got Cash as : ")
                        print("Notes of 1000 : ",knotes)
                        notes = str(notes).split('.')[1]
                        print("Notes of 100  : ",notes)
                        print("Remaining balance is : ",balance )
                        try:
                            cursor.execute("UPDATE test SET balance=%s WHERE username=%s",(balance,username))
                            conn.commit()
                        except Exception as err:
                            print("Error is :",err)
                    else:
                        print("Cannot Dispense Cash")    
                else:
                    print("Insufficient Balance")   
            else :
                print("Enter Correct Pin") 
        elif b == 2:
            print("Balance is Rs : ",balance)
        else :
                print("Please Select Correct Option")
            
    except Exception as err:
        print("Error is : ",err)
    finally:
        cursor.close()
        conn.close()
 
def existinguser():
    userinput = input("Enter username to Search :")
    userpin = getpass.getpass("Enter Pin")
    conn = psycopg2.connect("dbname=abc user=postgres password=postgre")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username,balance from test WHERE username=%s AND pin=%s",(userinput,userpin))
        row = cursor.fetchall()
        try:
                for r in row:
                    print("Welcome",r[0])
                    print("Your Account Balance is",r[1])
                username = r[0]    
                balance = int(r[1])
                print("Select Service : ")
                b = int(input("To Withdraw Money Select 1 or To Get Balance Select 2 or 3 to Add Cash: "))
                if b == 1:
                    money = int(input("Enter Amount to Withdraw in multiple of 100 or 1000 only : "))
                    if money <= balance :
                            if money%100==0 and money < 1000 :
                                notes = int(money/100)
                                balance = balance - money 
                                print("Amount of Rs",money,"Withdrawn Successfully...! ")
                                print("You Got Cash as : ")
                                print("Notes of Rs 100 : ",notes)
                                print("Remaining balance is : ",balance )
                                try:
                                    cursor.execute("UPDATE test SET balance=%s WHERE username=%s",(balance,username))
                                    conn.commit()
                                except Exception as err:
                                    print("Error is :",err)    
                            elif money%100==0 and money > 1000 :
                                notes = money/1000
                                balance = balance - money 
                                print("Amount of Rs",money,"Withdrawn Successfully...! ")
                                knotes = int(notes)
                                print("Yot Got Cash as : ")
                                print("Notes of 1000 : ",knotes)
                                notes = str(notes).split('.')[1]
                                
                                if int(notes)>0:
                                    print("Notes of 100  : ",notes)
                                else:
                                    pass    
                                print("Remaining balance is : ",balance )
                                cursor.execute("UPDATE test SET balance=%s WHERE username=%s",(balance,username))
                                conn.commit()
                            else:
                                print("Cannot Dispense Cash")    
                    else:
                        print("Insufficient Balance")   
                elif b == 2:
                    print("Balance is Rs : ",balance)
                elif b==3:
                    addcash = int(input("Enter Amount to Add"))
                    balance = balance + addcash                    
                    try:
                        cursor.execute("UPDATE test SET balance=%s WHERE username=%s",(balance,username))
                        conn.commit()
                        print("Amount of Rs",addcash,"addedd Successfully...!!")
                    except Exception as err:
                        print("Error is Addcash:",err)
                else :
                        print("Please Select Correct Option")
                    
        except :
                 print("Wrong Pin") 
    except Exception as err:
        print("Erros is last line : ",err)     
                       
    finally:
            cursor.close()
            conn.close()    
               
print("Welcome to ABC ATM System")
a = int(input("Are You new here ? Press 1 for New User Press 2 for Existing User : "))
if a == 1:
    newuser()
elif a == 2:
    existinguser()
else : 
    print("Wrong Input")
    

print("Thank You for using ABC ATM System")     


       
