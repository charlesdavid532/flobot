import requests
class HandoverOffer(object):
	"""docstring for HandoverOffer"""
	def __init__(self):
		super(HandoverOffer, self).__init__()


	def handoverOffer(self):
		headers = {
		    'Content-Type': 'application/json',
		}

		params = (
		    ('access_token', 'EAACtGhC8ZAjsBAB6hZBfPCUZAm9kvK5NtjARZCl99uNx5S4yRMPxVINPc3z5RYNtHQYKB8iMG8xeSlq57xVbtbRZCBz7N4kOu1EZAZBJizDTzgi53C7UHWz1FWaiaIVn6juYGFQY80sxBWIbGo6LwH91X8YPqMauZCjVgqANFYWLGQZDZD'),
		)

		data = '{\n  "recipient":{"id":"1932650863441865"},\n  "target_app_id":"190327461537339",\n  "metadata":"String to pass to secondary receiver app" \n}'

		response = requests.post('https://graph.facebook.com/v2.6/me/pass_thread_control', headers=headers, params=params, data=data)

		print(str(response))
		print(response.content)
		#NB. Original query string below. It seems impossible to parse and
		#reproduce query strings 100% accurately so the one below is given
		#in case the reproduced version is not "correct".
		# response = requests.post('https://graph.facebook.com/v2.6/me/pass_thread_control?access_token=<PAGE_ACCESS_TOKEN>', headers=headers, data=data)

		