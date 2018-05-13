import csv
import random


def pick_recipe_of_type(recipes, type):
	return random.choice([recipe for recipe in recipes if recipe['类型'] == type])


def make_meal(recipes, menu_so_far):
	meal = []
	while not meal:
		recipe = random.choice(recipes)
		if menu_so_far:
			last_meal = menu_so_far[-1]
			for last_recipe in last_meal:
				if last_recipe['次数'] != '1':
					# we only cook ahead for meat so this is fine
					recipe = last_recipe
					recipe['次数'] = str(int(last_recipe['次数']) -1)
					items = []
					for item in recipe['素配料'].split('、'):
						if item:
							item = item.split('/')[0] + '/0'
						items.append(item)
					all_items = '、'.join(items)
					recipe['素配料'] = all_items
					for item in recipe['荤配料'].split('、'):
						if item:
							item = item.split('/')[0] + '/0'
						items.append(item)
					all_items = '、'.join(items)
					recipe['荤配料'] = all_items

		if recipe['类型'] == '零食':
			recipes.remove(recipe)
		elif recipe['类型'] == '荤菜':
			veg = pick_recipe_of_type(recipes, '素菜')
			if veg:
				meal.append(recipe)
				meal.append(veg)
				if recipe in recipes:
					recipes.remove(recipe)
				recipes.remove(veg)
				break
		elif recipe['类型'] == '素菜':
			protein = pick_recipe_of_type(recipes, '荤菜')
			if protein:
				meal.append(recipe)
				meal.append(protein)
				if recipe in recipes:
					recipes.remove(recipe)
				recipes.remove(protein)
				break
		else:
			meal.append(recipe)
			if recipe in recipes:
				recipes.remove(recipe)
			break
	return meal

def make_weekly_meals(weekly_meals, recipes, meal_list):
	grocery_list = {'meat': {}, 'veg': {}, 'condi':set()}
	menu_so_far = []
	with open(meal_list, 'w') as file:
		i = 1
		while weekly_meals !=0:
			meal = make_meal(recipes, menu_so_far)
			menu_so_far.append(meal)
			file.write('Meal ' + str(i) + '\n') 
			file.write(str(meal)+ '\n')
			grocery_list = make_grocery_list(meal, grocery_list)
			i += 1
			weekly_meals -= 1
		file.write("Groceries:"+ '\n')
		file.write(str(grocery_list))

def make_grocery_list(meal, grocery_list):
	for recipe in meal:
		for item in recipe['荤配料'].split('、'):
			if item:
				if item.split('/')[0] not in grocery_list['meat']:
					grocery_list['meat'][item.split('/')[0]] = float(item.split('/')[1])
				else:
					grocery_list['meat'][item.split('/')[0]] += float(item.split('/')[1])
		for item in recipe['素配料'].split('、'):
			if item:
				if item.split('/')[0] not in grocery_list['veg']:
					grocery_list['veg'][item.split('/')[0]] = float(item.split('/')[1])
				else:
					grocery_list['veg'][item.split('/')[0]] += float(item.split('/')[1])
		grocery_list['condi'] = set(recipe['调料'].split('、')) | grocery_list['condi']
	return grocery_list

def main():
	recipes_path = './recipes.csv'
	weekly_meals = 9
	meal_list = './meal_list.txt'
	recipes = []
	with open(recipes_path, newline='') as file:
		recipes_reader = csv.DictReader(file)
		for row in recipes_reader:
			recipe = {}
			for entry in row:
				recipe[entry] = row[entry]
			recipes.append(recipe)
	make_weekly_meals(weekly_meals, recipes, meal_list)



if __name__ == "__main__":
    main()