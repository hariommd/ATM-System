import getpass
import psycopg2
import time

def newuser():
    conn = psycopg2.connect("dbname=abc user=postgres password=postgres")
    cursor = conn.cursor()
    username = input("Enter Your Name : ")
    cursor.execute("SELECT username from test WHERE username=%s",(username,))
    row = cursor.fetchall()
    if len(row)>0:
        print("Username exist")
    else:
        pin = getpass.getpass("Enter 4 Digit Pin for ATM : ")
        if len(pin)!=4:    
            print("Pleasse Proivde Correct Pin")    
        else:   
            cnfpin = getpass.getpass("Enter Pin Again : ")
            if pin == cnfpin :
                balance = int(input("Enter Balance : "))
            else:
                print("Pin doest not match....Register Again !!")    
        cursor.execute("INSERT INTO test (username,pin,balance) VALUES (%s,%s,%s)",(username,pin,balance))
        conn.commit()
        cursor.execute("SELECT username,balance,accno from test where username=%s",(username,))
        row = cursor.fetchall()
        for r in row:
            print("Welcome Mr.",r[0],)
            print("Your Account No is :",r[2],)
            print("Your Balance is :",r[1],)

        print("Select Service : ")
        b = int(input("1-Withdraw Money 2-Get Balance 3-Add Cash :"))
        if b == 1:
            transaction = "Withdrawl"
            date = time.strftime('%Y-%m-%d %H:%M:%S')
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
                            cursor.execute("INSERT INTO test1 (username,transaction,date,amount) VALUES (%s,%s,%s,%s)",(username,transaction,date,money,))
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
                        try:
                            cursor.execute("INSERT INTO test1 (username,transaction,date,amount) VALUES (%s,%s,%s,%s)",(username,transaction,date,money,))
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
        elif b == 3:
            transaction = "Credit"
            date = time.strftime('%Y-%m-%d %H:%M:%S')
            addcash = int(input("Enter Amount to Add"))
            balance = balance + addcash                    
            try:
                cursor.execute("INSERT INTO test1 (username,transaction,date,amount) VALUES (%s,%s,%s,%s)",(username,transaction,date,addcash,))
                cursor.execute("UPDATE test SET balance=%s WHERE username=%s",(balance,username))
                conn.commit()
                print("Amount of Rs",addcash,"addedd Successfully...!!")
            except Exception as err:
                print("Error is Addcash:",err)
        
        else :
            print("Please Select Correct Option")
    cursor.close()
    conn.close()
 
def existinguser():
    try:
        conn = psycopg2.connect("dbname=abc user=postgres password=postgres")
        cursor = conn.cursor()
        userinput = input("Enter username to Search :")
        cursor.execute("SELECT username from test WHERE username=%s",(userinput,))
        row = cursor.fetchall()
        if len(row)==0:
            print("Username does not exist")
        else:
            userpin = getpass.getpass("Enter Pin")
            conn = psycopg2.connect("dbname=abc user=postgres password=postgres")
            cursor = conn.cursor()
            
            cursor.execute("SELECT username,balance,accno from test WHERE username=%s AND pin=%s",(userinput,userpin))
            row = cursor.fetchall()
            while len(row)==0:
                attempt = 2
                while attempt >=1:
                    print("Wrong Pin Entered...Attempt Left",attempt)
                    userpin = getpass.getpass("Enter Pin")
                    cursor.execute("SELECT username,balance,accno from test WHERE username=%s AND pin=%s",(userinput,userpin))
                    row = cursor.fetchall()
                    if len(row)==0:
                        attempt = attempt-1
                    else:
                        break   
                else :
                    print("Attempt Exceeded")    
                    break
            else:

                print("Pin Accepted Logging You into system please wait...!!")    
                for r in row:
                            print("Welcome Mr.",r[0])
                            print("Your Account Number is  :",r[2])
                            print("Your Account Balance is Rs",r[1])
                username = r[0]    
                balance = int(r[1])
                date = time.strftime('%Y-%m-%d %H:%M:%S')
                print("Select Service : ")
                b = int(input("1-Withdraw Money 2-Get Balance 3-Add Cash 4-View Past Transactions: "))
                if b == 1:
                    transaction = "Withdrawl"
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
                                    cursor.execute("INSERT INTO test1 (username,transaction,date,amount) VALUES (%s,%s,%s,%s)",(username,transaction,date,money,))
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
                                cursor.execute("INSERT INTO test1 (username,transaction,date,amount) VALUES (%s,%s,%s,%s)",(username,transaction,date,money,))
                                cursor.execute("UPDATE test SET balance=%s WHERE username=%s",(balance,username))
                                conn.commit()
                            else:
                                print("Cannot Dispense Cash")    
                    else:
                        print("Insufficient Balance")   
                elif b == 2:
                    print("Balance is Rs : ",balance)
                elif b==3:
                    transaction = "Credit"
                    date = time.strftime('%Y-%m-%d %H:%M:%S')
                    addcash = int(input("Enter Amount to Add :"))
                    balance = balance + addcash                    
                    try:
                        cursor.execute("INSERT INTO test1 (username,transaction,date,amount) VALUES (%s,%s,%s,%s)",(username,transaction,date,addcash,))
                        cursor.execute("UPDATE test SET balance=%s WHERE username=%s",(balance,username))
                        conn.commit()
                        print("Amount of Rs",addcash,"addedd Successfully...!!")
                    except Exception as err:
                        print("Error is Addcash:",err)
                elif b==4:
                    cursor.execute("SELECT username,transaction,date,amount from test1 WHERE username=%s",(username,))
                    row = cursor.fetchall()
                    if len(row)>0:
                        print("Transaction Details :")
                        print ("    Date    Type      Amount")
                        for r in row:
                            print(r[2],r[1],r[3],)
                    else:
                        print("No Transactions Found")        
                else :
                        print("Please Select Correct Option")
            
            
    finally:
            cursor.close()
            conn.close()    
               
print("Welcome to ABC ATM ")
a = int(input("Are You new here ? Press 1 for New User Press 2 for Existing User : "))
if a == 1:
    newuser()
elif a == 2:
    existinguser()
else : 
    print("Wrong Input")
    

print("Thank You for using ABC ATM")     


       
