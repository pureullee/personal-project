
import pandas as pd
import tkinter as tk
import numpy as np
proficiency = 3

def addRecipe() :
    
    inputValue = maincookEntry.get()
    inputPrice = mainCookPriceEntry.get()
    last=len[df] 
    df.loc[last] = [inputValue] + [(value.get()) for pair in zip(subCookEntries, subCookQuaEntries) for value in pair] +[inputPrice] #pair가 양 값을 가지고 그 pair를 value로 풀어서 get
    df.loc[df['target']==inputValue, 'price'] = mainCookPriceEntry.get() # 같은 타겟이면 전부 똑같은 가격 설정
    df.loc[last]['iscook'] = 1 if df.loc[last]['sub1'] != None else 0 #1은 요리, 0은 원재료
    print("저장 성공")
    print(df.tail())
    
def setPrice() :
    
    inputValue = maincookEntry.get()
    df.loc[df['target']==inputValue, 'price'] = mainCookPriceEntry.get() # 같은 타겟이면 전부 똑같은 가격 설정
    print("setPirce")
    print(df[df['target']==inputValue])
    
def tracePrice(target) :
    
    # 매개변수 target의 값이 target 시리즈에 있는 행에 대해서 iscook 값이 0인, 즉 원재료인경우라면 그 원재료 가격의 평균을 리턴함
    if df.loc[df['target'] == target,'iscook'].iloc[0] == 0 :
        return df.loc[df['target']== target,'price'].mean()
    
    # iscook 값이 1인경우엔, sub1 부터 sub5 까지 순환하며 다시 재귀적으로 함수를 콜함
    else :
        #하위 요리명만을 가진 데이터 프레임을 생성함
        newDf = df.loc[df['target'] == target, ['sub1','sub2','sub3','sub4','sub5']]
        
        #newDf의 길이만큼 각 행에 대해 sub1~sub5까지의 하위 재료를 각각 재귀함수에 넣음
        
        for i in range(len(newDf)) :
            cost = 0
            for v in newDf.iloc[i] :
                if v is not np.nan  :
                    cost += tracePrice(v) 
            cost //= proficiency
            
            df.loc[df['target'] == target, 'cost'] = cost
            print(df.loc[df['target'] == target, 'cost'])
                    
            
    

fileName = 'recipe.xlsx' 

try :
    df = pd.read_excel(fileName,)
    
except FileNotFoundError : 
    df = pd.DataFrame(columns=['target','sub1','sub1_qua','sub2','sub2_qua','sub3','sub3_qua','sub4','sub4_qua','sub5','sub5_qua','price', 'cost' 'iscook'], )
print(df)

tracePrice('채소 볶음')
    
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
    
    
    
    


