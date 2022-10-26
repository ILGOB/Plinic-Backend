from drf_yasg.inspectors import SwaggerAutoSchema


class ViewSetAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get("tags", None) or getattr(self.view, "my_tags", [])
        if not tags:
            tags = [operation_keys[0]]

        return tags
