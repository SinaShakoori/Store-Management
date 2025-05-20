import sqlite3
from tkinter import *
from tkinter import ttk,messagebox



def mydb():
    global cnn , curs
    f1=open('mydb.db','a')
    cnn=sqlite3.connect('mydb.db')
    curs=cnn.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS market(id integer primary key autoincrement, name text , priceb integer , prices integer , qnt integer)""")






def op():
    global jadval,namee,pricebb,pricess,qntt,win
    mydb()
    win=Tk()
    win.geometry('700x380')
    win.title('مدیریت فروشگاه')
    frm0=Frame(win,height=150, bg='lightblue').pack(side=TOP,fill=X)
    frm1=Frame(win).pack(side=LEFT,fill=Y)
    #############################

    lbname=Label(frm0,text='نام کالا').place(x=20,y=20)
    lbpriceb=Label(frm0,text='قیمت خرید').place(x=350,y=20)
    lbprices=Label(frm0,text='قیمت فروش').place(x=20,y=80)
    lbqnt=Label(frm0,text='تعداد').place(x=350,y=80)
    namee=StringVar()
    pricebb=StringVar()
    pricess=StringVar()
    qntt=StringVar()
    Entry(frm0,textvariable=namee).place(x=100,y=20)
    Entry(frm0,textvariable=pricebb).place(x=430,y=20)
    Entry(frm0,textvariable=pricess).place(x=100,y=80)
    Entry(frm0,textvariable=qntt).place(x=430,y=80)
    btnadd=Button(frm0,text='اضافه کردن', command=add).place(x=20,y=120)
    btnsearch=Button(frm0,text='جستجو کردن', command=search).place(x=150,y=120)
    btnedit=Button(frm0,text='ویرایش کردن', command=edit).place(x=280,y=120)
    btndelt=Button(frm0,text='حذف کردن', command=delt).place(x=410,y=120)
    btnclose=Button(frm0,text='بستن', command=close).place(x=540,y=120)

    ##############################
    jadval=ttk.Treeview(frm1,columns=('id','name','priceb','prices','qnt'),show='headings')
    jadval.heading('id',text='کد')
    jadval.heading('name',text='نام کالا')
    jadval.heading('priceb',text='قیمت خرید')
    jadval.heading('prices',text='قیمت فروش')
    jadval.heading('qnt',text='تعداد')
    jadval.column('id',width=50)
    jadval.column('name',width=120)
    jadval.column('priceb',width=100)
    jadval.column('prices',width=100)
    jadval.column('qnt',width=120)
    jadval.bind('<<TreeviewSelect>>',select)
    jadval.pack(side=TOP,fill=X)
    show()
    ###############################
    mainloop()




def add():
    mydb()
    n=namee.get()
    p=pricebb.get()
    ps=pricess.get()
    q=qntt.get()
    if n=='' or p=='' or ps=='' or q=='':
        messagebox.showinfo('اخطار','لطفا فیلد ها را کامل پر کنید')
    
    else:
        curs.execute('INSERT INTO market(name,priceb,prices,qnt)values(?,?,?,?)',(n,p,ps,q))
        cnn.commit()
        show()
        messagebox.showinfo('اطلاعیه','رکورد ذخیره شد')

def show():
    mydb()
    jadval.delete(*jadval.get_children())
    curs.execute('select * from market')
    myrecord=curs.fetchall()
    for i in myrecord:
        jadval.insert('','end',values=i)


def search():
    mydb()
    jadval.delete(*jadval.get_children())
    n=namee.get()
    curs.execute(f'SELECT * FROM market where name like "%{n}%"')
    myrecords=curs.fetchall()
    for i in myrecords:
        jadval.insert('','end',values=i)


def close():
    win.destroy()


def select(event):
    global id_kalaa
    selected_item = jadval.focus()  # آیتم انتخاب‌شده
    if not selected_item:
        return  # اگر هیچ آیتمی انتخاب نشده، تابع را ترک کنید
    
    
    satr=jadval.focus()
    satrdata=jadval.item(satr)
    satrdataa=satrdata['values']
    if not satrdataa:
        return  # اگر آیتم داده‌ای ندارد، تابع را ترک کنید
    id_kalaa=satrdataa[0]
    namee.set(satrdataa[1])
    pricebb.set(satrdataa[2])
    pricess.set(satrdataa[3])
    qntt.set(satrdataa[4])


def edit():
    mydb()
    curs.execute(f'UPDATE market set name=?,priceb=?,prices=?,qnt=? \
                 where id=?',(namee.get(),pricebb.get(),pricess.get(),qntt.get(),id_kalaa))
    cnn.commit()
    show()
    messagebox.showinfo('اطلاعیه','رکورد ذخیره شد')


def delt():
    mydb()
    selected_items = jadval.selection()  # دریافت آیتم‌های انتخاب‌شده
    if not selected_items:
        messagebox.showinfo('اخطار', 'لطفا یک رکورد انتخاب کنید')
        return  # اگر هیچ آیتمی انتخاب نشده، تابع را ترک کنید

    for selected_item in selected_items:
        item_data = jadval.item(selected_item)['values']  # دریافت داده‌های آیتم
        if not item_data:
            messagebox.showinfo('اخطار', 'آیتم انتخابی معتبر نیست')
            return
        
        id_kala = item_data[0]  # دریافت شناسه کالا
        curs.execute('DELETE FROM market WHERE id = ?', (id_kala,))
        cnn.commit()
        jadval.delete(selected_item)  # حذف آیتم از جدول

    show()
    messagebox.showinfo('اطلاعیه', 'رکورد(ها) با موفقیت حذف شد')



op()
