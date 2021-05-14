# config settings are for testing on ubuntu
#from kivy.config import Config
#Config.set('graphics','resizable',True)
#coef = 78
#Config.set('graphics','height',coef*19)
#Config.set('graphics','width',coef*9)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.factory import Factory as F
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from PIL import Image
from sten import *

class MenuScreen(Screen):
	pass

class EncryptScreen(Screen):
	text = StringProperty("")
	error = StringProperty("")
	file = StringProperty(None)
	im = None

	def on_enter(self):
		if self.file:
			self.text = "File: "+self.file
		else:
			self.text = "No File Selected"

	def on_leave(self):
		self.clean()

	def load_file(self,file_name):
		self.file = file_name
		file_name = file_name.split('/')[-1]
		self.text = "File: "+file_name
		self.im = Image.open(self.file)

	def select_photo(self):
		if app.initialized:
			file_popup = F.FilePopup()
			file_popup.set_caller(self)
			file_popup.open()

	def load_image(self,im):
		self.file = "new_photo.png"
		self.text = "File: new_photo.png"
		self.im = im

	def encode(self):
		message = self.ids.message.text
		if not(self.file):
			self.error = "Error: No File Selected"
		elif not(message):
			self.error = "Error: Please Type a Message"
		else:
			im = encode(self.im,message)
			save_popup = F.SavePopup()
			save_popup.load_image(im)
			save_popup.open()
			self.clean()

	def clean(self):
		self.error = ""
		self.ids.message.text = ""
		self.text = ""
		self.file = ""
		self.im = None


class DecryptScreen(Screen):
	text = StringProperty("")
	error = StringProperty("")
	file = StringProperty(None)
	im = None

	def on_enter(self):
		if self.file:
			self.load_file(self.file)
		else:
			self.text = "No File Selected"

	def on_leave(self):
		self.file = ""
		self.error = ""
		self.im = None
		self.ids.message.text = ""

	def load_file(self,file_name):
		self.file = file_name
		file_name = file_name.split('/')[-1]
		self.text = "File: "+file_name
		self.im = Image.open(self.file)

	def select_photo(self):
		if app.initialized:
			file_popup = F.FilePopup()
			file_popup.set_caller(self)
			file_popup.open()

	def decode(self):
		if not(self.file):
			self.error = "Error: No File Selected"
		else:
			try:
				self.ids.message.text = decode(self.im)
				self.error = ""
			except:
				self.error = "Error: Problem Encountered During Decode"

class FilePopup(Popup):
	file = StringProperty("")
	error = StringProperty("")

	def set_caller(self, caller):
		self.caller = caller

	def file_selection(self,file_name):
		if file_name == []:
			return
		self.file = file_name[0]
		try:
			Image.open(self.file)
			self.caller.load_file(self.file)
			self.dismiss()
		except:
			self.error = "Error: Selected File is not an Image"

class SavePopup(Popup):
	error = StringProperty("")

	def load_image(self, im):
		self.im = im

	def save(self):
		file_name = self.ids.user_input.text
		if file_name:
			path = self.ids.filechooser.path
			save_file = path+'/'+file_name+'.png'
			Image.fromarray(self.im).save(save_file)
			self.dismiss()
		else:
			self.error = "Input File Name"

	def file_selection(self,file_name):
		if file_name == []:
			return
		file_name = file_name[0].split('/')[-1]
		file_name = file_name.split('.')[0]
		self.ids.user_input.text = file_name

class MyScreenManager(ScreenManager):
	pass

class MainApp(App):
	initialized = BooleanProperty(False)
	def build(self):
		self.initialized = True
		return Builder.load_file('screen.kv')

if __name__ == '__main__':
	app = MainApp()
	app.run()
