
import pandas as pd
import tkinter as tk


def addRecipe() :
    global df
    inputValue = maincookEntry.get()
    inputPrice = mainCookPriceEntry.get()
    df.loc[len(df)] = [inputValue] + [(value.get()) for pair in zip(subCookEntries, subCookQuaEntries) for value in pair] +[inputPrice] #pair가 양 값을 가지고 그 pair를 value로 풀어서 get
    df.loc[df['target']==inputValue, 'price'] = mainCookPriceEntry.get() # 같은 타겟이면 전부 똑같은 가격 설정
    print("저장 성공")
    print(df.tail())
    
def setPrice() :
    global df
    inputValue = maincookEntry.get()
    df.loc[df['target']==inputValue, 'price'] = mainCookPriceEntry.get() # 같은 타겟이면 전부 똑같은 가격 설정
    print("setPirce")
    print(df[df['target']==inputValue])
    

fileName = 'recipe.xlsx'

try :
    df = pd.read_excel(fileName,)
    
except FileNotFoundError : 
    df = pd.DataFrame(columns=['target','sub1','sub1_qua','sub2','sub2_qua','sub3','sub3_qua','sub4','sub4_qua','sub5','sub5_qua','price'], )
print(df)
    
window = tk.Tk()
window.title("Black Desert Calculation")
window.geometry("1080x480+200+200")
window.resizable(False, False)


            
        

top =tk.Label(window, text="황실 납품 이익 최대화 관련 프로그램입니다.\n insert 기능으로 상품의 조합식을 추가 할 수 있습니다. ", width=0, height=0,)
top.pack()

CookFrame = tk.Frame(window)
CookFrame.pack()

mainCookFrame = tk.Frame(CookFrame)
mainCookLabel = tk.Label(mainCookFrame, text="목표 요리")
maincookEntry = tk.Entry(mainCookFrame, width=20) 

mainCookPrice = tk.Frame(CookFrame)
mainCookPriceLabel = tk.Label(mainCookPrice, text = "Pirce")
mainCookPriceEntry = tk.Entry(mainCookPrice)

mainCookFrame.grid(row=0,column=0,padx=3, pady=10)
mainCookPrice.grid(row=0, column=1, padx=3, pady= 10)
mainCookLabel.pack(side=tk.TOP)
maincookEntry.pack(side=tk.BOTTOM )
mainCookPriceLabel.pack(side=tk.TOP)
mainCookPriceEntry.pack(side=tk.BOTTOM)

subCookFrames=[]    
subCookLabels=[]
subCookEntries=[]
subCooksizeLabels=[]
subCookQuaEntries=[]

for i in range(0,5):
    subCookFrame = tk.Frame(CookFrame)
    subCookLabel = tk.Label(subCookFrame, text="하위 요리{}".format(i+1))
    subCooksizeLabel = tk.Label(subCookFrame, text="수량")
    subCookEntry = tk.Entry(subCookFrame, width=15)
    subCookQuaEntry = tk.Entry(subCookFrame, width=5)
    if i<3 :
        subCookFrame.grid(row=1, column=i,padx=5,pady=20)
        subCookLabel.grid(row=0,column=0)
        subCooksizeLabel.grid(row=0,column=1)
        subCookEntry.grid(row=1,column=0 )
        subCookQuaEntry.grid(row=1,column=1)
    else :
        subCookFrame.grid(row=2, column=i-3,padx=5)
        subCookLabel.grid(row=0,column=0)
        subCooksizeLabel.grid(row=0,column=1)
        subCookEntry.grid(row=1,column=0 )
        subCookQuaEntry.grid(row=1,column=1)

    # 동적으로 생성된 변수에 대한 참조를 유지하기 위해 리스트에 추가
    subCookFrames.append(subCookFrame)
    subCookLabels.append(subCookLabel)
    subCookEntries.append(subCookEntry)
    subCooksizeLabels.append(subCooksizeLabel)
    subCookQuaEntries.append(subCookQuaEntry)

insertButton = tk.Button(window,text ="AddRecipe", command=addRecipe )
setPriceButton = tk.Button(window, text = "setPrice", command=setPrice)
insertButton.pack()
setPriceButton.pack()







window.mainloop()
df.to_excel(fileName,index=False ) #remove index  
    
    
    
    


