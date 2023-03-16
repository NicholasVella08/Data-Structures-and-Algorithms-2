import random


p = random.randint(1000, 3000)
X = set(random.sample(range(-3000, 3001), p))

q = random.randint(500, 1000)
Y = set(random.sample(range(-3000, 3001), q))

r = random.randint(500, 1000)
Z = set(random.sample(range(-3000, 3001), r))

print(f"Set X contains {len(X)} integers.")
print(f"Set Y contains {len(Y)} integers.")
print(f"Set Z contains {len(Z)} integers.")

print(X)
print(Y)
print(Z)

XY_intersection = X.intersection(Y)
XZ_intersection = X.intersection(Z)

print(f"Sets X and Y have {len(XY_intersection)} values in common.")
print(f"Sets X and Z have {len(XZ_intersection)} values in common.")