# ✅ Test CORS Fix - PowerShell

Write-Host "╔═══════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  TEST CORS FIX - Verify API Endpoints           ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n[1] Testing Health Endpoint..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing
    Write-Host "✅ Health: $($response.Content)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health failed: $_" -ForegroundColor Red
}

Write-Host "`n[2] Testing LDAP Login..." -ForegroundColor Cyan
try {
    $body = @{
        username = "student1"
        password = "password"
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/auth/ldap-login `
        -Method POST `
        -Headers @{"Content-Type" = "application/json"} `
        -Body $body `
        -UseBasicParsing
    
    Write-Host "✅ Login OK" -ForegroundColor Green
    $token = $response.Content | ConvertFrom-Json | Select-Object -ExpandProperty access_token
    Write-Host "Token: $($token.substring(0, 30))..." -ForegroundColor Yellow
    
    # Save token for next test
    $global:TOKEN = $token
} catch {
    Write-Host "❌ Login failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n[3] Testing GET /api/tp (NO auth required)..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/tp `
        -Method GET `
        -UseBasicParsing
    
    Write-Host "✅ GET /api/tp: $($response.StatusCode)" -ForegroundColor Green
    $tps = $response.Content | ConvertFrom-Json
    Write-Host "Found TPs: $($tps.Count)" -ForegroundColor Yellow
} catch {
    Write-Host "❌ GET /api/tp failed: $_" -ForegroundColor Red
}

Write-Host "`n[4] Testing GET /api/tp/1 (NO auth required)..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/tp/1 `
        -Method GET `
        -UseBasicParsing
    
    Write-Host "✅ GET /api/tp/1: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ GET /api/tp/1 failed: $_" -ForegroundColor Red
}

Write-Host "`n[5] Testing GET /api/tp/1/guacamole-access (requires JWT)..." -ForegroundColor Cyan
if ($null -eq $TOKEN) {
    Write-Host "⚠️  No token available, skipping..." -ForegroundColor Yellow
} else {
    try {
        $response = Invoke-WebRequest -Uri http://localhost:8000/api/tp/1/guacamole-access `
            -Method GET `
            -Headers @{"Authorization" = "Bearer $TOKEN"} `
            -UseBasicParsing
        
        Write-Host "✅ Guacamole access: $($response.StatusCode)" -ForegroundColor Green
        $guac = $response.Content | ConvertFrom-Json
        Write-Host "Guacamole URL: $($guac.guacamole_url)" -ForegroundColor Yellow
    } catch {
        Write-Host "❌ Guacamole access failed: $_" -ForegroundColor Red
    }
}

Write-Host "`n[6] Testing OPTIONS /api/tp (CORS preflight)..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/tp `
        -Method OPTIONS `
        -UseBasicParsing -ErrorAction SilentlyContinue
    
    Write-Host "✅ CORS preflight: OK" -ForegroundColor Green
    Write-Host "Response headers:" -ForegroundColor Yellow
    $response.Headers | Select-Object -Property "*" | Format-Table -AutoSize
} catch {
    Write-Host "⚠️  CORS preflight test: $_" -ForegroundColor Yellow
}

Write-Host "`n╔═══════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Test Complete!                                   ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════╝" -ForegroundColor Green
