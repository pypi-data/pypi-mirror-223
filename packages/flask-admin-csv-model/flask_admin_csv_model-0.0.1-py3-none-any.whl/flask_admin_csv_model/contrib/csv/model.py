import csv
import itertools
import pathlib


class TextField:
    pass


class Meta:
    file: pathlib.Path
    dialect: csv.Dialect


class RowModel:
    def __init__(self, enumerated_row: tuple[int, dict]) -> None:
        self._row_id, self._row_data = enumerated_row

    def __getattr__(self, _name):
        return self._row_data[_name]

    def row_id(self):
        return self._row_id

    def __str__(self) -> str:
        return ",".join([f"{k}:{v}" for k, v in self._row_data.items()])

    def __repr__(self) -> str:
        return f"RowModel(row_id:{self._row_id}, {self.__str__()}"


class Model:
    Meta: Meta = Meta

    class Cache:
        field_types: tuple = (TextField,)
        fieldnames: list = []

    @classmethod
    def _map_row_model(cls, rows):
        return map(RowModel, rows)

    @staticmethod
    def _wrap_row_model(row_id, row_data):
        return RowModel((row_id, row_data))

    @classmethod
    def get_all(cls):
        with cls.Meta.file.open(newline="") as f:
            reader = csv.DictReader(f, dialect=cls.Meta.dialect)
            yield from cls._map_row_model(enumerate(reader))

    @classmethod
    def get_range(cls, row_start: int, row_stop: int):
        with cls.Meta.file.open(newline="") as f:
            reader = csv.DictReader(f, dialect=cls.Meta.dialect)
            yield from cls._map_row_model(
                enumerate(itertools.islice(reader, row_start, row_stop), row_start)
            )

    @classmethod
    def get(cls, row):
        with cls.Meta.file.open(newline="") as f:
            reader = csv.DictReader(f, dialect=cls.Meta.dialect)
            return cls._wrap_row_model(
                row, next(itertools.islice(reader, row, row + 1))
            )

    @classmethod
    def get_fieldnames(cls):
        if not cls.Cache.fieldnames:
            print("load cache")
            with cls.Meta.file.open(newline="") as f:
                reader = csv.DictReader(f, dialect=cls.Meta.dialect)
                cls.Cache.fieldnames = reader.fieldnames
        return cls.Cache.fieldnames

    @classmethod
    def set(cls, row_id, data):
        with cls.Meta.file.open(newline="") as f:
            reader = csv.DictReader(f, dialect=cls.Meta.dialect)
            fieldnames = reader.fieldnames
            rows = [row for row in reader]

        rows[row_id] = data

        with cls.Meta.file.open(mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect=cls.Meta.dialect)
            writer.writeheader()
            writer.writerows(rows)
        return True

    @classmethod
    def create(cls, data):
        with cls.Meta.file.open(newline="") as f:
            reader = csv.DictReader(f, dialect=cls.Meta.dialect)
            fieldnames = reader.fieldnames

        with cls.Meta.file.open(mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect=cls.Meta.dialect)
            writer.writerow(data)
        return True

    @classmethod
    def delete(cls, row_id):
        with cls.Meta.file.open(newline="") as f:
            reader = csv.DictReader(f, dialect=cls.Meta.dialect)
            fieldnames = reader.fieldnames
            rows = [row for row in reader]

        del rows[row_id]

        with cls.Meta.file.open(mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect=cls.Meta.dialect)
            writer.writeheader()
            writer.writerows(rows)
        return True


if __name__ == "__main__":
    csv_file = pathlib.Path("./example.csv")
    with csv_file.open(newline="") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))

    class BaseModel(Model):
        class Meta:
            file: pathlib.Path = csv_file
            dialect: csv.Dialect = dialect

    class M(BaseModel):
        first = TextField()
        second = TextField()
        third = TextField()
        fourth = TextField()
        fifth = TextField()
