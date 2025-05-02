import requests
from django.conf import settings
import logging
from random import choice
import json

logger = logging.getLogger(__name__)


class TranslationService:

    # This is a medical dictionary created to give to the  assistant as i dont have any api key to connect to gpt
    MEDICAL_PHRASES = {
        'en': {
            'headache': {'es': 'dolor de cabeza', 'fr': 'mal de tête'},
            'fever': {'es': 'fiebre', 'fr': 'fièvre'},
            'pain': {'es': 'dolor', 'fr': 'douleur'},
            'allergy': {'es': 'alergia', 'fr': 'allergie'},
            'nausea': {'es': 'náusea', 'fr': 'nausée'},
            'dizziness': {'es': 'mareo', 'fr': 'étourdissement'},
            'chest pain': {'es': 'dolor en el pecho', 'fr': 'douleur thoracique'},
            'shortness of breath': {'es': 'dificultad para respirar', 'fr': 'essoufflement'}
        },
        'es': {
            'dolor de cabeza': {'en': 'headache', 'fr': 'mal de tête'},
            'fiebre': {'en': 'fever', 'fr': 'fièvre'},
            'dolor': {'en': 'pain', 'fr': 'douleur'},
            'alergia': {'en': 'allergy', 'fr': 'allergie'},
            'náusea': {'en': 'nausea', 'fr': 'nausée'},
            'mareo': {'en': 'dizziness', 'fr': 'étourdissement'},
            'dolor en el pecho': {'en': 'chest pain', 'fr': 'douleur thoracique'},
            'dificultad para respirar': {'en': 'shortness of breath', 'fr': 'essoufflement'}
        },
        'fr': {
            'mal de tête': {'en': 'headache', 'es': 'dolor de cabeza'},
            'fièvre': {'en': 'fever', 'es': 'fiebre'},
            'douleur': {'en': 'pain', 'es': 'dolor'},
            'allergie': {'en': 'allergy', 'es': 'alergia'}
        }
    }

    @classmethod
    def get_translation(cls, text, input_lang, output_lang):
        """
        Obtaining the translation using the most appropiate method available
        """

        # 1. verifying if it is a medical phrase known
        lower_text = text.lower().strip()
        medical_translation = cls._get_medical_translation(
            lower_text, input_lang, output_lang)
        if medical_translation:
            return medical_translation

        # 2. Here im trying to use memory api for the translation
        if getattr(settings, 'USE_MYMEMORY_API', True):
            api_translation = cls._get_mymemory_translation(
                text, input_lang, output_lang)
            if api_translation:
                return api_translation

        # 3. And here it returns a simulated translation
        return cls._get_simulated_translation(text, input_lang, output_lang)

    @classmethod
    def _get_medical_translation(cls, text, input_lang, output_lang):
        """ Looks for the embedded medical dictionary"""
        try:
            if input_lang in cls.MEDICAL_PHRASES and text in cls.MEDICAL_PHRASES[input_lang]:
                return cls.MEDICAL_PHRASES[input_lang][text].get(output_lang)
        except Exception as e:
            logger.error(f"Error in the dictionary: {str(e)}")
        return None

    @classmethod
    def _get_mymemory_translation(cls, text, input_lang, output_lang):
        """Trying to use memory translation API currently no used"""
        try:
            response = requests.get(
                'https://api.mymemory.translated.net/get',
                params={
                    'q': text,
                    'langpair': f"{input_lang}|{output_lang}",
                    'key': getattr(settings, 'MYMEMORY_API_KEY', '')
                },
                timeout=3  # Timeout de 3  seconds
            )

            if response.status_code == 200:
                data = response.json()
                return data.get('responseData', {}).get('translatedText')
        except Exception as e:
            logger.error(f"Error en MyMemory API: {str(e)}")
        return None

    @classmethod
    def _get_simulated_translation(cls, text, input_lang, output_lang):
        return f"[SIMULATION] {text} ({input_lang}→{output_lang})"
