import json
import matplotlib.pyplot as plt
import bcrypt
import tkinter as tk
from tkinter import ttk



class TextFormatting:
    # Text styles
    RESET = "\033[0m"  # Reset all formatting
    BOLD = "\033[1m"   # Bold text
    UNDERLINE = "\033[4m"  # Underline text

    # Text colors
    RED = "\033[91m"   # Red text
    GREEN = "\033[92m"  # Green text
    YELLOW = "\033[93m"  # Yellow text
    BLUE = "\033[94m"    # Blue text


class Menu:
   def __init__(self,menu_file,order_file,sale_file,user_file):
       
       self.menu_file=menu_file
       self.order_file=order_file
       self.sale_file=sale_file
       self.user_file=user_file
       self.items=self.load_menu_from_file()
   
#    to display all dishes
   def load_menu_from_file(self):
      try:
         with open(self.menu_file,"r") as file:
            menu_data=json.load(file)
            return menu_data
      except FileNotFoundError:
         return []
#    get orderdata
   def load_orderdata_from_file(self):
       try:
         with open(self.order_file,"r") as file:
            order_data=json.load(file)
            return order_data
       except FileNotFoundError:
         return []
       
#  to get saledata
   def load_saledata_from_file(self):
       try:
         with open(self.sale_file,"r") as file:
            sale_data=json.load(file)
            return sale_data
       except FileNotFoundError:
         return []
       
#    to getuserdata
   def load_userdata_from_file(self):
      try:
         with open(self.user_file,"r") as file:
            user_data=json.load(file)
            return user_data
      except FileNotFoundError:
        return []
   

#    to add adish to menu
   def addDish(self,item):
  
      itemdata=self.items["items"]
      id=None
      if itemdata==[]:
         id=1
      else:
         lastid=itemdata[len(itemdata)-1]["id"]
         id=lastid+1
        
      itemdata.append({"id":id,**item})

      with open(self.menu_file,"w") as file:
       json.dump(self.items,file)

      return "Dish added successfully."
#    to remove dish
   def removeDish(self,dish_id):
       itemdata=self.items["items"]
       removelist=[i for i in itemdata if i["id"]!=dish_id]
       self.items["items"]=removelist
       with open(self.menu_file,"w") as file:
            json.dump(self.items,file)
       formatted_string = f"{TextFormatting.GREEN}{TextFormatting.BOLD} Dish removed successfully.{TextFormatting.RESET}"
       return formatted_string 
   
#     to update dish
   def updateDish(self,dish_id,data):
       itemdata=self.items["items"]
       for i in itemdata:
           if i["id"]==dish_id:
               i.update(data)
               break       
       self.items["items"]=itemdata
       with open(self.menu_file,"w") as file:
         json.dump(self.items,file)
       
       formatted_string = f"{TextFormatting.GREEN}{TextFormatting.BOLD} Dish {TextFormatting.BLUE} {list(data.keys())[0]} updated successfully.{TextFormatting.RESET}"
       return formatted_string 
       
   
#    to take order  
   def takeOrder(self,dish_id,):
       orderfile=self.load_orderdata_from_file()
       orderdata=orderfile["orderdata"]
       id=None
       if orderdata==[]:
        id=1
       else:
         lastid=orderdata[len(orderdata)-1]["id"]
         id=lastid+1
        
       orderdata.append({"id":id,"dishid":dish_id,"orderstatus":"received"})
       orderfile["orderdata"]=orderdata
       with open(self.order_file,"w") as file:
        json.dump(orderfile,file)
       
       formatted_string = f"{TextFormatting.GREEN}{TextFormatting.BOLD} order received successfully. {TextFormatting.RESET}"
       return formatted_string
      
   
#   to change order status
   def changeOrderstatus(self,id,data):
      
      orderfile=self.load_orderdata_from_file()
      orderdata=orderfile["orderdata"]
      salefile=self.load_saledata_from_file()
      saledata=salefile["saledata"]
      menudata=self.items["items"]
      saledata_id:None
      if saledata==[]:
         saledata_id=1
      else:
         lastidofsaledata=saledata[len(saledata)-1]
         saledata_id=lastidofsaledata["id"]+1


      dish_id=None
      dish_name=None
      dish_price=None
      dish_caategory=None
      for i in orderdata:
           if i["id"]==id:
               i.update(data)
               dish_id=i["dishid"]
               break
       
      for i in menudata:
         if i["id"]==dish_id:
            dish_name=i["name"]
            dish_price=i['price']
            dish_caategory=i["category"]
         
      
      if data["orderstatus"]=="delivered":
           itemfount=False
           for i in saledata:
              if i["dishid"]==dish_id:
                 i["salecount"]+=1
                 i["saleamount"]=int(dish_price)*(i["salecount"])
                 itemfount=True
                 break
           if not itemfount:
              newitem={
                 "id":saledata_id,
                 "dishid":dish_id,
                 "name":dish_name,
                 "price":dish_price,
                 "category":dish_caategory,
                 "salecount":1,
                 "saleamount":dish_price
              }
              salefile["saledata"].append(newitem)

           with open(self.sale_file,"w") as file:
            json.dump(salefile,file)

      orderfile["orderdata"]=orderdata
      with open(self.order_file,"w") as file:
         json.dump(orderfile,file)
      
      formatted_string = f"{TextFormatting.GREEN}{TextFormatting.BOLD} order status changed to {TextFormatting.BLUE} {data['orderstatus']}. {TextFormatting.RESET}"
      return formatted_string
   
   
#  to show the sale data
   def showsaleData(self):
      salefile=self.load_saledata_from_file()
      saledata=salefile["saledata"]
      return saledata
#   to show the net sale  
   def showNetSale(self):
    salefile=self.load_saledata_from_file()
    saledata=salefile["saledata"]
    totalsaleamount=0
    for i in saledata:
       totalsaleamount +=int(i["saleamount"])
    
    return totalsaleamount
# saleanalytics
  

   def showsaleAnalytics(self):
    salefile = self.load_saledata_from_file()
    saledata = salefile["saledata"]

    snacksCount = 0
    beveragesCount = 0
    desertsCount = 0
    snacksAmount = 0
    beveragesAmount = 0
    desertsAmount = 0

    for i in saledata:
        if i["category"] == "snacks":
            snacksCount += int(i["salecount"])
            snacksAmount += int(i["saleamount"])
        elif i["category"] == "beverages":
            beveragesCount += int(i["salecount"])
            beveragesAmount += int(i["saleamount"])
        elif i["category"] == "desserts":
            desertsCount += int(i["salecount"])
            desertsAmount +=int(i["saleamount"])

    categories = ["snacks", "beverages", "desserts"]
    sale_count = [snacksCount, beveragesCount, desertsCount]
    sale_amount = [snacksAmount, beveragesAmount, desertsAmount]

    bar_width = 0.35
    index = range(len(categories))

    plt.bar(index, sale_count, bar_width, label='Sale Count', align='center', alpha=0.7)
    plt.bar([i + bar_width for i in index], sale_amount, bar_width, label='Sale Amount', align='center', alpha=0.7)

    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Sale Analytics')
    plt.xticks([i + bar_width / 2 for i in index], categories)
    plt.legend()
    
    # Add value labels on top of each bar
    for i in index:
        plt.text(i, sale_count[i] + 1, str(sale_count[i]), ha='center', va='bottom')
        plt.text(i + bar_width, sale_amount[i] + 1, str(sale_amount[i]), ha='center', va='bottom')

    return plt.show()

   




#  to show avilable dish
   def showAvailableDish(self):
       itemdata=self.items["items"]
       availabledish=[i for i in itemdata if i["available"]==True]
       return availabledish
   
#  to check valid id or not for order data
   def CheckIdValidforOrder(self,id):
       orderfile=self.load_orderdata_from_file()
       orderdata=orderfile["orderdata"]
       id_found=False
       for i in orderdata:
           if i["id"]==id:
               id_found=True
               break
       return id_found
   
#   to check valid id or not for available dish
   def CheckIdValidForAvaille(self,dish_id):
       itemdata=self.showAvailableDish()
       id_found=False
       for i in itemdata:
           if i["id"]==dish_id:
               id_found=True
               break
       return id_found

#   to check valid id or not
   def CheckIdValid(self,dish_id):
       itemdata=self.items["items"]
       id_found=False
       for i in itemdata:
           if i["id"]==dish_id:
               id_found=True
               break
       return id_found

class User:
   def __init__(self,username,password,role):
        self.username = username
        self.password = password
        self.role = role   

class Supplier(User):
   def __init__(self,username,password):
      super().__init__(username,password,"supplier")

class Cashier(User):
   def __init__(self, username, password):
      super().__init__(username, password,"cashier")













def destroy_all_widgets(parent_widget):
    for widget in parent_widget.winfo_children():
        widget.destroy()
username_entry=None
password_entry=None
def login():
    global username_entry,password_entry
    userfile=menu.load_userdata_from_file()
    userlist=userfile["users"]
    entered_username = username_entry.get()
    entered_password = password_entry.get()
   
    global user
    for i in userlist:
       if i["username"]==entered_username:
            entered_password_bytes=entered_password.encode('utf-8')
            retrived_password_bytes=i["password"].encode('utf-8')
            if bcrypt.checkpw(entered_password_bytes, retrived_password_bytes):
             user=i["role"]
             if user=="admin":
              show_menu_page()
             elif user=="supplier":
                show_menu_for_supplier()
             elif user=="cashier":
                show_menu_for_cashier()
    else:
        err_lable=tk.Label(root,text="Wronge credential")
        err_lable.pack()
        root.after(2000, err_lable.destroy)
       

def logout():
    destroy_all_widgets(root)
    global username_entry,password_entry
    username_label = tk.Label(root, text="Username:")
    username_entry = tk.Entry(root)
    password_label = tk.Label(root, text="Password:")
    password_entry = tk.Entry(root, show="*")  # Hide password characters
    login_button = tk.Button(root, text="Login", command=login)
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack()

   

def show_menu_page():
    # Clear the login page widgets
    destroy_all_widgets(root)
    logout_button = tk.Button(root, text="Logout" ,command=logout)
    logout_button.pack(anchor='ne')
    # Create widgets for the menu page
    role_lable=tk.Label(root,text=f"you are logined as {user}")
    menu_label = tk.Label(root, text="Welcome to the Menu Page")
    display_menu_button = tk.Button(root, text="Display Menu", command=display_menu)
    add_dish_button = tk.Button(root, text="Add  a Dish",command=add_dish)
    remove_dish_button = tk.Button(root, text="remove a Dish",command=remove_dish)
    update_dish_button = tk.Button(root, text="update a Dish",command=update_dish)
    view_saledata_button = tk.Button(root, text="view sale data",command=view_saledata)
    view_saleanalytics_button = tk.Button(root, text="view sale anaytics",command=view_saleAnalytics)
    add_staff_button = tk.Button(root, text="Add a staff", command=add_staff)
    

    menu_label.pack()
    role_lable.pack()
    display_menu_button.pack()
    add_dish_button.pack()
    remove_dish_button.pack()
    update_dish_button.pack()
    view_saledata_button.pack()
    view_saleanalytics_button.pack()
    add_staff_button.pack()

def show_menu_for_supplier():
    destroy_all_widgets(root)
    logout_button = tk.Button(root, text="Logout" ,command=logout)
    logout_button.pack(anchor='ne')
    # Create widgets for the menu page
    role_lable=tk.Label(root,text=f"you are logined as {user}")
    menu_label = tk.Label(root, text="Welcome to the Menu Page")
    take_order_button = tk.Button(root, text="take order", command=take_order)

    menu_label.pack()
    role_lable.pack()
    take_order_button.pack()

def show_menu_for_cashier():
    destroy_all_widgets(root)
    logout_button = tk.Button(root, text="Logout" ,command=logout)
    logout_button.pack(anchor='ne')
    # Create widgets for the menu page
    role_lable=tk.Label(root,text=f"you are logined as {user}")
    menu_label = tk.Label(root, text="Welcome to the Menu Page")
    update_order_status_button = tk.Button(root, text="update orderStatus", command=update_order_status)
    view_sale_data_button= tk.Button(root, text="view saledata", command=viewsale_data_for_cashier)

    menu_label.pack()
    role_lable.pack()
    update_order_status_button.pack()
    view_sale_data_button.pack()

def display_menu():
   # Call destroy_all_widgets to clear the show_menu_page
   destroy_all_widgets(root)

    
   previous_menu_button = tk.Button(root, text="go back",command=show_menu_page )
   previous_menu_button.pack(anchor='ne')
   datafile=menu.load_menu_from_file()
   datalist=datafile["items"]
   # Create a Frame to hold the table within the existing window
   menu_frame = tk.Frame(root)
   menu_frame.pack(fill="both", expand=True)
   
   # Create a Treeview widget to display the table
   tree = ttk.Treeview(menu_frame, columns=("ID", "Name", "Price", "Category", "Available"), show="headings")

   # Define column headings
   tree.heading("ID", text="ID")
   tree.heading("Name", text="Name")
   tree.heading("Price", text="Price")
   tree.heading("Category", text="Category")
   tree.heading("Available", text="Available")

   # Add data to the table
   for item in datalist:
       tree.insert("", "end", values=(item["id"], item["name"], item["price"], item["category"], item["available"]))

   # Pack the Treeview widget
   tree.pack(fill="both", expand=True)


# Define name_entry, price_entry, and category_entry as global variables
name_entry = None
price_entry = None
category_entry = None

def add_dish():
    destroy_all_widgets(root)
    previous_menu_button = tk.Button(root, text="go back", command=show_menu_page)
    previous_menu_button.pack(anchor='ne')

    global name_entry, price_entry, category_entry

    name_label = tk.Label(root, text="Dish name:")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    price_label = tk.Label(root, text="Dish price:")
    price_label.pack()
    price_entry = tk.Entry(root)
    price_entry.pack()

    category_label = tk.Label(root, text="Dish category (desserts/beverages/snacks):")
    category_label.pack()
    category_entry = tk.Entry(root)
    category_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=submit_dish)
    submit_button.pack()

def submit_dish():
    global name_entry, price_entry, category_entry

    name = name_entry.get()
    price = price_entry.get()
    category = category_entry.get()

    if name and price and category:
        try:
            price = int(price)
            # Check if category is one of the allowed categories
            if category in ["snacks", "beverages","desserts"]:
                dish = {
                    "name": name,
                    "price": price,
                    "category": category,
                    "available": False
                }
                menu.addDish(dish)
                msg_lable=tk.Label(root,text="Created successfully")
                msg_lable.pack()
            else:
                err_lable=tk.Label(root,text="invalid catogory")
                err_lable.pack()
                
        except ValueError:
            err_lable=tk.Label(root,text="invalid price input")
            err_lable.pack()

id_entry=None
def remove_dish():
   destroy_all_widgets(root)
   display_menu()
   dish_id=tk.Label(root,text="enter the id of dish to remove")
   global id_entry
   dish_id.pack()
   id_entry = tk.Entry(root)
   id_entry.pack()
   submit_button = tk.Button(root, text="Submit", command=submit_remove)
   submit_button.pack()


def submit_remove():
   global id_entry
   id=id_entry.get()
   try:
     id = int(id)
     menu.removeDish(id)
     msg_lable=tk.Label(root,text="Removed successfully")
     msg_lable.pack()
   except ValueError:
     err_lable=tk.Label(root,text="invalid id in put")
     err_lable.pack() 

update_id_entry=None
update_name_entry=None
update_price_entry=None
update_category_entry=None
update_available_entry=None


def update_dish():
   destroy_all_widgets(root)
   display_menu()
   global update_name_entry,update_price_entry,update_category_entry,update_available_entry,update_id_entry
   
   id_lable=tk.Label(root,text="enter id of the dish")
   id_lable.pack()
   update_id_entry=tk.Entry(root)
   update_id_entry.pack()

   name_lable=tk.Label(root,text="enter name of the dish")
   name_lable.pack()
   update_name_entry=tk.Entry(root)
   update_name_entry.pack()

   price_lable=tk.Label(root,text="enter price of the dish")
   price_lable.pack()
   update_price_entry=tk.Entry(root)
   update_price_entry.pack()

   category_lable=tk.Label(root,text="enter category of the dish snacks/beverages/desserts")
   category_lable.pack()
   update_category_entry=tk.Entry(root)
   update_category_entry.pack()

   available_lable=tk.Label(root,text="enter name of the dish  yes/no")
   available_lable.pack()
   update_available_entry=tk.Entry(root)
   update_available_entry.pack()

   submit_button = tk.Button(root, text="Submit", command=submit_update)
   submit_button.pack()

def submit_update():
   global update_name_entry,update_price_entry,update_category_entry,update_available_entry,update_id_entry
   
   name=update_name_entry.get()
   price=update_price_entry.get()
   category=update_category_entry.get()
   available=update_available_entry.get()
   id=update_id_entry.get()
   print(category)
   dish_obj={}
   if name:
      dish_obj["name"]=name

   if available:
       if available in ["yes","no"]:
         if available=="yes":
          dish_obj["available"]=True
         elif available=="no":
             dish_obj["available"]=False
       else:
        errr_lable=tk.Label(root,text="invalid id category")
        errr_lable.pack()

   if id:
     try:
       id = int(id)   
     except ValueError:
       err_lable=tk.Label(root,text="invalid id input")
       err_lable.pack() 

   if price:
     try:
       price = int(price) 
       dish_obj["price"]=price  
     except ValueError:
       err_lable=tk.Label(root,text="invalid price input")
       err_lable.pack() 
    
   if category:
      if category in ["snacks", "beverages","desserts"]:
         dish_obj["category"]=category
      else:
       errr_lable=tk.Label(root,text="invalid id category")
       errr_lable.pack()

   datafile=menu.load_menu_from_file()
   datalist=datafile["items"]
   
   is_id_present=False
   for i in datalist:
      if i["id"]==id:
         is_id_present=True
         break
   if is_id_present:
      print(dish_obj)
      menu.updateDish(id,dish_obj)
      msg_lable=tk.Label(root,text="updated successfully")
      msg_lable.pack()
      update_dish()

def view_saledata():
   destroy_all_widgets(root)
   previous_menu_button = tk.Button(root, text="go back",command=show_menu_page )
   previous_menu_button.pack(anchor='ne')
   datafile=menu.load_saledata_from_file()
   datalist=datafile["saledata"]
   # Create a Frame to hold the table within the existing window
   menu_frame = tk.Frame(root)
   menu_frame.pack(fill="both", expand=True)
   
   # Create a Treeview widget to display the table
   tree = ttk.Treeview(menu_frame, columns=("ID","Dish ID", "Name", "Price", "Category", "Sale Count","Sale Amount"), show="headings")

   # Define column headings
   tree.heading("ID", text="ID")
   tree.heading("Dish ID", text="Dish Id")
   tree.heading("Name", text="Name")
   tree.heading("Price", text="Price")
   tree.heading("Category", text="Category")
   tree.heading("Sale Count", text="Sale Count")
   tree.heading("Sale Amount", text="Sale Amount")

   # Add data to the table
   for item in datalist:
       tree.insert("", "end", values=(item["id"], item["dishid"],item["name"], item["price"], item["category"], item["salecount"],item["saleamount"]))

   # Pack the Treeview widget
   tree.pack(fill="both", expand=True)

def view_saleAnalytics():
    menu.showsaleAnalytics()

staff_role_entry=None
staff_username_entry=None
staff_password_entry=None

def add_staff():
   destroy_all_widgets(root)
   previous_menu_button = tk.Button(root, text="go back", command=show_menu_page)
   previous_menu_button.pack(anchor='ne')
   global staff_role_entry,staff_username_entry,staff_password_entry

   staff_username_lable=tk.Label(root,text="create username")
   staff_username_lable.pack()
   staff_username_entry=tk.Entry(root)
   staff_username_entry.pack()

   staff_password_lable=tk.Label(root,text="create password")
   staff_password_lable.pack()
   staff_password_entry=tk.Entry(root)
   staff_password_entry.pack()

   staff_role_lable=tk.Label(root,text="enter role supplier/cashier")
   staff_role_lable.pack()
   staff_role_entry=tk.Entry(root)
   staff_role_entry.pack()

   submit_button = tk.Button(root, text="Submit", command=submit_addstaff)
   submit_button.pack()

def submit_addstaff():
   global staff_role_entry,staff_username_entry,staff_password_entry

   role=staff_role_entry.get()
   username=staff_username_entry.get()
   password=staff_password_entry.get()

   userfile=menu.load_userdata_from_file()
   userlist=userfile["users"]
   lastUserId = userlist[-1]["id"]

   if role and username and password:
        if role in ["supplier","cashier"]:
           salt = bcrypt.gensalt() 
           password_bytes = password.encode('utf-8')
           hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
           hashed_password=hashed_password_bytes.decode('utf-8')
           if role=="supplier":
              supplier=Supplier(username,hashed_password)
              userlist.append({
              "id":lastUserId+1,
              "username":supplier.username,
              "password":supplier.password,
              "role":supplier.role
              })
              userfile["users"]=userlist
              with open(menu.user_file,"w") as file:
               json.dump(userfile,file)
              msg_lable=tk.Label(root,text="new supplier added successfully")
              msg_lable.pack()
           elif role=="cashier":
              cashier=Cashier(username,hashed_password)
              userlist.append({
              "id":lastUserId+1,
              "username":cashier.username,
              "password":cashier.password,
              "role":cashier.role
              })
              userfile["users"]=userlist
              with open(menu.user_file,"w") as file:
               json.dump(userfile,file)
              msg_lable=tk.Label(root,text="new cashier added successfully")
              msg_lable.pack()
        else :
           errr_lable=tk.Label(root,text="role is in valid enter cashier/supplier")
           errr_lable.pack()
   else:
       errr_lable=tk.Label(root,text="all the fields are required")
       errr_lable.pack()

id_entry_for_takeorder=None
def take_order():
   destroy_all_widgets(root)
   display_menu()
   dish_id=tk.Label(root,text="enter the id of dish to remove")
   global id_entry_for_takeorder
   dish_id.pack()
   id_entry_for_takeorder = tk.Entry(root)
   id_entry_for_takeorder.pack()
   submit_button = tk.Button(root, text="Submit", command=submit_take_order)
   submit_button.pack() 

def submit_take_order():
   global id_entry_for_takeorder
   id=id_entry_for_takeorder.get()
   try:
     id = int(id)
     menu.takeOrder(id)
     msg_lable=tk.Label(root,text="order taked successfully successfully")
     msg_lable.pack()
   except ValueError:
     err_lable=tk.Label(root,text="invalid id in put")
     err_lable.pack() 

def viewsale_data_for_cashier():
   destroy_all_widgets(root)
   previous_menu_button = tk.Button(root, text="go back",command=show_menu_for_cashier )
   previous_menu_button.pack(anchor='ne')
   datafile=menu.load_saledata_from_file()
   datalist=datafile["saledata"]
   # Create a Frame to hold the table within the existing window
   menu_frame = tk.Frame(root)
   menu_frame.pack(fill="both", expand=True)
   
   # Create a Treeview widget to display the table
   tree = ttk.Treeview(menu_frame, columns=("ID","Dish ID", "Name", "Price", "Category", "Sale Count","Sale Amount"), show="headings")

   # Define column headings
   tree.heading("ID", text="ID")
   tree.heading("Dish ID", text="Dish Id")
   tree.heading("Name", text="Name")
   tree.heading("Price", text="Price")
   tree.heading("Category", text="Category")
   tree.heading("Sale Count", text="Sale Count")
   tree.heading("Sale Amount", text="Sale Amount")

   # Add data to the table
   for item in datalist:
       tree.insert("", "end", values=(item["id"], item["dishid"],item["name"], item["price"], item["category"], item["salecount"],item["saleamount"]))

   # Pack the Treeview widget
   tree.pack(fill="both", expand=True)


update_id_entry_for_orderstatus=None
update_status_entry_for_orderstatus=None

def update_order_status():
   destroy_all_widgets(root)
   previous_menu_button = tk.Button(root, text="go back",command=show_menu_for_cashier )
   previous_menu_button.pack(anchor='ne')
   datafile=menu.load_orderdata_from_file()
   datalist=datafile["orderdata"]
   # Create a Frame to hold the table within the existing window
   menu_frame = tk.Frame(root)
   menu_frame.pack(fill="both", expand=True)
   
   # Create a Treeview widget to display the table
   tree = ttk.Treeview(menu_frame, columns=("ID", "Dish id", "Order status"), show="headings")

   # Define column headings
   tree.heading("ID", text="ID")
   tree.heading("Dish id", text="Dish id")
   tree.heading("Order status", text="Order status")

   # Add data to the table
   for item in datalist:
       tree.insert("", "end", values=(item["id"], item["dishid"], item["orderstatus"]))

   # Pack the Treeview widget
   tree.pack(fill="both", expand=True)

   global update_id_entry_for_orderstatus,update_status_entry_for_orderstatus
   
   id_lable=tk.Label(root,text="enter id of the Order ")
   id_lable.pack()
   update_id_entry_for_orderstatus=tk.Entry(root)
   update_id_entry_for_orderstatus.pack()

   name_lable=tk.Label(root,text="enter status preparing/delivered")
   name_lable.pack()
   update_status_entry_for_orderstatus=tk.Entry(root)
   update_status_entry_for_orderstatus.pack()
   submit_button = tk.Button(root, text="Submit", command=submit_order_status_change)
   submit_button.pack()

def submit_order_status_change():
    global update_id_entry_for_orderstatus,update_status_entry_for_orderstatus
    status=update_status_entry_for_orderstatus.get()
    id=update_id_entry_for_orderstatus.get()
    if status:
     status_obj={"orderstatus":status}
     print(status_obj)
    if id:
     try:
       id = int(id)  
       menu.changeOrderstatus(id,status_obj)
       update_order_status()
     except ValueError:
       err_lable=tk.Label(root,text="invalid id input")
       err_lable.pack()




          
              
              
              
   


   
   
   
      
      
         
         
    
    
      
      
     


   
   
   
   
          
        

root = tk.Tk()
root.title("Login Page")

label = tk.Label(root, text="Enter your username and password:")
menu_file = 'menu.json'
order_file ="orders.json"
sale_file ="sale.json"
user_file="users.json"
menu = Menu(menu_file,order_file,sale_file,user_file)

error_label = tk.Label(root, text="", fg="red")  # Initially an empty error label
error_label.pack()

username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root)
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")  # Hide password characters
login_button = tk.Button(root, text="Login", command=login)

label.pack()
username_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
login_button.pack()

root.mainloop()

