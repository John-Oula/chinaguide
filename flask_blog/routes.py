import re
import os
import secrets
from flask_mail import Mail,Message
from PIL import Image
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


from flask import render_template, url_for, flash, redirect, session, request,send_from_directory
from flask_admin import *
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, login_required, current_user, logout_user


from flask_blog.forms import UpdateAccount, Verify_form, Signup_form, Login_form, Upload_form, Session_form, \
    Lesson_form, Comment_form,Request_reset,Reset_password
from flask_blog.models import *
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cjohn222.jc@gmail.com'
app.config['MAIL_PASSWORD'] = 'johncurtis222'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
#from Werkzeug import secure_filename

#app.config[‘UPLOAD_FOLDER’] ='static/profile_pics'





admin = Admin(app, name='DASHBOARD')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Lesson, db.session))
admin.add_view(ModelView(Upload, db.session))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
@login_required
def profile():
#   if session['loggedin']:
#       mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#       mycursor.execute(" SELECT * FROM user WHERE   userid= %s ", [session['id']])
#       account = mycursor.fetchone()


#       return render_template('USER_BASE.html',account=account)

    flash('Please verify your account')
    return render_template('USER_BASE.html')


@app.route('/discover_h', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def discover_h(req_path):

    # Permission

    BASE_DIR = '/Users/ASUS/Desktop/100CHINAGUIDE/flask_blog/static'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return os.abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_from_directory(abs_path)

    # Show directory contents
    upload = os.listdir(abs_path)
    uploads = Upload.query.all()


    print(upload)
#    uploads = send_from_directory(directory='videos',filename='videos')
    return render_template('discover_h.html',user=user,uploads=uploads)

@app.route('/event')
def event():
    return render_template('EVENTS.html')

@app.route('/consult')
def consult():
    all_posts = Post.query.all()

    return render_template('CONSULT.html',all_posts=all_posts)

@app.route('/unitalk')
def unitalk():
    return render_template('UNITALK.html')

@app.route('/about')
def about():
    return render_template('ABOUT.html')


@app.route('/coronavirus')
def corona():
    return render_template('corona.html')


@app.route('/signup',methods=['POST','GET'])
def signup():
    form = Signup_form(request.form)
    if form.validate_on_submit() and request.method == "POST":
        flash('True')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,
                    username= form.username.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))


    return render_template('signup.html', form=form)



@app.route('/login',methods=['POST','GET'])
def login():
        form = Login_form()
        if form.validate_on_submit() and request.method == 'POST':
            user = User.query.filter_by(username = form.username.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                session['known'] = True
                session['known'] = form.username.data
                display_name = User.query.filter_by(username = form.username.data).first()
                session['known'] = display_name.id
                if current_user.role == 1 and current_user.sub_role == 0:
                    return redirect(url_for('session_admin',id = current_user.id))
                elif current_user.role == 1 and current_user.sub_role == 1:
                        return redirect(url_for('video_admin',id = current_user.id))
                elif current_user.role == 1 and current_user.sub_role == 2:
                    return redirect(url_for('info_admin',id = current_user.id))
                elif current_user.role == 1 and current_user.sub_role == 3:
                    return redirect(url_for('payment_admin',id = current_user.id))
                elif current_user.role == 1 and current_user.sub_role == 4:
                    return redirect(url_for('badge_admin',id = current_user.id))
                else:
                    return redirect(url_for('user_profile', username=current_user.username))
            else:
                pass
        return render_template('LOGIN.html', form=form)


#PROFILE FUNCTIONS

@app.route('/prefer')
@login_required
def prefer():
    return render_template('PREFER.html')

@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    user_role = current_user.role
    user = User.query.filter_by(username=username).first_or_404()
    uploads = Upload.query.all()

    all_users = User.query.all()
    total_users = len(all_users)
    all_posts = len(Post.query.all())
    data = Post.query.all()
    user_posts = len(current_user.posts)
    book_posts = len(current_user.book)
    booked = all_users
#    post_schema = PostSchema( many=True)
#    output = post_schema.dump(all_users)
#    return jsonify({output.data })
#    print(output)
    for booked in current_user.book:
        post_dict={
            "title": booked.title  ,
        "date": booked.date ,
        "start": booked.start_time
        }
        print(post_dict)
        f = open("package.json", "a")
        f.write(str(post_dict),)
        f.close()
    my_posts = len(current_user.posts)
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
#    for event in data:
#
#       #open and read the file after the appending: event._sa_instance_state = None
#       f = open("demofile2.txt", "r") new_event= (jsonpickle.encode(data, unpicklable=False))
#       print(f.read() print(new_event)
#    print(current_user.username ,'has',len(current_user.posts),'posts',all_posts)
    return render_template('Dashboard.html',uploads= uploads,user=user,my_posts=my_posts,book_posts=book_posts,total_users=total_users,user_role=user_role,all_users=all_users,user_posts = user_posts,image_file=image_file)




def reverse_admin():
    user = User.query.filter_by(role=1).first()
    user.role = 0
    db.session.commit()










def time():
    date = Post.query.all()
    for time in date:
        start = time.start_time
        x = re.split(r'([T+])', start)






@app.route('/update_admin/<int:id>')
@login_required
def update_to_admin(id):
    user = User.query.filter_by(id=id).first()
    user.role = 1
    db.session.commit()
    return redirect(url_for('user_profile',username=current_user.username))

@app.route('/update_session/<int:id>')
def assign_session(id):
    user = User.query.filter_by(id=id).first()

    user.sub_role = 0
    db.session.commit()
    return redirect(url_for('user_profile',username=current_user.username))

@app.route('/update_video_role/<int:id>')
def assign_video(id):
    user = User.query.filter_by(id=id).first()
    user.sub_role = 1
    db.session.commit()
    return redirect(url_for('user_profile',username=current_user.username))

@app.route('/update_info_role/<int:id>')
def assign_info(id):
    user = User.query.filter_by(id=id).first()
    user.sub_role = 2
    db.session.commit()
    return redirect(url_for('user_profile',username=current_user.username))

@app.route('/update_payment/<int:id>')
def assign_payment(id):
    user = User.query.filter_by(id=id).first()
    user.sub_role = 3
    db.session.commit()
    return redirect(url_for('user_profile',username=current_user.username))

@app.route('/update_badge/<int:id>')
def assign_badge(id):
    user = User.query.filter_by(id=id).first()
    user.sub_role = 4
    db.session.commit()
    return redirect(url_for('user_profile',username=current_user.username))






@app.route('/settings/<username>',methods=['GET','POST'])
@login_required
def settings(username):
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()
    user = User.query.filter_by(username=username).first_or_404()

    form = UpdateAccount()
    if request.method == 'POST':
        if form.pic.data:
            pic_file = save_pic(form.pic.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.password = form.password.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Updated!')
        return redirect(url_for('settings', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.password.data = current_user.password
        form.email.data = current_user.email
    return render_template('SETTINGS.html',user=user,all_users = all_users,user_role=user_role,form=form,image_file=image_file)


@app.route('/verify/<username>',methods=['POST','GET'])
@login_required
def verify(username):
    form = Verify_form()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        current_user.id_type = form.id_type.data
        current_user.id_number = form.id_number.data
        current_user.id_document = form.id_document.data
        current_user.nationality = form.nationality.data
        current_user.occupation = form.occupation.data
        current_user.email = form.email.data
        current_user.province = form.province.data
        current_user.phone = form.phone.data
        db.session.commit()
        return redirect(url_for('user_profile',username=current_user.username))
    return render_template('VERIFY.html',image_file=image_file,form=form,user=user)



@app.route('/logout')
@login_required
def  logout():

    logout_user()
    session['known'] = False
    print(session)

    return redirect(url_for('login'))


@app.route('/<username>')
@login_required
def user_profile(username):

    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    followed_posts=Post.query.join(followers, (followers.c.followed_id == Post.user_id)).all()

    all_posts = Post.query.all()

    all_users = User.query.all()
    author = db.session.query(Post.title).join(User.posts)
    user_role = current_user.role
    session['username'] = username



    return render_template('USER.html',followed_posts=followed_posts,user=user,user_role=user_role,all_users=all_users,all_posts = all_posts,author=author, image_file = image_file)
#    return redirect(url_for('login'))

#TRAINER PROFILE FUNCTIONS




#LOGIC FUNCTIONS



@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename ='profile_pics/' + user.image_file)

    all_posts = Post.query.all()
    all_lessons = Lesson.query.all()


#    uploads = url_for('static', filename='videos/' + current_user.uploads)
#    followed_posts = Post.query(User).join(Post)
#    print(followed_posts)
    return render_template('USER_BASE.html',user=user,image_file=image_file,all_posts=all_posts,all_lessons = all_lessons)




@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))




def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path,'static/profile_pics',pic_fn)
    output_size = (500,500)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_fn




UPLOADS_URL = 'http://localhost:5000/static/videos'


@app.route('/discover/<username>', defaults={'req_path': ''})
@app.route('/<path:req_path>')
@login_required
def discover(req_path,username):
    user = User.query.filter_by(username=username).first_or_404()

    session['username'] = current_user.username
    username= session['username']
    # Profile pic
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    # Permission
    user_role = current_user.role

    BASE_DIR = '/Users/ASUS/Desktop/100CHINAGUIDE/flask_blog/static'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return os.abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_from_directory(abs_path)

    # Show directory contents
    upload = os.listdir(abs_path)
    uploads = Upload.query.all()


    print(upload)
#    uploads = send_from_directory(directory='videos',filename='videos')
    return render_template('Discover.html',user=user,uploads=uploads,user_role=user_role,image_file=image_file)

@app.route('/book/<int:id>')
@login_required
def book(id):
    post=Post.query.filter_by(id=id).first()
    post.bookers.append(current_user)
    db.session.commit()

    return redirect(url_for('user_profile',username=current_user.username))

@app.route('/unbook/<int:id>')
@login_required
def unbook(id):
    post=Post.query.filter_by(id=id).first()
    post.bookers.remove(current_user)
    db.session.commit()

    return redirect(url_for('user_profile',username=current_user.username))


@app.route('/post/<int:id>')
@login_required
def  post(id):
    post = Post.query.get_or404(id)
    return redirect(url_for('login'))

@app.route('/videos/<upload_ref>' , methods=['POST','GET'])
@login_required

def video(upload_ref):
    form = Comment_form()
    video = Upload.query.filter_by(upload_ref=upload_ref).first()
    uploads  = Upload.query.all()
    user = User.query.all()
    comments = Comment.query.all()
    if request.method == 'POST':
        comment = Comment(content = form.content.data,user_id=current_user.id,upload_id=video.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('video',upload_ref=video.upload_ref))


    return render_template('VIDEO.html',comments = comments,video=video,uploads=uploads,user=user,form=form)

@app.route('/like/video=<int:id>')
@login_required
def like(id):
    video = Upload.query.filter_by(id=id).first()
    video.liked.append(current_user)
    db.session.commit()
    return redirect(url_for('video',upload_ref=video.upload_ref))

def unlike():
    video = Upload.query.filter_by(id=id).first()
    video.liked.remove(current_user)
    db.session.commit()

@app.route('/unlike/video=<int:id>')
@login_required
def unlike(id):
    video = Upload.query.filter_by(id=id).first()
    video.liked.remove(current_user)
    db.session.commit()
    return redirect(url_for('video',upload_ref=video.upload_ref))





@app.route('/create/<username>',methods=['GET','POST'])
@login_required
def create(username):
    user = User.query.filter_by(username=username).first_or_404()

    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    lesson_form = Lesson_form()
    form = Session_form()
    verify_form = Verify_form()
    if request.method =='POST':
        time = request.form['date-time']
        end_time = request.form['end-time']
        start = re.split(r'([T+])', time)
        end = re.split(r'([T+])', end_time)
        post = Post(title=form.title.data,category=form.category.data,description=form.description.data,date= start[0],start_time= start[2] ,end_time = end[2], author=current_user)
        lesson = Lesson(title=request.form['title'],description=request.form['description'])
        verify = User(id_type = verify_form.id_type.data,id_number = verify_form.id_number.data,id_document = verify_form.id_document.data,
                     nationality = verify_form.nationality.data,occupation = verify_form.occupation.data,email = verify_form.email.data,phone = verify_form.phone.data)

        db.session.add(post,verify)



        print(session)
        db.session.commit()
        return redirect(url_for('lesson',username=current_user.username,id=post.id ))
    return render_template('CREATE1.html',user=user,user_role = user_role,form=form,verify_form=verify_form,lesson_form=lesson_form,image_file=image_file)



@app.route('/uploads/<username>',methods=['POST','GET'])
@login_required
def upload(username):
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    user = User.query.filter_by(username=username).first_or_404()
    form = Upload_form()
    if request.method == 'POST':
        random_hex = secrets.token_hex(8)
        file  = request.files['file']
        file_data  = request.files['file']
        _, f_ext = os.path.splitext(file.filename)
        file_hex = random_hex
        file_fn = random_hex + f_ext
        file.save(os.path.join(app.root_path, 'static/videos/discover videos', file_fn))
        path = os.path.join(file_fn)
        upload = Upload(title=form.title.data,description=form.description.data,category=form.category.data,price= form.price.data,upload_ref=path,uploader=current_user)
        db.session.add(upload)
        db.session.commit()


        print(file_hex)

 #       f.save(os.path.join(app.config['UPLOAD_FOLDER']+f))
        return redirect(url_for('discover',upload_ref=file_hex,username=current_user.username))
    return render_template('UPLOADS.html',user=user,user_role=user_role,form =form,image_file=image_file)


@app.route('/lesson<int:id><username>', methods=['POST','GET'])
@login_required
def lesson(username,id):
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)

    user = User.query.filter_by(username=username).first_or_404()
    form = Lesson_form()
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST':


        lesson = Lesson(title = request.form['title'],description = form.description.data,post_id=id,user_id=current_user.id)
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for('user_profile',username=current_user.username))



    return render_template('LESSON.html',user=user,post=post,form=form,image_file=image_file)

@app.route('/userview/<username>',methods=['GET','POST'])
@login_required
def userview(username):
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('USER_VIEW.html',user=user,all_users = all_users,user_role=user_role,image_file=image_file)





# Superadmin

@app.route('/superadminview',methods=['GET','POST'])
@login_required
def superview():
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('USER_VIEW.html',user=user,all_users = all_users,user_role=user_role,image_file=image_file)

#session role
@app.route('/session_admin/<int:id>',methods=['GET','POST'])
@login_required
def session_admin(id):
    user = User.query.filter_by(id=id).first_or_404()
    all_posts = Post.query.all()

    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('session_admin.html',user=user,all_users = all_users,all_posts=all_posts,user_role=user_role,image_file=image_file)

@app.route('/session_view/<int:id>',methods=['GET','POST'])
@login_required
def session_view(id):
    session_post = Post.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first_or_404()
    comments = Comment.query.all()
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('session_view.html',session_post=session_post,comments=comments,video=video,user=user,all_users = all_users,user_role=user_role,image_file=image_file)

@app.route('/session_verify/<int:id>',methods=['GET','POST'])
@login_required
def session_verify(id):
    session_post = Post.query.filter_by(id=id).first()
    session_post.verified = 1
    db.session.commit()

    return redirect(url_for('session_admin',id=session_post.id))

@app.route('/session_unverify/<int:id>',methods=['GET','POST'])
@login_required
def session_unverify(id):
    session_post = Post.query.filter_by(id=id).first()
    session_post.verified = 0
    db.session.commit()

    return redirect(url_for('session_admin',id=session_post.id))

@app.route('/video_admin/<int:id>',methods=['GET','POST'])
@login_required
def video_admin(id):
    user = User.query.filter_by(id=id).first_or_404()
    uploads  = Upload.query.all()
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('video_admin.html',uploads=uploads,user=user,all_users = all_users,user_role=user_role,image_file=image_file)

@app.route('/video/<upload_ref>',methods=['GET','POST'])
@login_required
def video_view(upload_ref):
    video = Upload.query.filter_by(upload_ref=upload_ref).first()
    user = User.query.all()
    comments = Comment.query.all()
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('video_view.html',comments=comments,video=video,user=user,all_users = all_users,user_role=user_role,image_file=image_file)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def video_admin_dashboard():
    total_videos = Upload.query.all()
    comments = Comment.query.all()
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    total_users = User.query.all()

    return render_template('video_admin_dashboard.html',comments=comments,total_videos=len(total_videos),user=user,total_users = len(total_users) ,image_file=image_file)

@app.route('/admin/payment/<int:id>',methods=['GET','POST'])
@login_required
def payment_admin():
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('Payment_admin.html',user=user,all_users = all_users,user_role=user_role,image_file=image_file)

@app.route('/admin/info_admin/<int:id>',methods=['GET','POST'])
@login_required
def info_admin():
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('Information_admin.html',user=user,all_users = all_users,user_role=user_role,image_file=image_file)

@app.route('/admin/badge/<int:id>',methods=['GET','POST'])
@login_required
def badge_admin():
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('Badge_admin.html',user=user,all_users = all_users,user_role=user_role,image_file=image_file)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Requset',
                  sender='cjohn222.jc@gmail.com',
                  recipients=[user.email])
    msg.body = f'''THIS IS A TEST
    {url_for('reset_token',token=token,_external=True)}

    '''
    mail.send(msg)


@app.route('/reset_password' , methods=['POST','GET'])
def reset_request():
    form = Request_reset(request.form)
    if  request.method == 'POST':
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to your mail')
    return render_template('request_reset.html', form =form)

@app.route('/reset_password/<token>' , methods=['POST','GET'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form = Reset_password()
    if form.validate_on_submit() and request.method == "POST":

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Updated')

        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
