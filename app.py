from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Account:
    accNo = 0
    name = ''
    deposit = 0
    type = ''  #current/saving

    def createAccount(self, accNo, name, type, deposit):
        self.accNo = accNo
        self.name = name
        self.type = type
        self.deposit = deposit

    def showAccount(self):
        return {
            "Account Number": self.accNo,
            "Account Holder Name": self.name,
            "Type of Account": self.type,
            "Balance": self.deposit,
        }

    def modifyAccount(self, name, type, deposit):
        self.name = name
        self.type = type
        self.deposit = deposit

    def depositAmount(self, amount):
        self.deposit += amount

    def withdrawAmount(self, amount):
        self.deposit -= amount

accounts = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    accNo = int(request.form['accountNo'])
    name = request.form['accountHolderName']
    account_type = request.form['accountType']
    deposit = float(request.form['initialAmount'])

    account = Account()
    account.createAccount(accNo, name, account_type, deposit)
    accounts.append(account)
    
    return redirect(url_for('home')) 

@app.route('/display_all')
def display_all():
    account_info = [account.showAccount() for account in accounts] #list comprehension
    return render_template('display_all.html', accounts=account_info)

@app.route('/display_specific', methods=['POST'])
def display_specific():
    account_number = int(request.form['accountNumber'])

    for account in accounts:
        if account.accNo == account_number:
            account_info = account.showAccount()
            return render_template('display_specific.html', account=account_info)
    
    return "Account not found."

@app.route('/deposit_withdraw', methods=['POST'])
def deposit_withdraw():
    account_number = int(request.form['accountNumber'])
    amount = float(request.form['amount'])
    action = request.form['action']

    for account in accounts:
        if account.accNo == account_number:
            if action == 'Deposit':
                account.depositAmount(amount)
            elif action == 'Withdraw':
                account.withdrawAmount(amount)
            return redirect(url_for('home'))
    
    return "Account not found."

if __name__ == '__main__':
    app.run(debug=True)
 