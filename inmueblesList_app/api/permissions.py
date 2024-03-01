from rest_framework import permissions


# Admins pueden escribir, otros solo leer. Hereda de IsAdminUser, pero permite lecturas a todos.
class IsAdminOrReadOnly(permissions.IsAdminUser): 
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        staff_permission = bool(request.user and request.user.is_staff)
        return staff_permission
    

# Creador de comentario puede editar, otros solo leer. Verifica creador o admin para escritura.
class IsComentarioUserOrReadOnly(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.comentario_user == request.user or request.user.is_staff


