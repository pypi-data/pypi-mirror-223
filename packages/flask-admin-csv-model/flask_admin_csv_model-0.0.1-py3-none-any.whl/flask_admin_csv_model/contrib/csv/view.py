from flask_admin import model
from wtforms import fields, form


class ModelView(model.BaseModelView):
    def scaffold_list_columns(self):
        columns = []

        for field_name in self.model.get_fieldnames():
            if hasattr(self.model, field_name):
                attr = getattr(self.model, field_name)
                if isinstance(attr, self.model.Cache.field_types):
                    columns.append(field_name)
        return columns

    def scaffold_form(self):
        class RowModelForm(form.Form):
            pass

        for field_name in self.model.get_fieldnames():
            if hasattr(self.model, field_name):
                attr = getattr(self.model, field_name)
                if isinstance(attr, self.model.Cache.field_types):
                    setattr(
                        RowModelForm,
                        field_name,
                        fields.StringField(field_name),
                    )
        return RowModelForm

    def scaffold_sortable_columns(self):
        return None

    def get_one(self, row_as_str):
        row = int(row_as_str)
        model = self.model
        return model.get(row)

    def get_list(self, page, sort_field, sort_desc, search, filters, page_size=None):
        model = self.model

        if search:
            search = search.lower()
            sources = list(
                item for item in model.get_all() if str(item).lower().find(search) >= 0
            )
        else:
            sources = list(model.get_all())

        total = len(sources)

        if not page_size:
            page_size = self.page_size

        results = self.sampling(sources, page * page_size, page_size)
        # print(len(results), total, page, page_size, search)
        return total, results

    def init_search(self):
        return True

    def get_pk_value(self, model_):
        return model_.row_id()

    @staticmethod
    def sampling(selection, offset=0, limit=None):
        return selection[offset : (limit + offset if limit is not None else None)]

    def update_model(self, form, model):
        return self.model.set(
            model.row_id(), {field.name: field.data for field in form}
        )

    def create_model(self, form):
        return self.model.create({field.name: field.data for field in form})

    def delete_model(self, model):
        return self.model.delete(model.row_id())
