'use stric'

var nombre, apellido, celular, direccion, correo, asunto, msj;


// guardar_datos();
obtener_localstorange();



function obtener_localstorange() {

    let nombre = localStorage.setItem("nombre");
    console.log(nombre)

}

function guardar_datos() {
    let persona = {
        usuario: nombre,
        apellido: apellido,
        tel: celular,
        vivienda: direccion,
        correo: correo,
        Asunto: asunto,
        mensaje: msj

    };

    let personita = "Chicos";

    localStorage.setItem("solouno", personita)
    localStorage.setItem("Datos De Usuario", JSON.stringify(persona));

}