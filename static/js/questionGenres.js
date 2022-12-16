
//const axios = require('axios');


/** GENRES */
var blocksgenre = document.getElementsByClassName('block_genres');
for(var i = 0; i < blocksgenre.length; i++) {
    blocksgenre[i].onclick = function() {
        if(this.classList.contains('block_genresgrab')){
            this.className = "block_genres";
        }else{
            this.className += "grab";
            
        }};

}
    

function sendListGenres(){
    var listeGenres = [];
    var liste = document.getElementsByClassName('block_genresgrab');

    
    for(var i = 0; i < liste.length; i++) {
       
        listeGenres.push(liste[i].getAttribute("data-value"));
        
    }

    return(listeGenres);
    /*
   $.ajax({
        url: "",
        type:"get",
        contentType: "application/json",
        data: {
            listeGenres
        },
        success: function(response){
            console.log("ok");
        }




   })*/
 


  



}

/** ACTORS */

var blocksactors = document.getElementsByClassName('block_actors');
for(var i = 0; i < blocksactors.length; i++) {
    blocksactors[i].onclick = function() {
        if(this.classList.contains('block_actorsgrab')){
            this.className = "block_actors";
        }else{
            this.className += "grab";
            
        }};

}
function sendListActors(){
    var listeGenres = [];
    var liste = document.getElementsByClassName('block_actorsgrab');
   
    
    for(var i = 0; i < liste.length; i++) {
       
        listeGenres.push(liste[i].getAttribute("data-value"));
        
    }
    return(listeGenres);


 


  



}


/** DIRECTORS */

var blocksdirectors = document.getElementsByClassName('block_directors');
for(var i = 0; i < blocksdirectors.length; i++) {
    blocksdirectors[i].onclick = function() {
        if(this.classList.contains('block_directorsgrab')){
            this.className = "block_directors";
        }else{
            this.className += "grab";
            
        }};

}
function sendListDirectors(){
    var listeGenres = [];
    var liste = document.getElementsByClassName('block_directorsgrab');

    
    for(var i = 0; i < liste.length; i++) {
       
        listeGenres.push(liste[i].getAttribute("data-value"));
        
    }

    return(listeGenres);

 


  



}


/** MOVIES */

var blocksfilms = document.getElementsByClassName('block_films');
for(var i = 0; i < blocksfilms.length; i++) {
    blocksfilms[i].onclick = function() {
        if(this.classList.contains('block_filmsgrab')){
            this.className = "block_films";
        }else{
            this.className += "grab";
            
        }};

}
function sendListFilms(){
    var listeGenres = [];
    var liste = document.getElementsByClassName('block_filmsgrab');
    
    
    for(var i = 0; i < liste.length; i++) {
       
        listeGenres.push(liste[i].getAttribute("data-value"));
        
    }
    return(listeGenres);


 


  



}




function send(){


    var genres = sendListGenres();
    var actors = sendListActors();
    var directors = sendListDirectors();
    var films = sendListFilms();

    var tab=[genres,actors,directors,films]


    //for(var i = 0; i < liste.length; i++) {

      //  listeGenres.push(liste[i].getAttribute("data-value"));

    //}
    lien='/question?type_film='+genres+'&film_linked='+films+'&actor='+actors+'&realisator='+directors+''
    window.location=lien;
  }

