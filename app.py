from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import yaml
import os
import platform
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class ConfigForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    metaUrl = StringField('Meta URL', validators=[DataRequired()])
    bucketEndpoint = StringField('Bucket Endpoint', validators=[DataRequired()])
    accessKey = StringField('Access Key', validators=[DataRequired()])
    secretKey = StringField('Secret Key', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'w') as file:
            yaml.dump({}, file)
    
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    os_type = platform.system()
    
    try:
        juicefs_version = subprocess.check_output(['./juicefs', '--version']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        juicefs_version = "无法获取版本号"
    
    return render_template('home.html', config=config, os_type=os_type, juicefs_version=juicefs_version)

@app.route('/delete/<name>', methods=['POST'])
def delete_config(name):
    if request.form.get('confirm') == 'yes':
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        
        if name in config:
            del config[name]
            
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file)
        
        flash('配置已删除', 'success')
    else:
        flash('删除操作已取消', 'info')
    
    return redirect(url_for('home'))

@app.route('/view/<name>', methods=['GET'])
def view_config(name):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    if name not in config:
        return "Configuration not found", 404
    
    details = config[name]
    status_info = get_juicefs_status(details['metaUrl'])
    
    return render_template('view_config.html', name=name, details=details, status_info=status_info)

@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit_config(name):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    if name not in config:
        return "Configuration not found", 404
    
    details = config[name]
    form = ConfigForm(data={
        'name': name,
        'metaUrl': details['metaUrl'],
        'bucketEndpoint': details['bucket']['endpoint'],
        'accessKey': details['bucket']['accessKey'],
        'secretKey': details['bucket']['secretKey']
    })
    
    if form.validate_on_submit():
        updated_config = {
            form.name.data: {
                'metaUrl': form.metaUrl.data,
                'bucket': {
                    'endpoint': form.bucketEndpoint.data,
                    'accessKey': form.accessKey.data,
                    'secretKey': form.secretKey.data
                }
            }
        }
        
        # 更新配置
        config.update(updated_config)
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
        
        flash('配置已更新', 'success')
        return redirect(url_for('view_config', name=form.name.data))
    
    return render_template('edit_config.html', form=form)

def get_juicefs_status(metaUrl):
    try:
        res = subprocess.run(['./juicefs', 'status', f'{metaUrl}'], capture_output=True, text=True, timeout=10)
        if res.returncode != 0:
            status_info = res.stderr
        else:
            status_info = res.stdout
    except subprocess.TimeoutExpired:
        status_info = "获取文件系统状态超时"

    return status_info

@app.route('/create_filesystem', methods=['GET', 'POST'])
def create_filesystem():
    form = ConfigForm()
    if form.validate_on_submit():
        command = [
            './juicefs', 'format',
            '--storage', 's3',
            '--bucket', form.bucketEndpoint.data,
            '--access-key', form.accessKey.data,
            '--secret-key', form.secretKey.data,
            form.metaUrl.data,
            form.name.data
        ]
        
        try:
            res = subprocess.run(command, capture_output=True, text=True, timeout=30)
            if res.returncode == 0:
                flash('文件系统创建成功', 'success')

                # 保存配置信息到 config.yaml
                with open('config.yaml', 'r') as file:
                    config = yaml.safe_load(file)
                
                new_config = {
                    form.name.data: {
                        'metaUrl': form.metaUrl.data,
                        'bucket': {
                            'endpoint': form.bucketEndpoint.data,
                            'accessKey': form.accessKey.data,
                            'secretKey': form.secretKey.data
                        }
                    }
                }

                config.update(new_config)

                with open('new_config.yaml', 'w') as file:
                    yaml.dump(config, file)

                return redirect(url_for('view_config', name=form.name.data))
            else:
                error_message = f'文件系统创建失败: {res.stderr}'
                return render_template('new_config.html', form=form, error=error_message)
        except subprocess.TimeoutExpired:
            error_message = '文件系统创建超时'
            return render_template('new_config.html', form=form, error=error_message)
    
    return render_template('new_config.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
