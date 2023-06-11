class EditPermissionsMixin:

    context: dict

    perms = [
        "storage.add_%s",
        "storage.change_%s",
        "storage.delete_%s",
    ]

    def get_permissions_map(self, created):
        current_user = self.context["request"].user
        res = {
            perm % self.Meta.model._meta.model_name: [current_user]
            for perm in self.perms
        }
        return res
