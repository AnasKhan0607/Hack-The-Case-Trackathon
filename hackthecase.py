from firebase import firebase
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial

d = firebase.FirebaseApplication('https://hackthecase-18c09-default-rtdb.firebaseio.com/', None)

data = d.get('https://hackthecase-18c09-default-rtdb.firebaseio.com/user', '')
# print(data)


def get_users(data: dict, location_dict: dict, location: str):
    user_window = tk.Tk()
    user_window.title("Users")
    user_window.geometry("400x700")
    label1 = tk.Label(user_window, text="User Info", relief="solid", width="20", font=("bold", 15))
    label1.place(x=90, y=40)
    label = tk.Label(user_window)
    label.grid(row=0, column=0, pady=20, padx=1)
    i=1

    for name in location_dict[location][1:]:
        i += 1
        ipaddress = data[name].get("IPaddress")
        number = data[name].get("number")
        homeaddress = data[name].get("homeaddress")
        currentlocation = data[name].get("location")
        label = tk.Label(user_window, text=f"{name} \n IPaddress: {ipaddress} \n Number: {number} \n Home Address: {homeaddress}, \n Current Location: {currentlocation}", bg="red")
        label.grid(row=i, column=0, pady=20, padx=90, ipadx=20, ipady=20)
        print(f"{name}: {data[name]}")


def get_hot_spots(data: dict, hot_spot_number: int):
    people_per_location = {}
    for name in data:
        if data[name].get("facility") == "apartment":
            if data[name].get("IPaddress") not in people_per_location:
                people_per_location[data[name].get("IPaddress")] = [1]
                people_per_location[data[name].get("IPaddress")].append(name)
            else:
                lst = []
                for name_ in people_per_location[data[name].get("IPaddress")][1:]:
                    lst.append(data[name_].get("homeaddress"))
                if data[name].get("homeaddress") not in lst:
                    people_per_location[data[name].get("IPaddress")][0] += 1
                    people_per_location[data[name].get("IPaddress")].append(name)
        if data[name].get("facility") == "House":
            if data[name].get("location") not in people_per_location:
                people_per_location[data[name].get("location")] = [1]
                people_per_location[data[name].get("location")].append(name)
            else:
                lst = []
                for name_ in people_per_location[data[name].get("location")][1:]:
                    lst.append(data[name_].get("homeaddress"))
                if data[name].get("homeaddress") not in lst:
                    people_per_location[data[name].get("location")][0] += 1
                    people_per_location[data[name].get("location")].append(name)
    print(people_per_location)

    result_window = tk.Tk()
    result_window.title("Results")
    result_window.geometry("400x700")
    label1 = tk.Label(result_window, text="Hot Spots", relief="solid", width="20", font=("bold", 15))
    label1.place(x=90, y=40)
    label = tk.Label(result_window)
    label.grid(row=0, column=0, pady=20, padx=1)
    i = 1
    for location in people_per_location:
        if people_per_location[location][0] >= hot_spot_number:
            i += 1
            label = tk.Button(result_window, text=f"{location} is a danger zone", bg="red", command=partial(get_users, data, people_per_location, location))
            label.grid(row=i, column=0, pady=20, padx=90, ipadx=20, ipady=20)

    result_window.mainloop()



window = tk.Tk()
window.geometry("600x600")
window.title("Trackathon")

def exitt():
    exit()

imge = Image.open(r"C:\Users\maste\Desktop\csc148\logo.png")
photo = ImageTk.PhotoImage(imge)
lab = tk.Label(image=photo)
lab.place(x=120, y=20)
fn = tk.IntVar()

label1 = tk.Label(window, text="Get Tracking", relief="solid", width="20", font=("bold", 15))
label1.place(x=190, y=230)

label2 = tk.Label(window, text="Enter max amount of people: ", width=25)
label2.place(x=120, y=300)

entry_1 = tk.Entry(window, textvar=fn)
entry_1.place(x=300, y=300)

button_search = tk.Button(window, text="Search", width=12, bg="red", fg="white", command=lambda: get_hot_spots(data, fn.get()))
button_search.place(x= 250, y=400)

window.mainloop()
