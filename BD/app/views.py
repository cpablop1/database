from django.contrib.messages.api import warning
from django.http import request
from django.shortcuts import render
from django.contrib import messages

import data.rol as rol
import data.Usuario as user
import data.Proveedor as proveedor
import data.Contacto as Contacto

# Create your views here.
# Modificado


def Index(request):

    return render(request, 'layout.html')

def CrearRolUsuario(request):
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
                print(dicccionario)
                data = rol.Rol_permiso_sup()
                data.create(dicccionario)
                messages.success(request, 'Rol de usuario creado exitosamente')
        else:
            messages.warning(request, 'Ingrese nombre de rol')

    return render(request, 'admin/crear_rol_usuario.html')

def CrearRolGrupo(request):
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
    return render(request, 'admin/menu_crear_usuario.html')

def CrearUsuarioGrupo(request):
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
        print(dic)
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
    return render(request, 'admin/ver_rol.html')

def VerRolGrupo(request):
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
    return render(request, 'admin/ver_usuario.html')

def VerUsuarioGrupo(request):
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
                print(result)
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

def Login(request):
    return render(request, 'login.html')

def Registrarse(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        correo = request.POST['correo']
        print('Usuario: ', usuario)
        print('Password1: ', password1)
        print('Password2: ', password2)
        print('Correo: ', correo)
    return render(request, 'Registrarse.html')

def MenuAdmin(request):
    return render(request, 'admin/menu_admin.html')


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
        print (resultado)
    return render(request, 'crear_permiso.html')

