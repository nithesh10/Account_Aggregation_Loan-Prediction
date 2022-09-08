
from distutils.command.config import config
import pandas as pd
import config
def get_cibil():
    df1= pd.read_excel('payment_history.xlsx')
    df2=pd.read_excel('enquiry.xlsx')
    df3=pd.read_excel('parameter_additional.xlsx')
    df4=pd.read_excel('status.xlsx')
    UID=int(config.mobile_num)
    df1=pd.DataFrame(df1)
    cibil=0
    df1=df1[df1.uid==UID]



    if df1.iloc[0]['std_count']>0:
        cibil+=df1.iloc[0]['std_count']/12*3/4*315
    if df1.iloc[0]['perfect_repay_count']>0:
        cibil+=df1.iloc[0]['perfect_repay_count']/12*4/4*315
    if df1.iloc[0]['lss_count']>0:
        cibil+=0
    if df1.iloc[0]['sub_count']>0:
        cibil+=df1.iloc[0]['sub_count']/12*2/4*315
    if df1.iloc[0]['sma_count']>=0:
        cibil+=df1.iloc[0]['sma_count']/12*1/4*315




    df3=df3[df3.uid==UID]
    credit_exposure=180-df3.iloc[0]['money_request']/df3.iloc[0]['money_request']*180
    cibil+=credit_exposure



    df4=df4[df4.uid==UID]
    if df4.iloc[0]['amount_overdue']>0:
        credit_type_and_duration=0
    else:
        credit_type_and_duration=25/100*900
        cibil+=credit_type_and_duration
    df2=df2[df2.uid==UID]


    if cibil<=500:
      out=("<br>    Customer behaviour: Poor "    +
           "    Cibil score:"    +str(cibil)+ "    The customer is not eligible</br>")
    elif (cibil>500) & (cibil<=650): 
      out=("<br>    Customer behaviour: Average "    +
           "    Cibil score:"    +str(cibil)+ "    The customer is eligible</br>")
    if (cibil>500) & (cibil<=750):
        out+=("<br>    Customer behaviour: Good "    +
           "    Cibil score:"    +str(cibil)+ "    The customer is eligible </br>")
        out+=("<br>    Looking into additional details... </br>")
        out+=("<br>    Income of the applicant:"    +str(df3.iloc[0]['income'])+str("</br>"))
        out+=("<br>    Total EMI being paid:"    +str(df3.iloc[0]['money_request']+str("</br>")))
        out+=("<br>    EMI to income ratio:"    +str(df3.iloc[0]['money_request']/df3.iloc[0]['income'])+str("</br>"))
        out+=("<br>    Total borrowing capacity:"    +str(50/100*df3.iloc[0]['income'])+str("</br>"))
        out+=("<br>    Total increment EMI applicant can afford:"    +str((50/100*df3.iloc[0]['income'])-(df3.iloc[0]['money_request']))+str("</br>"))
        out+=("<br>    Is customer eligible by every norms?:"    +str(df3.iloc[0]['approved'])+str("</br>"))
    elif(cibil>750) & (cibil<=900):
        out=("<br>    Customer behaviour: Excellent "    ,
           "    Cibil score:"    ,cibil, "    The customer is eligible </br>")
        out+=("<br>    Looking into additional details... </br>")
        out+=("<br>    Income of the applicant:"    +str(df3.iloc[0]['income'])+str("</br>"))
        out+=("<br>    Total EMI being paid:"    +str(df3.iloc[0]['money_request']+str("</br>")))
        out+=("<br>    EMI to income ratio:"    +str(df3.iloc[0]['money_request']/df3.iloc[0]['income'])+str("</br>"))
        out+=("<br>    Total borrowing capacity:"    +str(50/100*df3.iloc[0]['income'])+str("</br>"))
        out+=("<br>    Total increment EMI applicant can afford:"    +str((50/100*df3.iloc[0]['income'])-(df3.iloc[0]['money_request']))+str("</br>"))
        out+=("<br>    Is customer eligible by every norms?:"    +str(df3.iloc[0]['approved'])+str("</br>"))

    return out


print(get_cibil())



