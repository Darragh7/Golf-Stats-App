from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,RadioField,DateField,PasswordField
from wtforms.validators import InputRequired , EqualTo

class RegistrationForm(FlaskForm):
    user_id= StringField("New User id:",
                         validators=[InputRequired()])
    password=PasswordField("Enter New Password",
                           validators=[InputRequired()])
    password2=PasswordField("Re-enter New Password",
                           validators=[InputRequired(),EqualTo('password')],)
    submit=SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id= StringField("User id:",
                         validators=[InputRequired()])
    password=PasswordField("Enter Password",
                           validators=[InputRequired()])
    submit=SubmitField("Submit")



class EnterRound(FlaskForm):
    name=RadioField("Pick a course from one of the following",
                      choices=['Blarney','Lee Valley','Cork','Douglas','Mahon','Muskerry','Monkestown','Raffeen Creek','Fota Island Resort'],
                      validators=[InputRequired()])
    score=IntegerField("Enter Score :",
                       validators=[InputRequired()])
    puttStat1=IntegerField("Putts Per Round :",
                       validators=[InputRequired()])
    puttStat2=IntegerField("One-Putt Percentage :",
                       validators=[InputRequired()])
    puttStat3=IntegerField("3-Putt Avoidance :",
                       validators=[InputRequired()])
    puttStat4=IntegerField("Average Distance Of Putts Made :",
                       validators=[InputRequired()])
    date=DateField("Enter date round was played:",
                       validators=[InputRequired()])
    add_round=SubmitField("Add Round:")

class ViewStats(FlaskForm):
    start_date_one=DateField("Enter start date:",
                         validators=[InputRequired()])
    end_date_one=DateField("Enter end date:",
                       validators=[InputRequired()])
    see_stats=SubmitField("See Stats:")

class ViewHistory(FlaskForm):
    start_date=DateField("Enter start date:",
                         validators=[InputRequired()])
    end_date=DateField("Enter end date:",
                       validators=[InputRequired()])
    see_rounds=SubmitField("See Rounds:")

class Leaderboard(FlaskForm):
    name =RadioField("View a leaderboard from one of the following courses:",
                      choices=['Blarney','Lee Valley','Cork','Douglas','Mahon','Muskerry','Monkestown','Raffeen Creek','Fota Island Resort'],
                      validators=[InputRequired()])
    view_leaderboard=SubmitField("View Leaderboard:")
    
class DeleteRounds(FlaskForm):
    dateDelete = DateField("Select the Date of the Round to Delete:", 
                     validators=[InputRequired()])
    delete_round = SubmitField("Delete Round")

class UpdateRounds(FlaskForm):
    dateSelect = DateField("Select the Date of the Round to Update:", 
                     validators=[InputRequired()])
    newScore = IntegerField("Enter New Score :",
                       validators=[InputRequired()])
    newPuttStat1=IntegerField("New Number Of Putts Per Round :",
                       validators=[InputRequired()])
    newPuttStat2=IntegerField("New One-Putt Percentage :",
                       validators=[InputRequired()])
    newPuttStat3=IntegerField("New 3-Putt Avoidance :",
                       validators=[InputRequired()])
    newPuttStat4=IntegerField("New Average Distance Of Putts Made :",
                       validators=[InputRequired()])
    update_round = SubmitField("Update Round")