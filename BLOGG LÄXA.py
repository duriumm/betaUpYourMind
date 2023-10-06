import datetime #Importerar modulen datetime för hantering av datum och tid
import json#Importerar modulen json för funktioner med JSON-data, för datautbyte.

class MyBlog:
    """definerar klassen myblog"""
    def __init__(self): #Definerar kontruktorn init för klassen MyBlog
        self.my_entries = []#Konstruktorn initierar insatsvariabeln my_entries för att lagra blogginlägg


    def create_entry(self, entry):
        """Definerar metoden create_entry för att skapa nya inlägg"""
        if not self.find_entry(entry.my_title): #OM INTE find_entry metoden hittar ett inlägg med samma titel fortsätter koden
            self.my_entries.append(entry) #Om villkoret returnerar NONE så lägger vi till inlägget(entry) i my_entries[]
            self.my_entries.sort(key=lambda e: e.my_date, reverse=True) #Efter att det läggs till sorteras det efter datum i omvänd ordning
            return True# Om allt returnerar True indikerar det att inlägget las till
        return False#Om villkoret  if not self.find_entry(entry.my_title): inte är sant(samma titel finns) returneras False

    def get_all_entries(self):
        """Definerar en metod get_all_entries som returnerar alla inlägg i bloggen. Argumentet är bara self, referens till insatsen av klassen"""
        return self.my_entries#Returnerar listan my_entries som innehåller alla blogginlägg

    def find_entry(self, title):
        """Definerar metoden find_entry för att leta efter inlägg efter titeln(argumentet)"""
        self.my_entries.sort(key=lambda e: e.my_title)#Sorterar inläggens titel i stigande ordning med lambda som använder titeln som nyckel
        low, high = 0, len(self.my_entries) - 1 #Initierar variable low high för vart sökningen ska göras. Low är index för lägsta värdet(första i bokstavsordning) i området och high det högsta värdet

        while low <= high: #Inleder loop sålänge low är mindre eller lika med high, området som det finns att söka inom
            mid = (low + high) // 2 #Räknar ut mitten av indexet och sökområdet och tilldelar variabeln "mid"
            entry = self.my_entries[mid]#Hämtar inlägget vid index "mid" från my_entries, tilldelar den variabeln "entry". Inlägget jämförs med sökta titeln.

            if entry.my_title == title:#Jämför titel på det aktuella blogginlägget med den sökta titeln, om den stämmer
                return entry#Returnera det hittade inlägget entry
            elif entry.my_title < title: #Om entry är mindre än den sökta titeln uppdateras low till mid +1 för att söka högre
                low = mid + 1
            else: #Annars uppdateras high till mid -1 för att söka lägre
                high = mid - 1

        return None

    def edit_entry(self, title, new_title, new_content):
        """definerar metoden edit_entry för att redigera inlägg"""
        entry = self.find_entry(title)#Använder find_entry metoden för att hitta inlägget med titeln
        if entry:#Om inlägget med den befintliga titeln hittas
            entry.my_title, entry.my_content = new_title, new_content#Uppdatera inläggets titel, innehåll och tid med de nya värdena

    def remove_entry(self, title):
        """Definerar metoden remove entry för att radera inlägg"""
        entry = self.find_entry(title)#Hämtar det befintliga inlägget med den befintliga titeln från listan my_entries. Hittas den tilldelas den variabeln "entry"
        if entry:# Om entry har tilldellats något värde(är inte None)
            self.my_entries.remove(entry) #Tas entry bort från listan my_entries

    def save_to_file(self, filename):
        """Metod för att spara bloggdata till en JSON.fil"""
        with open(filename, 'w') as file: #Öppnar filen med filnamnet i w-läge(skrivläge). Använder with uttrycket för att se till så att filen stängs korrekt
            # Skapar en lista av dictionaries där varje dictionary representerar ett blogginlägg.
            # Varje dictionary innehåller nycklarna 'title', 'content', och 'date' med motsvarande värden från blogginläggen i self.my_entries-listan.
            data = [{'title': entry.my_title, 'content': entry.my_content, 'date': entry.my_date.isoformat()} for entry in self.my_entries]
            json.dump(data, file)#Omvandlar data till JSON format i den specifierade filen("file")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file: #Försöker öppna filnamnet för läsning("r")
                data = json.load(file) #Läser och tolkar JSON-data från filen som tidigare skrevs med 'w' och återskapar datan i variabeln data
                #Skapar en ny lista av MyEntry objekt av den inlästa datan
                #Itererar över varje dictionary(entry) i den tidigaren "data" och skapar ett nytt MyEntry-onjekt för varje inlägg
                #Vi konverterar även datetime från isoformat till datetime
                self.my_entries = [MyEntry(entry['title'], entry['content'], datetime.datetime.fromisoformat(entry['date'])) for entry in data]
                self.my_entries.sort(key=lambda e: e.my_date, reverse=True)#Sorterar den nya listan efter datum i omvänd ordning med nyast först
        except FileNotFoundError: #Hittar vi inte data i JSON-filen så låter vi self.my_entries vara oförändrad
                pass

class MyEntry:
    def __init__(self, title, content, date):
        self.my_title = title  # Skapar en instansvariabel "my_title" för inläggets titel
        self.my_content = content  # Skapar en instansvariabel "my_content" för inläggets innehåll
        self.my_date = date  # Skapar en instansvariabel "my_date" för inläggets datum


def start():
    my_blog = MyBlog()  # Skapar en instans av MyBlog-klassen och lagrar den i variabeln "my_blog"
    while True:
        print("\nWhat would you like to do with the blog?")
        print("1. View all entries")
        print("2. Add an entry")
        print("3. Search for an entry")
        print("4. Edit an entry")
        print("5. Remove an entry")
        print("6. Save entries to a file")
        print("7. Load entries from a file")
        print("8. Exit the blog")

        choice = input("Choose an option: ")

        if choice == "1":
            all_entries = my_blog.get_all_entries()#hämtar alla inlägg från myBlog
            if not all_entries: #Om det inte finns några inlägg att visa
                print("There are no entries to display.")
            else: # Annars loopar vi igenom alla inlägg och skriver ut deras titel, inlägg, datum och tid
                for entry in all_entries:
                    #Vi infogar blogginlägget titel(entry.my_title)
                    #Infogar blogginläggets datum och tid genom att formatera med .strftime enligt formatet ÅR MÅN DAG och tid
                    #Entry.my_content är platsen där blogginläggets inlägg kommer att infogas
                    print(f"{entry.my_title} ({entry.my_date.strftime('%Y-%m-%d %H:%M:%S')}):\n{entry.my_content}\n")
        elif choice == "2":
            title = input("Enter the title of your entry: ")
            content = input("Enter the content of your entry: ")
            date = datetime.datetime.now()# Lägger till nuvarande datum och tid
            new_entry = MyEntry(title, content, date)#Skapar ett nytt inlägg med användarens data
            if my_blog.create_entry(new_entry):# Anropar metoden create_entry på objektet my_blog och används för att skapa ny blogginlägg
                print("Your entry has been added successfully!")
            else:
                print("An entry with the same title already exists.")
        elif choice == "3":
            title = input("Enter the title of the entry you want to search for: ")
            entry = my_blog.find_entry(title)#Söker efter inlägget med samma titel
            if entry:#Om entry hittas skriver vi ut dess titel, datum och tid och inlägget
                print(f"{entry.my_title} ({entry.my_date.strftime('%Y-%m-%d %H:%M:%S')}):\n{entry.my_content}\n")
            else:
                print("No entry was found with that title.")
        elif choice == "4":
            title = input("Enter the title of the entry you want to edit: ") #Skriver titeln på nuvarande blogg
            new_title = input("Enter the new title for your entry: ")#Skriver titeln som den ska ändras till
            new_content = input("Enter the new content for your entry: ")#Skriver nytt inlägg som den ska ändras till
            my_blog.edit_entry(title, new_title, new_content) # Redigerar blogginlägget med den nya texten
            print("Your entry has been edited successfully!")
        elif choice == "5":
            title = input("Enter the title of the entry you want to remove: ")#Skriver in titeln på nuvarande blogg
            my_blog.remove_entry(title) #Vi raderar blogginlägget med samma titel
            print("Your entry has been removed successfully!")
        elif choice == "6":
            filename = input("Enter the filename to save to: ")#Användaren får skriva in namnet på filen han vill spara till
            my_blog.save_to_file(filename) # Vi sparar inlägget till den angivna filen
            print("Blog data has been saved to a file.")
        elif choice == "7":
            filename = input("Enter the filename to load from: ")#Användaren får skriva in namnet på filen han vill hämta ifrån
            my_blog.load_from_file(filename) #Vi laddar inlägget från de angivna filen
            print("Blog data has been loaded from a file.")
        elif choice == "8":
            print("Exiting the blog. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option (1-8).")

if __name__ == "__main__": # Startar och kör hela bloggprogrammet när filen körs som ett fristående skript
    start()
