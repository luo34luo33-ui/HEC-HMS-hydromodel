"""
API层 - 路由定义
提供REST API端点
"""
import os
import ast
from datetime import datetime
from flask import Flask, request, send_from_directory
from flask_json import FlaskJSON, JsonError, json_response
from flask_uploads import UploadSet, configure_uploads
from werkzeug.utils import secure_filename

from services.model_service import ModelService, TaskService
from services.data_service import DataService
from utils.validators import validate_run_id
from config import paths

# 创建Flask应用
app = Flask(__name__)
flask_json = FlaskJSON()

# 配置上传
UPLOADS_DEFAULT_DEST = paths.get_upload_dir()
app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(UPLOADS_DEFAULT_DEST, 'hec_hms')
app.config['UPLOADED_FILES_ALLOW'] = 'csv'

model_hec = UploadSet('modelHec', extensions='csv')
configure_uploads(app, model_hec)
flask_json.init_app(app)

# 服务实例
model_service = ModelService()
data_service = DataService()
task_service = TaskService()


@app.route('/hec_hms/', methods=['POST', 'GET'])
def init_default():
    """默认端点"""
    return json_response(status_=200, description='HEC-HMS API Server')


@app.route('/hec_hms/init-start-single', methods=['POST'])
def init_hec_hms_single():
    """初始化单一模型"""
    req_args = request.args.to_dict()

    if 'run-name' not in req_args or not req_args['run-name']:
        raise JsonError(status_=400, description='run-name is not specified.')

    run_name = req_args['run-name']
    run_datetime_str = request.args.get(
        'datetime',
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        type=str
    )
    init_state_str = request.args.get('init-state', default=False, type=str)
    init_state = ast.literal_eval(init_state_str)

    run_datetime = datetime.strptime(run_datetime_str, '%Y-%m-%d %H:%M:%S')
    input_dir_rel_path = os.path.join(run_datetime.strftime('%Y-%m-%d'), run_name, 'input')
    input_dir_abs_path = os.path.join(UPLOADS_DEFAULT_DEST, input_dir_rel_path)

    if os.path.exists(input_dir_abs_path):
        raise JsonError(
            status_=400,
            description=f'run-name: {run_name} is already taken for run date: {run_datetime}'
        )

    req_files = request.files
    if 'rainfall' in req_files:
        rainfall_path = os.path.join(input_dir_rel_path, 'DailyRain.csv')
        model_hec.save(req_files['rainfall'], folder=input_dir_rel_path, name='DailyRain.csv')
        result = model_service.init_model('single', run_name, run_datetime_str, rainfall_path, init_state)
        return json_response(status_=200, **result)

    raise JsonError(status_=400, description='Missing required input file. Required DailyRain.csv')


@app.route('/hec_hms/init-start-distributed', methods=['POST'])
def init_hec_hms_distributed():
    """初始化分布式模型"""
    req_args = request.args.to_dict()

    if 'run-name' not in req_args or not req_args['run-name']:
        raise JsonError(status_=400, description='run-name is not specified.')

    run_name = req_args['run-name']
    run_datetime_str = request.args.get(
        'datetime',
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        type=str
    )
    run_datetime = datetime.strptime(run_datetime_str, '%Y-%m-%d %H:%M:%S')

    input_dir_rel_path = os.path.join(run_datetime.strftime('%Y-%m-%d'), run_name, 'input')
    input_dir_abs_path = os.path.join(UPLOADS_DEFAULT_DEST, input_dir_rel_path)

    if os.path.exists(input_dir_abs_path):
        raise JsonError(
            status_=400,
            description=f'run-name: {run_name} is already taken for run date: {run_datetime}'
        )

    for f in request.files.getlist('rainfall'):
        filename = secure_filename(f.filename)
        f.save(os.path.join(input_dir_rel_path, filename))

    return json_response(status_=200, description='Successfully saved files.')


@app.route('/hec_hms/init-run', methods=['POST', 'GET'])
def run_hec_hms():
    """运行模型"""
    req_args = request.args.to_dict()

    if 'run-name' not in req_args or not req_args['run-name']:
        raise JsonError(status_=400, description='run-name is not specified.')

    run_name = req_args['run-name']
    run_datetime = request.args.get(
        'datetime',
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        type=str
    )

    run_date = datetime.strptime(run_datetime, '%Y-%m-%d %H:%M:%S')
    run_date_str = run_date.strftime('%Y-%m-%d')
    run_id = f"HECHMS:single:{run_date_str}:{run_name}"

    result = model_service.run_model(run_id)
    return json_response(status_=200, **result)


@app.route('/hec_hms/upload_data', methods=['POST'])
def upload_hec_data():
    """上传数据"""
    req_args = request.args.to_dict()

    if 'run-name' not in req_args or not req_args['run-name']:
        raise JsonError(status_=400, description='run-name is not specified.')

    run_name = req_args['run-name']
    run_datetime_str = request.args.get(
        'datetime',
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        type=str
    )
    force_insert_str = request.args.get('force-insert', default=False, type=str)
    force_insert = ast.literal_eval(force_insert_str)

    # TODO: 实现数据上传逻辑
    return json_response(status_=200, description='Data uploaded successfully.')


@app.route('/hec_hms/upload', methods=['POST'])
def upload_output():
    """上传输出文件"""
    req_args = request.args.to_dict()

    if 'run-id' not in req_args or not req_args['run-id']:
        raise JsonError(status_=400, description='run-id is not specified.')
    if 'zip-file-name' not in req_args or not req_args['zip-file-name']:
        raise JsonError(status_=400, description='zip-file-name is not specified.')

    # TODO: 实现文件打包逻辑
    return json_response(status_=200, description='Files packaged successfully.')


def create_app():
    """创建Flask应用"""
    return app
