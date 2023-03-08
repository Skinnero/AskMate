import bcrypt

# salt = bcrypt.gensalt()
# p = '123'
# hp = bcrypt.hashpw(p.encode(), salt)
# print(hp.decode())

print(bcrypt.checkpw('admin'.encode(),
                     '$2b$12$Kf3wEeR8Iznd1Dqlbp5NC.nh9YfhyK/zTZsewh.pjYPjTRo2N5AgW'.encode()))
