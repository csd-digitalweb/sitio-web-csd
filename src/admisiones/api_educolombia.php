<?php
/**
 * API Educolombia - Consulta en tiempo real de Admisión y Cupo 2027
 * Colegio Semillero Dos Mil (Corporación Educativa CSD) - csd.edu.co
 * 
 * Uso: Colocar este archivo en la raíz o carpeta de csd.edu.co
 * Ejemplo de llamada: api_educolombia.php?doc=1234342096
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');

$doc = isset($_GET['doc']) ? preg_replace('/[^0-9]/', '', $_GET['doc']) : '';
if (empty($doc)) {
    echo json_encode([
        'admitido' => false,
        'message' => 'Por favor ingrese un número de documento válido.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// 1. Iniciar sesión en educolombia.org
$ch = curl_init('https://educolombia.org/querys/usuarios/login.php');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
    'user' => 'semillerosec',
    'pwd' => 'Semillero2025',
    'hash' => 'frmweb'
]));
curl_setopt($ch, CURLOPT_COOKIEJAR, '');
curl_setopt($ch, CURLOPT_COOKIEFILE, '');
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_exec($ch);

// 2. Descargar reporte 16 de aspirantes/estudiantes
curl_setopt($ch, CURLOPT_URL, 'https://educolombia.org/querys/excel/reportes.php?reporte=16');
curl_setopt($ch, CURLOPT_POST, false);
$csv_data = curl_exec($ch);
curl_close($ch);

if (empty($csv_data)) {
    echo json_encode([
        'admitido' => false,
        'doc' => $doc,
        'motivo' => 'ERROR_CONEXION_EDUCOLOMBIA'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// Mapeo oficial de progresión de grados al 2027
$grade_map = [
    'PREJARDIN' => 'JARDIN',
    'JARDIN' => 'TRANSICION',
    'TRANSICION' => 'PRIMERO',
    'PRIMERO' => 'SEGUNDO',
    'SEGUNDO' => 'TERCERO',
    'TERCERO' => 'CUARTO',
    'CUARTO' => 'QUINTO',
    'QUINTO' => 'SEXTO',
    'SEXTO' => 'SEPTIMO',
    'SEPTIMO' => 'OCTAVO',
    'OCTAVO' => 'NOVENO',
    'NOVENO' => 'DECIMO',
    'DECIMO' => 'UNDECIMO'
];

$lines = explode("\n", $csv_data);
$header = null;
foreach ($lines as $line) {
    $line = trim($line);
    if (empty($line)) continue;
    $row = str_getcsv($line, ';');
    if (!$header) {
        $header = $row;
        continue;
    }
    if (count($row) < count($header)) continue;
    
    $item = array_combine($header, $row);
    if (isset($item['doc']) && trim($item['doc']) === $doc) {
        $salon = trim($item['nombre'] ?? '');
        $nom = trim(($item['nombre1txt'] ?? '') . ' ' . ($item['nombre2'] ?? '') . ' ' . ($item['apellido1txt'] ?? '') . ' ' . ($item['apellido2'] ?? ''));
        $nom = preg_replace('/\s+/', ' ', $nom);
        
        // Condición de admisión: Tiene un salón asignado válido en Educolombia
        if (!empty($salon) && strtoupper($salon) !== 'SIN ASIGNAR') {
            $salon_upper = strtoupper($salon);
            $grado_admitido = $grade_map[$salon_upper] ?? $salon_upper;
            
            echo json_encode([
                'admitido' => true,
                'doc' => $doc,
                'nombre' => $nom,
                'salon' => $salon,
                'grado_2027' => $grado_admitido,
                'acudiente' => 'Acudiente Registrado',
                'doc_acudiente' => '',
                'estado_pago' => 'PENDIENTE'
            ], JSON_UNESCAPED_UNICODE);
            exit;
        } else {
            echo json_encode([
                'admitido' => false,
                'doc' => $doc,
                'nombre' => $nom,
                'motivo' => 'SIN_SALON'
            ], JSON_UNESCAPED_UNICODE);
            exit;
        }
    }
}

// No encontrado en el censo
echo json_encode([
    'admitido' => false,
    'doc' => $doc,
    'motivo' => 'NO_REGISTRADO'
], JSON_UNESCAPED_UNICODE);
?>
