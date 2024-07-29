from LittleLemonAPI.models import Category, MenuItem

# Create categories
soups = Category.objects.create(slug='soups', title='Soups')
veg_appetizers = Category.objects.create(slug='veg-appetizers', title='Veg Appetizers')
non_veg_appetizers = Category.objects.create(slug='non-veg-appetizers', title='Non-Veg Appetizers')
veg_curries = Category.objects.create(slug='veg-curries', title='Veg Curries')
chicken_curries = Category.objects.create(slug='chicken-curries', title='Chicken Curries')
rice_and_noodles = Category.objects.create(slug='rice-and-noodles', title='Rice and Noodles')
biryani = Category.objects.create(slug='biryani', title='Biryani')
tandoori_and_grill = Category.objects.create(slug='tandoori-and-grill', title='Tandoori and Grill')
naan_and_roti = Category.objects.create(slug='naan-and-roti', title='Naan and Roti')
desserts = Category.objects.create(slug='desserts', title='Desserts')
beverages = Category.objects.create(slug='beverages', title='Beverages')
specials = Category.objects.create(slug='specials', title='Specials')

# Create menu items for Soups
MenuItem.objects.create(title='Chicken Creamy Baby Corn Soup', price=6.99, featured=False, category=soups)
MenuItem.objects.create(title='Chicken Manchow Soup', price=6.99, featured=False, category=soups)
MenuItem.objects.create(title='Hot And Sour Veg Soup', price=5.99, featured=False, category=soups)

# Create menu items for Veg Appetizers
MenuItem.objects.create(title='Baby corn 65', price=11.99, featured=False, category=veg_appetizers)
MenuItem.objects.create(title='Baby corn Manchuria', price=11.99, featured=False, category=veg_appetizers)
MenuItem.objects.create(title='Crispy Corn 65', price=10.99, featured=False, category=veg_appetizers)

# Create menu items for Non-Veg Appetizers
MenuItem.objects.create(title='Chicken Lollipops', price=15.99, featured=False, category=non_veg_appetizers)
MenuItem.objects.create(title='Vanjaram Fish Fry', price=18.99, featured=False, category=non_veg_appetizers)
MenuItem.objects.create(title='Chili Chicken', price=14.99, featured=False, category=non_veg_appetizers)

# Create menu items for Veg Curries
MenuItem.objects.create(title='Channa Korma', price=13.99, featured=False, category=veg_curries)
MenuItem.objects.create(title='Channa Masala', price=13.99, featured=False, category=veg_curries)
MenuItem.objects.create(title='Daal Makhani', price=14.99, featured=False, category=veg_curries)

# Create menu items for Chicken Curries
MenuItem.objects.create(title='Achari Chicken Masala', price=15.99, featured=False, category=chicken_curries)
MenuItem.objects.create(title='Butter Chicken', price=15.99, featured=False, category=chicken_curries)
MenuItem.objects.create(title='Chicken Korma', price=15.99, featured=False, category=chicken_curries)

# Create menu items for Rice and Noodles
MenuItem.objects.create(title='Egg Fried Rice', price=15.99, featured=False, category=rice_and_noodles)
MenuItem.objects.create(title='Chicken Fried Rice', price=16.99, featured=False, category=rice_and_noodles)
MenuItem.objects.create(title='Hakka Paneer Veg Noodles', price=16.99, featured=False, category=rice_and_noodles)

# Create menu items for Biryani
MenuItem.objects.create(title='Fish Biryani', price=18.99, featured=False, category=biryani)
MenuItem.objects.create(title='Lamb Boneless Biryani', price=19.99, featured=False, category=biryani)
MenuItem.objects.create(title='Shrimp Biryani', price=18.99, featured=False, category=biryani)

# Create menu items for Tandoori and Grill
MenuItem.objects.create(title='Masala Papad (2 Pieces)', price=7.99, featured=False, category=tandoori_and_grill)
MenuItem.objects.create(title='Tandoori Chicken Wings (10 Pieces)', price=23.99, featured=False, category=tandoori_and_grill)
MenuItem.objects.create(title='Tandoori Goat Chops', price=23.99, featured=False, category=tandoori_and_grill)

# Create menu items for Naan and Roti
MenuItem.objects.create(title='Paneer Kulcha', price=5.99, featured=False, category=naan_and_roti)
MenuItem.objects.create(title='Cheese Kulcha', price=5.99, featured=False, category=naan_and_roti)
MenuItem.objects.create(title='Peshawari Naan', price=4.99, featured=False, category=naan_and_roti)

# Create menu items for Desserts
MenuItem.objects.create(title='Carrot Halwa', price=4.99, featured=False, category=desserts)
MenuItem.objects.create(title='Kulfi Mango', price=5.99, featured=False, category=desserts)
MenuItem.objects.create(title='Pineapple Souffle', price=6.99, featured=False, category=desserts)

# Create menu items for Beverages
MenuItem.objects.create(title='Coke', price=2.49, featured=False, category=beverages)
MenuItem.objects.create(title='Sprite', price=2.49, featured=False, category=beverages)
MenuItem.objects.create(title='Sweet Tea', price=4.99, featured=False, category=beverages)

# Create special menu items
MenuItem.objects.create(title='Haleem (16 Oz)', price=17.99, featured=True, category=specials)
MenuItem.objects.create(title='Haleem (32 Oz)', price=32.99, featured=True, category=specials)
MenuItem.objects.create(title='Jeera Rice', price=7.99, featured=True, category=specials)
MenuItem.objects.create(title='Natukodi Fry Biryani (chicken)', price=14.99, featured=True, category=specials)
MenuItem.objects.create(title='Natukodi Rasam (Country Chicken Soup)', price=5.99, featured=True, category=specials)

print("Database populated successfully!")