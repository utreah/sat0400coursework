import time
import os 
import random
# TO DO LIST: 

# [WIP?] MAKE A TEST TABLE AND SEND IT WITH COURSEWORK -> NOT STARTED YET
# [WIP] 
# [DONE] converting between data types.
# [DONE] Customer Food/Drink append method completely changed.
# [DONE] Coupon apply method completely changed and old version has been commented (for future references)
# [DONE] ADD while loop to customer_coupon_answer so if the customer types something different than y/n, they'll have another chance (maybe we can add a limit like max 3 attempts)
# [DONE] FINISH VALIDITYCHECKS FOR NAME -> NOT STARTED AT ALL <- 4 days later "DONE"
# [DONE] MERGE CUSTOMERPAYMENTPAGE AND COUPON FUNCTION. MAKE THEM WORK TOGETHER -> ALMOST DONE, NEED TO CODE SMT TO CHECK MONTH AND DAY CHECK FOR CARD PAYMENTS <- "DONE"
# [SOLVED] CHANGE WHILE LOOP (AT LEAST ONE OF THEM MUST HAVE A CONDITION) - "SOLVED" -> now, the first while loop has a condition to exit.
# [SOLVED] CHECK ADJUST PRICE AND ITEM REMOVE FUNCTIONS. SMT WRONG WITH ADJUST PRICE. DOESN'T DELETE THE PRICE PROPERLY(%50 OF THE CASES) -> "SOLVED", total_price has been moved inside the loop. It wasn't being updated after adjustPrice function
# [SOLVED] It applies discount, changing total_price but the first line of the while loop rewrites the original price back. -> total price adjuster has been moved outside the while loop, now prices are being updated every time a customer adds/removes an item.
# [SOLVED] Another problem related to remove/add item function. "SOLVED" -> Removes the first item that the function encounters, then updates the price | SHOULD BE FIXED :(


selected_items = []
selected_items_total_price = []
price_list = [5.95, 6.95, 4.95, 2.00, 2.50, 2.10, 6.80, 7.10, 5.43]
menuArr = ["Croissant", "Chicken Mayo Sandwich","Poached Eggs with Avocado","Orange Juice","Capuccino","Flat White","Corona Bottle","Moretti Pint","Guinness Pint" ]
age_restirected_items = ["Corona Bottle","Moretti Pint","Guiness Pint"]
credit_card_day_check = [31,28,31,30,31,30,31,31,30,31,30,31]
credit_card_month_check = [1,2,3,4,5,6,7,8,9,10,11,12]
# customer_basket_totalPrice = 0
def is_valid_name(customer_name):
    name_check = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$', '%', '^', '&', '*', '_']
    for char in customer_name:
        if char in name_check:
            return False  # Name contains a symbol or number
    return True  # Name is valid
        
def customer_printMenu():

##    beer_random_id1 = random.randint(0,2) # assign a new id everytime it prints the menu between the range to avoid people <18 to order alcoholic beverages. 
##    beer_random_id2 = random.randint(2,4) # as of 21.11.23 this has no use as I changed my append food/drink method and added age restirected item check.
##    beer_random_id3 = random.randint(4,6)
    print("|---------------------------------------------|")
    print("\t\t Food Menu")
    print(f"|->\n 1-Croissant {price_list[0]}£ \n 2-Chicken Mayo Sandwich {price_list[1]}£ \n 3-Poached Eggs with Avocado {price_list[2]}£ ")
    print("|---------------------------------------------|")
    print("\t\t Drink Menu")
    print(f"|->\n 4-Orange Juice {price_list[3]}£\n 5-Capuccino {price_list[4]}£\n 6-Flat White {price_list[5]}£")
    print("|---------------------------------------------|")
    print("\t\t Alcohol Menu")
    print("NOTE: This section has age restirictions. If you are not 18 or above you CAN NOT order beverages contains ALCOHOL!")
    print(f"|->\n 7-Corona Bottle {price_list[6]}£\n 8-Moretti Pint {price_list[7]}£\n 9-Guiness Pint {price_list[8]}£")

def customer_appendChoices(customer_item_choices, customer_age):
    if len(customer_item_choices) < 4: # If item name is less than 4 characters, it will return false -> This check was added to prevent adding different products containing the same letters.
        print("Use atleast 4 or more characters!")
        return False # returns false so customer can keep adding new item(s)
    item_found = False
    for itemNameToAppend, price in zip(menuArr, price_list):
        if customer_item_choices.lower() in itemNameToAppend.lower():
            age_restricted = False # flag for age restirected items 
            for restirectedItemCheck in age_restirected_items:
                if customer_age < 18 and customer_item_choices.lower() in restirectedItemCheck.lower():
                    print("Age restricted item. It cannot be added to the basket.")
                    age_restricted = True # if the item is age restricted raise the flag
                    break  # No need to continue checking other restricted items
            if not age_restricted: # If no flag 
                selected_items.append(itemNameToAppend) # append food name
                selected_items_total_price.append(price) # append Its price
                item_found = True
    if not item_found:
        print(f"Item ''{customer_item_choices}'' cannot be found. Please check your spelling or make sure that item is on the menu!")

def print_customer_basket(selected_items,selected_items_total_price):
    seenFood = set()
    customer_basket_totalPrice = 0
    print("Products in your basket:")
    for orderCounter,price in zip(selected_items,selected_items_total_price): #loops through 2 array.
        if orderCounter not in seenFood: #if that food/drink hasn't been counted/added to seenFood list.
            foodCounter = selected_items.count(orderCounter) # count number of the food/drink and save it to foodCounter.
            print(f"{orderCounter} x{foodCounter}: {price*foodCounter}£") # prints everything we found
            seenFood.add(orderCounter) # adds it to seenFood list so we wont count it more than one
            customer_basket_totalPrice += price
    
def customer_basket_total_price(selected_items_total_price):
    customer_basket_totalPrice = 0
    for price in selected_items_total_price: #loops through 2 array.
            customer_basket_totalPrice += price # sums up the numbers in selected_items_total_price
    # total_price = customer_basket_totalPrice -> found a better solution, I may use it later so I'll keep it
    return customer_basket_totalPrice

def customer_removeItem(itemToRemove, selected_items, selected_items_total_price):
    item_found = False  # Flag to check if the item was found
    for item in selected_items:
        if itemToRemove.lower() in item.lower():
            selected_items.remove(item)
            customer_adjustPrice(item, selected_items_total_price)
            item_found = True
            break

    if not item_found:
        print(f"Item '{itemToRemove}' could not be found! Please make sure you are using correct spelling!")

def customer_adjustPrice(removeItem_from_Basket, selected_items_total_price):
    # menuArr = ["Croissant", "Chicken Mayo Sandwich", "Poached Eggs with Avocado", "Orange Juice",
    #             "Capuccino", "Flat White", "Corona Bottle", "Moretti Pint", "Guinness Pint"]
    priceArr = [5.95, 6.95, 4.95, 2.00, 2.50, 2.10, 6.80, 7.10, 5.43]
    indexOf_item_to_remove = menuArr.index(removeItem_from_Basket) # find index of the item in menuArr
    removed_price = priceArr[indexOf_item_to_remove] # assign the index to removed_price variable
    if removed_price in selected_items_total_price: # if removed price is present in the specified array
        selected_items_total_price.remove(removed_price) # remove
    else:
        print("Error: Price not found for the removed item.") # if not print error or pass

def customer_applyCoupon(customerCoupon,total_price_discounted_by_coupon):
    couponList = ["MDX10","MDX25","MDX50"]
    couponDiscountPercantage = [10/100,25/100,50/100]
    if customerCoupon in couponList:
        indexOf_coupon_to_apply = couponList.index(customerCoupon)
        print(f"Coupon {customerCoupon} has been validated and applied on Basket Amount.") 
        return total_price_discounted_by_coupon-(total_price_discounted_by_coupon*couponDiscountPercantage[indexOf_coupon_to_apply])
    #for validCoupon in couponList: # loops through coupon list
    #if customerCoupon == couponList[0]:
    #    print(f"Coupon '{couponList[0]}' has been validated and applied to total price!")
    #   return total_price_discounted_by_coupon-(total_price_discounted_by_coupon*10/100)
    #elif customerCoupon == couponList[1]:
    #    print(f"Coupon '{couponList[1]}' has been validated and applied to total price!")
    #    return total_price_discounted_by_coupon-(total_price_discounted_by_coupon*25/100)
    #elif customerCoupon == couponList[2]:
    #    print(f"Coupon '{couponList[2]}' has been validated and applied to total price!")
    #    return total_price_discounted_by_coupon-(total_price_discounted_by_coupon*50/100)
    else:
        print("Coupon could not be applied! Original price has been returned")
        return total_price_discounted_by_coupon
                
def customer_payment_page(total_price): # NOTE to REVIEWER: JUST USE SOME RANDOM NUMBERS IT WILL ACCEPT ANYWAY ( I'll add some checks for date tho ) <- "DONE"
    print(f"Amount that needs to be paid : {total_price}£")
    customer_coupon_answer_attempts = 0
    while customer_coupon_answer_attempts < 3:
        if customer_coupon_answer_attempts != 0:
            print("Attempts Left: ",3-customer_coupon_answer_attempts)
        customer_coupon_answer = input("Do you have a coupon?(y/n) : ")
        if "y" in customer_coupon_answer or "yes" in customer_coupon_answer or "Yes" in customer_coupon_answer:
            customerCoupon = str(input("Can I have the coupon please? :"))
            total_price_new_discounted = customer_applyCoupon(customerCoupon,total_price)
            print(f"New amount: {round(total_price_new_discounted,2)}£")
            break
        elif "n" in customer_coupon_answer or "no" in customer_coupon_answer or "No" in customer_coupon_answer:
            total_price_new_discounted = total_price
            print("No coupon has been applied! You are being redirected to payment area")
            break
        else:
            print("Invalid input")
            customer_coupon_answer_attempts += 1
            if customer_coupon_answer_attempts >= 3:
                print("You are being redirected to payment page!")
                break
    customer_payment_way = input("How would you like to pay?\n1-Credit/Debit Card\n2-Cash\nChoice:")

    if "1" in customer_payment_way or "card" in customer_payment_way.lower():  # Use lower() to make the comparison case-insensitive
        customer_card_16_digit_number = input("Please provide your 16 digit credit card number: ")

        if len(customer_card_16_digit_number) != 16 or not customer_card_16_digit_number.isdigit():
            print("Card Number should be a 16-digit number. Current length:", len(customer_card_16_digit_number))
        
            while len(customer_card_16_digit_number) != 16 or not customer_card_16_digit_number.isdigit():
                customer_card_16_digit_number = input("Please provide your 16 digit credit card number: ")

        customer_card_cvc_number = input("Please provide your CVC: ")
    
        if len(customer_card_cvc_number) != 3 or not customer_card_cvc_number.isdigit():
            print("CVC information should be a 3-digit number.")
        
            while len(customer_card_cvc_number) != 3 or not customer_card_cvc_number.isdigit():
                customer_card_cvc_number = input("Please provide your CVC: ")

##        customer_card_valid_date = str(input("Please provide your valid date as the following format (ddmm): ")) 

        # Validate the date format
        while True:
            customer_card_valid_date = str(input("Please provide your valid date in the format (ddmm): "))

            if len(customer_card_valid_date) == 4 and customer_card_valid_date.isdigit():
                customer_card_valid_date_dd = int(customer_card_valid_date[:2])
                customer_card_valid_date_mm = int(customer_card_valid_date[2:])
        
        # Validate month and day
                if 1 <= customer_card_valid_date_mm <= 12 and 1 <= customer_card_valid_date_dd <= 31:
                    print("Payment has been processed! Have a nice day!")
                    break
                else:
                    print("Invalid month or day in the date. Please try again.")
            else:
                print("Invalid date format. Please provide the date in the format (ddmm).")

        

    # Add the case for cash payment (too lazy to do anything so this WILL NEED TO do the work)
    elif "2" in customer_payment_way:
        print("Payment by cash selected.")
        print("Customer has been paid. Have a nice day!")
    else:
        print("Invalid payment choice.")
        

    
total_price = 0
customer_name = str(input("Name : "))
is_valid = False
while is_valid != True:
    if is_valid_name(customer_name):
        print("Hello "+customer_name,"Welcome to our Cafe!")
        break
    else:
        customer_name=input("Invalid name. Name should not contain symbols or numbers.\nPlease enter your name again. :")
    
customer_age = int(input("I need to know your age to show our menu. How old are you? : "))
print("Okay ",customer_name,"you are ",customer_age," years old.")
print("Menu will be printed in 5 seconds and this screen will be cleared!")
time.sleep(5)
os.system("clear||cls")
customer_printMenu()

while_dummy_variable = "x" # dont mind it just some dummy variable that I created for while loop
QUIT_KEY = "q" # handsome quit_key #define QUIT_KEY "q" ??

while while_dummy_variable != QUIT_KEY:
        customer_Take_Order = input("What would you like to order? (Type 'q' to quit): ")
        while_dummy_variable = customer_Take_Order
        #if customer_Take_Order == 'q':
        #    break
        customer_appendChoices(customer_Take_Order, customer_age)
total_price = customer_basket_total_price(selected_items_total_price)
while True:
    customer_menu_choice = int(input("Choose one of the following\n1-Print Items in the basket and total price \n2-Remove Item\n3-Add Item\n4-Payment/Discount Page\nChoice: "))
    if customer_menu_choice == 1:
        os.system("clear||cls")
        print_customer_basket(selected_items,selected_items_total_price)
        print(f"Total Price: {total_price}£")
        total_price = customer_basket_total_price(selected_items_total_price)
    elif customer_menu_choice == 2:
        print_customer_basket(selected_items,selected_items_total_price)
        itemtoRemove = str(input("Which Item would you like to remove? : "))
        customer_removeItem(itemtoRemove,selected_items,selected_items_total_price)
        total_price = customer_basket_total_price(selected_items_total_price)
       # customer_adjustPrice(itemtoRemove, selected_items_total_price) <- doesn't work(need to rewrite whole adjustPrice function to make this work)UPDATE:problem solved without rewriting the whole function. Will keep it for test case(s)
    elif customer_menu_choice == 3:
        while True:
            customer_Take_Order = input("What would you like to order? (Type 'q' to quit): ")
            if customer_Take_Order == 'q':
                break
            customer_appendChoices(customer_Take_Order, customer_age)
        total_price = customer_basket_total_price(selected_items_total_price)
##    elif customer_menu_choice == 4: # will be merged with option 5
##        customerCoupon = (input("Please provide your coupon code: "))
##        totalPrice_after_discount = customer_applyCoupon(customerCoupon,total_price)
##        print(f"Original Price : {total_price}£ Discounted Price : {totalPrice_after_discount}£")
##        total_price = totalPrice_after_discount
    elif customer_menu_choice == 4:
        print("Notice! You can validate your coupon in the payment page(if you have one)")
        print("You are being redirected in 3 seconds, please wait.")
        time.sleep(3)
        os.system("clear||cls")
        customer_payment_page(total_price)
    else:
        print("Invalid choice!")
