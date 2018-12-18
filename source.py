
class data ():   
    temp=''
    date_year=''
    date_month=''
    date_day=''
    item=''
    cost=  ''  
    def __init__(self, date_year, date_month, date_day, item, cost):
        self.temp=''
        self.date_year=date_year
        self.date_month=date_month
        self.date_day=date_day
        self.item=item
        self.cost=cost
    def output(self):
        self.temp=self.date_year+' '+self.date_month+' '+self.date_day+' '+self.item+' '+self.cost+'\n'
        return self.temp
