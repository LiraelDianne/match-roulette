from ..login_reg.models import Gender, User
from .models import UserAnswer

def findMatch(mostrecent, queue):
    #gets a list of sessions
    #if anyone matches above 0 on my 25 to -25 rating system,
    #returns that user's session
    threshold = 20
    #sets a rating above which you want a connection
    while threshold >= 0:
        match = checkMatch(mostrecent, queue, threshold)
        if match:
            return match
        else:
            threshold -= 5
    return None


def checkMatch(mostrecent, queue, threshold):
    #checks the first 200 users and returns a user if a match is found
    limiter = 200
    for session in queue:
        if limiter == 0:
            break
        limiter -= 1
        user = User.objects.get(id=session['id'])
        if compare(mostrecent, user) > threshold:
            return session
    return False

def compare(user, match):
    #gets two orm user objects
    rating = 0
    #lists of the user answers for both those users
    useranswers = UserAnswer.objects.filter(answerer=user)
    matchanswers = UserAnswer.objects.filter(answerer=match)
    for answer in useranswers:
        #find the same question in both lists
        #if we have optional questions, there won't always be a matching one
        matchanswer = matchanswers.get(question=answer.question)
        # increase the rating if the answer is the same, decrease if not
        if answer.answer == matchanswer.answer:
            rating += answer.importance
        else:
            rating -= importance
    return rating

