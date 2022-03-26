from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from Quizker.forms import QuizForm,TrueOrFalseForm,OpenEndedForm,MultipleChoiceForm,ChoiceForm
from .models import Quiz,Question,Choice,MultipleChoice,TrueOrFalse,OpenEnded,QuizAttempt,Category,Profile,User
from django.shortcuts import redirect,reverse
from django.urls import reverse 
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import datetime
from django.template.defaultfilters import slugify 
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

def Home(request):
    return render(request, 'Quizker/Home.html',context={'Quizzes':Quiz.objects.all().order_by('-likes')[:5]})

@login_required
def CreateQuiz(request):
     form = QuizForm()
     user = request.user
     if request.method == 'POST':
          form = QuizForm(request.POST)
          if form.is_valid():
               quiz = form.save(commit=False)
               quiz.date = datetime.date.today()
               quiz.creator = request.user
               quiz.likes = 0 
               quiz.save()

               user.profile.nrOfQuizzesCreated += 1
               user.save()

               return redirect(reverse("Quizker:CreateQuestion" ,kwargs={'quiz_title_slug':quiz.slug,}))
              
          else:
               print(form.errors)
          
     return render(request, 'Quizker/CreateQuiz.html',context={'form':form,'numberofquizzes':((Quiz.objects.filter(creator=request.user).count())+1)})

@login_required
def CreateQuestion(request,quiz_title_slug):
          quiz = Quiz.objects.get(slug=quiz_title_slug)
          if quiz.creator!=request.user:
               return redirect('/Quizker/')
          questionType = quiz.questionType
          print(questionType)
          if questionType=="OpenEnded":
             form = OpenEndedForm
          elif questionType =="TrueOrFalse":
             form = TrueOrFalseForm
          else: 
             form = MultipleChoiceForm
          if request.method == 'POST':
             completedForm = form(request.POST)
             if completedForm.is_valid():
               Q = completedForm.save(commit=False)
               Q.quiz = Quiz.objects.get(slug=quiz_title_slug)
               if 'image' in request.FILES:
                    Q.image = request.FILES['image']
               Q.save()
             if questionType=='MultipleChoice':
                return redirect(reverse('Quizker:CreateChoice',kwargs={'question_id':Q.id}))
             else:
               print(completedForm.errors)
        
          return render(request, 'Quizker/CreateQuestion.html',context={'form':form(),'Quiz':quiz,'Questions':Question.objects.filter(quiz=quiz)}) 
     
@login_required
def CreateChoice(request, question_id):
        
        if request.method == 'POST':
          form = ChoiceForm(request.POST)
          
          
          if form.is_valid():
               C = form.save(commit=False)
               C.question = MultipleChoice.objects.get(id = int(question_id))
               if C.question.correct():
                  C.correct = False
               C.save()
          else:
               print(form.errors)
        context_dict ={}
        context_dict['Choices'] = Choice.objects.filter(question=MultipleChoice.objects.get(id=question_id))
        context_dict['question'] = MultipleChoice.objects.get(id=question_id)
        print(context_dict['question'].correct())
        context_dict['form'] = ChoiceForm()
        return render(request, 'Quizker/CreateChoice.html',context_dict)
 
def Quizzes(request):
    return render(request, 'Quizker/Quizzes.html',context={'Quizzes':Quiz.objects.all().order_by('-date')})

@login_required 
def ParticipateQuiz(request, quiz_title_slug):
    quiz = Quiz.objects.get(slug=quiz_title_slug)
    if Question.objects.filter(quiz=quiz).count()==0:
       Quiz.objects.get(slug=quiz_title_slug).delete()
       return redirect('/Quizker/')
       
    quizAttempt = QuizAttempt.objects.get_or_create(quiz=quiz,user=request.user)[0]
    if (quizAttempt.questionsCompleted  == Question.objects.filter(quiz=quiz).count()):
                   return redirect(reverse('Quizker:Results',kwargs={'quiz_title_slug':quiz_title_slug}))    
    context_dict ={"Quiz":quiz}
    quizType = quiz.questionType
    
    if (quizType=="TrueOrFalse"):
        QList = list(TrueOrFalse.objects.filter(quiz=quiz))
    elif(quizType=="MultipleChoice"):
        QList = list(MultipleChoice.objects.filter(quiz=quiz))
    else:
        QList = list(OpenEnded.objects.filter(quiz=quiz))
    context_dict[quizType] = True    
    if request.method == "POST" :
          answeredQuestion = QList[quizAttempt.questionsCompleted]
          answer = request.POST.get('answer', None)  
          if answer!=None:          
           
           if (quizType=="TrueOrFalse"):
              if (answer=="True"):
                  correct =  answeredQuestion.answer ==True
              else:
                  correct =  answeredQuestion.answer == False
           elif (quizType=="MultipleChoice"):
              if (answer=="True"):
                  correct =  True
              else:
                  correct =  False
           else:
              correct = answeredQuestion.correctAnswer(answer)
           quizAttempt.questionsCompleted+=1
           quizAttempt.save()
           if correct: 
              quizAttempt = QuizAttempt.objects.get(quiz=quiz,user=request.user)
              quizAttempt.score += 1 
              quizAttempt.save()
              context_dict['correct'] = "Well done you got it right!"
           else:
              context_dict['correct'] = "Oh no, you got it wrong!!"
           if (quizAttempt.questionsCompleted  == Question.objects.filter(quiz=quiz).count()):
                   return redirect(reverse('Quizker:Results',kwargs={'quiz_title_slug':quiz_title_slug}))      
          
    if (quizType=="MultipleChoice"):
        context_dict['Choices'] = Choice.objects.filter(question = QList[quizAttempt.questionsCompleted]) 
    context_dict['Question'] = QList[quizAttempt.questionsCompleted]
    context_dict['quizAttempt'] = quizAttempt
    context_dict['QuestionNumber'] = quizAttempt.questionsCompleted + 1 

    
  
    return render(request,'Quizker/ParticipateQuiz.html',context=context_dict)

@login_required
def Results(request,quiz_title_slug):
    user = request.user
    quiz = Quiz.objects.get(slug=quiz_title_slug)
    quizAttempt = QuizAttempt.objects.get(quiz=quiz,user=user)

    user.profile.score += quizAttempt.score
    user.profile.nrOfQuizzesCompleted += 1
    user.save()

    context_dict ={}
    context_dict['NoQuestions'] = Question.objects.filter(quiz=quiz).count()
    context_dict['score'] = quizAttempt.score
    context_dict['quiz'] = quiz
    context_dict['QuizAttempts'] = QuizAttempt.objects.filter(quiz=quiz).order_by('-score')[:5]

    return render(request,'Quizker/Results.html',context_dict)

@login_required
def FinishQuiz(request,quiz_title_slug):
    quiz = Quiz.objects.get(slug=quiz_title_slug)
    if Question.objects.filter(quiz=quiz).count()==0:
        Quiz.objects.get(slug=quiz_title_slug).delete()
    return redirect('/Quizker/')

@login_required          
def RemoveQuestion(request, quiz_id):
    quiz = Question.objects.get(id=quiz_id).quiz
    if quiz.creator!=request.user:
        return redirect('/Quizker/')
    Question.objects.get(id=quiz_id).delete()   
    return redirect(reverse("Quizker:CreateQuestion" ,kwargs={'quiz_title_slug':quiz.slug,}))

@login_required          
def RemoveChoice(request, choice_id):
    question = Choice.objects.get(id=choice_id).question
    if question.quiz.creator!=request.user:
        return redirect('/Quizker/')
    Choice.objects.get(id=choice_id).delete()   
    return redirect(reverse("Quizker:CreateChoice" ,kwargs={'question_id':question.id,}))

@login_required
def AddChoices(request, question_id):
    question = MultipleChoice.objects.get(id=question_id)
    if question.quiz.creator!=request.user:
        print("1")
        return redirect('/Quizker/')
    if Choice.objects.filter(question=question).count()<2:
       print("2")
       return redirect(reverse("Quizker:CreateChoice" ,kwargs={'question_id':question_id,}))
    if question.correct()==False:
        print("3")
        MultipleChoice.objects.get(id=question_id).delete()
    return redirect(reverse("Quizker:CreateQuestion" ,kwargs={'quiz_title_slug':question.quiz.slug,}))

@login_required
def LikeQuiz(request , quiz_title_slug):
        if request.method=="POST":
          quiz = Quiz.objects.get(slug=quiz_title_slug)
          quizAttempt = QuizAttempt.objects.get(quiz=quiz,user=request.user)
          if (quizAttempt.liked ==False):
                 quiz.likes += 1 
                 quizAttempt.liked = True
          else:
                 quiz.likes -= 1  
                 quizAttempt.liked = False
          quiz.save()     
          quizAttempt.save()
        return redirect(reverse('Quizker:Results',kwargs={'quiz_title_slug':quiz_title_slug}))

@login_required
def UserProfile(request):
    user = request.user
    context_dict = {}
    context_dict['Quizzes'] = Quiz.objects.filter(creator=user).order_by('-date')
    context_dict['User'] = user
    
    return render(request, 'Quizker/UserProfile.html',context=context_dict)

def Leaderboard(request):
    return render(request, 'Quizker/Leaderboard.html',context={'Users':Profile.objects.all().order_by('-score')})

def ContactUs(request):
    return render(request, 'Quizker/ContactUs.html')