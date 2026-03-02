from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Legal"])


@router.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return """
<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Politica de Privacidad - VibeLink</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6;
               background: #1a1a2e; color: #e0e0e0; }
        h1 { color: #e94560; }
        h2 { color: #00d4ff; margin-top: 30px; }
        a { color: #7bed9f; }
    </style>
</head>
<body>
    <h1>Politica de Privacidad de VibeLink</h1>
    <p><strong>Ultima actualizacion:</strong> Febrero 2024</p>
    <h2>1. Informacion que Recopilamos</h2>
    <p>Recopilamos la informacion que nos proporcionas al registrarte: nombre de usuario, email, fecha de nacimiento y genero. Tambien recopilamos tus preferencias de contenido (peliculas, series y videojuegos que te gustan).</p>
    <h2>2. Como Usamos tu Informacion</h2>
    <p>Usamos tu informacion para: crear y mantener tu cuenta, calcular compatibilidad con otros usuarios, mostrarte contenido relevante y mejorar nuestros servicios.</p>
    <h2>3. Comparticion de Datos</h2>
    <p>No vendemos ni compartimos tu informacion personal con terceros, excepto proveedores de servicios esenciales (hosting, procesamiento de pagos).</p>
    <h2>4. Seguridad</h2>
    <p>Implementamos medidas de seguridad para proteger tu informacion, incluyendo encriptacion de contrasenas y comunicaciones seguras (HTTPS).</p>
    <h2>5. Tus Derechos (RGPD)</h2>
    <p>Tienes derecho a acceder, rectificar, eliminar y portar tus datos personales. Contactanos para ejercer estos derechos.</p>
    <h2>6. Eliminacion de Cuenta</h2>
    <p>Puedes solicitar la eliminacion de tu cuenta y todos los datos asociados contactandonos por email.</p>
    <h2>7. Menores de Edad</h2>
    <p>VibeLink no esta dirigido a menores de 18 anos. No recopilamos intencionadamente informacion de menores.</p>
    <h2>8. Cambios en esta Politica</h2>
    <p>Podemos actualizar esta politica periodicamente. Te notificaremos de cambios significativos.</p>
    <h2>9. Contacto</h2>
    <p>Email: <a href='mailto:ignaciodalesio1995@gmail.com'>ignaciodalesio1995@gmail.com</a></p>
</body>
</html>"""


@router.get("/terms", response_class=HTMLResponse)
async def terms():
    return """
<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Terminos de Uso - VibeLink</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6;
               background: #1a1a2e; color: #e0e0e0; }
        h1 { color: #e94560; }
        h2 { color: #00d4ff; margin-top: 30px; }
        a { color: #7bed9f; }
    </style>
</head>
<body>
    <h1>Terminos de Uso de VibeLink</h1>
    <p><strong>Ultima actualizacion:</strong> Febrero 2024</p>
    <h2>1. Aceptacion de Terminos</h2>
    <p>Al usar VibeLink, aceptas estos terminos de uso. Si no estas de acuerdo, no uses la aplicacion.</p>
    <h2>2. Uso del Servicio</h2>
    <p>VibeLink es una plataforma para conocer personas basada en compatibilidad de gustos en entretenimiento.</p>
    <h2>3. Cuenta de Usuario</h2>
    <p>Eres responsable de mantener la confidencialidad de tu cuenta y contrasena.</p>
    <h2>4. Contenido</h2>
    <p>Te comprometes a no publicar contenido ofensivo, ilegal o que viole los derechos de otros.</p>
    <h2>5. Suscripcion Premium</h2>
    <p>Las funciones premium requieren un pago. Los pagos se procesan a traves de Stripe de forma segura.</p>
    <h2>6. Limitacion de Responsabilidad</h2>
    <p>VibeLink no se responsabiliza de las interacciones entre usuarios fuera de la plataforma.</p>
    <h2>7. Contacto</h2>
    <p>Email: <a href='mailto:ignaciodalesio1995@gmail.com'>ignaciodalesio1995@gmail.com</a></p>
</body>
</html>"""


@router.get("/support", response_class=HTMLResponse)
async def support():
    return """
<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Soporte - VibeLink</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6;
               background: #1a1a2e; color: #e0e0e0; }
        h1 { color: #e94560; }
        h2 { color: #00d4ff; margin-top: 30px; }
        a { color: #7bed9f; }
    </style>
</head>
<body>
    <h1>Soporte - VibeLink</h1>
    <h2>Preguntas Frecuentes</h2>
    <p><strong>Como funciona VibeLink?</strong> VibeLink te conecta con personas que comparten tus gustos en peliculas, series y videojuegos.</p>
    <p><strong>Como se calcula la compatibilidad?</strong> Comparamos tus likes con los de otros usuarios para calcular un porcentaje de compatibilidad.</p>
    <p><strong>Que es Premium?</strong> Con Premium tienes swipes ilimitados para descubrir mas contenido y personas.</p>
    <p><strong>Como elimino mi cuenta?</strong> Contactanos por email y procesaremos tu solicitud.</p>
    <h2>Contacto</h2>
    <p>Email: <a href='mailto:ignaciodalesio1995@gmail.com'>ignaciodalesio1995@gmail.com</a></p>
</body>
</html>"""
