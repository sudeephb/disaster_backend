from django.http import HttpResponse, JsonResponse
import json
from rest_framework.decorators import api_view
from hierarchical_classifier.hierarchical_classifier import predict

class_hierarchy = {
    'natural': {"label1": "natural", "label2": "null", "label3": "null"},
    'technological': {"label1": "technological", "label2": "null", "label3": "null"},
    'geophysical': {"label1": "natural", "label2": "geophysical", "label3": "null"},
    'earthquake': {"label1": "natural", "label2": "geophysical", "label3":"earthquake"},
    'landslide': {"label1": "natural", "label2": "geophysical", "label3":"landslide"},
    'meterological': {"label1": "natural", "label2": "meterological", "label3": "null"},
    'storm': {"label1": "natural", "label2": "meterological", "label3": "storm"},
    'rainfall': {"label1": "natural", "label2": "meterological", "label3": "rainfall"},
    'thunder_and_lightning': {"label1": "natural", "label2": "meterological", "label3": "thunder_and_lightning"},
    'extreme_temperature': {"label1": "natural", "label2": "meterological", "label3": "extreme_temperature"},
    'hydrological': {"label1": "natural", "label2": "hydrological", "label3": "null"},
    'flood': {"label1": "natural", "label2": "hydrological", "label3": "flood"},
    'avalanche': {"label1": "natural", "label2": "hydrological", "label3": "avalanche"},
    'climatological': {"label1": "natural", "label2": "climatological", "label3": "null"},
    'drought': {"label1": "natural", "label2": "climatological", "label3": "drought"},
    'wildfire': {"label1": "natural", "label2": "climatological", "label3":"wildfire" },
    'biological': {"label1": "natural", "label2": "biological", "label3": "null"},
    'insect_infestation': {"label1": "natural", "label2": "biological", "label3": "insect_infestation"},
    'epidemic': {"label1": "natural", "label2": "biological", "label3": "epidemic"},
    'transport_accident': {"label1": "technological", "label2": "transport_accident", "label3": "null"},
    'air_accident': {"label1": "technological", "label2": "transport_accident", "label3": "air_accident"},
    'road_accident': {"label1": "technological", "label2": "transport_accident", "label3": "road_accident"},
    'fire_and_explosion': {"label1": "technological", "label2": "miscellaneous", "label3": "fire_and_explosion"},
}

@api_view(['POST'])
def index(request):
    """Provides predicted class for given title

    Args:
        request should contain list of news title with its id in body
        example:
        [
            {"id" : "1" ,"title" : "Some news 1"},
            {"id" : "2" ,"title" : "Some news 2"}
        ]

    Returns:
        json: list of predicted classes along with id
    """
    if request.method == 'POST':
        json_list = request.data
        print(json_list)
        if json_list:
            if type(json_list) == str:
                json_array = json.loads(json_list)
            else:
                json_array = json_list
            predicted_df = predict(json_array)

            return_list = []
            for id, title, result in predicted_df.values:
                return_dict = class_hierarchy[result]
                return_dict["id"] = id
                return_list.append(return_dict)
            print(return_list)
            return JsonResponse(return_list,safe=False)
        else:
            return JsonResponse({"error": "no title_list in post data"})
    return JsonResponse({"error": "not_post"})