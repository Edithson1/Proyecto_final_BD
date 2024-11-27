
from flask import Blueprint, request, jsonify
from services.influencer_service import InfluencerService

influencer_controller = Blueprint('influencer_controller', __name__)

# Verificar si una persona tiene más de 1000 seguidores y convertirla en influencer
@influencer_controller.route('/personas/<int:idPersona>/convertir_en_influencer', methods=['POST'])
def convertir_en_influencer(idPersona):
    """
    Verificar si una persona tiene más de 1000 seguidores y convertirla en influencer.
    """
    resultado = InfluencerService.convertir_en_influencer(idPersona)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200
