from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from pymysql import install_as_MySQLdb
from flask_script import Manager #对项目进行管理
from flask_migrate import Migrate,MigrateCommand #迁移指令
from sqlalchemy import or_
import math
from sqlalchemy import func

app=Flask(__name__)
install_as_MySQLdb()
#连接到MySQL中flaskDB数据库
app.config['SQLALCHEMY_DATABASE_URI']=\
    "mysql+pymysql://root:123456@127.0.0.1:3306/flaskDB"

#指定不需要信号追踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#制定程序的启动为调试模式
app.config['DEBUG']=True

#制定执行完增删改查之后的自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
#创建SQLALchemy的实例
db=SQLAlchemy(app)

#创建Manager对象并指定要管理的app
manager=Manager(app)
#创建Migrate对象并指定关联的app和db
migrate=Migrate(app,db)
#为manager增加数据库的迁移命令-db（自定义）,
# 具体操作由MigrateCommand来提供
manager.add_command('db',MigrateCommand)

#创建实体类-Users，映射到数据库中叫users表
#创建字段id，逐渐，自增
#创建字段username，长度为80的字符串，不能为空，值唯一，加索引
#创建字段age，整数，允许为空
#创建字段email，长度为120的字符串，必须唯一

class Users(db.Model):
    tablename='users'
    id=db.Column(
        db.Integer,
        primary_key=True,
    )
    username=db.Column(
        db.String(80),
        nullable=False,
        unique=True,
        index=True,
    )
    age=db.Column(
        db.Integer,
        nullable=True,
    )
    email=db.Column(
        db.String(120),
        unique=True,
    )
    isActive=db.Column(
        db.Boolean,
        default=True
    )
    birthday=db.Column(db.Date)

class Teacher(db.Model):
    id=db.Column(db.Integer,
                 primary_key=True)
    tname=db.Column(db.String(30),
                    nullable=False)
    tage=db.Column(db.Integer,
                   nullable=False)
    #增加一个外键列-course_id，引用自course类
    # （course表）的主键id
    course_id=db.Column(
        db.Integer,
        db.ForeignKey('course.id')
    )
    #增加一个关联属性，表示的要引用wife的信息
    #关联属性：在teacher中要增加那个属性用于表示对wife的引用
    #反向引用关系属性：在teacher中设置但要增加到wife中，表示的是在wife中要增加哪个
    #属性表示对teacher的引用
    wife=db.relationship(
        'Wife',
        backref="teacher",
        uselist=False,
    )
class Course(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    cname = db.Column(db.String(30),
                      nullable=False)
    #增加对teacher的关联属性和反向引用关系属性
    teachers=db.relationship(
        'Teacher',
        backref='course',#对应的是teacher中老师所对应的课程
        lazy='dynamic',
    )

class Student(db.Model):
    tablename='student'
    id=db.Column(
        db.Integer,
        primary_key=True,
    )
    sname=db.Column(
        db.String(120),
        nullable=True,
    )
    sage=db.Column(
        db.Integer
    )
    isActive=db.Column(
        db.Boolean,
        default=True,
    )

class Wife(db.Model):
    id=db.Column(db.Integer,
                 primary_key=True)
    wname=db.Column(
        db.String(30))
#增加一个属性-teacher_id，表示对teacher类的主键引用，并且实施唯一约束
    teacher_id=db.Column(
        db.Integer,
        db.ForeignKey('teacher.id'),
        unique=True
    )


#先删除所有表结构(用于修改表的结构，在没有数据的情况下)
# db.drop_all()

#将所有的实体类生成对应的表结构
#前提：表不存在的情况下才能生成
# db.create_all()

@app.route('/01-add')
def add_views():
    #创建Users的对象并赋值
    user=Users()
    user.username='祁QTX'
    user.age=30
    user.email='qiqtx.lv@163.com'
    user.birthday='2005-10-12'
    #将Users的对象保存会数据库
    db.session.add(user)
    #提交事务
    # db.session.commit()
    #响应一句话
    return "增加数据成功"

@app.route('/02-reg',methods=['GET','POST'])
def reg():
    if request.method=='GET':
        return render_template('02-reg.html')
    else:
        #接收前段传递过来的数据并创建Users对象
        user=Users()
        user.username=request.form['username']
        user.age=request.form['age']
        user.email=request.form['email']
        user.birthday=request.form['birthday']
        if 'isActive' not in request.form:
            user.isActive=False
        #2.保存
        db.session.add(user)
        return '注册成功'

@app.route('/03-query')
def query_views():
    # query=db.session.query(Users.id,
    #                        Users.username)
    # print(query)
    # print('type:',type(query))
    users=db.session.query(Users).all()
    for u in users:
        print('id:%d,user:%s,age:%d,email:%s'
              % (u.id,u.username,u.age,u.email))
    return '查询成功'

    #查询Users实体中的第一条数据
    user=db.session.query(Users).first()
    print(user)
    #查询Users实体中共有多少数据
    count=db.session.query(Users).count()
    print(count)

@app.route('/04-filter')
def filter_views():
    #查询年龄大于30的users
    # result=db.session.query(Users).filter(
    #     Users.age>20
    # ).all()
    # print(result)
    # print('type:',type(result))
    #查询id为2的Users的信息
    result=db.session.query(Users).filter(Users.id==2).first()
    print(result)
    #方案2：使用filter(条件1，条件2)
    users=db.session.query(Users).filter(
        Users.isActive==True,Users.age>=30
    ).all()
    print(users)
    #查询isActive为True或者年龄大于30岁的Users
    #or：使用or_ 函数
    #from sqlalchemy import or_
    users=db.session.query(Users).filter(
        or_(
            Users.isActive==True,
            Users.age>=30
        )
    ).all()
    print(users)
    return 'ok'

@app.route('/05-users')
def user_views():
    # users=db.session.query(Users).filter(Users.isActive==True)
    users=db.session.query(Users).filter(
        Users.isActive==True
    )
    #判断是否有kw参数传递到视图中
    if 'kw' in request.args:
        kw=request.args['kw']
        users=users.filter(
            or_(
                Users.username.like('%'+kw+'%'),
                Users.email.like('%'+kw+'%')
            )
        )
    users=users.all()
    return render_template('05-users.html',
                           users=users)

@app.route('/06-limit')
def limit_views():
    users=db.session.query(Users).limit(2).offset(2).all()
    print(users)
    return 'ok'

@app.route('/07-page')
def page_views():
    #变量-pageSize,表示每页显示的记录数量
    pageSize=2
    #变量-currentPage,表示当前想看的页数
    currentPage=int(request.args.get(
        'currentPage',1))
    #查询第currentPage页的数据
    #跳过（currentPage-1）*pageSize条数据，再获取
    #前pageSize条数据
    ost=(currentPage-1)*pageSize
    users=db.session.query(Users).offset(ost).\
        limit(pageSize).all()
    #通过pageSize和总记录数计算尾页页码
    totalCount=db.session.query(Users).count()
    lastPage=math.ceil(totalCount/pageSize)
    #计算上一页的页码
    #如果currentPage大于1的话，那么上一页就是currentPage-1,
    #否则上一页就是1
    prevPage=1
    if currentPage>1:
        prevPage=currentPage-1
    #计算下一页页码
    #如果currentPage小于1的话，那么下一页就是currentPage+1
    #否则下一页就是尾页
    nextPage=lastPage
    if currentPage<lastPage:
        nextPage=currentPage+1
    return render_template('07-page.html',
            params=locals())
    pass

@app.route('/08-aggr')
def aggregat_views():
    result=db.session.query(
        func.avg(Users.age),
        func.sum(Users.age),
        func.min(Users.age),
        func.max(Users.age)).all()
    print(result)
    return 'ok'
@app.route('/09-aggr-exer')
def aggr_exer():
#     result=db.session.query(func.avg(Users.age))\
#         .fileter(Users.age>18)
#     print(result)
#     result=db.session.query(
#         Users.isActive,
#     func.count(Users.id)).group_by('isActive')
#     print(result)
#     result=db.session.query(
#         Users.isActive,
#         func.count(Users.id)
#     ).group_by('isActive').having(
#         func.count(Users.id>2)
#     ).all()
#     print(result)
#     result=db.session.quert(
#         Users.isActive,
#     func.count(Users.id))\
#         .filter(Users.age>18)\
#         .group_by('isActive')\
#         .having(func.count(Users.id>2)).all()
#     return result
    #查询users表中年龄大于‘老王’的users表的信息
    result=db.session.query(Users).filter(
        Users.age>db.session.query(Users.age).filter(Users.username=='老王')).all()
    print(result)
    return 'ok'

@app.route('/10-update')
def update_views():
    #修改
    user=db.session.query(Users).filter_by(username='老王').first()
    user.isActive=False
    db.session.add(user)
    db.session.delete(user)
    return '修改数据成功'

@app.route('/11-upuser',methods=['GET','POST'])
def upuser():
    if request.method=='GET':
        #接受id
        id=request.args['id']
        #按id查询对象
        user=db.session.query(Users).filter_by(id=id).first()
        #将对象发送到模板上
        return render_template(
            '11-upuser.html',user=user)
    else:
        #接受请求的参数
        id=request.form['id']
        #查询除对应的对象
        user=db.session.query(Users).filter_by(id=id).first()
        #为对象赋值
        user.username=request.form['username']
        user.age=request.form['age']
        user.email=request.form['email']
        user.birthday=request.form['birthday']
        if 'isActive' in request.form:
            user.isActive=True
        else:
            user.isActive=False
        #保存回数据库
        db.session.add(user)
        return redirect('/05-users')

@app.route('/12-regtea')
def regtea():
    #两种方法
    #1.通过teacher对象的course_id属性插入关联的数据
    # teaqi=Teacher()
    # teaqi.tname='张三'
    # teaqi.tage=30
    # teaqi.course_id=1
    # db.session.add(teaqi)
    #2.通过teacher对象的course属性插入关联属性
    course=Course.query.filter_by(cname='python高级').first()
    tea=Teacher()
    tea.tname='吕哲玛利亚'
    tea.tage=31
    tea.course=course #底层是将course.id给了
    # teacher.course_id属性
    db.session.add(tea)
    return 'sucessed'
@app.route('/13-otm',methods=['GET','POST'])
def otm():
    if request.method=='GET':
        #查询除course中的所有数据
        courses=Course.query.all()
        #渲染模板
        return render_template('13-otm.html',courses=courses)
    else:
        tname=request.form['tname']
        tage=request.form['tage']
        course_id=request.form['cid']
        tea=Teacher()
        tea.tname=tname
        tea.tage=tage
        tea.course_id=course_id
        db.session.add(tea)
        return '注册成功!'

@app.route('/14-otm-query')
def otm_query():
    # cour=Course.query.filter_by(id=1).first()
    # print('课程名称：',cour.cname)
    # result=cour.teachers.all()
    # print('result:',result)
    # print('type:',type(result))
    tea=Teacher.query.filter_by(tname='张三').first()
    cour=tea.course
    print('老师姓名：',tea.tname)
    print('所教课程',cour.cname)
    return 'sucessed!'

@app.route('/15-otm-exer')
def otm_exer():
    #1.查询褚所有的课程
    courses=Course.query.all()
    #获取前段提交过来的cid参数值，如果没有当0处理
    cid=int(request.args.get('cid',0))
    print(type(cid))
    #如果cid的值是非0的话则按照cid的值查询老师信息
    if cid==0:
        teachers=Teacher.query.all()
    else:
        # teachers=Teacher.query.filter_by(course_id=cid).all()
        #方案2;通过cid获取课程信息，再通过课程找到对应的老师们
        course=Course.query.filter_by(id=cid).first()
        teachers=course.teachers.all()
    #将课程和老师渲染到模板中
    #2.查询出所有的老师
    # teachers=Teacher.query.all()
    #3.将课程和老师渲染到模板中
    return render_template('15-otm-exer.html',params=locals())

@app.route('/16-oto')
def oto_views():
    #1.通过wife对象中的teacher_id属性表示要引用的teacher的主键
    # wife=Wife()
    # wife.wname='如花'
    # wife.teacher_id=1
    # db.session.add(wife)
    #2.通过wife对象中的teacher属性表示要引用的teahcer对象
    teacher=Teacher.query.filter_by(id=2).first()
    wife=Wife()
    wife.wname='小泽夫人'
    wife.teacher=teacher
    db.session.add(wife)
    return "ok"
if __name__=='__main__':
    # app.run(debug=True,host='0.0.0.0:5555')
    manager.run()