from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from matplotlib import image
from matplotlib import pyplot
import io
# from Auxiliares.funciones import obtener_datos
# from Auxiliares.funciones import escribir_cfdi
# from Auxiliares.captcha import identifica
import time
from pathlib import Path
import base64
import cv2

import numpy as np
import pytesseract
import string


class SATCFDICiec:

	def __init__(self, rfc, psswd):
		#Abrir el navegador y la pagina del SAT
		self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
		# driver.set_window_size(1920, 1080)
		# driver = webdriver.Edge()
		self.driver.get("https://portalcfdi.facturaelectronica.sat.gob.mx/")
		self.rfc = rfc
		self.psswd = psswd

	def login(self):

		#Datos de usuario
		#assert "Python" in driver.title
		#elem = driver.find_element(By.NAME,"q")
		rfc = self.driver.find_element(By.ID, "rfc")
		psw = self.driver.find_element(By.ID, "password")

		rfc.clear()
		rfc.send_keys(self.rfc)
		# rfc.send_keys("VIRG900207RR3")

		psw.clear()
		psw.send_keys(self.psswd)
		# psw.send_keys("oH9Fib7o")

		#--------------------------------------------------------------------------------------------------------------

		#Manejo del Captcha

		captcha = self.driver.find_element(By.NAME, "userCaptcha")

		imagen = self.driver.find_element(By.ID,"divCaptcha")

		archivo = imagen.find_element(By.CSS_SELECTOR,"*")

		imgstring=archivo.get_attribute("src")

		filename = "tmp/descarga.jpg"

		with open(filename,"wb") as f:
			f.write(base64.b64decode(imgstring[22:]))


		img = cv2.imread("tmp/descarga.jpg")
		sal,sugerencia = self.identifica(img)


		pyplot.imshow(sal)
		pyplot.show(block=False)
		pyplot.pause(0.01)

		#tambien se puede hacer lo del captcha a mano asi:
		#respuesta  = input("Captcha sugerencia " + sugerencia + " enter para aceptar sugerencia= ")

		#if respuesta == "":
		#	respuesta = sugerencia

		print(sugerencia)
		respuesta = sugerencia

		pyplot.close()

		captcha.clear()
		captcha.send_keys(respuesta)

		boton = self.driver.find_element(By.ID,"submit")
		boton.click()

	#--------------------------------------------------------------------------------------------------------------

	def query_sat_emitidos(self, start_date, end_date):

		self.login()

		wait = WebDriverWait(self.driver, 7)

		# action = driver.find_element(By.CSS_SELECTOR, "a[href='ConsultaEmisor.aspx']")
		action = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "a[href='ConsultaEmisor.aspx']")))  # Reemplaza con tu selector
		if action:
			action.click()
		else:
			self.close_session()
			return
		# find_date = driver.find_element(By.ID, "ctl00_MainContent_RdoFechas")
		# find_date = wait.until(expected_conditions.presence_of_element_located((By.ID, "ctl00_MainContent_RdoFechas")))
		WebDriverWait(self.driver, 5)
		# find_date = wait.until(expected_conditions.element_to_be_clickable((By.ID, "ctl00_MainContent_RdoFechas")))
		find_date = self.driver.find_element(By.ID, "ctl00_MainContent_RdoFechas")
		self.driver.execute_script("document.getElementById('ctl00_MainContent_RdoFechas').click();")
		if find_date:
			# find_date.click()
			time.sleep(3)
			# start_date_inpt = driver.find_element(By.ID, "ctl00_MainContent_CldFechaInicial2_Calendario_text")
			# # start_date_inpt.clear()
			# start_date_inpt.send_keys(start_date)
			self.driver.execute_script("document.getElementById('ctl00_MainContent_CldFechaInicial2_Calendario_text').value = '"+ start_date +"';")
			# end_date_inpt = driver.find_element(By.ID, "ctl00_MainContent_CldFechaFinal2_Calendario_text")
			# # end_date_inpt.clear()
			# end_date_inpt.send_keys(end_date)
			self.driver.execute_script("document.getElementById('ctl00_MainContent_CldFechaFinal2_Calendario_text').value = '"+ end_date +"';")
			find_cfdis = self.driver.find_element(By.ID, "ctl00_MainContent_BtnBusqueda")
			find_cfdis.click()
			time.sleep(5)
			wait = WebDriverWait(self.driver, 5)
			all_elements = wait.until(expected_conditions.presence_of_element_located((By.ID, "seleccionador")))
			all_elements.click()
			WebDriverWait(self.driver, 3)
			send_download = self.driver.find_element(By.ID, "ctl00_MainContent_BtnDescargar")
			send_download.click()
			time.sleep(5)
		else:
			self.close_session()
			return

		self.close_session()

	def download_sat_package(self, lgn = True):
		if lgn:
			self.login()
		wait = WebDriverWait(self.driver, 7)

		action = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "a[href='ConsultaDescargaMasiva.aspx']")))  # Reemplaza con tu selector
		if action:
			action.click()
		else:
			self.close_session()
			return




	def query_sat_recibidos(self):
		action = self.driver.find_element(By.CSS_SELECTOR, "a[href='ConsultaReceptor.aspx']")
		action.click()

	def close_session(self):
		time.sleep(5)
		# close_sess = driver.find_element(By.ID, "anchorClose")
		# close_sess.click()
		self.driver.execute_script("document.getElementById('anchorClose').click();")

		time.sleep(2)
		self.driver.close()

	def identifica(self, img):
		sal = np.ones(img.shape[0:2])*255

		v,n = np.unique(img.reshape(-1,img.shape[2]),axis=0,return_counts=True)

		ind = [x for _, x in sorted(zip(n,v), key=lambda x:x[0], reverse=True)]

		kernel = np.ones((4,4),np.uint8)

		for i in range(1,7):
			mask = cv2.inRange(img,ind[i],ind[i])
			submask = np.zeros(img.shape[0:2])
			contours, h = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			areamax=[]
			isal=0
			for j,con in enumerate(contours):
				area=cv2.contourArea(con)
				areamax.append([area,j])
			areamax.sort(reverse=True)
			con = contours[areamax[0][1]]
			cv2.fillPoly(submask,[np.array([[c[0][0],c[0][1]] for c in con])],255)
			submask = cv2.erode(submask,kernel)
			br=cv2.boundingRect(contours[areamax[1][1]])
			cx = int(br[0] + br[2]/2)
			cy = int(br[1] + br[3]/2)
			M = np.float32([[1,0,0],[0,1,-1*cy+13]])
			shiftedmask = cv2.warpAffine(mask,M,(img.shape[1],img.shape[0]))
			shiftedsubmask = cv2.warpAffine(submask,M,(img.shape[1],img.shape[0]))
			sal[shiftedsubmask==255] = shiftedmask[shiftedsubmask==255]

		sal=cv2.cvtColor(np.uint8(sal[0:25,:]),cv2.COLOR_GRAY2BGR)
		sal=cv2.resize(sal,[1200,200],interpolation=cv2.INTER_CUBIC)
		sugerencia=pytesseract.image_to_string(sal,config = r"--oem 3 --psm 10 -c tessedit_char_whitelist=123456789BCDFGHJKLMNPQRSTVWXYZ")
		sugerencia = sugerencia.replace(" ","")

		sugerencia = sugerencia.replace("\n","")

		sugerencia = sugerencia.translate(str.maketrans("","",string.punctuation))

		return sal,sugerencia

# if __name__ =="__main__":
#	 img = cv2.imread("descarga.jpg")
#	 sal, sugerencia = identifica(img)
#	 print(sugerencia)
#	 cv2.imshow("",img)
#	 cv2.imshow(" ",sal)
