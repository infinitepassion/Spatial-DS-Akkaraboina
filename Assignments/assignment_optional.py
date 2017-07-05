fantasy_team = []
fantasy_team.append("frank gore")
print(fantasy_team)
# Prints: ['frank gore']

fantasy_team.append("calvin johnson") 
print(fantasy_team[1])
# Prints: calvin johnson

fantasy_team.remove("calvin johnson") 
fantasy_team[0] = "aaron rodgers"
print(fantasy_team)
# Prints: ['aaron rodgers']

#############################################
print ("###############################################")
a = [1, 5, 4, 2, 3] 
print(a[0], a[-1])
# Prints: ?? 1 3

a[4] = a[2] + a[-2]
print(a)
# Prints: ??

print(len(a))
# Prints: ?? 5 which is length of a

print(4 in a)
# Prints: ?? True

a[1] = [a[1], a[0]]
print(a)
# Prints: ?? [1, [5, 1], 4, 2, 6]


#############################################
print ("###############################################")
fruits = ['apple', 'pineapple']
fruits.append('banana')



#############################################
print ("###############################################")

def remove_all(el, lst):
    #x[:] = (value for value in x if value != el)
    while el in lst:
        lst.remove(el)
    return lst
def add_this_many(x, y, lst):
    cnt=0
    for x1 in lst:
        if x==x1:
            cnt+=1
    while cnt>0:
        cnt-=1
        lst.append(y)
    return lst


x = [3, 1, 2, 1, 5, 1, 1, 7]
x=remove_all(1,x)
print(x)
lst = [1, 2, 4, 2, 1]
lst=add_this_many(1,5,lst)
print (lst)
   

#############################################
print ("###############################################")
a = [0, 1, 2, 3, 4, 5, 6]
print(a[1:4])
# Prints: [1, 2, 3]
print(a[1:6:2])
# Prints: [1, 3, 5]
print(a[:4]) # equivalent to a[0:4]
# Prints: [0, 1, 2, 3]
print(a[3:]) # equivalent to a[3:len(a)]
# Prints: [3, 4, 5, 6]
print(a[1:4:]) # equivalent to a[1:4:1] or a[1:4] 
# Prints: [1, 2, 3]
print(a[-1:])
# Prints: [6]

#############################################
print ("1.3 D###############################################")

a = [3, 1, 4, 2, 5, 3]
print(a[:4])
# Prints: ?? [3, 1, 4, 2]

print(a)
# Prints: ?? [3, 1, 4, 2, 5, 3]

print(a[1::2])
# Prints: ?? [1,2,3]

print(a[:])
# Prints: ?? [3, 1, 4, 2, 5, 3]

print(a[4:2])
# Prints: ?? []

print(a[1:-2])
# Prints: ?? [1,4,2]

print(a[::-1])
# Prints: ?? reverse order [3,5,2,4,1,3]


print ("******************1.4 E*****************")
def reverse(lst):
    lst.reverse()
    return lst

x = [3, 2, 4, 5, 1] 
print(reverse(x))


print ("******************1.4 F*****************")

def rotates(lst, k):
    return lst[-k:] + lst[:-k]

x = [1, 2, 3, 4, 5]
print(rotates(x,3))

print ("******************2 G*****************")
superbowls = {'joe montana': 4, 'tom brady':3, 'joe flacco': 0}
print(superbowls['tom brady'])
# Prints: 3

superbowls['peyton manning'] = 1
print(superbowls)
# Prints: {'peyton manning': 1, 'tom brady': 3, 'joe flacco': 0, 'joe montana': 4}

superbowls['joe flacco'] = 1
print(superbowls)
# Prints:{'peyton manning': 1, 'tom brady': 3, 'joe flacco': 1, 'joe montana': 4}

print ("******************2 H*****************")

print('colin kaepernick' in superbowls)
#Prints: ?? False

print(len(superbowls))
#Prints: ?? 4

print(superbowls['peyton manning'] == superbowls['joe montana'])
#Prints: ?? False

superbowls[('eli manning', 'giants')] = 2
print(superbowls) 
#Prints: ?? {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1, ('eli manning', 'giants'): 2}

superbowls[3] = 'cat'
print(superbowls)
#Prints: ?? {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1, ('eli manning', 'giants'): 2, 3: 'cat'}


superbowls[('eli manning', 'giants')] =  superbowls['joe montana'] + superbowls['peyton manning']
print(superbowls)
#Prints: ?? {'joe montana': 4, 'tom brady': 3, 'joe flacco': 1, 'peyton manning': 1, ('eli manning', 'giants'): 5, 3: 'cat'}

#superbowls[['steelers', '49ers']] = 11
#print(superbowls)
#Prints: ?? superbowls[['steelers', '49ers']] = 11
#TypeError: unhashable type: 'list'


print ("******************2 I*****************")
