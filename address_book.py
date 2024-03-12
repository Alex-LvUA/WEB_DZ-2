from collections import UserDict
from datetime import datetime
from mod import Mod
import time
import pickle
import os



"""
Консольна програма записує телефонні номери у словник, реалізована з технологією класів.

Методи класу Record:
add_birthday(self, birthday_s) - додає день народження
days_to_birthday(self) -пише скільки днів залишилось до дня народження
add_phone(self,phone_s) - Додає телефон до списку запису
edit_phone(self, old_phone, new_phone) -Змінює телефон
remove_phone(self, phone) -видаляє телефон зі списку запису
find_phone(self, num_phone) - знаходить теелефон

Методи класу AddressBook:
add_record(self, record) -додає запис до книги(словник-імя:дані)
get_all_in_page(self,n) - видає книгу по порціям п-записів за раз, якщо не вказати товидасть всі записи за раз
get_all(self,count=-1) видає книгу по порціям count-записів за раз, якщо не вказати товидасть всі записи за раз
find(self, name) -Знаходить запис по імені
delete(self, name) Видаляє запис з книги по імені
get_find(self,found="") Виводить в консоль записи які включають в собі пошуковий рядок(частина номера або імені)

Клас Address_book має один статичний метод саll для роботи зкористувачем(викликає і обробляє всі можливі запити)
Працює зі словником for_user, який містить команду для виклику запита, опис запита і функцію для виконання запиту

"""
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW="\033[93m"
RESET = "\033[0m"
BLUE = "\033[94m"
filename = os.path.join("files", "save_contacts.bin")



class Field:
    def __init__(self, value):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value=new_value



    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super.__init__(self,value)



class Phone(Field):
   def __init__(self, value):
        if int(value) and len(value)==10:
            self.value = value
        else:
            raise ValueError


class Birthday(Field):
    def __init__(self, value):
      try:
           self.value = value
           d=value.split("-")
           self.date=datetime(int(d[2]),int(d[1]),int(d[0]))
      except Exception as e:
          raise ValueError



class Name(Field):
    def __init__(self, value):
        self.value = value



class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday=birthday
        if birthday:
            try:
                self.date=Birthday(birthday)
            except  ValueError:
                print('день народження повинен бути в строковому типі "DD-MM-YYYY"')

    def add_birthday(self, birthday_s):
        try:
            self.value=birthday_s
            self.birthday = Birthday(birthday_s)
        except  ValueError:
            print(f'{birthday_s} день народження повинен бути в строковому типі "DD-MM-YYYY"')

    def days_to_birthday(self):
        if self.birthday:
            current_datetime = datetime.now()
            dbirt=datetime(current_datetime.year, self.birthday.date.month, self.birthday.date.day)
            if current_datetime>dbirt:
                dbirt=datetime(current_datetime.year+1, self.birthday.date.month, self.birthday.date.day)

            days= dbirt-current_datetime
            print(f"До дня народження {self.name}  залишилось {days.days} днів")
        else:
            print(f"birthday of {self.name} is unknown")

    def add_phone(self,phone_s):
      try:
          self.phones.append(Phone(phone_s))
      except ValueError as e:
          if len(str(e))>0:
             print(f'{RED}{e}{YELLOW} -у номері телефона мають бути тільки цифри {RESET}')
          else:
             print(f'{RED}{phone_s}{YELLOW}  номер телефона має складатись з 10 цифр{RESET}')

    def edit_phone(self, old_phone, new_phone):
        n=0
        f=True
        for phone in self.phones:
            if phone.value==old_phone:
                f=False
                self.phones.pop(n)
                self.phones.insert(n,Phone(new_phone))
            n+=1
        if f:
            raise ValueError

    def remove_phone(self, phone):
        n = 0
        f = True
        try:
            for phon in self.phones:
                if phon.value == phone:
                    f = False
                    self.phones.pop(n)
                n += 1
            if f:
                raise ValueError
        except ValueError:
            print(f'{RED}{phone} {YELLOW}- не знайдений{RESET}')

    def find_phone(self, num_phone):
        for phone in self.phones:
            if phone.value == num_phone:
                return phone

    def __str__(self):
        sp=f"{BLUE} phones:{YELLOW} {'; '.join(p.value for p in self.phones)}" if self.phones else ""
        sb=f",{BLUE} birthday: {YELLOW} {self.birthday}{RESET}" if self.birthday else ""
        return (f"{BLUE}Contact name:{YELLOW} {self.name.value} {sp} {sb}")


class AddressBook(UserDict):

    def add_record(self, record):
       self[record.name.value]=record


    def get_all_in_page(self,n=0):

        list_rec=[]
        for name, record in self.data.items():
            list_rec.append(record)
        if n<=0:
           n=len(list_rec)

        def list_generator(n, x=0):
            y = n + x
            for l in list_rec[x:y]:
                print(l)
            if y >= len(list_rec):
                return
            
            if input("нажміть  Enter для продовження") == "":
                if (x + n) <= len(list_rec):
                    x = x + n
                    list_generator(n, x)

        list_generator(n)

    def get_find(self,found=""):
        for name, record in self.data.items():
           find_tel=0
           for num in record.phones:
              if str(num).find(found)>=0:
                  find_tel=1
           if (name.find(found)>=0 or find_tel==1):
               print(record)


    def get_some(self,x,y):
        i=0
        for name, record in self.data.items():
           if (x <=i and i<=y):
               print(record)
           i += 1
    def get_all(self,count=-1):
        if count==-1 or count>len(self.data.items()):
            a = len(self.data.items())
        else:
            a=count-1

        y=a
        self.get_some(0,y)
        while y<len(self.data.items()):
            if input("нажміть  Enter для продовження")=="":
                print("%" * 50)
                x=y+1
                y+=a+1
                self.get_some(x, y)

    def find(self, name):
        for nam, rec in self.data.items():
            if rec.name.value==name:
               return rec

    def delete(self, name):
       for nam, rec in self.data.items():
            if nam == name:
                del self[nam]
                return nam
       return None

    def save_to_file(self,filename):
        with open(filename, 'wb') as fh:
            pickle.dump(self,fh)


def read_from_file(file):
        with open(file, 'rb') as fh:
            return pickle.load(fh)

def greate_book(filename):
    try:
        book=read_from_file(filename)
        #book.get_all()
    except Exception as ex:
        print(f"{ex}-------")
        book = AddressBook()
    return book



def add(book):
    name = input("веедіть імя :")
    if (name):
        record = Record(name)
        phone = input("веедіть номер тел (або Enter для пропуску):")
        if phone:
            record.add_phone(phone)
        birthday = input("веедіть lane дату народження [DD-MM-YYYY](або Enter для пропуску):")
        if birthday:
            record.add_birthday(birthday)
        book.add_record(record)
def add_tel(book):
    name = input("веедіть імя :")
    if (name):
        rec = book.find(name)
        if rec:
            phone = input("веедіть номер тел:")
            rec.add_phone(phone)
        else:
            print(f"ім'я {name} не знайдено у книзі")
def delete(book) :
     name = input("веедіть імя :")
     if (name):
         nam = book.delete(name)
         if nam:
             print(f"{nam} видалено з книги")
         else:
             print(f"{name} не знайдено в книзі")
def all(book) :
    n = -1
    if len(book.data.items()) > 10:
        n = 10
    book.get_all(n)
def find(book):
    f = input("введіть пошуковий рядок (частину імені або телефона):")
    book.get_find(f)
def exit(book):
    book.save_to_file(filename)


def help(book):
    print(f' List of command:')
    for com in for_user:
        print(f'{YELLOW} {com} {BLUE}{for_user[com][0]}{RESET}')

for_user=dict()

for_user["add"]=['add contact to phone book',add]
for_user["add tel"] = ['add phone to record with Name', add_tel]
for_user["delete"] = ['delete  record from list', delete]
for_user["all"] = ['показати всі записи', all]
for_user["find"] = ['пошук по фрагменту імені або  номера телефона', find]
for_user["exit"] = ['exit from program', exit]
for_user["back"] = ['повернення в попереднє меню', exit]
for_user["help"] = ['help', help]

class Address_book(Mod):
    @staticmethod
    def call()->bool:
        filename_address_book = os.path.join("files", "save_contacts.bin")
        book=greate_book(filename_address_book)

        while True:
            data = input("address book>").lower()
            if data in for_user:
                for_user[data][1](book)
                if data=="back":   # вихід в попереднє меню
                    return False
                if data=="exit":  # вихід
                    return True
            else:
                print(f'команда "{data}" не визначена')


def main():

    print(f'{YELLOW}Вітаю! Ви зайшли в книгу контаків, для виходу введіть "exit" , Довідка по командам -"Help"{RESET}')

    Address_book.call()





if __name__ == "__main__":
    main()
    pass

