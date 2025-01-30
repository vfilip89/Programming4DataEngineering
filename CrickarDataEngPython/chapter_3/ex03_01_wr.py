from faker import Faker
import csv

fake = Faker()
output = open('data.csv','w')
header = ['name', 'age', 'street', 'city', 'state', 'zip', 'lng', 'lat']
mywriter = csv.writer(output)

mywriter.writerow(header)
for _ in range(1000):
    mywriter.writerow([
        fake.name(),
        fake.random_int(min=18, max=80),
        fake.street_address(),
        fake.city(),
        fake.state(),
        fake.zipcode(),
        fake.longitude(),
        fake.latitude()
    ])

output.close()


with open('data.csv') as f:
    myreader = csv.DictReader(f)
    header = next(myreader)
    for row in myreader:
        print(row['name'])