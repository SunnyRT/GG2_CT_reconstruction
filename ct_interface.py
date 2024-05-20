
from ct_test_example import *

def test():	
	while True:
		print("Please choose a test to proceed: ")
		print("1. test_1(plot)")
		print("2. test_2(mean value)")
		print("3. test_3(variance of specific materials)")
		print("q. Quit")
        
		choice = input("Enter your choice: ")
      
		if choice == '1':
			print("Please choose a phantom to scan: ")
			print("1. pic_1")
			print("2. pic_2")
			print("3. pic_3")

			pic = float(input("Enter your choice: "))
			
			test_1(pic)

		elif choice == '2':
		# 	print("Please choose a phantom to scan: ")
		# 	print("1. pic_1")
		# 	print("2. pic_2")
		# 	print("3. pic_3")

		# 	pic = float(input("Enter your choice: "))
			
			test_2()
			
		elif choice == '3':
			print("Please choose a phantom to scan: ")
			print("1. pic_1")
			print("2. pic_2")
			print("3. pic_3")

			pic = float(input("Enter your choice: "))

			print("Please choose a source of photons: ")
		
			# Mapping dictionary
			input_map = {
				1: "100kVp, 1mm Al",
				2: "100kVp, 2mm Al",
				3: "100kVp, 3mm Al",
				4: "100kVp, 4mm Al",
				5: "80kVp, 1mm Al",
				6: "80kVp, 2mm Al",
				7: "80kVp, 3mm Al",
				8: "80kVp, 4mm Al"
			}

			def get_string(input_value):
				return input_map.get(input_value, "Invalid input")

			# Print options for the user
			print("Please choose a source of photons: ")
			print("1. 100kVp, 1mm Al")
			print("2. 100kVp, 2mm Al")
			print("3. 100kVp, 3mm Al")
			print("4. 100kVp, 4mm Al")
			print("5. 80kVp, 1mm Al")
			print("6. 80kVp, 2mm Al")
			print("7. 80kVp, 3mm Al")
			print("8. 80kVp, 4mm Al")

			# Get user input
			source_input = int(input("Enter your choice: "))

			# Get the corresponding string from the map
			source = get_string(source_input)

			if source == "Invalid input":
				print("Invalid input. Please enter a number between 1 and 8.")
			else:
				# Pass the source_string to the test_3 function
				# Assuming pic is defined elsewhere in your code
				test_3(pic, source)

		elif choice == 'q' or choice == 'Q':
			print("Exiting...")
			break
		else:
			print("Invalid choice, please try again.")
            
	