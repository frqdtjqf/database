import hashlib

def compute_id(base) -> str:
    digest = hashlib.sha256(base.encode()).hexdigest()
    return digest[:16]

base1 = "5c12df59b1eb1691x1"
base2 = "5c12df59b1eb1691x2"

print(compute_id(base1))
print(compute_id(base2))


