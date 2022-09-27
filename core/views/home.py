from django.views import View
from django.shortcuts import render


class HomeView(View):
	context = {}
	template_name = 'home.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, self.context)
