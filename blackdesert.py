
import pandas as pd
import tkinter as tk
import numpy as np
proficiency = 3
no_data = set([])
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
    if targetRow.empty:
        no_data.add(target)     
        return np.nan
    
    # 가장 하위 재료인 경우는 가격을 바로 리턴 시킴
    elif targetRow['iscook'].iloc[0] == 0 :
        return targetRow['price'].iloc[0]
    
    # 요리인데, cost의 값이 이미 존재하는 경우는 그냥 그 요리의 코스트 값을 리턴 
    elif (targetRow['iscook'].iloc[0] == 1) and not pd.isna(targetRow['cost'].iloc[0]) :
        return targetRow['cost'].iloc[0]
    
    subCooks = ['sub1', 'sub2', 'sub3', 'sub4', 'sub5']
    subCooksQua = ['sub1_qua', 'sub2_qua', 'sub3_qua', 'sub4_qua', 'sub5_qua']

    #하위 요리, 수량을 각각 선택후
    checkData = True 
    for subCook, subCookQua in zip(subCooks, subCooksQua):
        subCookValue = targetRow[subCook].iloc[0]
        subCookQuaValue = targetRow[subCookQua].iloc[0]
        
        #subCookValue의 값이 비어 있는게 아니라면    
        if pd.notna(subCookValue):
            x = traceCost(subCookValue)
            if x is not np.nan:
                cost += x * subCookQuaValue
            else :
                checkData = False
            
    if checkData == False : return np.nan 
            
                
               
    return cost//proficiency       
    # targetRow의 cost 컬럼에 요소의 값에 관계없이 하위 재료부터 새롭게 
    # 위의 경우가 아니라면 setCost를 수행

def clear() :
    #entry 값 초기화
    maincookEntry.delete(0, tk.END) 
    mainCookPriceEntry.delete(0, tk.END) 
    for e in subCookEntries :
        e.delete(0, tk.END) 
    for e in subCookQuaEntries:
        e.delete(0, tk.END) 
    
    #focus 이동
    maincookEntry.focus_set()
    
def search() :
    searchValue = maincookEntry.get()
    searchWindow = tk.Toplevel(window)
    searchWindow.title("검색 결과")
    
    searchDF = df.loc[df['target'] == searchValue]
    
    #label을 맨위에 만듬
    s_mainLabel = tk.Label(searchWindow, text=searchValue)
    s_mainLabel.grid(row=0, column=0, padx=3, pady=10)
    
    for i in range(len(searchDF)) :
        #searchDF의 길이는 곧, 검색된 요리 레시피의 개수. row 1에 최초할당후 레시피는2,3에 다음 row는 4
        s_numberLabel = tk.Label(searchWindow, text=f"요리#{i+1}")
        s_numberLabel.grid(row=1+i*3, column=0, padx=3, pady=10)
        #count가 3이 되면 밑 행 쓸 예정
        count = 0
        c_count = 0
        
        subCooks = ['sub1', 'sub2', 'sub3', 'sub4', 'sub5']
        subCooksQua = ['sub1_qua', 'sub2_qua', 'sub3_qua', 'sub4_qua', 'sub5_qua']
        
        for v, n in zip(searchDF.iloc[i][subCooks], searchDF.iloc[i][subCooksQua]):
            if pd.notna(v) :
                
                if count<3 :
                    s_subLabel = tk.Label(searchWindow, text=f"{v}*{n}")
                    s_subLabel.grid(row=2+i*3,column=c_count, padx=3, pady=10)
                    
                else :
                    s_subLabel = tk.Label(searchWindow, text=f"{v}*{n}")
                    s_subLabel.grid(row=3+i*3, column=c_count, padx=3, pady=10)
                    
                count +=1
                c_count+=1
                if c_count == 3 : c_count=0

fileName = 'recipe.xlsx' 

try :
    df = pd.read_excel(fileName,)
    
except FileNotFoundError : 
    df = pd.DataFrame(columns=['target','sub1','sub1_qua','sub2','sub2_qua','sub3','sub3_qua','sub4','sub4_qua','sub5','sub5_qua','price', 'cost' 'iscook'], )
print(df)


setCost()  
window = tk.Tk()
window.title("Black Desert Calculation")
window.geometry("720x480+200+200")
window.resizable(False, False)

top =tk.Label(window, text="황실 납품 이익 최대화 관련 프로그램입니다.\n insert 기능으로 상품의 조합식을 추가 할 수 있습니다. ", width=0, height=0,)
top.pack()

CookFrame = tk.Frame(window, borderwidth=3, relief="solid", pady=10)
CookFrame.pack()

mainCookFrame = tk.Frame(CookFrame)
mainCookLabel = tk.Label(mainCookFrame, text="목표 요리")
maincookEntry = tk.Entry(mainCookFrame, width=20) 

mainCookPrice = tk.Frame(CookFrame)
mainCookPriceLabel = tk.Label(mainCookPrice, text = "Pirce")
mainCookPriceEntry = tk.Entry(mainCookPrice)

mainCookFrame.grid(row=0,column=0,padx=3, )
mainCookPrice.grid(row=0, column=1, padx=3, )
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
    

#Button Frame 부분
ButtonFrame = tk.Frame(window)
insertButton = tk.Button(ButtonFrame,text ="AddRecipe", command=addRecipe )
setPriceButton = tk.Button(ButtonFrame, text = "setPrice", command=setPrice)
clearButton =  tk.Button(ButtonFrame, text="clear", command=clear)
searchButton = tk.Button(ButtonFrame, text="search", command=search )

ButtonFrame.pack()
insertButton.grid(row=0, column=0,padx=3)
setPriceButton.grid(row=0,column=1,padx=3)
clearButton.grid(row=0, column=2,padx=3)
searchButton.grid(row=0,column=3,padx=3)

#데이터가 아직 등록되지 않은 부분에 대한 프레임    
no_dataFrame = tk.Frame(window)
no_dataLabel = tk.Label(no_dataFrame, text = "아직 등록 되지 않은 레시피")
no_datalistLabel = tk.Label(no_dataFrame,text=", ".join(list(no_data)))
no_dataFrame.pack(pady=10,)
no_dataLabel.grid(row=0, column=0)
no_datalistLabel.grid(row=1,column=0)

window.mainloop()
df.to_excel(fileName,index=False ) #remove index  
    
    
    
    


