import datetime


def load_laptop_data(file_name):
    """Load laptop data from a text file and return it as a list of lists"""
    with open(file_name, 'r') as file:
        laptop_data = [line.strip().split(', ') for line in file.readlines()]
    return laptop_data


def display_laptops(laptop_data):
    """Display the available laptops to the user"""
    print('Available Laptops:')
    for laptop in laptop_data:
        print(f"{laptop[0]} | {laptop[1]} | {laptop[2]} | {laptop[3]} | {laptop[4]} | {laptop[5]} | {laptop[6]}")


def get_user_choice(laptop_data):
    """Get the user's choice of laptop and quantity"""
    while True:
        user_choice = input('Enter the name of the laptop you want to order: ')
        user_quantity = int(input('Enter the quantity you want to order: '))
        for laptop in laptop_data:
            if laptop[1] == user_choice:
                if int(laptop[4]) >= user_quantity:
                    return laptop, user_quantity
                else:
                    print('Amount not in stock')
                    break
        else:
            print('Invalid laptop name')


def create_invoice(laptop, quantity):
    """Create an invoice and save it to a text file"""
    customer_name = input('Enter your name: ')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    invoice_data = f"SN: {laptop[0]}\nName: {laptop[1]}\nBrand: {laptop[2]}\nPrice: ${laptop[3]}\nQuantity: {quantity}\nCustomer Name: {customer_name}\nDate: {current_time}"
    with open('invoice.txt', 'w') as file:
        file.write(invoice_data)
    print(f"Invoice saved to 'invoice.txt'")


# Load the laptop data
laptop_data = load_laptop_data('laptop_data.txt')

# Display the available laptops to the user
display_laptops(laptop_data)

# Get the user's choice of laptop and quantity
chosen_laptop, order_quantity = get_user_choice(laptop_data)

# Create an invoice and save it to a text file
create_invoice(chosen_laptop, order_quantity)
