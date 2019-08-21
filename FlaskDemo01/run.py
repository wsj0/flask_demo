from flask import Flask,request,render_template
import datetime
import os
#创建实例对象
app=Flask(__name__)

def generate_filename(filename):
    """
    通过原始文件名称生成一个由时间来组成的新文件名
    :param filename: 原始文件名称
    :return: 生成新文件
    """
    ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    ext=filename.split('.')[-1]
    filename=ftime+'.'+ext
    return filename

def generate_upload_path(file,dirname,filename):
    """

    :param file: 获取当前文件的根路径的文件
    :param dirname: 保存文件的具体目录
    :param filename: 保存的文件名称
    :return:
    """
    base_dir=os.path.dirname(file)
    upload_path=os.path.join(base_dir,dirname,filename)
    return upload_path

@app.route('/01-file',methods=['GET','POST'])
def file_views():
    if request.method=='GET':
        return render_template('01-file.html')
    else:


        # 1、接受前段传递过来的图片
        if 'uimg' in request.files:
            file=request.files.get('uimg')
            #2、拼年月日时分秒作为文件名称
            ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            #3、获取上传文件的扩展名
            #去后缀名
            ext=file.filename.split('.')[-1]
            filename=ftime+'.'+ext
            # 4、准备上传路径
            #可以得到run.py的路劲
            basedir=os.path.dirname(__file__)
            print('basedir:',basedir)
            #拼上传的完整路径
            #加到run.py所在路径的static文件夹下,取名为filename的值
            upload_path=os.path.join(basedir,"static",filename)
            file.save(upload_path)
            return '上传文件成功'

@app.route('/02-file-exer',methods=['GET','POST'])
def file_exer():
    if request.method=='GET':
        return render_template('02-file-exer.html')
    else:
        title=request.form.get('title')
        type = request.form.get('type')
        content = request.form.get('content')
        print("标题：%s,类型：%s,内容：%s" % (title,type,content))
        #判断文件上传
        if 'img' in request.files:
            file=request.files.get('img')
            filename=generate_filename(file.filename)
            up_path=generate_upload_path(__file__,
                                         'static/upload',
                                         filename)
            file.save(up_path)
        return '获取数据成功'

#启动服务
if __name__=='__main__':
    app.run(debug=True)