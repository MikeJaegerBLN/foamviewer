# -*- coding: utf-8 -*-

import os
from matplotlib import pyplot
import tkinter as TK
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import filedialog
from xlwt import Workbook
import numpy
from tkinter import ttk



class ARUPFOAM_Monitor(object):
    
    def __init__(self):
        
        self.inlet_labels = ['inlet', 'Inlet', 'intake', 'Intake']
        self.outlet_labels = ['outlet', 'Outlet', 'Exhaust', 'exhaust']
        
        self.cut_inelets = False
        self.cut_outlets = False
        
        self.bg_color     = '#343837'
        self.text_color   = 'snow'
        self.btn_color    = 'gray25'
        self.btn_color2   = 'gray10'
        self.root         = TK.Tk()
        self.root.geometry('890x750')
        self.root.title('ARUPFOAM Simulation Monitor')
        
        self.show_patches()
    
    
    def show_probes(self):
        
        self.button_probes.config(state='disabled')
        self.button_residuals.config(state='normal')
        self.button_patches.config(state='normal')
        
        self.fig_pro = pyplot.figure(figsize=(10,6), dpi=100)
        self.fig_pro.patch.set_facecolor('xkcd:charcoal')
        self.ax_pro  = self.fig_pro.add_subplot(111)
        
        try:
            self.ax_avg.cla()
            self.ax_res.cla()
        except:
            pass
        
        try:
            self.get_probes()
            
            self.NoProbesLabel = TK.Label(self.frame3, text='Probes found but plotted in next version :)', bg=self.bg_color, fg=self.text_color)
            self.NoProbesLabel.place(x=350, y=200)
        except:
            
            self.frame3 = TK.Frame(self.root, width=2000, height=2000, bg=self.bg_color)
            self.frame3.place(x=0,y=40)
                        
            self.NoProbesLabel = TK.Label(self.frame3, text='No Probes Found!', bg=self.bg_color, fg=self.text_color)
            self.NoProbesLabel.place(x=350, y=200)
        
        
    def get_probes(self):
        
        probes = []
        for j in range(1,len(self.path)):
            if self.path[-j]=='/':
                break
            
        with open(self.path[0:-j] + '/system/controlDict', 'r') as infile:
            lines = infile.readlines()
        
        for i, line in enumerate(lines):
            if 'probeLocations' in line:
                break
            
        for q in range(i+1,len(lines)):
            if '(' in lines[q] and ')' in lines[q]:
                probes.append(lines[q])
            if ';' in lines[q]:
                break
        
        self.probe_labels = []
        self.probe_number = []
        self.probe_values = []
        for o, prob in enumerate(probes):
            for i, char in enumerate(prob):
                if char=='(':
                    break
            probe = str(prob[i+1:]).replace(' ', ',').split(',')
            
            self.probe_labels.append(str(probe[-1][2:]))
            if self.probe_labels[-1]=='':
                self.probe_labels[-1] = str(probe[1:4])
                
            self.probe_number.append(o)
            self.probe_values.append([])
        self.probe_values.append([])
                        
        #print (self.probe_labels)
        #print (self.probe_number)
                
        
        dic = []
        for y in os.listdir(self.path + '/probes'):
            dic.append(int(y))
            
        dic = numpy.max(dic)
        
        no = []
        for h in os.listdir(self.path + '/probes' + '/' + str(dic)):
            for q, sign in enumerate(h):
                if '_' in sign:
                    if not h[q-1]=='p':
                        no.append(int(h[q+1]))
        
        if len(no)==1:
            pass
        if len(no)>1:
            no = numpy.max(no)

        if len(no)==0:
            string = r'/T' 
        else:
            string = r'/T_' + str(no)[1]
            
        with open(self.path + '/probes/' + str(dic) + '/' + string, 'r') as infile:
            lines = infile.readlines()
        
        for q, line in enumerate(lines):
            if 'Time' in line:
                break
        
        for i in range(q+1,len(lines)):
            line = lines[i].replace(' ', ',').split(',')
            probe_no = 0
            for entry in line:
                if not entry == '':
                    self.probe_values[probe_no].append(float(entry))
                    probe_no += 1
                else:
                    pass
                    
       
        
        
    
    def show_residuals(self):
        
        self.button_patches.config(state='normal')
        self.button_residuals.config(state='disabled')
        self.button_probes.config(state='normal')
        
        self.fig_res = pyplot.figure(figsize=(10,6), dpi=100)
        self.fig_res.patch.set_facecolor('xkcd:charcoal')
        self.ax_res  = self.fig_res.add_subplot(111)
        
        self.ax_avg.cla()
        
        self.frame.bind("<Button-1>", self.refresh_chart_residuals)
        
        
        
        self.get_residuals()
        #self.plot_residuals()
        
    
                        
    def get_residuals(self):
        #threading.Timer(5.0, self.get_residuals).start()
        
        dic_temp = []
        for y in os.listdir(self.path + '/residuals'):
            dic_temp.append(int(y))
            
        dic = numpy.max(dic_temp)
        
        no = []
        for h in os.listdir(self.path + '/residuals' + '/' + str(dic)):
            for q, sign in enumerate(h):
                if '_' in sign:
                    no.append(int(h[q+1]))
        
        if len(no)==1:
            pass
        if len(no)>1:
            no = numpy.max(no)

        if len(no)==0:
            string = r'/residuals.dat' 
        else:
            string = r'/residuals_' + str(no)[1] + r'.dat'   
            
        if len(dic_temp)>1:
            with open(self.path + '/residuals/' + str(dic_temp[0]) + '/' + string, 'r') as infile:
                lines = infile.readlines()
                
            for z in range(len(dic_temp)-1):   
                with open(self.path + '/residuals/' + str(dic_temp[z+1]) + '/' + string, 'r') as infile:
                    lines_append = infile.readlines()
                
                for l in range(2,len(lines_append)):
                    lines.append(lines_append[l])
        else:
            with open(self.path + '/residuals/' + str(dic) + '/' + string, 'r') as infile:
                lines = infile.readlines()
        
        self.filepath = str(dic)+string
        self.residual_labels  = []
        k                     = 10
        while k<(len(lines[1])):   
            ind1 = False
            ind2 = True
            k += 1
            for i in range (k, len(lines[1])):
                if not lines[1][i]==' ' and ind2==True:
                    begin = i+1
                    ind1 = True
                    ind2 = False
                if lines[1][i]==' ' and ind1==True:
                    end = i
                    self.residual_labels.append(str(lines[1][begin:end]))
                    k   = i
                    break
        
        self.residual_values = []
        for i in range(len(self.residual_labels)):
            self.residual_values.append([])
        self.residual_iteration = []
            
        for result_no in range(2,len(lines)):
            k           = 5
            result_type = 0
            self.residual_iteration.append(int(result_no-1))
            while k<(len(lines[result_no])): 
                ind2         = True
                ind1         = False
                k           += 1 
                for i in range (k, len(lines[result_no])):
                    if not lines[result_no][i]==' ' and ind2==True:
                        begin = i+1
                        ind2 = False
                        ind1 = True
                    if lines[result_no][i]=='e' and ind1==True:
                        end = i+4
                        self.residual_values[result_type].append(float(lines[result_no][begin:end]))
                        result_type += 1
                        k   = i+3
                        break
        self.plot_residuals()
        
    def plot_residuals(self):
        
        try:
            for i in range(len(self.ax_res.lines)):
                self.ax_res.lines.pop(0)
        except:
            pass
        '''Plot Results'''
        
        
        
        for i in range(len(self.residual_values)):
            self.ax_res.plot(self.residual_iteration, self.residual_values[i], label=self.residual_labels[i])
            
        
        self.ax_res.grid(True)
        self.ax_res.legend(loc=1, fontsize=8, ncol=2)#, bbox_to_anchor=(float(self.xpos_legend.get()),float(self.ypos_legend.get())), ncol=int(self.ncols.get()), fontsize=float(self.legendsize.get()))
        self.ax_res.set_ylabel('Value')
        self.ax_res.set_xlabel('Iteration')
        self.ax_res.set_facecolor('xkcd:charcoal')
        
        self.ax_res.tick_params(axis='x', colors='white')
        self.ax_res.tick_params(axis='y', colors='white')
        self.ax_res.yaxis.label.set_color('white')
        self.ax_res.xaxis.label.set_color('white')
        self.ax_res.grid(True, linestyle=':')
        self.ax_res.set_yscale('log')
               
        self.canvas = FigureCanvasTkAgg(self.fig_res, self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=self.x0-100+40,y=self.y0+70)
        
        self.frame2 = TK.Frame(self.root, width=2000, height=150, bg=self.bg_color)
        self.frame2.place(x=0,y=40)
        self.frame2.bind("<Button-1>", self.refresh_chart_residuals)
        
        self.infolabel2 = TK.Label(self.root, text='CASE:    '  + self.path, bg=self.bg_color, fg=self.text_color)
        self.infolabel2.place(x=self.x0+100, y=self.y0+80)
        self.infolabel2.bind("<Button-1>", self.refresh_chart_residuals)
        
        self.infolabel = TK.Label(self.root, text='FILE:       ' + self.filepath, bg=self.bg_color, fg=self.text_color)
        self.infolabel.place(x=self.x0+100, y=self.y0+100)
        self.infolabel.bind("<Button-1>", self.refresh_chart_residuals)
        
        #self.timer_residuals.enter(60,1,self.get_residuals)
        
        
    def refresh_chart_residuals(self, event):
        
        for i in range(len(self.ax_res.lines)):
            self.ax_res.lines.pop(0)
        self.infolabel2.destroy()
            
        self.get_residuals()
        self.plot_residuals()
             

    
    
    def show_patches(self): 
        
                      
        self.frame = TK.Frame(self.root, width=2000, height=2000, bg=self.bg_color)
        self.frame.place(x=0,y=0)
        
        self.x0    = 10
        self.y0    = 50
        self.fig_avg = pyplot.figure(figsize=(10,6), dpi=100)
        self.fig_avg.patch.set_facecolor('xkcd:charcoal')
        #self.fig_avg.patch.set_alpha(0)
        self.ax_avg  = self.fig_avg.add_subplot(111)
        
        self.button_residuals = TK.Button(self.frame, text='Residuals', width=20, height=2, bg='coral', command=self.show_residuals)
        self.button_residuals.place(x=self.x0,y=0)
        self.button_patches = TK.Button(self.frame, text='Patches', width=20, height=2, state='disabled', bg='coral', command=self.show_patches)
        self.button_patches.place(x=self.x0+240, y=0)
        self.button_probes = TK.Button(self.frame, text='Probes', width=20, height=2, state='normal', bg='coral', command=self.show_probes)
        self.button_probes.place(x=self.x0+480, y=0)
        
        self.button_temperature = TK.Button(self.frame, text='Temperature', width=9 , height=1, bg=self.btn_color, fg=self.text_color, state='disabled') 
        self.button_temperature.place(x=self.x0+240, y=self.y0-10)
        self.button_temperature.config(command=lambda button=self.button_temperature: self.switch_patch(button))
        
        self.button_pressure = TK.Button(self.frame, text='Pressure', width=9, height=1, bg=self.btn_color, fg=self.text_color, state='normal')
        self.button_pressure.config(command=lambda button=self.button_pressure: self.switch_patch(button))
        self.button_pressure.place(x=self.x0+317, y=self.y0-10)
        
        self.button_Ux = TK.Button(self.frame, text='Ux', width=2, height=1, bg=self.btn_color, fg=self.text_color, state='normal') 
        self.button_Ux.config(command=lambda button=self.button_Ux: self.switch_patch(button))
        self.button_Ux.place(x=self.x0+240, y=self.y0+16)
        
        self.button_Uy = TK.Button(self.frame, text='Uy', width=2, height=1, bg=self.btn_color, fg=self.text_color, state='normal') 
        self.button_Uy.config(command=lambda button=self.button_Uy: self.switch_patch(button))
        self.button_Uy.place(x=self.x0+265, y=self.y0+16)
        
        self.button_Uz = TK.Button(self.frame, text='Uz', width=2, height=1, bg=self.btn_color, fg=self.text_color, state='normal') 
        self.button_Uz.config(command=lambda button=self.button_Uz: self.switch_patch(button))
        self.button_Uz.place(x=self.x0+290, y=self.y0+16)
        
        self.button_UMag = TK.Button(self.frame, text='U Magnitude', width=9, height=1, bg=self.btn_color, fg=self.text_color, state='normal') 
        self.button_UMag.config(command=lambda button=self.button_UMag: self.switch_patch(button))
        self.button_UMag.place(x=self.x0+317, y=self.y0+16)
        
        
        self.button_browse = TK.Button(self.frame, text='Browse Case', command=self.get_path, width=10, height=1, bg=self.btn_color, fg=self.text_color)
        self.button_browse.place(x=self.x0, y=self.y0)
        
        self.patch_buttons = [self.button_temperature, self.button_pressure, self.button_Ux, self.button_Uy, self.button_Uz, self.button_UMag]
        
        TK.Button(self.frame, text='Save', command=self.save_results, width=10, height=1, bg=self.btn_color, fg=self.text_color).place(x=self.x0, y=self.y0+40)
        TK.Label(self.frame, text='Save results to ', bg=self.bg_color, fg=self.text_color).place(x=self.x0+80, y=self.y0+35)
        TK.Label(self.frame, text='postProcessing dir as .xsl', bg=self.bg_color, fg=self.text_color).place(x=self.x0+80, y=self.y0+50)
        
        self.button_cut_outlets = TK.Button(self.frame, text='Cut Outlets', command=self.switch_cut_outlets, width=10, height=1, bg=self.btn_color, fg=self.text_color)
        self.button_cut_outlets.place(x=self.x0+394, y=self.y0-35)
        if self.cut_outlets == True:
            self.button_cut_outlets.config(bg='green', text='Plot Outlets')
        
        if hasattr(self, 'residual_labels') or hasattr(self, 'probe_labels'):
            self.refresh_chart_patches('required')
            self.frame.bind("<Button-1>", self.refresh_chart_patches)
      
    def switch_patch(self, button):
        
        for activate_button in self.patch_buttons:
            activate_button.config(state='normal')
        button.config(state='disabled')
        self.refresh_chart_patches('required')
            
    def switch_cut_outlets(self):
        
        if self.cut_outlets==False:
            self.cut_outlets = True
            self.button_cut_outlets.config(bg='green', text='Plot Outlets')
        else:
            self.cut_outlets = False
            self.button_cut_outlets.config(bg=self.btn_color, text='Cut Outlets')
          
        self.refresh_chart_patches('test')
       
            
    def check_outlet_strings(self, resultstring):
        do = True
        if self.cut_outlets==True:
            for outletstring in self.outlet_labels:
                if outletstring in resultstring:
                    do = False
        else:
            pass
        return do

    def clear_results(self):
        
        self.ResultList   = []
        self.AVG_Labels   = []
        self.MAX_Labels   = []
        self.AVG_Curves_T = []
        self.MAX_Curves_T = []
        self.times        = []
        
    def refresh_chart_patches(self, event):
        ### dont do sth with the event, it wont work!
        
        for i in range(len(self.ax_avg.lines)):
            self.ax_avg.lines.pop(0)
        self.infolabel.destroy()
            
        self.clear_results()
        self.get_results()
        
        try: 
            if len(self.AVG_Curves_T[0])<1:
                pass
            else:
                self.plot_results_avg()  
        except:
            pass
        
        
    
        
    def get_path(self):
        
        try:
            for i in range(len(self.ax_avg.lines)):
                self.ax_avg.lines.pop(0)
            self.infolabel.destroy()
        except:
            pass
        
        self.clear_results()
        path = filedialog.askdirectory(initialdir = r'U:\Jobs')
        if path=='':
            pass
        else:
            self.path = path + '/postProcessing'
            #self.path = 'U:/Jobs/267263-00_FR11/Runs/Phase2/20191210_FR11_Model_Update2_AermecChillers_Distributed_V1/postProcessing'
            #print (self.path)
            self.get_results()
            try:
                if len(self.AVG_Curves_T[0])<1:
                    pass
                else:
                    self.plot_results_avg()  
            except:
                pass
            
            self.frame.bind("<Button-1>", self.refresh_chart_patches)
        
        
        
       
        
        
        
    def get_results(self):
        
        ### resultType  - 1 = Temperature, 2 = Pressure
        offset = 0
        ind_U  = 0
        if str(self.button_temperature['state'])=='disabled':
            self.resultType = 1
            offset = 273.15
        if str(self.button_pressure['state'])=='disabled':
            self.resultType = -1
        if str(self.button_UMag['state'])=='disabled':
            self.resultType = 3
        if str(self.button_Ux['state'])=='disabled':
            self.resultType = 3
            ind_U           = 1
        if str(self.button_Uy['state'])=='disabled':
            self.resultType = 3
            ind_U           = 2
        if str(self.button_Uz['state'])=='disabled':
            self.resultType = 3
            ind_U           = 3
            
            
        
        
        for x in os.listdir(self.path):
            self.ResultList.append(x)
        
        for i, label in enumerate(self.ResultList):
            if 'avg' in label:
                if not 'txt' in label:
                    break
        
        ### Get the latest reults dictionary (dic) and .dat file (string) ###
        dic_temp = []
        for y in os.listdir(self.path + '/' + self.ResultList[i]):
            dic_temp.append(int(y))
        
        dic = numpy.max(dic_temp)
        
        no = []
        for h in os.listdir(self.path + '/' + self.ResultList[i] + '/' + str(dic)):
            for q, sign in enumerate(h):
                if '_' in sign:
                    no.append(int(h[q+1]))
        
        if len(no)==1:
            pass
        if len(no)>1:
            no = numpy.max(no)

        if len(no)==0:
            string = r'/surfaceFieldValue.dat' 
        else:
            string = r'/surfaceFieldValue_' + str(no)[1] + r'.dat'                    
                
        ### Getting results ###     
        if len(dic_temp)>1:
            with open(self.path + '/' + self.ResultList[i] + '/' + str(dic_temp[0]) + string, 'r') as infile:
                lines = infile.readlines()
            
            for z in range(len(dic_temp)-1):
                with open(self.path + '/' + self.ResultList[i] + '/' + str(dic_temp[z+1]) + string, 'r') as infile:
                    lines_append = infile.readlines()
    
                for l in range(5,len(lines_append)):
                    lines.append(lines_append[l])
        else:
            if self.ResultList[i]=='residuals':
                Labels = []
                Curves = []
                
            else:
                with open(self.path + '/' + self.ResultList[i] + '/' + str(dic) + string, 'r') as curve:
                    lines = curve.readlines()
                for k in range(5,len(lines)):    
                    lines[k] = lines[k].split('\t')  
                    self.times.append(int(lines[k][0]))
                
                for j in range(len(self.ResultList)):
                    x = self.ResultList[j]
                    do = True
                    if 'avg' in x:
                        if not 'txt' in x:
                            do = self.check_outlet_strings(x)
                            if do==True:                                          
                                self.AVG_Curves_T.append([])       
                                self.AVG_Labels.append(x)
                                
                                if len(dic_temp)>1:
                                    with open(self.path + '/' + x + '/' + str(dic_temp[0]) + string, 'r') as infile:
                                        lines = infile.readlines()
                                    for z in range(len(dic_temp)-1):
                                        with open(self.path + '/' + x + '/' + str(dic_temp[z+1]) + string, 'r') as infile:
                                            lines_append = infile.readlines()
                        
                                        for l in range(5,len(lines_append)):
                                            lines.append(lines_append[l])
                                else:
                                    with open(self.path + '/' + x + '/' + str(dic) + string, 'r') as curve:
                                        lines = curve.readlines()      
                                
                                for k in range(5,len(lines)): 
                                    lines[k] = lines[k].split('\t') 
                                    if self.resultType==3:
                                        line  = lines[k][self.resultType][1:-1].replace(' ', ',').split(',')
                                       
                                        if ind_U==1:
                                            value = abs(float(line[0]))
                                        if ind_U==2:
                                            value = abs(float(line[1]))
                                        if ind_U==3:
                                            value = abs(float(line[2]))
                                        else:
                                            value = numpy.sqrt(float(line[0])**2+float(line[1])**2+float(line[2])**2) 
                                       
                                        self.AVG_Curves_T[-1].append(value)
                                    else:
                                        self.AVG_Curves_T[-1].append(float(lines[k][self.resultType])-offset)
                            else:
                                pass
                            
                    if 'max' in x:
                        self.MAX_Curves_T.append([])       
                        self.MAX_Labels.append(x)
                        with open(self.path + '/' + x + '/' + str(dic) + string, 'r') as curve:
                            lines = curve.readlines()
                            for i in range(len(lines)):
                                lines[i] = lines[i].split('\t')           
                        
                        for k in range(5,len(lines)):          
                            self.MAX_Curves_T[-1].append(float(lines[k][self.resultType])-offset)
                
                Labels = [self.AVG_Labels, self.MAX_Labels]
                Curves = [self.AVG_Curves_T, self.MAX_Curves_T]
                
                self.filepath = str(dic)+string
        
        return Labels, Curves
        
    def save_results(self):
        '''Write Results'''
        self.xslx = Workbook()
        sheet1 = self.xslx.add_sheet('AVG Temperatures')
        sheet2 = self.xslx.add_sheet('MAX Temperatures')
        
        which_time = self.times[self.selecttime.current()]
        for p in range(len(self.times)):
            if self.times[p]==which_time:
                break
        print (which_time)
        for i in range(len(self.AVG_Curves_T)):
            sheet1.write(i,0,str(self.AVG_Labels[i]))
            sheet1.write(i,1,str(self.AVG_Curves_T[i][p]).replace('.',','))
        for i in range(len(self.MAX_Curves_T)):
            sheet2.write(i,0,str(self.MAX_Labels[i]))
            sheet2.write(i,1,str(self.MAX_Curves_T[i][p]).replace('.',',')) 
        
        if self.resultType == 1:
            self.xslx.save(self.path + '\FieldValues_temp.xls')
        if self.resultType == -1:
            self.xslx.save(self.path + '\FieldValues_press.xls')
        
    def plot_results_avg(self):
        #self.ax_avg.cla()
        '''Plot Results'''
        
        maximum = []
        minimum = []
        for i in range(len(self.AVG_Curves_T)):
            self.ax_avg.plot(self.times, self.AVG_Curves_T[i], label=self.AVG_Labels[i])
            maximum.append(numpy.max(self.AVG_Curves_T[i]))
            minimum.append(numpy.min(self.AVG_Curves_T[i]))
               
        self.ax_avg.grid(True)
        #self.ax_avg.legend(loc='best')
        if self.resultType==1:
            self.ax_avg.set_ylabel('Temperature in C')
            self.ax_avg.axis([0,self.times[-1], int(numpy.min(minimum)-2), int(numpy.max(maximum)+2)])
        if self.resultType==-1:
            self.ax_avg.set_ylabel('Pressure in Pa')
            self.ax_avg.axis([0,self.times[-1], -100, 0])
        if self.resultType==3:
            self.ax_avg.set_ylabel('Velocity m/s')
            self.ax_avg.axis([0,self.times[-1], 0, int(numpy.max(maximum)+2)])
        self.ax_avg.set_xlabel('Iteration')
        self.ax_avg.set_facecolor('xkcd:charcoal')
        
        self.ax_avg.tick_params(axis='x', colors='white')
        self.ax_avg.tick_params(axis='y', colors='white')
        self.ax_avg.yaxis.label.set_color('white')
        self.ax_avg.xaxis.label.set_color('white')
        self.ax_avg.grid(True, linestyle=':')
        
              
        self.canvas = FigureCanvasTkAgg(self.fig_avg, self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=self.x0-100+40,y=self.y0+70)
        
        self.infolabel2 = TK.Label(self.root, text='CASE:    ' + self.path, bg=self.bg_color, fg=self.text_color)
        self.infolabel2.place(x=self.x0+100, y=self.y0+80)
        self.infolabel2.bind("<Button-1>", self.refresh_chart_patches)
        
        self.infolabel = TK.Label(self.root, text='FILE:       ' + self.filepath, bg=self.bg_color, fg=self.text_color)
        self.infolabel.place(x=self.x0+100, y=self.y0+100)
        self.infolabel.bind("<Button-1>", self.refresh_chart_patches)
                
#        '''Write Results'''
#        self.xslx = Workbook()
#        sheet1 = self.xslx.add_sheet('AVG Temperatures')
#        sheet2 = self.xslx.add_sheet('MAX Temperatures')
#        
        
        var1 = (TK.StringVar(self.root)).get()
        self.selecttime = ttk.Combobox(self.root, width=5, textvariable=var1)
        self.selecttime['values'] = self.times
        self.selecttime.place(x=self.x0+30, y=self.y0+70)
        self.selecttime.current(len(self.times)-1)
        TK.Label(self.root, text='Time:', bg=self.bg_color, fg=self.text_color).place(x=self.x0-2, y=self.y0+70)
        
#        which_time = self.times[self.selecttime.current()]
#        for p in range(len(self.times)):
#            if self.times[p]==which_time:
#                break
#        print (which_time)
#        for i in range(len(self.AVG_Curves_T)):
#            sheet1.write(i,0,str(self.AVG_Labels[i]))
#            sheet1.write(i,1,str(self.AVG_Curves_T[i][p]).replace('.',','))
#        for i in range(len(self.MAX_Curves_T)):
#            sheet2.write(i,0,str(self.MAX_Labels[i]))
#            sheet2.write(i,1,str(self.MAX_Curves_T[i][p]).replace('.',',')) 
        

if __name__ == "__main__":

    app = ARUPFOAM_Monitor()
    app.root.mainloop()