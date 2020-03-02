# -*- coding: utf-8 -*-
from app import app
from flask import request, jsonify, send_file, session, send_from_directory
from werkzeug.utils import secure_filename
import os
import re
import csv
import time


@app.route('/echo', methods=['GET', 'PUT'])
def echo():
    if request.method == 'GET':
        if 'USER_ANSWER' in session:
            return jsonify({'string': session['USER_ANSWER']})
        else:
            return jsonify({'error': 'String is not set up still'})
    else:
        if 'str' in request.args:
            session['USER_ANSWER'] = request.args.get('str')
            return jsonify({'status': 'ok'})
        else:
            return jsonify({'error':"There is no argument 'str'"})


@app.route('/top', methods=['POST'])
def top():
    st = time.clock()
    if 'input' in request.files:
        file = request.files['input']
        filename = secure_filename(file.filename)
        if filename.split('.')[-1] == 'csv':
            if 'field' in request.form:
                if 'count' in request.form:
                    field = request.form['field']
                    count = request.form['count']
                    try:
                        count = int(count)
                    except ValueError:
                        return jsonify({'error': "Argument 'count' must be positive integer"})
                    if count > 0:
                        plain = file.read().decode("utf-8")
                        rows = re.split('\n|\r|\t',plain)
                        rows = [re.split(',|;', row) for row in rows if row]
                        header = [item.strip().replace('"','') for item in rows[0]]
                        rows = rows[1:]
                        sorted_filename = 'sorted_csv.csv'
                        if field in header:
                            rows.sort(key=lambda i: i[header.index(field)])
                            sorted_rows = rows[:count]
                            with open(os.path.join(app.root_path + '\\files', sorted_filename), 'w') as output:
                                writer = csv.writer(output, delimiter=';')
                                writer.writerow(header)
                                for row in sorted_rows:
                                    writer.writerow(row)
                            return jsonify(
                                {'status': 'ok', 'url': request.host_url + 'download?file=' + sorted_filename,
                                 'time': time.clock() - st})
                        else:
                            return jsonify({'error': "There is no column '{}' ".format(field)})
                    else:
                        return jsonify({'error': "Argument 'count' must be positive integer"})
                else:
                    return jsonify({'error': "There is no argument 'count' in file"})
            else:
                return jsonify({'error': "There is no argument 'field' "})
        else:
            return jsonify({'error': "Please send .csv file"})
    else:
        return jsonify({'error': "There is no file with parameter called 'input' "})


@app.route('/download', methods=['GET'])
def download():
    if 'file' in request.args:
        filename = request.args.get('file')
        if not filename in os.listdir(app.root_path + '\\files'):
            return jsonify({'error': "There is no file '{}'".format(filename)})
        else:
            return send_file(os.path.join(app.root_path + '\\files', filename),
                             as_attachment=True,
                             attachment_filename=filename,
                             mimetype='csv')
    else:
        return jsonify({'error': "There is no argument 'file'"})
