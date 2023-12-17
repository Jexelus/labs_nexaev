from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os
import json
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/lab2', methods=['GET', 'POST'])
def lab2():
    if request.method == 'POST':
        uid = str(uuid.uuid4())
        form = request.form.to_dict()
        if os.path.exists('./form_requests/forms.json'):
            with open('./form_requests/forms.json', 'r') as f:
                data = json.load(f)
                f.close()
            with open('./form_requests/forms.json', 'w') as f:
                data[uid] = form
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.close()
        else:
            with open('./form_requests/forms.json', 'w') as f:
                json.dump({uid: form}, f, indent=4, ensure_ascii=False)
                f.close()
        with open('./static/'+uid+'.txt', 'w') as f:
            f.writelines('ФИО: '+form['FIO']+'\n')
            f.writelines('Серия паспорта: '+form['doc_ser']+'\n')
            f.writelines('Номер паспорта: '+form['doc_no']+'\n')
            f.writelines(f'request time: {datetime.now().strftime("%H:%M:%S")}'+'\n')
            f.close()
        return jsonify({'uid': uid})
                  
    if request.method == 'GET':
        return render_template('lab2.html')
    return render_template('error.html')

@app.route('/get_lecinse', methods=['GET'])
def get_lecinse():
    args = request.args.to_dict()
    print(args)
    if request.method == 'GET':
        return jsonify({'link': next(iter(args))+'.txt'})
    return render_template('error.html')

@app.route('/lab1', methods=['GET', 'POST'])
def lab1():
    if request.method == 'POST':
        form = request.form.to_dict()
        if os.path.exists('./form_requests/forms.json'):
            with open('./form_requests/forms.json', 'r') as f:
                data = json.load(f)
                f.close()
            with open('./form_requests/forms.json', 'w') as f:
                data[str(uuid.uuid4())] = form
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.close()
        else:
            with open('./form_requests/forms.json', 'w') as f:
                json.dump({str(uuid.uuid4()): form}, f, indent=4, ensure_ascii=False)
                f.close()
        return render_template('lab1.html', toast={'time': datetime.now().strftime('%H:%M'),
                                                   'body': 'Your form has been submitted successfully! (´｡• ω •｡`)'})
    if request.method == 'GET':
        return render_template('lab1.html')
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)