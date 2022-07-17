class Cookbook:
    def __init__(self):
        self.recipes = {}

    def read_file(self, file_path):
        with open(file_path, encoding='utf-8') as file:
            dish_name = None
            while line := file.readline():
                line = line.strip()
                if not line:
                    dish_name = None
                    continue
                if dish_name is None:
                    dish_name = line
                    self.recipes[dish_name] = []
                    continue
                if line.isdigit():
                    for _ in range(int(line)):
                        ingredient_info = file.readline()
                        ingredient_name, quantity, measure = map(lambda x: x.strip(), ingredient_info.split('|'))
                        self.recipes[dish_name].append({
                            'ingredient_name': ingredient_name,
                            'quantity': int(quantity),
                            'measure': measure
                        })
                else:
                    raise Exception('Invalid file format, an integer is expected.')
        return True

    def get_shop_list_by_dishes(self, dishes, person_count):
        shop_list = {}
        for dish in dishes:
            if dish not in self.recipes:
                raise Exception(f'Can\'t find dish "{dish}" in the cookbook!')
            for ingredient in self.recipes[dish]:
                ingredient_name = ingredient['ingredient_name']
                if ingredient_name not in shop_list:
                    shop_list[ingredient_name] = {'measure': ingredient['measure'], 'quantity': 0}
                elif ingredient['measure'] != shop_list[ingredient_name]['measure']:
                    raise Exception(
                            f'Can\'t add a certain amount of "{ingredient["measure"]}" '
                            f'to "{shop_list[ingredient_name]["measure"]}"'
                        )
                shop_list[ingredient_name]['quantity'] += ingredient['quantity'] * person_count
        return shop_list


if __name__ == '__main__':
    cookbook = Cookbook()
    cookbook.read_file('recipes.txt')
    shop_list = cookbook.get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
    expected_shop_list = {
        'Картофель': {'measure': 'кг', 'quantity': 2},
        'Молоко': {'measure': 'мл', 'quantity': 200},
        'Помидор': {'measure': 'шт', 'quantity': 4},
        'Сыр гауда': {'measure': 'г', 'quantity': 200},
        'Яйцо': {'measure': 'шт', 'quantity': 4},
        'Чеснок': {'measure': 'зубч', 'quantity': 6}
    }
    assert shop_list == expected_shop_list
