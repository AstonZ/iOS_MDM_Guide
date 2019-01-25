# coding=utf-8
from flask import Flask, request, jsonify, send_from_directory
import os, logging
from log_util2 import start_logging, dlog

start_logging('mdm')
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/device_enroll')
def device_enroll():
    dlog('get device enroll')
    return "Hi, welcome"


@app.route('/server', methods=['PUT', 'GET'])
def server():
    dlog('/server called method: ' + request.method)
    params = None
    if request.json:
        params = request.json
        dlog('params from json')
    elif request.args:
        params = request.args
        dlog('params from args')
    elif request.form:
        params = request.form
        dlog('params from form')
    if not params:
        dlog('there is no data')
        params = {'data': 'nodata'}
    dlog(params)
    return "server callback"


@app.route('/queue', methods=['PUT'])
def queue_cmd():
    dlog('/queue called')
    params = None
    if request.json:
        params = request.json
        dlog('params from json')
    elif request.args:
        params = request.args
        dlog('params from args')
    elif request.form:
        params = request.form
        dlog('params from form')
    if not params:
        dlog('there is no data')
        params = {'data': 'nodata'}
    dlog(params)
    return "queue callback"


@app.route('/checkin', methods=['PUT'])
def checkin():
    dlog('/checkin called')
    params = None
    if request.json:
        params = request.json
        dlog('params from json')
    elif request.args:
        params = request.args
        dlog('params from args')
    elif request.form:
        params = request.form
        dlog('params from form')
    if not params:
        dlog('there is no data')
        params = {'data': 'nodata'}
    dlog(params)
    return "checkin callback"


@app.route('/profile', methods=['GET'])
def download_profile():
    # os.getcwd()
    dlog('/download_profile called')
    params = None
    if request.json:
        params = request.json
        dlog('params from json')
    elif request.args:
        params = request.args
        dlog('params from args')
    elif request.form:
        params = request.form
        dlog('params from form')
    if not params:
        dlog('there is no data')
        params = {'data': 'none'}
    dlog(params)
    dlog('donwnloading profile')
    filename = 'MDM_local_test_signed.mobileconfig'
    response = send_from_directory('../../profile/', filename, as_attachment=True)
    # response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
    return response

@app.route('/signed_profile', methods=['GET'])
def download_profile():
    # os.getcwd()
    dlog('/download_profile called')
    params = None
    if request.json:
        params = request.json
        dlog('params from json')
    elif request.args:
        params = request.args
        dlog('params from args')
    elif request.form:
        params = request.form
        dlog('params from form')
    if not params:
        dlog('there is no data')
        params = {'data': 'none'}
    dlog(params)
    dlog('donwnloading profile')
    filename = 'MDM_local_test_signed.mobileconfig'
    response = send_from_directory('../../profile/', filename, as_attachment=True)
    # response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
    return response

# if __name__ == '__main__':
#     start_logging('mdm_server')
#     dlog(' server started !')
#     pass
    # 安全起见没有放在仓库
    # crt_path = '../../https/server/server-cert.cer'
    # key_path = '../../https/server/server-key.key'
    # ssl_contex=(crt_path, key_path)
    # if not os.path.exists(crt_path):
    #     dlog(crt_path + ' is not exitst !')
    #     raise ValueError(10000, 'pem_path is not exitst')
    # app.run('0.0.0.0', debug=True, port=8800)