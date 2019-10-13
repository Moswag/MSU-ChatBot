import bcrypt

from django.shortcuts import render, render_to_response, HttpResponse, redirect
from django.http import HttpResponse
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from chatterbot import ChatBot

from msu.models import User, Student, Program, Module, Lecturer, Admin

chatbot = ChatBot(
	'Ron Obvious',
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)


# Train based on the english corpus

# Already trained and it's supposed to be persistent
# chatbot.train("chatterbot.corpus.english")

@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		message = data['message']

		chat_response = chatbot.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
		content_type="application/json"
	)


def home(request, template_name="home.html"):
	user = User.objects.get(id=request.session['id'])
	context = {
		"user": user,
	}
	return render_to_response(template_name, context)


def login(request):
	return render(request, 'login.html')

def logout_view(request):
	logout(request)
	messages.add_message(request,messages.INFO,"Successfully logged out")
	return redirect(login)

def signin(request):
	if (User.objects.filter(email=request.POST['email']).exists()):
		user = User.objects.filter(email=request.POST['email'])[0]

		if (bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
			request.session['id'] = user.id
			request.session['first_name'] = user.first_name
			request.session['last_name'] = user.last_name
			request.session['email'] = user.email
			request.session['role'] = user.role

			messages.add_message(request,messages.INFO,'Welcome to MSU Chat Bot Assistant '+ user.first_name+' '+user.last_name)
			if user.role=='admin':
				return redirect(dashboard)
			elif user.role=='student':
				return redirect(home)
			else:
				return redirect(dashboard)

		else:
			messages.error(request, 'Oops, Wrong password, please try a diffrerent one')
			return redirect('/')
	else:
		messages.error(request, 'Oops, That email or reg number do not exist')
		return redirect('/')


def dashboard(request):
	user = User.objects.get(id=request.session['id'])
	context = {
		"user": user
	}
	return render(request, 'admin/dashboard.html', context)


#----------------STUDENT-----------------------

def addStudent(request):
	programs = Program.objects.all()
	context = {
		"programs": programs
	}
	return render(request, 'admin/add_student.html', context)

def saveStudent(request):
	if request.method == 'POST':
		myProgram = User.objects.filter(email=request.POST["reg_number"])
		if myProgram.exists():
			messages.error(request, "Student with that Reg Number already exists")
			return redirect(addProgram)
		else:
			hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

			student = Student.objects.create(
				name=request.POST['first_name'] +' '+ request.POST['last_name'],
				reg_number=request.POST['reg_number'],
				program=request.POST['program'],
				level=request.POST['level'],
				status='Active'
			)
			student.save()
			user = User.objects.create(
				first_name=request.POST['first_name'],
				last_name=request.POST['last_name'],
				email=request.POST['reg_number'],
				role='student',
				password=hashed_password
			)
			user.save()
			messages.add_message(request, messages.INFO, 'User successfully added')
			return redirect(viewStudents)




def viewStudents(request):
	students = Student.objects.all()
	context = {
		"students": students
	}
	return render(request, 'admin/view_students.html', context)



def viewUsers(request):
	students = Student.objects.all()
	context = {
		"students": students
	}
	return render(request, 'admin/view_students.html', context)


#-------------------Program-----------------------

def addProgram(request):
	return render(request, 'admin/add_program.html')

def saveProgram(request):
	if request.method == 'POST':
		myProgram = Program.objects.filter(name=request.POST["name"])
		if myProgram.exists():
			messages.error(request, "Program with that Name already exists")
			return redirect(addProgram)
		else:
			program = Program.objects.create(
				name=request.POST["name"],
				description=request.POST["description"],
				status="Free"
			)
			program.save()
			messages.add_message(request, messages.INFO, "Program successfully added")
			return redirect(viewPrograms)

def viewPrograms(request):
	programs = Program.objects.all()
	context = {
		"programs": programs
	}
	return render(request, 'admin/view_programs.html', context)



def editProgram(request, program_id):
	program = Program.objects.filter(pk=program_id).get()
	context = {
		"program": program
	}
	return render(request, 'admin/edit_program.html', context)


def deleteProgram(request, program_id):
	program = Program.objects.filter(pk=program_id).delete()
	messages.add_message(request, messages.INFO, 'Program successfully deleted')
	return redirect(viewPrograms)

#--------------Modules-------------------------
def addModule(request):
	programs = Program.objects.all()
	context = {
		"programs": programs
	}
	return render(request, 'admin/add_module.html', context)

def saveModule(request):
	if request.method == 'POST':
		myModule = Module.objects.filter(code=request.POST["code"])
		if myModule.exists():
			messages.error(request, "Module with that code already exists")
			return redirect(addProgram)
		else:
			module = Module.objects.create(
				name=request.POST['name'] ,
				code=request.POST['code'],
				program=request.POST['program'],
				level=request.POST['level'],
				status='Active'
			)
			module.save()

			messages.add_message(request, messages.INFO, 'Module successfully added')
			return redirect(viewModules)

def viewModules(request):
	modules = Module.objects.all()
	context = {
		"modules": modules
	}
	return render(request, 'admin/view_modules.html', context)



#--------------Lecturers-------------------------
def addLecturer(request):
	modules = Module.objects.all()
	context = {
		"modules": modules
	}
	return render(request, 'admin/add_lecturer.html', context)





def saveLecturer(request):
	if request.method == 'POST':
		kaUser = User.objects.filter(email=request.POST["email"])
		if kaUser.exists():
			messages.error(request, "User with that email already exists")
			return redirect(addLecturer)
		else:
			hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

			lecturer = Lecturer.objects.create(
				name=request.POST['first_name'] +' '+ request.POST['last_name'],
				email=request.POST['email'],
				national_id=request.POST['national_id'],
				module=request.POST['module'],
				status='Active'
			)
			lecturer.save()
			user = User.objects.create(
				first_name=request.POST['first_name'],
				last_name=request.POST['last_name'],
				email=request.POST['email'],
				role='lecturer',
				password=hashed_password)
			user.save()
			messages.add_message(request, messages.INFO, 'Lecturer successfully added')
			return redirect(viewLecturers)


def viewLecturers(request):
	lecturers = Lecturer.objects.all()
	context = {
		"lecturers": lecturers
	}
	return render(request, 'admin/view_lecturers.html', context)



#--------------Admin-------------------------

def addAdmin(request):
	return render(request, 'admin/add_admin.html')

def saveAdmin(request):
	if request.method == 'POST':
		kaUser = User.objects.filter(email=request.POST["email"])
		if kaUser.exists():
			messages.error(request, "User with that email already exists")
			return redirect(addLecturer)
		else:
			hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

			admin = Admin.objects.create(
				name=request.POST['first_name'] +' '+ request.POST['last_name'],
				email=request.POST['email'],
				national_id=request.POST['national_id'],
				address=request.POST['address'],
				status='Active'
			)
			admin.save()
			user = User.objects.create(
				first_name=request.POST['first_name'],
				last_name=request.POST['last_name'],
				email=request.POST['email'],
				role='admin',
				password=hashed_password)
			user.save()
			messages.add_message(request, messages.INFO, 'Admin successfully added')
			return redirect(viewAdmins)


def viewAdmins(request):
	admins = Admin.objects.all()
	context = {
		"admins": admins
	}
	return render(request, 'admin/view_admins.html', context)






