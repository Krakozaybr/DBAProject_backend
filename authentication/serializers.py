from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя и создания нового."""

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ["email", "username", "password", "tokens"]

    def get_tokens(self, user):
        tokens = user.get_refresh_token()
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {"refresh": refresh, "access": access}
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None:
            raise serializers.ValidationError(
                "An username address is required to log in."
            )

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        # Метод authenticate предоставляется Django и выполняет проверку, что
        # предоставленные почта и пароль соответствуют какому-то пользователю в
        # нашей базе данных. Мы передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.
        user = authenticate(username=username, password=password)

        # Если пользователь с данными почтой/паролем не найден, то authenticate
        # вернет None. Возбудить исключение в таком случае.
        if user is None:
            raise serializers.ValidationError(
                "A user with this username and password was not found."
            )

        # Django предоставляет флаг is_active для модели User. Его цель
        # сообщить, был ли пользователь деактивирован или заблокирован.
        # Проверить стоит, вызвать исключение в случае True.
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        # Метод validate должен возвращать словать проверенных данных. Это
        # данные, которые передются в т.ч. в методы create и update.
        return {
            "email": user.email,
            "username": user.username,
        }

    def get_tokens(self, data):
        email = data.get("email", None)
        username = data.get("username", None)
        user = User.objects.get(username=username, email=email)
        refresh = user.get_refresh_token()
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserSerializer(serializers.ModelSerializer):
    """Ощуществляет сериализацию и десериализацию объектов User."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    is_student = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password")

        # Параметр read_only_fields является альтернативой явному указанию поля
        # с помощью read_only = True, как мы это делали для пароля выше.
        # Причина, по которой мы хотим использовать здесь 'read_only_fields'
        # состоит в том, что нам не нужно ничего указывать о поле. В поле
        # пароля требуются свойства min_length и max_length,
        # но это не относится к полю токена.
        read_only_fields = ("token",)

    def update(self, instance, validated_data):
        """Выполняет обновление User."""

        # В отличие от других полей, пароли не следует обрабатывать с помощью
        # setattr. Django предоставляет функцию, которая обрабатывает пароли
        # хешированием и 'солением'. Это означает, что нам нужно удалить поле
        # пароля из словаря 'validated_data' перед его использованием далее.
        password = validated_data.pop("password", None)

        for key, value in validated_data.items():
            # Для ключей, оставшихся в validated_data мы устанавливаем значения
            # в текущий экземпляр User по одному.
            setattr(instance, key, value)

        if password is not None:
            # 'set_password()' решает все вопросы, связанные с безопасностью
            # при обновлении пароля, потому нам не нужно беспокоиться об этом.
            instance.set_password(password)

        # После того, как все было обновлено, мы должны сохранить наш экземпляр
        # User. Стоит отметить, что set_password() не сохраняет модель.
        instance.save()

        return instance
