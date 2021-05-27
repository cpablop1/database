'use strict'


console.log("Genial")


const btn_login = document.querySelector('nav.navegacion>a.logeo ');

btn_login.addEventListener('click', () => {
    console.log("Logeando")

    //Generando el Login
    const ventana = document.createElement('DIV');
    const titulo2 = document.createElement('H2');
    titulo2.textContent = "Iniciar Sesion";


    const texto1 = document.createElement('LABEL');
    texto1.textContent = 'Nombre';

    const inputtext = document.createElement('INPUT');
    inputtext.placeholder = "Escriba su nombre"


    const clave1 = document.createElement('LABEL');
    clave1.textContent = 'Clave';

    const inputtext2 = document.createElement('INPUT');
    inputtext2.type = "password"

    ventana.classList.add('login-box');
    ventana.appendChild(titulo2);
    ventana.appendChild(texto1);
    ventana.appendChild(inputtext);
    ventana.appendChild(clave1);
    ventana.appendChild(inputtext2);


    //Agregarlo al documento
    const navegacion = document.querySelector('.contenido-hero');
    navegacion.appendChild(ventana)


});