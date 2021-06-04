from django.contrib.messages.api import warning
from django.http import request
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

import data.rol as rol
import data.Usuario as user
import data.Proveedor as proveedor
import data.Cuenta_bancaria as cuenta_bancaria

import data.Contacto as Contacto


def Index(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    return render(request, 'inicio.html')

def CrearRolUsuario(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    dicccionario = {"nombre": "nombre",                   
                        "crud_users": 0,
                        "imprimir_cheque": 0,
                        "anular_cheque": 0,
                        "modificar_cheque": 0,
                        "reporte_cheque": 0,
                        "auditar_user": 0,
                        "admin_cuenta_banc": 0,
                        "auditar_cuenta": 0,
                        "mostrar_bitacora_user": 0,
                        "mostrar_bitacora_group": 0,
                        "mostrar_bitacora_jefe": 0,
                        "jefe": 0}
    if request.method == 'POST':
        nombre = request.POST['nombre_rol']
        permiso = request.POST.getlist('permiso',)
        if nombre.strip() != '':
            dicccionario['nombre'] = nombre
            if not permiso:
                messages.warning(request, 'Seleccione los permisos a conceder al usuario')
            else:
                for i in permiso:
                    dicccionario[i] = 1
                data = rol.Rol_permiso_sup()
                data.create(dicccionario)
                messages.success(request, 'Rol de usuario creado exitosamente')
        else:
            messages.warning(request, 'Ingrese nombre de rol')

    return render(request, 'admin/crear_rol_usuario.html')

def CrearRolGrupo(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    if request.method == 'POST':
        nombre_rol_grupo = request.POST['nombre_rol_grupo']
        monto_maximo = request.POST['monto_maximo']
        monto_minimo = request.POST['monto_minimo']
        if nombre_rol_grupo.strip() != '':
            if monto_maximo.strip() != '':
                if monto_minimo.strip() != '':
                    diccionario = {f"nombre" : nombre_rol_grupo, 
                                    "monto_min" : monto_minimo, 
                                    "monto_max": monto_maximo}
                    data = rol.Rol_grupo()
                    data.create(diccionario)
                    messages.success(request, 'Rol grupo creada exitosamente!!!')
                else:
                    messages.warning(request, 'Ingrese el monto mínimo para continuar')
            else:
                messages.warning(request, 'Ingrese el monto máximo para continuar')
        else:
            messages.warning(request, 'Ingrese un nombre de rol de grupo')
    return render(request, 'admin/crear_rol_grupo.html')

def MenuCrearUsuario(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    return render(request, 'admin/menu_crear_usuario.html')

def CrearUsuarioGrupo(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    valor = []
    dic = ''
    try:
        data = rol.Rol_grupo()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila['id_rol'])
            valor.append(fila['nombre'])
        dic = dict(zip(clave, valor))
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los roles!')

    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        apellido = request.POST['apellido']
        dpi = request.POST['dpi']
        direccion = request.POST['direccion']
        clave1 = request.POST['clave1']
        clave2 = request.POST['clave2']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        compania = request.POST['compania']
        pais = request.POST['pais']
        rolu = request.POST['rol']
        if nombre_usuario.strip() != '' and apellido.strip() != '':
            if dpi.strip() != '':
                if direccion.strip() != '':
                    if clave1.strip() != '' and clave2.strip() != '':
                        if clave1.strip() == clave2.strip():
                            if correo.strip() != '':
                                if telefono.strip() != '':
                                    if compania.strip() != '':
                                        if pais.strip() != '':
                                            if int(rolu) > 0:
                                                diccionario = {"nombre" : nombre_usuario,
                                                                "apellido" : apellido,
                                                                "DPI" : dpi,
                                                                "direccion" : direccion,
                                                                "id_rol" : rolu,
                                                                "clave" : clave1,
                                                                "correo" : correo,
                                                                "numero" : telefono,
                                                                "compania" : compania,
                                                                "pais" : pais}
                                                data = user.Usuario()
                                                try:
                                                    result = data.create(diccionario)
                                                    if result['id'] != 'Correo, ya existente':
                                                        if result['id'] != 'Numero de telefono, ya existente':
                                                            messages.success(request, 'Usuario creada correctamente!')
                                                        else:
                                                            messages.error(request, result['id'])
                                                    else:
                                                        messages.error(request, result['id'])
                                                except:
                                                    messages.error(request, 'Hubo un error al crear el usuario!')
                                            else:
                                                messages.warning(request, 'Seleccione un rol para el usuario.')
                                        else:
                                            messages.warning(request, 'Campo país está vacío.')
                                    else:
                                        messages.warning(request, 'Ingrese la companía al pertenece el teléfono.')
                                else:
                                    messages.warning(request, 'Campo teléfono está vacío.')
                            else:
                                messages.warning(request, 'Campo correo está vacío.')
                        else:
                            messages.warning(request, 'Las constraseñas no coinciden.')
                    else:
                        messages.warning(request, 'Los campos contraseñas están vacíos.')
                else:
                    messages.warning(request, 'Campo dirección está vacío.')
            else:
                messages.warning(request, 'Campo DPI está vacío.')
        else:
            messages.warning(request, 'Alguno de los campos de nombre y apellido están vacíos.')
    
    return render(request, 'admin/crear_usuario_grupo.html', {
        'dic': dic
    })

def CrearUsuarioSingular(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    valor = []
    dic = ''
    try:
        data = rol.Rol_permiso_sup()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila['id_rol'])
            valor.append(fila['nombre'])
        dic = dict(zip(clave, valor))
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los roles!')

    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        apellido = request.POST['apellido']
        dpi = request.POST['dpi']
        direccion = request.POST['direccion']
        clave1 = request.POST['clave1']
        clave2 = request.POST['clave2']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        compania = request.POST['compania']
        pais = request.POST['pais']
        rolu = request.POST['rol']
        if nombre_usuario.strip() != '' and apellido.strip() != '':
            if dpi.strip() != '':
                if direccion.strip() != '':
                    if clave1.strip() != '' and clave2.strip() != '':
                        if clave1.strip() == clave2.strip():
                            if correo.strip() != '':
                                if telefono.strip() != '':
                                    if compania.strip() != '':
                                        if pais.strip() != '':
                                            if int(rolu) > 0:
                                                diccionario = {"nombre" : nombre_usuario,
                                                                "apellido" : apellido,
                                                                "DPI" : dpi,
                                                                "direccion" : direccion,
                                                                "id_rol" : rolu,
                                                                "clave" : clave1,
                                                                "correo" : correo,
                                                                "numero" : telefono,
                                                                "compania" : compania,
                                                                "pais" : pais}
                                                data = user.Usuario()
                                                try:
                                                    result = data.create(diccionario)
                                                    if result['id'] != 'Correo, ya existente':
                                                        if result['id'] != 'Numero de telefono, ya existente':
                                                            messages.success(request, 'Usuario creada correctamente!')
                                                        else:
                                                            messages.error(request, result['id'])
                                                    else:
                                                        messages.error(request, result['id'])
                                                except:
                                                    messages.error(request, 'Hubo un error al crear el usuario!')
                                            else:
                                                messages.warning(request, 'Seleccione un rol para el usuario.')
                                        else:
                                            messages.warning(request, 'Campo país está vacío.')
                                    else:
                                        messages.warning(request, 'Ingrese la companía al pertenece el teléfono.')
                                else:
                                    messages.warning(request, 'Campo teléfono está vacío.')
                            else:
                                messages.warning(request, 'Campo correo está vacío.')
                        else:
                            messages.warning(request, 'Las constraseñas no coinciden.')
                    else:
                        messages.warning(request, 'Los campos contraseñas están vacíos.')
                else:
                    messages.warning(request, 'Campo dirección está vacío.')
            else:
                messages.warning(request, 'Campo DPI está vacío.')
        else:
            messages.warning(request, 'Alguno de los campos de nombre y apellido están vacíos.')
    
    return render(request, 'admin/crear_usuario_singular.html', {
        'dic': dic
    })

def VerRol(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    return render(request, 'admin/ver_rol.html')

def VerRolGrupo(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = rol.Rol_permiso_sup()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los roles!')

    return render(request, 'admin/ver_rol_grupo.html', {
        'leer': clave
    })

def VerRolSingular(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = rol.Rol_grupo()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los roles!')

    return render(request, 'admin/ver_rol_singular.html', {
        'leer': clave
    })

def VerRolesTodos(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = rol.Rol_all()
        leer = data.read_all()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los roles!')

    return render(request, 'admin/ver_rol_todos.html', {
        'leer': clave
    })

def VerUsuario(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    return render(request, 'admin/ver_usuario.html')

def VerUsuarioGrupo(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = user.Usuario()
        leer = data.read_grup()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los usuarios!')

    return render(request, 'admin/ver_usuario_grupo.html', {
        'leer': clave
    })

def VerUsuarioSingular(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = user.Usuario()
        leer = data.read_permiso_sup()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los usuarios!')

    return render(request, 'admin/ver_usuario_singular.html', {
        'leer': clave
    })

def VerUsuarioTodos(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = user.Usuario()
        leer = data.read_all_user()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los usuarios!')

    return render(request, 'admin/ver_usuario_todos.html', {
        'leer': clave
    })

def CrearProveedor(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    if request.method == 'POST':

        empresa = request.POST['empresa']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        nit = request.POST['nit']
        direccion = request.POST['direccion']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        compania = request.POST['compania']
        pais = request.POST['pais']

        if empresa.strip() == '':
            messages.warning(request, 'Ingrese el nombre de la empresa.')
        elif nombre.strip() == '':
            messages.warning(request, 'Ingrese nombre del proveedor.')
        elif apellido.strip() == '':
            messages.warning(request, 'Ingrese apellido del proveedor.')
        elif nit.strip() == '':
            messages.warning(request, 'Ingrese NIT del proveedor.')
        elif direccion.strip() == '':
            messages.warning(request, 'Ingrese la dirección del proveedor.')
        elif correo.strip() == '':
            messages.warning(request, 'Ingrese el correo electrónico del proveedor.')
        elif telefono.strip() == '':
            messages.warning(request, 'Ingrese el número de teléfono del proveedor.')
        elif compania.strip() == '': 
            messages.warning(request, 'Ingrese la companía al que pertenece el teléfono del proveedor.')
        elif pais.strip() == '':
            messages.warning(request, 'Ingrese el país del proveedor.')
        else:
            diccionario = {"nit":nit,
                            "nombre_empresa" : empresa,
                            "prov_name" : nombre,
                            "prov_lastname" : apellido,
                            "direccion" : direccion,
                            "correo" : correo,
                            "numero" : telefono,
                            "compania" : compania,
                            "pais" : pais}
            data = proveedor.Proveedor()
            try:
                result = data.create(diccionario)
                if result['id'] != 'Nit, ya existente':
                    if result['id'] != 'Numero de telefono, ya existente':
                        if result['id'] != 'Correo, ya existente':
                            messages.success(request, 'Proveedor creada correctamente!')
                        else:
                            messages.error(request, result['id'])
                    else:
                        messages.error(request, result['id'])
                else:
                    messages.error(request, result['id'])
            except:
                messages.error(request, 'Hubo un error al crear el usuario!')
            

    return render(request, 'admin/crear_proveedor.html')

def CrearCuentaBancaria(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    if request.method == 'POST':
        nombre_banco = request.POST['nombre_banco']
        numero_cuenta = request.POST['numero_cuenta']
        nombre_cuenta = request.POST['nombre_cuenta']
        fondo_cuenta = request.POST['fondo_cuenta']

        if nombre_banco.strip() == '':
            messages.warning(request, 'Ingrese el nombre del banco.')
        elif numero_cuenta.strip() == '':
            messages.warning(request, 'Ingrese el número de cuenta.')
        elif nombre_cuenta.strip() == '':
            messages.warning(request, 'Ingrese el nombre de la cuenta.')
        elif fondo_cuenta.strip() == '':
            messages.warning(request, 'Ingrese el fondo de la cuenta.')
        else:
            diccionario = {"num_cuenta":numero_cuenta,
                            "nombre_banco" : nombre_banco,
                            "nombre_cuenta" : nombre_cuenta,
                            "fondo" : fondo_cuenta}
            data = cuenta_bancaria.Cuenta_bancaria()
            try:
                result = data.create(diccionario)
                if result['id'] == 'Numero de cuenta, ya existente':
                    messages.error(request, result['id'])
                elif result['id'] == 'Fondo, no puede ser negativo':
                    messages.error(request, result['id'])
                else:
                    messages.success(request, 'Cuenta bancaria creada correctamente!')
            except:
                messages.error(request, 'Hubo un error al crear el usuario!')

    return render(request, 'gerencia/crear_cuenta_bancaria.html')

def CrearChequera(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Cuenta_bancaria()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila['num_cuenta'])
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los números de cuentas!')

    if request.method == 'POST':
        numero_chequera = request.POST['numero_chequera']
        numero_cuenta = request.POST['numero_cuenta']
        numero_cheque_disponible = request.POST['numero_cheque_disponible']
        if numero_chequera.strip() == '':
            messages.warning(request, 'Ingrese el número de la chequera.')
        elif numero_cuenta == '0':
            messages.warning(request, 'Seleccione el número de la cuenta.')
        elif numero_cheque_disponible.strip() == '':
            messages.warning(request, 'Ingrese el número de cheques disponibles.')
        else:
            diccionario = {'num_chequera':numero_chequera,
                            'num_cuenta':numero_cuenta,
                            'num_cheque_dispo':numero_cheque_disponible}
            data = cuenta_bancaria.Chequera()
            try:
                result = data.create(diccionario)
                if result['id'] == 'Numero de chequera, ya existente':
                    messages.error(request, result['id'])
                elif result['id'] == 'Fondo, no puede ser negativo':
                    messages.error(request, result['id'])
                else:
                    messages.success(request, 'Chequera creada correctamente!')
            except:
                messages.error(request, 'Hubo un error al crear la chequera!')

    return render(request, 'gerencia/crear_chequera.html', {
        'leer': clave
    })

def RegistrarDeposito(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Cuenta_bancaria()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila['num_cuenta'])
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar los números de cuentas!')

    if request.method == 'POST':
        numero_deposito = request.POST['numero_deposito']
        monto = request.POST['monto']
        numero_cuenta = request.POST['numero_cuenta']
        if numero_deposito.strip() == '':
            messages.warning(request, 'Ingrese el número de depósito.')
        elif monto.strip() == '':
            messages.warning(request, 'Ingrese el monto del depósito.')
        elif numero_cuenta == '0':
            messages.warning(request, 'Seleccione el número de cuenta.')
        else:
            diccionario = {'no_deposito':numero_deposito,
                            'monto':monto,
                            'num_cuenta':numero_cuenta}
            data = cuenta_bancaria.Deposito()
            try:
                result = data.create(diccionario)
                if result['id'].find('existente') > 0 :
                    messages.error(request, result['id'])
                elif result['id'].find('invalido') > 0:
                    messages.error(request, result['id'])
                else:
                    messages.success(request, 'Depósito registrada correctamente!')
            except:
                messages.error(request, 'Hubo un error al registrar el depósito!')

    return render(request, 'gerencia/registrar_deposito.html', {
        'leer': clave
    })

def VerDeposito(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Deposito()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar las chequeras!')

    return render(request, 'gerencia/ver_deposito.html', {
        'leer': clave
    })

def VerChequera(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    return render(request, 'gerencia/ver_chequera.html')

def VerChequeraTodos(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Chequera()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar las chequeras!')

    return render(request, 'gerencia/ver_chequera_todos.html', {
        'leer': clave
    })

def VerChequeraAlerta(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Chequera()
        leer = data.read()
        for fila in leer['res']:
            if fila['estado'] == 'alerta':
                clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar las chequeras!')

    return render(request, 'gerencia/ver_chequera_alerta.html', {
        'leer': clave
    })

def VerChequeraAgotado(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Chequera()
        leer = data.read()
        for fila in leer['res']:
            if fila['estado'] == 'agotado':
                clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar las chequeras!')

    return render(request, 'gerencia/ver_chequera_agotado.html', {
        'leer': clave
    })

def VerChequeraDisponible(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Chequera()
        leer = data.read()
        for fila in leer['res']:
            if fila['estado'] == 'disponible':
                clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar las chequeras!')

    return render(request, 'gerencia/ver_chequera_disponible.html', {
        'leer': clave
    })

def VerCuentaBancaria(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    return render(request, 'gerencia/ver_cuenta_bancaria.html')

def VerCuentaBancariaTodas(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Cuenta_bancaria()
        leer = data.read()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar las cuentas bancarias!')

    return render(request, 'gerencia/ver_cuenta_bancaria_todas.html', {
        'leer': clave
    })

def VerCuentaBancariaActiva(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Cuenta_bancaria()
        leer = data.read()
        for fila in leer['res']:
            if fila['estado '] == 'activo':
                clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar las cuentas bancarias!')

    return render(request, 'gerencia/ver_cuenta_bancaria_activa.html', {
        'leer': clave
    })

def VerCuentaBancariaNoActiva(request):
    if request.method == 'GET':
        if ('correo' in request.COOKIES) == False:
            return redirect('login')

    clave = []
    try:
        data = cuenta_bancaria.Cuenta_bancaria()
        leer = data.read_desactiva()
        for fila in leer['res']:
            clave.append(fila)
    except:
        messages.error(request, 'Error de conexión, no se podrán visualizar las cuentas bancarias!')
    
    return render(request, 'gerencia/ver_cuenta_bancaria_no_activa.html', {
        'leer': clave
    })

def Login(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password = request.POST['password']
        correo = request.POST['correo']
        if usuario.strip() == '':
            messages.warning(request, 'Ingrese el usuario.')
        elif password.strip() == '':
            messages.warning(request, 'Ingrese la contraseña.')
        elif correo.strip() == '':
            messages.warning(request, 'Ingrese el correo electrónico.')
        else:
            data = user.Usuario()
            try:
                result = data.read_all_user(nombre=usuario,clave=password,correo=correo)
                if result['res'] == 'No hay registros que mostrar':
                    messages.error(request, 'Usuario inválido!')
                else:
                    #https://programmerclick.com/article/8199519103/
                    response = HttpResponse("""
                    <script type="text/javascript">
                        window.location="http://127.0.0.1:8000/";
                    </script>
                    """)
                    for id in result['res']:
                        response.set_cookie('nombre_rol', f'{id["nombre_rol"]}')
                        response.set_cookie('id_user', f'{id["id_user"]}')
                        response.set_cookie('nombre', f'{id["nombre"]}')
                        response.set_cookie('correo', f'{id["correo"]}')
                    messages.success(request, 'Usuario correcto!!')
                    return response
            except:
                messages.error(request, 'Error de conexión, No es posible autenticarse por el momento!')
    return render(request, 'login.html')

def Salir(request):

    response = HttpResponse("""
    <script type="text/javascript">
        window.location="http://127.0.0.1:8000/login/";
    </script>
    """)
    response.delete_cookie('correo')
    response.delete_cookie('nombre_rol')
    response.delete_cookie('nombre')
    response.delete_cookie('id_user')

    return response
































def Registrarse(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        correo = request.POST['correo']
    return render(request, 'Registrarse.html')

def CrearPermisos(request):
    if request.method == 'POST':
        dicccionario = {"nombre": "Cajero",                   
                "crud_users": 0,
                "imprimir_cheque": 1,
                "anular_cheque": 0,
                "modificar_cheque": 0,
                "reporte_cheque": 0,
                "auditar_user": 0,
                "admin_cuenta_banc": 0,
                "auditar_cuenta": 0,
                "mostrar_bitacora_user": 0,
                "mostrar_bitacora_group": 0,
                "mostrar_bitacora_jefe": 0,
                "jefe": 0}
        data = rol.Rol_permiso_sup()
        #resultado = data.create(dicccionario)
        resultado = data.read(2)
    return render(request, 'crear_permiso.html')

