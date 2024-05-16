
from ct_test_example import *

def test():	
	while True:
		print("Please choose a test to proceed: ")
		print("1. test_1")
		print("2. test_2")
		print("3. test_3")
		print("q. Quit")
        
		choice = input("Enter your choice: ")
      
		if choice == '1':
			print("Please choose a phantom to scan: ")q
			print("1. pic_1")
			print("2. pic_2")
			print("3. pic_3")

			pic = float(input("Enter your choice: "))
			
			test_1(pic)

		elif choice == '2':
			print("Please choose a phantom to scan: ")
			print("1. pic_1")
			print("2. pic_2")
			print("3. pic_3")

			pic = float(input("Enter your choice: "))
			
			test_2(pic)
			
		elif choice == '3':
			print("Please choose a phantom to scan: ")
			print("1. pic_1")
			print("2. pic_2")
			print("3. pic_3")

			pic = float(input("Enter your choice: "))

			test_3(pic)
		elif choice == 'q' or choice == 'Q':
			print("Exiting...")
			break
		else:
			print("Invalid choice, please try again.")
            
	