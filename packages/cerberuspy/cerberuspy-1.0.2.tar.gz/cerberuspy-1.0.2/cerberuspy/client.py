import requests

from typing import Literal, Final


class Client():
	"""
	Клиент для использования API ИС "Цербер".
	"""
	def __init__(self, cerber_id: str, proxies: dict = None):
		self.api: str = "https://api.iscerberus.ru"
		self.cerber_id: str = cerber_id

	def get_info(self):
		return requests.post(
			f"{self.api}/get_info",
			json={
				"cerber_id": self.cerber_id
			}
		).json()

	def search(self, target: str, target_type: Literal["phone", "email", "telegram", "card", "company", "inn", "full_name", "ip"]):
		return requests.post(
			f"{self.api}/search", 
			json={
				"cerber_id": self.cerber_id,
				"target": target,
				"target_type": target_type
			}
		).json()
