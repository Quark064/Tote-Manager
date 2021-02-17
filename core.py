import json
import os

# Get the current working directory and joins it to locate "storage.json".
jsonStorage = os.path.join(os.getcwd(), "store.json")

# Loads the JSON storage file, do "data = loadJSON()" to update dict.
def loadJSON():
    with open(jsonStorage, "r+") as file:
        data = json.load(file)
        return data

# Writes the modified Python dict back to the "store.json" file.
def writeJSON(var):
    f = open(jsonStorage, "w")
    f.write(json.dumps(var))
    f.close()

# Takes a raw OsteoRemedies barcode and prints a formatted version.
def printBarFormat(bcStr):
    expDate = "20{}-{}-{}".format(bcStr[18:20], bcStr[20:22], bcStr[22:24])
    lot = bcStr[26:]
    ref = bcStr[2:16]
    print("REF: {}      LOT: {}     EXP: {}".format(ref, lot, expDate))

# Verification Mode - Verifies totes and can show/remove unexpected contents.
def vMode():
    print("\nVerify Mode:\n\nScan the items in the tote, you will be notified\nif a scanned item isn't in the tote. Type 'exit' at anytime\nto exit Verify Mode.\n")
    masterArr = []                  # Initialize variables for comparisons.
    userScan = []
    data = loadJSON()               # Load in the JSON file and store it as "data".
    tote = input("Scan Tote Barcode: ").lower()


    # Checks if the scanned tote exists.
    try:
        test = data[tote]
        pass

    except Exception:
        print("\nTote not found.\n")
        startUp()
        return

    # After verifying the tote exists, stores all the components of the kit in list "masterArr".
    unexpArr = []
    for x in range(0, (len(data[tote]['parts']))):
        tmp = data[tote]['parts'][x]
        masterArr.append(tmp)

    # Prints the tote nickname and the total number of expected items.
    print("\n{}\nComponents in Kit: {}\n".format(data[tote]['name'], len(data[tote]['parts'])))

    # Main scan loop; While running, it will accept scans until the user types "continue",
    # or until the kit has been verified. (masterArr is empty)
    count = 1
    while (len(masterArr) != 0):            # Checks if masterArr is empty, and loops if it has contents.
        storeString = input('Scan Component {}: '.format(count))

        # Breaks out of verification scan, and calls startUp().
        if storeString.lower() == 'exit':
            print("\n")
            startUp()
            return

        # Enters a removal mode that allows a user to remove a scanned item by scanning it again.
        if storeString.lower() == 'remove':
            remove = input('Scan component to remove from current scan: ')

            if remove in unexpArr:
                unexpArr.remove(remove)
            else:
                print("Scanned item was not marked as unexpected.")


        # Calls the end of the verification scan early, meaning that there are still some items
        # remaining in "masterArr". Gives the option for the user to remove the items remaining.
        if storeString.lower() == 'continue':
            print("The following items were expected but not scanned, please verify usage:\n")

            for x in range(0, len(masterArr)):     # Prints all remaining items.
                printBarFormat(masterArr[x])       # Calls printBarFormat to pretty print.

            check = input("\nRemove the above items from tote? (y/n): ") # Check if user wants to remove.

            # User chose Yes; removes remaining items in "masterArr" from "store.json" and
            # writes the result to disk.
            if check.lower() == 'y':

                for x in range(0, len(masterArr)):
                    data[tote]['parts'].remove(masterArr[x])
                    writeJSON(data)

                print('\nRemoved {} components from tote.\n'.format(len(masterArr)))
                startUp()           # Verification finished; calls "startUp()".

            # The user chose No or entered an invalid character.
            else:
                print("\nNo changes made.\n")


        # No special inputs were made, we assume a component barcode was scanned.
        # All if and elif statements work with a barcode from this point.
        elif storeString in masterArr: # Barcode scanned matched one in kit; remove it from "masterArr".
            masterArr.remove(storeString)
            print("\nItems Scanned: {}\nItems Remaining: {}\n".format(count, len(masterArr)))
            count += 1                 # Increments count, which is used for printing current scan number.

        else:
            print('\nItem not in Kit.\nUnexpected Items:') # Barcode scanned was not in kit, add it to
            unexpArr.append(storeString)                   # "unexpArr" and print all items in the list.
            for x in range(0, len(unexpArr)):
                printBarFormat(unexpArr[x])
            print("\n")

    # While loop is broken, meaning "masterArr" is now empty.
    # Check if we have unexpected items in the "unexpArr" list, and if it is not
    # empty, print items that are unexpected.
    print('Tote Verified.\n')
    if len(unexpArr) != 0:
        print("However, the following items were scanned but not expected:\n")

        for x in range(0, len(unexpArr)):   # Prints formatted values in "unexpArr".
            printBarFormat(unexpArr[x])
        print("\n")

    startUp()       # Calls main "startUp()" function.
    return          # and returns the function as a failsafe.


# Scans items into an existing tote.
def sMode():
    print("Add Mode: Scan Items Into a Tote\n\nScan your items now, when finished, simply type 'continue'\nto complete the transfers.")
    userScan = []                                   # Initialize starting variables.
    data = loadJSON()                               # Update the "data" dict with "storage.json".
    tote = input("Scan Tote Barcode: ").lower()     # Gets tote barcode/identifier.

    try:
        test = data[tote]                           # Checks to see if scanned tote exists.
        pass
    except Exception:                               # If not, print and call "startUp()".
        print("\nTote not found.\n")
        startUp()

    # Scanned tote exists and we can now work with it; gets number of components in kit.
    print("\n{}\nComponents in Kit: {}\n".format(data[tote]['name'], len(data[tote]['parts'])))

    count = 1                       # Use for incrementing numbers.
    scan = True                     # Keeps the scan while loop running.

    while scan == True:
        userIn = input("Scan item {} into kit: ".format(count)) # Gets barcode of item to add.

        if userIn == 'continue':                                # Checks if the user is done.
            scan = False                                        # Stops while loop execution.

            for x in range(0, len(userScan)):
                data[tote]['parts'].append(userScan[x])         # Adds the scanned items into "data" dict.
                writeJSON(data)                                 # Writes "data" dict to "storage.json".

            print('\nAdded {} components to tote.\n'.format(len(userScan)))

            startUp()                                           # Calls main "startUp()" loop.

        else:                                                   # User is not done.
            userScan.append(userIn)                             # Adds the scan to the "userScan" list.
            count += 1                                          # Increments "count" by 1.
    return                                                      # Returns as a failsafe.


# Remove mode; Removes scanned items from a kit.
def rMode():
    print("Remove Mode: Remove Items From Totes\n\nScan items to remove from a tote.\nWhen finished, type 'continue' to complete the transfers.")
    userScan = []                                   # Initialize scan storage list "userScan".
    data = loadJSON()                               # Updates "data" dict with "storage.json".
    tote = input("Scan Tote Barcode: ").lower()     # Gets tote barcode.

    try:
        test = data[tote]                           # Checks if scanned tote exists.
        pass
    except Exception:                               # Tote is not found, falls back to
        print("\nTote not found.\n")                # main function "startUp()".
        startUp()

    # Assuming we have a valid tote; prints number of components in scanned kit.
    print("\n{}\nComponents in Kit: {}\n".format(data[tote]['name'], len(data[tote]['parts'])))

    count = 1               # Initialize count and scan variables.
    scan = True

    while scan == True:     # Main scanning loop, scans items to remove until user enters a keyword.
        userIn = input("Scan item {} to remove from kit: ".format(count))

        if userIn == 'continue':        # Checks if user has entered "continue".
            scan = False                # Stops while loop execution.

            for x in range(0, len(userScan)):               # Takes all items scanned into the "userScan"
                data[tote]['parts'].remove(userScan[x])     # list and removes them from the "data" dict.
            writeJSON(data)                                 # Writes "data" dict to "storage.json".

            print('Removed {} scanned items from tote.'.format(count - 1))

        elif userIn == 'exit':      # Quits the loop, ignores any input given
            startUp()               # and returns to the main function "startUp()".
            return                  # Returns as a failsafe.

        else:                                       # No keyword was entered, treats input as a barcode.
            if userIn in data[tote]['parts']:       # Checks if item flagged for removal is in tote.
                userScan.append(userIn)             # Appends the scanned barcode into the "userScan" list
                count += 1                          # for removal and increments the count.

            else:
                print("\nScanned component isn't in tote.\n")
    return


# Tote Mode; has two sub-modes "create" and "delete".
# Used for managing totes.
def tMode():
    data = loadJSON()           # Updates the "data" dict with "store.json".
    blankArr = {}

    # Gets user input on which submode to run, or to go back.
    mode = input("\nTote Mode:\n'c' - Create a New Tote\n'd' - Delete an Existing Tote\n'exit' - Go Back\n\nChoose Mode: ")

    if mode.lower() == 'c':      # User selected the option to create a tote.
        newTote = input("Scan Tote Barcode or Identifier: ").lower()

        if newTote.lower() == 'exit':   # Checks if the user wants to exit.
            startUp()                   # Returns to main function "startUp()".
            return                      # Returns as a failsafe.

        else:
            try:            # "Try" attempts to create a new tote, prints an error
                            # message if it was unsuccessful.

                try:                                    # "Try" checks to see if a tote with that name
                    test = data[newTote]                # already exists.
                    print('\nTote Already Exists.\n')

                except Exception:                       # Runs if tote did not already exist.

                    check = input("Create nickname for the tote? (y/n): ").lower()

                    if check == "n":    # Checks if the user wants to add a nickname to the
                        toteName = newTote      # tote (gets stored in "data[toteName]['name']").
                                                # If not, assigns "data[toteName]['name']" with the
                    elif check == "y":  # scanned barcode/identifier.
                        toteName = input("Add a tote nickname: ")

                    else:                       # User didn't enter "y" or "n", assumes no.
                        print("\nNot a valid input, asssuming no.\n")
                        toteName = newTote

                    data[newTote] = blankArr            # Creates a new array and writes the
                    data[newTote]['parts'] = []         # with proper formatting.
                    data[newTote]['name'] = toteName
                    writeJSON(data)                     # Updates "storage.json".

                    print("\nCreated new tote '{}'.\n".format(newTote))


            except Exception:                           # Runs if above code fails to execute.
                print("\nCouldn't create tote.\n")

            startUp()                                   # Returns to main function "startUp()".
            return

    # -- End of create tote code --

    elif mode.lower() == 'd':           # User selected the option to delete a tote.
        data = loadJSON()               # Update "data" dict.
        test = ""                       # Initializes "test" string for existance testing

        deleteTote = input("Scan Barcode or Enter Name of Tote To Delete: ").lower()

        try:
            test = data[deleteTote]

        except Exception:               # Executes if the scanned tote does not exist.
            print("\nSpecified Tote Does Not Exist.\n")
            startUp()                   # Returns to main function "startUp()".
            return

        doubleCheck = input("\nAre you sure you want to delete tote '{}'? (y/n): ".format(deleteTote))

        if doubleCheck.lower() == 'y':          # User entered 'y'; deletes the scanned tote.
            del(data[deleteTote])

            print("Deleted tote '{}'".format(deleteTote))

            writeJSON(data)                     # Updates "data" dict and returns execution to
            startUp()                           # main function "startUp()".

        else:                                   # User choose no or another character, returns
            startUp()                           # execution to "startUp()".
            return

        # -- End of delete tote code --


    elif mode.lower() == 'exit':                # Quits prematurely.
        startUp()                               # Returns execution to "startUp()".
        return

    else:                                       # User didn't make a valid selection,
        print("\nNot a valid input.\n")         # returns to "startUp()".
        tMode()
        return

# List Mode; Lists totes and their compnents.
def lMode():
    data = loadJSON()                      # Updates "data" dict.

    print("\nTotes:\n")

    for x in range(0, len(data)):           # Runs through "storage.json" and prints every
        barcode = list(data.keys())[x]      # tote in the file.
        name = data[barcode]['name']        # Gets nickname of totes to print as well.

        if barcode == name:                 # If tote doesn't have a nickname, sets the name
            name = 'N/A'                    # to "N/A".


        final = list(str(barcode))                          # PRETTY PRINTER
        while (len(final) != 20) and (len(final) < 21):     # Aligns all of the columns to be
            final.append(' ')                               # nice and organized.

        print("{}: Name: {} Nickname: {}\n".format((x + 1), ''.join(final), name))

    toteNum = int(input("Select Tote To View Contents of: ")) # Get the tote the user selected.

    barcode = list(data.keys())[toteNum - 1]               # Gets the selected tote's barcode/identifier.
    print("\n\n{}\n".format(data[barcode]['name']))

    length = len(data[barcode]['parts'])             # Assigns "length" the amount of components in kit.

    if length == 0:                                  # Checks if the selected tote is empty.
        print("\nTote is empty.\n")

    else:                                            # If not empty, prints all components in the kit.
        for x in range(0, length):
            printBarFormat(data[barcode]['parts'][x])

    startUp()                                        # Returns execution to "startUp()".


# Main controller function; gets user input and runs the corresponding functions.
def startUp():
    selectMode = input("\nSelect Mode:\n'v' - Verify Tote\n's' - Scan Items Into a Tote\n'r' - Remove Items From a Tote\n't' - Tote Mode: Create or Delete Totes\n'l' - List Tote Names And Contents\n\nChoose Mode: ")

    if (selectMode.lower() == "v"):
        vMode()

    elif (selectMode.lower() == "s"):
        sMode()

    elif (selectMode.lower() == 'r'):
        rMode()

    elif (selectMode.lower() == 't'):
        tMode()

    elif (selectMode.lower() == 'l'):
        lMode()

    elif (selectMode.lower() == 'quit'):
        print("Goodbye!")

    else:
        print('\nNot a valid key.\n')
        startUp()


startUp()
