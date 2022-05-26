import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from django.utils.translation import gettext

class GRAPH:
    def graph_pie(data_names,data_values,data_colors,text_center,show_legend=True):
      
        dpi = 80
        fig = plt.figure(dpi = dpi, figsize = (370 / dpi, 370 / dpi) )
    
        plt.title('')
       
        plt.pie(data_values, radius = 1.2,colors =data_colors,wedgeprops = {'width': 0.3, 'linewidth': 1, 'edgecolor':'w'})
        
        if show_legend==True:
            plt.legend(labels = data_names,loc="lower left",fontsize=10,bbox_to_anchor=(-0.3,-0.15),borderaxespad=0.2,bbox_transform=plt.gcf().transFigure  )
        elif text_center!="":
           plt.text(0.01, 0.01, text_center, size=12, rotation=0,
         ha="center", va="center",
         bbox=dict(boxstyle="round", color='white')
         )
    
         
        imgdatapie = StringIO()
        fig.savefig(imgdatapie, format='svg')
    
        
        #imgdatapie.seek(0)
    
        data = imgdatapie.getvalue()
        return data
    
    def graph_pie_with_center(data_names,data_values,legend_bottom = False):
      
        dpi = 80
        fig = plt.figure(dpi = dpi, figsize = (260 / dpi, 230 / dpi) )

    
        plt.title('')
       
    
        plt.pie(
            #data_values, autopct=lambda pct: format_value(pct ,data_values), radius = 1.1, wedgeprops = {'width': 0.3, 'linewidth': 1, 'edgecolor':'w'})
            data_values,  radius = 1.2, wedgeprops = {'width': 0.3, 'linewidth': 1, 'edgecolor':'w'})
       
        if legend_bottom ==True:            
            leg=plt.legend(labels = data_names,loc="center",fontsize=10,bbox_to_anchor=(0.5,0.5))
        else:     
            leg=plt.legend(labels = data_names,loc="center",fontsize=10,bbox_to_anchor=(0.5,0.5))
    

        #leg._legend_box.align = "right"

        
        imgdatapie = StringIO()
        fig.savefig(imgdatapie, format='svg')
    
        #imgdatapie.seek(0)
    
        data = imgdatapie.getvalue()
        return data
     
    
    def graph_bar(data_names,data_values,mini=True,title=''):
      
        dpi = 80
        if mini==True:
            fig = plt.figure(dpi = dpi, figsize = (240 / dpi, 220 / dpi))
            
        else:
            fig = plt.figure(dpi = dpi, figsize = (320 / dpi, 300 / dpi))
        mpl.rcParams.update({'font.size': 9})
    
        plt.title(title)  
        
        xs = range(len(data_names))
        #xy = range(len(data_values))
        
        #plt.bar(xs, data_values, color=['blue', 'red', 'green', 'Orange', 'brown', 'blueviolet','navy'])    
        plt.bar(xs, data_values, color=['teal'])    
        
        number = 0
        for val in data_values:
           plt.text(number,val+40,val,fontsize=9,horizontalalignment="center")
           number+=1
    
        plt.xticks(xs, data_names)    
        #plt.yticks(xy, data_values)
        
        ax = fig.gca()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(True)
        ax.spines["bottom"].set_visible(True)
        
        plt.subplots_adjust(left=0, bottom=0.2, right=1, top=0.93)
        
        if mini!=True:
            ax.tick_params( labelrotation = -45)    #  Поворот подписей
        
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
    
        #imgdata.seek(0)
    
        data = imgdata.getvalue()
        return data
    
    def graph_bar_double(data_names,data_values,data_values2,title='',title2=''):
            #g_title, y_title, x_labels, data_series, file_name, cat_title, x_title):
        barWidth = 0.25
        
        #fig = plt.subplots(figsize =(12, 8))
    
        dpi = 80
        fig = plt.figure(dpi = dpi, figsize = (300 / dpi, 300 / dpi))
        mpl.rcParams.update({'font.size': 9})

         
        # Set position of bar on X axis
        br1 = np.arange(len(data_values))
        br2 = [x + barWidth for x in br1]
         
        # Make the plot
        plt.bar(br1, data_values, color ='r', width = barWidth,
                edgecolor ='grey', label = gettext('cost'))
        plt.bar(br2, data_values2, color ='g', width = barWidth,
                edgecolor ='grey', label = gettext('profit'))
    
         
        # Adding Xticks
        #plt.xlabel('Branch', fontweight ='bold', fontsize = 15)
        #plt.ylabel('Students passed', fontweight ='bold', fontsize = 15)
        plt.xticks([r + barWidth for r in range(len(data_values))],data_names)
         
        plt.legend(loc="upper left",fontsize=10,bbox_to_anchor=(0,1.1))
        
        ax = fig.gca()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(True)
        ax.spines["bottom"].set_visible(True)
        
        ax.grid(axis = 'y')#Горизонтальні лінії
        
        ax.tick_params(axis = 'x', labelrotation = -45)    #  Поворот підписів
        
        plt.subplots_adjust(left=0.15, bottom=0.2, right=1, top=0.93)#Розміри графа
        
        
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
    
        #imgdata.seek(0)
    
        data = imgdata.getvalue()
        return data    
    
def format_value(pct, allvals,withpersent = False):
    absolute = int(pct/100.*np.sum(allvals))
    if withpersent:
        return "{:.1f}%\n({:d})".format(pct, absolute)    
    else:
        return "{:d}".format( absolute)   