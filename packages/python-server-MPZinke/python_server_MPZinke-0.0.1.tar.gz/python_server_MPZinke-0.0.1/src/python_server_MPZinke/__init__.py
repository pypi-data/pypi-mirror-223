#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.12.23                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
import re
import sys
import threading
import traceback
from typing import Any, Dict, List
from werkzeug.exceptions import Forbidden, HTTPException, Unauthorized


HTTP_METHOD = str
HTTP_CALLBACK = str
HTTP_METHOD_MAPPING = Dict[HTTP_METHOD, HTTP_CALLBACK]
URL = str


class Route:
	def __init__(self, url, method_mappings: HTTP_METHOD_MAPPING, *, additional_args: Dict[type, any]=None,
	  secure: bool=True
	):
		self._additional_args: Dict[type, any] = additional_args or {}
		self._methods: HTTP_METHOD_MAPPING = {method.upper(): callback for method, callback in method_mappings.items()}
		self._secure: bool = secure
		self._url: str = url

		self._validate_HTTP_methods()
		self._validate_method_callbacks()


	def __call__(self, **kwargs: dict) -> str:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		RETURNS: 
		"""
		if(self._secure):
			if("Authorization" not in request.headers):
				raise Unauthorized();

			if(self.unauthorized()):
				raise Forbidden();

		# Add additional arg to method call.
		for type, value in self._additional_args.items():
			if(type in (params := self._methods[request.method].__annotations__).values()):
				kwargs[list(params.keys())[list(params.values()).index(type)]] = value

		return self._methods[request.method](**kwargs)


	def unauthorized(self) -> bool:
		"""
		TODO: Make so passed as a function to the route/server
		"""
		AUTHORIZED, UNAUTHORIZED = False, True

		token: str = os.getenv("SMARTCURTAIN_API_TOKEN")
		if(request.headers.get("Authorization") == f"Bearer {token}"):
			return AUTHORIZED

		return UNAUTHORIZED


	# ————————————————————————————————————————— ROUTES::CALLBACK  VALIDATION ————————————————————————————————————————— #

	@staticmethod
	def compare_function_params(func1: Dict[str, type], func2: Dict[str, type]) -> Dict[str, type]:
		"""
		SUMMARY: Compares the args and types of two functions.
		PARAMS:  Takes the args and types of function 1 and the args and types of function 2.
		DETAILS: Iterates through the functions' parameters. Checks whether each of the parameters names and types matches.
		RETURNS: A dictionary of {<param_name>: [<function1_type>, <function2_type>]} for mismatched parameters.
		"""
		mismatched_function_params = {}
		for param in set(list(func1) + list(func2)):
			if(param != "return" and (param not in func1 or param not in func2 or func1[param] != func2[param])):
				mismatched_function_params[param] = [func[param] if(param in func) else None for func in [func1, func2]]

		return mismatched_function_params


	def params_for_url(self) -> Dict[str, type]:
		"""
		SUMMARY: Determines the parameters and types for a URL.
		PARAMS:  Takes the URL to determine the parameters for.
		DETAILS: Determines the parameters and their types with a RegEx. Orders the parameters and types into a
		         dictionary.
		RETURNS: A dictionary of {<parameter>: <type>}.
		"""
		params = re.findall(r"<(int|string):([_a-zA-Z][_a-zA-Z0-9]*)>", self._url)
		return {param: {"int": int, "string": str}[type] for type, param in params}


	def _format_exception_string_for_bad_params(self, http_method: str, unknown_params: Dict[str, list[type]]) -> str:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		RETURNS: 
		"""
		callback_name = self._methods[http_method].__name__
		callback_params = self._methods[http_method].__annotations__

		message_strings = [f"""'{http_method}' callback '{callback_name}' is in compatable with URL '{self._url}'."""]
		if(len(params_missing_from_callback := [param for param in unknown_params if(param not in callback_params)])):
			message_strings.append(f"""'{"', '".join(params_missing_from_callback)}' missing from '{callback_name}'.""")

		url_params: Dict[str, type] = self.params_for_url()
		if(len(params_missing_from_url := [param for param in unknown_params if(param not in url_params)])):
			message_strings.append(f"""Params '{"', '".join(params_missing_from_url)}' missing from '{self._url}'.""")

		mismatched_types = [param for param in unknown_params if(param in url_params and param in callback_params)]
		if(len(mismatched_types_str := "', '".join(mismatched_types))):
			string = f"""'{http_method}' callback is missing arg(s) '{mismatched_types_str}' for URL '{self._url}'."""
			message_strings.append(string)

		return " ".join(message_strings)


	def _validate_HTTP_methods(self) -> None:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		RETURNS: 
		"""
		http_methods = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]

		# Ensure all methods are correct HTTP methods.
		bad_methods: list[str] = [method for method in self._methods if(method.upper() not in http_methods)]
		if((bad_methods_string := "', '".join(bad_methods)) != ""):
			raise Exception(f"Method(s) '{bad_methods_string}' not an HTTP method for URL '{self._url}'")

		if(len(self._methods) == 0):  # Ensure at least 1 method supplied
			raise Exception(f"At least one HTTP method must be supplied for URL '{self._url}")


	def _validate_method_callbacks(self) -> None:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		RETURNS: 
		"""
		# Ensure all set methods have a callback (as opposed to a different type being passed)
		for http_method, callback in self._methods.items():
			if(not hasattr(callback, '__call__')):
				url = self._url
				message = f"""'{http_method}' arg must be of type 'callable', not '{type(callback)}' for URL '{url}'"""
				raise Exception(message)

		url_params = self.params_for_url()
		for http_method, callback in self._methods.items():
			additional_arg_types: list[list[type]] = list(self._additional_args.keys())

			callback_params = callback.__annotations__
			unknown_params: Dict[str, list[Optional[type]]] = Route.compare_function_params(callback_params, url_params)

			# If any url param type is not None or callback param is not in additional arg types
			if(any(types[1] is not None for types in unknown_params.values())
			or any(types[0] not in additional_arg_types for types in unknown_params.values())):
				message = self._format_exception_string_for_bad_params(http_method, unknown_params)
				raise Exception(message)


class Server:
	def __init__(self, *, handle_error: callable=None, host: str="0.0.0.0", name: str="Flask App", port: int=8080,
	  version: str="1.0.0"
	):
		self._app = Flask(__name__)

		self._cors = CORS(self._app)
		self._app.config['CORS_HEADERS'] = 'Content-Type'
		self._app.register_error_handler(Exception, self._handle_error)
		self._app.after_request(self._after_request)

		self._handle_error = handle_error or self._handle_error
		self._host: str = host
		self._port: int = port
		self._routes: list[Route] = []
		self._version: str = version

	# ———————————————————————————————————————————————————— THREAD ———————————————————————————————————————————————————— #

	def __call__(self) -> None:
		"""
		SUMMARY: Adds routes to server & class, and starts the server instance.
		DETAILS: Sets routes using hardcoded routes, functions & HTTP request methods. Calls the Flask::run method.
		"""
		self._app.run(host=self._host, port=self._port)


	# ——————————————————————————————————————————————— REQUEST HANDLING ——————————————————————————————————————————————— #

	def _after_request(self, response):
		"""
		FROM: https://stackoverflow.com/a/30717205
		"""
		response.headers["Content-Type"] = "application/json"
		response.headers["Version"] = self._version
		return response


	def debug(self, flag: bool=True) -> None:
		self._app.debug = flag


	def _handle_error(self, error):
		"""
		SUMMARY: Handles the return response for any server error that occurs during a request.
		PARAMS:  Takes the error that has occured.
		RETURNS: The JSON of the error.
		FROM: https://readthedocs.org/projects/pallet/downloads/pdf/latest/
		 AND: https://stackoverflow.com/a/29332131
		"""
		if isinstance(error, HTTPException):
			return jsonify(error=str(error)), error.code

		try:
			exception_traceback = traceback.format_exc()
		except:
			exception_traceback = "Unknown traceback"

		print(str(error), exception_traceback, file=sys.stderr)
		return jsonify(error=str(error), traceback=exception_traceback), 500


	# ———————————————————————————————————————————————————— ROUTES ———————————————————————————————————————————————————— #
	# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————— #


	def route(self, url: URL, GET: callable=None, *, additional_args: Dict[type, any]=None, secure: bool=True,
	  **methods: Dict[HTTP_METHOD, callable]
	) -> None:
		"""
		SUMMARY: 
		PARAMS:  
		DETAILS: 
		"""
		additional_args = additional_args or {}
		methods = {method.upper(): function for method, function in methods.items()}

		if(GET is not None):  # Use the GET argument
			if("GET" in [key.upper() for key in methods]):  # Ensure 'GET' is not doubly supplied
				raise Exception(f"Ambiguous supplying of argument 'GET' and keyword argument 'GET' for URL '{url}'")

			methods["GET"] = GET

		self._routes.append((route := Route(url, methods, additional_args=additional_args, secure=secure)))

		# Set URLs for both urls that do and do not end with '/', with the exception of the root URL
		# Get the url without and with the ending '/', then remove the blank urls (ie if the root url is provided)
		urls = set(url for url in [url.rstrip("/"), (f"{url}/" if(url[-1] != "/") else url)] if(url))
		[self._app.add_url_rule(url, url, route, methods=list(methods)) for url in urls]
