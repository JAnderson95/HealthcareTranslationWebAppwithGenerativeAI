
from django.http import JsonResponse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import render, get_list_or_404
from django.contrib import messages
import json
import logging
from .models import  TranslationRecord, TranslationSession
from .services import TranslationService

# Create your views here.

# Logger Config
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class TranslationView(View):
    template_name = 'translation/translate.html'

    def post(self, request):
        try:
            #VALIDATING AJAX

            if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid Request'}, status=400)

            data = json.loads(request.body)
            text = data.get('text', '')
            input_lang = data.get('input_lang', 'es')
            output_lang = data.get('output_lang', 'en')

            #VALIDATIN ALL THE PARAMS

            if not text:
                return JsonResponse({'error': 'Empty Text'}, status=400)
            if len(text) > 1000:
                return JsonResponse({'error': 'Text too long'}, status=400)

            # Validating supported languages

            valid_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ar']
            if input_lang not in valid_languages or output_lang not in valid_languages:
                return JsonResponse({'error': 'Unsupported language'}, status=400)

            # Obtaining translation
            translated_text = TranslationService.get_translation(text, input_lang, output_lang)

            # Saving data in BD if user is authenticated
            translation_record = None
            if request.user.is_authenticated:
                translation_record = self._save_translation(
                    request.user, text, translated_text, input_lang, output_lang
                )

            return JsonResponse({
                'original': text,
                'translated': translated_text,
                'translation_id': translation_record.id if translation_record else None
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse({'error': 'Internal server error'}, status=500)

    def get(self, request):
        languages = [
            ('en', 'English'),
            ('es', 'Español'),
            ('fr', 'Français'),
            ('de', 'Deutsch'),
            ('it', 'Italiano'),
            ('pt', 'Português'),
            ('ru', 'Русский'),
            ('zh', '中文'),
            ('ja', '日本語'),
            ('ar', 'العربية')
        ]

        # Obtaining last languages used by the user.

        last_session = None
        if request.user.is_authenticated:
            last_session = TranslationSession.objects.filter(user=request.user).last()

        context = {
            'languages': languages,
            'last_input_lang': last_session.input_language if last_session else 'es',
            'last_output_lang': last_session.output_language if last_session else 'en'
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def _save_translation(self, user, original_text, translated_text, input_lang, output_lang):
        """Saving the information in the db"""
        try:
            # Creating or obtaining translating session

            session_id = f"{user.id}-{input_lang}-{output_lang}"
            translation_session, _ = TranslationSession.objects.get_or_create(
                user=user,
                input_language=input_lang,
                output_language=output_lang,
                defaults={'session_id': session_id}
            )

            # creating translation registration
            return TranslationRecord.objects.create(
                session=translation_session,
                original_text=original_text,
                translated_text=translated_text
            )
        except Exception as e:
            logger.error(f"Error saving the translation: {str(e)}")
            return None


class TranslationHistoryView(LoginRequiredMixin, View):
    template_name = 'translation/history.html'

    def get(request, self):
        translations = TranslationRecord.objects.filter(
            session__user=request.user
        ).select_related('session').order_by('-created_at')[:50]  # This limits to the  50 newest

        return render(request, self.template_name, {
            'translations': translations
        })


def delete_translations(request, pk):
    '''This view is created to delete a translation in case needed'''

    if request.method == 'POST':
        translation = get_list_or_404(
            TranslationRecord,
            pk=pk,
            session__user=request.user
        )
        translation.delete()
        messages.success(request, 'The translation has been deleted correctly')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'This method is not permitted'}, status=405)
