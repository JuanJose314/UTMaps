from flask import Flask, render_template, request, jsonify
import networkx as nx
from geopy.distance import geodesic
import folium
import os

app = Flask(__name__)

# ========== DICCIONARIO DE UBICACIONES ==========
# ¡COPIA AQUÍ TU DICCIONARIO "ubicaciones" DESDE TU NOTEBOOK!
# Desde "Instituto de Fisica y Matematicas" hasta "V134"

ubicaciones = {
    # === INSTITUTOS ===
    "Instituto de Fisica y Matematicas": (17.827858, -97.80525),
    "Instituto de Hidrologia": (17.827656, -97.806427),
    "Instituto de Agroindustrias": (17.827459, -97.806357),
    "Instituto de Mineria": (17.827219, -97.806054),
    "Instituto de computacion": (17.828049, -97.804874),
    "Instituto de electrónica y mecatronica": (17.828113, -97.805783),
    "Instituto de Diseño": (17.828284, -97.805247),
    "Instituto de Ingeniería Industrial y Automotriz": (17.826893, -97.803876),
    "Instituto de Ciencias Sociales y Humanidades": (17.826655, -97.803442),
    "Instituto de Idiomas": (17.82689, -97.802785),
    "Instituto de ingeniería civil": (17.832183, -97.803498),


    # === TALLERES ===
    "Taller de plasticos": (17.828361, -97.805834),
    "Taller de vidrios y textiles": (17.828544, -97.805523),
    "Taller de metales": (17.828601, -97.805177),
    "Taller de maderas": (17.828527, -97.805003),
    "Taller de serigrafia": (17.826581, -97.802372),
    "Taller de electronica": (17.826430, -97.801865),
    "Taller ingenieria automotriz": (17.831302, -97.803638),

    # === SERVICIOS ESCOLARES Y ADMINISTRATIVOS ===
    "Servicios Escolares": (17.827202, -97.804499),
    "Rectoria": (17.827237, -97.804155),
    "vicerrectoria academica": (17.827597, -97.804464),
    "vicerrectoria administrativa": (17.827554, -97.804134),
    "Biblioteca": (17.827922, -97.80286),
    "Centro de copiado": (17.828026, -97.802854),

    # === SALAS DE COMPUTO ===
    "Salas de dibujo 1-2": (17.826453, -97.801723),
    "Sala de computo 01": (17.827321, -97.803828),
    "Sala de computo 02": (17.827321, -97.803828),
    "Sala de computo 03": (17.827301, -97.803654),
    "Sala de computo 04": (17.827301, -97.803654),
    "Sala de computo 05": (17.827301, -97.803654),
    "Sala de computo 06": (17.827301, -97.803654),
    "Sala de computo 07": (17.826494, -97.802632),
    "Sala de computo 08": (17.826494, -97.802632),
    "Sala de computo 09": (17.826494, -97.802632),
    "Sala de computo 10": (17.826494, -97.802632),
    "Sala de computo 11": (17.826494, -97.802632),
    "Sala de computo 12": (17.826494, -97.802632),
    "Sala de computo 13": (17.826469, -97.802085),

    # === AULAS ===
    "Aula 01": (17.826009, -97.802774),
    "Aula 02": (17.826009, -97.802774),
    "Aula 03": (17.826009, -97.802774),
    "Aula 04": (17.826009, -97.802774),
    "Aula 05": (17.826009, -97.802774),
    "Aula 06": (17.825835, -97.80264),
    "Aula 07": (17.825835, -97.80264),
    "Aula 08": (17.825835, -97.80264),
    "Aula 09": (17.825835, -97.80264),
    "Aula 10": (17.825835, -97.80264),
    "Aula 11": (17.825736, -97.802468),
    "Aula 12": (17.825736, -97.802468),
    "Aula 13": (17.825736, -97.802468),
    "Aula 14": (17.825736, -97.802468),
    "Aula 15": (17.825677, -97.802305),
    "Aula 16": (17.825677, -97.802305),
    "Aula 17": (17.825677, -97.802305),
    "Aula 18": (17.825677, -97.802305),
    "Aula 19": (17.825677, -97.802305),
    "Aula 20": (17.825662, -97.80213),
    "Aula 21": (17.825662, -97.80213),
    "Aula 22": (17.825662, -97.80213),
    "Aula 23": (17.825662, -97.80213),
    "Aula 24": (17.825662, -97.80213),
    "Aula 25": (17.825823, -97.801741),
    "Aula 26": (17.825823, -97.801741),
    "Aula 27": (17.825823, -97.801741),
    "Aula 28": (17.825823, -97.801741),
    "Aula 29": (17.825823, -97.801741),
    "Aula 30": (17.825823, -97.801741),
    "Aula 31": (17.826282, -97.80191),
    "Aula 32": (17.826282, -97.80191),
    "Aula 33": (17.826453, -97.801723),
    "Aula 34": (17.826453, -97.801723),
    "Aula 35": (17.826453, -97.801723),
    "Aula 36": (17.826453, -97.801723),
    "Aula 37": (17.826453, -97.801723),
    "Aula 38": (17.826218, -97.801543),
    "Aula 39": (17.826218, -97.801543),
    "Aula 40": (17.826218, -97.801543),
    "Aula 41": (17.826218, -97.801543),
    "Aula 42": (17.826218, -97.801543),
    "Aula 43": (17.825938, -97.801457),
    "Aula 44": (17.825938, -97.801457),
    "Aula 45": (17.825938, -97.801457),
    "Aula 46": (17.825938, -97.801457),
    "Aula 47": (17.825938, -97.801457),
    "Aula 48": (17.825802, -97.801119),
    "Aula 49": (17.825802, -97.801119),
    "Aula 50": (17.825802, -97.801119),
    "Aula 51": (17.825802, -97.801119),
    "Aula 52": (17.825802, -97.801119),
    "Aula 53": (17.825557, -97.801157),
    "Aula 54": (17.825557, -97.801157),
    "Aula 55": (17.825557, -97.801157),
    "Aula 56": (17.825557, -97.801157),
    "Aula 57": (17.825557, -97.801157),

    # === LABORATORIOS ===
    "Laboratorio de Tecnología Avanzada y Manufactura": (17.827268, -97.806993),
    "Laboratorio Quimico Biologico": (17.827543, -97.806532),
    "Laboratorios de posgrado": (17.827945, -97.806017),
    "Laboratorio de Alimentos": (17.827789, -97.80569),
    "Laboratorios de Electronica Avanzados": (17.827084, -97.802997),
    "Laboratorio de Idiomas": (17.826969, -97.802559),
    "Laboratorio de Fisica": (17.826323, -97.802162),
    "Laboratorio de matematicas": (17.826594, -97.801854),
    "Laboratorio de robotica II": (17.826178, -97.801951),
    "Laboratorio de sistemas": (17.826739, -97.802125),
    "Laboratorio de quimica": (17.826535, -97.802246),

    # === CENTROS, DIVISIONES Y OTROS ===
    "Auditorio": (17.827477, -97.805167),
    "Centro de Modelacion Matematica": (17.828041, -97.805572),
    "Division de estudios de posgrado": (17.827766, -97.804922),
    "Centro cultural": (17.82712, -97.806473),
    "Centro de EStudios Estrategicos de la EMpresa": (17.826714, -97.803082),
    "Planta de Tratamientos de Aguas residuales por lodos activados": (17.826670, -97.801403),
    "Paraninfo": (17.827087, -97.803656),
    "Sala de Auto Acceso": (17.826724, -97.802549),
    "Planta purificadora de agua": (17.826364, -97.802822),
    "Enfermeria": (17.826882, -97.803689),
    "Almacen": (17.827178, -97.805454),
    "Helipuerto": (17.829962, -97.805006),
    "Granja Solar": (17.830988, -97.804434),
    "Vivero": (17.830212, -97.803209),
    "Agavetum": (17.830212, -97.803209),
    "GYM": (17.835599, -97.802176),
    "Cafeteria chica": (17.826979, -97.803241),
    "Cafeteria grande": (17.826448, -97.803133),

    # === ENTRADA ===
    "Entrada": (17.826936, -97.804365),

    # === SANITARIOS ==
    "Sanitario almacen": (17.827148, -97.805242),
    "Sanitario VA" : (17.827544, -97.804002),
    "Sanitario compu": (17.827429, -97.803745),
    "Sanitario A1-5": (17.825897, -97.802798),
    "Sanitario A11-14": (17.825634, -97.802519),
    "Sanitario A25-30": (17.825662, -97.801739),
    "Sanitario A33-37": (17.826622, -97.801688),
    "Sanitario LabSis": (17.826711, -97.802020),

    # === VERTICES (V) ===
    "V1": (17.827076, -97.804359),
    "V2": (17.827028, -97.803756),
    "V3": (17.827189, -97.803764),
    "V4": (17.826979, -97.803378),
    "V5": (17.827204, -97.803206),
    "V6": (17.827352, -97.803163),
    "V7": (17.827546, -97.803093),
    "V8": (17.827944, -97.803077),
    "V9": (17.826859, -97.803337),
    "V10": (17.826864, -97.803246),
    "V11": (17.826841, -97.80305),
    "V12": (17.826811, -97.802924),
    "V13": (17.826982, -97.802954),
    "V14": (17.826788, -97.802715),
    "V15": (17.826867, -97.802635),
    "V16": (17.826755, -97.802436),
    "V17": (17.826637, -97.802224),
    "V18": (17.826609, -97.802047),
    "V19": (17.826517, -97.801988),
    "V20": (17.826484, -97.801916),
    "V21": (17.826129, -97.802047),
    "V22": (17.826068, -97.801905),
    "V23": (17.826691, -97.801741),
    "V24": (17.826035, -97.801715),
    "V25": (17.826379, -97.801613),
    "V26": (17.825912, -97.801626),
    "V27": (17.82569, -97.801111),
    "V28": (17.825636, -97.8011),
    "V29": (17.825595, -97.801366),
    "V30": (17.825457, -97.801406),
    "V31": (17.825593, -97.801897),
    "V32": (17.825784, -97.801951),
    "V33": (17.825897, -97.802146),
    "V34": (17.825802, -97.802173),
    "V35": (17.825496, -97.802267),
    "V36": (17.825845, -97.802358),
    "V37": (17.82557, -97.802452),
    "V38": (17.825907, -97.802492),
    "V39": (17.825639, -97.802589),
    "V40": (17.825965, -97.802608),
    "V41": (17.826065, -97.802635),
    "V42": (17.825749, -97.802755),
    "V43": (17.82642, -97.80271),
    "V44": (17.826387, -97.802624),
    "V45": (17.826492, -97.802959),
    "V46": (17.82665, -97.803238),
    "V47": (17.827628, -97.804327),
    "V48": (17.827615, -97.804222),
    "V49": (17.827584, -97.803952),
    "V50": (17.8275, -97.80423),
    "V51": (17.82748, -97.803965),
    "V52": (17.827462, -97.803584),
    "V53": (17.827385, -97.803487),
    "V54": (17.827817, -97.8043),
    "V55": (17.827911, -97.804383),
    "V56": (17.827214, -97.804981),
    "V57": (17.827288, -97.804874),
    "V58": (17.827196, -97.804689),
    "V59": (17.827122, -97.804662),
    "V60": (17.827275, -97.805038),
    "V61": (17.827365, -97.805314),
    "V62": (17.827413, -97.805443),
    "V63": (17.827431, -97.805864),
    "V64": (17.827567, -97.80614),
    "V65": (17.827561, -97.806242),
    "V66": (17.827835, -97.806344),
    "V67": (17.827814, -97.806481),
    "V68": (17.82763, -97.806733),
    "V69": (17.827288, -97.806744),
    "V70": (17.82773, -97.806419),
    "V71": (17.827475, -97.806274),
    "V72": (17.827365, -97.806154),
    "V73": (17.827301, -97.806838),
    "V74": (17.827222, -97.806551),
    "V75": (17.827957, -97.806264),
    "V76": (17.827827, -97.806078),
    "V77": (17.827794, -97.805931),
    "V78": (17.827983, -97.805668),
    "V79": (17.827947, -97.805577),
    "V80": (17.827827, -97.805437),
    "V81": (17.828011, -97.805346),
    "V82": (17.827988, -97.805236),
    "V83": (17.827939, -97.805191),
    "V84": (17.827914, -97.805049),
    "V85": (17.827975, -97.804949),
    "V86": (17.827916, -97.804834),
    "V87": (17.827911, -97.804703),
    "V88": (17.828003, -97.804689),
    "V89": (17.828105, -97.804619),
    "V90": (17.828218, -97.805829),
    "V91": (17.828473, -97.805475),
    "V92": (17.828529, -97.805349),
    "V93": (17.828435, -97.805183),
    "V94": (17.828322, -97.80504),
    "V95": (17.828182, -97.804786),
    "V96": (17.827105, -97.804528),
    "V97": (17.827247, -97.80433),
    "V98": (17.827521, -97.804319),
    "V99": (17.826721, -97.803337),
    "V100": (17.826206, -97.802195),
    "V101": (17.827464, -97.803742),
    "V102": (17.827143, -97.803319),
    "V103": (17.827046, -97.803128),
    "V104": (17.826847, -97.803163),
    "V105": (17.826706, -97.802449),
    "V106": (17.826663, -97.801591),
    "V107": (17.825785, -97.80132),
    "V108": (17.826267, -97.802356),
    "V109": (17.826492, -97.801787),
    "V110": (17.825759, -97.80183),
    "V111": (17.828026, -97.805518),
    "V112": (17.828159, -97.804145),
    "V113": (17.828537, -97.804525),
    "V114": (17.828693, -97.804552),
    "V115": (17.829157, -97.804507),
    "V116": (17.829336, -97.804657),
    "V117": (17.829808, -97.804625),
    "V118": (17.830168, -97.804609),
    "V119": (17.830286, -97.804523),
    "V120": (17.830398, -97.804276),
    "V121": (17.830654, -97.804142),
    "V122": (17.830656, -97.804448),
    "V123": (17.830401, -97.803579),
    "V124": (17.830242, -97.803431),
    "V125": (17.830694, -97.803380),
    "V126": (17.830952, -97.803356),
    "V127": (17.831190, -97.803418),
    "V128": (17.831757, -97.803415),
    "V129": (17.832178, -97.803319),
    "V130": (17.833373, -97.803034),
    "V131": (17.833728, -97.802818),
    "V132": (17.833899, -97.802232),
    "V133": (17.834810, -97.801731),
    "V134": (17.835313, -97.801851)
}

# ========== CREAR EL GRAFO ==========
G = nx.Graph()

def conectar(origen, destino):
    """Conecta dos lugares y calcula automáticamente la distancia"""
    distancia = geodesic(ubicaciones[origen], ubicaciones[destino]).meters
    G.add_edge(origen, destino, weight=distancia)

# ========== CONEXIONES DEL GRAFO (COPIA TODAS LAS QUE ESTÁN EN TU NOTEBOOK) ==========
conectar("V1","V97")
conectar("V1","V2")
conectar("V1","V96")
conectar("V59","V96")
conectar("V58","V59")
conectar("V57","V58")
conectar("V56","V57")
conectar("V60","V56")
conectar("V61","V60")
conectar("V61","V62")
conectar("V63","V62")
conectar("V62","V80")
conectar("V64","V63")
conectar("V65","V64")
conectar("V65","V71")
conectar("V71","V72")
conectar("V70","V65")
conectar("V66","V64")
conectar("V67","V66")
conectar("V68","V67")
conectar("V69","V68")
conectar("V73","V69")
conectar("V69","V74")
conectar("V66","V75")
conectar("V75","V76")
conectar("V76","V77")
conectar("V77","V78")
conectar("V78","V79")
conectar("V79","V80")
conectar("V80","V81")
conectar("V81","V111")
conectar("V111","V79")
conectar("V81","V82")
conectar("V82","V83")
conectar("V83","V84")
conectar("V84","V85")
conectar("V85","V86")
conectar("V86","V87")
conectar("V87","V88")
conectar("V88","V89")
conectar("V82","V94")
conectar("V75","V90")
conectar("V90","V91")
conectar("V91","V92")
conectar("V92","V93")
conectar("V93","V94")
conectar("V94","V95")
conectar("V95","V89")
conectar("V89","V55")
conectar("V55","V57")
conectar("V55","V54")
conectar("V54","V47")
conectar("V47","V48")
conectar("V47","V98")
conectar("V48","V50")
conectar("V98","V50")
conectar("V50","V51")
conectar("V48","V49")
conectar("V49","V51")
conectar("V51","V101")
conectar("V101","V52")
conectar("V52","V53")
conectar("V2","V3")
conectar("V3","V101")
conectar("V2","V4")
conectar("V4","V102")
conectar("V102","V5")
conectar("V5","V6")
conectar("V53","V6")
conectar("V6","V7")
conectar("V7","V8")
conectar("V97","V98")
conectar("V4","V9")
conectar("V9","V99")
conectar("V9","V10")
conectar("V9","V46")
conectar("V10","V104")
conectar("V5","V103")
conectar("V104","V11")
conectar("V103","V104")
conectar("V11","V12")
conectar("V12","V13")
conectar("V12","V14")
conectar("V45","V46")
conectar("V45","V12")
conectar("V14","V15")
conectar("V15","V16")
conectar("V16","V105")
conectar("V105","V17")
conectar("V17","V18")
conectar("V18","V19")
conectar("V20","V21")
conectar("V45","V43")
conectar("V43","V44")
conectar("V44","V105")
conectar("V44","V108")
conectar("V108","V100")
conectar("V100","V21")
conectar("V21","V22")
conectar("V22","V109")
conectar("V109","V23")
conectar("V22","V24")
conectar("V24","V25")
conectar("V23","V106")
conectar("V106","V25")
conectar("V24","V26")
conectar("V26","V107")
conectar("V107","V27")
conectar("V27","V28")
conectar("V28","V29")
conectar("V107","V29")
conectar("V29","V30")
conectar("V31","V30")
conectar("V32","V31")
conectar("V32","V33")
conectar("V33","V21")
conectar("V33","V34")
conectar("V34","V35")
conectar("V34","V36")
conectar("V36","V37")
conectar("V38","V36")
conectar("V39","V38")
conectar("V38","V40")
conectar("V40","V41")
conectar("V41","V42")
conectar("V43","V41")
conectar("V108","V38")
conectar("V20","V109")
conectar("V110","V32")
conectar("V110","V31")
conectar("V110","V24")
conectar("V1","Entrada")
conectar("Auditorio", "V60")
conectar("Instituto de Fisica y Matematicas", "V83")
conectar("Division de estudios de posgrado", "V86")
conectar("Centro de Modelacion Matematica", "V111")
conectar("Laboratorio de Tecnología Avanzada y Manufactura", "V73")
conectar("Centro cultural", "V74")
conectar("Laboratorio Quimico Biologico", "V68")
conectar("Instituto de Hidrologia", "V70")
conectar("Instituto de Agroindustrias", "V71")
conectar("Instituto de Mineria", "V72")
conectar("Almacen", "V61")
conectar("Instituto de computacion", "V95")
conectar("Laboratorios de posgrado", "V76")
conectar("Laboratorio de Alimentos", "V77")
conectar("Instituto de electrónica y mecatronica", "V90")
conectar("Taller de plasticos", "V90")
conectar("Instituto de Diseño", "V93")
conectar("Taller de vidrios y textiles", "V91")
conectar("Taller de metales", "V93")
conectar("Taller de maderas", "V93")
conectar("vicerrectoria academica", "V47")
conectar("Servicios Escolares", "V96")
conectar("Rectoria", "V97")
conectar("vicerrectoria administrativa", "V48")
conectar("Instituto de Ingeniería Industrial y Automotriz", "V2")
conectar("Enfermeria", "V2")
conectar("Paraninfo", "V2")
conectar("Sala de computo 01", "V3")
conectar("Sala de computo 02", "V3")
conectar("Sala de computo 03", "V3")
conectar("Sala de computo 04", "V3")
conectar("Sala de computo 05", "V3")
conectar("Sala de computo 06", "V3")
conectar("Instituto de Ciencias Sociales y Humanidades", "V99")
conectar("Centro de EStudios Estrategicos de la EMpresa", "V11")
conectar("Cafeteria chica", "V10")
conectar("Cafeteria chica", "V103")
conectar("Cafeteria grande", "V45")
conectar("Laboratorios de Electronica Avanzados", "V13")
conectar("Instituto de Idiomas", "V14")
conectar("Laboratorio de Idiomas", "V15")
conectar("Sala de Auto Acceso", "V15")
conectar("Sala de computo 07", "V44")
conectar("Sala de computo 08", "V44")
conectar("Sala de computo 09", "V44")
conectar("Sala de computo 10", "V44")
conectar("Sala de computo 11", "V44")
conectar("Sala de computo 12", "V44")
conectar("Planta purificadora de agua", "V43")
conectar("Taller de serigrafia", "V105")
conectar("Laboratorio de Fisica", "V100")
conectar("Laboratorio de matematicas", "V19")
conectar("Biblioteca", "V8")
conectar("Centro de copiado", "V8")
conectar("Aula 01", "V41")
conectar("Aula 02", "V41")
conectar("Aula 03", "V41")
conectar("Aula 04", "V41")
conectar("Aula 05", "V41")
conectar("Aula 06", "V42")
conectar("Aula 07", "V42")
conectar("Aula 08", "V42")
conectar("Aula 09", "V42")
conectar("Aula 10", "V42")
conectar("Aula 11", "V39")
conectar("Aula 12", "V39")
conectar("Aula 13", "V39")
conectar("Aula 14", "V39")
conectar("Aula 15", "V37")
conectar("Aula 16", "V37")
conectar("Aula 17", "V37")
conectar("Aula 18", "V37")
conectar("Aula 19", "V37")
conectar("Aula 20", "V35")
conectar("Aula 21", "V35")
conectar("Aula 22", "V35")
conectar("Aula 23", "V35")
conectar("Aula 24", "V35")
conectar("Aula 25", "V110")
conectar("Aula 26", "V110")
conectar("Aula 27", "V110")
conectar("Aula 28", "V110")
conectar("Aula 29", "V110")
conectar("Aula 30", "V110")
conectar("Aula 31", "V21")
conectar("Aula 32", "V21")
conectar("Aula 33", "V109")
conectar("Aula 34", "V109")
conectar("Aula 35", "V109")
conectar("Aula 36", "V109")
conectar("Aula 37", "V109")
conectar("Aula 38", "V25")
conectar("Aula 39", "V25")
conectar("Aula 40", "V25")
conectar("Aula 41", "V25")
conectar("Aula 42", "V25")
conectar("Aula 43", "V26")
conectar("Aula 44", "V26")
conectar("Aula 45", "V26")
conectar("Aula 46", "V26")
conectar("Aula 47", "V26")
conectar("Aula 48", "V27")
conectar("Aula 49", "V27")
conectar("Aula 50", "V27")
conectar("Aula 51", "V27")
conectar("Aula 52", "V27")
conectar("Aula 53", "V28")
conectar("Aula 54", "V28")
conectar("Aula 55", "V28")
conectar("Aula 56", "V28")
conectar("Aula 57", "V28")
conectar("Sanitario almacen","V61")
conectar("Taller de electronica","V20")
conectar("Salas de dibujo 1-2","V109")
conectar("Laboratorio de sistemas","V17")
conectar("Sala de computo 13","V18")
conectar("Laboratorio de quimica","V17")
conectar("Sanitario VA","V49")
conectar("Sanitario VA","V51")
conectar("Sanitario compu","V101")
conectar("Sanitario A1-5","Aula 05")
conectar("Sanitario A11-14","V39")
conectar("Sanitario A25-30","V110")
conectar("Sanitario A33-37","V23")
conectar("Sanitario LabSis","V18")
conectar("Laboratorio de robotica II","V21")
conectar("V106","Planta de Tratamientos de Aguas residuales por lodos activados")
conectar("V55","V112")
conectar("V112","V113")
conectar("V113","V114")
conectar("V114","V115")
conectar("V115","V116")
conectar("V116","V117")
conectar("V117","Helipuerto")
conectar("V117","V118")
conectar("V118","V119")
conectar("V119","V120")
conectar("V120","V121")
conectar("V121","V122")
conectar("V122","Granja Solar")
conectar("V120","V123")
conectar("V123","V124")
conectar("V124","Vivero")
conectar("V124","Agavetum")
conectar("V123","V125")
conectar("V125","V126")
conectar("V126","V127")
conectar("V127","Taller ingenieria automotriz")
conectar("V127","V128")
conectar("V128","V129")
conectar("V129","V130")
conectar("V130","V131")
conectar("V131","V132")
conectar("V132","V133")
conectar("V133","V134")
conectar("V134","GYM")
conectar("Instituto de ingeniería civil","V129")

# ========== FUNCIONES DE RUTA ==========
def caminito(inicio, fin):
    """Encuentra la ruta más corta entre dos ubicaciones usando Dijkstra"""
    return nx.dijkstra_path(G, inicio, fin, weight="weight")

def crear_mapa_ruta(inicio, fin):
    """Crea un mapa de folium con la ruta más corta entre dos puntos"""
    # Obtener coordenadas
    lat_inicio, lon_inicio = ubicaciones[inicio]
    lat_fin, lon_fin = ubicaciones[fin]

@app.route('/bano_cercano', methods=['POST'])
def bano_cercano():
    """Encuentra el baño más cercano al origen"""
    data = request.get_json()
    origen = data.get('origen')
    
    if not origen:
        return jsonify({'error': 'Faltan parámetros'}), 400
    
    # Lista de todos los sanitarios
    sanitarios = [
        "Sanitario almacen", "Sanitario VA", "Sanitario compu",
        "Sanitario A1-5", "Sanitario A11-14", "Sanitario A25-30",
        "Sanitario A33-37", "Sanitario LabSis"
    ]
    
    # Calcular distancia a cada sanitario
    mejor_bano = None
    mejor_distancia = float('inf')
    
    for bano in sanitarios:
        if bano in G.nodes and origen in G.nodes:
            try:
                distancia = nx.dijkstra_path_length(G, origen, bano, weight="weight")
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_bano = bano
            except nx.NetworkXNoPath:
                continue
    
    if not mejor_bano:
        return jsonify({'error': 'No hay baños accesibles desde este punto'}), 404
    
    # Obtener la ruta
    ruta = nx.dijkstra_path(G, origen, mejor_bano, weight="weight")
    
    # Obtener coordenadas de la ruta
    coordenadas = [ubicaciones[punto] for punto in ruta]
    
    return jsonify({
        'ruta': ruta,
        'coordenadas': coordenadas,
        'distancia': round(mejor_distancia, 2),
        'pasos': len(ruta) - 1,
        'destino': mejor_bano
    })

    # Centrar el mapa
    centro_lat = (lat_inicio + lat_fin) / 2
    centro_lon = (lon_inicio + lon_fin) / 2
    
    # Crear mapa
    mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=18)
    
    # Agregar marcadores de inicio y fin
    folium.Marker(
        [lat_inicio, lon_inicio],
        popup=f"<b>INICIO</b><br>{inicio}",
        tooltip=inicio,
        icon=folium.Icon(color='green', icon='play', prefix='fa')
    ).add_to(mapa)
    
    folium.Marker(
        [lat_fin, lon_fin],
        popup=f"<b>DESTINO</b><br>{fin}",
        tooltip=fin,
        icon=folium.Icon(color='red', icon='flag-checkered', prefix='fa')
    ).add_to(mapa)
    
    # Obtener y dibujar la ruta
    try:
        ruta = caminito(inicio, fin)
        
        # Dibujar cada segmento de la ruta
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            lat1, lon1 = ubicaciones[origen]
            lat2, lon2 = ubicaciones[destino]
            
            folium.PolyLine(
                locations=[[lat1, lon1], [lat2, lon2]],
                color='blue',
                weight=5,
                opacity=0.8,
                popup=f"{origen} → {destino}"
            ).add_to(mapa)
        
        # Guardar la ruta en el mapa como string HTML
        return mapa._repr_html_(), ruta
    except nx.NetworkXNoPath:
        return None, None

# ========== RUTAS DE FLASK ==========
@app.route('/')
def index():
    """Página principal con el menú desplegable"""
    lugares = sorted(ubicaciones.keys())
    return render_template('index.html', lugares=lugares)

@app.route('/ruta', methods=['POST'])
def obtener_ruta():
    """Endpoint para obtener la ruta entre dos lugares"""
    data = request.get_json()
    origen = data.get('origen')
    destino = data.get('destino')
    
    if not origen or not destino:
        return jsonify({'error': 'Faltan parámetros'}), 400
    
    if origen == destino:
        return jsonify({'error': 'El origen y destino son iguales'}), 400
    
    try:
        ruta = nx.dijkstra_path(G, origen, destino, weight="weight")
        distancia_total = nx.dijkstra_path_length(G, origen, destino, weight="weight")
        
        # Obtener coordenadas de cada punto de la ruta
        coordenadas = [ubicaciones[punto] for punto in ruta]
        
        return jsonify({
            'ruta': ruta,
            'coordenadas': coordenadas,
            'distancia': round(distancia_total, 2),
            'pasos': len(ruta) - 1
        })
    except nx.NetworkXNoPath:
        return jsonify({'error': 'No hay ruta disponible entre estos puntos'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Quita debug=True