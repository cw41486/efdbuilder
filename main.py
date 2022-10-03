import json
import os.path
import time
from datetime import datetime
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
from tkinter import messagebox

# This is only a test.


#   Global Variables/Objects

logged = []
failures = []


#   Load JSON file data

#ecu_json = open('JSON/ECUS.json','r')
with open('JSON/ECUS.json','r') as ecu_json:
    ecu_data = json.load(ecu_json)


#   Setup the Chrome Driver.
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "C:\FCA Tests\FCA Tests\Buck_Vehicle Flash Tests\Vehicle Reports\Flash Support Status"}
options.add_experimental_option("prefs",prefs)


#   Authenticaion
efdBuilder = 'https://stage.fca-tools.com/workbench/index.php/utilities-efd-test/'
username = ''
password = ''
utility_passkey = 'INt3rn@lF1a5HT3stingEFD'
skipTest = ""
environment = 'eb2Template'




def infoWindow(title, message):
    root = Tk()
    root.withdraw()
    root.update()
    messagebox.showinfo(title=title,
                        message=message)
    root.destroy()

def UserInputWindow():
    root = Tk()
    root.wm_title('Enter EFD Builder credentials')
    root.geometry('520x320')


    def closeWindow(*args):
        global username
        username = user.get()
        global password
        password = pass_key.get()
        #global utility_passkey
        #utility_passkey = utility.get()
        root.destroy()

    def mainExit(*args):
        infoWindow(title='Exit program',message='Window closed by the user, test will be skipped.')
        sys.exit(0)


    def assignStage(*args):
        l = Label(root,text=f'Stage selected')
        l.grid(row=4,column=1,pady=10)
        global environment
        environment = 'eb2Stage'

    def assignTemplate(*args):
        l = Label(root, text=f'Template selected')
        l.grid(row=4, column=1, pady=10)
        global environment
        environment = 'eb2Template'

    def assignDev(*args):
        l = Label(root, text=f'Dev selected')
        l.grid(row=4, column=1, pady=10)
        global environment
        environment = 'efdBuilder2Dev'


    L1 = Label(root, text='Username', background='blue', foreground='yellow')
    L1.grid(row=0, column=0, pady=20, padx=20)
    user = Entry(root, width=50)
    user.grid(row=0, column=1, pady=10, padx=5)

    L2 = Label(root, text='password', background='blue', foreground='yellow')
    L2.grid(row=1, column=0, pady=20, padx=20)
    pass_key = Entry(root, show='*', width=50)
    pass_key.grid(row=1, column=1, pady=10, padx=5)

    #L3 = Label(root, text='Utilites page password', background='blue', foreground='yellow')
    #L3.grid(row=2, column=0, pady=20, padx=20)
    #utility = Entry(root, show='#', width=50)
    #utility.grid(row=2, column=1, pady=10, padx=5)

    okay_button = Button(root, text="Ok", command=closeWindow)
    okay_button.grid(row=3, column=2, pady=10)

    stageButton = Button(root,text="Stage Environment", command=assignStage)
    stageButton.grid(row=4,column=0,pady=10)

    templateButton = Button(root, text="Template Environment", command=assignTemplate)
    templateButton.grid(row=5, column=0, pady=10)

    devButton = Button(root, text="Dev Environment", command=assignDev)
    devButton.grid(row=5, column=1, pady=10)

    root.protocol(name="WM_DELETE_WINDOW",func=mainExit)
    root.mainloop()

#def log(x):
#    f = open('Logfile.txt','a')
#    f.write(f'{datetime.now().strftime("$m $d $Y)} :: {x}\n')
#    f.close()

def log(x):
    logged.append(f'{datetime.now().strftime("%m %d %Y")}  :: {x}\n')

#   Start of program

UserInputWindow()
driver = webdriver.Chrome('driver/chromedriver.exe', chrome_options=options)
driver.maximize_window()

try:
    #UserInputWindow()
    #driver = webdriver.Chrome('driver/chromedriver.exe', chrome_options=options)
    #driver.maximize_window()
    act = ActionChains(driver)      #   Action element.
    log(f'{environment} environment selected.')
    driver.get(efdBuilder)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'pwbox-6589')))
    driver.find_element(By.ID,'pwbox-6589').send_keys(utility_passkey)
    driver.find_element(By.XPATH,'//*[@id="page-6589"]/div/form/p[2]/input').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,f'//*[@id="{environment}"]/div/figure/a/img')))
    time.sleep(3)
    driver.find_element(By.XPATH,f'//*[@id="{environment}"]/div/figure/a/img').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ui-id-2"]')))
    time.sleep(3)
    driver.find_element(By.ID,f'auth-username-{environment}').send_keys(username)
    driver.find_element(By.ID,f'auth-password-{environment}').send_keys(password)
    driver.find_element(By.XPATH,'//span[contains(text(),"Login")]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ft-identifiers')))
    EB2_version = driver.find_element(By.CLASS_NAME,'app-version').text
    # currentVersion = ""
    with open('JSON/builderVersion.json','r') as eb2Version:
        currentVersion = json.load(eb2Version)

    if currentVersion["Version"] == EB2_version:
        log(f"{currentVersion['Version']} has already been tested")
        infoWindow("Test Skipped","Version has already been tested.")
    else:
        previousVersion = currentVersion["Version"]
        currentVersion["Version"] = EB2_version

    # log(f"Current Version of EB2: {EB2_version}")
        time.sleep(5)
        log("Template creation beginning.")

        #   Start to Create Template.  Loop through all ECUs.
        for ecu in ecu_data['ECU']:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(),"Create Template")]')))
            driver.find_element(By.XPATH, '//a[contains(text(),"Create Template")]').click()
            log("Clicked on 'Create Template'")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(),"Flash Format")]')))
            log("Opened to flash format page.")
            time.sleep(3)
            driver.find_element(By.XPATH, '//a[contains(text(),"EFD/2.7.3")]').click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(),"Add New Template")]')))
            log("Add new template")
            time.sleep(1)
            driver.find_element(By.XPATH, '//app-sdd-list').click()
            time.sleep(1)
            driver.find_element(By.XPATH, f'//option[contains(text(),"{ecu["SDD"]}")]').click()
            log(f"Selected {ecu['Template']['Protocol']}")
            time.sleep(1)
            driver.find_element(By.XPATH, '//app-sdd-list').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//div[@class="tab-row"]/div[@class="tab-controls"]').click()
            time.sleep(1)

        #   Add basic ECU Data.
            driver.find_element(By.XPATH, '//select[@title="Auto Flash"]').click()
            driver.find_element(By.XPATH, '//option[contains(text(),"Enabled")]').click()
            driver.find_element(By.XPATH, '//label[contains(@form-key,"ECUAcronym")]').send_keys(ecu['Name'])
            driver.find_element(By.XPATH, '//label[contains(@form-key,"ECUIdentifier")]').send_keys(ecu['ID'])
            driver.find_element(By.XPATH, '//label[contains(@form-key,"ECUVariant")]').send_keys(ecu["Variant"])
            elem = driver.find_element(By.XPATH, '//label[contains(@form-key,"ECUSupplier")]')
            act.double_click(elem)
            elem.send_keys(ecu["Supplier"])
            time.sleep(1)
            driver.find_element(By.XPATH, f'//span[contains(text(),"{ecu["SupplierID"]}")]').click()
            # driver.find_element(By.XPATH, '//label[contains(@form-key,"ECUSupplier")]').send_keys(ecu["Supplier"])
            elem = driver.find_element(By.XPATH, '//input[contains(@class,"ECUClass")]')
            elem.clear()
            elem.send_keys(f'{ecu["Class"]}_{datetime.today().strftime("%m_%d_%Y_%H_%M_%S ")}')
            time.sleep(1)
            if(ecu["Unlock"] == "None"):
                pass
            else:
                driver.find_element(By.XPATH,'//input[contains(@class,"SecurityUnlockScript")]').send_keys(os.path.abspath(f'unlocks/{ecu["Unlock"]}'))
            time.sleep(5)

        #   CAN IDs
            try:
                elem = driver.find_element(By.XPATH, '//input[contains(@class,"CANRequestFrame hex")]')
                act.move_to_element(elem)
                elem.send_keys(ecu['Template']['Req_ID'])
                elem = driver.find_element(By.XPATH, '//input[contains(@class,"CANResponseFrame hex")]')
                elem.send_keys(ecu['Template']['Res_ID'])
                if(ecu['Template']['Alt_Req_ID'] != "None"):
                    elem = driver.find_element(By.XPATH, '//input[contains(@class,"AltRequestFrame hex")]')
                    elem.send_keys(ecu['Template']['Alt_Req_ID'])
                if(ecu['Template']['Alt_Res_ID'] != "None"):
                    elem = driver.find_element(By.XPATH, '//input[contains(@class,"AltResponseFrame hex")]')
                    elem.send_keys(ecu['Template']['Alt_Res_ID'])

                log("CAN IDs successfully added.")
            except:
                driver.save_screenshot('./screenshots/CAN_ID_Error.png')
                failures.append("Failed to add CAN IDs.")
                failures.append(sys.exc_info())

        #   Bus/Protocl Info
            try:
                elem = driver.find_element(By.XPATH, '//label[contains(@form-key,"BusType")]/select')
                act.move_to_element(elem)
                elem.click()
                elem = driver.find_element(By.XPATH, f'//option[contains(text(),"{ecu["Template"]["BusType"]}")]')
                elem.click()
                log("Bus/Protocol Info successfully added.")
            except:
                driver.save_screenshot('./screenshots/Bus_protocol_Error.png')
                failures.append("Failed to select Bus/Protocol.")
                failures.append(sys.exc_info())

        #   Protcol Type
            try:
                elem = driver.find_element(By.XPATH, '//label[contains(@form-key,"ProtocolType")]/select')
                act.move_to_element(elem)
                elem.click()
                elem = driver.find_element(By.XPATH, f'//option[contains(text(),"{ecu["Template"]["Protocol"]}")]')
                elem.click()
                log("Protocol type successfully added.")
            except:
                driver.save_screenshot('./screenshots/Flash_protocol_Error.png')
                failures.append("Failed to select Flash Protocol.")
                failures.append(sys.exc_info())

        #   Process Type
            try:
                elem = driver.find_element(By.XPATH, '//label[contains(@form-key,"FlashProcessType")]/select')
                act.move_to_element(elem)
                elem.click()
                newelem = elem.find_element(By.XPATH, f'./option[contains(text(),"{ecu["Template"]["FlashProcess"]}")]')
                newelem.click()
                log("Process type successfully added.")
            except:
                driver.save_screenshot('./screenshots/Flash_Process_Error.png')
                failures.append("Failed to select flash prcoess.")
                failures.append(sys.exc_info())

        #   Checksum Definition
            try:
                elem = driver.find_element(By.XPATH, '/html/body/div/app-root/app-page-main/div/app-module-root-component/app-page-master/app-page/div/div/app-ecu-template-edit-form/app-main-content-panel/div/div/div[2]/form/div[1]/app-model-form-renderer/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field/app-main-content-customizable-tab/div/div[2]/div[1]/div/app-list-item-wrapper/div/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-object-field[2]/app-main-content-customizable-tab/div/div/div[2]')
                act.move_to_element(elem)
                elem.click()
                time.sleep(1)
                elem = driver.find_element(By.XPATH, '//label[contains(@form-key,"ChecksumType")]/select')
                elem.click()
                elem = driver.find_element(By.XPATH, f'//option[contains(text(),"{ecu["Template"]["Checksum"]}")]')
                elem.click()
                elem = driver.find_element(By.XPATH,'/html/body/div/app-root/app-page-main/div/app-module-root-component/app-page-master/app-page/div/div/app-ecu-template-edit-form/app-main-content-panel/div/div/div[2]/form/div[1]/app-model-form-renderer/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field/app-main-content-customizable-tab/div/div[2]/div[1]/div/app-list-item-wrapper/div/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field[1]/app-main-content-customizable-tab/div/div/div[2]')
                log('Whole Flash checksum successfully added.')
            except:
                driver.save_screenshot(f'./screenshots/Checksum_Definition_Error_{datetime.today().strftime("%m %d %Y")}.png')
                failures.append("Failed to select whole flash checksum.")
                failures.append(sys.exc_info())


        #   Logical Block Creation
            for ranges in ecu["Template"]["LogicalBlocks"]:
            #   Multiple Logical Blocks.
                if(len(ranges) > 1):
                    log("More than one block detected")
                    act.move_to_element(elem)
                    elem.click()
                    for add in range(len(ranges)-1):
                        elem = driver.find_element(By.XPATH, '//div[contains(text(),"Add another \'Logical Block\'")]')
                        act.move_to_element(elem)
                        elem.click()

                #   Logicla Block types
                    index = 1
                    elems = driver.find_elements(By.XPATH, '//label[contains(@form-key,"LogicalBlockType")]/select')
                    log(len(elems))

                    for types in elems:
                        elem = types
                        newElem = elem.find_element(By.XPATH, f'./*[contains(text(),"{ranges[f"LB{index}"]["Type"]}")]')
                        newElem.click()
                        index += 1
                    log('LB types added successfully.')

                #   Compression Mode
                    #   TODO: Add compression selection
                    elems = driver.find_elements(By.XPATH, '//label[@form-key="CompressionMode"]/input')
                    index = 1
                    for compression in elems:
                        if (ranges[f"LB{index}"]["CompressionMode"] != "None"):
                            pass
                        index += 1
                    log('Compression modes added successfully.')


                 #  Encryption Mode
                    # TODO:  Add Encyption selection
                    elems = driver.find_elements(By.XPATH, '//label[@form-key="EncryptionMode"]/input')
                    index = 1
                    for encrypt in elems:
                        if (ranges[f"LB{index}"]["EncryptionMode"] != "None"):
                            pass
                        index += 1
                    log('Encryption modes added successfully.')

                #   Signature Type
                #   TODO:   Add signature type selection
                    try:
                        elems = driver.find_elements(By.XPATH, '//label[@form-key="Signature"]/select')
                        index = 1
                        log(f'{len(elems)} Siganture objects detected.')
                        for signature in elems:
                            elem = signature
                            elem.click()
                            newElem = elem.find_element(By.XPATH, f'./option[contains(text(),"{ranges[f"LB{index}"]["Signature"]}")]')
                            newElem.click()
                            index += 1
                        log('Signature types added successfully.')

                    except:
                        driver.save_screenshot(f'./screenshots/Add Signatures error_{datetime.today().strftime("%m %d %Y")}.png')
                        failures.append("Failed to Add Signatures.")
                        failures.append(sys.exc_info())

                #   PKI settings.

                    count = 0

                    try:
                        elems = driver.find_elements(By.XPATH, '//app-main-content-customizable-tab[contains(@form-key,"PKI")]/div[contains(@class,"tab-container disabled")]')
                        log(f'{len(elems)} PKI tablets found.')

                        for pki in elems:
                            elem = pki
                            newElem = elem.find_element(By.XPATH, './div/div[contains(@class,"tab-controls")]')
                            try:
                                if(newElem.is_displayed()):
                                    log("located PKI element, clicking now.")
                                    newElem.click()
                                else:
                                    pass
                            except:
                                driver.save_screenshot('./screenshots/failed_to_select_PKI.png')
                                failures.append("Failed to select PKI.")
                                failures.append(sys.exc_info())

                        elems = driver.find_elements(By.XPATH, '//div[contains(@class,"tab-tree-padding PKI")]')
                        log(f'found {len(elems)} PKI elements')

                        lbIndex = 1

                        for settings in elems:
                            index = 0
                            elem = settings
                            elem_settings = elem.find_elements(By.XPATH,f'./app-form-input/label/input')
                            log(f'found {len(elem_settings)} PKI fields')
                            try:
                                # log(f'{len(ecu["Template"]["LogicalBlocks"][0].keys())} blocks found.')
                                for tries in range(1,len(ecu["Template"]["LogicalBlocks"][0].keys())):
                                    try:
                                        for id,val in ranges[f'LB{lbIndex}']["PKI Settings"].items():
                                            log(f'Sending {val} to PKI setting {id} for LB{lbIndex}')
                                            elem_settings[index].send_keys(val)
                                            index += 1
                                        break
                                    except:
                                        log(f"Skipping LB{lbIndex} since PKI is not there.")
                                    finally:
                                        lbIndex += 1

                            except:
                                driver.save_screenshot(f'./screenshots/Add PKI settings_Error_{count}_{datetime.today().strftime("%m %d %Y")}.png')
                                failures.append("Failed to Add PKI settings.")
                                failures.append(sys.exc_info())
                            finally:
                                count += 1


                    except:
                        driver.save_screenshot(f'./screenshots/PKI_Settings_Error_{count}_{datetime.today().strftime("%m %d %Y")}.png')
                        failures.append("Failed to Add PKI settings.")
                        failures.append(sys.exc_info())




                #   Checksum Definitions
                    # elems = driver.find_elements(By.XPATH, '//label[@form-key="ChecksumType"]/select')
                    elems = driver.find_elements(By.XPATH, '//app-main-content-customizable-tab[@form-key="ChecksumDefinition"]/div/div/div/app-form-select/label/select')
                    del elems[0]                #   delete the whole flash checksum selection.
                    index = 1
                    print(len(elems))
                    for checksum in elems:
                        elem = checksum
                        elem.click()
                        newElem = elem.find_element(By.XPATH, f'./*[contains(text(),"{ranges[f"LB{index}"]["Checksum"]}")]')
                        newElem.click()
                        index += 1
                    log('LB Checksums added successfully.')


                #   Address Ranges
                    elems = driver.find_elements(By.XPATH, '//div[@class="tab-row"]/h3[contains(text(),"Address Range")]')
                    # print(len(elems))
                    index = 1
                    for address in elems:
                        elem = address
                        newElem = elem.find_element(By.XPATH, './following-sibling::div[@class="tab-controls"]')
                        newElem.click()
                    log('LB address ranges added successfully.')

                #   Start Addresses
                    elems = driver.find_elements(By.XPATH, '//label[@form-key="StartAddress"]/input[@class="StartAddress hex"]')
                    index = 1
                    print(len(elems))
                    for start in elems:
                        elem = start
                        elem.send_keys(ranges[f"LB{index}"]["PhysicalBlocks"][0]["Start"])
                        index += 1

                #   End Addresses
                    elems = driver.find_elements(By.XPATH, '//label[@form-key="EndAddress"]/input[@class="EndAddress hex"]')
                    index = 1
                    print(len(elems))
                    for start in elems:
                        elem = start
                        elem.send_keys(ranges[f"LB{index}"]["PhysicalBlocks"][0]["Stop"])
                        index += 1


                #   Update Control Type

                    elems = driver.find_elements(By.XPATH, '//div[@class="tab-row"]/h3[contains(text(),"Update Control Definition")]')
                    print(len(elems))
                    index = 1
                    for address in elems:
                        if(ranges[f"LB{index}"]["Update Control Type"] == "None"):
                            pass
                        else:
                            elem = address
                            newElem = elem.find_element(By.XPATH, './following-sibling::div[@class="tab-controls"]')
                            newElem.click()
                        index += 1

                    elems = driver.find_elements(By.XPATH, '//label[@form-key="UpdateControlType"]/select')
                    log(f'{len(elems)} update control types found.')
                    index = 1
                    for update in elems:
                        elem = update
                        elem.click()
                        newElem = elem.find_element(By.XPATH, f'./option[contains(text(),"{ranges[f"LB{index}"]["Update Control Type"]}")]')
                        newElem.click()
                        index += 1

                    #   header start address
                    index = 1

                    elems = driver.find_elements(By.XPATH, "//label[@form-key='HeaderStart']")
                    log(f'{len(elems)} stripped headers found.')
                    for header in elems:
                        try:
                            if ranges[f"LB{index}"]["Stripped"] is True:
                                log(f"Stripped header detected. for LB{index}")
                                elem = header
                                elem.send_keys(ranges[f"LB{index}"]["PhysicalBlocks"][0]["Start"])
                                log(f'Successfully added header start address for LB{index}')

                        except(KeyError):
                            log(f'Skipping LB{index}.  No stripped header data.')
                        except:
                            driver.save_screenshot(f'./screenshots/Stripped_Header_Error_{datetime.today().strftime("%m %d %Y")}.png')
                            failures.append("Failed to add Stripped Header data.")
                            failures.append(sys.exc_info())
                        finally:
                            index += 1

                    #   Header length

                    index = 1

                    elems = driver.find_elements(By.XPATH, "//label[@form-key='HeaderLength']")
                    log(f'{len(elems)} header lengths found.')
                    for headerLength in elems:
                        try:
                            if ranges[f"LB{index}"]["Stripped"] is True:
                                log(f"Stripped header detected. for LB{index}")
                                elem = headerLength
                                elem.send_keys("448")
                                log(f'Successfully added header length 448 to LB{index}')

                        except(KeyError):
                            log(f'Skipping LB{index}.  No stripped header data.')
                        except:
                            driver.save_screenshot('./screenshots/Stripped_Header_Error.png')
                            failures.append("Failed to add Stripped Header data.")
                            failures.append(sys.exc_info())
                        finally:
                            index += 1

                    log('Update control types added successfully.')


                #   SWIL
                    #   TODO: Add SWIL selection
                    elems = driver.find_elements(By.XPATH,'//div[@class="tab-row"]/h3[contains(text(),"SWIL1")]')
                    print(len(elems))
                    index = 1
                    for address in elems:
                        if (ranges[f"LB{index}"]["SWIL"] == "None"):
                            pass
                        else:
                            elem = address
                            newElem = elem.find_element(By.XPATH, './following-sibling::div[@class="tab-controls"]')
                            newElem.click()
                        index += 1

                    elems = driver.find_elements(By.XPATH, '//input[@class="PhysicalBlock"]')
                    index = 1
                    log(f'{len(elems)} SWIL blocks found.')
                    for swil in elems:
                        swil.send_keys(os.path.abspath(f'SWIL/{ranges[f"LB{index}"]["SWIL"]["Filename"]}'))
                        time.sleep(1)

                    elems = driver.find_elements(By.XPATH, '//div[@class="tab-tree-padding SWIL1"]/app-object-field/app-main-content-customizable-tab/div/div/div/app-form-select/label/select')
                    log(f'{len(elems)} SWIL checksums detected.')
                    index = 1
                    for swilCheck in elems:
                        elem = swilCheck
                        elem.click()
                        newElem = elem.find_element(By.XPATH, f'./option[contains(text(),"{ranges[f"LB{index}"]["SWIL"]["Checksum"]}")]')
                        newElem.click()

                    log('SWIL added successfully.')

            #   Only 1 LB
                else:
                    act.move_to_element(elem)
                    elem.click()
                    elem = driver.find_element(By.XPATH, '//label[contains(@form-key,"LogicalBlockType")]/select')
                    elem.click()
                    elem = driver.find_element(By.XPATH, f'//option[contains(text(),"{ranges["LB1"]["Type"]}")]')
                    elem.click()
                    if(ranges["LB1"]["CompressionMode"] != "None"):
                        pass
                    if(ranges["LB1"]["EncryptionMode"] != "None"):
                        pass
                    if(ranges["LB1"]["Signature"] != "None"):
                        pass

                #   Checksum Definition
                    time.sleep(1)
                    elem = driver.find_element(By.XPATH, '//label[contains(@form-key,"ChecksumType")]')
                    act.move_to_element(elem)
                    elem.click()
                    elem = driver.find_element(By.XPATH, '/html/body/div/app-root/app-page-main/div/app-module-root-component/app-page-master/app-page/div/div/app-ecu-template-edit-form/app-main-content-panel/div/div/div[2]/form/div[1]/app-model-form-renderer/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field/app-main-content-customizable-tab/div/div[2]/div[1]/div/app-list-item-wrapper/div/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field[1]/app-main-content-customizable-tab/div/div[2]/div[1]/div/app-list-item-wrapper/div/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field/app-main-content-customizable-tab/div/div/div[2]')
                    elem.click()

                #   Address Ranges
                    if(len(ranges["LB1"]["PhysicalBlocks"]) > 1):
                        pass
                    else:
                        elem = driver.find_element(By.XPATH, '//input[@class="StartAddress hex"]')
                        act.move_to_element(elem)
                        elem.click()
                        elem.send_keys(f'{ranges["LB1"]["PhysicalBlocks"][0]["Start"]}')
                        elem = driver.find_element(By.XPATH, '//input[@class="EndAddress hex"]')
                        elem.send_keys(f'{ranges["LB1"]["PhysicalBlocks"][0]["Stop"]}')

                #   Update Control Type
                    if(ranges["LB1"]["Update Control Type"] != "None"):
                        elem = driver.find_element(By.XPATH,'/html/body/div/app-root/app-page-main/div/app-module-root-component/app-page-master/app-page/div/div/app-ecu-template-edit-form/app-main-content-panel/div/div/div[2]/form/div[1]/app-model-form-renderer/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field/app-main-content-customizable-tab/div/div[2]/div[1]/div/app-list-item-wrapper/div/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field[1]/app-main-content-customizable-tab/div/div[2]/div[1]/div/app-list-item-wrapper/div/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-object-field[3]/app-main-content-customizable-tab/div/div/div[2]')
                        act.move_to_element(elem)
                        elem.click()
                        elem = driver.find_element(By.XPATH, '//label[contains(@form-key,"UpdateControlType")]/select')
                        elem.click()
                        elem = driver.find_element(By.XPATH, f'//option[contains(text(),"{ranges["LB1"]["Update Control Type"]}")]')
                        elem.click()
                    else:
                        pass
                #   SWIL
                #   TODO:  Add abilty to insert SWIL into templates that require a SWIL.
                    if(ranges["LB1"]["SWIL"] != "None"):
                        pass
                    else:
                        pass

        #   Add scripts
            try:
                log("Adding new scripts")
                count = len(ecu["Template"]["Add Scripts"])
                log(f'{count} add scripts found')
                elem = driver.find_element(By.XPATH,'//div[@class="tab-row"]/h3[contains(text(),"Add Script")]/following-sibling::div[@class="tab-controls"]')
                elem.click()
                log("Attempt to add scripts")
                if(count > 1):
                    for x in range(len(ecu["Template"]["Scripts"])-1):
                        elem = driver.find_element(By.XPATH, '//div[contains(text(),"Add another \'Add Script\'")]')
                        elem.click()
                        log("Added another Add script")
                log("Select Script")
                index = 0
                elems = driver.find_elements(By.XPATH, '//label[@form-key="ScriptType"]/select')
                log(f'{len(elems)} select buttons found for Add scripts')
                for t in elems:
                    elem = t
                    elem.click()
                    newElem = elem.find_element(By.XPATH, f'./option[contains(text(),"{ecu["Template"]["Add Scripts"][index]["ScriptType"]}")]')
                    newElem.click()
                    index += 1
                log("Scriptypes selected.")
                index = 0
                elems = driver.find_elements(By.XPATH, '//label[@form-key="Script"]/em/a[@class="base-button small"]')
                log(f'{len(elems)} found for script select buttons.')
                log("Load script into the template")
                for t in elems:
                    elem = t
                    elem.click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="input-box"]')))
                    elem = driver.find_element(By.XPATH, '//div[@class="input-box"]')
                    elem.find_element(By.XPATH, './input').send_keys(f'{ecu["Template"]["Add Scripts"][index]["ScriptName"]}')
                    elem = driver.find_element(By.XPATH, '//ul[@class="on-right"]/li/a[@class="base-button"]')
                    elem.click()
                    time.sleep(3)
                    elem = driver.find_element(By.XPATH, '//div[@class="x-efd-scripts-table-holder"]/table[@class="scripts"]/tbody/tr/td[@class="column-name"]')
                    act1 = ActionChains(driver)
                    act1.double_click(elem).perform()
                    time.sleep(3)
                    log(f'{ecu["Template"]["Add Scripts"][index]["ScriptName"]} Successfully loaded')
                log("All \'add Scripts\' loaded.")
            except:
                driver.save_screenshot(f'./screenshots/Add_scripts_Error_{datetime.today().strftime("%m %d %Y")}.png')
                failures.append("Failed to Add Scripts.")
                failures.append(sys.exc_info())

        #   Replace Scripts
            try:
                log("Begin adding Replace Scripts")
                count = 0
                if(ecu["Template"]["Replace Scripts"] != "None"):
                    count = len(ecu["Template"]["Replace Scripts"])
                    log(f'Found {count} replace scripts.')
                if(count > 0):
                    elem = driver.find_element(By.XPATH, '//div[@class="tab-row"]/h3[contains(text(),"Replace Script")]/following-sibling::div[@class="tab-controls"]')
                    act.move_to_element(elem)
                    elem.click()
                    log("Attempt to add \'Replace scripts\'")
                    if (count > 1):
                        for x in range(len(ecu["Template"]["Replace Scripts"])-1):
                            elem = driver.find_element(By.XPATH, '//div[contains(text(),"Add another \'Replace Script\'")]')
                            elem.click()
                            log("Added another Replace script")
                    log("Select Script")
                    index = 0
                    elems = driver.find_elements(By.XPATH, '//label[@form-key="ScriptType"]/select')
                    for x in range(len(ecu["Template"]["Add Scripts"])):       # delete add script elements from the list.
                        del elems[0]
                    log(f'{len(elems)} replace items found.')
                    for t in elems:
                        elem = t
                        act.move_to_element(elem)
                        elem.click()
                        newElem = elem.find_element(By.XPATH, f'./option[contains(text(),"{ecu["Template"]["Replace Scripts"][index]["ScriptType"]}")]')
                        newElem.click()
                        index += 1
                    log("Scriptypes selected.")
                    index = 0
                    elems = driver.find_elements(By.XPATH, '//label[@form-key="Script"]/em/a[@class="base-button small"]')
                    log(f'{len(elems)} found for script select buttons.')
                    log("Load script into the template")
                    for t in elems:
                        elem = t
                        elem.click()
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="input-box"]')))
                        elem = driver.find_element(By.XPATH, '//div[@class="input-box"]')
                        elem.find_element(By.XPATH, './input').send_keys(f'{ecu["Template"]["Replace Scripts"][index]["ScriptName"]}')
                        elem = driver.find_element(By.XPATH, '//ul[@class="on-right"]/li/a[@class="base-button"]')
                        elem.click()
                        time.sleep(3)
                        elem = driver.find_element(By.XPATH,'//div[@class="x-efd-scripts-table-holder"]/table[@class="scripts"]/tbody/tr/td[@class="column-name"]')
                        act2 = ActionChains(driver)
                        act2.double_click(elem).perform()
                        time.sleep(3)
                        log(f'{ecu["Template"]["Replace Scripts"][index]["ScriptName"]}Successfully loaded')
                        index += 1
                    log("All \'Replace Scripts\' loaded.")
            except:
                driver.save_screenshot(f'./screenshots/Replace_Scripts_Error_{datetime.today().strftime("%m %d %Y")}.png')
                failures.append("Failed to replace scripts.")
                failures.append(sys.exc_info())

            #   Properties
            try:
                if(ecu["Template"]["Properties"] != "None"):
                    elem = driver.find_element(By.XPATH, '/html/body/div/app-root/app-page-main/div/app-module-root-component/app-page-master/app-page/div/div/app-ecu-template-edit-form/app-main-content-panel/div/div/div[2]/form/div[1]/app-model-form-renderer/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field/app-main-content-customizable-tab/div/div[2]/div[1]/div/app-list-item-wrapper/div/app-object-field/app-main-content-customizable-tab/div/div[2]/div/app-list-field[4]/app-main-content-customizable-tab/div/div/div[2]')
                    act.move_to_element(elem)
                    elem.click()
                    for i in range(len(ecu["Template"]["Properties"])-1):
                        elem = driver.find_element(By.XPATH, '//div[contains(text(),"Add another \'Property\'")]')
                        elem.click()
                        time.sleep(1)
                    index = 0
                    propertyNames = driver.find_elements(By.XPATH, '//input[contains(@class,"PropertyName")]')
                    propertyValues = driver.find_elements(By.XPATH, '//input[contains(@class,"PropertyValue")]')
                    keyProps = list(ecu["Template"]["Properties"].keys())
                    valProps = list(ecu["Template"]["Properties"].values())
                    for x in propertyNames:
                        x.send_keys(f'{keyProps[index]}')
                        index += 1
                    index = 0
                    for x in propertyValues:
                        x.send_keys(f'{valProps[index]}')
                        index += 1
            except:
                driver.save_screenshot(f'./screenshots/Properties_Error_{datetime.today().strftime("%m %d %Y")}.png')
                failures.append("Failed to add properties.")
                failures.append(sys.exc_info())

            #   Tags
            try:
                elem = driver.find_element(By.XPATH, '//h3[contains(text(),"Tags")]')
                act.move_to_element(elem)
                elem.click()
                elem = driver.find_element(By.XPATH, '/html/body/div[1]/app-root/app-page-main/div/app-module-root-component/app-page-master/app-page/div/div/app-ecu-template-edit-form/app-main-content-panel/div/div/div[2]/form/app-main-content-customizable-tab/div/div[2]/div/app-ecu-template-tag-list/label[5]/input')
                act.move_to_element(elem)
                elem.click()
                time.sleep(1)
            except:
                driver.save_screenshot(f'./screenshots/Tags_Error_{datetime.today().strftime("%m %d %Y")}.png')
                failures.append("Failed to select Tags.")
                failures.append(sys.exc_info())

            try:
                #   Build Note
                elem = driver.find_element(By.XPATH, '/html/body/div[1]/app-root/app-page-main/div/app-module-root-component/app-page-master/app-page/div/div/app-ecu-template-edit-form/app-main-content-panel/div/div/div[2]/form/label[2]/textarea')
                act.move_to_element(elem)
                elem.send_keys("EB2 Automated Template Creation.")

                #   Draft and Publish
                elem = driver.find_element(By.XPATH, '//a[contains(text(),"Draft")]')
                elem.click()
                time.sleep(3)

            except UnexpectedAlertPresentException:
                driver.save_screenshot(f'./screenshots/Alert_Window_appeared_{datetime.today().strftime("%m %d %Y")}.png')
                alert = Alert(driver)
                alert.accept()

            #   Go back to ECU Templates
            elem = driver.find_element(By.XPATH, '//a[contains(@href,"/flash-templates")]')
            act.move_to_element(elem)
            elem.click()

        with open('JSON/builderVersion.json', 'w') as eb2Version:
            json.dump(currentVersion, eb2Version)
        log(f'Updated EB2 version from {previousVersion} to {currentVersion["Version"]}')



except UnexpectedAlertPresentException:

    driver.save_screenshot(f'./screenshots/Alert_Window_appeared_{datetime.today().strftime("%m %d %Y")}.png')
    alert = Alert(driver)
    alert.accept()

except:
    print("Error detected")
    driver.save_screenshot('./screenshots/Error_Detected_{}.png'.format(datetime.today().strftime("%m %d %Y")))
    failures.append(sys.exc_info())

finally:
    driver.close()
    fileNum = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    while(1):
        if(os.path.isfile('./logging/log_{}.txt'.format(fileNum))):
            fileNum += 1
        else:
            f = open('./logging/log_{}.txt'.format(fileNum),'a')
            for x in logged:
                f.write(x)
            f.close()
            break
    if(len(failures) > 0):
        fail = open('./logging/failures_{}.txt'.format(fileNum),'a')
        fails = list(failures)
        for y in fails:
            for z in y:
                fail.write(str(z))
        fail.close()
        infoWindow("Failures were detected.","Check on the failures that were detected during testing.")
    else:
        infoWindow(title="Exit Program",message="Process completed.  :)")

