gramms_per_bun = 100


def calculate_buns_to_bake(data: dict):
    return data['meal'] // gramms_per_bun
