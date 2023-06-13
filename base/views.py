from django.shortcuts import render
from .forms import Calculator, Mortgage
from .tax_rates import state_income_tax, federal_income_tax, STATES
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

def calculator(request):
    tax_bracket=0
    form=Calculator()
    context={
        'states':STATES,
        'form':form
    }
    if request.method == 'POST':
        form=Calculator(request.POST)
        if form.is_valid():
            state=form.cleaned_data['state']
            annual_income=form.cleaned_data['annual_income']
            context['state']=state
            context['annual_income']=annual_income
            annual_income_clean = locale.currency(annual_income, grouping=True)
            context['annual_income_clean']=annual_income_clean


            state_tax_owed=0
            threshold_list=[]
            rate_list=[]
            fica=annual_income*0.0765
            state_rate=0
            graduated_tax=0
            threshold_bracket=0

            for threshold, rate in state_income_tax[state].items():
                if threshold<=annual_income:
                    threshold_list.append(threshold)
                    rate_list.append(rate)
                    state_bracket=rate
  
            if len(threshold_list) > 1:
                tally=0
                graduated_tax=0
                for threashold in range(len(threshold_list)):
                    if len(threshold_list)-1 > threashold:
                        graduated_tax+=(threshold_list[tally+1]-threshold_list[tally])*(rate_list[tally]/100)
                        tally+=1
                        threshold_bracket=threshold_list[tally]

            state_tax_owed=graduated_tax+(annual_income-threshold_bracket)*state_bracket/100
            state_tax_owed+=(annual_income-state_bracket)*(state_rate/100)

            federal_rates=list(federal_income_tax)
            for bracket in federal_rates:
                if annual_income>bracket:
                    tax_bracket=bracket
                elif annual_income<bracket:
                    break

            federal_rate=federal_income_tax.get(tax_bracket)

            if federal_rate:
                for fed_deduction, rate in federal_rate.items():
                    federal_tax_owed=fed_deduction
                    tax_remainder=(annual_income - tax_bracket)*rate/100
                    federal_tax_owed+=tax_remainder

                after_total_tax=annual_income - federal_tax_owed - state_tax_owed - fica 
                context["after_total_tax"]=after_total_tax

            monthly_take_home_float=after_total_tax/12
            monthly_take_home = locale.currency(monthly_take_home_float, grouping=True)


            gross_pay=locale.currency(after_total_tax, grouping=True)
            context['gross_pay']=gross_pay

            monthly_household_float=monthly_take_home_float*.3
            monthly_household = locale.currency(monthly_household_float, grouping=True)

            savings_monthly_float = monthly_take_home_float*.15
            savings_monthly = locale.currency(savings_monthly_float, grouping=True)

            fun_monthly_float = monthly_take_home_float*.25
            fun_monthly = locale.currency(fun_monthly_float, grouping=True)
            
            fica_taxes_owed_clean = locale.currency(fica, grouping=True)

            state_tax_owed_clean = locale.currency(state_tax_owed, grouping=True)

            federal_tax_owed_clean = locale.currency(federal_tax_owed, grouping=True)
            context['state_tax_owed']=state_tax_owed
            context['federal_tax_owed']=federal_tax_owed
            context['fica_taxes_owed']=fica
            context['fun_monthly']=fun_monthly
            context['savings_monthly']=savings_monthly
            context['monthly_household']=monthly_household
            context['monthly_take_home']=monthly_take_home
            context['fica_taxes_owed_clean']=fica_taxes_owed_clean
            context['state_tax_owed_clean']=state_tax_owed_clean
            context['federal_tax_owed_clean']=federal_tax_owed_clean
            

            return render(request,'base/display-sheet.html', context)
        else:
            form = Calculator()

    return render(request, 'base/calculator.html', context)



def mortgage(request):
    form=Mortgage(request.POST)
    context={
        'form':form
    }
    form=Mortgage(request.POST)

    if request.method == 'POST':
        form=Mortgage(request.POST)
        if form.is_valid():
            purchase_price=form.cleaned_data['purchase_price']
            down_payment=form.cleaned_data['down_payment']

            
            interest_rate=form.cleaned_data['interest_rate']

           
            loan_term=form.cleaned_data['loan_term']
            context['purchase_price']=purchase_price
            context['down_payment']=down_payment
            context['interest_rate']=interest_rate
            context['loan_term']=loan_term

            loan_amount = purchase_price - (purchase_price*down_payment/100)
            loan_amount_clean = locale.currency(loan_amount, grouping=True)
            context['loan_amount']=loan_amount_clean

            monthly_interest_rate = interest_rate / 12 / 100
            loan_term=int(loan_term)
            amount_monthly_payments = int(loan_term * 12)
            context["amount_monthly_payments"]=amount_monthly_payments

            monthly_payment = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** amount_monthly_payments / ((1 + monthly_interest_rate)**(amount_monthly_payments) - 1)
            monthly_payment_clean = locale.currency(monthly_payment, grouping=True)
            context['monthly_payment']=monthly_payment_clean
            

            return render(request,'base/mortgage-sheet.html', context)


 
    return render(request, 'base/mortgage.html', context)