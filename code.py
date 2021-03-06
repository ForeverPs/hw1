import cv2
import math
import struct
import numpy as np
import matplotlib.pyplot as plt

class Homework_First(object):

	def __init__(self):
		self.bmp=cv2.imread('7.bmp',cv2.IMREAD_GRAYSCALE)
#		self.byte=bytearray(self.bmp)
# Function bytearray can convert the bmp array into one dimensional array
		self.lena=cv2.imread('lena.bmp',cv2.IMREAD_GRAYSCALE)
		self.elain=cv2.imread('elain.bmp',cv2.IMREAD_GRAYSCALE)
		self.shear_lena_x = None
		self.shear_lena_y = None

	def get_inf(self):
		bmp = open('lena.bmp','rb')
		print('Type                   :',bmp.read(2).decode())
		print('File Size(B)           :',struct.unpack('I', bmp.read(4))[0])
		print('Reserved 1             :',struct.unpack('H', bmp.read(2))[0])
		print('Reserved 2             :',struct.unpack('H', bmp.read(2))[0])
		print('Offset                 :',struct.unpack('I', bmp.read(4))[0])
		print('Header Size(B)         :',struct.unpack('I', bmp.read(4))[0])
		print('Width                  :',struct.unpack('I', bmp.read(4))[0])
		print('Height                 :',struct.unpack('I', bmp.read(4))[0])
		print('Colour Planes          :',struct.unpack('H', bmp.read(2))[0])
		print('Bits per Pixel         :',struct.unpack('H', bmp.read(2))[0])
		print('Compression Method     :',struct.unpack('I', bmp.read(4))[0])
		print('Raw Image Size         :',struct.unpack('I', bmp.read(4))[0])
		print('Horizontal Resolution  :',struct.unpack('I', bmp.read(4))[0])
		print('Vertical   Resolution  :',struct.unpack('I', bmp.read(4))[0])
		print('Number of Colours      :',struct.unpack('I', bmp.read(4))[0])
		print('Important Colours      :',struct.unpack('I', bmp.read(4))[0])

	def bits(self,k=8):
		plt.figure('Homework of Digital Image Processing')
		while k>=1:
			new=self.change(self.lena,k)
			plt.subplot(2,4,k)
			plt.imshow(new,cmap='gray')
			#declaration for gray is necessary
			plt.title('lena  k='+str(k))
			k-=1
		plt.show()

	def change(self,img,k):
		gray=img.copy()
		gray= 2**k * ((gray - np.min(gray))/(np.max(gray)))
		return gray.astype(int)

	def mean_var(self):
		me=np.mean(self.lena)
		var=np.var(self.lena)
		print('Lena PICTURE\nMEAN: '+str(me)+'\nVAR : '+str(var))

	def zoom(self, key, src, size = [2048, 2048]):
		m, n = np.shape(src)
		if key == 'nearest':
			dst = np.zeros((size[0], size[1]))
			for i in range(size[0]):
				for j in range(size[1]):
					dst[i, j] = src[int(m / size[0] * i), int(n / size[1]* j)]
			return dst
		if key == 'bilinear':
			src = np.pad(src,((0,1),(0,1)),'constant')
			dst = np.zeros((size[0], size[1]))
			for i in range(size[0]):
				for j in range(size[1]):
					x = i * m / size[0]
					y = j * n / size[1]
					xx = math.floor(x)
					yy = math.floor(y)
					u = x - xx
					v = y - yy
					dst[i, j] = int((1-u)*(1-v)*src[xx,yy] + u*(1-v)*src[xx+1,yy] + (1-u)*v*src[xx,yy+1] + u*v*src[xx+1,yy+1])
			return dst
		if key == 'bicube':
			dst = np.zeros((size[0], size[1]))
			filters = np.zeros((4, 4))
			for i in range(size[0]):
				for j in range(size[1]):
					x = i * m / size[0]
					y = j * n / size[1]
					xx = math.floor(x)
					yy = math.floor(y)
					u = x - xx
					v = y - yy
					if xx < m-2 and yy < n-2 and xx > 0 and yy > 0:
						A = np.matrix([self.W(1+u), self.W(u), self.W(1-u), self.W(2-u)])
						C = np.matrix([self.W(1+v), self.W(v), self.W(1-v), self.W(2-v)]).T
						B = src[xx-1:xx+3,yy-1:yy+3]
						dst[i, j] = int(A * B * C)
			return dst

	def shear(self, alpha, axis, img):
		m, n = np.shape(img)
		if axis == 'x':
			new = np.zeros((2*m, n))
			for i in range(m):
				for j in range(n):
					co = np.matrix([[1, -math.tan(alpha/180*math.pi)],[0, 1]]) * np.matrix([i, j]).T
					xx = int(co[0])
					yy = int(co[1])
					new[xx+int(n/3), yy] = img[i, j]
			for i in range(m):
				if np.max(new[i,:]) > 0:
					new = new[i:-1,:]
					break
			for i in range(-1,-2*m,-1):
				if np.max(new[i,:]) > 0:
					new = new[0:i,:]
					break
		elif axis == 'y':
			new = np.zeros((m, 2*n))
			for i in range(m):
				for j in range(n):
					co = np.matrix([[1,0],[-math.tan(alpha/180*math.pi), 1]]) * np.matrix([i, j]).T
					xx = int(co[0])
					yy = int(co[1])
					new[xx, yy+int(m/3)] = img[i, j]
			for i in range(n):
				if np.max(new[:,i]) > 0:
					new = new[:,i:-1]
					break
			for i in range(-1,-2*n,-1):
				if np.max(new[:,i]) > 0:
					new = new[:,0:i]
					break
		return new

	def rotate(self, alpha, img):
		alpha = alpha / 180 * math.pi
		rotation = np.matrix([[math.cos(alpha), math.sin(alpha)],[-1*math.sin(alpha), math.cos(alpha)]])
		m, n = np.shape(img)
		new = np.zeros((int(np.sqrt(m**2 + n**2)), int(np.sqrt(m**2 + n**2))))
		p, q = np.shape(new)
		for i in range(p):
			for j in range(q):
				co = rotation.I * np.matrix([i, j - int(n/2)]).T
				xx = int(co[0])
				yy = int(co[1])
				if xx < m and yy < n and xx > 0 and yy > 0:
					new[i, j] = img[xx, yy]
		for i in range(p):
			if np.max(new[i,:]) > 0:
				new = new[i:-1,:]
				break
		for i in range(-1,-1*p,-1):
			if np.max(new[i,:]) > 0:
				new = new[0:i+1,:]
				break
		for j in range(q):
			if np.max(new[:, j]) > 0:
				new = new[:, j:-1]
				break
		for j in range(-1,-1*q,-1):
			if np.max(new[:,j]) > 0:
				new = new[:,0:j+1]
				break
		plt.imshow(new, cmap = 'gray')
		plt.show()
		return new

	def W(self, x, a = -0.5):
		if abs(x) <= 1:
			return (a+2)*abs(x)**3-(a+3)*abs(x)**2+1
		elif abs(x) > 1 and abs(x) < 2:
			return a*abs(x)**3-5*a*abs(x)**2+8*a*abs(x)-4*a
		return 0

	def draw(self, alist, name):
		num = len(alist)
		size = [np.shape(alist[0])[0], np.shape(alist[0])[1]]
		plt.figure('Lena')
		for k in range(1,num+1):
			plt.subplot(1,num,k)
			plt.imshow(alist[k-1], cmap = 'gray')
			plt.title('Size:  '+str(size[0])+' * '+str(size[1])+'      Method:  '+name[k-1])
		plt.show()

if __name__ == '__main__':
	homework=Homework_First()
	#homework.get_inf()
	homework.bits()
	#homework.mean_var()
	#nearest = homework.zoom(key = 'nearest', src = homework.lena)
	#bilinear = homework.zoom(key = 'bilinear', src = homework.lena)
	#bicube = homework.zoom(key = 'bicube', src = homework.lena)
	#homework.draw(alist = [nearest, bilinear, bicube], name = ['Nearest', 'Bilinear', 'Bicube'])
	homework.shear_lena_x = homework.shear(15, 'x', homework.lena)
	#homework.shear_lena_y = homework.shear(15, 'y', homework.lena)
	nearest = homework.zoom(key = 'nearest', src = homework.shear_lena_x)
	bilinear = homework.zoom(key = 'bilinear', src = homework.shear_lena_x)
	bicube = homework.zoom(key = 'bicube', src = homework.shear_lena_x)
	homework.draw(alist = [nearest, bilinear, bicube], name = ['Nearest', 'Bilinear', 'Bicube'])
	#rotate_elain = homework.rotate(30, homework.elain)
	#nearest = homework.zoom(key = 'nearest', src = rotate_elain)
	#bilinear = homework.zoom(key = 'bilinear', src = rotate_elain)
	#bicube = homework.zoom(key = 'bicube', src = rotate_elain)
	#homework.draw(alist = [nearest, bilinear, bicube], name = ['Nearest', 'Bilinear', 'Bicube'])
