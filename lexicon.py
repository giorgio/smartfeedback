# Léxico en español para el motor de análisis local.
# Todo el procesamiento ocurre en el 'navegador': ningún dato sale del equipo del usuario.

POSITIVE_WORDS = {
  'excelente': 3, 'genial': 2, 'fantástico': 3, 'fantástica': 3, 'maravilloso': 3, 'maravillosa': 3,
  'increíble': 2, 'perfecto': 3, 'perfecta': 3, 'buenísimo': 3, 'buenísima': 3, 'bueno': 1, 'buena': 1,
  'buenos': 1, 'buenas': 1, 'bien': 1, 'rápido': 1, 'rápida': 1, 'eficiente': 2, 'eficaz': 2,
  'amable': 2, 'amables': 2, 'atento': 2, 'atenta': 2, 'atentos': 2, 'profesional': 2, 'profesionales': 2,
  'recomiendo': 2, 'recomendable': 2, 'recomendado': 2, 'satisfecho': 2, 'satisfecha': 2, 'contento': 2,
  'contenta': 2, 'feliz': 2, 'encantado': 2, 'encantada': 2, 'encantados': 2, 'útil': 1, 'fácil': 1,
  'intuitivo': 1, 'intuitiva': 1, 'cómodo': 1, 'cómoda': 1, 'limpio': 1, 'limpia': 1, 'puntual': 2,
  'calidad': 1, 'estupendo': 2, 'estupenda': 2, 'magnífico': 3, 'magnífica': 3, 'impecable': 3,
  'solucionaron': 2, 'solucionó': 2, 'resolvieron': 2, 'resuelto': 2, 'gracias': 1, 'agradecido': 2,
  'agradecida': 2, 'volveré': 2, 'repetiré': 2, 'merece': 1, 'encanta': 2, 'encantó': 2, 'gustó': 1,
  'gusta': 1, 'gustaron': 1, 'sorprendió': 1, 'destacar': 1, 'destacable': 1, 'cumplieron': 1,
  'cumplió': 1, 'económico': 1, 'económica': 1, 'barato': 1, 'barata': 1, 'precio': 0,
}

NEGATIVE_WORDS = {
  'terrible': 3, 'horrible': 3, 'pésimo': 3, 'pésima': 3, 'malísimo': 3, 'malísima': 3, 'malo': 2,
  'mala': 2, 'malos': 2, 'malas': 2, 'mal': 1, 'peor': 2, 'peores': 2, 'lento': 2, 'lenta': 2, 'lentos': 2,
  'lentas': 2, 'tarde': 1, 'retraso': 2, 'retrasos': 2, 'demora': 2, 'demoras': 2, 'espera': 1,
  'esperando': 1, 'error': 2, 'errores': 2, 'falla': 2, 'fallas': 2, 'fallo': 2, 'fallos': 2, 'fallan': 2,
  'roto': 2, 'rota': 2, 'rotos': 2, 'defectuoso': 2, 'defectuosa': 2, 'sucio': 2, 'sucia': 2, 'caro': 2,
  'cara': 2, 'carísimo': 3, 'carísima': 3, 'abusivo': 3, 'abusiva': 3, 'estafa': 3, 'timo': 3, 'engaño': 3,
  'engañaron': 3, 'mentira': 3, 'mienten': 3, 'incompetente': 3, 'incompetentes': 3, 'grosero': 3,
  'grosera': 3, 'maleducado': 3, 'maleducada': 3, 'antipático': 2, 'antipática': 2, 'desastre': 3,
  'desastroso': 3, 'desastrosa': 3, 'caos': 2, 'caótico': 2, 'imposible': 2, 'inútil': 2, 'inservible': 3,
  'decepción': 3, 'decepcionado': 3, 'decepcionada': 3, 'decepcionante': 3, 'frustrante': 2,
  'frustrado': 2, 'frustrada': 2, 'enfadado': 2, 'enfadada': 2, 'enfado': 2, 'indignado': 3,
  'indignada': 3, 'vergüenza': 3, 'vergonzoso': 3, 'vergonzosa': 3, 'inaceptable': 3, 'lamentable': 3,
  'penoso': 3, 'penosa': 3, 'nunca': 1, 'jamás': 2, 'nadie': 1, 'tampoco': 1, 'queja': 2, 'quejas': 2,
  'reclamación': 2, 'reclamar': 2, 'devolución': 1, 'devolver': 1, 'cancelar': 2, 'cancelé': 2,
  'cancelaron': 2, 'cobraron': 1, 'cobran': 1, 'cobro': 1, 'cobros': 1, 'problema': 1, 'problemas': 1,
  'lío': 2, 'líos': 2, 'molesto': 1, 'molesta': 1, 'incómodo': 1, 'incómoda': 1, 'confuso': 1, 'confusa': 1,
  'complicado': 1, 'complicada': 1, 'difícil': 1, 'dificilísimo': 2, 'cuelga': 2, 'cuelgan': 2,
  'bloquea': 2, 'bloquean': 2, 'perdió': 2, 'perdieron': 2, 'perdida': 2, 'perdí': 2, 'desapareció': 2,
}

INTENSIFIERS = set([
  'muy', 'mucho', 'mucha', 'muchísimo', 'muchísima', 'súper', 'super', 'totalmente',
  'completamente', 'absolutamente', 'extremadamente', 'realmente', 'tremendamente',
  'demasiado', 'demasiada', 'bastante', 'tan', 'toda', 'todo', 'siempre', 'nunca', 'jamás',
])

DIMINISHERS = set([
  'poco', 'algo', 'apenas', 'ligeramente', 'levemente', 'medio', 'casi',
])

NEGATIONS = set([
  'no', 'ni', 'tampoco', 'nunca', 'jamás', 'sin', 'nadie', 'nada',
])

URGENCY_WORDS = {
  'urgente': 30, 'urgencia': 30, 'inmediatamente': 25, 'inmediato': 25, 'ya': 10, 'hoy': 10,
  'denuncia': 40, 'denunciar': 40, 'denunciare': 40, 'denunciaré': 40, 'abogado': 35, 'abogados': 35,
  'consumo': 25, 'hoja': 20, 'reclamaciones': 25, 'legal': 25, 'estafa': 35, 'timo': 35, 'fraude': 35,
  'cancelar': 25, 'cancelo': 25, 'cancelaré': 25, 'baja': 20, 'dado': 5, 'competencia': 25,
  'nunca más': 35, 'nunca mas': 35, 'jamás volveré': 35, 'no volveré': 30, 'no vuelvo': 30,
  'vergüenza': 25, 'inaceptable': 25, 'escándalo': 30, 'harto': 30, 'harta': 30, 'hasta aquí': 20,
}


TOPICS = [
  {
    'id': 'precio',
    'label': 'Precio y ofertas',
    'keywords': ['precio', 'precios', 'caro', 'cara', 'carísimo', 'barato', 'barata', 'oferta', 'ofertas', 'descuento', 'descuentos', 'cuesta', 'cuestan', 'vale', 'valen', 'euros', 'euro', 'subido', 'subida', 'rebaja', 'rebajas', 'pagar', 'pagué', 'pago'],
    'action': 'Revisar la política de precios y comunicar mejor ofertas y descuentos vigentes.',
  },
  {
    'id': 'atencion',
    'label': 'Atención al cliente',
    'keywords': ['atención', 'atendieron', 'atendió', 'camarero', 'camarera', 'empleado', 'empleada', 'empleados', 'dependienta', 'dependiente', 'comercial', 'agente', 'operador', 'operadora', 'amable', 'amables', 'grosero', 'grosera', 'maleducado', 'trato', 'antipático', 'educado', 'simpático', 'simpática', 'teléfono', 'llamada', 'llamé', 'contestan', 'contestó', 'responden', 'respondieron'],
    'action': 'Reforzar la formación del equipo de atención y establecer tiempos máximos de respuesta.',
  },
  {
    'id': 'envio',
    'label': 'Envío y entrega',
    'keywords': ['envío', 'envio', 'envíos', 'entrega', 'entregaron', 'entregó', 'llegó', 'llego', 'llegaron', 'paquete', 'paquetería', 'mensajero', 'mensajería', 'repartidor', 'reparto', 'transporte', 'seguimiento', 'almacén', 'pedido llegó'],
    'action': 'Auditar la cadena logística y mejorar la información de seguimiento al cliente.',
  },
  {
    'id': 'calidad',
    'label': 'Calidad del producto',
    'keywords': ['calidad', 'producto', 'productos', 'material', 'materiales', 'acabado', 'acabados', 'roto', 'rota', 'defectuoso', 'defectuosa', 'defecto', 'defectos', 'funciona', 'funcionaba', 'duró', 'dura', 'resistente', 'frágil', 'sabor', 'comida', 'plato', 'platos', 'café', 'carta'],
    'action': 'Revisar el control de calidad y contactar a los clientes con productos defectuosos.',
  },
  {
    'id': 'web',
    'label': 'Web y aplicación',
    'keywords': ['web', 'página', 'pagina', 'app', 'aplicación', 'aplicacion', 'webapp', 'online', 'línea', 'linea', 'registro', 'contraseña', 'login', 'sesión', 'sesion', 'pantalla', 'botón', 'boton', 'carga', 'cargar', 'cuelga', 'bloquea', 'navegar', 'buscador', 'checkout', 'carrito', 'intuitiva', 'usabilidad'],
    'action': 'Priorizar los errores de la web/app más mencionados y simplificar el proceso de compra.',
  },
  {
    'id': 'devoluciones',
    'label': 'Devoluciones y reembolsos',
    'keywords': ['devolución', 'devolucion', 'devolver', 'devolví', 'devolvieron', 'devuelto', 'reembolso', 'reembolsar', 'reembolsaron', 'dinero', 'devuelvan', 'garantía', 'garantia', 'cambio', 'cambiar', 'ticket', 'factura', 'facturación', 'facturacion', 'cobro', 'cobraron', 'cobran', 'cargo'],
    'action': 'Agilizar el proceso de devoluciones y fijar un plazo máximo de reembolso comunicado al cliente.',
  },
  {
    'id': 'tiempos',
    'label': 'Tiempos de espera',
    'keywords': ['espera', 'esperando', 'esperé', 'esperamos', 'cola', 'colas', 'fila', 'tardaron', 'tardó', 'tarda', 'tardan', 'lento', 'lenta', 'lentos', 'retraso', 'retrasos', 'demora', 'demoras', 'horas', 'minutos', 'días', 'semanas', 'turno', 'cita'],
    'action': 'Medir los tiempos reales de servicio y ajustar la planificación de personal en horas punta.',
  },
  {
    'id': 'instalaciones',
    'label': 'Instalaciones y ambiente',
    'keywords': ['local', 'tienda', 'sucursal', 'oficina', 'local', 'limpio', 'limpia', 'sucio', 'sucia', 'baño', 'baños', 'aseo', 'terraza', 'mesa', 'mesas', 'silla', 'sillas', 'ruido', 'música', 'musica', 'temperatura', 'frío', 'frio', 'calor', 'aparcamiento', 'parking', 'acceso', 'espacio'],
    'action': 'Programar mejoras de limpieza y mantenimiento en los puntos más señalados.',
  },
]

STOPWORDS = set([
  'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'a', 'al', 'en', 'con',
  'por', 'para', 'sin', 'sobre', 'entre', 'y', 'o', 'u', 'ni', 'que', 'qué', 'como', 'cómo',
  'pero', 'sino', 'porque', 'pues', 'si', 'sí', 'no', 'se', 'su', 'sus', 'mi', 'mis', 'tu',
  'tus', 'me', 'te', 'le', 'les', 'lo', 'nos', 'os', 'es', 'son', 'fue', 'fueron', 'era',
  'eran', 'ser', 'está', 'están', 'estaba', 'estaban', 'estar', 'estoy', 'estamos', 'ha',
  'han', 'he', 'has', 'haber', 'hay', 'muy', 'más', 'mas', 'ya', 'también', 'tambien',
  'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 'aquel', 'aquella',
  'esto', 'eso', 'todo', 'toda', 'todos', 'todas', 'otro', 'otra', 'otros', 'otras', 'algo',
  'nada', 'mucho', 'mucha', 'poco', 'poca', 'cuando', 'cuándo', 'donde', 'dónde', 'hasta',
  'desde', 'durante', 'cada', 'vez', 'veces', 'así', 'asi', 'entonces', 'además', 'ademas',
  'aunque', 'mientras', 'después', 'despues', 'antes', 'hoy', 'ayer', 'ahora', 'aquí', 'aqui',
  'allí', 'alli', 'hecho', 'hace', 'hacen', 'hacer', 'tener', 'tiene', 'tienen', 'tenía',
  'tenia', 'tenían', 'poder', 'puede', 'pueden', 'pude', 'quería', 'queria', 'quiero',
  'quieren', 'fui', 'fueron', 'voy', 'van', 'iba', 'iban', 'dije', 'dijo', 'dijeron',
  'cliente', 'clientes', 'persona', 'personas', 'gente', 'cosa', 'cosas', 'parte', 'vez',
])
