print("#It's Gpa Calculator")

i = 0

print("")

sn_sem = input("Sks smm xch pdch ")

res = int(sn_sem) * 30
print(res , "kreditov")

sn_prdm = input("Sks u tb prd ")
bari_for = int(sn_prdm)

def inter_for1():
    x_kred = input("skka kredito prd" )
    kred = int(x_kred)

    x_mark = input('otsn po prd')
    mark = int(x_kred)

    wan_gpa = ((mark*kred)/res)
    print(wan_gpa)

while i < bari_for:
    inter_for1()
    i += 1

z = int(input("semes"))  * 30


x = int(input("kredit " ))



y = int(input("bal"))


res = (y * x)/z
print(res)



