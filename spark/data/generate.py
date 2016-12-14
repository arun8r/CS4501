import random

def generate_log(file, num_lines, num_products, num_users):
    with open(file, 'w') as f:
        for i in range(num_lines):
            user_id = random.randint(1, num_users)
            product_id = random.randint(1, num_products)
            f.write('%s\t%s\n' % (user_id, product_id))

generate_log("access.log", 30, 5, 10)