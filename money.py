# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Ui_money import Ui_Dialog
import source
import matplotlib.pyplot as plt
import os
import sys

class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_push_save_clicked(self):
        """
        
        存cost、date、item
        先把cost、date、item存成不同的字串
        然後再用(date_year, date_month, date_day, item, cost)來存
        
        最後輸出成檔案
        """
        cost=self.input_cost.text()
        item=self.input_item.text()
        temp=self.input_date.text()
        if len(temp)!=8:
            self.label_cost.setText('你超雷')
            return
        date_year=temp[0]+temp[1]+temp[2]+temp[3]
        date_month=temp[4]+temp[5]
        date_day=temp[6]+temp[7]
        file = open( 'money_save.txt', 'a',encoding='utf-16')
        file.write(date_year+'\t'+date_month+'\t'+date_day+'\t'+item+'\t'+cost+'\n')
        file.close()
        self.label_cost.setText('saved')
        self.input_cost.clear()
        item=self.input_item.clear()
        temp=self.input_date.clear()
        # TODO: not implemented yet
        
    
    @pyqtSlot()
    def on_push_plot_clicked(self):
        """
        Slot documentation goes here.
        畫圖
        """
        #讀檔
        file = open( 'money_save.txt', 'r',encoding='utf-16')
        data=[]
        line = file.readline()
        while line:
            data.append(source.data(line.split()[0],line.split()[1],line.split()[2],line.split()[3],line.split()[4]))
            line = file.readline()
        #關檔    
        file.close()
        x=[]
        x.append(data[0].date_day)
        y=[]
        y.append(0)
        count=0
        for input in data:
            if x[count]==input.date_day:
                y[count]+=int(input.cost)
            elif x[count]!=input.date_day:
                count=count+1
                x.append(input.date_day)
                y.append(int(input.cost))
        plt.ylim(0,300)
        plt.plot(x, y, '-o')
        plt.show()
        # TODO: not implemented yet
    @pyqtSlot()
    def on_plot_date_clicked(self):
        """
        Slot documentation goes here.
        畫圖_日期
        """
 #讀檔
        file = open( 'money_save.txt', 'r',encoding='utf-16')
        data=[]
        line = file.readline()
        while line:
            data.append(source.data(line.split()[0],line.split()[1],line.split()[2],line.split()[3],line.split()[4]))
            line = file.readline()
        #關檔    
        file.close()
        month_choose=self.input_month.text()
        x=[]
        y=[]
        for i in data:
            if i.date_month==month_choose:
                x.append(i.date_day)
                break
        y.append(0)
        count=0
        
        for input in data:
            if input.date_month==month_choose:
                if x[count]==input.date_day:
                    y[count]+=int(input.cost)
                elif x[count]!=input.date_day:
                    count=count+1
                    x.append(input.date_day)
                    y.append(int(input.cost))
        plt.plot(x,y, '-o')
        plt.show()
    @pyqtSlot()
    def on_push_origin_clicked(self):
        """
        Slot documentation goes here.
        """
        os.system('D:\E3\Code測試區\pythonTest\money\money_save.txt');
        
    @pyqtSlot()
    def on_push_average_clicked(self):
        """
        Slot documentation goes here.
        """
#讀檔
        file = open( 'money_save.txt', 'r',encoding='utf-16')
        data=[]
        line = file.readline()
        while line:
            data.append(source.data(line.split()[0],line.split()[1],line.split()[2],line.split()[3],line.split()[4]))
            line = file.readline()
        #關檔    
        file.close()
        x=[]
        x.append(data[0].date_day)
        y=[]
        y.append(0)
        count=0
        temp=0
        for input in data:
            if x[count]==input.date_day:
                y[count]+=int(input.cost)
            elif x[count]!=input.date_day:
                count=count+1
                x.append(input.date_day)
                y.append(int(input.cost))            
        for i in y:
            temp=temp+i
        temp=temp/len(y)
        self.label_average.setText('平均消費='+str(int(temp))+'元')

if __name__ == "__main__":
   if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
    
