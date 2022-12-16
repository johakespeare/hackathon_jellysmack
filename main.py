from flask import Flask , request , render_template , session , redirect , url_for
import json
from recommender import Recommender
import time
import random





app = Flask(__name__)
app=Flask(__name__,template_folder='templates')
app.secret_key = "any random string"

def Session():
    return 'username' in session

@app.route('/',methods=['GET', 'POST'])
def index():
    if Session():
        # dic_film_algo=
        rcm = Recommender()
        with open('bdd.json') as mon_fichier :
            data = json.load(mon_fichier)
        words_dict = [{'keywords' : ['knight' , 'tank' , 'war'] , 'cast' : ['garyoldman' , 'johhnydepp'] ,
                       'director' : ['stanleykubrick' , 'stevenspielberg'] , 'genres' : ['action']}]
        words_dict =[{'keywords':['knight','tank','war'],'cast':data["login"][session['indice']]["actor"],'director':data["login"][session['indice']]["realisator"],'genres':data["login"][session['indice']]["type_of_movie"]}]

        #### GET RECOMMANDATION FROM PROFILE ####
        films_from_profile = rcm.recommendation_from_profile(words_dict , 10)

        film_rand = random.choice(data["login"][session['indice']]["film_liked"])
        films_from_film = rcm.recommendation_from_movie(film_rand , 5)

        film_name = films_from_film[1]["title"]
        film_name = []
        for n in range(len(films_from_film)) :
            film_name.append(films_from_film[n]["title"])



        by_caste = rcm.recommendation_naive(10 , filters_to_apply=['cast' , data["login"][session['indice']]["actor"]])
        by_directore=rcm.recommendation_naive(10 , filters_to_apply=['director' , data["login"][session['indice']]["realisator"]])
        by_cast=[]
        by_director=[]
        for n in range(len( by_caste)) :
            by_cast.append( by_caste[n]["title"])
        for n in range(len(by_directore)) :
                by_director.append(by_directore[n]["title"])





        #by_director = rcm.recommendation_naive(10 ,filters_to_apply=['director' , data["login"][session['indice']]["realisator"]])
        #by_cast = rcm.recommendation_naive(10 ,filters_to_apply=['cast' , data["login"][session['indice']]["actor"]])



        a = len(film_name)

        c= len( by_director)
        d=len(by_cast)
        by_genre=""

        # film_realisator=films_from_film[0]["c"]

        return render_template('home.html' , film_name=film_name ,by_director=by_director,by_cast=by_cast,a=a,c=c,d=d)

    else:
        return redirect(url_for('login'))




@app.route('/login', methods=['GET', 'POST'])
def login():

    erreur=''
    if request.method == 'POST':

        login = request.form.get('username')
        password = request.form.get('password')

        with open('bdd.json') as mon_fichier :
            data = json.load(mon_fichier)

        for n in range(len(data["login"])) :
            if login == data["login"][n]["username"] and password == data["login"][n]["password"]  :
                session['username'] = request.form['username']
                session['indice'] =data["login"][n]["id"]

                return redirect(url_for('index'))

    return render_template('login.html',erreur='')

@app.route('/create_account',methods=['GET', 'POST'])
def creationAccount():
    msg = ''
    if request.method == 'POST' :
        with open('bdd.json') as mon_fichier :
            data = json.load(mon_fichier)

        login = request.form.get('username')
        password = request.form.get('password')
        confirm_password=request.form.get('confirm_password')

        if  login != None and password != None   :

            no_in_bdd=True
            for n in range(len(data["login"])):

                if login==data["login"][n]["username"] :
                    msg="Username deja pris veuillez mettre un autre"
                    no_in_bdd = False
            if  no_in_bdd==True:

                    data["login"].append({"id":len(data["login"]),"username":login,"password":password,"type_of_movie":[],"actor":[],"film_liked":[],"realisator":[]})
                    with open('bdd.json','w') as mon_fichier :
                        json.dump(data , mon_fichier)
                    session['username'] = request.form['username']
                    session['indice'] = data["login"][n]["id"]



            return redirect('/question')

    return render_template('sign-up.html',msg=msg)

@app.route('/profil')
def profil():
    if Session():

        username=session["username"]
        return render_template('profil.html',username=username)
    else :
        return redirect('/login')

@app.route('/question',methods=['GET', 'POST'])
def question():
    if Session():

        list_of_type_of_film = request.args.get('type_film')

        list_film_linked = request.args.get('film_linked')
        list_actor = request.args.get('actor')
        list_realisator = request.args.get('realisator')
        list_of_type_of_film = request.args.get('type_film')





        if list_of_type_of_film != None or list_actor!= None or list_realisator != None or list_of_type_of_film!=None :

            list_of_type_of_film = list_of_type_of_film.split(",")
            list_actor= list_actor.split(",")
            list_realisator=list_realisator.split(",")
            list_film_linked=list_film_linked.split(",")
            session['indice']=session['indice']+1


            with open('bdd.json') as mon_fichier :
                data = json.load(mon_fichier)

            list_film_type = data["login"][session['indice']]["type_of_movie"]
            list_film_actor = data["login"][session['indice']]["actor"]
            list_film_liked = data["login"][session['indice']]["film_liked"]

            list_film_realisator = data["login"][session['indice']]["realisator"]


            for n in range(len(list_of_type_of_film)) :
                list_film_type.append(list_of_type_of_film[n])
            for n in range(len(list_actor)) :
                list_film_actor.append(list_actor[n])
            for n in range(len(list_film_linked)) :
                list_film_liked.append(list_film_linked[n])
            for n in range(len(list_realisator)) :
                list_film_realisator.append(list_realisator[n])


            with open('bdd.json' , 'w') as mon_fichier :
                json.dump(data , mon_fichier)
            return redirect('/')

        return render_template('questions.html')
    else :
        return redirect('/login')




@app.route('/type_of_film',methods=['GET', 'POST'])
def genre():
    if Session():
        #list_of_type_of_film = request.form.get('type_of_film')
        list_of_type_of_film=['Action', 'Adventure', 'Fantasy', 'Science Fiction']
        with open('bdd.json') as mon_fichier :
            data = json.load(mon_fichier)
        list_film = data["login"][session['indice']]["type_of_movie"]
        for n in range(len(list_of_type_of_film)):
         list_film.append(list_of_type_of_film[n])

        with open('bdd.json' , 'w') as mon_fichier :
            json.dump(data , mon_fichier)
        return render_template('questionGenres.html')

    else :
        return redirect('/login')
@app.route('/actor',methods=['GET', 'POST'])
def actor():
    #list_actor=request.form.get('actor')
    list_actor=["acteur1","acteur2"]
    if Session() :
        with open('bdd.json') as mon_fichier :
            data = json.load(mon_fichier)
        list_film = data["login"][session['indice']]["actor"]
        for n in range(len(list_actor)):
         list_film.append(list_actor[n])

        with open('bdd.json' , 'w') as mon_fichier :
            json.dump(data , mon_fichier)
        return render_template('questionActeurs.html')
    else :
        return redirect('/login')

@app.route('/film_liked',methods=['GET', 'POST'])
def film_liked():
    #list_film_linked=request.form.get('film_liked')
    list_film_linked =["Superman","Batman","Aquaman"]

    if Session():
        with open('bdd.json') as mon_fichier :
            data = json.load(mon_fichier)
        list_film = data["login"][session['indice']]["film_liked"]
        for n in range(len(list_film_linked)):
         list_film.append(list_film_linked[n])

        with open('bdd.json' , 'w') as mon_fichier :
            json.dump(data , mon_fichier)

        return render_template('questionFilms.html')
    else :
        return redirect('/login')

@app.route('/my_list')
def my_list():

    with open('bdd.json') as mon_fichier :
        data = json.load(mon_fichier)
    if Session():
        list_film = data["login"][session["indice"]]["film_liked"]
        return render_template('create_account.html',msg=list_film)
    else :
        return redirect('/login')
@app.route('/all_films')
def all_film():
    if Session():
        return render_template('profil.html')

    else :
        return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

