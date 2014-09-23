#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, wave, requests, time
from sys import stdout
from core import NDEVRequest, NDEVResponse, _get_language_input, red, green
from time import sleep

class ASR(object):
	
	chunk_size = 2048
	send_chunk_delay = 0.05
	
	"""
	specify the type, and use the dictionary to construct the value
	 i.e. wav -> audio/x-wav;codec=pcm;bit=16;rate=8000
	 i.e. speex -> audio/x-speex;rate=8000
	 i.e. amr -> audio/amr
	"""
	ContentType = {
		'wav': {
			'mimetype': 'audio/x-wav',
			'codec': 'pcm',
			'bit': 16,
			'rate': [8000,16000] # 8k for ENUS only 
		},
		'speex': { 
			'mimetype': 'audio/x-speex',
			'rate': [8000, 16000] # 8k for ENUS only 
		},
		'amr': { # ENUS only
			'mimetype': 'audio/amr' 
		},
		'qcelp': { # ENUS only
			'mimetype': 'audio/qcelp'
		},
		'evrc': { # ENUS only
			'mimetype': 'audio/evrc'
		}
	}
	
	"""
	results come back as plain text. separated by new lines
	"""
	Accept = {
		'xml': 'application/xml',
		'text': 'text/plain'
	}

	"""
	the desired language for Accept-Language
	"""
	Languages = {
	    "Arabic (Egypt)": {
	        "code": "ar_EG", 
	        "code6": "ara-EGY", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Arabic (International)": {
	        "code": "ar_AE", 
	        "code6": "ara-XWW", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Arabic (Saudi Arabia)": {
	        "code": "ar_SA", 
	        "code6": "ara-SAU", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Bahasa (Indonesia)": {
	        "code": "id_ID", 
	        "code6": "ind-IDN", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Cantonese (Simplified)": {
	        "code": "zh_HK", 
	        "code6": "yue-CHN", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Catalan": {
	        "code": "ca_ES", 
	        "code6": "cat-ESP", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Croatian New": {
	        "code": "N/A", 
	        "code6": "hrv-HRV", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Czech": {
	        "code": "cs_CZ", 
	        "code6": "ces-CZE", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Danish": {
	        "code": "da_DK", 
	        "code6": "dan-DNK", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Dutch": {
	        "code": "nl_NL", 
	        "code6": "nld-NLD", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "English (Australia)*": {
	        "code": "en_AU", 
	        "code6": "eng-AUS", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "English (GB)*": {
	        "code": "en_GB", 
	        "code6": "eng-GBR", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "English (India) New": {
	        "code": "N/A", 
	        "code6": "eng-IND", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "English (US)*": {
	        "code": "en_US", 
	        "code6": "eng-USA", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Finnish": {
	        "code": "fi_FI", 
	        "code6": "fin-FIN", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "French (Canada)": {
	        "code": "fr_CA", 
	        "code6": "fra-CAN", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "French (France)*": {
	        "code": "fr_FR", 
	        "code6": "fra-FRA", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "German*": {
	        "code": "de_DE", 
	        "code6": "deu-DEU", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Greek": {
	        "code": "el_GR", 
	        "code6": "ell-GRC", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Hebrew": {
	        "code": "he_IL", 
	        "code6": "heb-ISR", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Hindi New": {
	        "code": "uk_UA", 
	        "code6": "hin-IND", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Hungarian": {
	        "code": "hu_HU", 
	        "code6": "hun-HUN", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Italian": {
	        "code": "it_IT", 
	        "code6": "ita-ITA", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Japanese": {
	        "code": "ja_JP", 
	        "code6": "jpn-JPN", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Korean": {
	        "code": "ko_KR", 
	        "code6": "kor-KOR", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Malay": {
	        "code": "ms_MY", 
	        "code6": "zlm-MYS", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Mandarin (China / Simplified)": {
	        "code": "cn_MA", 
	        "code6": "cmn-CHN", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Mandarin (Taiwan / Traditional)": {
	        "code": "zh_TW", 
	        "code6": "cmn-TWN", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Norwegian": {
	        "code": "no_NO", 
	        "code6": "nor-NOR", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Polish": {
	        "code": "pl_PL", 
	        "code6": "pol-POL", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Portuguese (Brazil)": {
	        "code": "pt_BR", 
	        "code6": "por-BRA", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Portuguese (Portugal)": {
	        "code": "pt_PT", 
	        "code6": "por-PRT", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Romanian": {
	        "code": "ro_RO", 
	        "code6": "ron-ROU", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Russian": {
	        "code": "ru_RU", 
	        "code6": "rus-RUS", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Slovak": {
	        "code": "sk_SK", 
	        "code6": "slk-SVK", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Spanish (LatAm)": {
	        "code": "es_MX", 
	        "code6": "spa-XLA", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Spanish (Spain)": {
	        "code": "es_ES", 
	        "code6": "spa-ESP", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Swedish": {
	        "code": "sv_SE", 
	        "code6": "swe-SWE", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Thai": {
	        "code": "th_TH", 
	        "code6": "tha-THA", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Turkish": {
	        "code": "tr_TR", 
	        "code6": "tur-TUR", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Ukrainian": {
	        "code": "uk_UA", 
	        "code6": "ukr-UKR", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }, 
	    "Vietnamese": {
	        "code": "vi_VN", 
	        "code6": "vie-VNM", 
	        "frequencies": [
	            "8000", 
	            "16000"
	        ]
	    }
	}

	"""
	generator file for streaming the audio file in chunks
	"""
	@staticmethod
	def __read_wav_file_in_chunks(filepath):
		file_to_play = wave.open(filepath, 'rb')
		total_size = os.path.getsize(filepath) - 44 # 44 = wave header size
		print "  Audio File          %s" % filepath
		data = file_to_play.readframes(ASR.chunk_size)
		total_chunks = 0
		while data != '':
			total_chunks += len(data)
			stdout.write("\r  Bytes Sent          %d/%d \t%d%% " % (total_chunks,total_size,100*total_chunks/total_size))
			stdout.flush()
			sleep(ASR.send_chunk_delay)
			yield data
			data = file_to_play.readframes(ASR.chunk_size)
		stdout.write("\n\n")
		
	"""
	generator file that will stream any given file. 
	"""
	@staticmethod
	def __read_file_in_chunks(filepath):
		file_to_play = open(filepath, 'rb')
		total_size = os.path.getsize(filepath) 
		print "  Audio File         %s" % filepath
		data = file_to_play.read(ASR.chunk_size)
		total_chunks = 0
		while data != '':
			total_chunks += len(data)
			stdout.write("\r  bytes sent: \t%d/%d \t%d%% " % (total_chunks,total_size,100*total_chunks/total_size))
			stdout.flush()
			sleep(ASR.send_chunk_delay)
			yield data
			data = file_to_play.read(ASR.chunk_size)
		stdout.write("\n\n")
		
	"""
	
	"""
	@staticmethod
	def make_request(creds=None, desired_asr_lang=None, filename=None, mode='quiet', requestor_id=None):

		aReq = ChunkedASRRequest(desired_asr_lang, credentials=creds, requestor_id=requestor_id)
		aReq.load_file(filename)
		
		analyze_function = None
		if aReq.audio_type == 'wav':
			analyze_function = ASR.__read_wav_file_in_chunks
		elif aReq.audio_type == 'speex':
			analyze_function = ASR.__read_file_in_chunks
		
		if analyze_function is None:
			print "Don't know how to stream this file... %s" % filename
			sys.exit(-1)
			
		if mode == 'verbose':
			result = aReq.analyze(analyze_function, mode)
		else:
			result = aReq.analyze(analyze_function)

		if result.was_successful():
			print green("✓ ASR",bold=True)
		else:
			print red("× ASR",bold=True)

		return aReq
	
	"""
	Utilities
	"""
	@staticmethod
	def get_language_input(language_code=None):
		ret = None
		if language_code is not None:
			for (k,v) in list(ASR.Languages.items()):
				if v['code'] == language_code or v['code6'] == language_code:
					ret = (k,v)

		if ret is not None:
			return {
				'display': ret[0],
				'properties': ret[1]
			}
		return _get_language_input('Recognition', ASR, default="English (US)")
		
	"""
	Returns the Audio Type {wav,}
	"""
	@staticmethod
	def get_audio_type(filename=None):
		if filename is None:
			return 'wav' # assume wav
		extension = filename[filename.rindex('.')+1:]
		ret = {
			'wav': 'wav',
			'ogg': 'speex',
			'spx': 'speex',
			'amr': 'amr',
			'qcp': 'qcelp',
			'evrc': 'evrc',
		}
		if extension not in ret:
			raise Exception("Bad file extension: '%s' is not supported" % extension)
		return ret[extension]
	
"""
An ASR Response 
"""
class ASRResponse(NDEVResponse):

	def __init__(self, response):
		super(ASRResponse,self).__init__()
		self.status_code = response.status_code
		self._parse_response(response)

	def more_than_one_result(self):
		return len(self.results) > 1

	def get_recognition_result(self):
		return self.results[0]
	
"""
An ASR Request. Done via Transfer-Encoding: Chunked.
"""	
class ChunkedASRRequest(NDEVRequest):

	def __init__(self, language, credentials=None):
		super(ChunkedASRRequest,self).__init__(credentials=credentials)
		self.url = credentials.asr_url
		self.path = credentials.asr_endpoint
		self.language = language 
		self.audio_type = "wav"
		self.response_type = 'text'
		self.bit_rate = ASR.ContentType[self.audio_type]['bit']
		self.filename = None
		self.response = None # will be populated when `analyze` is called

	def load_file(self, filename):
		self.filename = filename
		self.audio_type = ASR.get_audio_type(filename)
		if self.audio_type == 'wav':
			file_to_play = wave.open(filename, 'rb')
			self.sample_width = file_to_play.getsampwidth()
			self.sample_rate = file_to_play.getframerate()
			self.nchannels = file_to_play.getnchannels()
			self.bit_rate = ASR.ContentType[self.audio_type]['bit']

	def get_headers(self):
		headers = {
			u"Content-Type": self._build_header_value(ASR.ContentType,self.audio_type),
			u"Transfer-Encoding": u"chunked", 
			u"Accept": ASR.Accept[self.response_type],
			u"Accept-Topic": u"Dictation"
		}
		if hasattr(self.language['properties'], 'code6'):
			headers[u"Accept-Language"] = self.language['properties']['code6']
		else:
			headers[u"Accept-Language"] = self.language['properties']['code']

		return headers

	def build_url(self):
		ret = "%s%s?appId=%s&appKey=%s&id=%s" % (self.url, self.path, self.app_id, self.app_key, self.requestor_id)
		return ret

	def analyze(self, readstream, mode='quiet'):
		hdrs = self.get_headers()
		url = self.build_url()
		if mode != 'quiet':
			print "* analyzing audio stream..."
			print ""
			print "  Request URL         %s%s" % (self.url,self.path)
			print ""
			print "  Request Params"
			print "  ---------------"
			print "  appId               %s" % self.app_id
			print "  appKey              %s" % self.app_key
			print "  id                  %s" % self.requestor_id
			print ""
			print "  Request Headers "
			print "  --------------- "
			print "  Content-Type        %s" % hdrs[u'Content-Type']
			print "  Transfer-Encoding   %s" % hdrs['Transfer-Encoding']
			print "  Accept              %s" % hdrs['Accept']
			print "  Accept-Topic        %s" % hdrs['Accept-Topic']
			print "  Accept-Language     %s" % hdrs['Accept-Language']
			print ""
			print "  Audio Information "
			print "  ----------------- "
			print "  Sample Width        %d" % self.sample_width
			print "  Sample Rate         %d" % self.sample_rate
			print "  Num Channels        %d" % self.nchannels
			print "  Bit Rate            %d" % self.bit_rate
			print " "
		res = requests.post(url, data=readstream(self.filename), headers=hdrs)
		print "* analyzed stream.\n"
		self.response = ASRResponse(res)
		return self.response



