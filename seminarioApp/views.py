from django.shortcuts import render, redirect
from .serializers import InstitucionesSerializer, ParticipanteSerializer
from .forms import FormParticipantes
from .models import Participante, Instituciones
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import Http404


# Create your views here.

def index(request):
    return render(request, 'index.html', {})

#CRUD PARA AGREGAR, ELIMINAR, ACTUALIZAR Y LISTAR INSCRISTO#

def crud(request):
    return render(request, 'crud.html', {})

def cartaNavidad(request):
    return render(request, 'carta_navidad.html', {})

def lista_participante(request):
    participantes = Participante.objects.all()
    data = {'participantes': participantes}
    return render(request, 'listar_participante.html', data)

def agrega_participante(request):
    form = FormParticipantes()
    if request.method == 'POST':
        form = FormParticipantes(request.POST)
        if form.is_valid() :
            form.save()
        return index(request)
    data = {'form' : form}
    return render(request, 'agregar_participante.html', data)

def elimina_participante(request, id):
    participante = Participante.objects.get(id = id)
    participante.delete()
    return redirect('/listar_participante')

def actualiza_participante(request, id):
    participante_actualizado = Participante.objects.get(id = id)
    form = FormParticipantes(instance=participante_actualizado)
    if request.method == 'POST':
        form = FormParticipantes(request.POST, instance=participante_actualizado)
        if form.is_valid() :
            form.save()
        return redirect('/listar_participante')
    data = {'form' : form}
    return render(request, 'actualizar_participante.html', data)

#se trabaja con la api#

def verparticipantesDB(request):
    participantes = Participante.objects.all()
    data = {'participantes': list(participantes.values('nombre','telefono','fecha_inscripcion','instituciones','hora_inscripcion','estado'))}
    return JsonResponse(data)

# class based view#

class ParticipantesLista(APIView):
    def get(self, request):
        participantes = Participante.objects.all()
        serial = ParticipanteSerializer(participantes, many=True)
        return Response(serial.data)

    def post(self, request):
        serial = ParticipanteSerializer(data = request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

class ParticipantesDetalle(APIView):
    def get_object(self, pk):
        try:
            return Participante.objects.get(id=pk)
        except Participante.DoesNotExist:
            return Http404

    def get(self, request, pk):
        participantes = self.get_object(pk)
        serial = ParticipanteSerializer(participantes)
        return Response(serial.data)
                
    def put(self, request, pk):
        participantes = self.get_object(pk)
        serial = ParticipanteSerializer(participantes, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        participantes = self.get_object(pk)
        participantes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    #function based view de intituciones#
    
    
@api_view (['GET', 'POST'])
def InstitucionesLista(request):
    if request.method == 'GET':
        instituciones = Instituciones.objects.all()
        serial = InstitucionesSerializer(instituciones, many=True)
        return Response(serial.data)
    
    if request.method == 'POST':
        serial = InstitucionesSerializer(data= request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def InstitucionesDetalle(request, pk):
    try:
        instituciones = Instituciones.objects.get(id=pk)
    except Instituciones.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serial = InstitucionesSerializer(instituciones)
        return Response(serial.data)
        
    if request.method == 'PUT':
        serial = InstitucionesSerializer(instituciones, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        instituciones.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    