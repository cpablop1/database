'use strict'


function imprimirCheque() {
    var imprime = document.getElementById('cheque').innerHTML;
    //encabezado de la pagina ALTA VERAPAZ
    const titulo = document.querySelector('#header');
    titulo.style.display = 'none';

    //ocultar titulo2
    const titulo2 = document.getElementById('padd');
    titulo2.style.display = 'none';

    //ocultar navegacion
    const privado = document.getElementById('ocultar');
    //ocultar boton
    privado.style.display = 'none';

    //ocular boton1 
    const btns = document.querySelector('.enviar');
    btns.style.display = 'none';

    const btns1 = document.querySelector('.enviar2');
    btns1.style.display = 'none';

    //ocultar el footer
    const abajo = document.querySelector('#foter');
    abajo.style.display = 'none';

    document.getElementById('cheque').innerHTML;

    window.print();

}

setTimeout(function volver() {
    const titulo = document.querySelector('#header');
    titulo.style.display = 'block';

    //ocultar titulo2
    const titulo2 = document.getElementById('padd');
    titulo2.style.display = 'block';

    //ocultar navegacion
    const privado = document.getElementById('ocultar');
    //ocultar boton
    privado.style.display = 'block';

    //ocular boton1 
    const btns = document.querySelector('.enviar');
    btns.style.display = 'block';

    const btns1 = document.querySelector('.enviar2');
    btns1.style.display = 'block';

    //ocultar el footer
    const abajo = document.querySelector('#foter');
    abajo.style.display = 'block';
}, 21000);




