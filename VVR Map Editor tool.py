import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
import traceback

root = tk.Tk()
root.title("VVR Map Editor Tool")
root.geometry("500x500")
root.resizable(False,True)
titleText = tk.Label(root, text="VVR Map Editor", font="bold")
titleText.place(x=250, y=20, anchor="n")

class vtmFile:
    staticPrefabsStart = 0
    fileDir = ""
    importedFile = []
        
    def import_file():
        vtmFile.fileDir = fd.askopenfilename(title="Import the .vtm Map File", filetypes=[("Map files", "*.vtm")])
        file = open(vtmFile.fileDir, "r")
        try:
            print("File Directory:", vtmFile.fileDir)
            vtmFile.importedFile = file.readlines()
            print("File Data", vtmFile.importedFile)
        except:
            traceback.print_exc()
        file.close()
        
        for element in range(0, len(vtmFile.importedFile)):
            try:
                vtmFile.importedFile[element].index("StaticPrefabs")
                vtmFile.staticPrefabsStart = element
                print("staticPrefabsStart =", vtmFile.staticPrefabsStart)
            except ValueError: #Catches the error if "StaticPrefabs" is not found so it doesnt clog the console
                None
            except:
                traceback.print_exc() #If a different error is found, it prints it for easy debugging

        
class PreciseStaticPrefab:
    prefabName = None
    Id = None
    xCoord = None
    yCoord = None
    zCoord = None
    xRot = None
    yRot = None
    zRot = None
    template = ["\t\tStaticPrefab\n",
                "\t\t{\n",
                "\t\t\tprefab = {prefab}\n",
                "\t\t\tid = {idNum}\n",
                "\t\t\tglobalPos = ({coordx}, {coordy}, {coordz})\n",
                "\t\t\trotation = ({rotx}, {roty}, {rotz})\n",
                "\t\t}\n"]
        
    def display():
        print("Loading PreciseStaticPrefab.display()")
        PreciseStaticPrefab.prefabName = ttk.Entry(width=20)
        prefabText = tk.Label(root, text="Prefab Name")
        
        PreciseStaticPrefab.Id = ttk.Entry(width=6)
        IdText = tk.Label(root, text="Prefab Id Number")
        PreciseStaticPrefab.Id.insert(0, "0")
        
        useNextIdButton = ttk.Button(root, text="Use Next Id", command=lambda: PreciseStaticPrefab.use_next_id())
        importButton = ttk.Button(root, text="Import Prefab", command=lambda: PreciseStaticPrefab.import_prefab())
        
        PreciseStaticPrefab.xCoord = ttk.Entry(width=10)
        xCoordText = tk.Label(root, text="X - Coordinate")
        PreciseStaticPrefab.xCoord.insert(0, "0")

        PreciseStaticPrefab.yCoord = ttk.Entry(width=10)
        yCoordText = tk.Label(root, text="Y - Coordinate")
        PreciseStaticPrefab.yCoord.insert(0, "0")

        PreciseStaticPrefab.zCoord = ttk.Entry(width=10)
        zCoordText = tk.Label(root, text="Z - Coordinate")
        PreciseStaticPrefab.zCoord.insert(0, "0")

        PreciseStaticPrefab.xRot = ttk.Entry(width=3)
        xRotText = tk.Label(root, text="X - Rotation")
        PreciseStaticPrefab.xRot.insert(0, "0")

        PreciseStaticPrefab.yRot = ttk.Entry(width=3)
        yRotText = tk.Label(root, text="Y - Rotation")
        PreciseStaticPrefab.yRot.insert(0, "0")

        PreciseStaticPrefab.zRot = ttk.Entry(width=3)
        zRotText = tk.Label(root, text="Z - Rotation")
        PreciseStaticPrefab.zRot.insert(0, "0")

        saveButton = ttk.Button(root, text="Save Prefab", command=lambda: PreciseStaticPrefab.save_prefab())
        deleteButton = ttk.Button(root, text="Delete Prefab", command=lambda: PreciseStaticPrefab.delete_prefab())
        clearButton = ttk.Button(root, text="Clear Settings", command=lambda: PreciseStaticPrefab.clear_settings())
        print("PreciseStaticPrefab.display() Loaded")

        xorigin = 110
        yorigin = 140

        prefabText.place(x=xorigin - 90, y=yorigin - 35)
        IdText.place(x=xorigin - 90, y=yorigin - 70)

        PreciseStaticPrefab.prefabName.place(x=xorigin - 10, y=yorigin - 35)
        PreciseStaticPrefab.Id.place(x=xorigin + 15, y=yorigin - 70)
        
        useNextIdButton.place(x=xorigin + 65, y=yorigin - 72)
        importButton.place(x=xorigin+148, y=yorigin - 72)
        
        PreciseStaticPrefab.xCoord.place(x=xorigin, y=yorigin)
        PreciseStaticPrefab.yCoord.place(x=xorigin, y=yorigin + 25)
        PreciseStaticPrefab.zCoord.place(x=xorigin, y=yorigin + 50)

        PreciseStaticPrefab.xRot.place(x=xorigin+165, y=yorigin)
        PreciseStaticPrefab.yRot.place(x=xorigin+165, y=yorigin + 25)
        PreciseStaticPrefab.zRot.place(x=xorigin+165, y=yorigin + 50)

        xCoordText.place(x=xorigin-90, y=yorigin)
        yCoordText.place(x=xorigin-90, y=yorigin + 25)
        zCoordText.place(x=xorigin-90, y=yorigin + 50)

        xRotText.place(x=xorigin+90, y=yorigin)
        yRotText.place(x=xorigin+90, y=yorigin + 25)
        zRotText.place(x=xorigin+90, y=yorigin + 50)
        
        saveButton.place(x=xorigin-90, y=yorigin + 85)
        deleteButton.place(x=xorigin, y=yorigin + 85)
        clearButton.place(x=xorigin+93, y=yorigin + 85)
      
    def use_next_id():
        PreciseStaticPrefab.Id.delete(0, "end")
        PreciseStaticPrefab.Id.insert(0, PreciseStaticPrefab.find_next_id())

    def find_next_id():
        high = -1
        for element in range(vtmFile.staticPrefabsStart, len(vtmFile.importedFile)):
            if vtmFile.importedFile[element] != "\t}\n":
                try:
                    vtmFile.importedFile[element].index("\t\t\tid =")
                    tempId = vtmFile.importedFile[element]
                    tempId = tempId[8:vtmFile.importedFile[element].index("\n")]
                    tempId = int(tempId)
                    if tempId > high:
                        high = tempId
                except ValueError:
                    None
                except:
                    traceback.print_exc()
        return high + 1

    def search_prefabs_for_id(Id):
        searchTerm = "\t\t\tid = " + str(Id)
        print("searching prefabs for id:", Id)
        for element in range(vtmFile.staticPrefabsStart, len(vtmFile.importedFile)):
            if vtmFile.importedFile[element] != "\t}\n":
                try:
                    vtmFile.importedFile[element].index(searchTerm)
                    prefabStartLocation = element - 3
                    print("Id found at Prefab location:", prefabStartLocation)
                    return prefabStartLocation
                except ValueError: #Catches the error if "\t\t\tid = " is not found so it doesnt clog the console
                    None
                except:
                    traceback.print_exc() #If a different error is found, it prints it for easy debugging
        return None

    def delete_prefab():
        deleteList = []
        element = PreciseStaticPrefab.search_prefabs_for_id(PreciseStaticPrefab.Id.get())
        if element == None:
            print("The selected Prefab could not be found. It either doesnt exist or is corrupted.")
            return None
        print("Deleting prefab starting at line:", element)
        while vtmFile.importedFile[element] != "\t\t}\n":
            deleteList.append(vtmFile.importedFile[element])
            element += 1
        deleteList.append(vtmFile.importedFile[element])
        print("deleteList:\n\n", deleteList)
        
        element = 0
        deleteElement = 0
        file = open(vtmFile.fileDir, "w")
        for line in vtmFile.importedFile:
            if deleteElement != len(deleteList):
                if deleteList[deleteElement] != vtmFile.importedFile[element]:
                    file.write(line)
                else:
                    deleteElement += 1
            else:
                file.write(line)
            element += 1
        file.close()

        file = open(vtmFile.fileDir, "r")
        vtmFile.importedFile = file.readlines()
        file.close()
        print("File deleted:\n\n", vtmFile.importedFile)

    def write_prefab():
        output = ["","","","","","",""]
        output[0] = PreciseStaticPrefab.template[0]
        output[1] = PreciseStaticPrefab.template[1]
        output[2] = PreciseStaticPrefab.template[2].format(prefab = PreciseStaticPrefab.prefabName.get())
        output[3] = PreciseStaticPrefab.template[3].format(idNum = PreciseStaticPrefab.Id.get())
        output[4] = PreciseStaticPrefab.template[4].format(coordx = PreciseStaticPrefab.xCoord.get(), coordy = PreciseStaticPrefab.yCoord.get(), coordz = PreciseStaticPrefab.zCoord.get())
        output[5] = PreciseStaticPrefab.template[5].format(rotx = PreciseStaticPrefab.xRot.get(), roty = PreciseStaticPrefab.yRot.get(), rotz = PreciseStaticPrefab.zRot.get())
        output[6] = PreciseStaticPrefab.template[6]

        print("output:\n\n", output)
        element = 0
        file = open(vtmFile.fileDir, "w+")
        for line in vtmFile.importedFile:
            if element == vtmFile.staticPrefabsStart + 2:
                file.writelines(output)
            file.write(line)
            element += 1
        vtmFile.importedFile = file.readlines()

    def import_prefab():
        importList = []
        element = PreciseStaticPrefab.search_prefabs_for_id(PreciseStaticPrefab.Id.get())
        if element == None:
            print("The selected Prefab could not be found. It either doesnt exist or is corrupted.")
            return None
        print("Importing prefab starting at line:", element)
        while vtmFile.importedFile[element] != "\t\t}\n":
            importList.append(vtmFile.importedFile[element])
            element += 1
        importList.append(vtmFile.importedFile[element])
        print("importList:\n\n", importList)

        print("condensed importList:\n\n")
        for element in range(0, len(importList)):
            if element == 2:
                prefab = importList[element]
                prefab = str(prefab[12:importList[element].index("\n")])
                
                PreciseStaticPrefab.prefabName.delete(0, "end")
                PreciseStaticPrefab.prefabName.insert(0, prefab)
                
                print(prefab)
            elif element == 4:
                globalPos = importList[element]
                globalPos = str(globalPos[15:importList[element].index("\n")])

                xCoordPointer = globalPos.index(",", 1)
                xCoord = globalPos[1:xCoordPointer]

                yCoordPointer = globalPos.index(",", xCoordPointer + 1)
                yCoord = globalPos[xCoordPointer + 2:yCoordPointer]

                zCoordPointer = globalPos.index(")", yCoordPointer + 1)
                zCoord = globalPos[yCoordPointer + 2:zCoordPointer]

                PreciseStaticPrefab.xCoord.delete(0, "end")
                PreciseStaticPrefab.yCoord.delete(0, "end")
                PreciseStaticPrefab.zCoord.delete(0, "end")
                
                PreciseStaticPrefab.xCoord.insert(0, xCoord)
                PreciseStaticPrefab.yCoord.insert(0, yCoord)
                PreciseStaticPrefab.zCoord.insert(0, zCoord)
                
                print(globalPos, ":", xCoord, yCoord, zCoord)
            elif element == 5:
                rotation = importList[element]
                rotation = str(rotation[14:importList[element].index("\n")])
                
                xRotPointer = rotation.index(",", 1)
                xRot = rotation[1:xRotPointer]

                yRotPointer = rotation.index(",", xRotPointer + 1)
                yRot = rotation[xRotPointer + 2:yRotPointer]

                zRotPointer = rotation.index(")", yRotPointer + 1)
                zRot = rotation[yRotPointer + 2:zRotPointer]

                PreciseStaticPrefab.xRot.delete(0, "end")
                PreciseStaticPrefab.yRot.delete(0, "end")
                PreciseStaticPrefab.zRot.delete(0, "end")
                
                PreciseStaticPrefab.xRot.insert(0, xRot)
                PreciseStaticPrefab.yRot.insert(0, yRot)
                PreciseStaticPrefab.zRot.insert(0, zRot)
                
                print(rotation, ":", xRot, yRot, zRot)

    def save_prefab():
        PreciseStaticPrefab.delete_prefab()
        PreciseStaticPrefab.write_prefab()

    def clear_settings():
        PreciseStaticPrefab.Id.delete(0, "end")
        PreciseStaticPrefab.prefabName.delete(0, "end")
        PreciseStaticPrefab.xCoord.delete(0, "end")
        PreciseStaticPrefab.yCoord.delete(0, "end")
        PreciseStaticPrefab.zCoord.delete(0, "end")
        PreciseStaticPrefab.xRot.delete(0, "end")
        PreciseStaticPrefab.yRot.delete(0, "end")
        PreciseStaticPrefab.zRot.delete(0, "end")

        PreciseStaticPrefab.Id.insert(0, 0)
        PreciseStaticPrefab.xCoord.insert(0, 0)
        PreciseStaticPrefab.yCoord.insert(0, 0)
        PreciseStaticPrefab.zCoord.insert(0, 0)
        PreciseStaticPrefab.xRot.insert(0, 0)
        PreciseStaticPrefab.yRot.insert(0, 0)
        PreciseStaticPrefab.zRot.insert(0, 0)

vtmFile.import_file()
PreciseStaticPrefab.display()
root.mainloop()
