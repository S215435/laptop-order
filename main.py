import datetime
import random


# Function to load laptops from the file
def load_laptops():
    laptops = []
    with open('laptops.txt', 'r') as file:
        for line in file:
            laptop_data = line.strip().split(',')
            laptops.append(laptop_data)
    return laptops


# Function to display laptops neatly
def display_laptops(laptops):
    print("Laptops available for sale:")
    print(f"{'SN':<5}{'Name':<15}{'Brand':<15}{'Price':<10}{'Quantity':<10}{'CPU':<20}{'GPU':<20}")
    for laptop in laptops:
        print(
            f"{laptop[0]:<5}{laptop[1]:<15}{laptop[2]:<15}${laptop[3]:<9}{laptop[4]:<10}{laptop[5]:<20}{laptop[6]:<20}")


# Function to create an invoice for restocking
def create_restock_invoice(laptop, distributor_name, quantity):
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    net_amount = float(laptop[3]) * quantity
    vat = net_amount * 0.13
    total_amount = net_amount + vat
    invoice_data = [distributor_name, laptop[1], laptop[2], str(
        now), str(quantity), str(net_amount), str(vat), str(total_amount)]
    file_name = f"restock_invoice{distributor_name.lower()}{laptop[2].lower()}{date_time}.txt"
    with open(file_name, 'w') as file:
        file.write("Distributor Name: " + invoice_data[0] + "\n")
        file.write("Name: " + invoice_data[1] + "\n")
        file.write("Brand: " + invoice_data[2] + "\n")
        file.write("Date of Purchase: " + invoice_data[3] + "\n")
        file.write("Quantity: " + invoice_data[4] + "\n")
        file.write("Net Amount: $" + invoice_data[5] + "\n")
        file.write("VAT: $" + invoice_data[6] + "\n")
        file.write("Total Amount: $" + invoice_data[7] + "\n")


# Function to create an invoice for a customer purchase
def create_customer_invoice(laptop, customer_name, quantity):
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    total_amount = float(laptop[3]) * quantity
    shipping_cost = random.randint(300, 3000)
    total_cost = total_amount + shipping_cost
    invoice_data = [laptop[0], laptop[1], laptop[2], str(laptop[3]), str(
        quantity), customer_name, str(now), str(total_amount), str(shipping_cost), str(total_cost)]
    file_name = f"invoice_{customer_name.lower()}_{date_time}.txt"
    with open(file_name, 'w') as file:
        file.write("SN: " + invoice_data[0] + "\n")
        file.write("Name: " + invoice_data[1] + "\n")
        file.write("Brand: " + invoice_data[2] + "\n")
        file.write("Price: $" + invoice_data[3] + "\n")
        file.write("Quantity: " + invoice_data[4] + "\n")
        file.write("Customer Name: " + invoice_data[5] + "\n")
        file.write("Order Date: " + invoice_data[6] + "\n")
        file.write("Total Amount Without Shipping: $" + invoice_data[7] + "\n")
        file.write("Shipping Cost: $" + invoice_data[8] + "\n")
        file.write("Total Cost: $" + invoice_data[9] + "\n")
        print(f"Successfully created invoice for {customer_name}!")


# to update laptop amount (event trigger: restock/sales) in laptops.txt file
# Function to update the quantity of a laptop
def update_laptop_amount(sn, new_amount):
    laptops = load_laptops()
    updated_laptops = []
    for laptop in laptops:
        if laptop[0] == sn:
            laptop[4] = str(int(new_amount))
        updated_laptops.append(laptop)
    with open('laptops.txt', 'w') as file:
        for laptop in updated_laptops:
            file.write(','.join(laptop) + '\n')
    print(f"Successfully updated the quantity of laptop with SN: {sn}")


def start():
    laptops = load_laptops()
    display_laptops(laptops)

    while True:
        sn = input(
            "Enter the SN of the laptop you want to purchase (or 'q' to quit): ")
        if sn.lower() == 'q':
            break

        found_laptop = None
        for laptop in laptops:
            if laptop[0] == sn:
                found_laptop = laptop
                break

        if found_laptop is None:
            print("Invalid SN, please try again.")
            continue

        quantity = int(input("Enter the quantity you want to purchase: "))
        if quantity <= 0:
            print("Invalid quantity, please try again.")
            continue

        # if customers' order cannot be filled then make purchase of twice the amount of laptop from manufacturer
        # half amount will fullfill users purchase order, rest will be restocked
        if quantity > int(found_laptop[4]):
            make_purchase = 2*(quantity - int(found_laptop[4]))
            # update the laptops amount from the laptops.txt
            update_laptop_amount(sn, make_purchase/2)
            # create restock invoice
            create_restock_invoice(
                found_laptop, 'distributor x', make_purchase)
            customer_name = input("Enter your name: ")
            create_customer_invoice(found_laptop, customer_name, quantity)
            print("Thank you for your purchase!")
            break

        customer_name = input("Enter your name: ")
        create_customer_invoice(found_laptop, customer_name, quantity)
        # update the laptops amount from the laptops.txt
        update_laptop_amount(sn, quantity - int(found_laptop[4]))
        print("Thank you for your purchase!")
        break


if __name__ == "__main__":
    start()
