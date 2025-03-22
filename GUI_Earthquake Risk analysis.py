import arcpy as ap
from arcpy.sa import *
import wx
import random
import numpy as np

def AUTO_Zoning(event):
    

    def Browse_LO_Input1(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "faultdist.tif", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        gosal = openFileDialog.GetPath()
        txtLO1.SetValue(gosal)
        openFileDialog.Destroy()


    def Browse_LO_Input2(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "Tarakom.shp", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        tarakom = openFileDialog.GetPath()
        txtLO2.SetValue(tarakom)
        openFileDialog.Destroy()


    def Browse_LO_Input3(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "TaminSokht.shp", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        tamin_sookht = openFileDialog.GetPath()
        txtLO3.SetValue(tamin_sookht)
        openFileDialog.Destroy()


    def Browse_LO_Input4(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "enteghalNiroo.shp", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        enteghal_niroo = openFileDialog.GetPath()
        txtLO4.SetValue(enteghal_niroo)
        openFileDialog.Destroy()


    def Browse_LO_Output(event):
            openFileDialog = wx.FileDialog(win11, "Save", "", "", 
                  "", 
                   wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

            openFileDialog.ShowModal()
            Output_Raster = openFileDialog.GetPath()
            txtLO5.SetValue(Output_Raster)
            openFileDialog.Destroy()



    def Zoning_ANALIZE(event):
        gosal = txtLO1.GetValue()
        tarakom = txtLO2.GetValue()
        tamin_sookht = txtLO3.GetValue()
        enteghal_niroo = txtLO4.GetValue()
        Output_Locating_Result = txtLO5.GetValue()
        
        win11.Close()

        num = random.random()
        ap.CheckOutExtension("Spatial")

        arcpy.env.extent = arcpy.Extent(534906.040766,3955219.924330, 543061.284793, 3961153.875958)
        
        #Euc_Dist_gosal=arcpy.sa.EucDistance(gosal, '#', '23.7358065111749', '#')
        Euc_Dist_tarakom=arcpy.sa.EucDistance(tarakom, '#', '23.7358065111749', '#')
        Euc_Dist_tamin_sookht=arcpy.sa.EucDistance(tamin_sookht, '#', '23.7358065111749', '#')
        Euc_Dist_enteghal_niroo=arcpy.sa.EucDistance(enteghal_niroo, '#', '23.7358065111749', '#')

        #fuzzy membership functions
        Tarakom_Far=arcpy.sa.FuzzyMembership(Euc_Dist_tarakom, 'LINEAR 40 450', 'NONE')
        Tarakom_Near=arcpy.sa.FuzzyMembership(Euc_Dist_tarakom, 'LINEAR 450 40', 'NONE')
        
        Gosal_Far=arcpy.sa.FuzzyMembership(gosal, 'LINEAR 1500 7000', 'NONE')
        Gosal_Near=arcpy.sa.FuzzyMembership(gosal, 'LINEAR 7000 1500', 'NONE')
        
        Sookht_Far=arcpy.sa.FuzzyMembership(Euc_Dist_tamin_sookht, 'LINEAR 200 950', 'NONE')
        Sookht_Near=arcpy.sa.FuzzyMembership(Euc_Dist_tamin_sookht, 'LINEAR 950 200', 'NONE')

        Niroo_Far=arcpy.sa.FuzzyMembership(Euc_Dist_enteghal_niroo, 'LINEAR 75 800', 'NONE')
        Niroo_Near=arcpy.sa.FuzzyMembership(Euc_Dist_enteghal_niroo, 'LINEAR 800 75', 'NONE')

        #fuzzy overlay
        R1 =FuzzyOverlay([Gosal_Near,Tarakom_Far,Sookht_Far,Niroo_Far], 'AND')
        R2 =FuzzyOverlay([Gosal_Near,Tarakom_Near,Sookht_Far,Niroo_Far], 'AND')
        R3 =FuzzyOverlay([Gosal_Near,Tarakom_Far,Sookht_Near,Niroo_Far], 'AND')
        R4 =FuzzyOverlay([Gosal_Near,Tarakom_Far,Sookht_Far,Niroo_Near], 'AND')
        R5 =FuzzyOverlay([Gosal_Near,Tarakom_Near,Sookht_Near,Niroo_Far], 'AND')
        R6 =FuzzyOverlay([Gosal_Near,Tarakom_Far,Sookht_Far,Niroo_Near], 'AND')
        R7 =FuzzyOverlay([Gosal_Near,Tarakom_Far,Sookht_Near,Niroo_Near], 'AND')
        R8 =FuzzyOverlay([Gosal_Near,Tarakom_Near,Sookht_Near,Niroo_Near], 'AND')
        R9 =FuzzyOverlay([Gosal_Far,Tarakom_Near,Sookht_Far,Niroo_Far], 'AND')
        R10=FuzzyOverlay([Gosal_Far,Tarakom_Near,Sookht_Near,Niroo_Far], 'AND')
        R11=FuzzyOverlay([Gosal_Far,Tarakom_Near,Sookht_Far,Niroo_Near], 'AND')
        R12=FuzzyOverlay([Gosal_Far,Tarakom_Near,Sookht_Near,Niroo_Near], 'AND')
        R13=FuzzyOverlay([Gosal_Far,Tarakom_Far,Sookht_Near,Niroo_Far], 'AND')
        R14=FuzzyOverlay([Gosal_Far,Tarakom_Far,Sookht_Near,Niroo_Near], 'AND')
        R15=FuzzyOverlay([Gosal_Far,Tarakom_Far,Sookht_Far,Niroo_Near], 'AND')
        R16=FuzzyOverlay([Gosal_Far,Tarakom_Far,Sookht_Far,Niroo_Far], 'AND')

        #makhraje simplified
        rule=[R1,R2,R3,R4, R5 ,R6 ,R7 ,R8 ,R9,R9,R10,R12,R13,R14,R15]
        total=0

        
        p1=Plus(R1,R2)
        p2=Plus(R3,R4)
        p3=Plus(R5,R6)
        p4=Plus(R7,R8)
        p5=Plus(R9,R10)
        p6=Plus(R11,R12)
        p7=Plus(R13,R14)
        p8=Plus(R15,R16)
        j1=Plus(p1,p2)
        j2=Plus(p3,p4)
        j3=Plus(p5,p6)
        j4=Plus(p7,p8)
        u1=Plus(j1,j2)
        u2=Plus(j3,j4)
        total=Plus(u1,u2)
        
        #soorate simplified 
        z1=np.multiply(R1,2)
        z2=np.multiply(R2,3)
        z3=np.multiply(R3,3)
        z4=np.multiply(R4,3)
        z5=np.multiply(R5,4)
        z6=np.multiply(R6,4)
        z7=np.multiply(R7,4)
        z8=np.multiply(R8,5)
        z9=np.multiply(R9,1)
        z10=np.multiply(R10,2)
        z11=np.multiply(R11,2)
        z12=np.multiply(R12,3)
        z13=np.multiply(R13,1)
        z14=np.multiply(R14,2)
        z15=np.multiply(R15,1)
        z16=np.multiply(R16,1)

        Z1=Plus(z1,z2)
        Z2=Plus(z3,z4)
        Z3=Plus(z5,z6)
        Z4=Plus(z7,z8)
        Z5=Plus(z9,z10)
        Z6=Plus(z11,z12)
        Z7=Plus(z13,z14)
        Z8=Plus(z15,z16)
        S1=Plus(Z1,Z2)
        S2=Plus(Z3,Z4)
        S3=Plus(Z5,Z6)
        S4=Plus(Z7,Z8)
        U1=Plus(S1,S2)
        U2=Plus(S3,S4)
        ToTal=Plus(U1,U2)
       
        #simplified 
        simplif=np.divide(ToTal,total)
        simplif.save(Output_Locating_Result.replace(Output_Locating_Result.split('\\')[-1],
                                                    'simp' + str(num)[2:4]))
        
        #fuzzy membership pahne bandi #monaseb va namonaseb 
        maax_out=simplif.maximum
        namonaseb=np.divide(simplif,maax_out)
        namonaseb.save(Output_Locating_Result.replace(Output_Locating_Result.split('\\')[-1],
                                                      'pmonsb' + str(num)[2:4]))
        monaseb=1-namonaseb
        monaseb.save(Output_Locating_Result.replace(Output_Locating_Result.split('\\')[-1],
                                                    'pnmonsb' + str(num)[2:4]))

        #khorooji nahayi
        final=Reclassify(simplif, 'Value',
                         '1 1.600000 1;1.600000 2.200000 2;2.200000 2.574404 3;2.574404 3.400000 4;3.400000 4 5',
                         'DATA')
        final.save(Output_Locating_Result.replace(Output_Locating_Result.split('\\')[-1],
                                                  'Final' + str(num)[2:4]))
        
        

        


    app= wx.App()
    win11=wx.Frame(None, title="AUTO_Zoning",size=(750,350))

    statictxtLO1=wx.StaticText(win11, label="Fault: ", pos=(10,10), size=(150, 20))
    txtLO1=wx.TextCtrl(win11, pos=(10,30),size=(640,25))

    statictxtLO2=wx.StaticText(win11, label="Population Density: ", pos=(10,60), size=(150, 40))
    txtLO2=wx.TextCtrl(win11, pos=(10,80),size=(640,25))

    statictxtLO3=wx.StaticText(win11, label="Gas Station: ", pos=(10,110), size=(150, 40))
    txtLO3=wx.TextCtrl(win11, pos=(10,130),size=(640,25))

    statictxtLO4=wx.StaticText(win11, label="Power Transmission: ", pos=(10,160), size=(150, 40))
    txtLO4=wx.TextCtrl(win11, pos=(10,180),size=(640,25))

    statictxtLO5=wx.StaticText(win11, label="Output Zoning Result: ", pos=(10,210), size=(150, 40))
    txtLO5=wx.TextCtrl(win11, pos=(10,230),size=(640,25))

    btnLO5=wx.Button(win11, label='Browse',pos=(660,230),size=(60,25))
    btnLO5.Bind(wx.EVT_BUTTON, Browse_LO_Output)

    btnLO4=wx.Button(win11, label='Browse',pos=(660,180),size=(60,25))
    btnLO4.Bind(wx.EVT_BUTTON, Browse_LO_Input4)
  
    btnLO3=wx.Button(win11, label='Browse',pos=(660,130),size=(60,25))
    btnLO3.Bind(wx.EVT_BUTTON, Browse_LO_Input3)

    btnLO2=wx.Button(win11, label='Browse',pos=(660,80),size=(60,25))
    btnLO2.Bind(wx.EVT_BUTTON, Browse_LO_Input2)
    
    btnLO1=wx.Button(win11, label='Browse',pos=(660,30),size=(60,25))
    btnLO1.Bind(wx.EVT_BUTTON, Browse_LO_Input1)


    btnLO6=wx.Button(win11, label='Run',pos=(10,270),size=(100,25))
    btnLO6.Bind(wx.EVT_BUTTON,Zoning_ANALIZE)

    

    win11.Show()
    app.MainLoop()
    
#***********************************************************************************#
def AUTO_Locating(event):
    

    def Browse_LO_Input1(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        pmonaseb = openFileDialog.GetPath()
        txtLO1.SetValue(pmonaseb)
        openFileDialog.Destroy()

        
    def Browse_LO_Input2(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        
        openFileDialog.ShowModal()
        pnamonaseb = openFileDialog.GetPath()
        txtLO2.SetValue(pnamonaseb)
        openFileDialog.Destroy()


    def Browse_LO_Input3(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "hospitalNetwork1.tif", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        hospital = openFileDialog.GetPath()
        txtLO3.SetValue(hospital)
        openFileDialog.Destroy()


    def Browse_LO_Input4(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "firestationNetwork1.tif", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        fire_station = openFileDialog.GetPath()
        txtLO4.SetValue(fire_station)
        openFileDialog.Destroy()


    def Browse_LO_Input5(event):
        openFileDialog = wx.FileDialog(win11, "Open", "", "", 
              "road.shp", 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        road = openFileDialog.GetPath()
        txtLO5.SetValue(road)
        openFileDialog.Destroy()


    def Browse_LO_Output(event):
            openFileDialog = wx.FileDialog(win11, "Save", "", "", 
                  "", 
                   wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

            openFileDialog.ShowModal()
            Output_Raster = openFileDialog.GetPath()
            txtLO6.SetValue(Output_Raster)
            openFileDialog.Destroy()



    def LOCATING_ANALIZE(event):
        monaseb = txtLO1.GetValue()
        namonaseb = txtLO2.GetValue()
        hospital = txtLO3.GetValue()
        fire_station = txtLO4.GetValue()
        road = txtLO5.GetValue()
        Output_Locating_Result = txtLO6.GetValue()
        
        win11.Close()

        num = random.random()
        ap.CheckOutExtension("Spatial")
        arcpy.env.extent = arcpy.Extent(534906.040766,3955219.924330, 543061.284793, 3961153.875958)

        Euc_Dist_road=arcpy.sa.EucDistance(road, '#', '23.7358065111749', '#')

        road_Far=arcpy.sa.FuzzyMembership(Euc_Dist_road, 'LINEAR 70 600', 'NONE')
        road_Near=arcpy.sa.FuzzyMembership(Euc_Dist_road, 'LINEAR 600 70', 'NONE')
        
        hosp_Far=arcpy.sa.FuzzyMembership(hospital, 'LINEAR 250 2500', 'NONE')
        hosp_Near=arcpy.sa.FuzzyMembership(hospital, 'LINEAR 2500 250', 'NONE')
        
        fire_Far=arcpy.sa.FuzzyMembership(fire_station, 'LINEAR 500 3000', 'NONE')
        fire_Near=arcpy.sa.FuzzyMembership(fire_station, 'LINEAR 3000 500', 'NONE')


        
        #fuzzy overlay
        Ru1 =FuzzyOverlay([road_Far,hosp_Far,fire_Far], 'AND')
        Ru2 =FuzzyOverlay([monaseb,road_Near,hosp_Far,fire_Far], 'AND')
        Ru3 =FuzzyOverlay([monaseb,road_Far,hosp_Near,fire_Far], 'AND')
        Ru4 =FuzzyOverlay([monaseb,road_Far,hosp_Far,fire_Near], 'AND')
        Ru5 =FuzzyOverlay([monaseb,road_Near,hosp_Near,fire_Far], 'AND')
        Ru6 =FuzzyOverlay([monaseb,road_Far,hosp_Far,fire_Near], 'AND')
        Ru7 =FuzzyOverlay([monaseb,road_Far,hosp_Near,fire_Near], 'AND')
        Ru8 =FuzzyOverlay([monaseb,road_Near,hosp_Near,fire_Near], 'AND')
        Ru9 =FuzzyOverlay([namonaseb,road_Near,hosp_Far,fire_Far], 'AND')
        Ru10=FuzzyOverlay([namonaseb,road_Near,hosp_Near,fire_Far], 'AND')
        Ru11=FuzzyOverlay([namonaseb,road_Near,hosp_Far,fire_Near], 'AND')
        Ru12=FuzzyOverlay([namonaseb,road_Near,hosp_Near,fire_Near], 'AND')
        Ru13=FuzzyOverlay([namonaseb,road_Far,hosp_Near,fire_Far], 'AND')
        Ru14=FuzzyOverlay([namonaseb,road_Far,hosp_Near,fire_Near], 'AND')
        Ru15=FuzzyOverlay([namonaseb,road_Far,hosp_Far,fire_Near], 'AND')
        Ru16=FuzzyOverlay([namonaseb,road_Far,hosp_Far,fire_Far], 'AND')
        

    app= wx.App()
    win11=wx.Frame(None, title="AUTO_LOCATING",size=(750,400))

    statictxtLO1=wx.StaticText(win11, label="fuzzy membership monaseb: ", pos=(10,10), size=(220, 20))
    txtLO1=wx.TextCtrl(win11, pos=(10,30),size=(640,25))

    statictxtLO2=wx.StaticText(win11, label="fuzzy membership monaseb: ", pos=(10,60), size=(200, 20))
    txtLO2=wx.TextCtrl(win11, pos=(10,80),size=(640,25))

    statictxtLO3=wx.StaticText(win11, label="hospital: ", pos=(10,110), size=(150, 20))
    txtLO3=wx.TextCtrl(win11, pos=(10,130),size=(640,25))

    statictxtLO4=wx.StaticText(win11, label="Fire station: ", pos=(10,160), size=(150, 20))
    txtLO4=wx.TextCtrl(win11, pos=(10,180),size=(640,25))

    statictxtLO5=wx.StaticText(win11, label="road: ", pos=(10,210), size=(150, 20))
    txtLO5=wx.TextCtrl(win11, pos=(10,230),size=(640,25))

    statictxtLO56=wx.StaticText(win11, label="Output Locating Result: ", pos=(10,260), size=(150, 20))
    txtLO6=wx.TextCtrl(win11, pos=(10,280),size=(640,25))

    btnLO6=wx.Button(win11, label='Browse',pos=(660,280),size=(60,25))
    btnLO6.Bind(wx.EVT_BUTTON, Browse_LO_Output)

    btnLO5=wx.Button(win11, label='Browse',pos=(660,230),size=(60,25))
    btnLO5.Bind(wx.EVT_BUTTON, Browse_LO_Input5)
  
    btnLO4=wx.Button(win11, label='Browse',pos=(660,180),size=(60,25))
    btnLO4.Bind(wx.EVT_BUTTON, Browse_LO_Input4)

    btnLO3=wx.Button(win11, label='Browse',pos=(660,130),size=(60,25))
    btnLO3.Bind(wx.EVT_BUTTON, Browse_LO_Input3)

    btnLO2=wx.Button(win11, label='Browse',pos=(660,80),size=(60,25))
    btnLO2.Bind(wx.EVT_BUTTON, Browse_LO_Input2)

    
    btnLO1=wx.Button(win11, label='Browse',pos=(660,30),size=(60,25))
    btnLO1.Bind(wx.EVT_BUTTON, Browse_LO_Input1)


    btnLO6=wx.Button(win11, label='Run',pos=(10,330),size=(100,25))
    btnLO6.Bind(wx.EVT_BUTTON,LOCATING_ANALIZE)

    

    win11.Show()
    app.MainLoop()
#*************************************************************#
    

app= wx.App()
win=wx.Frame(None, title="Choose ToolBox",size=(270,225))

btn1=wx.Button(win, label='Automatic Locating',pos=(10,60),size=(230,40))
btn2=wx.Button(win, label='Close',pos=(10,110),size=(230,40))
btn3=wx.Button(win, label='Automatic Zoning',pos=(10,10),size=(230,40))

btn1.Bind(wx.EVT_BUTTON, AUTO_Locating)
btn2.Bind(wx.EVT_BUTTON,quit)
btn3.Bind(wx.EVT_BUTTON,AUTO_Zoning)
win.Show()
app.MainLoop()

        

        
