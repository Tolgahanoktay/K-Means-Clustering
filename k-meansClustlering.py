from PyQt5.QtWidgets import *
import sys
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Window(QMainWindow):
    
    def __init__(self, *args, **kwargs):
       super(Window, self).__init__(*args, **kwargs)
       
       self.left = 50
       self.top = 50
       self.width = 1080
       self.height = 640
       self.title = "Clustering"
       
       self.setWindowTitle(self.title)
       self.setGeometry(self.left, self.top ,self.width, self.height )
       
       self.k = 1
       self.save_txt = ""
       
       
       self.widgets()
       self.tabwidgets()
       self.layouts()
       self.prepareData()
       self.show()
       
       
    def tabwidgets(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1,"Main")
       
       
    def widgets(self):
       
       #plot
       self.p = PlotCanvas(self,width = 5,height = 5)
       
       self.k_number_text = QLabel("Choose K: ")
       
       self.k_number = QSpinBox(self)
       self.k_number.setMinimum(1)
       self.k_number.setMaximum(9)
       self.k_number.setSingleStep(1)
       self.k_number.valueChanged.connect(self.k_numberFunction)
       
       self.text_save = QRadioButton("Save text",self)
       self.plot_save = QRadioButton("Save plot",self)
       self.text_plot_save = QRadioButton("Save text and Plot",self)
       self.text_plot_save.setChecked(True)
       
       self.cluster = QPushButton("Cluster",self)
       self.cluster.clicked.connect(self.clusterFunction)
       
       self.result_list = QListWidget(self)
       
       
    def prepareData(self):
        self.p.clear()
        
        data = pd.read_csv("data.csv")
        
        self.f1 = data.iloc[:,3].values
        self.f2 = data.iloc[:,4].values
        
        X = np.array(list(zip(self.f1,self.f2)))
        
        # we created centroid this part 
        self.C_x = np.random.randint(0,np.max(X) - 20,size = self.k)
        self.C_y = np.random.randint(0,np.max(X) - 20,size = self.k)
        
        self.p.plot(self.f1,self.f2,"black",7)
        self.p.plot(self.C_x,self.C_y,"red",200,"*")
        
        
        
    def k_numberFunction(self):
        
        self.k = self.k_number.value()
        self.prepareData()
        
        
    def dist(self,a,b):
        return np.linalg.norm(a - b, axis = 1)
        
        
    def kMenasClustering(self,f1,f2,C_x,C_y,k):
        
        X = np.array(list(zip(f1,f2)))
        
        C = np.array(list(zip(C_x,C_y)))
        
        clusters = np.zeros(len(X))
        
        for z in range(10):
            
            for i in range(len(X)):
                
                distances = self.dist(X[i], C)
                cluster = np.argmin(distances)
                clusters[i] = cluster
                
            for i in range(k):
                
                points = [ X[j] for j in range(len(X)) if clusters[j] == i]
                C[i] = np.mean(points, axis = 0)
        colors = ['black', 'red', 'cyan','magenta', 'blue', 'yellow',"darkgreen","silver","indigo","maroon"]
        
        for i in range(k):
            
            points = np.array([ X[j] for j in range(len(X)) if clusters[j] == i])
            self.p.plot(points[:,0],points[:,1],colors[i],7)
            self.p.plot(C[:,0],C[:,1],"red",200,"*")
            
            result_txt = "Cluster"+str(i+1)+": "+str(len(points)) + " ("+colors[i]+")"
            self.result_list.addItems([result_txt])
        
            self.save_txt = self.save_txt + result_txt + " -- "
        
        
    def clusterFunction(self):
        self.result_list.clear()
        self.p.clear()
        
        self.kMenasClustering(self.f1,self.f2,self.C_x,self.C_y,self.k)
        
        # radio button
        if self.text_save.isChecked():
            path_name = "cluster_result.txt"
            text_file = open(path_name,"w")
            text_file.write(self.save_txt)
            text_file.close()
        if self.plot_save.isChecked():
            self.p.fig.savefig("cluster_figure.jpg")
            
        if self.text_plot_save.isChecked():
            path_name = "cluster_result.txt"
            text_file = open(path_name,"w")
            text_file.write(self.save_txt)
            text_file.close()  
            
            self.p.fig.savefig("cluster_figure.jpg")
    
    def layouts(self):
        #layout
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.middleLayout = QFormLayout()
        self.rightLayout = QFormLayout()
        
        #left
        self.leftLayoutGroupBox =QGroupBox("Plot")
        self.leftLayout.addRow(self.p)
        self.leftLayoutGroupBox.setLayout(self.leftLayout)
        
        #middle
        self.middleLayoutGroupBox =QGroupBox("Clustering")
        self.middleLayout.addRow(self.k_number_text)
        self.middleLayout.addRow(self.k_number)
        self.middleLayout.addRow(self.text_save)
        self.middleLayout.addRow(self.plot_save)
        self.middleLayout.addRow(self.text_plot_save)
        self.middleLayout.addRow(self.cluster)
        self.middleLayoutGroupBox.setLayout(self.middleLayout)
        
        #right
        self.rightLayoutGroupBox = QGroupBox("Result")
        self.rightLayout.addRow(self.result_list)
        self.rightLayoutGroupBox.setLayout(self.rightLayout)
        
        #main 
        self.mainLayout.addWidget(self.leftLayoutGroupBox,50)
        self.mainLayout.addWidget(self.middleLayoutGroupBox,25)
        self.mainLayout.addWidget(self.rightLayoutGroupBox,25)
        self.tab1.setLayout(self.mainLayout)
        

class PlotCanvas(FigureCanvas):
    def __init__(self,parent = None,width = 5,height = 5,dpi = 100):
        self.fig = Figure(figsize=(width,height),dpi = dpi)
        
        FigureCanvas.__init__(self,self.fig)
        
    def plot(self,x,y,c,s,m = "."):
        self.ax = self.figure.add_subplot(111)
        self.ax.scatter(x,y,c = c,s= s,marker = m)
        self.ax.set_title("K-Means Clustering")
        self.ax.set_xlabel("Income")
        self.ax.set_ylabel("Number of Transaction")
        self.draw()
        
    def clear(self):
        self.fig.clf()
        
        
app = QApplication(sys.argv)

window = Window()
window.show()

app.exec_()

