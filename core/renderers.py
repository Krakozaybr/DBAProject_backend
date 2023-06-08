import json

from rest_framework.renderers import JSONRenderer


class SimpleJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        # Если представление выдает ошибку (например, пользователь не может
        # быть аутентифицирован), data будет содержать ключ error. Мы хотим,
        # чтобы стандартный JSONRenderer обрабатывал такие ошибки, поэтому
        # такой случай необходимо проверить.
        errors = data.get("errors", None)

        if errors is not None:
            # Позволим стандартному JSONRenderer обрабатывать ошибку.
            return super(SimpleJSONRenderer, self).render(data)

        # Наконец, мы можем отобразить наши данные в пространстве имен 'user'.
        return json.dumps(data, ensure_ascii=False)
