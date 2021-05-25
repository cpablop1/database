'use strict'

const datos = {
    nombre: '',
    apellido: '',
    celular: '',
    direccion: '',
    correo: '',
    mensaje: ''
}

const nombre = document.querySelector("#name");
const apellido = document.querySelector("#lastname");
const celular = document.querySelector("#numero");
const direccion = document.querySelector("#lugar");
const correo = document.querySelector("#correo");
const mensaje = document.querySelector("#text1");

const formulario = document.querySelector('.formulario');

nombre.addEventListener('input', llerTexto);
apellido.addEventListener('input', llerTexto);
celular.addEventListener('input', llerTexto);
direccion.addEventListener('input', llerTexto);
correo.addEventListener('input', llerTexto);
mensaje.addEventListener('input', llerTexto);

formulario.addEventListener('submit', (evento) => {


    evento.preventDefault();

    const { nombre, apellido, celular, direccion, correo, mensaje } = datos;
    if (nombre === '' ||
        apellido === '' ||
        celular === '' ||
        direccion === '' ||
        correo === '' ||
        mensaje === ''
    ) {
        alert("Todos los campos son obligatorios")
        return;
    }
    console.log('Enviado')
});


function llerTexto(e) {
    datos[event.target.id] = e.target.value;

    console.log(datos);
}

