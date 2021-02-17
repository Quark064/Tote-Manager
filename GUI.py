import PySimpleGUI as sg
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


data = loadJSON()

scannedItems = [
    [
        sg.Text("Image Folder")
    ],
    [
        sg.Listbox(values=data['z-1006827-1']['parts'], size=(40, 40))
    ]
]

unexpectedItems = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

layout = [
    [
        sg.Column(scannedItems),
        sg.VSeperator(),
        sg.Column(unexpectedItems),
    ]
]

window = sg.Window("Image Viewer", layout)
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
