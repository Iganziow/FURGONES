from django.contrib.auth import get_user_model
User = get_user_model()

# Listar todos los usuarios
print(User.objects.all())

# Ver un usuario en particular
admin_user = User.objects.filter(username="admin").first()
if admin_user:
    print("Encontrado:", admin_user.username)
    print("Contraseña correcta?", admin_user.check_password("contraseña_actual"))
