# adapters/web/rest/ai_blueprint.py
from flask import Blueprint, request, jsonify, g
from domain.services.ai_service.gemini_query_service import GeminiQueryService
import google.generativeai as genai
import os

def create_ai_blueprint(jwt_required_decorator):
    ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

    @ai_bp.route('/query', methods=['POST'])
    @jwt_required_decorator
    def ai_query():
        data = request.get_json()
        query = data.get('query', '')
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        api_key = os.getenv("GEMINI_API_KEY")
        genai.api_key = api_key
        gemini_service = GeminiQueryService(genai)
        locations = gemini_service.process_query(query)
        return jsonify({'locations': locations})

    return ai_bp