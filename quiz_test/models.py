from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = '1_Categories'
        
    def __str__(self):
        return self.title


class Quiz(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='quiz_test', null=True, blank=True)
    description = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quizzes'
        verbose_name = 'Quiz'
        verbose_name_plural = '2_Quizzes'
        ordering = ['create_date', ]
            
    def __str__(self):
        return self.name
        
        
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    label = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['create_date', ]
        verbose_name_plural = '3_Questions'
        
    def __str__(self):
        return self.label
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField()
    
    def __str__(self):
        return self.text
    
    
class QuizTaker(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    finish_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = '4_Quiz Takers'
    
    def __str__(self):
        return self.user.username
