from distutils.log import error
import smtplib
import os
from flask import Flask,render_template,redirect,request,session,url_for,current_app
from flask_admin import Admin,AdminIndexView
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from email.message import EmailMessage

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.sqlite3'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


db = SQLAlchemy(app)

class User(db.Model):
   __tablename__ = 'User'
   id = db.Column('user_id', db.Integer, primary_key = True)
   u_name = db.Column(db.String(100),nullable = False,unique=True)
   full_name = db.Column(db.String(100),nullable = False)
   password = db.Column(db.String,nullable = False)
   about = db.Column(db.Text(500),nullable = False)
   email = db.Column(db.String(200),nullable = False,unique=True)
   dob = db.Column(db.Date,nullable = False)
   city = db.Column(db.String)
   state = db.Column(db.String)
   photo = db.Column(db.String,nullable=False)
   cover_photo = db.Column(db.String,nullable=False)
   resume = db.Column(db.String,nullable=False)

   def __init__(self, u_name,full_name,password,about,email,dob,city,state,photo,cover_photo,resume):
      self.u_name = u_name
      self.full_name = full_name
      self.password = password
      self.about = about
      self.email = email
      self.dob = dob
      self.city = city
      self.state = state
      self.photo = photo
      self.cover_photo = cover_photo
      self.resume = resume

   def __str__(self):
      return self.full_name

class Education(db.Model):
   __tablename__ = 'Education'
   id = db.Column('edu_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   user = db.relationship("User",backref="User")
   degree_name = db.Column(db.String(100))
   university_name = db.Column(db.String(100))
   year = db.Column(db.Integer)
   city = db.Column(db.String)
   state = db.Column(db.String)
   score = db.Column(db.String)

   def __init__(self,user_id,degree_name,university_name,year,city,state,score):
      self.user_id= user_id
      self.degree_name = degree_name
      self.university_name = university_name
      self.year = year
      self.city = city
      self.state = state
      self.score = score

   def __str__(self):
      return self.degree_name

class Job(db.Model):
   __tablename__ = 'Job'
   id = db.Column('job_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   user = db.relationship("User")
   role = db.Column(db.String(100))
   company = db.Column(db.String(100))
   city = db.Column(db.String)
   state = db.Column(db.String)
   started_at = db.Column(db.Date)
   ended_at = db.Column(db.Date)

   def __init__(self,user_id,role,company,city,state,started_at,ended_at):
      self.user_id = user_id
      self.role = role
      self.company = company
      self.city = city
      self.state = state
      self.started_at = started_at
      self.ended_at =ended_at

   def __str__(self):
      return self.company

class Social_accounts(db.Model):
   __tablename__='Social Account'
   id = db.Column('sa_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   user = db.relationship("User")
   name = db.Column(db.String(100))
   url = db.Column(db.String(100))
   is_public = db.Column(db.Boolean)

   def __init__(self,user_id,name,url,icon,is_public):
      self.user_id = user_id
      self.name = name
      self.url = url
      self.icon = icon
      self.is_public = is_public

   def __str__(self):
      return self.name

class Project(db.Model):
   __tablename__='Project'
   id = db.Column('project_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   user = db.relationship("User")
   name = db.Column(db.String(100))
   description = db.Column(db.Text(1000))
   started_at = db.Column(db.Date)
   ended_at = db.Column(db.Date)
   url = db.Column(db.String(100))
   logo = db.Column(db.String )
   screenshots = db.Column(db.String)

   def __init__(self,user_id,name,description,started_at,ended_at,url,logo,screenshots):
      self.user_id = user_id
      self.name = name
      self.description = description
      self.started_at = started_at
      self.ended_at = ended_at
      self.url = url
      self.logo = logo
      self.screenshots = screenshots

   def __str__(self):
      return self.name

class Certification(db.Model):
   __tablename__='Certification'
   id = db.Column('certificate_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   user = db.relationship("User")
   name = db.Column(db.String(100))
   organization = db.Column(db.String(100))
   url = db.Column(db.String(100))

   def __init__(self,user_id,name,organization,url):
      self.user_id = user_id
      self.name = name
      self.organization = organization
      self.url = url

   def __str__(self):
      return self.name

class Skill_category(db.Model):
   __tablename__='Skill_category'
   id = db.Column('skill_category_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   user = db.relationship("User")
   name = db.Column(db.String(100))

   def __init__(self,user_id,name):
      self.user_id = user_id
      self.name = name

   def __str__(self):
      return self.name

class Skills(db.Model):
   __tablename__='User_Skills'
   id = db.Column('skill_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
   user = db.relationship("User")
   category_id = db.Column(db.Integer, db.ForeignKey('Skill_category.skill_category_id'))
   category = db.relationship("Skill_category", backref="Skill_category")
   name = db.Column(db.String(100))
   icon_small = db.Column(db.String(100))
   proficiency = db.Column(db.Integer())


   def __init__(self,user_id,name,category_id,proficiency,icon_small):
      self.user_id = user_id
      self.category_id = category_id
      self.name = name
      self.proficiency = proficiency
      self.icon_small = icon_small

   def __str__(self):
      return self.name



admin = Admin(app, name='Dashboard', template_mode='bootstrap3',url='/admin')

admin.add_view( ModelView(User, db.session, name='User') )
admin.add_view( ModelView(Education, db.session, name='Education') )
admin.add_view( ModelView(Job, db.session, name='Job') )
admin.add_view( ModelView(Social_accounts, db.session, name='Scocial Accounts') )
admin.add_view( ModelView(Project, db.session, name='Project') )
admin.add_view( ModelView(Skill_category, db.session, name='Skill Category') )
admin.add_view( ModelView(Skills, db.session, name='User Skills') )
admin.add_view( ModelView(Certification, db.session, name='Certification') )


@app.route('/', methods=['GET','POST'])
def welcome():
   user = User.query.count()
   if request.method == 'POST':
      name = request.form['name']
      email = request.form['email']
      subject = request.form['subject']
      message = request.form['message']
      your_name = 'Portfolio Web'
      your_email = #'portfolio_web_email_id'
      your_password = #'*************'
      server = smtplib.SMTP('smtp.gmail.com',587)
      server.ehlo()
      server.starttls()
      server.login(your_email,your_password)
      sender_email = #'portfolio_web_email_id'
      receiver_email = #'your_email_id'
      msg = EmailMessage()
      msg.set_content('\nDear Sanpreet Kaur,\n\nSomeone trying to contact you.\n\n'+'Name: '+str(name)+'\nEmail: '+str(email)+'\nMessage: '+str(message)+'\n\nRegards,\nPortfolio Web')
      msg['Subject'] = subject
      msg['From'] = sender_email  #portfolio_web_email_id
      msg['To'] = receiver_email  #your_email_id
      msg2 = EmailMessage()
      msg2.set_content('\nDear '+str(name)+',\n\nYour Message was sent Successfully.\n\nYour Message: '+str(message)+'\n\nRegards,\nPortfolio Web')
      msg2['Subject'] = 'Your Message was sent Successfully.'
      msg2['From'] = sender_email  #portfolio_web_email_id
      msg2['To'] = email #message_sender's_email_id
      try:
         server.send_message(msg)
         server.send_message(msg2)
         print('send')

      except:
         print('fail')
         pass
      return render_template('main.html',user = user)
   return render_template('main.html',user = user)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
   error = None
   if request.method == 'POST':
        u_name = request.form['u_name']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(u_name=u_name,email=email,password=password).first()
        if user:
         return redirect('/admin')
        else:
         error = 'Invalid Credentials'
   return render_template('login.html',error=error)


@app.route('/<u_name>', methods=['GET','POST'])
def index(u_name):
   user = User.query.filter_by(u_name=u_name).first()
   education = Education.query.filter_by(user=user)
   job = Job.query.filter_by(user=user)
   social = Social_accounts.query.filter_by(user=user)
   project = Project.query.filter_by(user=user)
   certification = Certification.query.filter_by(user=user)
   skill_category = Skill_category.query.filter_by(user=user)
   skills = Skills.query.filter_by(user=user)
   if user is None:
       return "Not Found"
   else:
      return render_template('index.html',user=user,education=education,job=job,social=social,project=project,certification=certification,skill_category=skill_category,skills=skills)

@app.route("/<u_name>/sendmail/", methods=['GET','POST'])
def sendmail(u_name):
   print("sendmail")
   user = User.query.filter_by(u_name=u_name).first()
   print(user.email)
   if request.method == 'POST':
      name = request.form['name']
      email = request.form['email']
      subject = request.form['subject']
      message = request.form['message']
      your_name = 'Portfolio Web'
      your_email = #'portfolio_web_email_id'
      your_password = #'*************'
      server = smtplib.SMTP('smtp.gmail.com',587)
      server.ehlo()
      server.starttls()
      server.login(your_email,your_password)
      sender_email = #'portfolio_web_email_id'
      receiver_email = user.email #user_email_id or your_email_id
      msg = EmailMessage()
      msg.set_content('\nDear '+user.full_name+',\n\nSomeone is trying to contact you through Portfolio Web.\n\n'+'Name: '+str(name)+'\nEmail: '+str(email)+'\nMessage: '+str(message)+'\n\nRegards,\nPortfolio Web')
      msg['Subject'] = 'You have a Message - '+subject
      msg['From'] = sender_email  #'portfolio_web_email_id'
      msg['To'] = receiver_email
      msg2 = EmailMessage()
      msg2.set_content('\nDear '+str(name)+',\n\nYour Message was sent Successfully.\n\nYour Message: '+str(message)+'\n\nRegards,\nPortfolio Web')
      msg2['Subject'] = 'Your Message was sent Successfully.'
      msg2['From'] = sender_email  #'portfolio_web_email_id'
      msg2['To'] = email  #message_sender's_email_id
      try:
         server.send_message(msg)
         server.send_message(msg2)
         print('send')
      except:
         print('fail')
         pass
   return redirect(url_for('index',u_name=u_name))

@app.route('/<u_name>/project/<p_name>')
def project(u_name,p_name):
   user = User.query.filter_by(u_name=u_name).first()
   project = Project.query.filter_by(user=user,name=p_name).first()
   description = project.description.split('.')
   social = Social_accounts.query.filter_by(user=user)
   if project is None:
      return "Not Found"
   return render_template('project.html',user=user,project=project,social=social,description=description)

if __name__ == '__main__':
    with app.app_context():
        print(current_app.name)
        db.create_all()
        app.debug = False
        app.run(host="0.0.0.0")
