print ("P(x, y) = x > y")
p_xy = "x>y"
exec("x=3")
exec("y=5")
ret = eval(p_xy)
print ("P(5, 3) = 5 > 3 = {}".format(ret))

print ("Q(x, y, z) = (x + y) < z")
q_xyz = "x+y<z"
exec("x=3")
exec("y=4")
exec("z=5")
ret = eval(q_xyz)
print ("Q(3, 4, 5) = (3 + 4) > 5 = {}".format(ret))
