import re

from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import login_required, current_user

from flaskApp.models import Post, db, Upload, User, Comment, Lesson
from flaskApp.posts.forms import Comment_form, Lesson_form

posts = Blueprint('posts',__name__)

def book(id):
    post=Post.query.filter_by(id=id).first()
    post.bookers.append(current_user)
    db.session.commit()
    return redirect(url_for('users.user_profile',username=current_user.username))


@posts.route('/book<int:id>/<choice>')
@login_required
def action(choice,id):
    return choice(id)


def unbook(id):
    post=Post.query.filter_by(id=id).first()
    post.bookers.remove(current_user)
    db.session.commit()

    return redirect(url_for('users.user_profile',username=current_user.username))


@posts.route('/post/<int:id>')
@login_required
def  post(id):
    post = Post.query.get_or404(id)
    return redirect(url_for('users.login'))

@posts.route('/videos/<upload_ref>' , methods=['POST','GET'])
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
        return redirect(url_for('posts.video',upload_ref=video.upload_ref))


    return render_template('VIDEO.html',comments = comments,video=video,uploads=uploads,user=user,form=form)



@posts.route('/lesson<int:id><username>', methods=['POST','GET'])
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
        return redirect(url_for('users.user_profile',username=current_user.username))



    return render_template('LESSON.html',user=user,post=post,form=form,image_file=image_file)


@posts.route('/video/<upload_ref>',methods=['GET','POST'])
@login_required
def video_view(upload_ref):
    video = Upload.query.filter_by(upload_ref=upload_ref).first()
    user = User.query.all()
    comments = Comment.query.all()
    image_file = url_for('static', filename ='profile_pics/' + current_user.image_file)
    user_role = current_user.role
    all_users = User.query.all()

    return render_template('video_view.html',comments=comments,video=video,user=user,all_users = all_users,user_role=user_role,image_file=image_file)


def time():
    date = Post.query.all()
    for time in date:
        start = time.start_time
        x = re.split(r'([T+])', start)