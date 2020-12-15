def handle_item(table_name, key, value):
    key_ = "id" if key == "pk" else key
    value_ = f"{value}" if type(value) == str else value
    return f"\"{table_name}\".\"{key_}\" = \'{value_}\'"

def get_where(table_name, kwargs):
    if len(kwargs) == 0:
        raise Exception("Expected an argument")

    if len(kwargs) == 1:
        for key, value in kwargs.items():
            return handle_item(table_name, key, value)

    list_ = []
    for key, value in kwargs.items():
        list_.append(handle_item(table_name, key, value))

    return " AND ".join(list_)


def get_set(pk, fks):
    if len(fks) == 1:
        return f"SELECT {pk}, {fks[0]}"

    list_ = f"SELECT {pk}, {fks[0]}"
    for fk in fks[1:]:
        list_ += f" UNION ALL SELECT {pk}, {fk}"

    return list_