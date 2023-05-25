
import pandas as pd
import tkinter as tk
import numpy as np
proficiency = 3

def addRecipe() :
    
    inputValue = maincookEntry.get()
    inputPrice = mainCookPriceEntry.get()
    last=len(df)
    
    df.loc[last,'target'] = inputValue
    #pair가 양 값을 가지고 그 pair를 value로 풀어서 get
    subCooks = ['sub1', 'sub2', 'sub3', 'sub4', 'sub5']
    subCooksQua = ['sub1_qua', 'sub2_qua', 'sub3_qua', 'sub4_qua', 'sub5_qua']
    df.loc[last, subCooks] = [value.get() for value in subCookEntries]
    df.loc[last, subCooksQua] = [int(value.get()) if value.get() != '' else '' for value in subCookQuaEntries]
    #df.loc[last,'sub1':'sub5_qua'] =[(value.get()) for pair in zip(subCookEntries, subCookQuaEntries) for value in pair]
    df.loc[last,'price']= inputPrice 
    
    # 같은 타겟이면 전부 똑같은 가격 설정
    df.loc[df['target']==inputValue, 'price'] = int(inputPrice)
    
    #1은 요리, 0은 원재료
    df.loc[last,'iscook'] = 0 if df.loc[last]['sub1'] == '' else 1 
    
    setCost()   
    print("저장 성공")
    print(df.tail())
    
def setPrice() :
    
    inputValue = maincookEntry.get()
    df.loc[df['target']==inputValue, 'price'] = mainCookPriceEntry.get() # 같은 타겟이면 전부 똑같은 가격 설정
    print("setPirce")
    print(df[df['target']==inputValue])
    setCost()
    

def setCost() : 
    df['cost'] = df['target'].apply(traceCost)
        
    
    
def traceCost(target) :  # target 요리에 대한 하위 요리의 가격 혹은 코스트 값을 기반으로 target 요리의 코스트를 추정하는 함수
    #target 요리가 있는 행을 추출 
    targetRow = df.loc[df['target']==target]
    
    cost = 0 
    #아직 등록되지 않은 경우라면
    if targetRow.empty: return np.nan
    
    # 가장 하위 재료인 경우는 가격을 바로 리턴 시킴
    elif targetRow['iscook'].iloc[0] == 0 :
        return targetRow['price'].iloc[0]
    
    # 요리인데, cost의 값이 이미 존재하는 경우는 그냥 그 요리의 코스트 값을 리턴 
    elif (targetRow['iscook'].iloc[0] == 1) and not pd.isna(targetRow['cost'].iloc[0]) :
        return targetRow['cost'].iloc[0]
    
    subCooks = ['sub1', 'sub2', 'sub3', 'sub4', 'sub5']
    subCooksQua = ['sub1_qua', 'sub2_qua', 'sub3_qua', 'sub4_qua', 'sub5_qua']

    #하위 요리, 수량을 각각 선택후
    for subCook, subCookQua in zip(subCooks, subCooksQua):
        subCookValue = targetRow[subCook].iloc[0]
        subCookQuaValue = targetRow[subCookQua].iloc[0]
        
        if pd.notna(subCookValue):
            x = traceCost(subCookValue)
            if x is np.nan:
                return np.nan
            else:
                cost += x * subCookQuaValue
               
    return cost//proficiency       
    # targetRow의 cost 컬럼에 요소의 값에 관계없이 하위 재료부터 새롭게 
    # 위의 경우가 아니라면 setCost를 수행
    
    
    
    
     
    

        
            
    
        
    
    
    
    
    
    pass
    

                    
            
    

fileName = 'recipe.xlsx' 

try :
    df = pd.read_excel(fileName,)
    
except FileNotFoundError : 
    df = pd.DataFrame(columns=['target','sub1','sub1_qua','sub2','sub2_qua','sub3','sub3_qua','sub4','sub4_qua','sub5','sub5_qua','price', 'cost' 'iscook'], )
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
    
    
    
    


