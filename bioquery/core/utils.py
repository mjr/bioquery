def get_where(table_name, kwargs):
    if len(kwargs) == 0:
        raise Exception('Expected an argument')

    if len(kwargs) == 1:
        for key, value in kwargs.items():
            key_ = 'id' if key == 'pk' else key
            value_ = f'{value}' if type(value) == str else value
            return f'{table_name}."{key_}" = "{value_}"'

    list_ = []
    for key, value in kwargs.items():
        key_ = 'id' if key == 'pk' else key
        value_ = f'{value}' if type(value) == str else value
        list_.append(f'{table_name}."{key_}" = "{value_}"')

    return ' AND '.join(list_)


def get_set(pk, fks):
    if len(fks) == 1:
        return f"SELECT {pk}, {fks[0]}"

    list_ = f"SELECT {pk}, {fks[0]}"
    for fk in fks[1:]:
        list_ += f" UNION ALL SELECT {pk}, {fk}"

    return list_