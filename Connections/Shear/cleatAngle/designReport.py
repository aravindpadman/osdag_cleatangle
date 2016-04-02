'''
Created on 16-Mar-2016

@author: reshma
'''
import sys
import time
import math
import pdfkit
# import os.path
# import pickle
from numpy.core.defchararray import rstrip
from PyQt4.Qt import QString 


uiObj ={'Member': {'ColumSection': 'ISSC 200', 'fu (MPa)': 410, 'BeamSection': 'ISMB 400', 'fy (MPa)': 250, 'Connectivity': 'Column web-Beam web'},
        'Plate': {'Width (mm)': 0, 'Height (mm)': 0, 'Thickness (mm)': 10},
        'Load': {'ShearForce (kN)': 120},
        'Weld': {'Size (mm)': 6},
        'Bolt': {'Grade': 8.8, 'Diameter (mm)': 20, 'Type': 'HSFG'}}
outObj ={'Plate': {'plateedge': 50.0, 'platethk': 12, 'momentcapacity': 17.673, 'beamdepth': 300.0, 'minHeight': 180.0, 'height': 180.0, 'minWidth': 110.0, 'width': 110.0, 'externalmoment': 7.8, 'colflangethk': 17.2, 'beamrootradius': 14.0, 'beamflangethk': 13.1, 'colrootradius': 17.0, 'blockshear': 377.36, 'web_plate_fy': 250}, 
         'Weld': {'thicknessprovided': 10, 'weld_fu': 410, 'weldstrength': 1325.596, 'effectiveWeldlength': 160.0, 'thickness': 10, 'resultantshear': 987.996}, 
         'Bolt': {'status': True, 'boltcapacity': 15.612, 'shearcapacity': 15.612, 'numofbolts': 8, 'enddist': 30.0, 'beam_fu': 410, 'web_plate_t': 12, 'boltgrpcapacity': 124.896, 'beam_w_t': 7.7, 'numofrow': 4, 'numofcol': 2, 'bolt_dia': 12, 'edge': 30.0, 'gauge': 30.0, 'bearingcapacity': 39.324, 'pitch': 40.0, 'dia_hole': 13, 'bolt_fu': 400, 'shearforce': 120, 'k_b': 0.519}}
dictBeamData = {'B': '140', 'Mass': '61.5', 'D': '400', 'FlangeSlope': '98', 'Zx': '1020', 'R1': '14',
                'Ix': '20500', 'Iy': '622', 'ry': '2.82', 'Area': '78.4', 'R2': '7', 'Id': '10', 'Zy': '88.9', 
                'tw': '8.9', 'rx': '16.2', 'T': '16', 'Designation': 'ISMB 400'}
dictColData ={'B': '200', 'Mass': '60.3', 'D': '200', 'FlangeSlope': '98', 'Zx': '553', 'R1': '18', 'Ix': '5530', 
              'Cy': '0', 'ry': '4.46', 'Area': '76.8', 'R2': '9', 'Id': '7', 'Zy': '153', 'tw': '9', 'rx': '8.48', 
              'T': '15', 'Iy': '1530', 'Designation': 'ISSC 200'}
   

def save_html(outputObj, uiObj, dictBeamData, dictColData,dictCleatData,reportsummary):
    fileName = ("/home/reshma/workspace/Osdag/output/finPlateReport3.html")
    myfile = open(fileName, 'w')
    myfile.write(t('! DOCTYPE html'))
    myfile.write(t('html'))
    myfile.write(t('head'))
    myfile.write(t('link type="text/css" rel="stylesheet" href="newstyle.css"/'))
    myfile.write(t('/head'))
    myfile.write(t('body'))
    print outObj
    
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DATA PARAMS
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#Project summary data
    companyname = str(reportsummary['CompanyName'])
    companylogo = str(reportsummary['CompanyLogo'])
    groupteamname = str(reportsummary['Group/TeamName'])
    designer = str(reportsummary['Designer'])
    projecttitle = str(reportsummary['CompanyName'])
    subtitle = str(reportsummary['Subtitle'])
    jobnumber = str(reportsummary['JobNumber'])
    method = str(reportsummary['Method'])
    addtionalcomments = str(reportsummary['AdditionalComments'])
    
    print "company" , companyname, groupteamname
    
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#FinPlate Main Data
    beam_sec = str(uiObj['Member']['BeamSection'])
    column_sec = str(uiObj['Member']['ColumSection'])
    connectivity = str(uiObj['Member']['Connectivity'])
    beam_fu = str(uiObj['Member']['fu (MPa)'])
    beam_fy = str(uiObj['Member']['fy (MPa)'])
              
    shear_load = str(uiObj['Load']['ShearForce (kN)'])
                  
    bolt_dia = str(uiObj['Bolt']['Diameter (mm)'])
    bolt_type  = str(uiObj["Bolt"]["Type"])
    bolt_grade = str(uiObj['Bolt']['Grade'])
   
    cleat_length = str(uiObj['cleat']['Height (mm)'])
    cleat_fu = str(uiObj['Member']['fu (MPa)'])
    cleat_fy = str(uiObj['Member']['fy (MPa)'])
    cleat_sec = str(uiObj['cleat']['section'])
    
    
#     dictbeamdata  = get_beamdata(beam_sec)
    beam_w_t = float(dictBeamData[QString("tw")])
    beam_f_t = float(dictBeamData[QString("T")])
    beam_d = float(dictBeamData[QString("D")])
    beam_R1 =float(dictBeamData[QString("R1")])
    beam_B =float(dictBeamData[QString("B")])
    beam_D =float(dictBeamData[QString("D")])
       
#      dictcolumndata = get_columndata(column_sec)
    column_w_t = float(dictColData[QString("tw")])
    column_f_t = float(dictColData[QString("T")])
    column_R1 =float(dictColData[QString("R1")])
    column_D = float(dictColData[QString("D")])
    column_B = float(dictColData[QString("B")])

        
   
#     dictCleatData = get_angledata(cleat_sec)
    cleat_legsize= int(dictCleatData[QString("A")])
    cleat_legsize_1 = int(dictCleatData[QString("B")])
    cleat_thk = int(dictCleatData[QString("t")])
    
    
    
    
    
    #'Size (mm)'
#     weld_Thick = str(uiObj['Weld']['Size (mm)'])
#     
#     beamdepth = str(int(round(outObj['Plate']['beamdepth'],1)))
#     beamflangethk = str(int(round(outObj['Plate']['beamflangethk'],1)))
#     beamrootradius = str(int(round(outObj['Plate']['beamrootradius'],1)))
#     platethk = str(int(round(outObj['Plate']['platethk'],1)))
#     blockshear = str(int(round(outObj['Plate']['blockshear'],1)))
#     colflangethk = str(int(round(outObj['Plate']["colflangethk"],1)))
#     colrootradius = str(int(round(outObj['Plate']['colrootradius'])))
#     
#     plateWidth = str(int(round(outObj['Plate']['width'],1)))
#     plateLength = str(int(round(outObj['Plate']['height'],1)))
#     weldSize = str(int(round(outObj['Weld']['thickness'],1)))   
#     plateDimension = plateLength +'X'+ plateWidth + 'X'+ plateThick
    
    
    
    ##########################Output###########################
    
    noOfBolts = str(outObj['Bolt']['numofbolts'])
    noOfRows = str(outObj['Bolt']['numofrow'])
    noOfCol = str(outObj['Bolt']['numofcol'])
    edge = str(int(round(outObj['Bolt']['edge'],1)))
    gauge = str(int(round(outObj['Bolt']['gauge'],1)))
    pitch = str(int(round(outObj['Bolt']['pitch'],1)))
    end = str(int(round(outObj['Bolt']['enddist'],1)))
    weld_strength = str(round(float(outObj['Weld']['weldstrength']/1000),3))
    moment_demand = str(outObj['Plate']['externalmoment'])
    
    beam_tw = str(float(dictBeamData["tw"]))

    bolt_fu = str(outObj['Bolt']['bolt_fu'])
    bolt_dia = str(outObj['Bolt']['bolt_dia'] )
    kb = str(outObj['Bolt']['k_b'])
    beam_w_t = str(outObj['Bolt']['beam_w_t'] )
    web_plate_t = str(outObj['Bolt']['web_plate_t'])
    beam_fu = str(outObj['Bolt']['beam_fu'])
    dia_hole = str(outObj['Bolt']['dia_hole'])
    web_plate_fy = str(outObj['Plate']['web_plate_fy'])
    weld_fu = str(outObj['Weld']['weld_fu'] )
    weld_l = str(outObj['Weld']['effectiveWeldlength'])
    shearCapacity = str(round(outObj['Bolt']['shearcapacity'],3))
    bearingcapacity = str(round(outObj['Bolt']['bearingcapacity'],4))
    momentDemand = str(outObj['Plate']['externalmoment'])
    
    gap = '20'
    
    ##################output beam part ###########
    shearCapacity_b = str(outputObj['Bolt']['shearcapacity'])  
    bearingcapacity_b = str(outputObj['Bolt']['bearingcapacity']) 
    boltCapacity_b = str(outputObj['Bolt']['boltcapacity'])
    noOfBolts_b = str(outputObj['Bolt']['numofbolts'])
    noOfRows_b =  str(outputObj['Bolt']['numofrow'])
    noOfCol_b = str(outputObj['Bolt']['numofcol'])
    pitch_b = str(outputObj['Bolt']['pitch'])
    edge_b  = str(outputObj['Bolt']['enddist']) 
    end_b   = str(outputObj['Bolt']['edge'])
    gauge_b =  str(outputObj['Bolt']['gauge'])  
    boltGrpCapacity_b =  str(outputObj['Bolt']['boltgrpcapacity'])
    thinner_b = str(outputObj['Bolt']['thinner'])
    ##################output column part ###########
    shearCapacity_c = str(outputObj['cleat']['shearcapacity'])  
    bearingcapacity_c = str(outputObj['cleat']['bearingcapacity']) 
    boltCapacity_c = str(outputObj['cleat']['boltcapacity'])
    noOfBolts_c = str(outputObj['cleat']['numofbolts'])
    noOfRows_c =  str(outputObj['cleat']['numofrow'])
    noOfCol_c = str(outputObj['cleat']['numofcol'])
    pitch_c = str(outputObj['cleat']['pitch'])
    edge_c  = str(outputObj['cleat']['enddist']) 
    end_c   = str(outputObj['cleat']['edge'])
    gauge_c =  str(outputObj['cleat']['gauge'])  
    boltGrpCapacity_c =  str(outputObj['cleat']['boltgrpcapacity'])
    thinner_c = str(outputObj['cleat']['thinner'])
    gap = '20'

    
    
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr = t('table')
    rstr += t('tr')
    row = [0, companylogo,'Created with'' &nbsp'' &nbsp' '<object type= "image/PNG" data= "Osdag_header.png" width= 150></object>']
    rstr += t('td colspan="2" align= "center" class= "viewbl" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" class="viewbl"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0,'Company Name']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0,  'Group/Team Name']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0,  'Subtitle']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Metdod']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')    
    rstr += t('/hr')    

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#Design Conclusion
    rstr += t('table')

    row = [0, "Design Conclusion", "IS800:2007/Limit state design"]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
      
    row = [1, "Cleat Angle", "Pass"]
    rstr += t('tr')
    rstr += t('td class="header1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1 safe"') + row[2] + t('/td')
    #rstr += t('td class="header1 safe"') + row[3] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Cleat Angle", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Connection Properties", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1_1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Connection ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    row = [1, "Connection Title", " Double Angle Cleat Angle"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [1, "Connection Type", "Shear Connection"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Connection Category ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    #row = [1, "Connectivity", "Column Web Beam Web"]
    row = [1, "Connectivity", connectivity]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [1, "Beam Connection", "Bolted"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
 
#     row = [1, "Beam Connection", "Bolted"]
#     rstr += t('tr')
#     rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td class="header2 "') + row[2] + t('/td')
#     rstr += t('/tr')
     
# 
    row = [1, "Column Connection", "Bolted"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Loading (Factored Load) ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    #row = [1, "Shear Force (kN)", "140"]
    row = [1,"Shear Force (kN)", shear_load]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
     
    row = [0, "Components ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    #row = [1, "Column Section", "ISSC 200"]
    row = [1,"Column Section", column_sec]
     
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [2, "Material", "Fe "+beam_fu]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [1, "Beam Section", "ISMB 400"]
    row = [1,"Beam Section",beam_sec]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [2, "Material", "Fe "+beam_fu]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [2, "Hole", "STD"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [1, "Cleat Section ", "ISA 300X10X100 "]
    row = [1, "Cleat Section",cleat_sec]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Thickness (mm)", "10"]
    row = [2, "Thickness (mm)", cleat_thk]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
#     row = [2, "Cleat Leg Size A (mm)", 50]
    row = [2, "Cleat Leg Size B (mm)", cleat_legsize]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
#     row = [2, "Cleat Leg Size B (mm)", 50]
    row = [2, "Cleat Leg Size A (mm)", cleat_legsize_1]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [2, "Hole", "STD"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
     
    row = [1, "Bolts on Beam", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Type", "HSFG"]
    row = [2, "Type", bolt_type]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Grade", "8.8"]
    row = [2, "Grade", bolt_grade]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Diameter (mm)", "20"]
    row = [2, "Diameter (mm)", bolt_dia]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Bolt Numbers", "3"]
    row = [2, "Bolt Numbers", noOfBolts_b]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Columns (Vertical Lines)", "1 "]
    row = [2, "Columns (Vertical Lines)", noOfCol_b]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Bolts Per Column", "3"]
    row = [2, "Bolts Per Column", noOfRows_b]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Gauge (mm)", "0"]
    row = [2, "Gauge (mm)", gauge_b]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Pitch (mm)", "100"]
    row = [2, "Pitch (mm)", pitch_b]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "End Distance (mm)", "50"]
    row = [2, "End Distance (mm)", end_b]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Edge Distance (mm)", "50"]
    row = [2, "Edge Distance (mm)", edge_b]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Bolts on Column", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    #row = [2, "Type", "HSFG"]
    row = [2, "Type", bolt_type]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Grade", "8.8"]
    row = [2, "Grade", bolt_grade]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    #row = [2, "Diameter (mm)", "20"]
    row = [2, "Diameter (mm)", bolt_dia]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Bolt Numbers", "3"]
    row = [2, "Bolt Numbers", noOfBolts_c]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Columns (Vertical Lines)", "1 "]
    row = [2, "Columns (Vertical Lines)", noOfCol_c]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Bolts Per Column", "3"]
    row = [2, "Bolts Per Column", noOfRows_c]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Gauge (mm)", "0"]
    row = [2, "Gauge (mm)", gauge_c]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Pitch (mm)", "100"]
    row = [2, "Pitch (mm)", pitch_c]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "End Distance (mm)", "50"]
    row = [2, "End Distance (mm)", end_c]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + row[2] + t('/td')
    rstr += t('/tr')
     
    #row = [2, "Edge Distance (mm)", "50"]
    row = [2, "Edge Distance (mm)", edge_c]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    row = [0, "Assembly ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    #row = [1, "Column-Beam Clearance (mm)", "20"]
    row = [1, "Column-Beam Clearance (mm)", gap]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    rstr += t('/table')
    rstr += t('h1 class="break"') # page break
    rstr += t('/h1')

#*************************************************************************************************************************
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table')
    rstr += t('tr')
    row = [0, companylogo,'Created with'' &nbsp'' &nbsp' '<object type= "image/PNG" data= "Osdag_header.png" width= 150></object>']
    rstr += t('td colspan="2" align= "center" class= "viewbl" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" class="viewbl"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0,'Company Name']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0,  'Group/Team Name']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0,  'Subtitle']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Metdod']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
    rstr += t('/hr')    

#*************************************************************************************************************************
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#Design Check

    rstr += t('table')
    row = [0, "Design Check: Beam Connectivity    ", " "]
    rstr += t('tr')
    rstr += t('td colspan="4" class="header1_1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    row =[0,"Check","Required","Provided","Remark"]
    rstr += t('td class="header1_2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1_2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header1_2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header1_2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    const = str(round(math.pi/4 *0.78,4))
    #row =[0,"Bolt shear capacity (kN)"," ","<i>V</i><sub>dsb</sub> = ((800*0.6123*20*20)/(&#8730;3*1.25*1000) = 90.53 <br> [cl. 10.3.3]"]
    row =[0,"Bolt shear capacity (kN)"," ", "<i>V</i><sub>dsb</sub> = ((" + bolt_fu + "*" + const + "*" + bolt_dia + "*" + bolt_dia +")/(&#8730;3*1.25*1000) = " + shearCapacity + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*"+ kb +"*" + bolt_dia + "*" + beam_tw +"*"+beam_fu +")/(1.25*1000)  = " + bearingcapacity + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    boltCapacity = bearingcapacity if bearingcapacity < shearCapacity else shearCapacity
    row =[0,"Bolt capacity (kN)","","Min (" + shearCapacity + ", " + bearingcapacity + ") = " + boltCapacity  , "<p align=right style=color:green><b>Pass</b></p>"]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
    bolts = str(round(float(shear_load)/float(boltCapacity),1))
    row =[0,"No. of bolts", shear_load + "/" + boltCapacity + " = " + bolts, noOfBolts, " <p align=right style=color:green><b>Pass</b></p>"]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"No.of column(s)","&#8804;2","1"]
    row =[0,"No.of column(s)"," &#8804;2",noOfCol, ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"No. of bolts per column"," ","3"]
    row =[0,"No. of bolts per column"," ",noOfRows, ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    minPitch =str(int(2.5 * float(bolt_dia)))
    maxPitch = str(300) if 32 * float(beam_tw)> 300 else str(int(math.ceil(32*float(beam_tw))))
    row =[0,"Bolt pitch (mm)"," &#8805;2.5* "+ bolt_dia + " = " + minPitch +",  &#8804;Min(32*"+ beam_tw +", 300) = "+ maxPitch +"<br> [cl. 10.2.2]",pitch, ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    minGauge =str(int(2.5 * float(bolt_dia)))
    maxGauge = str(300) if 32 * float(beam_tw)> 300 else str(int(math.ceil(32*float(beam_tw))))
    row =[0,"Bolt gauge (mm)"," &#8805;2.5*"+ bolt_dia+ " = " +minGauge+", &#8804;Min(32*" + beam_tw + ", 300) = "+ maxGauge + " <br> [cl. 10.2.2]",gauge, ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"End distance (mm)","&#8805;1.7* 22 = 37.4,&#8804;12*8.9 = 106.9 <br> [cl. 10.2.4]","50"]
    minEnd = str(1.7 * float(dia_hole))
    maxEnd = str(12*float(beam_tw))
    row =[0,"End distance (mm)"," &#8805;1.7*" + dia_hole+" = " +minEnd+", &#8804;12*"+beam_tw+" = "+maxEnd+" <br> [cl. 10.2.4]",end, ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Edge distance (mm)","&#8805; 1.7* 22 = 37.4,&#8804;12*8.9 = 106.9<br> [cl. 10.2.4]","50"," <p align=right style=color:green><b>Pass</b></p>"]
    minEdge = str(1.7 * float(dia_hole))
    maxEdge = str(12*float(beam_tw))
    row =[0,"Edge distance (mm)"," &#8805;1.7*"+ dia_hole+ " = "+minEdge+", &#8804;12*"+beam_tw+" = "+maxEdge+"<br> [cl. 10.2.4]",edge," <p align=right style=color:green><b>Pass</b></p>"]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    row = [0, "Block shear capacity (kN)", shear_load, "<i>V</i><sub>db</sub> = "+ blockshear + "<br>", ""] 
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Plate thickness (mm)","(5*140*1000)/(300*250)= 9.33","10"]
    minPlateThick = str(round(5 * float(shear_load) * 1000/(float(plateLength)*float(web_plate_fy)),2))
    row =[0,"Plate thickness (mm)","(5*" + shear_load + "*1000)/(" + plateLength + "*" + plateWidth + ") = "+ minPlateThick,plateThick, ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
     
    rstr += t('tr')
#     if
    minEdge = str(0.6 * float(beamdepth))
    maxEdge = str(float(beamdepth) - float(beamflangethk) - float(beamrootradius) - float(colflangethk)- float(colrootradius) - 5)
    row = [0, "Plate height (mm)", "&#8805;0.6*" + beamdepth+ "=" + minEdge+ ", &#8804;" + beamdepth+ "-"+beamflangethk+ "-"+beamrootradius+"-"+colflangethk+"-"+colrootradius+"- 5" "="+maxEdge+"<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]",edge," <p align=right style=color:green><b>Pass</b></p>","300", ""]
#     else
#     minEdge = str(0.6 * float(beamdepth))
#     maxEdge = str(float(beamdepth)- 2*float(beamflangethk)- 2*float(beamrootradius)- 10)
#     row =[0,"Plate height (mm)"," &#8805;0.6*"+ beamdepth+ " = "+minEdge+", &#8804;"+beamdepth +"-"+ " 2*"+beamflangethk+ "-" + " 2*"+beamrootradius+ "-"+" 10" " = "+maxEdge+"<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]",edge," <p align=right style=color:green><b>Pass</b></p>","300", ""]
    #row =[0,"Plate height (mm)","",plateLength]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    row =[0,"Plate width (mm)","","100", ""]
    #row =[0,"Plate width (mm)","",plateWidth]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Plate moment capacity (kNm)","(2*90.5*100<sup>2</sup>)/100 = 18.1","<i>M</i><sub>d</sub> =1.2*250*<i>Z</i> = 40.9 <br>[cl. 8.2.1.2]","<p align=right style=color:green><b>Pass</b></p>"]
    z = math.pow(float(plateLength),2)* (float(plateThick)/(6 *1.1* 1000000))
    momentCapacity = str(round(1.2 * float(web_plate_fy)* z,2))
    row =[0,"Plate moment capacity (kNm)","(2*"+shearCapacity+"*"+pitch+"<sup>2</sup>)/("+pitch+"*1000) = "+ moment_demand,"<i>M</i><sub>d</sub> = (1.2*" +web_plate_fy+"*<i>Z</i>)/(1000*1.1) = "+ momentCapacity +"<br>[cl. 8.2.1.2]","<p align=right style=color:green><b>Pass</b></p>"]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Effective weld length (mm)","","300 - 2*6 = 288"]
    effWeldLen = str(int(float(plateLength)-(2*float(weld_Thick))))
    row =[0,"Effective weld length (mm)","",  plateLength + "-2*" + weld_Thick +" = " + effWeldLen, ""]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Weld strength (kN/mm)","&#8730;[(18100*6)/(2*288)<sup>2</sup>]<sup>2</sup> + [140/(2*288)]<sup>2</sup> <br>=0.699","<i>f</i><sub>v</sub>=(0.7*6*410)/(&#8730;3*1.25)<br>= 0.795<br>[cl. 10.5.7]"," <p align=right style=color:green><b>Pass</b></p>"]
    a = float(2*float(effWeldLen))
    b = 2*math.pow((float(effWeldLen)),2)
    x = (float(momentDemand) * 1000 * 6)
    resultant_shear = str(round(math.sqrt(math.pow((x/b),2) + math.pow((float(shear_load)/a),2)),3))
    momentDemand_knmm = str(int(float(momentDemand) * 1000))
    row =[0,"Weld strength (kN/mm)"," &#8730;[("+momentDemand_knmm+"*6)/(2*"+effWeldLen+"<sup>2</sup>)]<sup>2</sup> + ["+shear_load+"/(2*"+effWeldLen+")]<sup>2</sup> <br>= "+ resultant_shear ,"<i>f</i><sub>v</sub>= (0.7*"+weldSize+"*"+weld_fu+")/(&#8730;3*1.25)<br>= "+ weld_strength+"<br>[cl. 10.5.7]"," <p align=right style=color:green><b>Pass</b></p>"]
    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    #row =[0,"Weld thickness (mm)","(0.699*&#8730;3*1.25)/(0.7*410)=5.27<br>[cl. 10.5.7]","6","<p align=right style=color:green><b>Pass</b></p>"]
    weld_thickness = str(round((float(resultant_shear) * 1000*(math.sqrt(3) * 1.25))/(0.7 * float(weld_fu)),2))
    x = str((float( platethk)*0.8))
#     maxWeld = str(9) if str(round((float(resultant_shear) * 1000*(math.sqrt(3) * 1.25))/(0.7 * float(weld_fu)),2)) == 9 else str((float( platethk)*0.8))
#     row =[0,"Weld thickness (mm)","Max(("+resultant_shear+"*&#8730;3*1.25)/(0.7*"+weld_fu+")"+", 0.8*"+platethk+") = "+ maxWeld + "<br>[cl. 10.5.7, Insdag Detailing Manual, 2002]",weldSize,"<p align=right style=color:green><b>Pass</b></p>"]
#     row =[0,"Weld thickness (mm)","max("+weld_thickness + ","+ x +") = " "<br>[cl. 10.5.7, Insdag Detailing Manual, 2002]",weldSize,"<p align=right style=color:green><b>Pass</b></p>"]

    rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
        
    rstr += t('/table')
    rstr += t('h1 class="break"') # page break
    rstr += t('/h1')

#*************************************************************************************************************************
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table')
    rstr += t('tr')
    row = [0, companylogo,'Created with'' &nbsp' '<object type= "image/PNG" data= "Osdag_header.png" width= 150></object>']
    rstr += t('td colspan="2" align= "center" class= "viewbl" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" class="viewbl1"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0,'Company Name']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0,  'Group/Team Name']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0,  'Subtitle']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Metdod']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
    rstr += t('/hr')    

#*************************************************************************************************************************
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#Digram

    rstr += t('table')

    row = [0, "Views", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class=" viewtbl header1_1"') + space(row[0]) + row[1] + t('/td')
    #rstr += t('td class=" viewtbl "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [0, '<object type="image/PNG" data="3D_Model.png" width ="550"></object>', '<object type="image/PNG" data="finTop.png" width ="480"></object>']
    rstr += t('tr')
    rstr += t('td  align="center" class=" viewtbl"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td  align="center" class=" viewtbl"') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [0, '<object type="image/PNG" data="finSide.png" width ="480"></object>', '<object type="image/PNG" data="finFront.png" width ="480"></object>']
    rstr += t('tr')
    rstr += t('td align="center" class=" viewtbl"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td align="center" class=" viewtbl "') + row[2] + t('/td')
    rstr += t('/tr')
    
    rstr += t('/table')
    rstr += t('h1 class="break"') # page break
    rstr += t('/h1')

#*************************************************************************************************************************
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table')
    rstr += t('tr')
    row = [0, companylogo,'Created with'' &nbsp'' &nbsp' '<object type= "image/PNG" data= "Osdag_header.png" width= 150></object>']
    rstr += t('td colspan="2" align= "center" class= "viewbl" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" class="viewbl"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0,'Company Name']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0,  'Group/Team Name']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0,  'Subtitle']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Metdod']
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "header1_3"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
    rstr += t('/hr')    

#*************************************************************************************************************************
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#Additional comments

    rstr += t('table')
    rstr += t('''col width=30%''')
    rstr += t('''col width=70%''')
    
    rstr += t('tr')
    row = [0, "Additional Comments",addtionalcomments]
    rstr += t('td class= "header2_col1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class= "header3" align="justified"') + row[2] + t('/td')
    rstr += t('/tr')
    
    rstr += t('/table')
    
    
    myfile.write(rstr)
    myfile.write(t('/body'))
    myfile.write(t('/html'))
    myfile.close()
    
def space(n):
    rstr = "&nbsp;" * 4 * n
    return rstr

def t(n):
    return '<' + n + '/>'

def quote(m):
    return '"' + m + '"'


# reportsummary = useUserProfile()
# print reportsummary
# save_html(outObj, uiObj, dictBeamData, dictColData)


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#COnverting HTML to PDF
# pdfkit.from_file('output/reshma.html','output/reshmaReport.pdf')
# print "PDF generated"



