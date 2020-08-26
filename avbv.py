#版权由编写者所有，如有侵权请联系，将及时删除
table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

#BV转AV
def bv_to_av(x):
	r=0
	for i in range(6):
		r+=tr[x[s[i]]]*58**i
	return (r-add)^xor

#AV转BV
def av_to_bv(x):
	x=(x^xor)+add
	r=list('BV1  4 1 7  ')
	for i in range(6):
		r[s[i]]=table[x//58**i%58]
	return ''.join(r)


