'''
Created on 07-May-2015
comment

@author: aravind
'''
from OCC import IGESControl
from OCC import VERSION, BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Display.pyqt4Display import qtViewer3d
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from OCC.IFSelect import IFSelect_RetDone
from OCC.Interface import Interface_Static_SetCVal
from OCC.Quantity import Quantity_NOC_RED, Quantity_NOC_BLUE1, Quantity_NOC_SADDLEBROWN
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.StlAPI import StlAPI_Writer
from OCC.TopoDS import topods, TopoDS_Shape
from OCC.gp import gp_Pnt
from PyQt4.Qt import QPrinter, QDialog
from PyQt4.QtCore import QString, pyqtSignal
from PyQt4.QtGui import QWidget
from PyQt4.QtWebKit import *
import os.path
import pickle
import svgwrite
import yaml


from ISection import ISection
from angle import Angle
from beamWebBeamWebConnectivity import BeamWebBeamWeb
from bolt import Bolt
from cleatCalc import cleatAngleConn
from colFlangeBeamWebConnectivity import ColFlangeBeamWeb
from colWebBeamWebConnectivity import ColWebBeamWeb
# from ui_popUpDialog import Ui_Dialog
from ui_popUpWindowR01 import Ui_Capacitydetals
from drawing2D import *
from drawing_2D import Fin2DCreatorFront
from model import *
from notch import Notch
from nut import Nut 
from nutBoltPlacement import NutBoltArray
from ui_cleatAngleR04 import Ui_MainWindow
from utilities import osdagDisplayShape


# Developed by aravind
class myDialog(QDialog, Ui_Capacitydetals):     
      
    def __init__(self, parent = None): 
        QDialog.__init__(self, parent)
        self.ui = Ui_Capacitydetals()
        self.ui.setupUi(self)
        
        m = MainController()
        x = m.outputdict()
        self.ui.shear_b.setText(str(x['Bolt']['shearcapacity']))
        self.ui.bearing_b.setText(str(x['Bolt']['bearingcapacity']))
        self.ui.capacity_b.setText(str(x['Bolt']['boltcapacity']))
        self.ui.boltGrp_b.setText(str(x['Bolt']['boltgrpcapacity']))
        #Column
        self.ui.shear.setText(str(x['Bolt']['shearcapacity']))
        self.ui.bearing.setText(str(x['Bolt']['bearingcapacity']))
        self.ui.capacity.setText(str(x['Bolt']['boltcapacity']))
        self.ui.boltGrp.setText(str(x['Bolt']['boltgrpcapacity']))
        #Cleat
        self.ui.mDemand.setText(str(x['cleat']['externalmoment']))
        self.ui.mCapacity.setText(str(x['cleat']['momentcapacity']))
        
        


class MainController(QtGui.QMainWindow):
    
    closed = pyqtSignal()
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
#         QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
#         self.uiPopUp = Ui_Dialog()
#         self.uiPopUp.setupUi(self)
        
        self.ui.combo_Beam.addItems(get_beamcombolist())
        self.ui.comboColSec.addItems(get_columncombolist())
        self.ui.comboCleatSection.addItems(get_anglecombolist())
        
        self.ui.inputDock.setFixedSize(310,710)
        
        self.gradeType ={'Please Select Type':'',
                         'HSFG': [8.8,10.8],
                         'Black Bolt':[3.6,4.6,4.8,5.6,5.8,6.8,9.8,12.9]}
        self.ui.comboBoltType.addItems(self.gradeType.keys())
        self.ui.comboBoltType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboBoltType.setCurrentIndex(0)
        
        
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()
        #Adding GUI changes for beam to beam connection
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convertColComboToBeam)
        ############################
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
#         self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock)) #USE WHEN ui_cleatAngle.py is used(btnOutput = toolButton)
       
        self.ui.toolButton.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.ui.btn_front.clicked.connect(lambda:self.call_2d_Drawing("Front"))
        self.ui.btn_top.clicked.connect(lambda:self.call_2d_Drawing("Top"))
        self.ui.btn_side.clicked.connect(lambda:self.call_2d_Drawing("Side"))
        
        self.ui.btn3D.clicked.connect(lambda:self.call_3DModel(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
#         self.ui.chkBxFinplate.clicked.connect(self.call_3DFinplate)
        self.ui.checkBoxCleat.clicked.connect(self.call_3DFinplate)
        
        validator = QtGui.QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)
        
        dbl_validator = QtGui.QDoubleValidator()
        self.ui.txtInputCleatHeight.setValidator(dbl_validator)
        self.ui.txtInputCleatHeight.setMaxLength(7)
        self.ui.txtShear.setValidator(dbl_validator)
        self.ui.txtShear.setMaxLength(7)
        
        minfuVal = 290
        maxfuVal = 590
        self.ui.txtFu.editingFinished.connect(lambda: self.check_range(self.ui.txtFu,self.ui.lbl_fu, minfuVal, maxfuVal))
        
        minfyVal = 165
        maxfyVal = 450
        self.ui.txtFy.editingFinished.connect(lambda: self.check_range(self.ui.txtFy,self.ui.lbl_fy, minfyVal, maxfyVal))
       
         ##### MenuBar #####
#         self.ui.actionQuit_cleat_angle_design.setShortcut('Ctrl+Q')
#         self.ui.actionQuit_cleat_angle_design.setStatusTip('Exit application')
#         self.ui.actionQuit_cleat_angle_design.triggered.connect(QtGui.qApp.quit)
         
        self.ui.actionCreate_design_report.triggered.connect(self.save_design)
        self.ui.actionSave_log_message.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.showFontDialogue)
        self.ui.actionZoom_in.triggered.connect(self.callZoomin)
        self.ui.actionZoom_out.triggered.connect(self.callZoomout)
        self.ui.actionSave_3D_model_as.triggered.connect(self.save3DcadImages)
        self.ui.actionSave_CAD_image.triggered.connect(self.save2DcadImages)
        self.ui.actionSave_Front_View.triggered.connect(lambda:self.call_2d_Drawing("Front"))
        self.ui.actionSave_Side_View.triggered.connect(lambda:self.call_2d_Drawing("Side"))
        self.ui.actionSave_Top_View.triggered.connect(lambda:self.call_2d_Drawing("Top"))
        self.ui.actionPan.triggered.connect(self.call_Pannig)
        
        
        self.ui.actionShow_beam.triggered.connect(self.call_3DBeam)
        self.ui.actionShow_column.triggered.connect(self.call_3DColumn)
        self.ui.actionShow_cleat_angle.triggered.connect(self.call_3DFinplate)
        self.ui.actionChange_background.triggered.connect(self.showColorDialog)
        ###############################MARCH_14#############################
        #populate cleat section and secondary beam according to user input

        self.ui.comboColSec.currentIndexChanged[int].connect(lambda:self.fillCleatSectionCombo())
        self.ui.combo_Beam.currentIndexChanged[str].connect(self.checkBeam_B)
        self.ui.comboColSec.currentIndexChanged[str].connect(self.checkBeam_B)
#         self.ui.txtInputCleatHeight.currentText.connect(self.checkCleatHeight())
#         cleatHeight = self.ui.txtInputCleatHeight.currentText()
#         if cleatHeight != 0:
#             self.
        self.ui.txtInputCleatHeight.editingFinished.connect(lambda: self.checkCleatHeight(self.ui.txtInputCleatHeight))

        
        ######################################################################################
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.save_design)#Saves the create design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)
        #################################################################
        self.ui.btn_capacity.clicked.connect(self.showButton_clicked)
        
        #################################################################
        
        
        # Saving and Restoring the finPlate window state.
        #self.retrieve_prevstate()
        
#         self.ui.btnZmIn.clicked.connect(self.callZoomin)
#         self.ui.btnZmOut.clicked.connect(self.callZoomout)
#         self.ui.btnRotatCw.clicked.connect(self.callRotation)
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        
        # Initialising the qtviewer
        self.display,_ = self.init_display(backend_str="pyqt4")
        
#         self.ui.btnSvgSave.clicked.connect(self.save3DcadImages)
        #self.ui.btnSvgSave.clicked.connect(lambda:self.saveTopng(self.display))
        
        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()
    
    
  
    
    def showButton_clicked(self):
        self.dialog = myDialog(self)
        self.dialog.show()
        
#         self.dialog = myDialog(self)
#         self.dialog.show()
        

    def fetchBeamPara(self):
        beam_sec = self.ui.combo_Beam.currentText()
        dictbeamdata  = get_beamdata(beam_sec)
        return dictbeamdata
    
    def fetchColumnPara(self):
        column_sec = self.ui.comboColSec.currentText()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            dictcoldata = get_beamdata(column_sec)
        else:
            dictcoldata = get_columndata(column_sec)
        return dictcoldata
    def fetchAnglePara(self):
        angle_sec = self.ui.comboCleatSection.currentText()
        dictangledata = get_angledata(angle_sec)
        return dictangledata

    def convertColComboToBeam(self):

        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            self.ui.beamSection_lbl.setText(" Secondary beam *")
            self.ui.columnSection_lbl.setText("Primary beam *")
            
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl_3.setFont(font)
            self.ui.outputBoltLbl_3.setText("Primary beam")
            self.ui.outputBoltLbl.setText("Secondary beam")
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl.setFont(font)
             

            
            self.ui.comboColSec.clear()
            self.ui.comboColSec.addItems(get_beamcombolist())
            
        elif loc == "Column web-Beam web" or loc == "Column flange-Beam web":
            
            self.ui.columnSection_lbl.setText("Column Section *")
            self.ui.beamSection_lbl.setText("Beam section *")
            self.ui.outputBoltLbl_3.setText("Column")
            self.ui.outputBoltLbl.setText("Beam")


            self.ui.comboColSec.clear()
            self.ui.comboColSec.addItems(get_columncombolist())
            
            self.ui.combo_Beam.setCurrentIndex(0)
            self.ui.comboColSec.setCurrentIndex(0)
    
    cleatAngleConn
    def fillCleatSectionCombo(self):
            
        '''Populates the cleat section on the basis  beam section and column section
        '''
         
        if self.ui.combo_Beam.currentText() == "Select Designation" or self.ui.comboColSec.currentText() == "Select Column":
            self.ui.comboCleatSection.setCurrentIndex(0)
        loc = self.ui.comboConnLoc.currentText() 
        if loc == "Column web-Beam web" or "Column flange-Beam web" : 
            loc = self.ui.comboConnLoc.currentText()
            dictbeamdata = self.fetchBeamPara()
            dictcoldata = self.fetchColumnPara()
            angleList = get_anglecombolist()
            col_D = float(dictcoldata[QString("D")])
            col_B = float(dictcoldata[QString("B")])
            col_T = float(dictcoldata[QString("T")])
            beam_tw = float(dictbeamdata[QString("tw")])
            
            if loc == "Column web-Beam web":
                colWeb = col_D - 2 * col_T
            elif loc == "Column flange-Beam web":
                colWeb = col_B
            newlist = ['Select Cleat']
                   
            for ele in angleList[1:]:
                angle_sec =  QtCore.QString(str(ele))
                dictAngleData = get_angledata(angle_sec)
                cleatLegsize_B = float(dictAngleData[QtCore.QString('B')])
                conLegsize  = 2 * cleatLegsize_B + beam_tw
                space = colWeb - conLegsize
                if space > 0 :
                    newlist.append(str(ele))
                else:
                    break
             
            self.ui.comboCleatSection.blockSignals(True)
                
            self.ui.comboCleatSection.clear()
            for i in newlist[:]:
                self.ui.comboCleatSection.addItem(str(i))
        
            self.ui.comboCleatSection.setCurrentIndex(-1)    
        
            self.ui.comboCleatSection.blockSignals(False)    
            self.ui.comboCleatSection.setCurrentIndex(0)
        else:
            pass   
            
     
    
             
               
    def checkBeam_B(self):
        loc = self.ui.comboConnLoc.currentText()
        if loc  == "Column web-Beam web":
#             if self.ui.comboColSec.currentIndex()== 0:
#                 QtGui.QMessageBox.about(self,"Information", "Please select column section")
#                 return
            column = self.ui.comboColSec.currentText()
          
            dictBeamData = self.fetchBeamPara()
            dictColData = self.fetchColumnPara()
            column_D = float(dictColData[QString("D")])
            column_T = float(dictColData[QString("T")])
            column_R1 = float(dictColData[QString("R1")])
            columnWebDepth = column_D - 2.0 *( column_T)
            
            beam_B = float(dictBeamData[QString('B')])
            
            if columnWebDepth <= beam_B:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self,'Information',"Beam flange is wider than clear depth of column web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)
        elif loc == "Beam-Beam":
#             if self.ui.comboColSec.currentIndex()== 0 or self.ui.combo_Beam.currentIndex()==0:
#                 QtGui.QMessageBox.about(self,"Information", "Please select column section")
#                 return
            primaryBeam = self.ui.comboColSec.currentText()
            dictSBeamData = self.fetchBeamPara()
            dictPBeamData = self.fetchColumnPara()
            PBeam_D = float(dictPBeamData[QString("D")])
            PBeam_T = float(dictPBeamData[QString("T")])
            PBeamWebDepth = PBeam_D - 2.0 *( PBeam_T)
            
            SBeam_D = float(dictSBeamData[QString("D")])
            
            if PBeamWebDepth <= SBeam_D:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self,'Information',"Secondary beam depth is higher than clear depth of primary beam web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)
    def checkCleatHeight(self,widget):
        loc = self.ui.combo_Beam.currentText()
        cleatHeight = widget.text()
        val = int(cleatHeight) 
        if cleatHeight == 0:
            pass
        else:
            column = self.ui.comboColSec.currentText()
            dictBeamData = self.fetchBeamPara()
            beam_D = float(dictBeamData[QString('D')])
            beam_T = float(dictBeamData[QString('T')])
            beam_R1 = float(dictBeamData[QString('R1')])
            clearDepth = 0.0
            if loc  == "Column web-Beam web" or loc == "Column flange-Beam web":
                clearDepth = beam_D - 2 * (beam_T + beam_R1)
            else:
                clearDepth = beam_D - (50 + beam_R1 + beam_T) 
                      
            if clearDepth <= cleatHeight:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self,'Information',"Height of the Cleat Angle exceeding the clear Depth of the Beam)")
            else:
                self.ui.btn_Design.setDisabled(False)
             
                

    def showFontDialogue(self):
        
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.ui.inputDock.setFont(font)
            self.ui.outputDock.setFont(font)
            self.ui.textEdit.setFont(font)
            
    def showColorDialog(self):
      
        col = QtGui.QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        self.display.set_bg_gradient_color(r,g,b,255,255,255)
        
    def callZoomin(self):
        self.display.ZoomFactor(2)
        
    def callZoomout(self):
        self.display.ZoomFactor(0.5)
        
    def callRotation(self):
        self.display.Rotation(15,0)
    def call_Pannig(self):
        self.display.Pan(50,0)
    
        
    def save2DcadImages(self):
        files_types = "PNG (*.png);;JPG (*.jpg);;GIF (*.gif)"
        fileName  = QtGui.QFileDialog.getSaveFileName(self, 'Export', "/home/aravind/Cadfiles/untitled.png", files_types )
        fName = str(fileName)
        file_extension = fName.split(".")[-1]
        
        if file_extension == 'png' or file_extension == 'jpg' or file_extension == 'gif':
            self.display.ExportToImage(fName)
        QtGui.QMessageBox.about(self,'Information',"File saved")
            
    
    def disableViewButtons(self):
        '''
        Disables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(False)
        self.ui.btn_top.setEnabled(False)
        self.ui.btn_side.setEnabled(False)
        
        self.ui.btn3D.setEnabled(False)
        self.ui.chkBxBeam.setEnabled(False)
        self.ui.chkBxCol.setEnabled(False)
        self.ui.checkBoxCleat.setEnabled(False)
    
    def enableViewButtons(self):
        '''
        Enables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(True)
        self.ui.btn_top.setEnabled(True)
        self.ui.btn_side.setEnabled(True)
        
        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.checkBoxCleat.setEnabled(True)
    
    def retrieve_prevstate(self):
        uiObj = self.get_prevstate()
        if(uiObj != None):
            
            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiObj['Member']['Connectivity'])))
            
            if uiObj['Member']['Connectivity'] == 'Beam-Beam':
                self.ui.beamSection_lbl.setText('Secondary beam *')
                self.ui.columnSection_lbl.setText('Primary beam *')
                self.ui.comboColSec.addItems(get_beamcombolist())
            
            self.ui.combo_Beam.setCurrentIndex(self.ui.combo_Beam.findText(uiObj['Member']['BeamSection']))
            self.ui.comboColSec.setCurrentIndex(self.ui.comboColSec.findText(uiObj['Member']['ColumSection']))
            
            
            self.ui.txtFu.setText(str(uiObj['Member']['fu (MPa)']))
            self.ui.txtFy.setText(str(uiObj['Member']['fy (MPa)']))
           
            
            self.ui.txtShear.setText(str(uiObj['Load']['ShearForce (kN)']))
            
            self.ui.comboDiameter.setCurrentIndex(self.ui.comboDiameter.findText(str(uiObj['Bolt']['Diameter (mm)'])))
            comboTypeIndex = self.ui.comboBoltType.findText(str(uiObj['Bolt']['Type']))
            self.ui.comboBoltType.setCurrentIndex(comboTypeIndex)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['Type']))
            
            prevValue = str(uiObj['Bolt']['Grade'])
        
            comboGradeIndex = self.ui.comboBoltGrade.findText(prevValue)
          
            self.ui.comboBoltGrade.setCurrentIndex(comboGradeIndex)
        
            self.ui.txtInputCleatHeight.setText(str(uiObj['cleat']['Height (mm)']))     
            self.ui.comboCleatSection.setCurrentIndex(self.ui.comboCleatSection.findText(str(uiObj['cleat']['section'])))
        
    def setimage_connection(self):
        '''
        Setting image to connctivity.
        '''
        self.ui.lbl_connectivity.show()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column flange-Beam web":
            
            #pixmap = QtGui.QPixmap(":/newPrefix/images/beam2.jpg")
            pixmap = QtGui.QPixmap(":/ResourceFiles/images/colF2.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
            #self.ui.lbl_connectivity.show()
        elif(loc == "Column web-Beam web"):
            #picmap = QtGui.QPixmap(":/newPrefix/images/beam.jpg")
            picmap = QtGui.QPixmap(":/ResourceFiles/images/colW3.png")
            picmap.scaledToHeight(60)
            picmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(picmap)
        else:
            self.ui.lbl_connectivity.hide()
            
    def getuser_inputs(self):
        '''(nothing) -> Dictionary
        
        Returns the dictionary object with the user input fields for designing cleat angle connection
        
        '''
        uiObj = {}
        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText().toInt()[0]
        uiObj["Bolt"]["Grade"] = float(self.ui.comboBoltGrade.currentText())  
#         uiObj["Bolt"]["Grade"] = 8.8                                                                                                                                                                                                                                                             
        uiObj["Bolt"]["Type"] = str(self.ui.comboBoltType.currentText())
        
                    
        uiObj['Member'] = {}
        uiObj['Member']['BeamSection'] = str(self.ui.combo_Beam.currentText())
        uiObj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        uiObj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiObj['Member']['fu (MPa)'] = self.ui.txtFu.text().toInt()[0]
        uiObj['Member']['fy (MPa)'] = self.ui.txtFy.text().toInt()[0]
        
        uiObj['cleat'] = {}
        uiObj['cleat']['section'] = str(self.ui.comboCleatSection.currentText())
        uiObj['cleat']['Height (mm)'] = float(self.ui.txtInputCleatHeight.text().toInt()[0]) # changes the label length to height 

        uiObj['Load'] = {}
        uiObj['Load']['ShearForce (kN)'] = float(self.ui.txtShear.text().toInt()[0])
        
        
        
        return uiObj    
        
    def save_inputs(self,uiObj):
         
        '''(Dictionary)--> None
         
        '''
        inputFile = QtCore.QFile('saveINPUT.txt')
        if not inputFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        #yaml.dump(uiObj, inputFile,allow_unicode=True, default_flow_style = False)
        pickle.dump(uiObj, inputFile)
        
    
    def get_prevstate(self):
        '''
        '''
        fileName = 'saveINPUT.txt'
         
        if os.path.isfile(fileName):
            fileObject = open(fileName,'r')
            uiObj = pickle.load(fileObject)
            return uiObj
        else:
            return None
    
            
    def outputdict(self):
        
        ''' Returns the output of design in dictionary object.
        '''
        
        uiObj = self.getuser_inputs()
        outputobj = cleatAngleConn(uiObj)
        
        return outputobj
#         outObj = {}
#         outObj['cleat'] ={}
#         outObj['cleat']["height"] = float(self.ui.outputCleatHeight.text())
# #         outObj['cleat']["External Moment (kN-m)"] = float(self.ui.txtExtMomnt.text())
#         outObj['cleat']["External Moment (kN-m)"] = self.ui.txtExtMomnt.text()
#         outObj['cleat']["Moment Capacity (kN-m)"] = float(self.ui.txtMomntCapacity.text())
#         
# #         outObj['Weld'] ={}
# #         #outObj['Weld']["Weld Thickness(mm)"] = float(self.ui.txtWeldThick.text())
# #         outObj['Weld']["Resultant Shear (kN/mm)"] = float(self.ui.txtResltShr.text())
# #         outObj['Weld']["Weld Strength (kN/mm)"] = float(self.ui.txtWeldStrng.text())
#         
#         outObj['Bolt'] = {}
#         outObj['Bolt']["Shear Capacity (kN)"] = float(self.ui.txtShrCapacity.text())
#         outObj['Bolt']["Bearing Capacity (kN)"] = float(self.ui.txtbearCapacity.text())
#         outObj['Bolt']["Capacity Of Bolt (kN)"] = float(self.ui.txtBoltCapacity.text())
#         outObj['Bolt']["No Of Bolts"] = float(self.ui.txtNoBolts.text())
#         outObj['Bolt']["No.Of Row"] = int(self.ui.txt_row.text())
#         outObj['Bolt']["No.Of Column"] = int(self.ui.txt_col.text())
#         outObj['Bolt']["Pitch Distance (mm)"] = float(self.ui.txtBeamPitch.text())
#         outObj['Bolt']["Guage Distance (mm)"] = float(self.ui.txtBeamGuage.text())
#         outObj['Bolt']["End Distance (mm)"]= float(self.ui.txtEndDist.text())
#         outObj['Bolt']["Edge Distance (mm)"]= float(self.ui.txtEdgeDist.text())
#         
#         return outObj
    
    
    def save_design(self):
        fileName,pat =QtGui.QFileDialog.getSaveFileNameAndFilter(self,"Save File As","output/finplate/","All Files (*);;Html Files (*.html)")
        self.call_2d_Drawing("All")
        self.outdict = self.resultObj#self.outputdict()
        self.inputdict = self.uiObj#self.getuser_inputs()
        #self.save_yaml(self.outdict,self.inputdict)
        dictBeamData  = self.fetchBeamPara()
        dictColData  = self.fetchColumnPara()
#         save_html(self.outdict, self.inputdict, dictBeamData, dictColData,fileName)
#         self.htmlToPdf()
        
        QtGui.QMessageBox.about(self,'Information',"Report Saved")
    
        #self.save(self.outdict,self.inputdict)cleatAngleConn
        
    def save_log(self):
        
        fileName,pat =QtGui.QFileDialog.getSaveFileNameAndFilter(self,"Save File As","/home/aravind/Desktop/eclipseWorkspace/osdag/cleatAngle/SaveMessages","Text files (*.txt)")
        return self.save_file(fileName+".txt")
          
    def save_file(self, fileName):
        '''(file open for writing)-> boolean
        '''
        fname = QtCore.QFile(fileName)
        
        if not fname.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (fileName, fname.errorString()))
            return False

        outf = QtCore.QTextStream(fname)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        #self.setCurrentFile(fileName);
        
        #QtGui.QMessageBox.about(self,'Information',"File saved")
       
    
    ################
    def save_yaml(self,outObj,uiObj):
        '''(dictiionary,dictionary) -> NoneType
        Saving input and output to file in following format.
        Bolt:
          diameter: 6
          grade: 8.800000190734863
          type: HSFG
        Load:
          shearForce: 100
          
        '''
        newDict = {"INPUT": uiObj, "OUTPUT": outObj} 
        fileName = QtGui.QFileDialog.getSaveFileName(self,"Save File As","/home/aravind/Desktop/eclipseWorkspace/osdag/cleatAngle/SaveDesign","Text File (*.txt)")
        f = open(fileName,'w')
        yaml.dump(newDict,f,allow_unicode=True, default_flow_style=False)
        
        #return self.save_file(fileName+".txt")
        #QtGui.QMessageBox.about(self,'Information',"File saved")
        
    def htmlToPdf(self):
        
        self.web.load(QtCore.QUrl("file:///home/deepa/EclipseWorkspace/OsdagLive/output/finplate/finPlateReport.html"))
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setColorMode(QPrinter.Color)
        printer.setOutputFileName("output/finplate/designReport.pdf")
        
        def convertIt():
            self.web.print_(printer)
          
        QtCore.QObject.connect(self.web, QtCore.SIGNAL("loadFinished(bool)"), convertIt)

        
    def resetbtn_clicked(self):
        '''(NoneType) -> NoneType
        
        Resets all fields in input as well as output window
    
        '''
        # user Inputs
        self.ui.combo_Beam.setCurrentIndex((0))
        self.ui.comboColSec.setCurrentIndex((0))
        self.ui.comboConnLoc.setCurrentIndex((0))
        self.ui.txtFu.clear()
        self.ui.txtFy.clear()
        
        self.ui.txtShear.clear()
        
        self.ui.comboDiameter.setCurrentIndex(0)
        self.ui.comboBoltType.setCurrentIndex((0))
        self.ui.comboBoltGrade.setCurrentIndex((0))
        
        self.ui.comboCleatSection.setCurrentIndex((0))
        self.ui.txtInputCleatHeight.clear()
#         self.ui.txtPlateWidth.clear()
        
#         self.ui.comboWldSize.setCurrentIndex((0))
        
        #----Output
#         self.ui.txtShrCapacity.clear()
#         self.ui.txtbearCapacity.clear()
#         self.ui.txtBoltCapacity.clear()
        self.ui.txtNoBolts.clear()
#         self.ui.txtBoltGrpCapacity.clear()
        self.ui.txt_row.clear()
        self.ui.txt_column.clear()
        self.ui.txtBeamPitch.clear()
        self.ui.txtBeamGuage.clear()
        self.ui.txtEndDist.clear()
        self.ui.txtEdgeDist.clear()
        
        #column
        self.ui.txtNoBolts_c.clear()
        self.ui.txt_row_c.clear()
        self.ui.txt_column_c.clear()
        self.ui.txtBeamPitch_c.clear()
        self.ui.txtBeamGuage_c.clear()
        self.ui.txtEndDist_c.clear()
        self.ui.txtEdgeDist_c.clear()
        
        #self.ui.txtPlateThick.clear()
        self.ui.outputCleatHeight.clear()
#         self.ui.txtplate_width.clear()
#         self.ui.txtExtMomnt.clear()
#         self.ui.txtMomntCapacity.clear()
        
        #self.ui.txtWeldThick.clear()
#         self.ui.txtResltShr.clear()
#         self.ui.txtWeldStrng.clear()
        self.ui.textEdit.clear()
        
        #------ Erase Display
        self.display.EraseAll()
        
    def dockbtn_clicked(self,widget):
        
        '''(QWidget) -> NoneType
        
        This method dock and undock widget(QdockWidget)
        '''
        
        flag = widget.isHidden()
        if(flag):
            
            widget.show()
        else:
            widget.hide()
            
    def  combotype_currentindexchanged(self,index):
        
        '''(Number) -> NoneType
        '''
        items = self.gradeType[str(index)]

        self.ui.comboBoltGrade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))
            
        self.ui.comboBoltGrade.addItems(strItems)
        
        
    def check_range(self, widget,lblwidget, minVal, maxVal):
        
        '''(QlineEdit,QLable,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yeild Strength) textfields
        '''
        textStr = widget.text()
        val = int(textStr) 
        if( val < minVal or val > maxVal):
            QtGui.QMessageBox.about(self,'Error','Please Enter a value between %s-%s' %(minVal, maxVal))
            widget.clear()
            widget.setFocus()
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QtGui.QPalette()
            lblwidget.setPalette(palette)
            
    def display_output(self, outputObj):
        '''(dictionary) --> NoneType
        Setting design result values to the respective textboxes in the output window
        '''
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                if (outputObj[k][key] == ""):
                    resultObj = outputObj
                else:
                    resultObj = outputObj
                    
        # resultObj['Bolt']
        shear_capacity = resultObj['Bolt']['shearcapacity']
#         self.uiPopUp.lineEdit_companyName.setText(str(shear_capacity))
        
        bearing_capacity = resultObj['Bolt']['bearingcapacity']
#         self.ui.txtbearCapacity.setText(str(bearing_capacity))
        
        bolt_capacity = resultObj['Bolt']['boltcapacity']
#         self.ui.txtBoltCapacity.setText(str(bolt_capacity))
        
        no_ofbolts = resultObj['Bolt']['numofbolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        #newly added field
        boltGrp_capacity = resultObj['Bolt']['boltgrpcapacity']
#         self.ui.txtBoltGrpCapacity.setText(str(boltGrp_capacity))
        
        no_ofrows = resultObj['Bolt']['numofrow']
        self.ui.txt_row.setText(str(no_ofrows))
        
        no_ofcol = resultObj['Bolt']['numofcol']
        self.ui.txt_column.setText(str(no_ofcol))
        
        pitch_dist = resultObj['Bolt']['pitch']
        self.ui.txtBeamPitch.setText(str(pitch_dist))
        
        gauge_dist = resultObj['Bolt']['gauge']
        self.ui.txtBeamGuage.setText(str(gauge_dist))
        
        end_dist = resultObj['Bolt']['enddist']
        self.ui.txtEndDist.setText(str(end_dist))
        
        edge_dist = resultObj['Bolt']['edge']
        self.ui.txtEdgeDist.setText(str(edge_dist))
        #column 
        c_noOfBolts = resultObj['cleat']['numofbolts']
        self.ui.txtNoBolts_c.setText(str(c_noOfBolts))
        cno_ofrows = resultObj['cleat']['numofrow']
        self.ui.txt_row_c.setText(str(cno_ofrows))
        
        no_ofcol = resultObj['cleat']['numofcol']
        self.ui.txt_column_c.setText(str(no_ofcol))
        
        pitch_dist = resultObj['cleat']['pitch']
        self.ui.txtBeamPitch_c.setText(str(pitch_dist))
        
        gauge_dist = resultObj['cleat']['guage']
        self.ui.txtBeamGuage_c.setText(str(gauge_dist))
        
        end_dist = resultObj['cleat']['end']
        self.ui.txtEndDist_c.setText(str(end_dist))
        
        edge_dist = resultObj['cleat']['edge']
        self.ui.txtEdgeDist_c.setText(str(edge_dist))
        
        
        

         
        
        # Newly included fields
        cleat_ht = resultObj['cleat']['height'] 
        self.ui.outputCleatHeight.setText(str(cleat_ht))
        
#         plate_width = resultObj['Cleat']['width'] 
#         self.ui.txtplate_width.setText(str(plate_width))
        
        moment_demand = resultObj['cleat']['externalmoment']
#         self.ui.txtExtMoment.setText(str(moment_demand))
        
        moment_capacity =  resultObj['cleat']['momentcapacity']
#         self.ui.txtMomntCapacity.setText(str(moment_capacity))
    
   
    def displaylog_totextedit(self):
        '''
        This method displaying Design messages(log messages)to textedit widget.
        '''
        
        afile = QtCore.QFile('./fin.log')
        
        if not afile.open(QtCore.QIODevice.ReadOnly):#ReadOnly
            QtGui.QMessageBox.information(None, 'info', afile.errorString())
        
        stream = QtCore.QTextStream(afile)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscrollBar = self.ui.textEdit.verticalScrollBar();
        vscrollBar.setValue(vscrollBar.maximum());
        afile.close()
        
        
    def get_backend(self):
        """
        loads a backend
        backends are loaded in order of preference
        since python comes with Tk included, but that PySide or PyQt4
        is much preferred
        """
#         try:
#             from PySide import QtCore, QtGui
#             return 'pyside'
#         except:
#             pass
        try:
            from PyQt4 import QtCore, QtGui
            return 'pyqt4'
        except:
            pass
        # Check wxPython
        try:
            import wx
            return 'wx'
        except:
            raise ImportError("No compliant GUI library found. You must have either PySide, PyQt4 or wxPython installed.")
            sys.exit(1)
        
    # QtViewer
    def init_display(self,backend_str=None, size=(1024, 768)):
        
        global display,start_display, app, _, USED_BACKEND
    
        if not backend_str:
            USED_BACKEND = self.get_backend()
        elif backend_str in [ 'pyside', 'pyqt4']:
            USED_BACKEND = backend_str
        else:
            raise ValueError("You should pass either 'qt' or 'tkinter' to the init_display function.")
            sys.exit(1)
    
        # Qt based simple GUI
        if USED_BACKEND in ['pyqt4', 'pyside']:
            if USED_BACKEND == 'pyqt4':
                from PyQt4 import QtCore, QtGui, QtOpenGL
                from OCC.Display.pyqt4Display import qtViewer3d
            
        self.ui.modelTab = qtViewer3d(self)
        #self.ui.model2dTab = qtViewer3d(self)
        
        self.setWindowTitle("Osdag-%s 3d viewer ('%s' backend)" % (VERSION, USED_BACKEND))
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab,"")
        #self.ui.mytabWidget.addTab(self.ui.model2dTab,"")
        
        self.ui.modelTab.InitDriver()
        display = self.ui.modelTab._display
        #display_2d = self.ui.model2dTab._display
        
        
        # background gradient
        display.set_bg_gradient_color(23,1,32,23,1,32)
        #display_2d.set_bg_gradient_color(255,255,255,255,255,255)
        # display black trihedron
        display.display_trihedron()
        display.View.SetProj(1, 1, 1)
        def centerOnScreen(self):
                    '''Centers the window on the screen.'''
                    resolution = QtGui.QDesktopWidget().screenGeometry()
                    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                              (resolution.height() / 2) - (self.frameSize().height() / 2))
        def start_display():
            
            self.ui.modelTab.raise_()
            #self.ui.model2dTab.raise_()   # make the application float to the top
          
        return display, start_display
    
    def display3Dmodel(self, component):
        self.display.EraseAll()
        self.display.SetModeShaded()
        display.DisableAntiAliasing()
        self.display.set_bg_gradient_color(23,1,32,23,1,32)
        self.display.set_bg_gradient_color(28,9,99,252,243,235)
        self.display.View_Front()
        self.display.View_Iso()
        self.display.FitAll()
        if component == "Column":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
        elif component == "Beam":
            osdagDisplayShape(self.display, self.connectivity.get_beamModel(), material = Graphic3d_NOT_2D_ALUMINUM, update=True)
            #osdagDisplayShape(self.display, self.connectivity.beamModel, material = Graphic3d_NOT_2D_ALUMINUM, update=True)
        elif component == "Finplate" :
#             osdagDisplayShape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
#             osdagDisplayShape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display,self.connectivity.angleModel,color = 'blue', update = True)
            osdagDisplayShape(self.display,self.connectivity.angleLeftModel,color = 'blue', update = True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display,nutbolt,color = Quantity_NOC_SADDLEBROWN,update = True)
            #self.display.DisplayShape(self.connectivity.nutBoltArray.getModels(), color = Quantity_NOC_SADDLEBROWN, update=True)
        elif component == "Model":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
            osdagDisplayShape(self.display, self.connectivity.beamModel, material = Graphic3d_NOT_2D_ALUMINUM, update=True)
#             osdagDisplayShape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
#             osdagDisplayShape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display,self.connectivity.angleModel,color = 'blue', update = True)
            osdagDisplayShape(self.display,self.connectivity.angleLeftModel,color = 'blue', update = True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display,nutbolt,color = Quantity_NOC_SADDLEBROWN,update = True)
            #self.display.DisplayShape(self.connectivity.nutBoltArray.getModels(), color = Quantity_NOC_SADDLEBROWN, update=True)
        
    def create3DBeamWebBeamWeb(self):
        '''
        creating 3d cad model with beam web beam web
       
        '''
        uiObj = self.getuser_inputs()
        resultObj = cleatAngleConn(uiObj)
       
        ##### PRIMARY BEAM PARAMETERS #####
       
        dictbeamdata  = self.fetchColumnPara()
        pBeam_D = int(dictbeamdata[QString("D")])
        pBeam_B = int(dictbeamdata[QString("B")])
        pBeam_tw = float(dictbeamdata[QString("tw")])
        pBeam_T = float(dictbeamdata[QString("T")])
        pBeam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        pBeam_R1 = float(dictbeamdata[QString("R1")])
        pBeam_R2 = float(dictbeamdata[QString("R2")])
        pBeam_length = 800.0 # This parameter as per view of 3D cad model
       
        #beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        column = ISection(B = pBeam_B, T = pBeam_T,D = pBeam_D,t = pBeam_tw,
                        R1 = pBeam_R1, R2 = pBeam_R2, alpha = pBeam_alpha,
                        length = pBeam_length,notchObj = None)
       
        ##### SECONDARY BEAM PARAMETERS ######
        dictbeamdata2 = self.fetchBeamPara()
       
        sBeam_D = int(dictbeamdata2[QString("D")])
        sBeam_B = int(dictbeamdata2[QString("B")])
        sBeam_tw = float(dictbeamdata2[QString("tw")])
        sBeam_T = float(dictbeamdata2[QString("T")])
        sBeam_alpha = float(dictbeamdata2[QString("FlangeSlope")])
        sBeam_R1 = float(dictbeamdata2[QString("R1")])
        sBeam_R2 = float(dictbeamdata2[QString("R2")])
       
        #--Notch dimensions
        notchObj = Notch(R1 = pBeam_R1, height = (pBeam_T + pBeam_R1), width= ((pBeam_B -(pBeam_tw + 40))/2.0 + 10),length = sBeam_B )
        #column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B = sBeam_B, T = sBeam_T, D = sBeam_D,
                           t = sBeam_tw, R1 = sBeam_R1, R2 = sBeam_R2,
                           alpha = sBeam_alpha, length = 500, notchObj = notchObj)
         
        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        
        dictAngleData = self.fetchAnglePara()
        cleat_length = resultObj['cleat']['height']
        
        cleat_thick = float(dictAngleData[QString("t")])
        angle_A = int(dictAngleData[QString("A")])
        angle_B = int(dictAngleData[QString("B")])
#         cleat_thick = 10
#         angle_A = 120
#         angle_B = 90
        
        
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = bolt_r + 7
        nut_R = bolt_R
        bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3750(1985)
        nut_T = 12.0 # minimum nut thickness As per Indian Standard
        nut_Ht = 12.2 #
        
        #plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L= cleat_length,A= angle_A, B= angle_B, T = cleat_thick)
        
        

        #bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R = bolt_R,T = bolt_T, H = bolt_Ht, r = bolt_r )
         
        #nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R = bolt_R, T = nut_T,  H = nut_Ht, innerR1 = bolt_r)
        
        gap =  sBeam_tw + 2 * cleat_thick+ nut_T
        cgap = pBeam_tw +  cleat_thick+ nut_T
    
        
        nutBoltArray = NutBoltArray(resultObj,nut,bolt,gap, cgap)
         
        beamwebconn = BeamWebBeamWeb(column,beam,notchObj,angle,nutBoltArray)
        beamwebconn.create_3dmodel()
         
        return  beamwebconn
             
    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web
        '''
        uiObj = self.getuser_inputs()
        resultObj = cleatAngleConn(uiObj)
        
        dictbeamdata  = self.fetchBeamPara()
        ##### BEAM PARAMETERS #####
        beam_D = int(dictbeamdata[QString("D")])
        beam_B = int(dictbeamdata[QString("B")])
        beam_tw = float(dictbeamdata[QString("tw")])
        beam_T = float(dictbeamdata[QString("T")])
        beam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(dictbeamdata[QString("R1")])
        beam_R2 = float(dictbeamdata[QString("R2")])
        beam_length = 500.0 # This parameter as per view of 3D cad model
        
        #beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B = beam_B, T = beam_T,D = beam_D,t = beam_tw,
                        R1 = beam_R1, R2 = beam_R2, alpha = beam_alpha,
                        length = beam_length)
        
        ##### COLUMN PARAMETERS ######
        dictcoldata = self.fetchColumnPara()
        
        column_D = int(dictcoldata[QString("D")])
        column_B = int(dictcoldata[QString("B")])
        column_tw = float(dictcoldata[QString("tw")])
        column_T = float(dictcoldata[QString("T")])
        column_alpha = float(dictcoldata[QString("FlangeSlope")])
        column_R1 = float(dictcoldata[QString("R1")])
        column_R2 = float(dictcoldata[QString("R2")])
        
        #column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B = column_B, T = column_T, D = column_D,
                           t = column_tw, R1 = column_R1, R2 = column_R2, alpha = column_alpha, length = 1000)
        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        dictAngleData = self.fetchAnglePara()
        cleat_length = resultObj['cleat']['height']
        
        cleat_thick = float(dictAngleData[QString("t")])
        angle_A = int(dictAngleData[QString("A")])
        angle_B = int(dictAngleData[QString("B")])
#         cleat_thick = 10
#         angle_A = 120
#         angle_B = 90
        
        
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = bolt_r + 7
        nut_R = bolt_R
        bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3750(1985)
        nut_T = 12.0 # minimum nut thickness As per Indian Standard
        nut_Ht = 12.2 #
        
        #plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L= cleat_length,A= angle_A, B= angle_B, T = cleat_thick)
        
        

        #bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R = bolt_R,T = bolt_T, H = bolt_Ht, r = bolt_r )
         
        #nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R = bolt_R, T = nut_T,  H = nut_Ht, innerR1 = bolt_r)
        
        gap = beam_tw + 2 * cleat_thick+ nut_T
        cgap = column_tw +  cleat_thick+ nut_T
    
        
        nutBoltArray = NutBoltArray(resultObj,nut,bolt,gap, cgap)
        
        colwebconn =  ColWebBeamWeb(column,beam,angle,nutBoltArray)
        colwebconn.create_3dmodel()
        
        return  colwebconn
        
    def create3DColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection
        
        '''
        uiObj = self.getuser_inputs()
        resultObj = cleatAngleConn(uiObj)
        
        dictbeamdata  = self.fetchBeamPara()
        ##### BEAM PARAMETERS #####
        beam_D = int(dictbeamdata[QString("D")])
        beam_B = int(dictbeamdata[QString("B")])
        beam_tw = float(dictbeamdata[QString("tw")])
        beam_T = float(dictbeamdata[QString("T")])
        beam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(dictbeamdata[QString("R1")])
        beam_R2 = float(dictbeamdata[QString("R2")])
        beam_length = 500.0 # This parameter as per view of 3D cad model
        
        #beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B = beam_B, T = beam_T,D = beam_D,t = beam_tw,
                        R1 = beam_R1, R2 = beam_R2, alpha = beam_alpha,
                        length = beam_length)
        
        ##### COLUMN PARAMETERS ######
        dictcoldata = self.fetchColumnPara()
        
        column_D = int(dictcoldata[QString("D")])
        column_B = int(dictcoldata[QString("B")])
        column_tw = float(dictcoldata[QString("tw")])
        column_T = float(dictcoldata[QString("T")])
        column_alpha = float(dictcoldata[QString("FlangeSlope")])
        column_R1 = float(dictcoldata[QString("R1")])
        column_R2 = float(dictcoldata[QString("R2")])
        
        #column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B = column_B, T = column_T, D = column_D,
                           t = column_tw, R1 = column_R1, R2 = column_R2, alpha = column_alpha, length = 1000)
        
        #### Cleat,BOLT AND NUT PARAMETERS #####
        dictAngleData = self.fetchAnglePara()
        cleat_length = resultObj['cleat']['height']
        
        cleat_thick = float(dictAngleData[QString("t")])
        angle_A = int(dictAngleData[QString("A")])
        angle_B = int(dictAngleData[QString("B")])
#         cleat_thick = 10
#         angle_A = 120
#         angle_B = 90
        
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = bolt_r + 7
        nut_R = bolt_R
        bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        bolt_Ht = 50.0 # minimum bolt length as per Indian Standard
        nut_T = 12.0 # minimum nut thickness As per Indian Standard
        nut_Ht = 12.2 #
        
        #plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L= cleat_length,A= angle_A, B= angle_B, T = cleat_thick)
        
       

        #bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R = bolt_R,T = bolt_T, H = bolt_Ht, r = bolt_r )
         
        #nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R = bolt_R, T = nut_T,  H = nut_Ht, innerR1 = bolt_r)
        
        gap = beam_tw + 2 * cleat_thick+ nut_T
        cgap = column_T +  cleat_thick+ nut_T
        
        nutBoltArray = NutBoltArray(resultObj,nut,bolt,gap, cgap)
        
        colflangeconn =  ColFlangeBeamWeb(column,beam,angle,nutBoltArray)
        colflangeconn.create_3dmodel()
        return colflangeconn
        
    
    def call_3DModel(self,flag): 
#         self.ui.btnSvgSave.setEnabled(True)
        if self.ui.btn3D.isEnabled():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            
        if flag == True:
            if self.ui.comboConnLoc.currentText()== "Column web-Beam web":    
                #self.create3DColWebBeamWeb()
                self.connectivity =  self.create3DColWebBeamWeb()
                self.fuse_model = None
            elif self.ui.comboConnLoc.currentText()== "Column flange-Beam web":
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity =  self.create3DColFlangeBeamWeb()
                self.fuse_model = None
                
            else :
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity =  self.create3DBeamWebBeamWeb()
                self.fuse_model = None

            self.display3Dmodel("Model")
            # beamOrigin = self.connectivity.beam.secOrigin + self.connectivity.beam.t/2 * (-self.connectivity.beam.uDir)
            # gpBeamOrigin = getGpPt(beamOrigin)
            # my_sphere2 = BRepPrimAPI_MakeSphere(gpBeamOrigin,1).Shape()
            # self.display.DisplayShape(my_sphere2,color = 'red',update = True)
            # beamOrigin = self.connectivity.beam.secOrigin 
            # gpBeamOrigin = getGpPt(beamOrigin)
            # my_sphere2 = BRepPrimAPI_MakeSphere(gpBeamOrigin,1).Shape()
            # self.display.DisplayShape(my_sphere2,color = 'blue',update = True)
            # plateOrigin =  (self.connectivity.plate.secOrigin + self.connectivity.plate.T/2.0 *(self.connectivity.plate.uDir)+ self.connectivity.weldLeft.L/2.0 * (self.connectivity.plate.vDir) + self.connectivity.plate.T * (-self.connectivity.weldLeft.uDir))
            # gpPntplateOrigin=  getGpPt(plateOrigin)
            # my_sphere = BRepPrimAPI_MakeSphere(gpPntplateOrigin,2).Shape()
            # self.display.DisplayShape(my_sphere,update=True)
            
        else:
            self.display.EraseAll()
            self.display.DisplayMessage(gp_Pnt(1000,0,400),"Sorry, can not create 3D model",height = 23.0)       
   
    def call_3DBeam(self):
        '''
        Creating and displaying 3D Beam
        '''
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        
        self.display3Dmodel("Beam")
            
    def call_3DColumn(self):
        '''
        '''
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.display3Dmodel( "Column")
        
    def call_3DFinplate(self):
        '''Displaying FinPlate in 3D
        '''
        if self.ui.checkBoxCleat.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            
        self.display3Dmodel( "Finplate")
    
        
    def design_btnclicked(self):
        '''
        '''
        self.ui.outputDock.setFixedSize(310,710)
        self.enableViewButtons()
        
        #self.set_designlogger()
        # Getting User Inputs.
        uiObj = self.getuser_inputs()
        
        # FinPlate Design Calculations. 
        resultObj = cleatAngleConn(uiObj)
        
        # Displaying Design Calculations To Output Window
        self.display_output(resultObj)
        
        # Displaying Messages related to FinPlate Design.
        self.displaylog_totextedit()

        # Displaying 3D Cad model
        status = resultObj['Bolt']['status']
        self.call_3DModel(status)
        
        print "inputs:  " , uiObj
        
        
    def create2Dcad(self,connectivity):
        ''' Returns the fuse model of cleat angle
        '''
        cadlist =  self.connectivity.get_models()
        final_model = cadlist[0]
        for model in cadlist[1:]:
            final_model = BRepAlgoAPI_Fuse(model,final_model).Shape()
        return final_model 
     
    
             
         
    # Export to IGS,STEP,STL,BREP
    def save3DcadImages(self):
        if self.connectivity == None:
            self.connectivity =  self.create3DColWebBeamWeb()
        if self.fuse_model == None:
            self.fuse_model = self.create2Dcad(self.connectivity)
        shape = self.fuse_model
        
        files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"
        fileName  = QtGui.QFileDialog.getSaveFileName(self, 'Export', "/home/aravind/Cadfiles/untitled.igs", files_types )
        
        fName = str(fileName)
        file_extension = fName.split(".")[-1]
        
        if file_extension == 'igs':
            IGESControl.IGESControl_Controller().Init()
            iges_writer = IGESControl.IGESControl_Writer()
            iges_writer.AddShape(shape)
            iges_writer.Write(fName)
            
        elif file_extension == 'brep':
            
            BRepTools.breptools.Write(shape, fName)
            
        elif file_extension == 'stp':
            # initialize the STEP exporter
            step_writer = STEPControl_Writer()
            Interface_Static_SetCVal("write.step.schema", "AP203")
            
            # transfer shapes and write file
            step_writer.Transfer(shape, STEPControl_AsIs)
            status = step_writer.Write(fName)
            
            assert(status == IFSelect_RetDone)
            
        else:
            stl_writer = StlAPI_Writer()
            stl_writer.SetASCIIMode(True)
            stl_writer.Write(shape,fName)
            
        QtGui.QMessageBox.about(self,'Information',"File saved")
        

    def display2DModelOriginal(self, final_model, viewName):
        
        self.display,_ = self.init_display()
        self.display.EraseAll()      
        #self.display.SetModeWireFrame()
        
        self.display.DisplayShape(final_model, update = True)
        self.display.SetModeHLR()
        
        if (viewName == "Front"):
            self.display.View_Front()
        elif (viewName == "Top"):
            self.display.View_Top()
        elif (viewName == "Right"):
            self.display.View_Right()
        else:
            pass

    def display2DModel(self, final_model, viewName):
        
        #display, start_display, _, _ = self.simpleGUI()
        #self.display2d,_,_ = self.init_display(backend_str="pyqt4")
        self.display.EraseAll()      

        self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)
        
        self.display.SetModeHLR()
        #self.display.SetModeShaded()
        # Get Context
        ais_context = self.display.GetContext().GetObject()

        # Get Prs3d_drawer from previous context
        drawer_handle = ais_context.DefaultDrawer()
        drawer = drawer_handle.GetObject()
        drawer.EnableDrawHiddenLine()
        
        hla = drawer.HiddenLineAspect().GetObject()
        hla.SetWidth(2)
        hla.SetColor(Quantity_NOC_RED)
        
        # increase line width in the current viewer
        # This is only viewed in the HLR mode (hit 'e' key for instance)
        
        line_aspect = drawer.SeenLineAspect().GetObject()
        line_aspect.SetWidth(2.8)
        line_aspect.SetColor(Quantity_NOC_BLUE1)
        
        self.display.DisplayShape(final_model, update = False)
        
        if (viewName == "Front"):
            self.display.View_Front()
        elif (viewName == "Top"):
            self.display.View_Top()
        elif (viewName == "Right"):
            self.display.View_Right()
        elif (viewName == "Left"):
            self.display.View_Left()
        else:
            pass
            
        #start_display()

    def call_Frontview(self):
        
        '''Displays front view of 2Dmodel
        '''
#         self.ui.btnSvgSave.setEnabled(False)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
        if self.ui.comboConnLoc.currentText()== "Column web-Beam web":
            self.display.EraseAll()
            self.ui.mytabWidget.setCurrentIndex(1)
            if self.connectivity == None:
                self.connectivity =  self.create3DColWebBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel( self.fuse_model,"Front")
            
            self.call_2d_Drawing()
        else:
            self.display.EraseAll()
            self.ui.mytabWidget.setCurrentIndex(0)
            if self.connectivity == None:
                self.connectivity =  self.create3DColFlangeBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel( self.fuse_model,"Left") 
            self.call_2d_Drawing()       
        
    
             
#     def call2D_Drawing(self):
#         uiObj = self.getuser_inputs()
#         
#         resultObj = cleatAngleConn(uiObj)
#         dictbeamdata  = self.fetchBeamPara()
#         dictcoldata = self.fetchColumnPara()
#         fin2DFront = Fin2DCreatorFront(uiObj,resultObj,dictbeamdata,dictcoldata)
#         fin2DFront.saveToSvg()
        
        
    def callDesired_View(self,fileName,view):
        
        uiObj = self.getuser_inputs()
        resultObj = cleatAngleConn(uiObj)
        dictbeamdata  = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        dictangledata = self.fetchAnglePara()
        finCommonObj = FinCommonData(uiObj,resultObj,dictbeamdata,dictcoldata,dictangledata)
        finCommonObj.saveToSvg(str(fileName),view)
    
    def call_2d_Drawing(self,view):
        
        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite pacage which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        if view == "All":
            fileName = ''
            self.callDesired_View(fileName, view)
            
            self.display.set_bg_gradient_color(255,255,255,255,255,255)
            self.display.ExportToImage('/home/aravind/3D_Model.png')
            
        else:
            
            fileName = QtGui.QFileDialog.getSaveFileName(self,
                    "Save SVG", '/home/aravind/untitle.svg',
                    "SVG files (*.svg)")
            f = open(fileName,'w')
            
            self.callDesired_View(fileName, view)
           
            f.close()
            
            
            
            
            
#         loc = self.ui.comboConnLoc.currentText()
#         uiObj = self.getuser_inputs()
#         
#         resultObj = cleatAngleConn(uiObj)
#         dictbeamdata  = self.fetchBeamPara()
#         dictcoldata = self.fetchColumnPara()
#         dictangledata = self.fetchAnglePara()
#         if loc == "Column flange-Beam web" or "Column web-Beam web":
#             cleat2Dfront = FinCommonData(uiObj,resultObj,dictbeamdata,dictcoldata,dictangledata)
#         else:
#             cleat2Dfront = FinCommonData(uiObj,resultObj,dictbeamdata,dictcoldata,dictangledata)
#         cleat2Dfront.saveToSvg('/home/aravind/cleattestFront.svg', 'Front')
#         cleat2Dfront.saveToSvg('/home/aravind/cleattestSide.svg', 'Side')
#         cleat2Dfront.saveToSvg('/home/aravind/cleattestTop.svg', 'Top')

        
        
            
    def call_Topview(self):
        
        '''Displays Top view of 2Dmodel
        '''
        self.ui.btnSvgSave.setEnabled(False)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
        
        if self.ui.comboConnLoc.currentText()== "Column web-Beam web":    
            self.display.EraseAll()
            self.ui.mytabWidget.setCurrentIndex(1)
            
            if self.connectivity == None:
                self.connectivity =  self.create3DColWebBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel( self.fuse_model,"Top")
        else:
            self.display.EraseAll()
            self.ui.mytabWidget.setCurrentIndex(0)
            
            if self.connectivity == None:
                self.connectivity =  self.create3DColFlangeBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel( self.fuse_model,"Top")
        
        
    def call_Sideview(self):
        
        '''Displays Side view of the 2Dmodel'
        '''
#         self.ui.btnSvgSave.setEnabled(False)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
        
        if self.ui.comboConnLoc.currentText()== "Column web-Beam web": 
            self.ui.mytabWidget.setCurrentIndex(1)
            
            if self.connectivity == None:
                self.connectivity =  self.create3DColWebBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel( self.fuse_model,"Right")
        else:
            self.ui.mytabWidget.setCurrentIndex(0)
            
            if self.connectivity == None:
                self.connectivity =  self.create3DColFlangeBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel( self.fuse_model,"Front")
            
    def closeEvent(self, event):
        '''
        Closing finPlate window.
        '''
        uiInput = self.getuser_inputs()
        self.save_inputs(uiInput)
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore() 

                        
def set_osdaglogger():
    
    logger = logging.getLogger("osdag")
    logger.setLevel(logging.DEBUG)
 
    # create the logging file handler
    fh = logging.FileHandler("./fin.log", mode="a")
    
    #,datefmt='%a, %d %b %Y %H:%M:%S'
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    formatter = logging.Formatter('''
    <div  class="LOG %(levelname)s">
        <span class="DATE">%(asctime)s</span>
        <span class="LEVEL">%(levelname)s</span>
        <span class="MSG">%(message)s</span>
    </div>''')
    formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    
def launchCleatAngleController(osdagMainWindow):
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("./Connections/Shear/Finplate/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="./Connections/Shear/Finplate/log.css"/>''')
     
    #app = QtGui.QApplication(sys.argv)
    window = MainController()
    osdagMainWindow.hide()
     
    window.show()
    window.closed.connect(osdagMainWindow.show)
     
    #sys.exit(app.exec_())


if __name__ == '__main__':
    #launchFinPlateController(None)
       
    # linking css to log file to display colour logs.
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="log.css"/>''')
    
    
       
    app = QtGui.QApplication(sys.argv)
    window = MainController()
    window.show()
    sys.exit(app.exec_())




