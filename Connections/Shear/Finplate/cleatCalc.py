'''
Created on 16-Jul-2015

@author: aravind
'''

'''
Created on 25-May-2015

@author: aravind
'''
''' 
Example 5.16 Page 409 N. Subramanium
Design of steel structures
Design of cleat angle:
Design a web side plate connection (welded to the column and site bolted to the beam) for ISMB 400 in Fe 410 grade steel and to carry a reaction of 140 kN due
to factored loads. The connection is to the flange of an ISSC 200 column.

'''
import cmath;
import math
import sys;

from math import sqrt
from model import *
from PyQt4.Qt import QString
import logging
flag  = 1
logger = None

def module_setup():
    
    global logger
    logger = logging.getLogger("osdag.finPlateCalc")

module_setup()

#FUNCTION DEFINITIONS---------------
#BOLT: determination of shear capacity of black bolt = fu * n * A / (root(3) * Y)
def black_bolt_shear(dia, n, fu):
    A = cmath.pi * dia * dia * 0.25 * 0.78; #threaded area = 0.78 x shank area
    root3 = cmath.sqrt(3);
    Vs = fu * n * A / (root3 * 1.25 * 1000)
    Vs = round(Vs.real,3)
    return Vs
#BOLT: Determination of factored design force of HSFG bolts Vsf = Vnsf / Ymf = uf * ne * Kh * Fo where Vnsf: The nominal shear capacity of bolt
def HSFG_bolt_shear(uf, dia, n, fu):
    Anb = cmath.pi * dia * dia * 0.25 * 0.78  #threaded area(Anb) = 0.78 x shank area
    Fo = Anb * 0.7 * fu 
    Kh = 1  # Assuming fastners in Clearence hole
    Ymf = 1.25  # Ymf = 1.25 if Slip resistance is designed at ultimate load
    Vsf = uf * n * Kh * Fo / (Ymf * 1000)
    Vsf = round(Vsf.real,3)
    return Vsf
#BOLT: determination of bearing capacity = 2.5 * kb * d * t * fu / Y
def bolt_bearing(dia, t, fu):
#add code to determine kb if pitch, gauge, edge distance known
    kb = 0.5;            #assumption
    Vb = 2.5 * kb * dia * t * fu / (1.25 * 1000);
    Vb = round(Vb.real,3);
    return Vb;
def get_min_cleat_height(bolt_required , bolt_dia ):
    min_edge_dist = int(1.7 * (bolt_dia)) 
    l_height = (2.5 * bolt_dia * (bolt_required - 1) + (2 * min_edge_dist))  #  sum of minimum pitch and minimum edge distance
    return int(l_height)

def single_boltline_shear(bolts_one_line , pitch , n , ex , Vx ,shear_force_x , shear_force_y):
    if bolts_one_line % 2 == 0:
        r_i = (n - 0.5) * pitch
        sum_r_i_sqr = 0.0
        for i in range(1, n+1):
            sum_r_i_sqr = sum_r_i_sqr + 2 * (i-0.5) * (i-0.5) * pitch * pitch
        shear_force_x = Vx * ex * r_i / (sum_r_i_sqr)         
    if bolts_one_line % 2 != 0:
        r_i = n * pitch
        sum_r_i_sqr = 0
        for i in range(1, n+1):
            sum_r_i_sqr = sum_r_i_sqr + 2 * i * i * pitch * pitch
        shear_force_x = Vx * ex * r_i / sum_r_i_sqr
    critical_bolt_shear = sqrt(shear_force_x * shear_force_x + shear_force_y * shear_force_y)          
    return critical_bolt_shear

def double_blotline_shear(bolts_one_line , pitch , gauge , n , ex , Vx , shear_force_x , shear_force_y):
    r_x = gauge / 2
    bolts_required = 2 * bolts_one_line
    if bolts_one_line % 2 == 0:
        r_y = (n - 0.5) * pitch
        sum_r_i_sqr = bolts_required * r_x * r_x 
        for i in range(1, n+1):
            sum_r_i_sqr = sum_r_i_sqr + 4 * (i-0.5) * (i-0.5) * pitch * pitch
        shear_force_x = Vx * ex * r_y / sum_r_i_sqr
        shear_force_y = shear_force_y + (Vx * ex * r_x) / sum_r_i_sqr
        
    if bolts_one_line % 2 != 0:
        r_i = n * pitch
        sum_r_i_sqr = bolts_required * r_x * r_x 
        for i in range(1, n+1):
            sum_r_i_sqr = sum_r_i_sqr +  4 * i * i * pitch * pitch
        shear_force_x = Vx * ex * r_i / sum_r_i_sqr
        shear_force_y = shear_force_y + (Vx * ex * r_x) / sum_r_i_sqr
    critical_bolt_shear = sqrt(shear_force_x * shear_force_x + shear_force_y * shear_force_y)          
    return critical_bolt_shear
        
def critical_bolt_shear(bolt_line , bolts_one_line , bolts_required , pitch , gauge , shear_load , beam_eccentricity ):
    n = int(bolts_one_line / 2)
    ex = beam_eccentricity
    Vx = shear_load / 2
    shear_force_y = Vx / bolts_required
    shear_force_x = 0
    
    if bolt_line == 1:
        critical_bolt_shear = single_boltline_shear(bolts_one_line, pitch, n, ex, Vx, shear_force_x, shear_force_y)           
    # double line bolt arrangement
    if bolt_line == 2:
       critical_bolt_shear = double_blotline_shear(bolts_one_line, pitch, gauge, n, ex, Vx, shear_force_x, shear_force_y)           
    return critical_bolt_shear
def column_critical_shear(c_bolt_line , c_bolts_one_line , c_bolts_required , c_pitch , c_gauge_type_2 , shear_load , c_eccentricity , c_edge_distance):
    force_x = 0.0
    force_y = shear_load * 0.5/ c_bolts_required
    Vx = shear_load / 2
    n = int(c_bolts_one_line / 2)
    if c_bolt_line == 1:
        if c_bolts_one_line % 2 == 0:
            r_i = (n - 0.5) * c_pitch
            sum_r_i_sqr = 0.0
            for i in range(1, n+1):
                sum_r_i_sqr = sum_r_i_sqr + 2 * (i-0.5) * (i-0.5) * c_pitch * c_pitch
            force_x = Vx * c_eccentricity * r_i / (sum_r_i_sqr)
                
        elif c_bolts_one_line % 2 != 0:
            r_i = n * c_pitch
            sum_r_i_sqr = 0.0
            for i in range(1, n+1):
                sum_r_i_sqr = sum_r_i_sqr + 2 * i * i * c_pitch * c_pitch
            force_x = Vx * c_eccentricity * r_i / sum_r_i_sqr
    # Double line of bolts
    if c_bolt_line == 2:
        r_x = c_gauge_type_2 / 2
        if c_bolts_one_line % 2 == 0:
            r_y = (n - 0.5) * c_pitch
            sum_r_i_sqr = c_bolts_required * r_x * r_x 
            for i in range(1, n+1):
                sum_r_i_sqr = sum_r_i_sqr + 4 * (i-0.5) * (i-0.5) * c_pitch * c_pitch
            force_x = Vx * c_eccentricity * r_y / sum_r_i_sqr
            force_y = force_y + (Vx * c_eccentricity * r_x) / sum_r_i_sqr
            
        if c_bolts_one_line % 2 != 0:
            r_i = n * c_pitch
            sum_r_i_sqr = c_bolts_required * r_x * r_x 
            for i in range(1, n+1):
                sum_r_i_sqr = sum_r_i_sqr +  4 * i * i * c_pitch * c_pitch
            force_x = Vx * c_eccentricity * r_i / sum_r_i_sqr
            force_y = force_y + (Vx * c_eccentricity * r_x) / sum_r_i_sqr
              
#     critical_bolt_shear = sqrt(force_x * force_x + shear_force_y * shear_force_y)
#     critical_bolt_shear = round(critical_bolt_shear , 3)
        
    
    # Assuming centre of pressure 25 mm below the top cleat and again calculating the horizontal force
    # Maximum of force_x and above mentioned horizontal force will be used to check the safety of the bolts
    
    force_x_1 = 0.0
    force_y_1 = shear_load * 0.5/ c_bolts_required
    if c_bolt_line == 1:
        r_i = c_edge_distance + (c_bolts_required - 1) * c_pitch - 25
        sum_r_i_sqr = 0
        for i in  range(1 , c_bolts_required + 1):
            r = c_edge_distance + (i - 1) * c_pitch -25
            sum_r_i_sqr = sum_r_i_sqr + 2 * r * r
        force_x_1 = Vx * c_eccentricity * r_i / sum_r_i_sqr  
    #     force_x = max(force_x , force_x_1) 
    #     resultant_shear = sqrt(force_x * force_x + force_y * force_y
    
    
    if c_bolt_line == 2:
        r_x = c_gauge_type_2 / 2
        r_i = c_edge_distance + (c_bolts_one_line - 1) * c_pitch - 25
        sum_r_i_sqr = 0
        for i in range(1 , c_bolts_one_line + 1):
            r_y = c_edge_distance + (i - 1) * c_pitch -25
            sum_r_i_sqr = sum_r_i_sqr + r_x * r_x + r_y * r_y
        force_x_1 = Vx * c_eccentricity * r_i / sum_r_i_sqr  
        force_y_1 = force_y_1 + Vx * c_eccentricity * r_x / sum_r_i_sqr  
                     
    force_x_2 = max(force_x , force_x_1) 
    force_y_2 = max(force_y , force_y_1)
    resultant_shear = sqrt(force_x_2 * force_x_2 + force_y_2 * force_y_2)
    return resultant_shear
    



def cleatAngleConn(uiObj):
    global logger
    beam_sec = uiObj['Member']['BeamSection']
    column_sec = uiObj['Member']['ColumSection']
    connectivity = uiObj['Member']['Connectivity']
    beam_fu = uiObj['Member']['fu (MPa)']
    beam_fy = uiObj['Member']['fy (MPa)']
              
    shear_load = uiObj['Load']['ShearForce (kN)']
                  
    bolt_dia = uiObj['Bolt']['Diameter (mm)']
    bolt_type  = uiObj["Bolt"]["Type"]
    bolt_grade = uiObj['Bolt']['Grade']
   
              
#     cleat_thk = uiObj['cleat']['Thickness (mm)']
#     cleat_thk = 8
    cleat_length = uiObj['cleat']['Height (mm)']
#     cleat_length = 290
    cleat_fu = uiObj['Member']['fu (MPa)']
    cleat_fy = uiObj['Member']['fy (MPa)']
    cleat_sec = uiObj['cleat']['section']
              
    bolt_planes = 1 
    dictbeamdata  = get_beamdata(beam_sec)
    beam_w_t = float(dictbeamdata[QString("tw")])
    beam_f_t = float(dictbeamdata[QString("T")])
    beam_d = float(dictbeamdata[QString("D")])
    beam_R1 =float(dictbeamdata[QString("R1")])
    beam_B =float(dictbeamdata[QString("B")])
    beam_D =float(dictbeamdata[QString("D")])
    
        
    if connectivity == "Column web-Beam web" or connectivity == "Column flange-Beam web": 
        dictcolumndata = get_columndata(column_sec)
        column_w_t = float(dictcolumndata[QString("tw")])
        column_f_t = float(dictcolumndata[QString("T")])
        column_R1 =float(dictcolumndata[QString("R1")])
        column_D = float(dictcolumndata[QString("D")])
        column_B = float(dictcolumndata[QString("B")])
    else:
        dictcolumndata = get_beamdata(column_sec)
        column_w_t = float(dictcolumndata[QString("tw")])
        column_f_t = float(dictcolumndata[QString("T")])
        column_R1 =float(dictcolumndata[QString("R1")])
        column_D = float(dictcolumndata[QString("D")])
        column_B = float(dictcolumndata[QString("B")])
        
   
    dictCleatData = get_angledata(cleat_sec)
    cleat_legsize= int(dictCleatData[QString("A")])
    cleat_legsize_1 = int(dictCleatData[QString("B")])
    cleat_thk = int(dictCleatData[QString("t")])
    
#     cleat_legsize= 90
#     cleat_thk = 10
    
    
    
    
    
    
   


    
  
########################################################################
# Bolt design:
# I: Check for number of bolts -------------------
    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade))*bolt_fu;
    
    t_thinner = min(beam_w_t.real,cleat_thk.real);
    bolt_shear_capacity = 0
    if bolt_type == 'HSFG':
        bolt_shear_capacity = HSFG_bolt_shear(0.48, bolt_dia, 2, bolt_fu)
    if bolt_type == 'Black Bolt':
        bolt_shear_capacity = black_bolt_shear(bolt_dia, 2, bolt_fu)
    bolt_bearing_capacity = bolt_bearing(bolt_dia, beam_w_t, bolt_fu)
    bolt_capacity = min(bolt_shear_capacity, bolt_bearing_capacity);
    
    
    bolts_required = int(shear_load/bolt_capacity) + 1;
    
    if bolts_required <= 3:
        bolts_required = 4
    
    # print('bolts req'+str(bolts_required))
    
    # Spacing of bolts for cleat -------------------
    if bolt_dia == 12 or bolt_dia == 14:
        dia_hole = bolt_dia + 1
    elif bolt_dia == 16 or bolt_dia == 18 or bolt_dia == 20 or bolt_dia == 22 or bolt_dia == 24:
        dia_hole = bolt_dia + 2
    else:
        dia_hole = bolt_dia + 3    
    
    # Minimum/maximum pitch and gauge
    min_pitch = int(2.5 * bolt_dia);
    min_gauge = int(2.5 * bolt_dia);
    
    if min_pitch%10 != 0 or min_gauge%10 != 0:
        min_pitch = (min_pitch/10)*10 + 10;
        min_gauge = (min_gauge/10)*10 + 10;
    else:
        min_pitch = min_pitch;
        min_gauge = min_gauge;
                            #clause 10.2.2 is800
    max_spacing = int(min(100 + 4 * t_thinner, 200));        #clause 10.2.3.3 is800
    
    min_edge_dist = int(1.7 * (dia_hole))
    if min_edge_dist%10 != 0:
        min_edge_dist = (min_edge_dist/10)*10 + 10;
    else:
        min_edge_dist = min_edge_dist;
        
    max_edge_dist = int((12 * t_thinner * cmath.sqrt(250/bolt_fy)).real)-1;
    
    
    
    #### # # # # # # Finalizing cleat lenght and validating inputs# # # # # # # # 
    # INPUT FOR PLATE DIMENSIONS (FOR OPTIONAL INPUTS) AND VALIDATION
    
    # Plate thickness check
    # Actully not needed because program is directly importing cleat section which has thickness greater than or equal to 8mm
    
    if (beam_d <= 450) and (cleat_thk != 8) :
        cleat_thk = 8
        
        
        
        
    
    # cleat height check
    # Maximum/minimum cleat height
    max_cleat_height = 0.75 * beam_d
    min_cleat_length = 0.0 
#######################
    D_notch = 50##NEED TO BE CHANGED   

##COLUMN FLANGE-BEAM WEB CONNECTIVITY  
    design_check = True   
    if connectivity == 'Column flange-Beam web':
        avbl_space = column_B 
        required_space = 2 * cleat_legsize_1 + beam_w_t
        maxLegsize = int((avbl_space - beam_w_t)/10) * 5
        if avbl_space < required_space:
            design_check = False
            logger.error(':Column cannot accommodate the given cleat agle due to space restriction  ')
            logger.warning(':The width of the column flange(B)  should be greater than %2.2f mm' %(int(required_space))) 
            logger.info('Cleat legsize(B)of the cleat angle should be less than or equal to %2.2f mm' %(maxLegsize))
        
    elif connectivity == 'Column web-Beam web':
        avbl_space = column_D - 2 * column_f_t
        required_space = 2 * cleat_legsize_1 + beam_w_t
        maxLegsize = int((avbl_space - beam_w_t)/10) * 5
        if avbl_space < required_space:
            design_check = False
            logger.error(':Column cannot accommodate the given cleat agle due to space restriction  ')
            logger.warning(':The depth of the column(D) should be greater than %2.2f mm' %(int(required_space))) 
            logger.info('Cleat legsize(B)of the cleat angle should be less than or equal to %2.2f mm' %(maxLegsize))
    else:
        #Always feasible in this case.No checks required
        pass   
                    
    
      
    # Height input and check
    # if this variable becomes false at least one time ,then user has to redesign by increasing the dimensions of cleat , bolt diameter etc 
    length_input = False         
    if cleat_length != 0:
        length_input = True
        pitch_possible = (cleat_length- 2 * min_edge_dist) / (bolts_required-1)
        if pitch_possible > min_pitch:
            min_cleat_length =  get_min_cleat_height(bolts_required, bolt_dia)
        else:
            bolts_reqrd = bolts_required/2 + 1 # double line of bolts will be there
            min_cleat_length = get_min_cleat_height(bolts_reqrd, bolt_dia) 

        if cleat_length < min_cleat_length:
            design_check = False
            logger.error(':Cleat length provided is less than the minimum cleat length ')
            logger.warning(':Cleat length should be greater than %2.2f mm' %(min_cleat_length))
        if min_cleat_length < cleat_length < max_cleat_height:
            pass
        if cleat_length > max_cleat_height:
            design_check = False            
            logger.error(':Cleat length provided is more than the maximum possible cleat length')
            logger.warning(':Cleat length should not be greater than %2.2f mm' %(max_cleat_height))
    else:
        cleat_length = (2 * min_edge_dist + min_pitch * (bolts_required - 1))
        if cleat_length > max_cleat_height:
            cleat_length = max_cleat_height
    
    
    ####################################################
##COLUMN FLANGE-BEAM WEB CONNECTIVITY  
     
    if connectivity == 'Column flange-Beam web':
        avbl_space = column_D - 2 * (column_f_t + column_R1)
        required_space = 2 * cleat_legsize_1 + beam_w_t
        if avbl_space < required_space:
            design_check = False
            logger.error(':Column cannot accommodate the given cleat agle due to space restriction  ')
            logger.warning(':The depth of the column(D) should be greater than %2.2f mm' %(required_space)) 
            logger.info('Decrease the legsize of the cleat angle')
        if avbl_space < beam_B:
            design_check = False
            logger.error(':Depth of the column is less than flange width of the beam  ')
            logger.warning(':The depth of the column(D) should be greater than %2.2f mm' %(beam_B)) 
            logger.info('Decrease the legsize of the cleat angle')
    elif connectivity == 'Column web-Beam web':
        avbl_space = column_B
        required_space = 2 * cleat_legsize_1 + beam_w_t
        if avbl_space < required_space:
            design_check = False
            logger.error(':Column cannot accommodate the given cleat agle due to space restriction  ')
            logger.warning(':The flange width of the column(B) should be greater than %2.2f mm' %(required_space)) 
            logger.info('Decrease the legsize of the cleat angle')
        if avbl_space < beam_B:
            design_check = False
            logger.error(':Depth of the column is less than flange width of the beam  ')
            logger.warning(':The depth of the column(D) should be greater than %2.2f mm' %(beam_B)) 
            logger.info('Decrease the legsize of the cleat angle')
    else:
        pass       
    
    
    
    
    
    # Ask about gauge restriction in Subramanya and dictionaries can be modified accordingly
    # Determine single or double line of bolts for cleat leg which is connected to beam flange
    # double_row_a, double_row_b, single_row_c are the values of a , b , c in page 341, Subramanya
    double_row_a = {100 : 40 , 110 : 45 , 115 : 45 , 125 : 45 , 130 : 50 , 150 : 55 , 200 : 75}
    double_row_b = {100 : 40 , 110 : 45 , 115 : 50 , 125 : 55 , 130 : 55 , 150 : 65 , 200 : 85}
    single_row_c = {55 : 30 , 60 : 35 , 65 : 35 , 70 : 40 , 75 : 40 , 80 : 45 , 90 : 50 , 95 : 55 , 100 : 60 , 110 : 65 , 115 : 70 , 125 : 75 , 130 : 80 , 150 : 90 , 200 : 115}
    max_dbl_row_bolt_dia = {100 : 12 , 110 : 12 , 115 : 12 , 125 : 20 , 130 : 20 , 150 : 22 , 200 : 27}             
    
    length_avail = (cleat_length-2*min_edge_dist)
    pitch = round(length_avail/(bolts_required-1),3)
    beam_eccentricity = 0.0
    end_dist = 0
    gauge = 0
    # column_eccentricity = 0.0
    # Single line of bolts
    
    if pitch >= min_pitch:
        bolt_line =1
        gauge = 0
        bolts_one_line = bolts_required
        beam_eccentricity = single_row_c[cleat_legsize]
        end_dist = cleat_legsize - single_row_c[cleat_legsize]
    #         column_eccentricity = single_row_c[cleat_legsize]
    
    # Multi-line of bolts
    # Double line of bolts is not possible in all cleat leg size
    # According to the guidelines provided by SP-1 of Bureau of Indian Standards / page-341 Subramanya
    if pitch < min_pitch:
        bolt_line = 2;
        if bolts_required % 2 == 0:
            bolts_one_line = bolts_required/2
            if bolts_one_line <= 1 :
                bolts_one_line = 2
            else:
                pass    
        else:
            bolts_one_line = int(bolts_required/2) + 1
            if bolts_one_line == 1:
                bolts_one_line = 2
                
        
        pitch = round(length_avail/(bolts_one_line-1),3) # pitch again modified
        gauge = min_gauge
        beam_eccentricity = single_row_c[cleat_legsize]
        end_dist = (single_row_c[cleat_legsize] + min_gauge/2)
                
        bolts_required = 2 * bolts_one_line     
    
    #  have bolt line, and all other parameters to check the design
    # Will incorporate gauge restrictions and also error message for leg sizes where double bolt line is not favourable   
    # calculating new bolts group capacity
    bolt_group_capacity = bolts_required * bolt_capacity 
    
    
    ####################  pitch and gauge modifications  ####################
    edge_distance = min_edge_dist
    if length_input == False:
        pitch = int((pitch - 5) / 5) *5 + 5
        cleat_length = 2 * min_edge_dist + (bolts_one_line -1) * pitch
        if cleat_length % 10 != 0:
            cleat_length = int(cleat_length / 10) * 10 +10
        edge_distance = float((cleat_length - (bolts_one_line - 1) * pitch) / 2 )
        if edge_distance % 5 != 0 :
            edge_distance = int(edge_distance / 5) * 5 + 5
        cleat_length = 2 * edge_distance + (bolts_one_line - 1) * pitch
        
    if pitch < min_pitch:
        design_check = False
        logger.error(':The cleat cannot accommodate the calculated number of bolts due to pitch restriction')
        logger.warning(':The pitch calculated by the program is less than the minimum pitch specified by IS 800')
        logger.info(':Reference -clause-10.22 IS 800 ')
    if pitch > max_spacing:
        if length_input == False:
            pitch = max_spacing
            cleat_length = edge_distance * 2 + (bolts_one_line - 1) * pitch
        else:
            design_check = False
            logger.error(':The cleat cannot accommodate the calculated number of bolts due to pitch restriction')    
            logger.warning(':The pitch calculated by the program is greater than the maximum spacing specified by IS 800')
            logger.info(':Reference -clause-10.23 IS 800 ')
    
    ######################## Connection to beam flange #############################
    
    bearing_capcity = bolt_bearing(dia_hole, t_thinner, bolt_fu)
    bolt_shear_value = 0.0
    if bolt_type == 'Black Bolt':
        bolt_shear_value = black_bolt_shear(bolt_dia, 1, bolt_fu)
    if bolt_type == 'HSFG':
        bolt_shear_value = HSFG_bolt_shear(0.48, bolt_dia, 1, bolt_fu)
    critical_bolt_capacity = min(bearing_capcity,bolt_shear_value)
    
        # single line bolt arrangement
    critical_shear = critical_bolt_shear(bolt_line, bolts_one_line, bolts_required, pitch, gauge, shear_load, beam_eccentricity)
    # new logger can be called including double line restriction
    
    if bolt_line == 1 and (critical_shear > critical_bolt_capacity): 
        bolts_one_line = bolts_one_line - 1
        edge_distance = (cleat_length - pitch * (bolts_one_line - 1)) / 2
        bolts_required = 2 * (bolts_one_line)
        gauge = min_gauge
        bolt_line = 2
        critical_shear = critical_bolt_shear(bolt_line, bolts_one_line, bolts_required, pitch, gauge, shear_load, beam_eccentricity)
        if  (critical_shear > critical_bolt_capacity):
            bolts_one_line = bolts_one_line + 1
            bolts_required = 2 * (bolts_one_line)
            edge_distance = (cleat_length - pitch * (bolts_one_line - 1)) / 2
            critical_shear = critical_bolt_shear(bolt_line, bolts_one_line, bolts_required, pitch, gauge, shear_load, beam_eccentricity)
    if (bolt_line == 2) and (cleat_legsize not in double_row_b):
        design_check = False
        logger.error(":Design requires double lines of bolt which is not possible in the given cleat section ")
        logger.warning (":Increase leg size of cleat section")
           
    
    if critical_shear > critical_bolt_capacity :  
        logger.error(":Bolt strength is insufficient to carry the shear force")
        logger.warning (":Increase bolt diameter or bolt grade")
        design_check = False
    else:
        pass
                
    
    
            
    ############################connection column flange  ###############################        
    # most of the variables started with 'c' is just indicate that the connectivity..'c' represents column  
    c_bolt_line = 1 # this variable is to introduce any further modification on bolt line
    thk_thinner =0.0
    if connectivity == 'Column flange-Beam web':
        thk_thinner = min(cleat_thk , column_f_t) 
    elif connectivity == 'Column web-Beam web':
        thk_thinner = min(cleat_thk , column_w_t)
    else:
        thk_thinner = min(cleat_thk , column_w_t)
        
    c_end_dist = 0.0
    c_bolt_bearing = bolt_bearing(dia_hole, thk_thinner, bolt_fu)
    c_bolt_shear_capacity = bolt_shear_value
    c_bolt_capacity = min(c_bolt_bearing , c_bolt_shear_capacity)
    c_bolts_required = int(0.5 * shear_load / c_bolt_capacity)+ 1 # need to discuss regarding double line bolts in on column flange
    c_bolts_one_line = 0
    if c_bolts_required <= 2:
        c_bolts_required = 3
        
    
    ############################determining pitch , bolt line and gauge ############################
    
    c_length_avail = (cleat_length-2*min_edge_dist)
    c_pitch = round(c_length_avail/(c_bolts_required-1),3)
    c_eccentricity = 0.0
    c_gauge_type_1 = 0.0
    c_gauge_type_2 = 0.0
    
    
    # Single line of bolts
    if c_pitch >= min_pitch:
        c_bolt_line =1
        c_pitch = pitch
        c_bolts_one_line = c_bolts_required
        c_gauge_type_1 = float(beam_w_t + 2 * single_row_c[cleat_legsize])
        c_gauge_type_2 = 0.0
        c_eccentricity = c_gauge_type_1 / 2
        c_end_dist = cleat_legsize_1 - single_row_c[cleat_legsize_1]    
    
    
    
    # Multi-line of bolts
    # Double line of bolts is not possible in all cleat leg size
    # According to the guidelines provided by SP-1 of Bureau of Indian Standards / page-341 Subramanya
    if c_pitch < min_pitch:
        c_bolt_line = 2
        if c_bolts_required % 2 == 0:
            c_bolts_one_line = c_bolts_required/2
            if c_bolts_one_line <= 2 :
                c_bolts_one_line = 3
               
        else:
            c_bolts_one_line = int(c_bolts_required/2) + 1
            if c_bolts_one_line <= 2 :
                c_bolts_one_line = 3
        
        c_pitch = round(length_avail/(c_bolts_one_line-1),3)
        c_gauge_type_2 = min_gauge
        c_eccentricity = float(beam_w_t / 2 + single_row_c[cleat_legsize_1])
        c_end_dist = cleat_legsize_1 - single_row_c[cleat_legsize_1] - min_gauge/2
        c_bolts_required = 2 * c_bolts_one_line 
         
    if c_pitch < min_pitch:
        design_check = False
        logger.error(':The cleat cannot accommodate the calculated number of bolts due to pitch restriction')
        logger.warning(':The pitch calculated by the program for connection to the column is less than the minimum pitch specified by IS 800')
        logger.info(':Reference -clause-10.22 IS 800 ')
    if c_pitch > max_spacing:
        c_pitch = max_spacing
        
    c_edge_distance = round((cleat_length - (c_bolts_one_line - 1) * c_pitch) * 0.5 , 2)      
    
    # pitch,gauge and bolt diameter is same as which is used in beam web
    
    # Horizontal shear force on bolt due to moment due to eccentricity
    critical_shear_1 = column_critical_shear(c_bolt_line, c_bolts_one_line, c_bolts_required, c_pitch, c_gauge_type_2, shear_load, c_eccentricity, c_edge_distance)
    # if single line of bolts fails then going for double line
    if c_bolt_line == 1 and (critical_shear_1 > c_bolt_capacity):
        if c_bolts_one_line > 3:
            c_bolts_one_line = c_bolts_one_line - 1
        c_edge_distance = (cleat_length - (c_bolts_one_line - 1) * c_pitch) * 0.5
        c_bolts_required = 2 * c_bolts_one_line
        c_gauge_type_2 = min_gauge
        c_bolt_line = 2
        critical_shear_1 = column_critical_shear(c_bolt_line, c_bolts_one_line, c_bolts_required, c_pitch, c_gauge_type_2, shear_load, c_eccentricity, c_edge_distance)
        if critical_shear_1 > c_bolt_capacity:
            c_bolts_one_line = c_bolts_one_line + 1
            c_bolts_required = 2 * c_bolts_one_line
            c_edge_distance = (cleat_length - (c_bolts_one_line - 1) * c_pitch) * 0.5
            critical_shear_1 = column_critical_shear(c_bolt_line, c_bolts_one_line, c_bolts_required, c_pitch, c_gauge_type_2, shear_load, c_eccentricity, c_edge_distance)
            
    if (c_bolt_line == 2) and (cleat_legsize_1 not in double_row_b):
        design_check = False
        logger.error(":Design requires double lines of bolt which is not possible in the given cleat section ")
        logger.warning (":Increase leg size of cleat section")
    
    if critical_shear_1 > c_bolt_capacity :
        logger.error(':column cleat connectivity is unsafe')
        logger.warning(':Increase the diameter or grade of the bolts') 
        design_check = False
    else:
        pass
            
    
    # checking the moment capacity of cleat angle
    moment_demand = 0.5 * shear_load * c_eccentricity / 1000
    moment_capacity = 1.2 * cleat_fy * cleat_thk * cleat_length * cleat_length / 1000000
    if moment_capacity < moment_demand:
        design_check = False
        logger.error(":Plate moment capacity is less than the moment demand")
        logger.warning(":Re-design with increased plate dimensions")
    ######################
#     if connectivity == 'Column flange-Beam web' or  'Column web-Beam web':
#         avbl_space = 2 * cleat_legsize_1 + beam_w_t 
#         required_space = 2 * cleat_legsize_1 + beam_w_t
#         c_gauge = 2 * cleat_legsize_1 + beam_w_t - 2*(c_end_dist + (c_bolt_line -1) * c_gauge_type_2)
#         end = cleat_legsize - end_dist - gauge *(bolt_line - 1)
#         if c_gauge < 90 :
#             design_check = False
#             logger.error(':cross center distance between bolts should be greater than 90 mm and less than 140mm ')
# #                 logger.warning(':The depth of the column(D) should be greater than %2.2f mm' %(required_space)) 
#             logger.info('Increse the legsize of the cleat angle')
#         if end < min_edge_dist:
#             design_check = False
#             logger.error(':The cleat cannot accommodate required bolts due to insufficient end distance ')
#             logger.warning(':The end distance should be greater than %2.2f mm' %(min_edge_dist)) 
# #                 logger.info('Decrease the legsize of the cleat angle')
#     
#             
#             
            
            
            
            
            
            
#         elif connectivity == 'Column web-Beam web':
#         avbl_space = column_B
#         required_space = 2 * cleat_legsize_1 + beam_w_t
#         if avbl_space < required_space:
#             design_check = False
#             logger.error(':Column cannot accommodate the given cleat agle due to space restriction  ')
#             logger.warning(':The flange width of the column(B) should be greater than %2.2f mm' %(required_space)) 
#             logger.info('Decrease the legsize of the cleat angle')
#         if avbl_space < beam_B:
#             design_check = False
#             logger.error(':Depth of the column is less than flange width of the beam  ')
#             logger.warning(':The depth of the column(D) should be greater than %2.2f mm' %(beam_B)) 
#             logger.info('Decrease the legsize of the cleat angle')
#     else:
#         pass                
    #####################################################################################
    
    
           
     # End of calculation
    outputObj = {}
    outputObj['Bolt'] ={}
    outputObj['Bolt']['status'] = True
    outputObj['Bolt']['shearcapacity'] = round(bolt_shear_capacity,3)
    outputObj['Bolt']['bearingcapacity'] = round(bolt_bearing_capacity,3)
    outputObj['Bolt']['boltcapacity'] = round(bolt_capacity,3)
    outputObj['Bolt']['numofbolts'] = bolts_required
    outputObj['Bolt']['boltgrpcapacity'] = round(bolt_group_capacity,3)
    outputObj['Bolt']['numofrow'] = bolts_one_line
    outputObj['Bolt']['numofcol'] = bolt_line
    outputObj['Bolt']['pitch'] = pitch
    outputObj['Bolt']['enddist'] = int(end_dist)
    outputObj['Bolt']['edge'] = int(edge_distance)
    outputObj['Bolt']['gauge'] = int(gauge)
#     outputObj['Bolt']['grade'] = bolt_grade
      
     
    outputObj['cleat'] = {}
    #     outputObj['Plate']['minHeight'] = web_plate_l_req
    outputObj['cleat']['height'] = int(cleat_length)
#     outputObj['cleat']['width'] = cleat_legsize
    outputObj['cleat']['externalmoment'] = round(moment_demand ,3)
    outputObj['cleat']['momentcapacity'] = round(moment_capacity,3)
    outputObj['cleat']['numofrow'] = c_bolts_one_line
    outputObj['cleat']['numofcol'] = c_bolt_line
    
    outputObj['cleat']['pitch'] = c_pitch
    outputObj['cleat']['guage'] = c_gauge_type_2
    outputObj['cleat']['edge'] = c_edge_distance
    outputObj['cleat']['end'] = c_end_dist
    outputObj['cleat']['legsize'] = cleat_legsize_1
#     print c_end_dist
#     print c_edge_distance
#     print c_gauge_type_2
#           
         
        
          
    
    if design_check == False:
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                outputObj[k][key] = ""
                    
    if outputObj['Bolt']['status'] == True:  
        logger.info(": Overall finplate connection design is safe \n")
        logger.info(" :=========End Of design===========")
          
    else:
        logger.error(": Design is not safe \n ")
        logger.error(" :=========End Of design===========")
      
    return outputObj                          
    







    