from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.core.paginator import Paginator
from songline import Sendline


token = '9Z2zvpB9saTwIWlJyMwt6Vz7Dk5jQGS9CC6oCmL97br'
messenger = Sendline(token)

##################
def GenerateToken(domain='http://localhost:8000/confirm/'):
	allchar = [ chr(i) for i in range(65,91)]
	allchar.extend([chr(i) for i in range(97,123)])
	allchar.extend([str(i) for i in range(10)])

	emailtoken =''

	for i in range(40):
		emailtoken += random.choice(allchar)

	url = domain + emailtoken
	
	return url
##################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

	myemail = 'zunoc123@gmail.com'
	mypassword = '0805465856'
	receiver = sendto

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj
	msg['From'] = 'Admin Web'
	msg['To'] = receiver
	text = detail

	part1 = MIMEText(text, 'plain')
	msg.attach(part1)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()

	s.login(myemail, mypassword)
	s.sendmail(myemail, receiver.split(','), msg.as_string())
	s.quit()


###########Start sending#############
subject = 'ยืนยันการสมัครเว็บไซต์'
newmember_name = 'Test'
content = ''' กรุณายืนยันอีเมล์ '''
msg = 'สวัสดี {}\n\n {}'.format(newmember_name,content)

#sendthai('zunoc123@gmail.com',subject,msg) 
##################



def Home(request):
	product = Allproduct.objects.all().order_by('id').reverse()[:3]
	perorder = Allproduct.objects.filter(quantity__lte=0)
	context = {'product':product,'perorder':perorder}

	return render(request, 'myapp/home.html', context)


def About(request):
	return render(request, 'myapp/about.html')


def Contact(request):
	return render(request, 'myapp/contact.html')


def Truk(request):
	return render(request, 'myapp/truk.html')


def AddProduct(request):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	if request.method == 'POST'and request.FILES['imageupload']:
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')

		new = Allproduct()
		new.name = name 
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit
		########### Save Image ########
		file_image = request.FILES['imageupload']
		file_image_name = request.FILES['imageupload'].name.replace(' ','')
		print('FILES_IMAGE:',file_image)
		print('IMAGE_NAME:', file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name, file_image)
		upload_file_url = fs.url(filename)
		new.image = upload_file_url[6:]
		###################
		new.save()

	return render(request, 'myapp/addproduct.html')


def Productall(request):
	product = Allproduct.objects.all().order_by('id').reverse()
	paginator = Paginator(product, 3)
	page = request.GET.get('page')
	product = paginator.get_page(page)
	context = {'product':product}

	return render(request, 'myapp/allproduct.html', context)


def Test(request):
	product = Allproduct.objects.all()
	context = {'product':product}
	return render(request, 'myapp/bug.html' , context)


def Register(request):
	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()

		##### send email 
		sendthai(email,subject,msg)

		user = authenticate(username=email, password=password)
		login(request, user)

	return render(request, 'myapp/register.html')


def AddtoCart(request, pid):
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)

	try:
		# กรณีสินค้าซ้ำ
		newcart = Cart.objects.get(user=user, productid=str(pid))
		newquan = newcart.quantity + 1
		newcart.quantity = newquan
		calculate = newcart.price * newquan
		newcart.total = calculate
		newcart.save()

		# update จำนวนของในตะกร้าสินค้า
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')
	except:
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price =int(check.price)
		newcart.quantity = 1
		calculate = int(check.price) * 1
		newcart.total = int(check.price)
		newcart.save()

		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')


def MyCart(request):
	username = request.user.username
	user = User.objects.get(username=username)
	
	context = {}

	if request.method == 'POST':
		# ใช้ลบสอนค้าเท่านั้น
		data = request.POST.copy()
		productid = data.get('productid')
		item = Cart.objects.get(user=user, productid=productid)
		item.delete()
		context['status'] = 'delete'
		# update ตัวเลข
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()


	mycart = Cart.objects.filter(user=user)
	count = sum([ c.quantity for c in mycart])
	total = sum([ c.total for c in mycart])

	context['mycart'] = mycart
	context['count'] = count
	context['total'] = total
	return render(request, 'myapp/mycart.html', context)


def MyCartEdit(request):
	# เช็ค username ว่าเป็นขอใคร
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}

	# ลบค่า
	if request.method == 'POST':
		data = request.POST.copy()
		print(data)

		if data.get('clear') == 'clear':
			print(data.get('clear'))
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')
		
		editlist = [] # สร้าง list เก็บสินค้าคืออะไร
		# เอา data เอา k, v เอาออกมา
		for k,v in data.items():
			print(k,v)
			# pv_7
			# เช็คตัวอักษรแรกว่าเป็น pd หรือไม่
			if k[:2] == 'pd':
				pid = int(k.split('_')[1])
				dt = [pid,int(v)]
				editlist.append(dt)
		print('Editlist:', editlist)

		for ed in editlist:
			edit = Cart.objects.get(productid=ed[0], user=user)
			edit.quantity = ed[1] #quan
			calculate = edit.price * ed[1]
			edit.total = calculate
			edit.save()

		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('mycart-page')

		'''
		if data.get('checksave') == 'checksave':
			
			return redirect('mycart-page')
		'''

	'''
	if request.method == 'POST':
		# ใช้ลบสอนค้าเท่านั้น
		data = request.POST.copy()
		productid = data.get('productid')
		item = Cart.objects.get(user=user, productid=productid)
		item.delete()
		context['status'] = 'delete'
		# update ตัวเลข
		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
	'''

	mycart = Cart.objects.filter(user=user)

	context['mycart'] = mycart
	return render(request, 'myapp/mycartedit.html', context)


def Checkout(request):
	username = request.user.username
	user = User.objects.get(username=username)

	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')

		if page == 'information':
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['address'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other
			
			mycart = Cart.objects.filter(user=user)
			count = sum([ c.quantity for c in mycart])
			total = sum([ c.total for c in mycart])

			context['mycart'] = mycart
			context['count'] = count
			context['total'] = total
			
			return render(request, 'myapp/checkout2.html', context)
		
		if page == 'confirm':
			print('Confirm')
			print(data)

			mycart = Cart.objects.filter(user=user)

			mid = str(user.id).zfill(4)
			dt = datetime.now().strftime('%Y%m%d%H%M%S')
			orderid ='OD' + mid + dt
			productorder = '' # เก็บข้อความ
			producttotal = 0 

			for pd in mycart:
				order = OrderList()
				order.orderid = orderid
				order.productid = pd.productid
				order.productname = pd.productname
				order.price = pd.price
				order.quantity = pd.quantity
				order.total = pd.total
				order.save()
				productorder = productorder + '- {}\n'.format(pd.productname)
				producttotal += pd.total # เพิ่ม pd.total เข้าไป

			texttoline = 'ODID: {}\n--\n{}ยอดรวม: {:,.2f} บาท ({})'.format(orderid, productorder, producttotal, name)
			# เช็คยอดสินค้า
			if producttotal > 10000:
				messenger.sticker(14,1,texttoline)
			else:
				messenger.sendtext(texttoline)
			# create order pending
			odp = OrderPending()
			odp.orderid = orderid
			odp.user = user
			odp.name = name
			odp.tel = tel
			odp.address = address
			odp.shipping = shipping
			odp.payment = payment
			odp.other = other
			odp.save()

			# clear cart
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')
			# generate order no. and save to Order Moels
			# save product in cart to OrderProduct models
			# clear cart
			# redirect to order list page

	return render(request, 'myapp/checkout1.html')


def OrderListPage(request):
	#user
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}	

	order = OrderPending.objects.filter(user=user)
	'''
		odlist 
			-object(1)
			-user:
			-name: ผู้รับ
	'''
	# join อีก models
	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		'''
			-orlist
				-object(1)
				-orderid:OD1033
				-product:รถถัง
				-toal:(2)
		'''
		total = sum([ c.total for c in odlist])
		od.total = total

		# สั่งนับ Order มีจำนวนกี่ชิ้น
		count = sum([ c.quantity for c in odlist])
		
		if od.shipping == 'ems':
			shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		# shipcost รวมค่าทั้งหมด
		else :
			shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	
		if od.payment == 'cod':
			shipcost += 20

		od.shipcost = shipcost


	paginator = Paginator(order, 4)
	page = request.GET.get('page')
	order = paginator.get_page(page)
	context['allorder'] = order
	return render(request, 'myapp/orderlist.html', context)


def AllOrderListPage(request):
	# Admin
	context = {}
		
	order = OrderPending.objects.all()

	# join อีก models
	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([ c.total for c in odlist])
		od.total = total

		count = sum([ c.quantity for c in odlist])
		
		if od.shipping == 'ems':
			shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		# shipcost รวมค่าทั้งหมด
		else :
			shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	
		if od.payment == 'cod':
			shipcost += 20

		od.shipcost = shipcost


	paginator = Paginator(order, 5)
	page = request.GET.get('page')
	order = paginator.get_page(page)

	context['allorder'] = order
	return render(request, 'myapp/allorderlist.html', context)


def UpoadSlip(request, orderid):
	print('Order id:', orderid)

	if request.method == 'POST'and request.FILES['slip']:
		data = request.POST.copy()
		sliptime = data.get('sliptime')

		update = OrderPending.objects.get(orderid=orderid)
		update.sliptime = sliptime

		file_image = request.FILES['slip']
		file_image_name = request.FILES['slip'].name.replace(' ','')
		print('FILES_IMAGE:',file_image)
		print('IMAGE_NAME:', file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name, file_image)
		upload_file_url = fs.url(filename)
		update.slip = upload_file_url[6:]
		update.save()

	odlist = OrderList.objects.filter(orderid=orderid)
	total = sum([ c.total for c in odlist])
	oddetail = OrderPending.objects.get(orderid=orderid)
	# คำนวนค่าส่งตามประเภทการส่ง
	count = sum([ c.quantity for c in odlist])
	if oddetail.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
	# shipcost รวมค่าทั้งหมด
	else :
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	
	if oddetail.payment == 'cod':
		shipcost += 20

	context = {'orderid':orderid, 'total':total, 
				'shipcost': shipcost, 
				'gradtotal':total+shipcost,
				'oddetail':oddetail,
				'count':count}

	return render(request, 'myapp/uploadslip.html', context)


def UpdatePaid(request, orderid, status):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
			
	order = OrderPending.objects.get(orderid=orderid)

	if status == 'confirm':
		order.paid = True
	elif status == 'cancel':
		order.paid = False
	order.save()
	return redirect('allorderlist-page')


def UpdateTracking(request, orderid):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
			
	# ems
	if request.method == 'POST':
		order = OrderPending.objects.get(orderid=orderid)
		data = request.POST.copy()
		trackingnumber = data.get('trackingnumber')
		order.trackingnumber = trackingnumber
		order.save()
		return redirect('allorderlist-page')

	order = OrderPending.objects.get(orderid=orderid)
	odlist = OrderList.objects.filter(orderid=orderid)
	
	# shipcost calculate
	total = sum([ c.total for c in odlist])
	order.total = total

	count = sum([ c.quantity for c in odlist])
		
	if order.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		# shipcost รวมค่าทั้งหมด
	else :
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	
	if order.payment == 'cod':
		shipcost += 20

	order.shipcost = shipcost

	context = {'order':order,'odlist':odlist,'total':total,'count':count}

	return render(request, 'myapp/updatetracking.html', context)


def MyOrder(request, orderid):
	username = request.user.username
	user = User.objects.get(username=username)
		

	order = OrderPending.objects.get(orderid=orderid)
	odlist = OrderList.objects.filter(orderid=orderid)
	
	# เช็กว่าเป็นของตัวเองไหม
	if user != order.user:
		return redirect('allproduct-page')
 
	# shipcost calculate
	total = sum([ c.total for c in odlist])
	order.total = total

	count = sum([ c.quantity for c in odlist])
		
	if order.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		# shipcost รวมค่าทั้งหมด
	else :
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	
	if order.payment == 'cod':
		shipcost += 20

	order.shipcost = shipcost

	context = {'order':order,'odlist':odlist,'total':total,'count':count}
	return render(request, 'myapp/myorder.html', context)