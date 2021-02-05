import json
import os


jsonStorage = os.path.join(os.getcwd(), "store.json")


def loadJSON():
    with open(jsonStorage, "r+") as file:
        data = json.load(file)
        return data


def writeJSON(var):
    f = open(jsonStorage, "w")
    f.write(json.dumps(var))
    f.close()


def vMode():
    print("\nVerify Mode:\n\nScan the items in the tote, you will be notified\nif a scanned item isn't in the tote. Type 'exit' at anytime\nto exit Verify Mode.\n")
    masterArr = []
    userScan = []
    data = loadJSON()
    tote = input("Scan Tote Barcode: ")
    try:
        test = data[tote]
        pass
    except Exception:
        print("\nTote not found.\n")
        startUp()
        return

    unexpArr = []
    for x in range(0, (len(data[tote]['parts']))):
        tmp = data[tote]['parts'][x]
        masterArr.append(tmp)

    print("\n{}\nComponents in Kit: {}\n".format(
        data[tote]['name'], len(data[tote]['parts'])))

    count = 1
    while (len(masterArr) != 0):
        storeString = input('Scan Component {}: '.format(count))
        if storeString.lower() == 'exit':
            print("\n")
            startUp()
            return
        if storeString.lower() == 'remove':
            remove = input('Scan component to remove from current scan: ')
            if remove in unexpArr:
                unexpArr.remove(remove)
            else:
                print("Scanned item was not marked as unexpected.")

        elif storeString in masterArr:
            masterArr.remove(storeString)
            print("\nItems Scanned: {}\nItems Remaining: {}\n".format(
                count, len(masterArr)))
            count += 1

        else:
            print('\nItem not in Kit.\nUnexpected Items:')
            unexpArr.append(storeString)
            for x in range(0, len(unexpArr)):
                print(unexpArr[x])
            print("\n")

    print('Tote Verified.\n')
    if len(unexpArr) != 0:
        print("However, the following items were scanned but not expected:\n")
        for x in range(0, len(unexpArr)):
            print(unexpArr[x])
        print("\n")

    startUp()
    return


def aMode():
    print("Add Mode: Scan Items Into a Tote\n\nScan your items now, when finished, simply type 'continue'\nto complete the transfers.")
    userScan = []
    data = loadJSON()
    tote = input("Scan Tote Barcode: ")
    try:
        test = data[tote]
        pass
    except Exception:
        print("\nTote not found.\n")
        startUp()

    print("\n{}\nComponents in Kit: {}\n".format(
        data[tote]['name'], len(data[tote]['parts'])))
    count = 1
    scan = True
    while scan == True:
        userIn = input("Scan item {} into kit: ".format(count))

        if userIn == 'continue':
            scan = False
            for x in range(0, len(userScan)):
                data[tote]['parts'].append(userScan[x])
                writeJSON(data)
            print('\nAdded {} components to tote.\n'.format(len(userScan)))
            startUp()
        else:
            userScan.append(userIn)
            count += 1
    return


def rMode():
    print("Remove Mode: Remove Items From Totes\n\nScan items to remove from a tote.\nWhen finished, type 'continue' to complete the transfers.")
    userScan = []
    data = loadJSON()
    tote = input("Scan Tote Barcode: ")
    try:
        test = data[tote]
        pass
    except Exception:
        print("\nTote not found.\n")
        startUp()

    print("\n{}\nComponents in Kit: {}\n".format(
        data[tote]['name'], len(data[tote]['parts'])))
    count = 1
    scan = True
    while scan == True:
        userIn = input("Scan item {} to remove from kit: ".format(count))

        if userIn == 'continue':
            scan = False
            for x in range(0, len(userScan)):
                data[tote]['parts'].remove(userScan[x])
                writeJSON(data)
            print('Removed {} scanned items from tote.'.format(count - 1))

        elif userIn == 'exit':
            startUp()
            return

        else:
            if userIn in data[tote]['parts']:
                userScan.append(userIn)
                count += 1
            else:
                print("\nScanned component isn't in tote.\n")
    return


def tMode():
    data = loadJSON()
    blankArr = []
    mode = input("\nTote Mode:\n'c' - Create a New Tote\n'd' - Delete an Existing Tote\n'exit' - Go Back\n\nChoose Mode: ")
    if mode.lower() == 'c':
        newTote = input("Scan Tote Barcode or Enter Name: ")
        if newTote.lower() == 'exit':
            startUp()
            return
        else:
            try:
                try:
                    test = data[newTote]
                    print('\nTote Already Exists.\n')
                except Exception:
                    data[newTote] = blankArr
                    writeJSON(data)
                    print("\nCreated new tote '{}'.\n".format(newTote))
            except Exception:
                print("\nCouldn't create tote.\n")

            startUp()
            return

    elif mode.lower() == 'd':
        data = loadJSON()
        test = ""
        deleteTote = input("Scan Barcode or Enter Name of Tote To Delete: ")

        try:
            test = data[deleteTote]

        except Exception:
            print("\nSpecified Tote Does Not Exist.\n")
            startUp()
            return

        doubleCheck = input(
            "\nAre you sure you want to delete tote '{}'? (y/n)".format(deleteTote))

        if doubleCheck.lower() == 'y':
            del(data[deleteTote])
            writeJSON(data)
            startUp()

        else:
            startUp()
            return

    elif mode.lower() == 'exit':
        startUp()
        return

    else:
        print("\nNot a valid input.\n")
        tMode()
        return


def startUp():
    selectMode = input("\nSelect Mode:\n'v' - Verify Tote\n'a' - Scan Items Into a Tote\n'r' - Remove Items From a Tote\n't' - Tote Mode: Create or Delete Totes\n\nChoose Mode: ")

    if (selectMode.lower() == "v"):
        vMode()
    elif (selectMode.lower() == "a"):
        aMode()
    elif (selectMode.lower() == 'r'):
        rMode()
    elif (selectMode.lower() == 't'):
        tMode()
    else:
        print('\nNot a valid key.\n')
        startUp()

startUp()
